"""
Populates the registry table from the live camera catalogue we already fetch
for capture purposes (config.ingest_client) — no manual entry of 30 cameras.

Called from main.py at startup (one extra call, doesn't touch capture/
detection logic) and from the dashboard on load (cheap: just re-upserts
rows from the already-cached catalogue).
"""
from __future__ import annotations

import logging

from config.ingest_client import get_catalogue, CameraInfo
from registry.db import RegistryEntry, upsert_registry_entry, init_registry_db, DEFAULT_STORAGE_NOTE
from registry.inference import infer_department, infer_camera_type

logger = logging.getLogger("sentinel.registry.sync")


def sync_registry_from_catalogue(prefer_cache: bool = True) -> int:
    """
    Upserts one registry row per camera in the live/cached catalogue.
    Returns the number of cameras synced. Safe to call repeatedly — this is
    idempotent (ON CONFLICT upsert), and connectivity/last_seen here reflect
    only "known to the catalogue," not live capture state; pair with
    registry.db.update_connectivity() (fed by the running pipeline's own
    status) for real-time connectivity.
    """
    init_registry_db()
    try:
        cams: list[CameraInfo] = get_catalogue(prefer_cache=prefer_cache)
    except Exception as e:
        logger.warning("Registry sync: catalogue fetch failed (%s)", e)
        return 0

    for cam in cams:
        camera_type = infer_camera_type(cam.location)
        department = infer_department(cam.location, camera_type)
        upsert_registry_entry(
            RegistryEntry(
                camera_id=cam.camera_id,
                display_name=cam.location,
                department=department,
                camera_type=camera_type,
                connectivity_status="unknown",
                last_seen=None,
                storage_details=DEFAULT_STORAGE_NOTE,
                source="catalogue",
            )
        )
    logger.info("Registry synced: %d cameras from catalogue", len(cams))
    return len(cams)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    n = sync_registry_from_catalogue(prefer_cache=False)
    print(f"Synced {n} cameras into the registry.")
