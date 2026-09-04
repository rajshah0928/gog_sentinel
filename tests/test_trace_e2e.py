"""
DoD check: end-to-end trace test — pick one plate, confirm the system can
show it appearing across 2+ different cameras with correct timestamps and
locations, in order.

Usage (after running main.py against multiple cameras long enough to log
detections for the same real plate on 2+ of them):
    python tests/test_trace_e2e.py GJ05AB1234
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from vehicle_trace.route_reconstruction import search_plate


def main():
    if len(sys.argv) != 2:
        print("Usage: python tests/test_trace_e2e.py <PLATE>")
        sys.exit(1)

    plate = sys.argv[1]
    stops = search_plate(plate)

    if not stops:
        print(f"FAIL: no detections found for {plate}")
        sys.exit(1)

    cameras_seen = {s.camera_id for s in stops}
    print(f"Route for {plate}: {len(stops)} detection(s) across {len(cameras_seen)} camera(s)")
    for s in stops:
        print(f"  {s.wall_clock_iso}  camera={s.camera_id}  location={s.location!r}  "
              f"pts_ms={s.pts_ms:.0f}  ocr_conf={s.ocr_confidence:.2f}")

    if len(cameras_seen) >= 2:
        print("OK: plate traced across 2+ distinct cameras")
    else:
        print("PARTIAL: plate only seen on a single camera so far — need more coverage for full DoD pass")


if __name__ == "__main__":
    main()
