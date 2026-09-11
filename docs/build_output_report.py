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
from vehicle_trace.route_reconstruction import search_plate

DOCS_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = DOCS_DIR / "evidence"
CSV_PATH = EVIDENCE_DIR / "output_report.csv"
MD_PATH = EVIDENCE_DIR / "output_report.md"
HTML_PATH = EVIDENCE_DIR / "_output_report_render.html"
PDF_PATH = EVIDENCE_DIR / "Output_Report.pdf"

# A specific, confirmed root cause (not a general heuristic): this exact
# OCR read is the video overlay's own burned-in timestamp/location caption
# ("18/06/2026 17:55:54, Madhuram Bypass Road Fix-2 (From Ak...)"), not a
# vehicle plate. Found by inspecting the annotated frame directly - the
# detector's bounding box sits on the on-screen caption text, not a
# vehicle. Annotated rather than deleted, so the report stays an honest,
# complete record of every real detection event.
KNOWN_OVERLAY_TEXT_PLATES = {"18062026175554MADHURAMBYPASSROADFIX2FROMAK"}

# Confirmed, unambiguous trace evidence: one vehicle's repeat sighting on
# a single camera, correctly linked across OCR-confusion-variant readings
# (see docs/evidence/trace_demonstration.md for the full methodology).
TRACE_EVIDENCE_PLATE = "BV2807"

# Cross-camera candidate (2026-09-11 check): found via the same exact +
# confusion-variant matching, filtered to plausible-length plates (>=5
# chars) to exclude single-character noise coincidences. Two independent
# detections, ~26 hours apart, geographically plausible (Junagadh <->
# Ahmedabad-area, reachable by road in that window) - a strong OCR-level
# match, not a database-verified same-vehicle confirmation, so it is
# reported as candidate evidence rather than certainty throughout.
CROSS_CAMERA_CANDIDATE_PLATES = {"GJ18ZT1282", "GJ182T1282"}

init_db()


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def is_plausible_plate(plate: str) -> bool:
    """
    Loose plausibility check, not a strict Indian-plate-format match: real
    OCR reads routinely lose or gain 1-2 characters relative to the
    canonical SS-DD-LL-DDDD shape, so requiring an exact format match
    would undercount genuine plates. This instead excludes what's clearly
    not a plate read: pure-digit or pure-letter fragments, single
    characters, and overly long concatenated strings (the overlay-text
    false positive above is 42 characters and is excluded by the length
    bound alone, without needing special-casing here).
    """
    if not (6 <= len(plate) <= 11):
        return False
    if not plate.isalnum():
        return False
    return any(c.isalpha() for c in plate) and any(c.isdigit() for c in plate)


def main():
    # A fixed cap silently truncated the report once the DB grew past it
    # (21,698 real detections accumulated over the sandbox run vs. the old
    # 5000-row limit) - the report is supposed to be a complete record, so
    # this pulls everything rather than guessing at a "big enough" number.
    dets = recent_detections(limit=1_000_000)
    dets = sorted(dets, key=lambda d: d["wall_clock_s"])
    alerts = recent_alerts(limit=10_000)
    alert_detection_ids = {a["detection_id"] for a in alerts}

    generated_at = datetime.now(timezone.utc)
    cameras = sorted({d["camera_id"] for d in dets})

    plausible_count = sum(1 for d in dets if is_plausible_plate(d["plate"]))
    overlay_text_count = sum(1 for d in dets if d["plate"] in KNOWN_OVERLAY_TEXT_PLATES)
    trace_stops = search_plate(TRACE_EVIDENCE_PLATE)
    trace_cameras = sorted({s.camera_id for s in trace_stops})
    cross_cam_rows = sorted(
        (d for d in dets if d["plate"] in CROSS_CAMERA_CANDIDATE_PLATES),
        key=lambda d: d["wall_clock_s"],
    )

    # --- CSV -----------------------------------------------------------------
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "plate", "camera_id", "location", "timestamp_utc", "pts_ms",
            "ocr_confidence", "detector_confidence", "watchlist_alert", "note",
        ])
        for d in dets:
            note = "KNOWN FALSE POSITIVE: video overlay timestamp/caption text, not a vehicle plate" \
                if d["plate"] in KNOWN_OVERLAY_TEXT_PLATES else ""
            w.writerow([
                d["plate"], d["camera_id"], d["location"], iso(d["wall_clock_s"]),
                f"{d['pts_ms']:.0f}", f"{d['ocr_confidence']:.3f}",
                f"{d['detector_confidence']:.3f}",
                "YES" if d["id"] in alert_detection_ids else "",
                note,
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

        f.write("## Summary\n\n")
        f.write(f"- **Total detections:** {len(dets)}\n")
        f.write(
            f"- **Plausible plate reads:** {plausible_count} "
            f"({plausible_count / len(dets):.0%} of total) — passes a loose alphanumeric "
            "shape check (6-11 characters, contains both letters and digits); the "
            "remainder are short OCR fragments, non-plate on-screen text, or the one "
            "known overlay-text false positive noted below\n"
        )
        f.write(f"- **Cameras onboarded:** {', '.join(cameras)}\n")
        f.write(f"- **Watchlist alerts generated:** {len(alerts)}\n")
        f.write(
            f"- **Confirmed single-camera trace:** plate `{TRACE_EVIDENCE_PLATE}` "
            f"detected {len(trace_stops)} times on camera(s) {', '.join(trace_cameras)}, "
            f"correctly linked across OCR-confusion variants "
            f"(see `trace_demonstration.md` for full detail)\n"
        )
        if cross_cam_rows:
            cross_cam_summary = "; ".join(
                f"`{d['plate']}` on {d['camera_id']} at {iso(d['wall_clock_s'])} "
                f"(OCR conf {d['ocr_confidence']:.0%})"
                for d in cross_cam_rows
            )
            f.write(
                f"- **Cross-camera candidate:** {cross_cam_summary} — a strong "
                "OCR-level match via exact + confusion-variant matching (checked across "
                "all plausible-length plates), not a database-verified same-vehicle "
                "confirmation; reported as candidate evidence, not certainty\n"
            )
        if overlay_text_count:
            f.write(
                f"- **Known false positive:** {overlay_text_count} detection(s) flagged "
                "below are the video overlay's own burned-in timestamp/caption text, not "
                "a vehicle plate — kept in the table rather than deleted, so this remains "
                "a complete record of every real detection event\n"
            )
        f.write("\n")

        f.write("## Detections\n\n")
        f.write("| Plate | Camera | Location | Timestamp (UTC) | OCR Conf. | Detector Conf. | Alert | Note |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for d in dets:
            flag = "🚨" if d["id"] in alert_detection_ids else ""
            note = "⚠️ overlay text, not a plate" if d["plate"] in KNOWN_OVERLAY_TEXT_PLATES else ""
            f.write(
                f"| {d['plate']} | {d['camera_id']} | {d['location']} | {iso(d['wall_clock_s'])} "
                f"| {d['ocr_confidence']:.0%} | {d['detector_confidence']:.0%} | {flag} | {note} |\n"
            )

    # --- PDF (styled HTML, rendered via headless Chromium) ---------------------
    import html as html_lib

    # Chromium's print-to-PDF fails outright on a table this large (21,698
    # real rows) rather than just being slow - confirmed by hitting
    # "Printing failed" from Page.printToPDF on the full dataset. The CSV
    # and Markdown outputs above already contain every row without any
    # cap, so they remain the complete, authoritative record; the PDF
    # samples down to a size Chromium can actually render, always keeping
    # every alert and every cross-camera-candidate row (the evidence that
    # actually matters for review) rather than truncating them away by
    # chance the way a plain "most recent N" cut could.
    PDF_ROW_CAP = 2000
    must_keep = [
        d for d in dets
        if d["id"] in alert_detection_ids or d["plate"] in CROSS_CAMERA_CANDIDATE_PLATES
    ]
    must_keep_ids = {d["id"] for d in must_keep}
    remainder = [d for d in dets if d["id"] not in must_keep_ids]
    sampled_dets = sorted(
        must_keep + remainder[-(PDF_ROW_CAP - len(must_keep)):],
        key=lambda d: d["wall_clock_s"],
    )
    pdf_is_sampled = len(sampled_dets) < len(dets)

    rows_html = []
    for d in sampled_dets:
        is_alert = d["id"] in alert_detection_ids
        is_overlay_fp = d["plate"] in KNOWN_OVERLAY_TEXT_PLATES
        row_style = ' style="background:#fff7e6;"' if is_alert else (
            ' style="background:#fef2f2;"' if is_overlay_fp else ""
        )
        flag = '<span style="color:#b45309;font-weight:700;">ALERT</span>' if is_alert else ""
        note = (
            '<span style="color:#b91c1c;">overlay text, not a plate</span>'
            if is_overlay_fp else ""
        )
        rows_html.append(
            f"<tr{row_style}><td>{html_lib.escape(d['plate'])}</td><td>{html_lib.escape(d['camera_id'])}</td>"
            f"<td>{html_lib.escape(d['location'])}</td><td>{iso(d['wall_clock_s'])}</td>"
            f"<td>{d['ocr_confidence']:.0%}</td><td>{d['detector_confidence']:.0%}</td>"
            f"<td>{flag}</td><td>{note}</td></tr>"
        )

    trace_cameras_html = html_lib.escape(", ".join(trace_cameras))
    overlay_note_html = ""
    if overlay_text_count:
        overlay_note_html = (
            f'<div class="summary-row"><b>Known false positive:</b> {overlay_text_count} '
            "detection(s) below are the video overlay's own burned-in timestamp/caption "
            "text, not a vehicle plate — kept in the table rather than deleted, so this "
            "remains a complete record of every real detection event (highlighted in red).</div>"
        )

    cross_cam_note_html = ""
    if cross_cam_rows:
        cross_cam_items = "".join(
            f"<li><b>{html_lib.escape(d['plate'])}</b> on {html_lib.escape(d['camera_id'])} "
            f"at {iso(d['wall_clock_s'])} (OCR conf {d['ocr_confidence']:.0%})</li>"
            for d in cross_cam_rows
        )
        cross_cam_note_html = (
            '<div class="summary-row"><b>Cross-camera candidate:</b> a strong OCR-level '
            "match via exact + confusion-variant matching (checked across all "
            "plausible-length plates), not a database-verified same-vehicle confirmation "
            f"— reported as candidate evidence, not certainty.<ul>{cross_cam_items}</ul></div>"
        )

    sample_note_html = ""
    if pdf_is_sampled:
        sample_note_html = (
            f'<div class="summary-row"><b>Table below is a sample:</b> {len(sampled_dets)} of '
            f'{len(dets)} total detections are shown (every watchlist alert and every '
            'cross-camera-candidate row is always included; the rest is a recent-activity '
            'sample). The complete, unsampled record of all detections is in '
            '<code>output_report.csv</code> and <code>output_report.md</code>.</div>'
        )

    html = f"""<!doctype html><html><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 18mm 14mm; }}
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #1a1a1a; font-size: 10.5px; }}
        h1 {{ font-size: 20px; margin-bottom: 2px; color: #0a0e14; }}
        h2 {{ font-size: 13px; margin: 16px 0 8px 0; color: #0a0e14; border-bottom: 1px solid #ddd; padding-bottom: 3px; }}
        .sub {{ color: #666; font-size: 11px; margin-bottom: 18px; }}
        .stats {{ display: flex; gap: 24px; margin-bottom: 14px; flex-wrap: wrap; }}
        .stat {{ border: 1px solid #ddd; border-radius: 6px; padding: 8px 14px; }}
        .stat .n {{ font-size: 18px; font-weight: 700; color: #3b82f6; }}
        .stat .l {{ font-size: 9px; color: #888; text-transform: uppercase; }}
        .summary-row {{ font-size: 10px; color: #333; margin: 4px 0; line-height: 1.5; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #0a0e14; color: white; text-align: left; padding: 6px 8px; font-size: 9.5px; }}
        td {{ padding: 5px 8px; border-bottom: 1px solid #eee; font-size: 9.5px; }}
        tr:nth-child(even) {{ background: #fafafa; }}
    </style></head><body>
    <h1>Sentinel — Government-Feed Output Report</h1>
    <div class="sub">Generated {generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')} &nbsp;·&nbsp;
    Gujarat Police Innovation Challenge 2026 · Model 2 &nbsp;·&nbsp; Live Sentinel sandbox feed</div>

    <h2>Summary</h2>
    <div class="stats">
        <div class="stat"><div class="n">{len(dets)}</div><div class="l">Total Detections</div></div>
        <div class="stat"><div class="n">{plausible_count}</div><div class="l">Plausible Plate Reads</div></div>
        <div class="stat"><div class="n">{len(alerts)}</div><div class="l">Watchlist Alerts</div></div>
        <div class="stat"><div class="n">{len(cameras)}</div><div class="l">Cameras Onboarded</div></div>
    </div>
    <div class="summary-row"><b>Confirmed single-camera trace:</b> plate
    <b>{html_lib.escape(TRACE_EVIDENCE_PLATE)}</b> detected {len(trace_stops)} times on
    camera(s) {trace_cameras_html}, correctly linked across OCR-confusion variants (see
    trace_demonstration.md for full detail).</div>
    {cross_cam_note_html}
    {overlay_note_html}
    {sample_note_html}

    <h2>Detections</h2>
    <table>
        <thead><tr><th>Plate</th><th>Camera</th><th>Location</th><th>Timestamp (UTC)</th>
        <th>OCR Conf.</th><th>Detector Conf.</th><th>Alert</th><th>Note</th></tr></thead>
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
