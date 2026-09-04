"""
Orchestration entrypoint: fetches the camera catalogue, opens capture +
ANPR pipelines for a chosen set of cameras, and runs until interrupted.
The dashboard (dashboard/app.py) reads from the same SQLite DB
concurrently — run this and `streamlit run dashboard/app.py` side by side.

Usage:
    SENTINEL_HOST=<host> python main.py --cameras 1,2,3
    SENTINEL_HOST=<host> python main.py --all       # every live camera in the catalogue
"""
from __future__ import annotations

import argparse
import logging
import signal
import sys
import time

from capture.capture_manager import CaptureManager
from analytics.anpr_pipeline import AnprPipeline
from watchlist.db import init_db
from config.settings import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
)
logger = logging.getLogger("sentinel.main")


def main():
    parser = argparse.ArgumentParser(description="Sentinel ANPR pipeline runner")
    parser.add_argument("--cameras", type=str, default="", help="Comma-separated camera ids to process")
    parser.add_argument("--all", action="store_true", help="Process every live camera in the catalogue")
    parser.add_argument("--sample-rate", type=int, default=None, help="Process every Nth frame")
    parser.add_argument("--status-interval", type=float, default=15.0, help="Seconds between status log lines")
    args = parser.parse_args()

    init_db()

    manager = CaptureManager()
    cams = manager.refresh_catalogue()
    if not cams:
        logger.error("Camera catalogue is empty. Check SENTINEL_HOST and gateway connectivity.")
        sys.exit(1)

    if args.all:
        camera_ids = [c.camera_id for c in cams if c.live]
    elif args.cameras:
        camera_ids = [c.strip() for c in args.cameras.split(",") if c.strip()]
    else:
        camera_ids = [c.camera_id for c in cams[:3]]
        logger.info("No --cameras/--all given; defaulting to first 3 catalogue entries: %s", camera_ids)

    pipeline = AnprPipeline(manager)
    for cam_id in camera_ids:
        try:
            pipeline.start_camera(cam_id, sample_rate=args.sample_rate)
            logger.info("Started ANPR for camera %s", cam_id)
        except Exception:
            logger.exception("Failed to start camera %s", cam_id)

    stop = {"flag": False}

    def handle_sigint(signum, frame):
        logger.info("Shutting down...")
        stop["flag"] = True

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    last_status = 0.0
    while not stop["flag"]:
        time.sleep(1.0)
        if time.time() - last_status >= args.status_interval:
            last_status = time.time()
            cap_status = manager.status()
            anpr_status = {s["camera_id"]: s for s in pipeline.status()}
            for cs in cap_status:
                a = anpr_status.get(cs["camera_id"], {})
                logger.info(
                    "STATUS cam=%s connected=%s frames=%d reconnects=%d reads=%d detections=%d",
                    cs["camera_id"], cs["connected"], cs["frames_received"], cs["reconnect_count"],
                    a.get("reads_count", 0), a.get("detections_count", 0),
                )

    pipeline.stop_all()
    manager.close_all()
    logger.info("Stopped cleanly.")


if __name__ == "__main__":
    main()
