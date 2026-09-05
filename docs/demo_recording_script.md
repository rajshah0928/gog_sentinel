# Demo Recording Script

Dashboard URL: **http://103.190.242.24:8501**
(If it doesn't load: `sudo firewall-cmd --add-port=8501/tcp --permanent && sudo firewall-cmd --reload` on the server, then retry.)

Both demos below use the same live system (real Sentinel sandbox feeds, real
detections) — this is intentional and stronger than staged footage. Record them as
two separate takes since they have different required talking points per the
submission spec.

---

## Demo 1: Own-Feed Demo (max 2-3 minutes)

Required to show: onboarding, AI detection/analytics running, watchlist correlation,
real-time alert generation. Must look like a working system, not a mockup.

**Suggested flow:**

1. **(15s) Intro** — "This is Sentinel, our Model 2 unified viewing and ANPR analytics
   platform, running live against camera feeds." Show the terminal/dashboard split
   view if convenient.
2. **(20s) Onboarding** — Show `python -m config.ingest_client` output or the
   Cameras tab in the dashboard, listing real cameras with their names/locations.
   Say: "The platform pulls its camera list live from the gateway — nothing is
   hardcoded."
3. **(45s) AI detection/analytics running** — Open a terminal and show `main.py`'s
   live log output scrolling (STATUS lines, `plate read:` lines appearing in real
   time). Say: "This is a real YOLO-based plate detector and PaddleOCR reading
   actual license plates from live video, right now, on this camera." Point out a
   specific full-plate read in the log if one appears (e.g. `GJ05AU9828` or similar)
   and its confidence score.
4. **(45s) Watchlist correlation** — Switch to the dashboard's Watchlist tab, show
   the seeded entries. Say: "We maintain a representative watchlist — plate, reason,
   category." Then switch to the Search/Trace tab, search a plate you know is in
   both the watchlist and the detections (check `docs/evidence/detection_report.md`
   for a real example, e.g. search `GJ05AU9828`), show the route/detection result
   appearing.
5. **(30s) Real-time alert generation** — Switch to the Live Alerts tab. Say: "When
   a detected plate matches the watchlist, an alert is generated automatically — no
   human in the loop — with the camera, location, and timestamp." Point out the
   alert row and its fields (camera_id, timestamp, match confidence).
6. **(15s) Close** — "Everything shown here is live, unrehearsed data from the
   actual camera feed — no recorded-and-replayed footage, no mockup."

**Tip:** before recording, check `docs/evidence/detection_report.md` (regenerate it
fresh first — see below) for concrete plate numbers/timestamps you can reference by
name while narrating, so the demo doesn't feel like you're improvising.

Regenerate the evidence report right before recording so it reflects the latest live
data:
```bash
cd /home/raj/GoG_Hack/sentinel-hackathon
source .venv/bin/activate
python3 -c "
import sys; sys.path.insert(0, '.')
from watchlist.db import recent_detections, recent_alerts
for d in recent_detections(limit=15):
    print(d['plate'], d['camera_id'], round(d['ocr_confidence'],2))
"
```

---

## Demo 2: Government-Feed Demo (screen-recorded, plus an output report)

Required to show: onboarding and live/recorded viewing of the **government-provided
(sandbox) feed** specifically, plus analytics output, plus a submitted output report
listing detected plates with timestamps.

Since Demo 1 already uses the sandbox live, this demo can be shorter and more
report-focused — the emphasis here is proving it's the *actual* government sandbox,
not just narrating the same thing twice.

**Suggested flow:**

1. **(20s)** Show the sandbox's own web UI or the `cameras.json` catalogue response
   directly (e.g. `curl` it, or show the browser at the sandbox's login/camera list
   page) to establish this is genuinely the government-provided grid, not a
   substitute.
2. **(40s)** Show the RTSP URL pattern / `main.py --cameras cam12,cam06,cam22`
   command actually running, connecting to real sandbox camera IDs.
3. **(40s)** Show live detections appearing in the dashboard or terminal log, same as
   Demo 1 but explicitly narrating "this is the government sandbox feed at
   [camera name/location from cameras.json]."
4. **(20s)** Close.

**Output report:** submit `docs/evidence/detection_report.md` (regenerate it fresh
right before submission) alongside the video — it already lists every detected plate
with camera, location, OCR confidence, and PTS timestamp, which is exactly what's
required. Convert to PDF if the submission portal wants a single file:
```bash
cd /home/raj/GoG_Hack/sentinel-hackathon
python3 -c "
import sys; sys.path.insert(0, '.')
from watchlist.db import recent_detections, recent_alerts
from datetime import datetime, timezone
dets = recent_detections(limit=500)
alerts = recent_alerts(limit=100)
with open('docs/evidence/detection_report.md', 'w') as f:
    f.write('# Sentinel ANPR Detection Report\n\n')
    f.write(f'Generated: {datetime.now(timezone.utc).isoformat()}\n\n')
    f.write(f'Total detections: {len(dets)}\n\n')
    f.write('## Alerts\n\n| Plate | Camera | Location | Match Conf | Category | Reason |\n|---|---|---|---|---|---|\n')
    for a in alerts:
        f.write(f\"| {a['plate']} | {a['camera_id']} | {a['location']} | {a['match_confidence']:.1f} | {a['category']} | {a['reason']} |\n\")
    f.write('\n## Detections\n\n| Plate | Camera | Location | OCR Conf | Detector Conf | PTS (ms) |\n|---|---|---|---|---|---|\n')
    for d in dets:
        f.write(f\"| {d['plate']} | {d['camera_id']} | {d['location']} | {d['ocr_confidence']:.2f} | {d['detector_confidence']:.2f} | {d['pts_ms']:.0f} |\n\")
print('regenerated')
"
```
Then open the `.md` in a browser/editor and print-to-PDF, or paste into a doc.

---

## Before you record — sanity checklist

- [ ] Dashboard loads at http://103.190.242.24:8501 from your machine
- [ ] Live Alerts tab shows at least 1 real alert (currently: yes, `GJ05AU9828`)
- [ ] Watchlist tab shows seeded entries
- [ ] Search tab returns a real result for a plate you'll mention by name
- [ ] Terminal showing `main.py` logs is visible/switchable during recording, if you
      want to show raw log output as evidence of "live," not just the polished UI

## While you're in the browser anyway — grab these for the HLD/PPT

I can't screenshot the live dashboard myself (no display access in this
environment), so please grab these during the recording session and drop the image
files into `docs/evidence/` (any filename, I'll wire them into the HLD/PPT after):

- [ ] Live Alerts tab with the `GJ05AU9828` alert visible
- [ ] Search/Trace tab showing a plate search result (e.g. `BV2807` — should show
      4 chronologically-ordered detections from the confusion-variant fix)
- [ ] Watchlist tab showing the seeded entries
- [ ] Cameras tab showing the real camera list (proves it's pulled live, not
      hardcoded)
