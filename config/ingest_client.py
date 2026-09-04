"""
Client for the Sentinel gateway's camera catalogue: GET https://<hls-host>/cameras.json.
This is the single source of truth for camera ids (cam01...cam30) and their
display names — nothing downstream should hardcode a camera id. Stream URLs
(RTSP/WHEP/HLS) are built from the templates in config.settings, which embed
the registered email/password credentials required by RTSP & WHEP.

The catalogue endpoint sits behind a browser-style session login (POST
/auth/login with email+password sets a `sentinel` session cookie) rather
than HTTP basic auth. This module logs in once and reuses the session.

Results are cached to disk so the dashboard/tools can inspect the catalogue
without hitting the gateway repeatedly.
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, asdict
from typing import Optional

import requests

from config.settings import (
    SENTINEL_HLS_HOST,
    CAMERAS_JSON_URL,
    SENTINEL_EMAIL,
    SENTINEL_PASSWORD,
    RTSP_URL_TEMPLATE,
    WHEP_URL_TEMPLATE,
    HLS_URL_TEMPLATE,
    CAMERA_CACHE_PATH,
)

logger = logging.getLogger("sentinel.ingest_client")

LOGIN_URL = f"https://{SENTINEL_HLS_HOST}/auth/login"

_session: Optional[requests.Session] = None


@dataclass
class CameraInfo:
    camera_id: str
    location: str
    codec: str
    live: bool
    rtsp_url: str
    whep_url: str
    hls_url: str
    extra: dict


def _get_authenticated_session(timeout_s: float = 10.0) -> requests.Session:
    """
    Logs in once (POST /auth/login with email+password) and caches the
    resulting session (holds the `sentinel` cookie) for reuse across calls
    within this process.
    """
    global _session
    if _session is not None:
        return _session

    if not SENTINEL_EMAIL or not SENTINEL_PASSWORD:
        raise RuntimeError(
            "SENTINEL_EMAIL / SENTINEL_PASSWORD are not set. Export both "
            "(the registered sandbox access credentials) before fetching "
            "the camera catalogue or opening any stream."
        )

    s = requests.Session()
    resp = s.post(
        LOGIN_URL,
        data={"email": SENTINEL_EMAIL, "password": SENTINEL_PASSWORD},
        timeout=timeout_s,
    )
    resp.raise_for_status()
    if "sentinel" not in s.cookies:
        raise RuntimeError(
            "Sentinel login did not return a session cookie — check "
            "SENTINEL_EMAIL/SENTINEL_PASSWORD (server said: "
            f"{'incorrect credentials' if 'incorrect' in resp.text else 'unknown error'})."
        )
    _session = s
    logger.info("Authenticated to Sentinel gateway as %s", SENTINEL_EMAIL)
    return s


def _extract_camera(raw: dict) -> CameraInfo:
    """
    Normalizes one cameras.json entry into a CameraInfo. Confirmed live
    payload shape is just {"id": "cam01", "name": "01 Chiman bhai Bridge"}
    — codec/live-status aren't advertised by the catalogue, so those default
    to unknown/assumed-live; per-camera codec is instead discovered from the
    stream itself when opened.
    """
    cam_id = str(raw.get("id") or raw.get("camera_id") or raw.get("cam_id") or raw.get("stream_id"))
    location = raw.get("name") or raw.get("location") or raw.get("site") or ""
    codec = raw.get("codec") or raw.get("video_codec") or ""
    live = bool(raw["live"]) if "live" in raw else bool(raw.get("status", "live") == "live") if "status" in raw else True

    rtsp_url = RTSP_URL_TEMPLATE.format(cam_id=cam_id)
    whep_url = WHEP_URL_TEMPLATE.format(cam_id=cam_id)
    hls_url = HLS_URL_TEMPLATE.format(cam_id=cam_id)

    known = {
        "id", "camera_id", "cam_id", "stream_id", "location", "name", "site",
        "codec", "video_codec", "live", "status",
    }
    extra = {k: v for k, v in raw.items() if k not in known}

    return CameraInfo(
        camera_id=cam_id,
        location=location,
        codec=codec,
        live=live,
        rtsp_url=rtsp_url,
        whep_url=whep_url,
        hls_url=hls_url,
        extra=extra,
    )


def fetch_camera_catalogue(timeout_s: float = 10.0) -> list[CameraInfo]:
    """
    Hits GET cameras.json (authenticated session) and returns the
    normalized camera list. Raises on network/HTTP/auth failure — callers
    decide whether to fall back to cache.
    """
    session = _get_authenticated_session(timeout_s=timeout_s)
    resp = session.get(CAMERAS_JSON_URL, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()

    raw_cameras = payload if isinstance(payload, list) else payload.get("cameras", payload.get("data", []))
    cameras = [_extract_camera(c) for c in raw_cameras]

    _write_cache(cameras)
    logger.info("Fetched %d cameras from %s", len(cameras), CAMERAS_JSON_URL)
    return cameras


def _write_cache(cameras: list[CameraInfo]) -> None:
    """
    Cached CameraInfo entries embed each camera's RTSP/WHEP URL, which
    carries the sandbox email:password as plaintext credentials — this
    machine is shared, so the cache file is created with owner-only
    permissions rather than the default (typically world-readable) mode.
    """
    fd = os.open(CAMERA_CACHE_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"fetched_at": time.time(), "cameras": [asdict(c) for c in cameras]}, f, indent=2)


def load_cached_catalogue() -> list[CameraInfo]:
    with open(CAMERA_CACHE_PATH) as f:
        data = json.load(f)
    return [CameraInfo(**c) for c in data["cameras"]]


def get_catalogue(prefer_cache: bool = False) -> list[CameraInfo]:
    """
    Convenience accessor: tries a live fetch first (catalogue can change),
    falling back to the last cached copy if the gateway is unreachable.
    Pass prefer_cache=True to skip the network call entirely (fast dev loop).
    """
    if prefer_cache:
        try:
            return load_cached_catalogue()
        except FileNotFoundError:
            pass
    try:
        return fetch_camera_catalogue()
    except Exception as e:
        logger.warning("Live catalogue fetch failed (%s); falling back to cache", e)
        return load_cached_catalogue()


def get_camera(camera_id: str, prefer_cache: bool = False) -> Optional[CameraInfo]:
    for cam in get_catalogue(prefer_cache=prefer_cache):
        if cam.camera_id == str(camera_id):
            return cam
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cams = fetch_camera_catalogue()
    for c in cams:
        print(f"{c.camera_id:>6}  {c.location}")
