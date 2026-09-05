"""
OCR on cropped plate regions using PaddleOCR.

Switched from EasyOCR after head-to-head testing on real sandbox footage:
on a genuinely legible plate crop (toll-plaza camera, close-range truck),
EasyOCR topped out around 0.2-0.4 confidence on partial fragments across
extensive preprocessing tuning (scale sweeps, unsharp masking, threshold
tuning), while PaddleOCR (PP-OCRv6) read the full plate at 0.87 confidence
on the same source crop, no special preprocessing beyond upscaling.

Requires enable_mkldnn=False — with MKL-DNN acceleration on, PaddleOCR's
text detector crashes on this host with a native oneDNN/PIR runtime error
(NotImplementedError: ConvertPirAttribute2RuntimeAttribute...). Pure-CPU
inference without MKL-DNN is slower but actually works; given our frame
sample rate this tradeoff is fine.
"""
from __future__ import annotations

import logging
import re
import threading
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger("sentinel.ocr")


@dataclass
class OcrResult:
    text: str
    confidence: float  # 0.0-1.0


class PlateOCR:
    """
    Lazily initializes PaddleOCR (loads model weights on first use). A
    single instance is shared across per-camera worker threads in
    AnprPipeline, so both lazy init and inference are serialized with a
    lock — the underlying paddle model is not documented as safe for
    concurrent calls from multiple threads on one instance.
    """

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._reader = None
        self._lock = threading.Lock()

    def _ensure_reader(self):
        if self._reader is None:
            from paddleocr import PaddleOCR  # deferred import: slow to load
            logger.info("Loading PaddleOCR reader (lang=%s)", self._lang)
            self._reader = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                lang=self._lang,
                enable_mkldnn=False,
            )
        return self._reader

    def read_plate(self, plate_crop_bgr: np.ndarray) -> Optional[OcrResult]:
        """
        Runs OCR on a cropped plate image (BGR, as produced by OpenCV crop).
        Returns the highest-confidence alphanumeric read, or None if nothing
        usable was found.
        """
        if plate_crop_bgr is None or plate_crop_bgr.size == 0:
            return None

        preprocessed = _preprocess_for_ocr(plate_crop_bgr)

        with self._lock:
            reader = self._ensure_reader()
            results = list(reader.predict(preprocessed))

        if not results:
            return None

        texts: list[str] = []
        scores: list[float] = []
        for r in results:
            texts.extend(r.get("rec_texts", []))
            scores.extend(r.get("rec_scores", []))

        if not texts:
            return None

        text = "".join(texts)
        text = re.sub(r"[^A-Z0-9]", "", text.upper())
        avg_conf = sum(scores) / len(scores) if scores else 0.0

        if not text:
            return None
        return OcrResult(text=text, confidence=avg_conf)


def _preprocess_for_ocr(crop_bgr: np.ndarray) -> np.ndarray:
    """
    Upscales small crops (plates are often small in a wide CCTV frame).
    Kept in color, not grayscale+CLAHE — testing showed CLAHE on small,
    JPEG-noisy crops amplified block artifacts more than it helped text
    edges; PaddleOCR's own preprocessing handles contrast internally.
    """
    h, w = crop_bgr.shape[:2]
    target_h = 240  # empirically the scale that worked in testing (~6x on a ~40px source)
    if h < target_h:
        scale = target_h / max(h, 1)
        crop_bgr = cv2.resize(
            crop_bgr, (int(w * scale), target_h), interpolation=cv2.INTER_LANCZOS4,
        )
    return crop_bgr
