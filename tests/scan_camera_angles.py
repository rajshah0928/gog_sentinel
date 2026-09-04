"""
One-off reconnaissance script: opens every camera in the catalogue briefly
(in small batches, per the "pace your load" integration rule), saves one
frame each, and reports plate-detector confidence on each frame. Used to
identify which cameras in the grid have close/low enough framing for ANPR
to actually be viable, vs wide-area junction cameras where plates are not
resolvable at any zoom.

Usage: python tests/scan_camera_angles.py [--out-dir DIR] [--batch-size 5]

Note: this script's rapid open/close-many-cameras-in-one-process pattern has
triggered a rare SIGABRT at interpreter exit (native FFmpeg/OpenCV teardown
race, not reproducible on demand, occurred once in ~4 runs) after all scan
results were already printed — so it doesn't lose data, but don't be
surprised by a nonzero exit code after the ranked results appear. This
pattern is diagnostic-only; main.py's actual usage (open a small fixed
camera set once, hold it for the run) does not exhibit this.
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from capture.capture_manager import CaptureManager
from analytics.plate_detector import PlateDetector

logging.basicConfig(level=logging.ERROR)  # suppress decoder warning spam for this scan


def scan(out_dir: Path, batch_size: int, settle_s: float):
    out_dir.mkdir(parents=True, exist_ok=True)
    manager = CaptureManager()
    cams = manager.refresh_catalogue()
    detector = PlateDetector(conf_threshold=0.1)

    results = []
    for i in range(0, len(cams), batch_size):
        batch = cams[i:i + batch_size]
        cam_ids = [c.camera_id for c in batch]
        print(f"Batch {i//batch_size + 1}: opening {cam_ids}")
        for c in batch:
            manager.open(c.camera_id)

        time.sleep(settle_s)

        for c in batch:
            frame = manager.get_frame(c.camera_id, timeout_s=3.0)
            if frame is None:
                print(f"  {c.camera_id} ({c.location}): NO FRAME")
                results.append((c.camera_id, c.location, -1, 0))
                continue
            path = out_dir / f"{c.camera_id}.jpg"
            cv2.imwrite(str(path), frame.image)
            boxes = detector.detect(frame.image)
            max_conf = max((b.confidence for b in boxes), default=0.0)
            print(f"  {c.camera_id} ({c.location}): {len(boxes)} candidates, max_conf={max_conf:.3f}")
            results.append((c.camera_id, c.location, max_conf, len(boxes)))

        for c in batch:
            manager.close(c.camera_id)

    print("\n--- Ranked by plate-detector confidence ---")
    for cam_id, loc, conf, n in sorted(results, key=lambda r: -r[2]):
        print(f"{cam_id:>6}  conf={conf:6.3f}  candidates={n}  {loc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=str, default="/tmp/sentinel_camera_scan")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--settle-s", type=float, default=9.0, help="Seconds to wait after opening a batch before grabbing frames")
    args = parser.parse_args()
    scan(Path(args.out_dir), args.batch_size, args.settle_s)
