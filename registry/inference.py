"""
Illustrative metadata inference for the registry.

The government catalogue (config/ingest_client.py -> cameras.json) gives us
only camera_id and a location/display name — no department, camera-type, or
geo-coordinate fields. Rather than leaving those blank or hand-typing 30
guesses, we infer them from the location-name pattern using the same
naming-convention approach already validated in docs/HLD.md's plate-
legibility findings (e.g. "Tollnaka" identifying cam12 as a toll-plaza
camera, which turned out to be the ANPR-viable one).

This is explicitly an illustrative mapping, not real department-supplied
data — every place this module's output is displayed (dashboard, HLD, PPT)
must say so.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Optional

import requests

logger = logging.getLogger("sentinel.registry.inference")

# --- department / camera_type inference -------------------------------------

_TOLL_PAT = re.compile(r"\btoll(naka)?\b", re.IGNORECASE)
_GATE_PAT = re.compile(r"\bgate\b", re.IGNORECASE)
_BYPASS_PAT = re.compile(r"\bbypass\b", re.IGNORECASE)
_JUNCTION_PAT = re.compile(r"\b(circle|char\s*rasta|chowk|junction|crossing|rasta|bridge|tran\s*rasta)\b", re.IGNORECASE)
_RTO_PAT = re.compile(r"\b(rto|transport|bus\s*port|bus\s*stand)\b", re.IGNORECASE)
_PANCHAYAT_PAT = re.compile(r"\b(gram\s*panchayat|panchayat)\b", re.IGNORECASE)


def infer_camera_type(location: str) -> str:
    """
    Best-effort camera_type from the location-name pattern only. Same
    approach as the HLD's ANPR-viability triage: toll plazas and gates are
    typically narrow, close-range, vehicle-facing (ANPR-viable); junctions/
    circles are typically wide-angle situational cameras.
    """
    loc = location or ""
    if _TOLL_PAT.search(loc):
        return "toll"
    if _GATE_PAT.search(loc):
        return "gate"
    if _BYPASS_PAT.search(loc):
        return "bypass"
    if _RTO_PAT.search(loc):
        return "transport-facility"
    if _PANCHAYAT_PAT.search(loc):
        return "administrative"
    if _JUNCTION_PAT.search(loc):
        return "junction"
    return "junction"  # most conservative default: treat as wide-angle/situational


# camera_type -> whether that category is typically ANPR-viable (close,
# vehicle-facing) vs situational-only (wide-angle scene coverage). This is
# the same distinction the plate-legibility soak test found empirically for
# cam12 (toll)/cam06 (gate)/cam22 (bypass) vs the wide junction cameras.
ANPR_VIABLE_TYPES = {"toll", "gate", "bypass"}


def is_anpr_viable_type(camera_type: str) -> bool:
    return camera_type in ANPR_VIABLE_TYPES


def infer_department(location: str, camera_type: Optional[str] = None) -> str:
    """
    Illustrative department mapping, inferred purely from location-name/
    camera_type pattern — not real department-supplied ownership data.
    """
    ctype = camera_type or infer_camera_type(location)
    if ctype in ("toll", "transport-facility"):
        return "Transport"
    if ctype == "administrative":
        return "Panchayat / Local Body"
    # gate / bypass / junction default to Police (traffic + law-and-order
    # cameras are overwhelmingly police-operated in this kind of grid)
    return "Police"


# --- geocoding ---------------------------------------------------------------

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "sentinel-hackathon-prototype/1.0 (Gujarat Police Innovation Challenge 2026 submission)"

# Strip a leading camera-catalogue index like "12 " or "06 " and any
# trailing disambiguator we know isn't a geocodable place fragment.
_LEADING_INDEX_PAT = re.compile(r"^\s*\d+\s+")

# Words describing the camera/installation itself, not the place — these
# help narrow a full-string query but block a match if left in on retries,
# so they're the first thing stripped when trying looser queries.
_INSTALLATION_WORDS = re.compile(
    r"\b(gate|tollnaka|toll|bypass|circle|chowk|char\s*rasta|tran\s*rasta|rasta|"
    r"junction|crossing|bridge|cctv|rlvd|p\d+|teen\s*rasta|showroom|office|"
    r"gram\s*panchayat|panchayat|taluka|district|bus\s*port|bus\s*stand|"
    r"vidhyalaya|park)\b",
    re.IGNORECASE,
)
_PUNCT_PAT = re.compile(r"[.,\-_]+")
_MULTI_SPACE_PAT = re.compile(r"\s+")

# Loose bounding box for Gujarat (with a little margin) — a geocode result
# outside this is almost certainly a false match on an ambiguous short
# place name (e.g. "kheram" resolving to Kashmir) and is rejected rather
# than silently plotted in the wrong state.
_GUJARAT_BBOX = {"lat_min": 20.0, "lat_max": 24.8, "lon_min": 68.0, "lon_max": 74.6}


def _in_gujarat_bbox(lat: float, lon: float) -> bool:
    b = _GUJARAT_BBOX
    return b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]


def _clean_location_for_geocode(location: str) -> str:
    loc = _LEADING_INDEX_PAT.sub("", location or "").strip()
    loc = _PUNCT_PAT.sub(" ", loc)
    loc = _MULTI_SPACE_PAT.sub(" ", loc).strip()
    return loc


def _loosened_query(location: str) -> str:
    """Drops installation-type words, leaving (hopefully) just the place name."""
    loc = _INSTALLATION_WORDS.sub(" ", location)
    loc = _MULTI_SPACE_PAT.sub(" ", loc).strip()
    return loc


def _try_geocode(query: str, timeout_s: float) -> Optional[tuple[float, float]]:
    if not query:
        return None
    try:
        resp = requests.get(
            _NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 1},
            headers={"User-Agent": _USER_AGENT},
            timeout=timeout_s,
        )
        resp.raise_for_status()
        results = resp.json()
        if not results:
            return None
        lat, lon = float(results[0]["lat"]), float(results[0]["lon"])
        if not _in_gujarat_bbox(lat, lon):
            logger.warning("Geocode result for query=%r (%s,%s) falls outside Gujarat bbox, rejected", query, lat, lon)
            return None
        return lat, lon
    except Exception as e:
        logger.warning("Geocode request failed for query=%r: %s", query, e)
        return None


def geocode_location(location: str, timeout_s: float = 8.0) -> Optional[tuple[float, float]]:
    """
    Best-effort geocode of a bare location name via Nominatim (OpenStreetMap),
    biased to Gujarat/India. Returns (lat, lon) or None if it can't resolve.
    This is approximate by construction — a place-name centroid, not a
    department-supplied camera coordinate — callers must treat/label the
    result as illustrative.

    Tries progressively looser queries (full cleaned name -> with
    installation-type words like "gate"/"tollnaka" stripped -> just the
    first word) since these location strings mix a real place name with
    installation descriptors that confuse a geocoder if left in. Every
    candidate result is checked against a Gujarat bounding box and rejected
    if it falls outside — an ambiguous short name (e.g. "kheram") can
    otherwise silently resolve to a same-named place in another state.
    """
    base = _clean_location_for_geocode(location)
    if not base:
        return None

    candidates = [
        f"{base}, Gujarat, India",
        f"{_loosened_query(base)}, Gujarat, India",
        f"{base.split(' ')[0]}, Gujarat, India" if base.split(" ") else None,
    ]
    for query in candidates:
        if not query:
            continue
        result = _try_geocode(query, timeout_s)
        if result:
            return result
    return None
