"""
Shared pydeck layer-building helpers for the Registry/Map tab (camera
locations, colored by connectivity/type) and the Search/Trace map view
(a plate's route across cameras). Kept separate from dashboard/app.py so
both call sites share one rendering convention instead of duplicating
pydeck boilerplate.
"""
from __future__ import annotations

import pydeck as pdk

# Approximate center of Gujarat, used only as the map's initial viewport
# when we have no camera coordinates yet.
GUJARAT_CENTER = {"lat": 22.6, "lon": 71.6, "zoom": 6.2}

CONNECTIVITY_COLORS = {
    "connected": [34, 197, 94],       # green
    "disconnected": [239, 68, 68],    # red
    "unknown": [148, 163, 184],       # gray
}

TYPE_COLORS = {
    "toll": [245, 158, 11],           # amber
    "gate": [59, 130, 246],           # blue
    "bypass": [168, 85, 247],         # purple
    "junction": [148, 163, 184],      # gray
    "transport-facility": [245, 158, 11],
    "administrative": [34, 197, 94],
}


def build_registry_scatter_layer(points: list[dict], color_by: str = "connectivity") -> pdk.Layer:
    """
    points: list of dicts with at minimum lat, lon, camera_id, display_name,
    connectivity_status, camera_type — as prepared by the dashboard from
    registry rows joined with geocode cache rows.
    """
    palette = CONNECTIVITY_COLORS if color_by == "connectivity" else TYPE_COLORS
    key = "connectivity_status" if color_by == "connectivity" else "camera_type"
    data = []
    for p in points:
        color = palette.get(p.get(key), [148, 163, 184])
        data.append({**p, "color": color})
    return pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius=350,
        radius_min_pixels=6,
        radius_max_pixels=18,
        pickable=True,
        stroked=True,
        get_line_color=[10, 14, 20],
        line_width_min_pixels=1,
    )


def build_route_layers(stops: list[dict]) -> list[pdk.Layer]:
    """
    stops: chronologically-ordered list of dicts with lat, lon, camera_id,
    location, wall_clock_iso, seq (1-indexed order). Returns a point layer
    for every stop plus (only if >1 distinct coordinate) a path layer
    connecting them in order, so a single-camera-only trace renders as one
    clearly visible point rather than a degenerate/invisible line.
    """
    layers = []
    if not stops:
        return layers

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=stops,
        get_position="[lon, lat]",
        get_fill_color=[59, 130, 246],
        get_radius=450,
        radius_min_pixels=8,
        radius_max_pixels=22,
        pickable=True,
        stroked=True,
        get_line_color=[10, 14, 20],
        line_width_min_pixels=2,
    )
    layers.append(point_layer)

    distinct_coords = {(s["lat"], s["lon"]) for s in stops}
    if len(stops) > 1 and len(distinct_coords) > 1:
        path = [[s["lon"], s["lat"]] for s in stops]
        path_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": path}],
            get_path="path",
            get_color=[59, 130, 246, 160],
            get_width=4,
            width_min_pixels=2,
        )
        layers.append(path_layer)

    return layers


def make_deck(layers: list[pdk.Layer], points_for_viewport: list[dict] | None = None, tooltip_html: str = None) -> pdk.Deck:
    if points_for_viewport:
        lats = [p["lat"] for p in points_for_viewport]
        lons = [p["lon"] for p in points_for_viewport]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        zoom = 10.5 if len(points_for_viewport) == 1 else 7.0
    else:
        center_lat, center_lon, zoom = GUJARAT_CENTER["lat"], GUJARAT_CENTER["lon"], GUJARAT_CENTER["zoom"]

    view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom)
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_provider="carto",
        map_style="dark",
        tooltip={"html": tooltip_html} if tooltip_html else True,
    )
