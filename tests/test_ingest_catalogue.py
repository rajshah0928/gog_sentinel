"""
DoD check: camera list/properties are read dynamically from cameras.json,
not hardcoded. Run once SENTINEL_EMAIL/SENTINEL_PASSWORD are set.

    source .env.local && python tests/test_ingest_catalogue.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.ingest_client import fetch_camera_catalogue


def main():
    cams = fetch_camera_catalogue()
    assert len(cams) > 0, "Catalogue returned zero cameras"
    print(f"OK: fetched {len(cams)} cameras from cameras.json")
    for c in cams[:5]:
        print(f"  {c.camera_id}  location={c.location!r}")
        assert c.rtsp_url, f"camera {c.camera_id} missing rtsp_url"
    print("OK: rtsp_url present on sampled cameras")


if __name__ == "__main__":
    main()
