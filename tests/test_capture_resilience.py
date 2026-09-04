"""
DoD checks:
  - pipeline connects to 2-3 live cameras simultaneously without crashing
  - sustained run (pass --duration 1200 for a 20 min soak test)
  - reconnect logic: manually kill network/feed mid-run and confirm recovery
    (this script just reports connection state changes; you trigger the
    interruption externally per the DoD's "manually kill/restart a feed")

    source .env.local && python tests/test_capture_resilience.py --duration 1200 --cameras cam01,cam02,cam03
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capture.capture_manager import CaptureManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=120.0, help="Test duration in seconds")
    parser.add_argument("--cameras", type=str, default="", help="Comma-separated camera ids; default = first 3")
    args = parser.parse_args()

    manager = CaptureManager()
    cams = manager.refresh_catalogue()
    assert cams, "Catalogue is empty — check SENTINEL_EMAIL/SENTINEL_PASSWORD"

    camera_ids = [c.strip() for c in args.cameras.split(",") if c.strip()] or [c.camera_id for c in cams[:3]]
    print(f"Opening cameras: {camera_ids}")
    for cam_id in camera_ids:
        manager.open(cam_id)

    start = time.time()
    prev_connected = {cid: None for cid in camera_ids}
    frame_counts = {cid: 0 for cid in camera_ids}

    while time.time() - start < args.duration:
        time.sleep(2.0)
        for status in manager.status():
            cid = status["camera_id"]
            if status["connected"] != prev_connected[cid]:
                print(f"[t={time.time()-start:6.1f}s] camera={cid} connected={status['connected']} "
                      f"reconnects={status['reconnect_count']} last_error={status['last_error']}")
                prev_connected[cid] = status["connected"]
            frame_counts[cid] = status["frames_received"]

    print("\n--- Summary ---")
    for cid in camera_ids:
        print(f"camera={cid}  frames_received={frame_counts[cid]}")
        assert frame_counts[cid] > 0, f"camera {cid} received zero frames over the test duration"

    manager.close_all()
    print("OK: all cameras received frames; no crash over the test duration")


if __name__ == "__main__":
    main()
