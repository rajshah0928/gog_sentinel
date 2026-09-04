"""
Manages a pool of CameraCapture instances, opening only the cameras
currently being processed and closing ones that are done — per integration
rule "pace your load" (don't hold all ~50 RTSP connections open at once).
"""
from __future__ import annotations

import logging
from typing import Optional

from capture.rtsp_capture import CameraCapture, Frame
from config.ingest_client import get_catalogue, CameraInfo

logger = logging.getLogger("sentinel.capture_manager")


class CaptureManager:
    def __init__(self):
        self._captures: dict[str, CameraCapture] = {}
        self._catalogue_by_id: dict[str, CameraInfo] = {}

    def refresh_catalogue(self, prefer_cache: bool = False) -> list[CameraInfo]:
        cams = get_catalogue(prefer_cache=prefer_cache)
        self._catalogue_by_id = {c.camera_id: c for c in cams}
        return cams

    def list_cameras(self) -> list[CameraInfo]:
        if not self._catalogue_by_id:
            self.refresh_catalogue()
        return list(self._catalogue_by_id.values())

    def open(self, camera_id: str) -> CameraCapture:
        if camera_id in self._captures:
            return self._captures[camera_id]

        cam = self._catalogue_by_id.get(camera_id)
        if cam is None:
            self.refresh_catalogue()
            cam = self._catalogue_by_id.get(camera_id)
        if cam is None:
            raise KeyError(f"Unknown camera_id={camera_id!r}; not present in /api/ingest catalogue")
        if not cam.rtsp_url:
            raise ValueError(f"camera_id={camera_id!r} has no rtsp_url in catalogue")

        cap = CameraCapture(camera_id=camera_id, rtsp_url=cam.rtsp_url, name=f"cam-{camera_id}")
        cap.start()
        self._captures[camera_id] = cap
        logger.info("Opened capture for camera %s (%s)", camera_id, cam.location)
        return cap

    def close(self, camera_id: str) -> None:
        cap = self._captures.pop(camera_id, None)
        if cap is not None:
            cap.stop()
            logger.info("Closed capture for camera %s", camera_id)

    def close_all(self) -> None:
        for camera_id in list(self._captures.keys()):
            self.close(camera_id)

    def get_frame(self, camera_id: str, timeout_s: float = 2.0) -> Optional[Frame]:
        cap = self._captures.get(camera_id)
        if cap is None:
            raise KeyError(f"camera_id={camera_id!r} is not open; call open() first")
        return cap.get_frame(timeout_s=timeout_s)

    def active_camera_ids(self) -> list[str]:
        return list(self._captures.keys())

    def status(self) -> list[dict]:
        out = []
        for cam_id, cap in self._captures.items():
            out.append({
                "camera_id": cam_id,
                "connected": cap.connected,
                "frames_received": cap.frames_received,
                "reconnect_count": cap.reconnect_count,
                "last_error": cap.last_error,
            })
        return out
