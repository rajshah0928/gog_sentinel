"""
SQLite-backed watchlist + alert log.

Two tables:
  watchlist   - representative "wanted vehicle" entries we create ourselves
                (plate, reason/category, date added)
  detections  - every OCR read above threshold, tied to camera + PTS-derived
                timestamp; this is also what route reconstruction (trace/)
                queries against
  alerts      - a detections row that matched a watchlist entry
"""
from __future__ import annotations

import os
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

from config.settings import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'wanted',
    date_added REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT NOT NULL,
    camera_id TEXT NOT NULL,
    location TEXT NOT NULL DEFAULT '',
    pts_ms REAL NOT NULL,
    wall_clock_s REAL NOT NULL,
    ocr_confidence REAL NOT NULL,
    detector_confidence REAL NOT NULL DEFAULT 0.0,
    raw_ocr_text TEXT NOT NULL DEFAULT '',
    crop_path TEXT,
    annotated_frame_path TEXT
);
CREATE INDEX IF NOT EXISTS idx_detections_plate ON detections(plate);
CREATE INDEX IF NOT EXISTS idx_detections_camera ON detections(camera_id);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detection_id INTEGER NOT NULL REFERENCES detections(id),
    watchlist_id INTEGER NOT NULL REFERENCES watchlist(id),
    plate TEXT NOT NULL,
    camera_id TEXT NOT NULL,
    location TEXT NOT NULL DEFAULT '',
    pts_ms REAL NOT NULL,
    wall_clock_s REAL NOT NULL,
    match_confidence REAL NOT NULL,
    reason TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at DESC);
"""


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # allow concurrent dashboard reads + pipeline writes
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """
    Creates the DB file (if absent) with owner-only permissions before
    SQLite opens it — this holds watchlist entries and live detection
    history, sensitive by nature of this project, on a shared host. Only
    fixes the mode on first creation; an existing file's permissions are
    left as whatever an operator has already set.
    """
    is_new = not os.path.exists(DB_PATH)
    if is_new:
        fd = os.open(DB_PATH, os.O_WRONLY | os.O_CREAT, 0o600)
        os.close(fd)
    with _connect() as conn:
        conn.executescript(SCHEMA)
        _migrate_add_image_columns(conn)


def _migrate_add_image_columns(conn: sqlite3.Connection) -> None:
    """
    Additive migration for a DB created before crop/annotated-frame image
    persistence existed. ALTER TABLE ADD COLUMN is safe to run against a
    live WAL-mode DB that other processes (the running capture pipelines)
    have open — existing INSERTs that don't reference the new columns stay
    valid, and this only ever adds nullable columns, never rewrites data.
    """
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(detections)")}
    if "crop_path" not in existing_cols:
        conn.execute("ALTER TABLE detections ADD COLUMN crop_path TEXT")
    if "annotated_frame_path" not in existing_cols:
        conn.execute("ALTER TABLE detections ADD COLUMN annotated_frame_path TEXT")


# --- watchlist -----------------------------------------------------------

def add_watchlist_entry(plate: str, reason: str, category: str = "wanted") -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO watchlist (plate, reason, category, date_added) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(plate) DO UPDATE SET reason=excluded.reason, category=excluded.category",
            (plate.upper().strip(), reason, category, time.time()),
        )
        return cur.lastrowid


def list_watchlist() -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute("SELECT * FROM watchlist ORDER BY date_added DESC").fetchall()


def remove_watchlist_entry(plate: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM watchlist WHERE plate = ?", (plate.upper().strip(),))


# --- detections ------------------------------------------------------------

@dataclass
class DetectionRecord:
    plate: str
    camera_id: str
    location: str
    pts_ms: float
    ocr_confidence: float
    detector_confidence: float = 0.0
    raw_ocr_text: str = ""
    crop_path: Optional[str] = None
    annotated_frame_path: Optional[str] = None


def log_detection(rec: DetectionRecord) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO detections (plate, camera_id, location, pts_ms, wall_clock_s, "
            "ocr_confidence, detector_confidence, raw_ocr_text, crop_path, annotated_frame_path) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                rec.plate, rec.camera_id, rec.location, rec.pts_ms, time.time(),
                rec.ocr_confidence, rec.detector_confidence, rec.raw_ocr_text,
                rec.crop_path, rec.annotated_frame_path,
            ),
        )
        return cur.lastrowid


def get_detections_for_plate(plate: str) -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM detections WHERE plate = ? ORDER BY pts_ms ASC",
            (plate.upper().strip(),),
        ).fetchall()


def recent_detections(limit: int = 100) -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM detections ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()


def get_detection(detection_id: int) -> Optional[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM detections WHERE id = ?", (detection_id,)
        ).fetchone()


def update_detection_images(
    detection_id: int, crop_path: Optional[str] = None, annotated_frame_path: Optional[str] = None,
) -> None:
    """
    Attaches image paths to an already-logged detection. Separate from
    log_detection() rather than an extra argument to it, since the crop/
    frame files are written to disk (by dashboard/evidence_capture.py)
    after the detection row already exists and has an id to name the
    files after.
    """
    with _connect() as conn:
        if crop_path is not None:
            conn.execute("UPDATE detections SET crop_path = ? WHERE id = ?", (crop_path, detection_id))
        if annotated_frame_path is not None:
            conn.execute(
                "UPDATE detections SET annotated_frame_path = ? WHERE id = ?",
                (annotated_frame_path, detection_id),
            )


def last_seen_per_camera() -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            """
            SELECT d.camera_id, d.location, d.plate, d.pts_ms, d.wall_clock_s,
                   d.ocr_confidence, d.crop_path, d.annotated_frame_path
            FROM detections d
            JOIN (
                SELECT camera_id, MAX(id) AS max_id FROM detections GROUP BY camera_id
            ) latest ON d.camera_id = latest.camera_id AND d.id = latest.max_id
            ORDER BY d.wall_clock_s DESC
            """
        ).fetchall()


# --- alerts ------------------------------------------------------------------

def log_alert(
    detection_id: int, watchlist_id: int, plate: str, camera_id: str, location: str,
    pts_ms: float, match_confidence: float, reason: str, category: str,
) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO alerts (detection_id, watchlist_id, plate, camera_id, location, "
            "pts_ms, wall_clock_s, match_confidence, reason, category, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                detection_id, watchlist_id, plate, camera_id, location, pts_ms,
                time.time(), match_confidence, reason, category, time.time(),
            ),
        )
        return cur.lastrowid


def recent_alerts(limit: int = 100) -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()


if __name__ == "__main__":
    init_db()
    print(f"Initialized DB at {DB_PATH}")
