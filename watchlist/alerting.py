"""
Wires a logged detection to watchlist matching and, on a match, writes an
alert row. Called synchronously from the ANPR pipeline right after each
detection is logged — matching a single plate against a small watchlist is
cheap enough not to need its own queue/worker for this prototype's scale.
"""
from __future__ import annotations

import logging

from watchlist.db import DetectionRecord, log_alert
from watchlist.matcher import match_against_watchlist

logger = logging.getLogger("sentinel.alerting")


def process_detection_for_alerts(detection_id: int, rec: DetectionRecord) -> None:
    match = match_against_watchlist(rec.plate)
    if match is None:
        return

    alert_id = log_alert(
        detection_id=detection_id,
        watchlist_id=match.watchlist_id,
        plate=rec.plate,
        camera_id=rec.camera_id,
        location=rec.location,
        pts_ms=rec.pts_ms,
        match_confidence=match.confidence,
        reason=match.reason,
        category=match.category,
    )
    logger.warning(
        "ALERT #%d: plate=%s matched watchlist entry '%s' (%s) at camera=%s location=%s pts=%.0fms conf=%.1f",
        alert_id, rec.plate, match.watchlist_plate, match.reason, rec.camera_id, rec.location,
        rec.pts_ms, match.confidence,
    )
