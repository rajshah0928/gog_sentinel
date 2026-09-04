"""
Central configuration for the Sentinel unified viewing/analytics prototype.
Everything host-specific or tunable lives here, sourced from environment
variables so the same code runs against the sandbox, a demo host, or local
test footage without edits.
"""
import os
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Sentinel sandbox gateway -----------------------------------------------
# HLS is served over a CDN host (works from anywhere, password-gated).
# RTSP/WHEP carry raw TCP/UDP media that a CDN can't proxy, so they connect
# directly to a public static IP and require email:password embedded in the
# URL (the @ in the email must be percent-encoded as %40).
SENTINEL_HLS_HOST = os.environ.get("SENTINEL_HLS_HOST", "cctv.corp8.cloud")
SENTINEL_RTSP_HOST = os.environ.get("SENTINEL_RTSP_HOST", "103.250.160.189")
SENTINEL_RTSP_PORT = os.environ.get("SENTINEL_RTSP_PORT", "8554")
SENTINEL_WHEP_PORT = os.environ.get("SENTINEL_WHEP_PORT", "8889")

SENTINEL_EMAIL = os.environ.get("SENTINEL_EMAIL", "")
SENTINEL_PASSWORD = os.environ.get("SENTINEL_PASSWORD", "")

_ENCODED_EMAIL = quote(SENTINEL_EMAIL, safe="") if SENTINEL_EMAIL else ""
_ENCODED_PASSWORD = quote(SENTINEL_PASSWORD, safe="") if SENTINEL_PASSWORD else ""
_CREDS = f"{_ENCODED_EMAIL}:{_ENCODED_PASSWORD}@" if SENTINEL_EMAIL and SENTINEL_PASSWORD else ""

CAMERAS_JSON_URL = f"https://{SENTINEL_HLS_HOST}/cameras.json"
RTSP_URL_TEMPLATE = f"rtsp://{_CREDS}{SENTINEL_RTSP_HOST}:{SENTINEL_RTSP_PORT}/stream/{{cam_id}}"
WHEP_URL_TEMPLATE = f"http://{_CREDS}{SENTINEL_RTSP_HOST}:{SENTINEL_WHEP_PORT}/stream/{{cam_id}}/whep"
HLS_URL_TEMPLATE = f"https://{SENTINEL_HLS_HOST}/{{cam_id}}/index.m3u8"

# --- Capture layer tuning ---------------------------------------------------
RECONNECT_BACKOFF_START_S = 2.0
RECONNECT_BACKOFF_CAP_S = 30.0
RTSP_TRANSPORT = "tcp"  # non-negotiable per integration rules

# --- ANPR pipeline tuning ---------------------------------------------------
# Process every Nth frame for CPU feasibility. Configurable per deployment.
FRAME_SAMPLE_RATE = int(os.environ.get("FRAME_SAMPLE_RATE", "5"))
PLATE_DETECTOR_CONF_THRESHOLD = float(os.environ.get("PLATE_CONF_THRESHOLD", "0.4"))
OCR_CONF_THRESHOLD = float(os.environ.get("OCR_CONF_THRESHOLD", "0.4"))
PLATE_DETECTOR_MODEL_PATH = os.environ.get(
    "PLATE_DETECTOR_MODEL_PATH", str(BASE_DIR / "analytics" / "models" / "plate_yolov8n.pt")
)
# Tiled detection re-runs the model per-tile at native resolution instead of
# one downscaled whole-frame pass, trading CPU cost for better recall on
# small/distant plates (wide-angle junction cameras). Off by default since
# it multiplies inference cost per sampled frame; enable per-deployment once
# a camera's traffic distance profile justifies it.
PLATE_DETECTOR_USE_TILING = os.environ.get("PLATE_DETECTOR_USE_TILING", "false").lower() == "true"
PLATE_DETECTOR_TILE_SIZE = int(os.environ.get("PLATE_DETECTOR_TILE_SIZE", "640"))
PLATE_DETECTOR_TILE_OVERLAP = float(os.environ.get("PLATE_DETECTOR_TILE_OVERLAP", "0.2"))

# --- Storage -----------------------------------------------------------------
DB_PATH = os.environ.get("SENTINEL_DB_PATH", str(BASE_DIR / "watchlist" / "sentinel.db"))
CAMERA_CACHE_PATH = str(BASE_DIR / "config" / "camera_cache.json")

# --- Misc --------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
