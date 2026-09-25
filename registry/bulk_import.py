"""
CSV bulk-import for onboarding cameras not present in the live gateway
catalogue (e.g. a department's own camera added out-of-band). Demonstrates
the registry-onboarding pattern required by Model 1 — this only needs to
show a working import function against a sample file, not be exercised
against real new cameras.

Expected CSV columns (header row required):
    camera_id,display_name,department,camera_type,storage_details

department/camera_type/storage_details are optional per row — left blank,
department/camera_type fall back to the same inference used for the live
catalogue (registry.inference), and storage_details falls back to the
default placeholder note.
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path

from registry.db import RegistryEntry, upsert_registry_entry, init_registry_db, DEFAULT_STORAGE_NOTE
from registry.inference import infer_department, infer_camera_type

logger = logging.getLogger("sentinel.registry.bulk_import")

REQUIRED_COLUMNS = {"camera_id", "display_name"}


def import_cameras_csv(csv_path: str | Path) -> tuple[int, list[str]]:
    """
    Imports cameras from a CSV file into the registry. Returns
    (rows_imported, errors) — errors are per-row messages for rows that were
    skipped, not raised, so one bad row doesn't abort the whole import.
    """
    init_registry_db()
    csv_path = Path(csv_path)
    errors: list[str] = []
    imported = 0

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"CSV must have at least columns {sorted(REQUIRED_COLUMNS)}; "
                f"found {reader.fieldnames}"
            )
        for i, row in enumerate(reader, start=2):  # start=2: header is row 1
            camera_id = (row.get("camera_id") or "").strip()
            display_name = (row.get("display_name") or "").strip()
            if not camera_id or not display_name:
                errors.append(f"Row {i}: missing camera_id or display_name, skipped")
                continue

            camera_type = (row.get("camera_type") or "").strip() or infer_camera_type(display_name)
            department = (row.get("department") or "").strip() or infer_department(display_name, camera_type)
            storage_details = (row.get("storage_details") or "").strip() or DEFAULT_STORAGE_NOTE

            upsert_registry_entry(
                RegistryEntry(
                    camera_id=camera_id,
                    display_name=display_name,
                    department=department,
                    camera_type=camera_type,
                    connectivity_status="unknown",
                    last_seen=None,
                    storage_details=storage_details,
                    source="csv_import",
                )
            )
            imported += 1

    logger.info("CSV import: %d cameras imported from %s (%d errors)", imported, csv_path, len(errors))
    return imported, errors


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m registry.bulk_import <path/to/cameras.csv>")
        sys.exit(1)
    logging.basicConfig(level=logging.INFO)
    n, errs = import_cameras_csv(sys.argv[1])
    print(f"Imported {n} cameras.")
    for e in errs:
        print(f"  {e}")
