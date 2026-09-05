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
from watchlist.matcher import normalize_plate, _confusion_variants


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

    Matches confusion-variant readings of the same plate too (0/O, 1/I,
    5/S, 8/B, 2/Z), not just the exact normalized string — the same real
    vehicle is routinely OCR'd slightly differently across sightings (a
    live sandbox detection of one physical vehicle came back as EV2807,
    8V2807, and BV2807 within 15 seconds), so an exact-only search would
    silently miss real sightings of the vehicle being searched for and
    under-report its route. This mirrors the same fix already applied to
    watchlist matching (watchlist/matcher.py::match_against_watchlist).
    """
    variants = _confusion_variants(plate)
    rows_by_id = {}
    for variant in variants:
        for r in get_detections_for_plate(variant):
            rows_by_id[r["id"]] = r

    stops = [
        RouteStop(
            camera_id=r["camera_id"],
            location=r["location"],
            pts_ms=r["pts_ms"],
            wall_clock_s=r["wall_clock_s"],
            ocr_confidence=r["ocr_confidence"],
        )
        for r in rows_by_id.values()
    ]
    stops.sort(key=lambda s: s.wall_clock_s)
    return stops


def search_plate(query: str) -> list[RouteStop]:
    """Convenience wrapper that normalizes user input before searching."""
    return reconstruct_route(normalize_plate(query))
