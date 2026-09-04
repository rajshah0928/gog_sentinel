"""
Resilient per-camera RTSP capture.

One CameraCapture instance owns one camera's RTSP connection. It force-TCPs
the transport, timestamps every frame from PTS (never wall clock, never
declared FPS), reconnects with exponential backoff on failure/EOF, tolerates
decoder warnings during join, and survives the hard scene-cut each looping
sandbox feed produces.

Usage:
    cap = CameraCapture(camera_id="1", rtsp_url="rtsp://host:8554/stream/1")
    cap.start()
    frame, pts_ms, camera_id = cap.get_frame(timeout_s=2.0)
    ...
    cap.stop()
"""
from __future__ import annotations

import logging
import os
import re
import threading
import time
from dataclasses import dataclass
from typing import Optional

# Must be set before any cv2.VideoCapture(..., CAP_FFMPEG) call is made,
# so it is set at import time here rather than deep inside connect().
os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

import cv2  # noqa: E402

from config.settings import RECONNECT_BACKOFF_START_S, RECONNECT_BACKOFF_CAP_S

logger = logging.getLogger("sentinel.capture")

_CREDS_RE = re.compile(r"://[^/@]+@")


def _redact_url(url: str) -> str:
    """Strips embedded email:password credentials before a URL is logged."""
    return _CREDS_RE.sub("://***:***@", url)


@dataclass
class Frame:
    image: "cv2.Mat"
    pts_ms: float
    camera_id: str
    wall_clock_s: float  # arrival time, kept only for logging/latency metrics


class CameraCapture:
    """
    Runs a background thread that keeps one camera's RTSP stream open,
    continuously reading frames into a 1-slot "latest frame" buffer (we want
    the freshest frame for live inference, not a backlog) and reconnecting
    on any failure.
    """

    def __init__(self, camera_id: str, rtsp_url: str, name: Optional[str] = None):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.name = name or f"cam-{camera_id}"

        self._cap: Optional[cv2.VideoCapture] = None
        self._thread: Optional[threading.Thread] = None
        self._running = threading.Event()
        self._lock = threading.Lock()
        self._latest: Optional[Frame] = None
        self._new_frame_event = threading.Event()

        # Track PTS across a scene-cut/reconnect: a fresh connection's PTS
        # clock restarts near zero, which would otherwise look like a huge
        # negative jump to any downstream consumer computing PTS deltas.
        self._last_pts_ms: Optional[float] = None
        self._pts_offset_ms: float = 0.0

        self.connected = False
        self.last_error: Optional[str] = None
        self.frames_received = 0
        self.reconnect_count = 0

    # -- lifecycle -----------------------------------------------------

    def start(self) -> "CameraCapture":
        if self._thread is not None:
            return self
        self._running.set()
        self._thread = threading.Thread(target=self._run, name=self.name, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        """
        Signals the worker thread to stop and waits for it to exit. The
        actual cv2.VideoCapture.release() always happens inside the worker
        thread itself (_run/_release_capture), never here — releasing a
        VideoCapture from a different thread than the one blocked inside
        its read() call is a known OpenCV/FFmpeg segfault (release() frees
        the underlying AVFormatContext while read() is still using it).
        If the worker is stuck in a blocking read() past the join timeout,
        we deliberately leave the capture object alone rather than force a
        cross-thread release; the daemon thread will clean up once read()
        eventually returns (EOF/timeout/error) and observes _running clear.
        """
        self._running.clear()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                logger.warning(
                    "[%s] worker thread did not exit within timeout (likely "
                    "blocked in a native read()); leaving it as a daemon to "
                    "unwind on its own rather than risk a cross-thread "
                    "VideoCapture.release()", self.name,
                )
            self._thread = None
        logger.info("[%s] stopped", self.name)

    # -- consumer interface ---------------------------------------------

    def get_frame(self, timeout_s: float = 2.0) -> Optional[Frame]:
        """
        Returns the most recent frame, waiting up to timeout_s for one if
        none has arrived yet. Returns None on timeout (caller should treat
        this as "no frame right now", not as a fatal error).
        """
        if self._new_frame_event.wait(timeout=timeout_s):
            with self._lock:
                self._new_frame_event.clear()
                return self._latest
        with self._lock:
            return self._latest

    # -- internals --------------------------------------------------------

    def _run(self) -> None:
        backoff_s = RECONNECT_BACKOFF_START_S
        while self._running.is_set():
            try:
                connected_ok = self._connect()
            except Exception as e:
                connected_ok = False
                self.last_error = str(e)
                logger.warning("[%s] connect() raised: %s", self.name, e)

            if not connected_ok:
                self.connected = False
                logger.info("[%s] reconnecting in %.1fs", self.name, backoff_s)
                if self._sleep_interruptible(backoff_s):
                    break
                backoff_s = min(backoff_s * 2, RECONNECT_BACKOFF_CAP_S)
                self.reconnect_count += 1
                continue

            # Connected: reset backoff and read frames until failure/EOF.
            backoff_s = RECONNECT_BACKOFF_START_S
            self.connected = True
            self._last_pts_ms = None  # new connection => new PTS clock
            self._read_loop()
            self.connected = False
            self._release_capture()

        self._release_capture()

    def _connect(self) -> bool:
        self._release_capture()
        logger.info("[%s] connecting to %s", self.name, _redact_url(self.rtsp_url))
        cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            cap.release()
            self.last_error = "VideoCapture failed to open"
            return False
        self._cap = cap
        return True

    def _read_loop(self) -> None:
        """
        Reads frames until the stream fails. Isolated decoder warnings at
        join (missing ref frames, RPS errors before the first IDR) show up
        as ordinary failed cap.read() calls or garbled early frames — we
        don't special-case them, we just don't abort on a handful of
        consecutive failures; only a sustained failure run triggers
        reconnect.
        """
        consecutive_failures = 0
        max_consecutive_failures = 30  # tolerate decoder warm-up at join

        while self._running.is_set():
            ok, frame = self._cap.read()
            if not ok or frame is None:
                consecutive_failures += 1
                if consecutive_failures >= max_consecutive_failures:
                    logger.info(
                        "[%s] %d consecutive read failures, treating as disconnect",
                        self.name, consecutive_failures,
                    )
                    return
                time.sleep(0.05)
                continue

            consecutive_failures = 0
            pts_ms = self._normalize_pts(self._cap.get(cv2.CAP_PROP_POS_MSEC))

            with self._lock:
                self._latest = Frame(
                    image=frame,
                    pts_ms=pts_ms,
                    camera_id=self.camera_id,
                    wall_clock_s=time.time(),
                )
                self.frames_received += 1
            self._new_frame_event.set()

    def _normalize_pts(self, raw_pts_ms: float) -> float:
        """
        Keeps the PTS clock monotonically increasing across reconnects and
        the sandbox's hard scene-cut loop points. On a detected backward
        jump (new connection restarting near 0, or a loop discontinuity),
        we fold in an offset so downstream PTS-delta math never sees a
        negative or wildly-jumped interval it would misread as a huge
        instantaneous "speed".
        """
        effective = raw_pts_ms + self._pts_offset_ms
        if self._last_pts_ms is not None and effective < self._last_pts_ms:
            # backward jump: bump the offset so the sequence continues
            # increasing from where it left off (with a nominal small step
            # rather than a big invented delta).
            self._pts_offset_ms += (self._last_pts_ms - effective) + 1.0
            effective = raw_pts_ms + self._pts_offset_ms
        self._last_pts_ms = effective
        return effective

    def _release_capture(self) -> None:
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None

    def _sleep_interruptible(self, seconds: float) -> bool:
        """Sleeps up to `seconds`, returning True early if stop() was called."""
        end = time.time() + seconds
        while time.time() < end:
            if not self._running.is_set():
                return True
            time.sleep(min(0.2, end - time.time()))
        return not self._running.is_set()
