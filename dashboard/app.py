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
import pydeck as pdk
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from watchlist.db import (
    init_db, recent_alerts, recent_detections, last_seen_per_camera,
    list_watchlist, add_watchlist_entry, get_detection,
)
from vehicle_trace.route_reconstruction import search_plate
from config.ingest_client import get_catalogue
from registry.db import (
    init_registry_db, list_registry, upsert_registry_entry, RegistryEntry,
    get_cached_geocode, cache_geocode, DEFAULT_STORAGE_NOTE,
)
from registry.sync import sync_registry_from_catalogue
from registry.inference import infer_department, infer_camera_type, geocode_location, is_anpr_viable_type
from registry.gap_analysis import compute_gap_analysis
from registry.bulk_import import import_cameras_csv
from registry.map_helpers import build_registry_scatter_layer, build_route_layers, make_deck

EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence_images"

st.set_page_config(page_title="Sentinel Unified Viewer", layout="wide", page_icon="🛰️")
init_db()
init_registry_db()

# Re-runs the whole script on a timer so alerts/detections appear without
# the user having to manually refresh the page or click anything.
st_autorefresh(interval=15000, key="live_refresh")

if "registry_synced" not in st.session_state:
    # Sync once per browser session, not on every 5s autorefresh — the
    # underlying catalogue rarely changes mid-session, and re-syncing
    # every tick would add avoidable load for no benefit.
    try:
        sync_registry_from_catalogue(prefer_cache=True)
    except Exception:
        pass
    st.session_state["registry_synced"] = True


if "failed_geocodes" not in st.session_state:
    # Locations that failed to geocode are retried at most once per browser
    # session, not on every 5s autorefresh — a live Nominatim lookup (with
    # its own retry/timeout chain) on every rerun for the same known-bad
    # name was adding several seconds to every tick.
    st.session_state["failed_geocodes"] = set()


def _registry_points_with_coords() -> list[dict]:
    """
    Joins registry rows with cached geocodes, geocoding on the fly (and
    caching the result) for any row not yet resolved. Rows that still can't
    be geocoded are skipped from the map (but still show up in the table/
    gap-analysis, which don't need coordinates).
    """
    points = []
    for r in list_registry():
        cached = get_cached_geocode(r["display_name"])
        if cached:
            lat, lon = cached["lat"], cached["lon"]
        elif r["display_name"] in st.session_state["failed_geocodes"]:
            continue
        else:
            coord = geocode_location(r["display_name"])
            if not coord:
                st.session_state["failed_geocodes"].add(r["display_name"])
                continue
            lat, lon = coord
            cache_geocode(r["display_name"], lat, lon, is_approximate=True)
        points.append({
            "camera_id": r["camera_id"],
            "display_name": r["display_name"],
            "department": r["department"],
            "camera_type": r["camera_type"],
            "connectivity_status": r["connectivity_status"],
            "last_seen": r["last_seen"],
            "lat": lat,
            "lon": lon,
        })
    return points

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

tab_alerts, tab_cameras, tab_search, tab_feed, tab_watchlist, tab_registry = st.tabs(
    ["🚨 Live Alerts", "📷 Cameras", "🔍 Search / Trace", "📡 Detection Feed", "📋 Watchlist", "🗺️ Registry"]
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

            view_list, view_map = st.tabs(["List", "Map"])

            with view_list:
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

            with view_map:
                # Reuses vehicle_trace.route_reconstruction's existing output
                # (stops, already chronologically ordered) — this only adds a
                # map rendering of that same data, no new trace/matching logic.
                registry_by_id = {r["camera_id"]: r for r in list_registry()}
                route_points = []
                missing_coords = []
                for i, s in enumerate(stops, start=1):
                    reg = registry_by_id.get(s.camera_id)
                    loc_name = reg["display_name"] if reg else s.location
                    cached = get_cached_geocode(loc_name)
                    if not cached and loc_name not in st.session_state["failed_geocodes"]:
                        coord = geocode_location(loc_name)
                        if coord:
                            cache_geocode(loc_name, coord[0], coord[1], is_approximate=True)
                            cached = {"lat": coord[0], "lon": coord[1]}
                        else:
                            st.session_state["failed_geocodes"].add(loc_name)
                    if not cached:
                        missing_coords.append(s.camera_id)
                        continue
                    route_points.append({
                        "seq": i,
                        "camera_id": s.camera_id,
                        "location": s.location,
                        "wall_clock_iso": s.wall_clock_iso,
                        "lat": cached["lat"],
                        "lon": cached["lon"],
                    })

                if route_points:
                    if len(route_points) == 1:
                        st.caption("Single-camera detection only — shown as one point, no route line.")
                    else:
                        st.caption("Route shown in chronological order (line connects detections by time, not necessarily by road).")
                    layers = build_route_layers(route_points)
                    tooltip_html = "<b>{camera_id}</b><br/>{location}<br/>{wall_clock_iso}"
                    deck = make_deck(layers, points_for_viewport=route_points, tooltip_html=tooltip_html)
                    st.pydeck_chart(deck, height=450)
                else:
                    st.info("No coordinates available for this route's camera(s) yet.")
                if missing_coords:
                    st.caption(f"No coordinates resolved for: {', '.join(missing_coords)} — omitted from the map, still shown in the List view.")
                st.caption("Coordinates are approximate (geocoded from location name), not department-supplied camera GPS — see Registry tab / HLD for detail.")
        else:
            st.warning("No detections found for this plate.")

# --- Detection Feed ------------------------------------------------------------

with tab_feed:
    st.caption("Live-updating stream of the most recent detections across all active cameras — watch the AI working in real time.")
    viable_camera_ids = {r["camera_id"] for r in list_registry() if is_anpr_viable_type(r["camera_type"])}
    recent_pool = recent_detections(limit=200)
    recent = [d for d in recent_pool if d["camera_id"] in viable_camera_ids][:12]
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

# --- Registry (Model 1 foundation) --------------------------------------------

with tab_registry:
    st.caption(
        "Model 1 (Registry & GIS Foundation) — a minimal foundation layer under our "
        "primary Model 2 submission, per the portal's requirement that every "
        "submission include it. Department, camera type, and map coordinates below "
        "are **illustrative**, inferred from location-name patterns and geocoding — "
        "not department-supplied ownership or GPS data. See the HLD for detail."
    )

    reg_rows = list_registry()

    if not reg_rows:
        st.info("Registry is empty — it populates automatically from the live camera catalogue.")
    else:
        # --- summary stats ---
        gap = compute_gap_analysis()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="sentinel-stat"><div class="n">{gap.total_cameras}</div><div class="l">Registered Cameras</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="sentinel-stat"><div class="n">{gap.disconnected_count}</div><div class="l">Disconnected</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="sentinel-stat"><div class="n">{gap.stale_count}</div><div class="l">No Detections in {gap.stale_hours_threshold:.0f}h</div></div>', unsafe_allow_html=True)
        with c4:
            viable_types = sum(v["count"] for v in gap.by_type.values() if v["anpr_viable"])
            st.markdown(f'<div class="sentinel-stat live"><div class="n">{viable_types}</div><div class="l">ANPR-Viable (by type)</div></div>', unsafe_allow_html=True)

        st.write("")
        st.subheader("Camera Map")
        color_by = st.radio("Color markers by", ["Connectivity", "Camera type"], horizontal=True, label_visibility="collapsed")
        map_points = _registry_points_with_coords()
        if map_points:
            layer = build_registry_scatter_layer(map_points, color_by="connectivity" if color_by == "Connectivity" else "type")
            tooltip_html = (
                "<b>{camera_id}</b> — {display_name}<br/>"
                "Dept: {department} &nbsp; Type: {camera_type}<br/>"
                "Status: {connectivity_status}"
            )
            deck = make_deck([layer], points_for_viewport=map_points, tooltip_html=tooltip_html)
            st.pydeck_chart(deck, height=450)
            n_missing = len(reg_rows) - len(map_points)
            if n_missing:
                st.caption(f"{n_missing} camera(s) omitted from the map — location name could not be geocoded.")
        else:
            st.info("No camera coordinates resolved yet.")
        st.caption("Coordinates are approximate (place-name geocoding via OpenStreetMap), not department-supplied GPS.")

        st.write("")
        st.subheader("Gap Analysis")
        gc1, gc2 = st.columns(2)
        with gc1:
            st.markdown("**Disconnected cameras**")
            if gap.disconnected_ids:
                st.write(", ".join(gap.disconnected_ids))
            else:
                st.caption("None currently disconnected.")
        with gc2:
            st.markdown(f"**No plate read in the last {gap.stale_hours_threshold:.0f}h**")
            if gap.stale_ids:
                st.write(", ".join(gap.stale_ids))
            else:
                st.caption("All cameras have recent detections.")

        st.markdown("**ANPR viability by camera type**")
        st.caption(
            "Reuses our earlier plate-legibility finding: close-range, vehicle-facing "
            "installations (toll/gate/bypass) are ANPR-viable; wide-angle junction/"
            "situational cameras typically aren't, without a closer secondary camera."
        )
        type_df = pd.DataFrame([
            {
                "camera_type": t,
                "count": v["count"],
                "anpr_viable": "Yes" if v["anpr_viable"] else "Situational only",
                "with_detections": v["with_detections"],
            }
            for t, v in gap.by_type.items()
        ])
        st.dataframe(type_df, use_container_width=True, hide_index=True)

        st.write("")
        st.subheader("Registry Table")
        reg_df = pd.DataFrame([dict(r) for r in reg_rows])
        reg_df["last_seen"] = pd.to_datetime(reg_df["last_seen"], unit="s", errors="coerce")
        st.dataframe(
            reg_df[["camera_id", "display_name", "department", "camera_type", "connectivity_status", "last_seen", "source"]],
            use_container_width=True, hide_index=True,
        )

    st.write("")
    st.subheader("Onboard a Camera")
    onboard_manual, onboard_csv = st.tabs(["Manual Entry", "CSV Bulk Import"])

    with onboard_manual:
        with st.form("add_registry_camera"):
            st.write("Add one camera's metadata manually")
            m_id = st.text_input("Camera ID", placeholder="e.g. cam31")
            m_name = st.text_input("Display name / location", placeholder="e.g. 31 Example Junction")
            m_dept = st.text_input("Department (optional — inferred if left blank)")
            m_type = st.selectbox("Camera type", ["", "toll", "gate", "bypass", "junction", "transport-facility", "administrative"])
            m_submitted = st.form_submit_button("Add camera")
            if m_submitted:
                if not m_id.strip() or not m_name.strip():
                    st.error("Camera ID and display name are required.")
                else:
                    cam_type = m_type or infer_camera_type(m_name)
                    dept = m_dept.strip() or infer_department(m_name, cam_type)
                    upsert_registry_entry(RegistryEntry(
                        camera_id=m_id.strip(),
                        display_name=m_name.strip(),
                        department=dept,
                        camera_type=cam_type,
                        connectivity_status="unknown",
                        last_seen=None,
                        storage_details=DEFAULT_STORAGE_NOTE,
                        source="manual",
                    ))
                    st.success(f"Added {m_id.strip()} to the registry.")
                    st.rerun()

    with onboard_csv:
        st.caption(
            "Demonstrates bulk-onboarding cameras not present in the live gateway "
            "catalogue. Required columns: camera_id, display_name. Optional: "
            "department, camera_type, storage_details (inferred/defaulted if omitted)."
        )
        sample_csv_path = Path(__file__).resolve().parent.parent / "registry" / "sample_data" / "sample_camera_import.csv"
        if sample_csv_path.exists():
            st.caption(f"Sample file available at `{sample_csv_path.relative_to(Path(__file__).resolve().parent.parent)}`")
        uploaded = st.file_uploader("Upload cameras CSV", type=["csv"])
        if uploaded is not None:
            tmp_path = Path("/tmp") / f"registry_import_{uploaded.name}"
            tmp_path.write_bytes(uploaded.getvalue())
            try:
                n_imported, errors = import_cameras_csv(tmp_path)
                st.success(f"Imported {n_imported} camera(s).")
                for e in errors:
                    st.warning(e)
                if n_imported:
                    st.rerun()
            except ValueError as e:
                st.error(str(e))
