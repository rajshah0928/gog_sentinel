# Sentinel — Unified Viewing & Metadata Analytics (Model 2)

Prototype for the Gujarat Police Innovation Challenge 2026. Connects directly
to heterogeneous CCTV feeds via RTSP (no middleware/federation layer), runs
CPU-only ANPR analytics, cross-references detections against a watchlist,
and reconstructs vehicle routes across the camera grid.

## Setup

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .
```

Set the sandbox credentials before running anything that touches live cameras
(never commit these — put them in `.env.local`, which is gitignored, and
`source .env.local` before running):

```bash
export SENTINEL_EMAIL="you@example.com"     # registered/approved sandbox access-list email
export SENTINEL_PASSWORD="XXXX-XXXX-XXXX"   # sandbox access password
```

HLS is served from `cctv.corp8.cloud` (CDN, works from any network) behind a
session login; RTSP/WHEP connect directly to the public IP
`103.250.160.189` and require `email:password` embedded in the URL
(handled automatically by `config/settings.py` — percent-encodes both).
Override hosts/ports via `SENTINEL_HLS_HOST` / `SENTINEL_RTSP_HOST` /
`SENTINEL_RTSP_PORT` / `SENTINEL_WHEP_PORT` if the sandbox changes them.

## Run order

```bash
# 1. Confirm the catalogue is reachable
python -m config.ingest_client

# 2. Seed a representative watchlist
python -m watchlist.seed_watchlist

# 3. Run the ANPR pipeline against a few cameras (ids are cam01...cam30)
python main.py --cameras cam01,cam02,cam04
# or: python main.py --all

# 4. In another terminal, launch the dashboard
streamlit run dashboard/app.py
```

## Repo layout

- `capture/` — resilient per-camera RTSP capture (TCP-forced, PTS-timestamped, auto-reconnect)
- `analytics/` — plate detection (YOLO) + OCR (PaddleOCR) pipeline
- `watchlist/` — SQLite schema, fuzzy plate matching, alert generation
- `vehicle_trace/` — route reconstruction (plate → ordered camera/location/timestamp history)
  (named `vehicle_trace`, not `trace`, to avoid shadowing Python's stdlib `trace` module)
- `dashboard/` — Streamlit UI: alerts, camera grid, plate search, watchlist admin
- `config/` — `cameras.json` catalogue client (session-auth), tunable settings
- `tests/` — scripts mapped to the Definition of Done checklist (see below)

## Tuning for distant/small plates

The 30 sandbox cameras are mostly wide-angle overhead traffic-junction CCTV — at
that framing, plates on far vehicles can be too small for the detector to find in
a single downscaled whole-frame pass. Set `PLATE_DETECTOR_USE_TILING=true` to
instead run detection per-tile at native resolution (`PLATE_DETECTOR_TILE_SIZE`,
default 640px, `PLATE_DETECTOR_TILE_OVERLAP`, default 0.2) — better recall on
small/distant plates at the cost of one model inference per tile per sampled
frame. Off by default; enable per-camera based on its actual traffic distance
profile rather than globally, since it multiplies CPU cost.

## Definition of Done — how to verify

| Check | Script |
|---|---|
| Catalogue read dynamically from `cameras.json` | `python tests/test_ingest_catalogue.py` |
| 2-3 cameras stay connected over a sustained run | `python tests/test_capture_resilience.py --duration 1200 --cameras cam01,cam02,cam04` |
| Reconnect recovers after a killed feed | `python tests/test_reconnect_forced.py --camera cam01` (no root on this host to sever a TCP connection externally, so this exercises the same stop/restart-recovery path a supervisor would use — see the script's docstring; the soak test above additionally shows natural recovery from real decoder-level interruptions) |
| Known test plate → correctly logged alert | `python tests/test_alert_e2e.py seed <PLATE>` then `... wait <PLATE>` while `main.py` runs |
| Trace across 2+ cameras, correct order | `python tests/test_trace_e2e.py <PLATE>` |
| Dashboard reflects live alerts without refresh | `streamlit run dashboard/app.py` — auto-refreshes every 5s via `streamlit_autorefresh`, no manual reload needed |

## Notes on the integration rules this code follows

- RTSP is always opened with `rtsp_transport=tcp` (`capture/rtsp_capture.py`).
- All timing (frame intervals, "last seen") is derived from `CAP_PROP_POS_MSEC`, never wall-clock arrival or declared FPS.
- Reconnects use exponential backoff (2s → 30s cap), never a tight loop.
- Decoder hiccups at join are tolerated (a run of failed reads only triggers reconnect past a threshold, not on the first failure).
- Camera list is always pulled from `cameras.json` — nothing is hardcoded.
- Only cameras actively being processed are held open (`CaptureManager.open`/`close`).
- Credentials are never logged: RTSP/WHEP URLs are redacted before any log line (`capture/rtsp_capture.py::_redact_url`).
