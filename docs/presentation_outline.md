# Sentinel — Solution Presentation Outline

Source material for the PPT/PDF deliverable. Each section below = roughly one slide.

## 1. Title
Sentinel — Unified Viewing & Metadata Analytics for Gujarat Police CCTV Integration
Gujarat Police Innovation Challenge 2026 · Model 2

## 2. Problem understanding
- 26 departments, independent CCTV/VMS, heterogeneous vendors/storage/retention.
- Central command centres need one view, not N separate viewers.
- Existing high-value databases (VAHAN, eGujCop/CCTNS, AFIS/NAFIS) are siloed from
  live video — no automated real-time correlation today.

## 3. Solution model + justification
- **Model 2: Unified Viewing & Metadata Analytics** — direct RTSP/ONVIF/vendor-API
  connection to each camera/VMS, no federation/middleware layer, departmental systems
  untouched.
- Why: lowest integration risk, no dependency on any department changing their VMS or
  storage; delivers the two capabilities the evaluation actually tests (live unified
  view + AI vehicle tracing) without a multi-department federation program. See
  `HLD.md` §1 for the full reasoning, including why Models 3/4 are out of scope given
  the timeline.

## 4. Architecture overview
(Use the ASCII diagram in HLD.md §2 as the basis for a proper diagram — Departmental
CCTV → Capture Layer → ANPR Pipeline → Watchlist/Alerting → Route Reconstruction →
Unified Dashboard.)
- Key point: no video is centrally stored — only structured detection metadata.

## 5. Live stream ingestion — built for real-world gateway behavior
- TCP-forced RTSP, PTS-derived timing (never wall clock / declared FPS), exponential
  backoff reconnect, tolerant of decoder warm-up noise and mixed H.264/H.265.
- Camera inventory always pulled live from the gateway — zero hardcoded camera IDs.
- **Proven, not just designed**: tested against the live 30-camera Sentinel sandbox —
  found and fixed a real cross-thread capture bug during load testing, confirmed
  automatic recovery after a forced restart, and ran a clean multi-camera sustained
  session with zero crashes and zero unwanted reconnects.

## 6. AI-powered video analytics
- ANPR (mandatory analytic): pretrained YOLO-class detector + PaddleOCR, CPU-only,
  configurable frame sampling for real-time feasibility on commodity hardware (no GPU
  required — built and validated on a 40-core CPU box).
- Indian-plate-aware OCR confusion handling (0/O, 1/I, 5/S, 8/B, 2/Z).
- Configurable tiled-detection mode for cameras where plates are small/distant.
- **The debugging story is the strongest evidence slide we have** — walk through it
  live, don't just state the conclusion (HLD §5 has full detail + numbers):
  1. Most sandbox cameras are wide-angle junction cams, genuinely not plate-resolvable
     at distance — an honest, real finding, not a failure.
  2. Went back to the camera catalogue's own naming and found a toll-plaza camera
     ("Tollnaka") — camera *metadata*, not just camera count, is the actionable signal.
  3. On that camera's legible plate crop, our first OCR engine (EasyOCR) capped at
     ~0.3 confidence after heavy tuning; swapping to PaddleOCR on the identical crop
     got 0.87 with no other change.
  4. Even then, the *real* pipeline still failed — root cause was our own bounding-box
     crop clipping characters. Fixed by padding the detector's box by 75% of its own
     size, verified against the actual detector output, not a hand-cropped image.
  5. Result over a multi-hour unattended run: 480+ detections above threshold across
     three independently-confirmed cameras, the large majority full plausible Indian
     plates (e.g. `GJ05AU9828` at 0.96 confidence; the same vehicle's `BV2807` read
     consistently across 3 independent passes).
- **Screenshot: `docs/evidence/detection_feed.png`** — real crop + real annotated frame
  (green bounding box drawn by the actual detector, OCR text/confidence overlaid) for
  two different real vehicles (`J02EKU873`, `GJ11CD3491`), captured live from the
  running dashboard, not staged. This is the single strongest evidence image in the
  whole deck — lead the analytics section with it.

## 7. Watchlist correlation + real-time alerting
- Every OCR read (not sampled after the fact) is normalized and matched — exact +
  confusion-aware pass, then fuzzy-similarity fallback.
- Match → alert written with camera, plate, PTS timestamp, confidence, matched entry
  — visible in the dashboard within seconds, no manual refresh.
- Screenshot: `docs/evidence/alert.png` — a real watchlist match (`GJ11BH7992`, 100%
  match confidence) shown with its actual plate crop, camera, location, and timestamp,
  live on the dashboard.
- Designed to plug into VAHAN / eGujCop-CCTNS as the real watchlist source in
  production (HLD §4); our own representative watchlist used for this demo, as
  explicitly permitted.

## 8. Vehicle route reconstruction — the evaluation's core test
- Given a plate, return every (camera, location, timestamp) detection in chronological
  order — this is exactly what "trace a designated vehicle across the grid" requires.
- Screenshot: `docs/evidence/trace.png` — a real search result rendered as a visual
  timeline with the plate crop shown at the sighting.
- Evidence: `docs/evidence/trace_demonstration.md` — a real vehicle, detected 4 times
  by the live pipeline within 16 seconds, correctly linked despite OCR reading it as
  both `BV2807` and `8V2807` (the confusion-variant fix, found via this exact data,
  is described there with before/after numbers).
- Honest status: three cameras (`cam12`, `cam06`, `cam22`) are independently confirmed
  ANPR-viable and ran simultaneously for hours accumulating 480+ real detections; a
  comprehensive check (exact + confusion-variant matching) found no same-plate sighting
  across two different cameras yet — real traffic timing and this sandbox's specific
  camera mix, not a code limitation. If one lands before submission, lead with it
  instead.

## 9. Unified dashboard
- Live alert feed (auto-refreshing), camera grid with last-seen plate per camera,
  plate search/trace view, watchlist admin, camera map.
- Screenshots (all real, captured live from the running dashboard):
  `docs/evidence/alert.png` (Live Alerts), `docs/evidence/detection_feed.png`
  (Detection Feed — the strongest visual evidence), `docs/evidence/trace.png`
  (Search/Trace), `docs/evidence/camera_feed.png` (Cameras),
  `docs/evidence/watchlist.png` (Watchlist).

## 10. Tech stack
- Capture: OpenCV + FFmpeg backend (Python)
- Detection: Ultralytics YOLO (pretrained, CPU)
- OCR: PaddleOCR (PP-OCRv6)
- Storage: SQLite (pilot scale; schema-compatible upgrade path to PostgreSQL)
- Dashboard: Streamlit
- No GPU / no external message bus required for this prototype's scale — deliberately
  minimal-dependency for fast, reliable deployment.

## 11. Scalability, security, deployment (summary — full detail in HLD §7)
- Horizontal scale-out: independent capture/ANPR workers, sharded by camera set.
- Edge pre-filtering and GPU/accelerator path for 80,000-camera scale.
- Credentials never logged; consume-only design (never pushes to or controls any
  gateway); RBAC/audit logging as the production hardening path.
- No department's existing VMS, storage, or retention policy is touched.

## 12. Operational benefits / impact
- Single pane of glass across departments without a multi-year federation project.
- Automated, continuous watchlist correlation — proactive alerting instead of manual
  after-the-fact video review.
- Fast path to statewide expansion: same architecture, more camera shards, no redesign.

## 13. What's next (roadmap, honest about current scope)
- FRS and other analytics (explicitly out of scope for this build, bonus territory).
- VAHAN/eGujCop live integration (currently a representative demo watchlist).
- Edge deployment pilot for bandwidth-constrained districts.
