"""
Saves visual evidence (plate crops + annotated full frames) for the
dashboard's detection/alert views. Presentation-layer support only — does
not affect detection, OCR, matching, or alerting logic. Called as a side
effect after a detection is already confirmed (see
analytics/anpr_pipeline.py's single additive call site).

Images are written under dashboard/evidence_images/, organized by camera,
so they can be served directly by Streamlit without a separate file server.
Crops are cheap (a few KB each) and saved for every detection. Annotated
full frames are larger, so we keep only a small rolling number per camera
rather than one per detection, to avoid unbounded disk growth on a long
unattended run.
"""
from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger("sentinel.evidence_capture")

EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence_images"
CROPS_DIR = EVIDENCE_DIR / "crops"
FRAMES_DIR = EVIDENCE_DIR / "frames"

MAX_ANNOTATED_FRAMES_PER_CAMERA = 5

_lock = threading.Lock()
_frame_counters: dict[str, int] = {}


def _ensure_dirs() -> None:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)


def save_crop(camera_id: str, detection_id: int, crop_bgr: np.ndarray) -> Optional[str]:
    """
    Saves a plate crop to disk, returns the path (relative to EVIDENCE_DIR)
    to store in the detections table, or None on failure (never raises —
    a failed image save should not break the detection pipeline itself).
    """
    if crop_bgr is None or crop_bgr.size == 0:
        return None
    try:
        _ensure_dirs()
        filename = f"{camera_id}_{detection_id}.jpg"
        path = CROPS_DIR / filename
        cv2.imwrite(str(path), crop_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return f"crops/{filename}"
    except Exception:
        logger.exception("Failed to save plate crop for detection %s", detection_id)
        return None


def save_annotated_frame(
    camera_id: str, detection_id: int, frame_bgr: np.ndarray,
    box_x1: int, box_y1: int, box_x2: int, box_y2: int,
    plate_text: str, ocr_confidence: float,
) -> Optional[str]:
    """
    Draws the plate bounding box + OCR text/confidence on a copy of the
    full frame and saves it, keeping only the most recent
    MAX_ANNOTATED_FRAMES_PER_CAMERA per camera (deletes the oldest when
    the cap is exceeded) so a long-running pipeline doesn't fill disk with
    full-resolution frames — one recent example per camera is enough to
    show "here is the AI's bounding box on a real frame."
    """
    if frame_bgr is None or frame_bgr.size == 0:
        return None
    try:
        _ensure_dirs()
        annotated = frame_bgr.copy()
        cv2.rectangle(annotated, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 3)
        label = f"{plate_text} ({ocr_confidence:.2f})"
        label_y = max(box_y1 - 12, 20)
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
        cv2.rectangle(
            annotated, (box_x1, label_y - text_h - 8), (box_x1 + text_w + 8, label_y + 4),
            (0, 255, 0), -1,
        )
        cv2.putText(
            annotated, label, (box_x1 + 4, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2,
        )

        filename = f"{camera_id}_{detection_id}.jpg"
        path = FRAMES_DIR / filename
        cv2.imwrite(str(path), annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])

        with _lock:
            _prune_old_frames(camera_id, keep_filename=filename)

        return f"frames/{filename}"
    except Exception:
        logger.exception("Failed to save annotated frame for detection %s", detection_id)
        return None


def _prune_old_frames(camera_id: str, keep_filename: str) -> None:
    existing = sorted(
        FRAMES_DIR.glob(f"{camera_id}_*.jpg"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for old_path in existing[MAX_ANNOTATED_FRAMES_PER_CAMERA:]:
        if old_path.name != keep_filename:
            try:
                old_path.unlink()
            except OSError:
                pass


def latest_annotated_frame(camera_id: str) -> Optional[Path]:
    """Returns the most recent annotated-frame path for a camera, if any."""
    candidates = sorted(
        FRAMES_DIR.glob(f"{camera_id}_*.jpg"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None
