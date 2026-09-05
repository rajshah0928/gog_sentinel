"""
Sentinel unified viewer dashboard: live alerts with visual plate evidence,
camera grid with thumbnails, plate search / route reconstruction shown as a
visual timeline, and watchlist administration.

Run with: streamlit run dashboard/app.py
Reads directly from the SQLite DB written by the ANPR pipeline/alerting -
no extra API layer needed for this prototype. Plate crops and annotated
frames are read from dashboard/evidence_images/ (written as a side effect
by analytics/anpr_pipeline.py via dashboard/evidence_capture.py).
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from watchlist.db import (
    init_db, recent_alerts, recent_detections, last_seen_per_camera,
    list_watchlist, add_watchlist_entry, get_detection,
)
from vehicle_trace.route_reconstruction import search_plate
from config.ingest_client import get_catalogue

EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence_images"

st.set_page_config(page_title="Sentinel Unified Viewer", layout="wide", page_icon="🛰️")
init_db()

# Re-runs the whole script on a timer so alerts/detections appear without
# the user having to manually refresh the page or click anything.
st_autorefresh(interval=5000, key="live_refresh")

CATEGORY_COLORS = {
    "stolen": "#ef4444",
    "wanted": "#f59e0b",
    "suspect": "#a855f7",
    "missing": "#3b82f6",
}


def _image_path(rel_path: str | None) -> Path | None:
    if not rel_path:
        return None
    p = EVIDENCE_DIR / rel_path
    return p if p.exists() else None


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }

        :root {
            --bg-0: #0a0e14;
            --bg-1: #111823;
            --bg-2: #16202e;
            --border: #1e2a3a;
            --text-hi: #e6edf5;
            --text-mid: #9fb0c6;
            --text-lo: #5c6b86;
            --accent: #3b82f6;
            --accent-glow: rgba(59, 130, 246, 0.15);
            --green: #22c55e;
        }

        .stApp { background: var(--bg-0); }
        section[data-testid="stSidebar"] { background: var(--bg-1); }

        /* Kill Streamlit's default top padding on the main block so our
           header sits flush at the top instead of leaving a dead gap
           above it. */
        div.block-container { padding-top: 1.2rem; }

        /* The header (st.markdown) and the tab bar (st.tabs) each render
           inside their own Streamlit element-container div, which carries
           its own default vertical gap - those two gaps stack between the
           title block and the nav row, which is the dead space this fix
           targets. Collapsing it only for the element-container that
           holds .sentinel-header (scoped via :has(), not applied
           globally) keeps every other tab's internal spacing untouched. */
        div[data-testid="stElementContainer"]:has(.sentinel-header) { margin-bottom: 0 !important; }

        /* Header */
        .sentinel-header {
            display: flex; align-items: baseline; gap: 14px;
            padding: 4px 0 10px 0;
        }
        .sentinel-header .logo { font-size: 22px; font-weight: 700; color: var(--text-hi); letter-spacing: 0.2px; }
        .sentinel-header .logo b { color: var(--accent); }
        .sentinel-header .tagline { font-size: 13px; color: var(--text-lo); font-family: 'JetBrains Mono', monospace; }
        .sentinel-header .live-dot {
            display: inline-block; width: 8px; height: 8px; border-radius: 50%;
            background: var(--green); margin-right: 6px;
            box-shadow: 0 0 8px var(--green); animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

        /* Nav bar - the tab list reads as one integrated bar directly
           under the header, not a plain row of text links floating in
           whitespace: a contained strip with its own background, a
           bottom rule to separate it from page content, and consistent
           padding per tab so each one reads as a nav item. */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background: var(--bg-1);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 5px;
            margin-top: 0;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 500;
            color: var(--text-mid); padding: 9px 18px; border-radius: 7px;
            transition: background 0.15s, color 0.15s;
        }
        .stTabs [data-baseweb="tab"]:hover { background: var(--bg-2); color: var(--text-hi); }
        .stTabs [aria-selected="true"] {
            color: var(--text-hi) !important; background: var(--bg-2);
        }
        .stTabs [data-baseweb="tab-highlight"] { background-color: var(--accent) !important; height: 2.5px; }
        .stTabs [data-baseweb="tab-border"] { display: none; }
        .stTabs { margin-bottom: 4px; }

        /* Cards */
        .sentinel-card {
            background: var(--bg-1); border: 1px solid var(--border); border-radius: 12px;
            padding: 16px; margin-bottom: 12px;
        }
        .sentinel-stat {
            background: var(--bg-1); border: 1px solid var(--border); border-radius: 11px;
            padding: 14px 16px; text-align: center;
        }
        .sentinel-stat .n { font-size: 26px; font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
        .sentinel-stat.live .n { color: var(--green); }
        .sentinel-stat .l { font-size: 11px; color: var(--text-lo); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }

        /* Alert card */
        .alert-card {
            background: var(--bg-1); border-radius: 12px; padding: 14px 16px;
            margin-bottom: 10px; display: flex; gap: 14px; align-items: center;
            border-left: 4px solid var(--cat-color, var(--accent));
        }
        .alert-plate {
            font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700;
            color: var(--text-hi); letter-spacing: 1px;
        }
        .alert-meta { font-size: 12px; color: var(--text-mid); margin-top: 2px; }
        .alert-badge {
            display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px;
            font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;
            background: var(--cat-color, var(--accent)); color: #0a0e14;
        }

        /* Camera card */
        .cam-card {
            background: var(--bg-1); border: 1px solid var(--border); border-radius: 12px;
            padding: 12px; margin-bottom: 12px;
        }
        .cam-card .cam-name { font-weight: 600; color: var(--text-hi); font-size: 14px; }
        .cam-card .cam-id { font-family: 'JetBrains Mono', monospace; color: var(--text-lo); font-size: 11px; }
        .cam-card .cam-plate {
            font-family: 'JetBrains Mono', monospace; color: var(--accent); font-size: 15px;
            font-weight: 700; margin-top: 6px;
        }

        /* Timeline (trace) */
        .timeline-item {
            display: flex; gap: 14px; padding: 12px 0; border-left: 2px solid var(--border);
            margin-left: 8px; padding-left: 20px; position: relative;
        }
        .timeline-item::before {
            content: ''; position: absolute; left: -7px; top: 18px; width: 12px; height: 12px;
            border-radius: 50%; background: var(--accent); border: 2px solid var(--bg-0);
        }
        .timeline-cam { font-weight: 600; color: var(--text-hi); font-size: 14px; }
        .timeline-time { font-family: 'JetBrains Mono', monospace; color: var(--text-lo); font-size: 12px; }

        [data-testid="stMetricValue"] { color: var(--accent); }
        div[data-testid="stForm"] { background: var(--bg-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="sentinel-header">
        <span class="logo">SENTI<b>NEL</b></span>
        <span class="tagline"><span class="live-dot"></span>UNIFIED VIEWING &amp; METADATA ANALYTICS — MODEL 2</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_alerts, tab_cameras, tab_search, tab_feed, tab_watchlist = st.tabs(
    ["🚨 Live Alerts", "📷 Cameras", "🔍 Search / Trace", "📡 Detection Feed", "📋 Watchlist"]
)

# --- Live Alerts -------------------------------------------------------------

with tab_alerts:
    alerts = recent_alerts(limit=200)
    detections_all = recent_detections(limit=500)
    total_dets = len(detections_all)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="sentinel-stat"><div class="n">{len(alerts)}</div><div class="l">Alerts</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="sentinel-stat live"><div class="n">{total_dets}</div><div class="l">Detections</div></div>', unsafe_allow_html=True)
    with c3:
        watchlist_count = len(list_watchlist())
        st.markdown(f'<div class="sentinel-stat"><div class="n">{watchlist_count}</div><div class="l">Watchlist Entries</div></div>', unsafe_allow_html=True)

    st.write("")

    if alerts:
        for a in alerts:
            color = CATEGORY_COLORS.get(a["category"], "#3b82f6")
            det = get_detection(a["detection_id"])
            crop_path = _image_path(det["crop_path"]) if det else None
            frame_path = _image_path(det["annotated_frame_path"]) if det else None

            st.markdown(f'<div style="border-left:4px solid {color}; border-radius:12px; background:#111823; padding:14px 18px; margin-bottom:10px;">', unsafe_allow_html=True)
            img_col, info_col = st.columns([1, 4])
            with img_col:
                if crop_path:
                    st.image(str(crop_path), width=140)
                elif frame_path:
                    st.image(str(frame_path), width=140)
                else:
                    st.markdown('<div style="color:#5c6b86; font-size:12px; padding:20px 0;">No image</div>', unsafe_allow_html=True)
            with info_col:
                ts = pd.to_datetime(a["created_at"], unit="s").strftime("%Y-%m-%d %H:%M:%S UTC")
                st.markdown(
                    f'<span class="alert-badge" style="--cat-color:{color};">{html.escape(a["category"])}</span>&nbsp;&nbsp;'
                    f'<span class="alert-plate">{html.escape(a["plate"])}</span>'
                    f'<div class="alert-meta">📍 {html.escape(a["location"])} ({html.escape(a["camera_id"])}) &nbsp;·&nbsp; 🕐 {ts} '
                    f'&nbsp;·&nbsp; match {a["match_confidence"]:.0f}%</div>'
                    f'<div class="alert-meta" style="margin-top:4px;">{html.escape(a["reason"])}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No alerts yet. Alerts appear here automatically when a detected plate matches the watchlist.")

# --- Cameras -----------------------------------------------------------------

with tab_cameras:
    try:
        cams = get_catalogue(prefer_cache=True)
    except FileNotFoundError:
        cams = []

    last_seen = {row["camera_id"]: dict(row) for row in last_seen_per_camera()}

    if cams:
        cols = st.columns(3)
        for i, c in enumerate(cams):
            seen = last_seen.get(c.camera_id)
            with cols[i % 3]:
                st.markdown('<div class="cam-card">', unsafe_allow_html=True)
                if seen and seen.get("crop_path"):
                    thumb = _image_path(seen["crop_path"])
                    if thumb:
                        st.image(str(thumb), use_container_width=True)
                st.markdown(
                    f'<div class="cam-name">{html.escape(c.location)}</div>'
                    f'<div class="cam-id">{html.escape(c.camera_id)}</div>',
                    unsafe_allow_html=True,
                )
                if seen:
                    conf = seen.get("ocr_confidence")
                    conf_str = f" ({conf:.0%})" if conf is not None else ""
                    st.markdown(f'<div class="cam-plate">{html.escape(seen["plate"])}{conf_str}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#5c6b86; font-size:12px; margin-top:6px;">No detections yet</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with_coords = [c for c in cams if "lat" in c.extra and "lon" in c.extra]
        if with_coords:
            st.subheader("Camera Map")
            map_df = pd.DataFrame([
                {"lat": c.extra["lat"], "lon": c.extra["lon"]} for c in with_coords
            ])
            st.map(map_df)
    else:
        st.warning(
            "No camera catalogue cached yet. Set SENTINEL_EMAIL/SENTINEL_PASSWORD and run "
            "`python -m config.ingest_client` once to populate it."
        )

# --- Search / Trace ------------------------------------------------------------

with tab_search:
    st.subheader("Search by Plate Number")
    query = st.text_input("Plate number", placeholder="e.g. GJ05AB1234", label_visibility="collapsed")
    if query:
        stops = search_plate(query)
        if stops:
            cams_seen = len(set(s.camera_id for s in stops))
            st.success(f"{len(stops)} detection(s) across {cams_seen} camera(s) — route reconstructed in chronological order.")

            for s in stops:
                crop = _image_path(s.crop_path)
                st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
                cols = st.columns([1, 5])
                with cols[0]:
                    if crop:
                        st.image(str(crop), width=100)
                with cols[1]:
                    st.markdown(
                        f'<div class="timeline-cam">📍 {html.escape(s.location)} <span style="color:#5c6b86; font-weight:400;">({html.escape(s.camera_id)})</span></div>'
                        f'<div class="timeline-time">{s.wall_clock_iso} &nbsp;·&nbsp; plate read: <b style="color:#e6edf5;">{html.escape(s.plate)}</b> '
                        f'&nbsp;·&nbsp; confidence {s.ocr_confidence:.0%}</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No detections found for this plate.")

# --- Detection Feed ------------------------------------------------------------

with tab_feed:
    st.caption("Live-updating stream of the most recent detections across all active cameras — watch the AI working in real time.")
    recent = recent_detections(limit=12)
    if recent:
        for d in recent:
            crop = _image_path(d["crop_path"])
            frame = _image_path(d["annotated_frame_path"])
            st.markdown('<div class="sentinel-card">', unsafe_allow_html=True)
            cols = st.columns([1, 1, 3])
            with cols[0]:
                if crop:
                    st.image(str(crop), caption="plate crop", use_container_width=True)
                else:
                    st.markdown('<div style="color:#5c6b86; font-size:12px;">no crop saved</div>', unsafe_allow_html=True)
            with cols[1]:
                if frame:
                    st.image(str(frame), caption="annotated frame", use_container_width=True)
            with cols[2]:
                ts = pd.to_datetime(d["wall_clock_s"], unit="s").strftime("%Y-%m-%d %H:%M:%S UTC")
                st.markdown(
                    f'<div class="alert-plate">{html.escape(d["plate"])}</div>'
                    f'<div class="alert-meta">📍 {html.escape(d["location"])} ({html.escape(d["camera_id"])})<br>'
                    f'🕐 {ts}<br>'
                    f'OCR confidence: <b style="color:#22c55e;">{d["ocr_confidence"]:.0%}</b> &nbsp;·&nbsp; '
                    f'Detector confidence: {d["detector_confidence"]:.0%}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No detections yet.")

# --- Watchlist ---------------------------------------------------------------

with tab_watchlist:
    st.subheader("Watchlist Database")
    entries = list_watchlist()
    if entries:
        df = pd.DataFrame([dict(e) for e in entries])
        df["date_added"] = pd.to_datetime(df["date_added"], unit="s")
        st.dataframe(df[["plate", "category", "reason", "date_added"]], use_container_width=True, hide_index=True)
    else:
        st.info("Watchlist is empty.")

    with st.form("add_watchlist"):
        st.write("Add entry")
        plate = st.text_input("Plate")
        reason = st.text_input("Reason")
        category = st.selectbox("Category", ["wanted", "stolen", "suspect", "missing"])
        submitted = st.form_submit_button("Add")
        if submitted and plate and reason:
            add_watchlist_entry(plate, reason, category)
            st.success(f"Added {plate.upper()} to watchlist.")
            st.rerun()
