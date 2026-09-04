"""
Minimal Streamlit dashboard: live alerts, camera list with last-seen plate,
plate search / route reconstruction, and a simple map of camera locations.

Run with: streamlit run dashboard/app.py
Reads directly from the SQLite DB written by the ANPR pipeline/alerting -
no extra API layer needed for this prototype.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from watchlist.db import init_db, recent_alerts, last_seen_per_camera, list_watchlist, add_watchlist_entry
from vehicle_trace.route_reconstruction import search_plate
from config.ingest_client import get_catalogue

st.set_page_config(page_title="Sentinel Unified Viewer", layout="wide")
init_db()

# Re-runs the whole script on a timer so alerts/detections appear without
# the user having to manually refresh the page or click anything.
st_autorefresh(interval=5000, key="live_refresh")

st.title("Sentinel — Unified Viewing & Metadata Analytics")
st.caption("Model 2 prototype: direct RTSP/ANPR integration, no federation layer")

tab_alerts, tab_cameras, tab_search, tab_watchlist = st.tabs(
    ["Live Alerts", "Cameras", "Search / Trace Vehicle", "Watchlist"]
)

with tab_alerts:
    st.subheader("Recent Alerts")
    alerts = recent_alerts(limit=200)
    if alerts:
        df = pd.DataFrame([dict(a) for a in alerts])
        df["created_at"] = pd.to_datetime(df["created_at"], unit="s")
        st.dataframe(
            df[["created_at", "plate", "camera_id", "location", "category", "reason", "match_confidence"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No alerts yet. Alerts appear here automatically when a detected plate matches the watchlist.")

with tab_cameras:
    st.subheader("Camera Grid")
    try:
        cams = get_catalogue(prefer_cache=True)
    except FileNotFoundError:
        cams = []

    last_seen = {row["camera_id"]: dict(row) for row in last_seen_per_camera()}

    if cams:
        rows = []
        for c in cams:
            seen = last_seen.get(c.camera_id)
            rows.append({
                "camera_id": c.camera_id,
                "location": c.location,
                "codec": c.codec,
                "live": c.live,
                "last_plate_seen": seen["plate"] if seen else "",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with_coords = [c for c in cams if "lat" in c.extra and "lon" in c.extra]
        if with_coords:
            st.subheader("Camera Map")
            map_df = pd.DataFrame([
                {"lat": c.extra["lat"], "lon": c.extra["lon"]} for c in with_coords
            ])
            st.map(map_df)
    else:
        st.warning(
            "No camera catalogue cached yet. Set SENTINEL_HOST and run "
            "`python -m config.ingest_client` once to populate it."
        )

with tab_search:
    st.subheader("Search by Plate Number")
    query = st.text_input("Plate number", placeholder="e.g. GJ05AB1234")
    if query:
        stops = search_plate(query)
        if stops:
            st.success(f"{len(stops)} detection(s) found — route reconstructed below (chronological order).")
            df = pd.DataFrame([{
                "seen_at": s.wall_clock_iso,
                "camera_id": s.camera_id,
                "location": s.location,
                "pts_ms": s.pts_ms,
                "ocr_confidence": round(s.ocr_confidence, 2),
            } for s in stops])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No detections found for this plate.")

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
