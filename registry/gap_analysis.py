"""
Gap-analysis queries for the Registry tab: which cameras are silent, which
are disconnected, and which categories of camera are ANPR-viable vs
situational-only. All of this reads from data we already have (registry +
detections) — no new tracking state.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from watchlist.db import _connect
from registry.inference import is_anpr_viable_type

STALE_HOURS_DEFAULT = 6.0


@dataclass
class GapAnalysis:
    total_cameras: int
    disconnected_count: int
    disconnected_ids: list[str]
    stale_count: int
    stale_ids: list[str]
    stale_hours_threshold: float
    by_type: dict  # camera_type -> {"count": int, "anpr_viable": bool, "with_detections": int}


def compute_gap_analysis(stale_hours: float = STALE_HOURS_DEFAULT) -> GapAnalysis:
    now = time.time()
    stale_cutoff = now - stale_hours * 3600

    with _connect() as conn:
        registry_rows = conn.execute("SELECT * FROM registry").fetchall()
        last_detection_by_cam = {
            row["camera_id"]: row["max_wc"]
            for row in conn.execute(
                "SELECT camera_id, MAX(wall_clock_s) AS max_wc FROM detections GROUP BY camera_id"
            ).fetchall()
        }

    disconnected_ids = [r["camera_id"] for r in registry_rows if r["connectivity_status"] == "disconnected"]

    stale_ids = []
    for r in registry_rows:
        last_wc = last_detection_by_cam.get(r["camera_id"])
        if last_wc is None or last_wc < stale_cutoff:
            stale_ids.append(r["camera_id"])

    by_type: dict[str, dict] = {}
    for r in registry_rows:
        ctype = r["camera_type"] or "unknown"
        bucket = by_type.setdefault(ctype, {"count": 0, "anpr_viable": is_anpr_viable_type(ctype), "with_detections": 0})
        bucket["count"] += 1
        if last_detection_by_cam.get(r["camera_id"]):
            bucket["with_detections"] += 1

    return GapAnalysis(
        total_cameras=len(registry_rows),
        disconnected_count=len(disconnected_ids),
        disconnected_ids=sorted(disconnected_ids),
        stale_count=len(stale_ids),
        stale_ids=sorted(stale_ids),
        stale_hours_threshold=stale_hours,
        by_type=dict(sorted(by_type.items())),
    )
