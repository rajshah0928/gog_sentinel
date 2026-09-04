"""
Given a plate number, reconstructs the vehicle's route across the camera
grid: every (camera_id, location, timestamp) where it was detected,
ordered by time. This is the exact capability the live evaluation tests.

Timestamps returned are PTS-derived (per detection, as logged by the ANPR
pipeline) plus the wall-clock time the detection was logged, so the
dashboard can show both "video time" and "when we saw it" without
conflating the two.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from watchlist.db import get_detections_for_plate
from watchlist.matcher import normalize_plate


@dataclass
class RouteStop:
    camera_id: str
    location: str
    pts_ms: float
    wall_clock_s: float
    ocr_confidence: float

    @property
    def wall_clock_iso(self) -> str:
        return datetime.fromtimestamp(self.wall_clock_s, tz=timezone.utc).isoformat()


def reconstruct_route(plate: str) -> list[RouteStop]:
    """
    Returns every detection of `plate`, ordered by wall_clock_s (the time
    our pipeline logged the detection). PTS is per-camera-connection and
    not comparable across different cameras, so it's included per stop for
    within-camera analysis but wall clock is what orders the cross-camera
    route.
    """
    rows = get_detections_for_plate(plate)
    stops = [
        RouteStop(
            camera_id=r["camera_id"],
            location=r["location"],
            pts_ms=r["pts_ms"],
            wall_clock_s=r["wall_clock_s"],
            ocr_confidence=r["ocr_confidence"],
        )
        for r in rows
    ]
    stops.sort(key=lambda s: s.wall_clock_s)
    return stops


def search_plate(query: str) -> list[RouteStop]:
    """Convenience wrapper that normalizes user input before searching."""
    return reconstruct_route(normalize_plate(query))
