"""
Plate text normalization and fuzzy matching against the watchlist.

Indian plates follow (roughly) SS DD LL(L) DDDD — e.g. "GJ 05 AB 1234".
OCR on cropped, motion-blurred, variably-lit plate crops commonly confuses:
  0/O, 1/I, 5/S, 8/B, 2/Z
We don't try to fully solve segmentation-aware correction (no per-position
character-class model here, given time constraints); instead we normalize
to a canonical alnum-uppercase form and rely on fuzzy string matching with
a high similarity threshold to absorb 1-2 character OCR errors.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from rapidfuzz import fuzz

from watchlist.db import list_watchlist

_STRIP_RE = re.compile(r"[^A-Z0-9]")

# Applied only as a *last-resort* fuzzy fallback score booster, not a
# rewrite of the OCR text — we match against both the raw normalized string
# and don't attempt to guess which characters were letters vs digits.
_CONFUSION_PAIRS = [("O", "0"), ("I", "1"), ("S", "5"), ("B", "8"), ("Z", "2")]

FUZZY_MATCH_THRESHOLD = 85.0  # rapidfuzz ratio 0-100


def normalize_plate(raw_text: str) -> str:
    """Uppercase, strip whitespace/punctuation/OCR noise characters."""
    return _STRIP_RE.sub("", raw_text.upper())


def _confusion_variants(plate: str) -> set[str]:
    """
    Generates plausible OCR-confusion variants of a normalized plate by
    swapping one character position at a time, so an exact-match fast path
    can catch the common single-character confusions without a full fuzzy
    scan.

    Deliberately per-position, not str.replace(): replace() substitutes
    every occurrence of a character in the string, so on a plate like
    "8V2807" (two '8's — one meant as a letter, one a genuine digit),
    replace("8","B") corrupts the real digit too, producing "BV2B07"
    instead of the intended "BV2807" — a real bug found via a live
    detection (the same physical vehicle's plate OCR'd as EV2807, 8V2807,
    and BV2807 within seconds of each other; only the position-aware
    version below correctly links all three back to one plate).
    """
    confusable = {a for a, _ in _CONFUSION_PAIRS} | {b for _, b in _CONFUSION_PAIRS}
    pair_map: dict[str, str] = {}
    for a, b in _CONFUSION_PAIRS:
        pair_map[a] = b
        pair_map[b] = a

    variants = {plate}
    for i, ch in enumerate(plate):
        if ch in confusable:
            swapped = plate[:i] + pair_map[ch] + plate[i + 1:]
            variants.add(swapped)
    return variants


@dataclass
class MatchResult:
    watchlist_id: int
    watchlist_plate: str
    reason: str
    category: str
    confidence: float  # 0-100 similarity


def match_against_watchlist(ocr_plate_raw: str) -> Optional[MatchResult]:
    """
    Normalizes the OCR'd plate text and checks it against every watchlist
    entry, first via exact/confusion-variant match (cheap, high precision),
    then via fuzzy ratio for anything else. Returns the best match above
    FUZZY_MATCH_THRESHOLD, or None.
    """
    normalized = normalize_plate(ocr_plate_raw)
    if not normalized:
        return None

    entries = list_watchlist()
    if not entries:
        return None

    variants = _confusion_variants(normalized)
    for entry in entries:
        entry_plate = normalize_plate(entry["plate"])
        if entry_plate in variants:
            return MatchResult(
                watchlist_id=entry["id"],
                watchlist_plate=entry["plate"],
                reason=entry["reason"],
                category=entry["category"],
                confidence=100.0,
            )

    best: Optional[MatchResult] = None
    for entry in entries:
        entry_plate = normalize_plate(entry["plate"])
        score = fuzz.ratio(normalized, entry_plate)
        if score >= FUZZY_MATCH_THRESHOLD and (best is None or score > best.confidence):
            best = MatchResult(
                watchlist_id=entry["id"],
                watchlist_plate=entry["plate"],
                reason=entry["reason"],
                category=entry["category"],
                confidence=score,
            )
    return best
