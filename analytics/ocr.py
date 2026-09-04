"""
OCR on cropped plate regions using EasyOCR.

EasyOCR is chosen over PaddleOCR here for simpler CPU-only install (pure
pip, no paddle wheel headaches) and adequate accuracy on plate-sized crops;
swap in PaddleOCR by changing only this module if it proves clearly better
in demo testing.
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

_ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


@dataclass
class OcrResult:
    text: str
    confidence: float  # 0.0-1.0


class PlateOCR:
    """
    Lazily initializes EasyOCR's reader (loads model weights on first use).
    A single instance is shared across per-camera worker threads in
    AnprPipeline, so both lazy init and inference are serialized with a
    lock, for the same reason as PlateDetector: avoid a racy double-init
    and concurrent calls into the underlying torch model from multiple
    threads.
    """

    def __init__(self, languages: list[str] = None, gpu: bool = False):
        self._languages = languages or ["en"]
        self._gpu = gpu
        self._reader = None
        self._lock = threading.Lock()

    def _ensure_reader(self):
        if self._reader is None:
            import easyocr  # deferred import: loading torch/easyocr is slow
            logger.info("Loading EasyOCR reader (languages=%s, gpu=%s)", self._languages, self._gpu)
            self._reader = easyocr.Reader(self._languages, gpu=self._gpu)
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
            results = reader.readtext(
                preprocessed,
                allowlist=_ALLOWED_CHARS,
                detail=1,
                paragraph=False,
            )
        if not results:
            return None

        # Multiple text fragments can appear (state code split from number,
        # e.g. "GJ 05" / "AB 1234") - concatenate in reading order (left to
        # right by box x-position) and average confidence.
        results.sort(key=lambda r: r[0][0][0])  # sort by top-left x of box
        text = "".join(r[1] for r in results)
        text = re.sub(r"[^A-Z0-9]", "", text.upper())
        avg_conf = sum(r[2] for r in results) / len(results)

        if not text:
            return None
        return OcrResult(text=text, confidence=avg_conf)


def _preprocess_for_ocr(crop_bgr: np.ndarray) -> np.ndarray:
    """
    Upscales small crops (plates are often small in a wide CCTV frame) and
    applies light contrast normalization to help OCR on low-quality footage.
    """
    h, w = crop_bgr.shape[:2]
    target_h = 64
    if h < target_h:
        scale = target_h / max(h, 1)
        crop_bgr = cv2.resize(crop_bgr, (int(w * scale), target_h), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    return gray
