"""
License plate bounding-box detection using a YOLOv8n-class model fine-tuned
for plates. We do not train from scratch — this wraps a pretrained weights
file (path from config.settings.PLATE_DETECTOR_MODEL_PATH). See
analytics/models/README.md for where those weights come from.
"""
from __future__ import annotations

import logging
import threading
from dataclasses import dataclass

import numpy as np

from config.settings import PLATE_DETECTOR_MODEL_PATH, PLATE_DETECTOR_CONF_THRESHOLD

logger = logging.getLogger("sentinel.plate_detector")


@dataclass
class PlateBox:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float

    def crop(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        x1, y1 = max(0, self.x1), max(0, self.y1)
        x2, y2 = min(w, self.x2), min(h, self.y2)
        return frame[y1:y2, x1:x2]


class PlateDetector:
    """
    Lazily loads the YOLO model (deferred import + weight load are slow).
    A single instance is shared across per-camera worker threads in
    AnprPipeline, so both lazy init and inference are serialized with a
    lock — ultralytics' YOLO.predict() is not documented as safe for
    concurrent calls from multiple threads on one model instance, and an
    unlocked lazy-init check-then-set would let two threads race to
    construct the model on first use.
    """

    def __init__(self, model_path: str = None, conf_threshold: float = None):
        self._model_path = model_path or PLATE_DETECTOR_MODEL_PATH
        self._conf_threshold = conf_threshold or PLATE_DETECTOR_CONF_THRESHOLD
        self._model = None
        self._lock = threading.Lock()

    def _ensure_model(self):
        if self._model is None:
            from ultralytics import YOLO
            logger.info("Loading plate detector weights from %s", self._model_path)
            self._model = YOLO(self._model_path)
        return self._model

    def detect(self, frame_bgr: np.ndarray) -> list[PlateBox]:
        """Single-pass detection on the whole frame, downscaled to the model's input size."""
        return self._detect_region(frame_bgr, x_offset=0, y_offset=0)

    def detect_tiled(
        self, frame_bgr: np.ndarray, tile_size: int = 640, overlap: float = 0.2,
    ) -> list[PlateBox]:
        """
        Splits the frame into overlapping tile_size x tile_size tiles and
        runs detection on each at full resolution, merging results back to
        full-frame coordinates. A plate that's a handful of pixels wide in
        a 1920x1080 frame gets downscaled to near-nothing by a single
        whole-frame pass (YOLO resizes its input to a fixed size, e.g.
        640x640) — tiling keeps far-away small objects at native resolution
        within their tile, at the cost of running the model multiple times
        per frame. Use only on cameras/sample rates where the extra CPU
        cost is affordable; not a fit for every camera in the grid.
        """
        h, w = frame_bgr.shape[:2]
        stride = int(tile_size * (1 - overlap))
        all_boxes: list[PlateBox] = []

        y = 0
        while y < h:
            x = 0
            tile_h = min(tile_size, h - y)
            while x < w:
                tile_w = min(tile_size, w - x)
                tile = frame_bgr[y:y + tile_h, x:x + tile_w]
                boxes = self._detect_region(tile, x_offset=x, y_offset=y)
                all_boxes.extend(boxes)
                if x + tile_w >= w:
                    break
                x += stride
            if y + tile_h >= h:
                break
            y += stride

        return _merge_overlapping_boxes(all_boxes)

    def _detect_region(self, region_bgr: np.ndarray, x_offset: int, y_offset: int) -> list[PlateBox]:
        with self._lock:
            model = self._ensure_model()
            results = model.predict(
                region_bgr, conf=self._conf_threshold, verbose=False,
            )
        boxes: list[PlateBox] = []
        for r in results:
            if r.boxes is None:
                continue
            for b in r.boxes:
                x1, y1, x2, y2 = [int(v) for v in b.xyxy[0].tolist()]
                conf = float(b.conf[0])
                boxes.append(PlateBox(
                    x1=x1 + x_offset, y1=y1 + y_offset,
                    x2=x2 + x_offset, y2=y2 + y_offset,
                    confidence=conf,
                ))
        return boxes


def _merge_overlapping_boxes(boxes: list[PlateBox], iou_threshold: float = 0.3) -> list[PlateBox]:
    """
    Simple greedy NMS across tile boundaries: overlapping tiles can produce
    duplicate detections for the same plate near a seam. Keeps the
    highest-confidence box in each overlapping cluster.
    """
    if not boxes:
        return []
    boxes_sorted = sorted(boxes, key=lambda b: -b.confidence)
    kept: list[PlateBox] = []
    for box in boxes_sorted:
        if all(_iou(box, k) < iou_threshold for k in kept):
            kept.append(box)
    return kept


def _iou(a: PlateBox, b: PlateBox) -> float:
    ix1, iy1 = max(a.x1, b.x1), max(a.y1, b.y1)
    ix2, iy2 = min(a.x2, b.x2), min(a.y2, b.y2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area_a = (a.x2 - a.x1) * (a.y2 - a.y1)
    area_b = (b.x2 - b.x1) * (b.y2 - b.y1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0
