"""
Per-camera ANPR pipeline: pulls frames from a CameraCapture, samples every
Nth frame (configurable, for CPU feasibility), runs plate detection + OCR,
filters by confidence, and logs every read as a detection. Watchlist
matching is triggered on each detection (see watchlist/alerting.py).
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Optional

from capture.capture_manager import CaptureManager
from analytics.plate_detector import PlateDetector
from analytics.ocr import PlateOCR
from config.settings import (
    FRAME_SAMPLE_RATE,
    OCR_CONF_THRESHOLD,
    PLATE_DETECTOR_USE_TILING,
    PLATE_DETECTOR_TILE_SIZE,
    PLATE_DETECTOR_TILE_OVERLAP,
)
from watchlist.db import DetectionRecord, log_detection, update_detection_images
from watchlist.alerting import process_detection_for_alerts
from dashboard.evidence_capture import save_crop, save_annotated_frame

logger = logging.getLogger("sentinel.anpr_pipeline")


class AnprWorker:
    """
    Runs ANPR for a single camera in a background thread: pulls the latest
    frame from CaptureManager, processes every Nth frame it sees (not every
    Nth wall-clock tick — sampling is frame-count based, so it naturally
    adapts to whatever irregular delivery rate the feed actually has).
    """

    def __init__(
        self,
        capture_manager: CaptureManager,
        camera_id: str,
        detector: PlateDetector,
        ocr: PlateOCR,
        sample_rate: int = None,
    ):
        self.capture_manager = capture_manager
        self.camera_id = camera_id
        self.detector = detector
        self.ocr = ocr
        self.sample_rate = sample_rate or FRAME_SAMPLE_RATE

        self._thread: Optional[threading.Thread] = None
        self._running = threading.Event()
        self._frame_counter = 0
        self._last_seen_pts: Optional[float] = None

        self.reads_count = 0
        self.detections_count = 0

    def start(self) -> "AnprWorker":
        self.capture_manager.open(self.camera_id)
        self._running.set()
        self._thread = threading.Thread(target=self._run, name=f"anpr-{self.camera_id}", daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        self._running.clear()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

    def _run(self) -> None:
        cam = None
        try:
            from config.ingest_client import get_camera
            cam = get_camera(self.camera_id, prefer_cache=True)
        except Exception:
            pass
        location = cam.location if cam else ""

        while self._running.is_set():
            frame_obj = self.capture_manager.get_frame(self.camera_id, timeout_s=2.0)
            if frame_obj is None:
                continue

            # Skip frames we've already processed (get_frame can return the
            # same latest frame repeatedly if the worker outpaces delivery).
            if self._last_seen_pts is not None and frame_obj.pts_ms == self._last_seen_pts:
                time.sleep(0.02)
                continue
            self._last_seen_pts = frame_obj.pts_ms

            self._frame_counter += 1
            if self._frame_counter % self.sample_rate != 0:
                continue

            try:
                self._process_frame(frame_obj, location)
            except Exception:
                logger.exception("[%s] frame processing failed", self.camera_id)

    def _process_frame(self, frame_obj, location: str) -> None:
        if PLATE_DETECTOR_USE_TILING:
            boxes = self.detector.detect_tiled(
                frame_obj.image, tile_size=PLATE_DETECTOR_TILE_SIZE, overlap=PLATE_DETECTOR_TILE_OVERLAP,
            )
        else:
            boxes = self.detector.detect(frame_obj.image)
        for box in boxes:
            crop = box.crop(frame_obj.image)
            ocr_result = self.ocr.read_plate(crop)
            self.reads_count += 1
            if ocr_result is None or ocr_result.confidence < OCR_CONF_THRESHOLD:
                continue

            self.detections_count += 1
            rec = DetectionRecord(
                plate=ocr_result.text,
                camera_id=self.camera_id,
                location=location,
                pts_ms=frame_obj.pts_ms,
                ocr_confidence=ocr_result.confidence,
                detector_confidence=box.confidence,
                raw_ocr_text=ocr_result.text,
            )
            detection_id = log_detection(rec)
            logger.info(
                "[%s] plate read: %s (ocr_conf=%.2f, det_conf=%.2f, pts=%.0fms)",
                self.camera_id, ocr_result.text, ocr_result.confidence, box.confidence, frame_obj.pts_ms,
            )

            # Visual evidence for the dashboard — a side effect on an
            # already-confirmed detection, never affects detection/OCR/
            # matching. Failures here are logged and swallowed inside
            # evidence_capture itself, so a disk/image error can't break
            # the detection pipeline.
            crop_path = save_crop(self.camera_id, detection_id, crop)
            annotated_path = save_annotated_frame(
                self.camera_id, detection_id, frame_obj.image,
                box.x1, box.y1, box.x2, box.y2,
                ocr_result.text, ocr_result.confidence,
            )
            if crop_path or annotated_path:
                update_detection_images(detection_id, crop_path, annotated_path)

            process_detection_for_alerts(detection_id, rec)


class AnprPipeline:
    """Owns one shared detector/OCR pair (expensive to load) across multiple per-camera workers."""

    def __init__(self, capture_manager: CaptureManager):
        self.capture_manager = capture_manager
        self.detector = PlateDetector()
        self.ocr = PlateOCR()
        self._workers: dict[str, AnprWorker] = {}

    def start_camera(self, camera_id: str, sample_rate: int = None) -> AnprWorker:
        if camera_id in self._workers:
            return self._workers[camera_id]
        worker = AnprWorker(
            self.capture_manager, camera_id, self.detector, self.ocr, sample_rate=sample_rate,
        )
        worker.start()
        self._workers[camera_id] = worker
        return worker

    def stop_camera(self, camera_id: str) -> None:
        worker = self._workers.pop(camera_id, None)
        if worker is not None:
            worker.stop()
        self.capture_manager.close(camera_id)

    def stop_all(self) -> None:
        for camera_id in list(self._workers.keys()):
            self.stop_camera(camera_id)

    def status(self) -> list[dict]:
        return [
            {
                "camera_id": cam_id,
                "reads_count": w.reads_count,
                "detections_count": w.detections_count,
            }
            for cam_id, w in self._workers.items()
        ]
