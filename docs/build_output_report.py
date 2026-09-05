"""
Builds the Government-Feed Output Report deliverable: a written record of
every detected plate with camera, location, timestamp, and confidence,
pulled live from the running pipeline's database. Separate artifact from
the demo video, as required by the submission spec.

Produces:
    docs/evidence/output_report.csv   - full data, every detection
    docs/evidence/output_report.md    - human-readable markdown table
    docs/evidence/Output_Report.pdf   - styled PDF (rendered via headless
                                         Chromium print-to-PDF)

Run from repo root:
    python docs/build_output_report.py
"""
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from watchlist.db import init_db, recent_detections, recent_alerts

DOCS_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = DOCS_DIR / "evidence"
CSV_PATH = EVIDENCE_DIR / "output_report.csv"
MD_PATH = EVIDENCE_DIR / "output_report.md"
HTML_PATH = EVIDENCE_DIR / "_output_report_render.html"
PDF_PATH = EVIDENCE_DIR / "Output_Report.pdf"

init_db()


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def main():
    dets = recent_detections(limit=5000)
    dets = sorted(dets, key=lambda d: d["wall_clock_s"])
    alerts = recent_alerts(limit=500)
    alert_detection_ids = {a["detection_id"] for a in alerts}

    generated_at = datetime.now(timezone.utc)
    cameras = sorted({d["camera_id"] for d in dets})

    # --- CSV -----------------------------------------------------------------
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "plate", "camera_id", "location", "timestamp_utc", "pts_ms",
            "ocr_confidence", "detector_confidence", "watchlist_alert",
        ])
        for d in dets:
            w.writerow([
                d["plate"], d["camera_id"], d["location"], iso(d["wall_clock_s"]),
                f"{d['pts_ms']:.0f}", f"{d['ocr_confidence']:.3f}",
                f"{d['detector_confidence']:.3f}",
                "YES" if d["id"] in alert_detection_ids else "",
            ])

    # --- Markdown --------------------------------------------------------------
    with open(MD_PATH, "w") as f:
        f.write("# Sentinel — Government-Feed Output Report\n\n")
        f.write(f"Generated: {generated_at.isoformat()}\n\n")
        f.write(
            "Detected vehicles/plates with corresponding timestamps, from the live "
            "Sentinel Gujarat sandbox feed (government-provided cameras). Every row "
            "is a real detection from the running ANPR pipeline — not simulated or "
            "replayed.\n\n"
        )
        f.write(f"**Total detections:** {len(dets)}  \n")
        f.write(f"**Cameras onboarded:** {', '.join(cameras)}  \n")
        f.write(f"**Watchlist alerts generated:** {len(alerts)}\n\n")
        f.write("| Plate | Camera | Location | Timestamp (UTC) | OCR Conf. | Detector Conf. | Alert |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for d in dets:
            flag = "🚨" if d["id"] in alert_detection_ids else ""
            f.write(
                f"| {d['plate']} | {d['camera_id']} | {d['location']} | {iso(d['wall_clock_s'])} "
                f"| {d['ocr_confidence']:.0%} | {d['detector_confidence']:.0%} | {flag} |\n"
            )

    # --- PDF (styled HTML, rendered via headless Chromium) ---------------------
    rows_html = []
    for d in dets:
        is_alert = d["id"] in alert_detection_ids
        row_style = ' style="background:#fff7e6;"' if is_alert else ""
        flag = '<span style="color:#b45309;font-weight:700;">ALERT</span>' if is_alert else ""
        rows_html.append(
            f"<tr{row_style}><td>{d['plate']}</td><td>{d['camera_id']}</td>"
            f"<td>{d['location']}</td><td>{iso(d['wall_clock_s'])}</td>"
            f"<td>{d['ocr_confidence']:.0%}</td><td>{d['detector_confidence']:.0%}</td>"
            f"<td>{flag}</td></tr>"
        )

    html = f"""<!doctype html><html><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 18mm 14mm; }}
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #1a1a1a; font-size: 10.5px; }}
        h1 {{ font-size: 20px; margin-bottom: 2px; color: #0a0e14; }}
        .sub {{ color: #666; font-size: 11px; margin-bottom: 18px; }}
        .stats {{ display: flex; gap: 24px; margin-bottom: 18px; }}
        .stat {{ border: 1px solid #ddd; border-radius: 6px; padding: 8px 14px; }}
        .stat .n {{ font-size: 18px; font-weight: 700; color: #3b82f6; }}
        .stat .l {{ font-size: 9px; color: #888; text-transform: uppercase; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #0a0e14; color: white; text-align: left; padding: 6px 8px; font-size: 9.5px; }}
        td {{ padding: 5px 8px; border-bottom: 1px solid #eee; font-size: 9.5px; }}
        tr:nth-child(even) {{ background: #fafafa; }}
    </style></head><body>
    <h1>Sentinel — Government-Feed Output Report</h1>
    <div class="sub">Generated {generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')} &nbsp;·&nbsp;
    Gujarat Police Innovation Challenge 2026 · Model 2 &nbsp;·&nbsp; Live Sentinel sandbox feed</div>
    <div class="stats">
        <div class="stat"><div class="n">{len(dets)}</div><div class="l">Detections</div></div>
        <div class="stat"><div class="n">{len(cameras)}</div><div class="l">Cameras Onboarded</div></div>
        <div class="stat"><div class="n">{len(alerts)}</div><div class="l">Watchlist Alerts</div></div>
    </div>
    <table>
        <thead><tr><th>Plate</th><th>Camera</th><th>Location</th><th>Timestamp (UTC)</th>
        <th>OCR Conf.</th><th>Detector Conf.</th><th>Alert</th></tr></thead>
        <tbody>{"".join(rows_html)}</tbody>
    </table>
    </body></html>"""

    HTML_PATH.write_text(html)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH}")
        page.pdf(path=str(PDF_PATH), format="A4", print_background=True)
        browser.close()
    HTML_PATH.unlink()

    print(f"Wrote {CSV_PATH} ({len(dets)} rows)")
    print(f"Wrote {MD_PATH}")
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
