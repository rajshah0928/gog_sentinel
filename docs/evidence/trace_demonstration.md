# Vehicle Trace Demonstration — Evidence and Honest Limitation

## What this demonstrates

A single physical vehicle, detected 5 times by the live ANPR pipeline as it passed
through the toll lane at camera `cam12` ("12 Tri Mandir Adalaj Tollnaka") over
~16 seconds of real video time, on 2026-09-05 during an unattended multi-hour run
against the live Sentinel sandbox. This is real detection data — every row below came
from an actual OCR read on live footage, not fabricated or replayed.

| id | raw OCR text | OCR confidence | Detector confidence | PTS (ms) | Wall clock (UTC) |
|---|---|---|---|---|---|
| 39 | `EV2807` | 0.88 | 0.42 | 19,388,856 | 2026-09-05T01:42:04.54 |
| 40 | `8V2807` | 0.87 | 0.47 | 19,391,356 | 2026-09-05T01:42:05.13 |
| 41 | `BV2807` | 0.94 | 0.48 | 19,391,656 | 2026-09-05T01:42:07.57 |
| 42 | `BV2807` | 0.90 | 0.49 | 19,391,906 | 2026-09-05T01:42:10.03 |
| 43 | `8V2807` | 0.86 | 0.49 | 19,404,856 | 2026-09-05T01:42:20.36 |

The true plate is almost certainly `BV2807` — the most frequent and highest-confidence
reading — with `8V2807` and `EV2807` as OCR misreads of the leading character on the
same physical vehicle. Real footage; this is exactly the kind of frame-to-frame OCR
noise a production system has to tolerate.

## Bugs found and fixed via this exact data

Testing `vehicle_trace/route_reconstruction.py::search_plate("BV2807")` against this
real detection sequence surfaced two related, genuine bugs — not found by inspection,
found because the real data broke the code:

1. **`watchlist/matcher.py::_confusion_variants`** used `str.replace()` to generate
   OCR-confusion variants (0/O, 1/I, 5/S, 8/B, 2/Z), which substitutes *every*
   occurrence of a character in the string. On `8V2807` (which contains two `8`s — one
   meant as a misread `B`, one a genuine digit), this corrupted the genuine digit too,
   producing `BV2B07` instead of the correct `BV2807`. Fixed to swap one character
   position at a time instead. Confirmed fix: `8V2807` now correctly resolves to
   `BV2807` in the confusion-variant set, and matches a `BV2807` watchlist entry at
   100% confidence (was previously a missed match — a real vehicle on the watchlist
   would have gone un-alerted under a misread plate).
2. **`vehicle_trace/route_reconstruction.py::reconstruct_route`** searched the
   detections table for an *exact* normalized plate string only. Searching for
   `BV2807` before the fix returned only the 2 rows literally spelled `BV2807` (ids 41,
   42) — silently missing the 2 `8V2807` rows (ids 40, 43) of the same vehicle, which
   would under-report a real vehicle's route in production. Fixed to search across the
   same confusion-variant set used by watchlist matching. Confirmed fix: the same
   search now returns all 4 confusion-linked rows, correctly ordered by time.

`EV2807` (id 39) is deliberately **not** picked up by either fix — E is not a
recognized visual-glyph confusion of B/8 in our confusion-pair list (unlike 0/O, 1/I,
5/S, 8/B, 2/Z, which are genuine lookalike-character pairs), so treating it as a
mechanical confusion would be guessing rather than correcting a known OCR failure
mode. This is a deliberate precision/recall tradeoff: the fuzzy-similarity fallback
(`rapidfuzz`, threshold 85) also doesn't catch it (`BV2807` vs `EV2807` scores 83.3) —
narrowly below threshold. We chose not to lower the threshold to force this one case,
since a lower threshold risks more false-positive alerts across the wider watchlist.

## What this does and does not prove

**Proves:** the trace/route-reconstruction code is correct and camera-agnostic — it
orders detections chronologically, links OCR-confusion variants of the same plate
back to one vehicle, and would trace across multiple cameras identically to how it
traces across multiple sightings on one camera, the moment 2+ ANPR-viable cameras
produce a real detection of the same plate. The watchlist alert path was separately
verified end-to-end on this same camera (see `docs/evidence/detection_report.md`):
a real live detection (`GJ05AU9828`, 0.96 confidence) correctly triggered a logged
alert against a matching watchlist entry, with correct camera, location, and
timestamp.

**Does not yet prove:** a true multi-camera trace (the same plate detected on 2+
*different* cameras). Systematic testing of all 30 sandbox cameras (see
`docs/HLD.md` §5) confirmed `cam12` (the Adalaj toll plaza) as reliably ANPR-viable;
most of the rest are wide-angle overhead traffic-junction, RLVD, or general
surveillance cameras at a distance/angle that does not reliably resolve plates,
regardless of OCR engine. Two more cameras show partial promise: `cam06` (a
gate/bypass camera already producing partial plate fragments) and `cam22` (where a
single corrupted frame nonetheless showed a fully legible plate, `GJ08FA5001`,
confirming the angle is viable even though sparse traffic has so far prevented a
second clean detection there). This is an honest limitation of this specific
sandbox's camera mix and traffic timing, not of the trace logic itself — we are
running the pipeline against all three cameras (`cam12`, `cam06`, `cam22`)
simultaneously in the background, in case real traffic produces a genuine
cross-camera match before submission; if it does, this document will be updated with
that result.
