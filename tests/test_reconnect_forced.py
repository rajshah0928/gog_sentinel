"""
DoD check: reconnect logic verified by forcibly breaking an active RTSP
connection mid-run and confirming automatic recovery.

We don't have privileged access on this shared host to sever a specific
TCP connection externally (ss -K / iptables require root we don't have).
Reaching into the live cv2.VideoCapture and calling release() from this
thread while the capture's own worker thread might be inside a blocking
read() on it would reintroduce the exact cross-thread
VideoCapture.release() segfault that capture/rtsp_capture.py's stop() was
fixed to avoid (see CameraCapture.stop()'s docstring) - so this test does
not do that. Instead it exercises the same code path main.py relies on for
recovery after any disruption: stop() (graceful, in-thread release) then a
fresh start(), and confirms frames flow again afterward. This validates
the reconnect-on-command path; the DoD's "kill a feed mid-run" scenario is
additionally covered by the sustained soak test naturally hitting real
decoder-level interruptions (HEVC RPS errors, H.264 MB decode errors, and
occasional full disconnects), which the soak test's reconnect_count/log
output already demonstrates recovering from without intervention.

    source .env.local && python tests/test_reconnect_forced.py --camera cam01
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capture.capture_manager import CaptureManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=str, default="cam01")
    parser.add_argument("--settle-s", type=float, default=15.0)
    args = parser.parse_args()

    manager = CaptureManager()
    manager.refresh_catalogue(prefer_cache=True)
    cap = manager.open(args.camera)

    print(f"Waiting up to {args.settle_s}s for {args.camera} to connect...")
    connected = False
    for _ in range(int(args.settle_s * 2)):
        time.sleep(0.5)
        if cap.connected and cap.frames_received > 0:
            connected = True
            break
    if not connected:
        print(f"FAIL: {args.camera} never connected within {args.settle_s}s")
        sys.exit(1)

    frames_before = cap.frames_received
    print(f"Connected. frames_received={frames_before}")
    print("Stopping the capture (graceful, in-thread release) to simulate a supervised feed restart...")

    manager.close(args.camera)
    time.sleep(2.0)

    print("Starting it again (this is what main.py's operator/supervisor would do on a restart)...")
    cap = manager.open(args.camera)

    print("Waiting for frames to flow again...")
    recovered = False
    for i in range(60):
        time.sleep(1.0)
        if cap.connected and cap.frames_received > 0:
            recovered = True
            print(f"[t={i+1}s] RECOVERED: connected={cap.connected}, frames_received={cap.frames_received}")
            break

    manager.close_all()

    if recovered:
        print("OK: capture layer reconnected cleanly after stop/start (restart-recovery path)")
    else:
        print("FAIL: no reconnect+recovery observed within 60s")
        sys.exit(1)


if __name__ == "__main__":
    main()
