"""
Model 1 (Registry & GIS Foundation) persistence layer.

The portal requires every submission to include this foundation regardless
of which primary model is built on top of it. Our primary model is Model 2
(Unified Viewing & Metadata Analytics) — this module adds a minimal,
additive registry on top of data we already collect for capture purposes
(the live camera catalogue from config/ingest_client.py), rather than
building a second, disconnected system.

Two tables, in the same SQLite file as the existing watchlist/detections/
alerts tables (WAL mode, safe for the live capture pipelines to keep
running against the DB while this module is added):

  registry          - one row per known camera: location, an inferred
                       department/camera_type (explicitly illustrative —
                       see registry/inference.py), connectivity + last-seen
                       (both reused from data the pipeline already produces,
                       not re-derived), and a storage_details placeholder
                       describing our actual architecture (feeds are
                       consumed live, never centrally stored by us).
  location_geocode   - cache of location-name -> (lat, lon) lookups so we
                       don't re-hit the geocoder on every dashboard refresh.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from watchlist.db import _connect  # reuse the same DB file/connection pattern

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry (
    camera_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL DEFAULT '',
    department TEXT NOT NULL DEFAULT '',
    camera_type TEXT NOT NULL DEFAULT '',
    connectivity_status TEXT NOT NULL DEFAULT 'unknown',
    last_seen REAL,
    storage_details TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT 'catalogue',
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS location_geocode (
    location TEXT PRIMARY KEY,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    is_approximate INTEGER NOT NULL DEFAULT 1,
    fetched_at REAL NOT NULL
);
"""

DEFAULT_STORAGE_NOTE = (
    "Owned and retained by the respective department's own VMS/gateway — "
    "Sentinel consumes the live feed only and does not centrally store "
    "camera footage."
)


def init_registry_db() -> None:
    """Additive: safe to call alongside watchlist.db.init_db() at any time."""
    with _connect() as conn:
        conn.executescript(SCHEMA)


@dataclass
class RegistryEntry:
    camera_id: str
    display_name: str
    department: str
    camera_type: str
    connectivity_status: str = "unknown"
    last_seen: Optional[float] = None
    storage_details: str = DEFAULT_STORAGE_NOTE
    source: str = "catalogue"


def upsert_registry_entry(entry: RegistryEntry) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO registry (camera_id, display_name, department, camera_type,
                connectivity_status, last_seen, storage_details, source, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(camera_id) DO UPDATE SET
                display_name=excluded.display_name,
                department=excluded.department,
                camera_type=excluded.camera_type,
                connectivity_status=excluded.connectivity_status,
                last_seen=COALESCE(excluded.last_seen, registry.last_seen),
                storage_details=excluded.storage_details,
                source=excluded.source,
                updated_at=excluded.updated_at
            """,
            (
                entry.camera_id, entry.display_name, entry.department, entry.camera_type,
                entry.connectivity_status, entry.last_seen, entry.storage_details,
                entry.source, time.time(),
            ),
        )


def list_registry() -> list:
    with _connect() as conn:
        return conn.execute("SELECT * FROM registry ORDER BY camera_id ASC").fetchall()


def get_registry_entry(camera_id: str):
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM registry WHERE camera_id = ?", (camera_id,)
        ).fetchone()


def update_connectivity(camera_id: str, connected: bool, last_seen: Optional[float] = None) -> None:
    """
    Cheap status-only update, used to refresh connectivity_status/last_seen
    from live capture state without re-running the full catalogue sync.
    """
    with _connect() as conn:
        conn.execute(
            "UPDATE registry SET connectivity_status = ?, last_seen = COALESCE(?, last_seen), "
            "updated_at = ? WHERE camera_id = ?",
            ("connected" if connected else "disconnected", last_seen, time.time(), camera_id),
        )


# --- geocode cache ---------------------------------------------------------

def get_cached_geocode(location: str):
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM location_geocode WHERE location = ?", (location,)
        ).fetchone()


def cache_geocode(location: str, lat: float, lon: float, is_approximate: bool = True) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO location_geocode (location, lat, lon, is_approximate, fetched_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(location) DO UPDATE SET
                lat=excluded.lat, lon=excluded.lon,
                is_approximate=excluded.is_approximate, fetched_at=excluded.fetched_at
            """,
            (location, lat, lon, int(is_approximate), time.time()),
        )


if __name__ == "__main__":
    init_registry_db()
    print("Initialized registry tables.")
