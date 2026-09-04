"""
DoD check: a known test plate, when injected into the watchlist, produces a
correctly logged alert with correct camera_id and timestamp when it appears
on a feed.

This does NOT fabricate a detection. The Sentinel sandbox is a remote camera
grid we don't control traffic on, so there is no way to physically place a
vehicle in front of a camera — instead, seed the watchlist with a plate
already seen in the detections table (from a prior main.py run), then run
main.py again and confirm a real, independent detection of that same plate
produces a correctly logged alert.

Usage:
    1. Run main.py for a while, then check `recent_detections()` (or the
       dashboard) for any real plate it already read, e.g. GJ05AB1234.
    2. python tests/test_alert_e2e.py seed GJ05AB1234
    3. In another terminal: source .env.local && python main.py --cameras <id>
    4. python tests/test_alert_e2e.py wait GJ05AB1234 --timeout 300
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from watchlist.db import init_db, add_watchlist_entry, recent_alerts


def cmd_seed(plate: str):
    init_db()
    add_watchlist_entry(plate, "E2E test entry", "wanted")
    print(f"Seeded watchlist with test plate {plate}")


def cmd_wait(plate: str, timeout: float):
    init_db()
    plate = plate.upper().strip()
    start = time.time()
    print(f"Waiting up to {timeout}s for an alert on plate {plate}...")
    while time.time() - start < timeout:
        for a in recent_alerts(limit=50):
            if a["plate"] == plate:
                print("OK: alert found")
                print(f"  camera_id={a['camera_id']}  location={a['location']}  "
                      f"pts_ms={a['pts_ms']}  match_confidence={a['match_confidence']}")
                return
        time.sleep(2.0)
    print(f"FAIL: no alert for {plate} within {timeout}s")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_seed = sub.add_parser("seed")
    p_seed.add_argument("plate")
    p_wait = sub.add_parser("wait")
    p_wait.add_argument("plate")
    p_wait.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args()

    if args.cmd == "seed":
        cmd_seed(args.plate)
    elif args.cmd == "wait":
        cmd_wait(args.plate, args.timeout)
