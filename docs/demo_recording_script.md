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
3. **(45s) AI detection/analytics running** — Switch to the dashboard's new
   **Detection Feed** tab: this shows the plate crop AND the full annotated frame
   (green bounding box + OCR text/confidence drawn directly on it) for each recent
   detection, updating live. This is the most convincing visual evidence in the whole
   demo — say: "Here's the actual plate crop and the full camera frame with the AI's
   bounding box drawn on it, next to the OCR-read text and confidence score, updating
   in real time." Optionally also show `main.py`'s terminal log scrolling alongside it.
4. **(45s) Watchlist correlation** — Switch to the dashboard's Watchlist tab, show
   the seeded entries. Say: "We maintain a representative watchlist — plate, reason,
   category." Then switch to the Search/Trace tab and search `GJ11BH7992` (a real,
   repeatedly-detected vehicle with a genuine plate-crop image attached) — show the
   route/detection result appearing as a visual timeline.
5. **(30s) Real-time alert generation** — Switch to the Live Alerts tab. Say: "When
   a detected plate matches the watchlist, an alert is generated automatically — no
   human in the loop — with the camera, location, and timestamp." Point out the
   `GJ11BH7992` alert card and its real plate-crop image, camera, timestamp, and
   100% match confidence.
6. **(15s) Close** — "Everything shown here is live, unrehearsed data from the
   actual camera feed — no recorded-and-replayed footage, no mockup."

**Tip:** before recording, check `docs/evidence/detection_report.md` (regenerate it
fresh first — see below) for concrete plate numbers/timestamps you can reference by
name while narrating, so the demo doesn't feel like you're improvising.

Regenerate the evidence report right before recording so it reflects the latest live
data (this now also gives you a fresh summary + plate list to reference by name):
```bash
cd /home/raj/GoG_Hack/sentinel-hackathon
source .venv/bin/activate
python3 docs/build_output_report.py
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

**Output report:** submit `docs/evidence/Output_Report.pdf` (regenerate it fresh right
before submission) alongside the video. It already includes a summary block (total
detections, plausible-plate count, watchlist alerts, cross-camera trace status) above
the full per-plate table with camera, location, timestamp, and confidence — plus the
one known overlay-text false positive clearly flagged rather than hidden. The CSV
(`output_report.csv`) and Markdown (`output_report.md`) versions are generated
alongside it if the portal prefers a different format:
```bash
cd /home/raj/GoG_Hack/sentinel-hackathon
source .venv/bin/activate
python3 docs/build_output_report.py
```

---

## Before you record — sanity checklist

- [ ] Dashboard loads at http://103.190.242.24:8501 from your machine
- [ ] Live Alerts tab shows the `GJ11BH7992` alert with its real plate-crop image
- [ ] Watchlist tab shows seeded entries
- [ ] Search tab returns a real result for `GJ11BH7992` (or any plate you'll mention
      by name — regenerate the output report first to find a fresh one if you want a
      different example)
- [ ] Terminal showing `main.py` logs is visible/switchable during recording, if you
      want to show raw log output as evidence of "live," not just the polished UI
