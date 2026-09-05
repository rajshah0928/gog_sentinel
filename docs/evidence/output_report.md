# Sentinel — Government-Feed Output Report

Generated: 2026-09-05T19:24:28.756166+00:00

Detected vehicles/plates with corresponding timestamps, from the live Sentinel Gujarat sandbox feed (government-provided cameras). Every row is a real detection from the running ANPR pipeline — not simulated or replayed.

## Summary

- **Total detections:** 932
- **Plausible plate reads:** 755 (81% of total) — passes a loose alphanumeric shape check (6-11 characters, contains both letters and digits); the remainder are short OCR fragments, non-plate on-screen text, or the one known overlay-text false positive noted below
- **Cameras onboarded:** cam01, cam02, cam03, cam06, cam12, cam22
- **Watchlist alerts generated:** 2
- **Cross-camera trace evidence:** no plate has yet been confirmed on two different cameras (checked exact + OCR-confusion-variant matching across all plausible-length plates). Strongest trace evidence to date: plate `BV2807` detected 4 times on camera(s) cam12, correctly linked across OCR-confusion variants (see `trace_demonstration.md` for full detail)
- **Known false positive:** 1 detection(s) flagged below are the video overlay's own burned-in timestamp/caption text, not a vehicle plate — kept in the table rather than deleted, so this remains a complete record of every real detection event

## Detections

| Plate | Camera | Location | Timestamp (UTC) | OCR Conf. | Detector Conf. | Alert | Note |
|---|---|---|---|---|---|---|---|
| IJ | cam03 | 03 O.N.G.C. Office | 2026-09-04 17:48:37 UTC | 44% | 45% |  |  |
| 493 | cam03 | 03 O.N.G.C. Office | 2026-09-04 17:57:33 UTC | 51% | 47% |  |  |
| UO6 | cam03 | 03 O.N.G.C. Office | 2026-09-04 17:59:18 UTC | 49% | 61% |  |  |
| 50 | cam02 | 02 Janpath | 2026-09-04 18:07:57 UTC | 89% | 77% |  |  |
| SUIHCARL | cam02 | 02 Janpath | 2026-09-04 18:07:58 UTC | 49% | 62% |  |  |
| SOUIH0 | cam02 | 02 Janpath | 2026-09-04 18:07:58 UTC | 58% | 40% |  |  |
| UO | cam03 | 03 O.N.G.C. Office | 2026-09-04 18:11:09 UTC | 45% | 49% |  |  |
| O | cam03 | 03 O.N.G.C. Office | 2026-09-04 18:11:26 UTC | 48% | 49% |  |  |
| UO | cam03 | 03 O.N.G.C. Office | 2026-09-04 18:33:30 UTC | 49% | 58% |  |  |
| EJ0 | cam01 | 01 Chiman bhai Bridge | 2026-09-04 18:44:27 UTC | 42% | 60% |  |  |
| AOU | cam03 | 03 O.N.G.C. Office | 2026-09-04 18:48:28 UTC | 63% | 42% |  |  |
| 6 | cam03 | 03 O.N.G.C. Office | 2026-09-04 18:59:08 UTC | 47% | 47% |  |  |
| WO | cam03 | 03 O.N.G.C. Office | 2026-09-04 19:01:42 UTC | 41% | 60% |  |  |
| S | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-04 22:59:03 UTC | 92% | 46% |  |  |
| 6346581555 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-04 23:40:02 UTC | 60% | 55% |  |  |
| RJ4EEATS55 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-04 23:40:12 UTC | 64% | 61% |  |  |
| RJ46E41555 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-04 23:40:39 UTC | 91% | 60% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:13:52 UTC | 64% | 58% |  |  |
| CTTEDRORE | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:32:03 UTC | 58% | 51% |  |  |
| E227176778 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:36:45 UTC | 67% | 56% |  |  |
| RATBE2B | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:40:18 UTC | 75% | 47% |  |  |
| CJ57 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:40:40 UTC | 42% | 55% |  |  |
| UAL | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:43:52 UTC | 58% | 50% |  |  |
| P8041F9815NAFE | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:49:30 UTC | 78% | 63% |  |  |
| EUPB3R40KHPEEDT2692 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 00:55:39 UTC | 70% | 54% |  |  |
| GJIBR19828 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:00:05 UTC | 95% | 42% |  |  |
| G3DHT05634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:08:31 UTC | 68% | 63% |  |  |
| 0T1T05614 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:10:47 UTC | 58% | 46% |  |  |
| 022T05634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:10:53 UTC | 76% | 59% |  |  |
| 5327T05634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:11:02 UTC | 91% | 66% |  |  |
| GJ27T05634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:11:32 UTC | 89% | 66% |  |  |
| RTY | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:12:07 UTC | 46% | 42% |  |  |
| CS | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:16:08 UTC | 63% | 53% |  |  |
| GJ05AU9828 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:16:09 UTC | 96% | 46% | 🚨 |  |
| EGOAL69089 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:28:14 UTC | 71% | 58% |  |  |
| 69092 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:28:15 UTC | 54% | 61% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:30:09 UTC | 83% | 58% |  |  |
| 10OC0 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:30:49 UTC | 53% | 40% |  |  |
| EV2807 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:42:04 UTC | 88% | 42% |  |  |
| 8V2807 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:42:05 UTC | 87% | 47% |  |  |
| BV2807 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:42:07 UTC | 94% | 48% |  |  |
| BV2807 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:42:10 UTC | 90% | 49% |  |  |
| 8V2807 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:42:20 UTC | 86% | 49% |  |  |
| Y2359 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:46:15 UTC | 73% | 64% |  |  |
| DULRMI124B2318 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:49:28 UTC | 65% | 44% |  |  |
| MULRMI12482318 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:49:30 UTC | 62% | 46% |  |  |
| 000203973 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:52:17 UTC | 93% | 41% |  |  |
| RJ090F1195 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:54:45 UTC | 84% | 58% |  |  |
| 3J0ZBT5997 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:58:56 UTC | 73% | 53% |  |  |
| GJOZBT8997 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 01:59:13 UTC | 91% | 50% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 02:05:39 UTC | 41% | 46% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 02:06:18 UTC | 62% | 44% |  |  |
| 12371 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 04:21:36 UTC | 86% | 41% |  |  |
| 12371 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 04:21:36 UTC | 92% | 40% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 04:27:52 UTC | 45% | 49% |  |  |
| 0001V9784 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:27:24 UTC | 92% | 61% |  |  |
| 0001V9794 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:29:08 UTC | 88% | 61% |  |  |
| R1158010 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:30:57 UTC | 66% | 54% |  |  |
| SNLI | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:33:27 UTC | 56% | 50% |  |  |
| 16006 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:40:46 UTC | 75% | 51% |  |  |
| GJ | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:45:12 UTC | 95% | 42% |  |  |
| R11T | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:46:15 UTC | 42% | 60% |  |  |
| GJ098L3843 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:48:32 UTC | 96% | 62% |  |  |
| 6142040 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:48:52 UTC | 70% | 55% |  |  |
| GJ12005869 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:50:10 UTC | 96% | 63% |  |  |
| ONEHEEX | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:50:48 UTC | 54% | 64% |  |  |
| GJ00002379 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:51:22 UTC | 94% | 61% |  |  |
| 6J08AY3301 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:52:32 UTC | 96% | 74% |  |  |
| GJ18GB1371 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:52:55 UTC | 96% | 62% |  |  |
| GJ01BK9850 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:53:32 UTC | 97% | 68% |  |  |
| GJ01KB5765 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:55:02 UTC | 90% | 61% |  |  |
| GJ31 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:56:11 UTC | 56% | 61% |  |  |
| GJA1157 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:56:17 UTC | 93% | 62% |  |  |
| GJA1157 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 05:56:18 UTC | 94% | 62% |  |  |
| 083 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 05:57:02 UTC | 89% | 60% |  |  |
| RJ20CF2562 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:57:04 UTC | 100% | 61% |  |  |
| GJ02DE7397 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 05:59:19 UTC | 100% | 65% |  |  |
| 6J11C09932 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:00:39 UTC | 94% | 59% |  |  |
| GJ01KJ5028 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:01:11 UTC | 100% | 62% |  |  |
| 4EOSGJ11C09932408 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:01:11 UTC | 60% | 58% |  |  |
| G117009992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:01:58 UTC | 70% | 46% |  |  |
| DL4CA04678 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:02:25 UTC | 96% | 61% |  |  |
| GJ08NG3852 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:02:31 UTC | 87% | 58% |  |  |
| 6J03F10419 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:02:43 UTC | 62% | 41% |  |  |
| GJ03MB7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:03:00 UTC | 96% | 60% |  |  |
| GJ32AG0028 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:03:01 UTC | 85% | 57% |  |  |
| GJ24AF3761 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:03:39 UTC | 100% | 68% |  |  |
| HH03DV1858 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:04:36 UTC | 91% | 68% |  |  |
| GJ06PG7144J | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:04:53 UTC | 96% | 50% |  |  |
| 6J45439 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:05:09 UTC | 58% | 45% |  |  |
| GJ03M87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:05:47 UTC | 94% | 64% |  |  |
| GJ115A0232 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:05:48 UTC | 91% | 50% |  |  |
| GJ03MB7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:06:09 UTC | 87% | 65% |  |  |
| FGJ03M87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:06:18 UTC | 87% | 60% |  |  |
| GJO2EA2T08 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:06:18 UTC | 69% | 43% |  |  |
| GJ03N7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:06:43 UTC | 56% | 61% |  |  |
| GJ03M97213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:06:45 UTC | 87% | 62% |  |  |
| PGJ03MM7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:06:47 UTC | 69% | 60% |  |  |
| 6J10GRRAN | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:10 UTC | 58% | 64% |  |  |
| GJ03N37213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:11 UTC | 96% | 64% |  |  |
| 6J088N5641 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:07:14 UTC | 93% | 58% |  |  |
| GJ03N37213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:14 UTC | 83% | 64% |  |  |
| 6313RIM | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:15 UTC | 47% | 63% |  |  |
| GJ03N87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:41 UTC | 86% | 64% |  |  |
| GJ03N97213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:07:43 UTC | 83% | 58% |  |  |
| PGJDGN87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:08:02 UTC | 75% | 54% |  |  |
| EGJ03MB7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:08:04 UTC | 59% | 62% |  |  |
| G1SARA | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:08:53 UTC | 50% | 42% |  |  |
| GJ03MB7213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:08:55 UTC | 83% | 63% |  |  |
| GJ03M97213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:08:57 UTC | 85% | 61% |  |  |
| 108 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:09:08 UTC | 95% | 75% |  |  |
| GJ11CL9466 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:09:29 UTC | 94% | 65% |  |  |
| EIZLNEG3 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:09:30 UTC | 60% | 63% |  |  |
| 1090A05 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:10:01 UTC | 89% | 48% |  |  |
| GJ16BG2786 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:10:06 UTC | 98% | 65% |  |  |
| 0022179 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:10:12 UTC | 74% | 52% |  |  |
| GJ03M87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:10:40 UTC | 91% | 63% |  |  |
| FGJ03M87213 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:10:41 UTC | 92% | 63% |  |  |
| GJ08DP1172 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:12:32 UTC | 99% | 64% |  |  |
| 0J08K6180 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:12:34 UTC | 75% | 51% |  |  |
| 610810N258 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:12:57 UTC | 82% | 63% |  |  |
| GJ01RE0022 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:13:10 UTC | 98% | 67% |  |  |
| PUP16 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:13:49 UTC | 68% | 49% |  |  |
| UP16BH4196 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:13:51 UTC | 95% | 63% |  |  |
| GJ3ZAG0028 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:14:02 UTC | 94% | 71% |  |  |
| GJ02DP1709 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:14:24 UTC | 94% | 64% |  |  |
| GJ08BB3420 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:16:22 UTC | 98% | 60% |  |  |
| GJ27CF6002 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:16:47 UTC | 100% | 63% |  |  |
| GJ08BN0077 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:17:59 UTC | 85% | 58% |  |  |
| GJ08BS2556 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:18:29 UTC | 97% | 69% |  |  |
| GJ2832AGOC | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:18:49 UTC | 95% | 69% |  |  |
| CE0B0L1 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:19:00 UTC | 55% | 66% |  |  |
| GJ02DN7462 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:19:02 UTC | 92% | 56% |  |  |
| GJ08AP5947 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:20:12 UTC | 100% | 60% |  |  |
| GJ08AP5947 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:20:16 UTC | 99% | 63% |  |  |
| GO080H1293 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:20:34 UTC | 79% | 63% |  |  |
| A118211188 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:20:41 UTC | 76% | 68% |  |  |
| GJ32AA4855 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:20:45 UTC | 100% | 66% |  |  |
| GJOBDHG | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:23:12 UTC | 73% | 60% |  |  |
| GJ01HY5808 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:24:49 UTC | 91% | 67% |  |  |
| GJ08DP5116 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:24:54 UTC | 98% | 66% |  |  |
| RJ24GA3342 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:25:18 UTC | 96% | 45% |  |  |
| GJ11CH9989 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:25:19 UTC | 100% | 58% |  |  |
| GJ08DP8780 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:25:26 UTC | 96% | 66% |  |  |
| 1703686J2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:26:54 UTC | 87% | 43% |  |  |
| GJ08DP4618 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:27:28 UTC | 100% | 66% |  |  |
| RJ27CR3745 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:27:47 UTC | 100% | 61% |  |  |
| DOLEAM | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:27:51 UTC | 46% | 49% |  |  |
| GJ11BH9494 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:28:07 UTC | 100% | 67% |  |  |
| RJ27CR3745 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:28:08 UTC | 100% | 66% |  |  |
| GJ05JL2253 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:28:21 UTC | 100% | 67% |  |  |
| ILL8BA | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:28:21 UTC | 42% | 48% |  |  |
| GJ08BN9797 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:29:16 UTC | 96% | 69% |  |  |
| GJT1TT5642 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:29:21 UTC | 86% | 45% |  |  |
| GJ278E7639 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:30:00 UTC | 97% | 63% |  |  |
| GJ01DZ8295 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:30:03 UTC | 94% | 53% |  |  |
| GJ01HX2640 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:31:23 UTC | 98% | 56% |  |  |
| GJ02BP0239 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:31:29 UTC | 100% | 56% |  |  |
| GJ08CC5192 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:31:33 UTC | 86% | 62% |  |  |
| GJ08CC5192 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:31:35 UTC | 95% | 47% |  |  |
| 1BR9267 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:31:47 UTC | 99% | 50% |  |  |
| GJ11CH6858 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:32:28 UTC | 100% | 63% |  |  |
| GJ27DH4954 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:33:04 UTC | 90% | 49% |  |  |
| 5J11807242 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:34:00 UTC | 81% | 60% |  |  |
| GJ08DG9215 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:34:59 UTC | 100% | 63% |  |  |
| GJ06F01685 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:36:26 UTC | 98% | 62% |  |  |
| GJ06F01685 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:36:27 UTC | 98% | 62% |  |  |
| GJ01WJ2537 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:36:28 UTC | 98% | 59% |  |  |
| AVAW | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:39:02 UTC | 79% | 46% |  |  |
| G50B8C01G9 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:39:33 UTC | 48% | 42% |  |  |
| GJ1426330 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:40:13 UTC | 94% | 65% |  |  |
| GJ23CG5643 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:40:37 UTC | 100% | 64% |  |  |
| VGJO8172621 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:42:20 UTC | 79% | 47% |  |  |
| GJ2JE39752 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:42:45 UTC | 84% | 47% |  |  |
| GJ09BJ3907 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:45:05 UTC | 95% | 67% |  |  |
| GJ32AA0052 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:45:38 UTC | 100% | 66% |  |  |
| GJ088N4698 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:45:56 UTC | 82% | 61% |  |  |
| 7649 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:47:01 UTC | 96% | 61% |  |  |
| GI05RF0RY | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:47:12 UTC | 51% | 42% |  |  |
| GJDBAW9204 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:47:25 UTC | 89% | 66% |  |  |
| GJ08BB1038 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:48:08 UTC | 99% | 69% |  |  |
| 20001025092 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:49:19 UTC | 66% | 50% |  |  |
| GJ18BM2507 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:49:39 UTC | 93% | 59% |  |  |
| GJ31UNAIS | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:49:50 UTC | 74% | 75% |  |  |
| 1610 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:53:26 UTC | 77% | 58% |  |  |
| LO35 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:53:46 UTC | 55% | 44% |  |  |
| GJ27TD3437 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:54:36 UTC | 97% | 66% |  |  |
| GJ18BN7581 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:55:31 UTC | 100% | 49% |  |  |
| GJ08DG5536 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:55:52 UTC | 99% | 56% |  |  |
| GJ080P0764 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:56:26 UTC | 95% | 47% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 06:56:34 UTC | 67% | 45% |  |  |
| 6J03JL8022 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 06:57:04 UTC | 98% | 54% |  |  |
| FO2211 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 06:57:07 UTC | 44% | 42% |  |  |
| GJ24A04739 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:57:16 UTC | 97% | 66% |  |  |
| GJ0822731 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:57:59 UTC | 90% | 53% |  |  |
| GJ020E13Z0 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 06:58:52 UTC | 94% | 59% |  |  |
| GJ08CG8724 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:00:10 UTC | 99% | 64% |  |  |
| 0J1B818237 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 07:01:55 UTC | 54% | 40% |  |  |
| GJ08BN0221 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:02:41 UTC | 97% | 57% |  |  |
| GJ01RC5387 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:02:58 UTC | 95% | 58% |  |  |
| GJ23BL2155 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:04:11 UTC | 98% | 70% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 07:04:43 UTC | 67% | 54% |  |  |
| RADTEL | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 07:05:27 UTC | 44% | 48% |  |  |
| GJ36R9479 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:07:31 UTC | 100% | 60% |  |  |
| GJ18BV4007 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:08:10 UTC | 96% | 69% |  |  |
| GJOIKE8165 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:09:20 UTC | 89% | 70% |  |  |
| GJ01WE8276 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:09:22 UTC | 97% | 69% |  |  |
| GJ08FA837A | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:09:24 UTC | 96% | 59% |  |  |
| GJ03KH7042 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:09:31 UTC | 90% | 53% |  |  |
| CJ03KH7044 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:09:33 UTC | 83% | 49% |  |  |
| GJJU | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:10:05 UTC | 76% | 58% |  |  |
| GJ05RV7911 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:10:33 UTC | 100% | 67% |  |  |
| GJ08AU9763 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:11:47 UTC | 99% | 66% |  |  |
| GJ08D07588 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:12:52 UTC | 91% | 61% |  |  |
| 32T8326 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:13:04 UTC | 62% | 60% |  |  |
| GJ27CF3096 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:13:57 UTC | 99% | 65% |  |  |
| PA011CH9O | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:15:09 UTC | 51% | 68% |  |  |
| GJ08AU2336 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:15:35 UTC | 96% | 65% |  |  |
| 9T | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:15:39 UTC | 42% | 60% |  |  |
| GJ118H9812 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:16:07 UTC | 94% | 65% |  |  |
| GJ118H9812 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:16:10 UTC | 94% | 65% |  |  |
| GJ32A61970 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:18:07 UTC | 85% | 42% |  |  |
| GJ24BF1145 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:18:43 UTC | 66% | 67% |  |  |
| GJ08DJ9897 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:18:54 UTC | 100% | 67% |  |  |
| GJD90L9469 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:19:01 UTC | 94% | 63% |  |  |
| GJ01KF5603 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:19:30 UTC | 100% | 61% |  |  |
| GJ01KF560 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:19:34 UTC | 95% | 63% |  |  |
| GJ0ZDE7255 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:20:59 UTC | 86% | 46% |  |  |
| GJ08DG6860 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:22:05 UTC | 99% | 65% |  |  |
| GJ32K4770 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:22:09 UTC | 99% | 66% |  |  |
| GJ32K4770 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:22:11 UTC | 99% | 66% |  |  |
| GJ02CA0565 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:23:42 UTC | 98% | 59% |  |  |
| 088SH | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:25:31 UTC | 74% | 45% |  |  |
| GJ08BF7604 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:25:56 UTC | 97% | 70% |  |  |
| O | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:26:00 UTC | 91% | 60% |  |  |
| OTZ425 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:27:10 UTC | 59% | 48% |  |  |
| GJUBA39095 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:27:14 UTC | 82% | 45% |  |  |
| GJ39CD0010 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:27:48 UTC | 99% | 68% |  |  |
| GJ08CR7283 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:28:22 UTC | 97% | 69% |  |  |
| GJ08CR7283 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:28:25 UTC | 99% | 70% |  |  |
| HILL | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:30:25 UTC | 64% | 42% |  |  |
| GJ0BCK7572 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:30:32 UTC | 95% | 64% |  |  |
| GJ08CS1650 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:32:06 UTC | 99% | 63% |  |  |
| 6010BR1112 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:32:42 UTC | 80% | 48% |  |  |
| GJ06RG9999 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:34:37 UTC | 92% | 69% |  |  |
| GJ1GX2537 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:34:52 UTC | 83% | 55% |  |  |
| 6200559004 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:35:31 UTC | 49% | 54% |  |  |
| GJ36AC4610 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:39:00 UTC | 97% | 59% |  |  |
| GJORDG7444 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:39:07 UTC | 91% | 66% |  |  |
| 6J23M9909 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:39:11 UTC | 97% | 68% |  |  |
| GJ11AB5688 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:39:30 UTC | 96% | 63% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:39:30 UTC | 100% | 62% |  |  |
| GJ388H3156 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:40:15 UTC | 96% | 68% |  |  |
| GJ27GF2081 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:41:26 UTC | 99% | 61% |  |  |
| 6J08AP2230 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:42:46 UTC | 87% | 67% |  |  |
| GJD8DM3012 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:43:54 UTC | 95% | 67% |  |  |
| GJ05RJ5069 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:44:20 UTC | 99% | 66% |  |  |
| G08ALL919 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:44:46 UTC | 73% | 68% |  |  |
| 6J11T | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:45:02 UTC | 90% | 63% |  |  |
| GJ13AT1638 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:45:18 UTC | 93% | 69% |  |  |
| GJ02DE4237 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:46:12 UTC | 93% | 52% |  |  |
| GJ08CG7002 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:46:19 UTC | 98% | 67% |  |  |
| 6111003137 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:49:35 UTC | 81% | 49% |  |  |
| GJ08DP9010CINDIA | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:49:59 UTC | 70% | 65% |  |  |
| GJ08DPD949 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:50:04 UTC | 94% | 60% |  |  |
| 25883730H | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:50:38 UTC | 91% | 47% |  |  |
| GJ18BF4959 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:50:47 UTC | 93% | 67% |  |  |
| GJ13CF9735 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:51:05 UTC | 100% | 70% |  |  |
| J091V6197RV8 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:51:13 UTC | 72% | 48% |  |  |
| GJ08DM3341 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:51:43 UTC | 100% | 64% |  |  |
| GJ01RL0777 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:52:07 UTC | 96% | 55% |  |  |
| GJ08CC6613 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:52:32 UTC | 99% | 65% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 07:52:33 UTC | 62% | 51% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 07:52:35 UTC | 52% | 45% |  |  |
| 1NOPGJT1CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 07:55:10 UTC | 57% | 45% |  |  |
| GJ08CS1695 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:57:30 UTC | 97% | 70% |  |  |
| GJ02EG9559 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:57:59 UTC | 100% | 67% |  |  |
| G102EK3085 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 07:59:11 UTC | 90% | 57% |  |  |
| GJ080N7245 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:00:43 UTC | 90% | 67% |  |  |
| BJUBA17000 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:02:17 UTC | 50% | 69% |  |  |
| FG125J7120 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:02:46 UTC | 80% | 60% |  |  |
| GJ08DG5071 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:02:49 UTC | 100% | 63% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:04:34 UTC | 100% | 66% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:04:36 UTC | 100% | 66% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:04:38 UTC | 100% | 65% |  |  |
| 5J25J7838 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:04:53 UTC | 88% | 43% |  |  |
| GJ24K3268 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:05:09 UTC | 100% | 65% |  |  |
| GJ01RC8654 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:06:12 UTC | 96% | 65% |  |  |
| GJ25J7346 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:07:52 UTC | 99% | 45% |  |  |
| GJ11COG602 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:08:15 UTC | 87% | 48% |  |  |
| GJ32K6476 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:08:28 UTC | 95% | 49% |  |  |
| GJ27C4145 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:08:56 UTC | 100% | 65% |  |  |
| GJ12FB3366 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:09:13 UTC | 94% | 55% |  |  |
| AREUQELPIA | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:10:08 UTC | 54% | 52% |  |  |
| GJ02AT4169 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:11:01 UTC | 96% | 66% |  |  |
| GJ08BF0295 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:11:32 UTC | 99% | 48% |  |  |
| GJ36AL1058 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:11:49 UTC | 100% | 67% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:11:49 UTC | 100% | 66% |  |  |
| GJ08DP0246 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:12:04 UTC | 99% | 66% |  |  |
| GJ01KZ3057 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:15:51 UTC | 97% | 62% |  |  |
| GJ08CS3826 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:16:14 UTC | 99% | 63% |  |  |
| ULU412 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:16:37 UTC | 72% | 42% |  |  |
| GJ08DS3750 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:16:44 UTC | 94% | 52% |  |  |
| AZ7319 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:16:45 UTC | 83% | 43% |  |  |
| G308AJ6736 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:16:52 UTC | 86% | 66% |  |  |
| TAXI | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:18:39 UTC | 100% | 45% |  |  |
| TAXI | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:18:44 UTC | 100% | 44% |  |  |
| GJ08CC4067 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:19:32 UTC | 98% | 41% |  |  |
| GJ01WZ8171 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:20:23 UTC | 99% | 63% |  |  |
| GJOB110267 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:20:31 UTC | 62% | 52% |  |  |
| UP32MW9107 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:21:10 UTC | 99% | 61% |  |  |
| GJ19BA8094 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:22:00 UTC | 98% | 62% |  |  |
| GJ08CR1190 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:22:35 UTC | 98% | 67% |  |  |
| GJ08FA3032 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:23:45 UTC | 100% | 60% |  |  |
| GJ24A05262 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:24:30 UTC | 99% | 63% |  |  |
| GJ16DS2234 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:25:19 UTC | 100% | 66% |  |  |
| GJ08DJ9900 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:26:15 UTC | 99% | 69% |  |  |
| GJ05RD8368 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:26:45 UTC | 94% | 64% |  |  |
| 5J08AZ3375 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:26:52 UTC | 71% | 66% |  |  |
| GJ18EF6816 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:28:04 UTC | 99% | 59% |  |  |
| GJ23H0090 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:28:55 UTC | 100% | 67% |  |  |
| GJ06KD3647 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:30:14 UTC | 99% | 67% |  |  |
| GJ19GC1237 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:31:12 UTC | 89% | 48% |  |  |
| GJ01BP9036 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:31:19 UTC | 99% | 46% |  |  |
| GJ08DJ0959 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:31:22 UTC | 100% | 64% |  |  |
| MNNCSD | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:31:43 UTC | 51% | 60% |  |  |
| SD | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:31:44 UTC | 43% | 42% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 08:32:26 UTC | 84% | 68% |  |  |
| GJ01HN8383 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:32:43 UTC | 98% | 64% |  |  |
| L | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:32:45 UTC | 90% | 55% |  |  |
| GJ01WP7247 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:32:53 UTC | 98% | 70% |  |  |
| GJ08DS4046 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:33:26 UTC | 100% | 63% |  |  |
| GJ02DP8346 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:34:25 UTC | 99% | 57% |  |  |
| GJ028P267RAILL | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:34:34 UTC | 84% | 68% |  |  |
| GJ02AC8443 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:34:52 UTC | 98% | 54% |  |  |
| GJ01WW1091 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:34:59 UTC | 99% | 63% |  |  |
| GJ08AU2557 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:35:42 UTC | 99% | 68% |  |  |
| AHA | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 08:35:51 UTC | 46% | 58% |  |  |
| Y6766 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:36:39 UTC | 99% | 59% |  |  |
| EITELRT060 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:37:16 UTC | 52% | 47% |  |  |
| GJO1WN2273 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:37:21 UTC | 96% | 63% |  |  |
| PH8Z11229 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:37:51 UTC | 76% | 55% |  |  |
| GJ08CS8963 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:38:16 UTC | 99% | 65% |  |  |
| GJ11CL5041 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:38:27 UTC | 100% | 68% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:38:28 UTC | 100% | 66% |  |  |
| 03300 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:39:06 UTC | 85% | 65% |  |  |
| GJ08F4110 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:39:14 UTC | 99% | 67% |  |  |
| GJJ282101 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:39:25 UTC | 95% | 43% |  |  |
| GJ08DD8918 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:39:27 UTC | 99% | 67% |  |  |
| GJD1HU2027 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:40:31 UTC | 97% | 69% |  |  |
| GJ01RS0338 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:41:06 UTC | 96% | 59% |  |  |
| 0MC10284 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:41:36 UTC | 45% | 42% |  |  |
| GJ08FB5545 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:41:42 UTC | 99% | 64% |  |  |
| CLDGJ080H882 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:41:48 UTC | 76% | 53% |  |  |
| GJ388A3274 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:44:02 UTC | 96% | 65% |  |  |
| GJ02ER2448 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:46:08 UTC | 98% | 65% |  |  |
| GJ080J0459 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:46:28 UTC | 94% | 65% |  |  |
| MAA | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:46:32 UTC | 41% | 53% |  |  |
| 0J020A3858 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:46:35 UTC | 72% | 61% |  |  |
| TOURIST | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:46:45 UTC | 100% | 45% |  |  |
| GJ02CG0222 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:46:47 UTC | 99% | 61% |  |  |
| GJ08DJ646 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:47:59 UTC | 98% | 57% |  |  |
| GJ08AP6381 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:48:09 UTC | 97% | 66% |  |  |
| 8 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:48:50 UTC | 98% | 48% |  |  |
| GJ02EN9888 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 08:49:04 UTC | 99% | 68% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:49:31 UTC | 99% | 66% |  |  |
| GJ11CH2 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:49:33 UTC | 100% | 66% |  |  |
| GJ32AA5 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:51:53 UTC | 80% | 51% |  |  |
| 0012422 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:54:39 UTC | 57% | 51% |  |  |
| MO | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:55:15 UTC | 67% | 42% |  |  |
| GJ19AF3952 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 08:56:09 UTC | 100% | 60% |  |  |
| GGJ11U03134 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:01:28 UTC | 87% | 42% |  |  |
| GJ14AP0234 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:01:30 UTC | 94% | 57% |  |  |
| FOLEL892 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:02:38 UTC | 59% | 56% |  |  |
| GJ189A0252 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:02:49 UTC | 85% | 47% |  |  |
| GJ01RV3408 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:06:26 UTC | 95% | 50% |  |  |
| X7632 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:07:00 UTC | 94% | 41% |  |  |
| FCJ06LE1781 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:07:11 UTC | 72% | 57% |  |  |
| GJ15CK8289 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:09:01 UTC | 79% | 60% |  |  |
| ARS | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:11:04 UTC | 72% | 53% |  |  |
| 013298169 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:15:02 UTC | 78% | 41% |  |  |
| GJ11CL7200 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:15:55 UTC | 100% | 68% |  |  |
| GJ11RH0062 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:17:33 UTC | 77% | 54% |  |  |
| 6 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:22:45 UTC | 76% | 64% |  |  |
| A05235 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:27:23 UTC | 71% | 42% |  |  |
| 0172105205 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:27:25 UTC | 83% | 64% |  |  |
| GJ06FC8439 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:31:33 UTC | 100% | 61% |  |  |
| GJ06FC8439 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:31:40 UTC | 100% | 61% |  |  |
| GJ06FC8439 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:31:43 UTC | 100% | 61% |  |  |
| 6 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:31:52 UTC | 96% | 63% |  |  |
| GJ11AS6908 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:34:03 UTC | 98% | 62% |  |  |
| GJ18GA279 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:34:40 UTC | 95% | 59% |  |  |
| 6J18GA2795 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:34:44 UTC | 95% | 48% |  |  |
| FGJ11CH9591 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:36:30 UTC | 88% | 46% |  |  |
| G101MT5556GJO1M | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:39:12 UTC | 80% | 58% |  |  |
| G101MT5556GJO1MT5556 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:39:14 UTC | 87% | 52% |  |  |
| MH12YZ0676 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:39:25 UTC | 91% | 52% |  |  |
| LUCKY | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:44:47 UTC | 100% | 45% |  |  |
| 03089226 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:45:08 UTC | 58% | 47% |  |  |
| GJ01WG4917 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:46:30 UTC | 93% | 53% |  |  |
| GJ01WG4917 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:46:33 UTC | 97% | 54% |  |  |
| GJ11C01380 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:47:26 UTC | 98% | 62% |  |  |
| GJ11C01380 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:47:29 UTC | 98% | 62% |  |  |
| 15932 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:49:13 UTC | 81% | 57% |  |  |
| GJ15CB6009 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:53:42 UTC | 93% | 45% |  |  |
| GJ15CB6009 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:53:45 UTC | 94% | 47% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:55:02 UTC | 98% | 50% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:55:29 UTC | 95% | 54% |  |  |
| U130 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:56:52 UTC | 57% | 52% |  |  |
| GJ3388357 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:57:33 UTC | 92% | 58% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:57:34 UTC | 99% | 56% |  |  |
| 6J03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:58:40 UTC | 96% | 59% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:58:42 UTC | 95% | 62% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:59:13 UTC | 96% | 50% |  |  |
| GJ03HK2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:59:26 UTC | 97% | 64% |  |  |
| GJ03HX2192 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 09:59:30 UTC | 94% | 61% |  |  |
| A6301028549 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 09:59:40 UTC | 67% | 44% |  |  |
| 6J1 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:00:58 UTC | 84% | 46% |  |  |
| GJ | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:01:00 UTC | 100% | 48% |  |  |
| GJ25AA9496 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:03:41 UTC | 90% | 62% |  |  |
| GJ23AM3796 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:03:54 UTC | 95% | 44% |  |  |
| 1089092 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:05:15 UTC | 94% | 45% |  |  |
| 5J11188841 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:13:06 UTC | 93% | 45% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 10:15:33 UTC | 69% | 46% |  |  |
| 6531828355 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:16:34 UTC | 59% | 43% |  |  |
| G1CH8647 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:17:13 UTC | 100% | 51% |  |  |
| HENION | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:17:34 UTC | 42% | 58% |  |  |
| 011930851 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:17:36 UTC | 73% | 55% |  |  |
| ACRAA0S | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:20:38 UTC | 43% | 61% |  |  |
| GJ11C09105 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:20:40 UTC | 100% | 69% |  |  |
| TEOLJIJIOL | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:21:25 UTC | 50% | 54% |  |  |
| FGJ13CF0026 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:25:02 UTC | 95% | 44% |  |  |
| GJ03NH6522 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:25:03 UTC | 93% | 40% |  |  |
| MTUMIZN | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:26:42 UTC | 53% | 60% |  |  |
| GJ119H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:30:04 UTC | 97% | 60% |  |  |
| GJ119H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:30:10 UTC | 97% | 63% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:30:13 UTC | 97% | 66% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:30:16 UTC | 99% | 65% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:31:10 UTC | 100% | 64% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:31:54 UTC | 100% | 58% |  |  |
| GJ118H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:32:19 UTC | 99% | 63% |  |  |
| FGJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:32:50 UTC | 93% | 64% |  |  |
| GJ118H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:33:08 UTC | 98% | 57% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:33:49 UTC | 99% | 65% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:33:54 UTC | 96% | 65% |  |  |
| GJ119H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:34:54 UTC | 97% | 60% |  |  |
| GJ119H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:34:58 UTC | 99% | 60% |  |  |
| 6511947992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:35:00 UTC | 85% | 59% |  |  |
| 47992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:35:02 UTC | 83% | 51% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:36:26 UTC | 99% | 60% |  |  |
| J11CH851 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:36:46 UTC | 99% | 55% |  |  |
| J11CH8514 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:36:51 UTC | 95% | 49% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:37:01 UTC | 100% | 62% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:37:03 UTC | 100% | 63% |  |  |
| FGJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:37:20 UTC | 95% | 62% |  |  |
| FGJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:37:21 UTC | 96% | 63% |  |  |
| GJ11BH7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:38:56 UTC | 99% | 64% | 🚨 |  |
| GJ118H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:39:16 UTC | 95% | 63% |  |  |
| GJ118H7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:39:18 UTC | 95% | 62% |  |  |
| GJ119H799 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:40:21 UTC | 92% | 47% |  |  |
| GJ11BR7992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:40:31 UTC | 91% | 66% |  |  |
| GJ01KDQ059 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:41:50 UTC | 90% | 64% |  |  |
| GJ08DP3522 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:44:16 UTC | 94% | 49% |  |  |
| GJ08803435 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:44:32 UTC | 95% | 64% |  |  |
| GJ080J5395 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:45:12 UTC | 77% | 70% |  |  |
| GJ01CX87 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:45:18 UTC | 90% | 42% |  |  |
| GJ01CX87 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:45:24 UTC | 93% | 44% |  |  |
| GJ11TT9175 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:45:45 UTC | 100% | 55% |  |  |
| GJ08DM2579 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:46:44 UTC | 92% | 45% |  |  |
| GJ11DB0049 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:46:57 UTC | 93% | 64% |  |  |
| GJ108099 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:47:34 UTC | 74% | 52% |  |  |
| GJ23AN596T | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:52:57 UTC | 85% | 67% |  |  |
| 0001602809 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:54:58 UTC | 58% | 64% |  |  |
| F6111E02803 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:55:00 UTC | 74% | 66% |  |  |
| GJB0HN4550 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 10:55:36 UTC | 87% | 47% |  |  |
| QU1JAD | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:58:23 UTC | 50% | 63% |  |  |
| 18062026175554MADHURAMBYPASSROADFIX2FROMAK | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 10:58:36 UTC | 99% | 43% |  | ⚠️ overlay text, not a plate |
| GJD815015 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:02:15 UTC | 77% | 45% |  |  |
| SGJ08FA7358 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:06:30 UTC | 68% | 52% |  |  |
| GJ11CD3491 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:09:22 UTC | 96% | 55% |  |  |
| J02EKU873 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:14:54 UTC | 87% | 56% |  |  |
| GJ3309646 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:21:52 UTC | 94% | 69% |  |  |
| GJOBR4 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:23:28 UTC | 86% | 40% |  |  |
| 116178 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:23:51 UTC | 61% | 52% |  |  |
| GJ08DG1047 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:27:25 UTC | 95% | 56% |  |  |
| GJ05RL9657 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:27:33 UTC | 62% | 68% |  |  |
| GJ02DE2346 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:28:43 UTC | 100% | 65% |  |  |
| GJ03ME2399 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:28:46 UTC | 98% | 68% |  |  |
| GJ11A82974 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:29:00 UTC | 90% | 56% |  |  |
| GJ11485588 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:31:02 UTC | 53% | 55% |  |  |
| GJ02DP8903 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:31:33 UTC | 98% | 52% |  |  |
| GJ11E | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:31:42 UTC | 96% | 49% |  |  |
| GJ11EA1355 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:31:45 UTC | 94% | 50% |  |  |
| GJ11BH9085 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:33:13 UTC | 100% | 62% |  |  |
| GJJ5T1655 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:33:44 UTC | 87% | 62% |  |  |
| GJ08DP9952 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:33:56 UTC | 98% | 67% |  |  |
| GJ148A4108 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:36:40 UTC | 88% | 59% |  |  |
| GJ23CF3136 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:36:41 UTC | 95% | 47% |  |  |
| GJ08AP2123 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:37:17 UTC | 99% | 65% |  |  |
| GJ16AA4815 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:37:36 UTC | 100% | 58% |  |  |
| GJ24AF1738 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:39:10 UTC | 96% | 70% |  |  |
| 6J11C07392 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:39:38 UTC | 88% | 47% |  |  |
| 6J11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:39:41 UTC | 85% | 43% |  |  |
| GJ11C07392 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:39:42 UTC | 88% | 48% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:40:03 UTC | 92% | 41% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:40:26 UTC | 97% | 53% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:40:31 UTC | 97% | 54% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:40:50 UTC | 86% | 48% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:40:53 UTC | 90% | 48% |  |  |
| GJ11C07932 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:41:21 UTC | 86% | 49% |  |  |
| 6J11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:41:45 UTC | 90% | 51% |  |  |
| GJ11C07332 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:43:06 UTC | 88% | 49% |  |  |
| GJ19AA3070 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:43:37 UTC | 99% | 54% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:43:58 UTC | 94% | 51% |  |  |
| GJ08DM9904 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:44:05 UTC | 95% | 65% |  |  |
| GJ01RU0948 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:45:32 UTC | 98% | 69% |  |  |
| GJ11BR4370 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:45:33 UTC | 99% | 61% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:45:34 UTC | 96% | 55% |  |  |
| GJ11C07992 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:46:11 UTC | 97% | 66% |  |  |
| GJ06P07674 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:47:16 UTC | 90% | 50% |  |  |
| GJ11C09395 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:49:01 UTC | 100% | 66% |  |  |
| 0 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 11:49:16 UTC | 57% | 51% |  |  |
| GJ07DD9992 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:51:33 UTC | 93% | 62% |  |  |
| G108AN6302 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:52:53 UTC | 73% | 59% |  |  |
| GJ38BB6446 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 11:58:07 UTC | 96% | 50% |  |  |
| GJ14ZJ812 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:02:57 UTC | 89% | 56% |  |  |
| 63110U6295 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:04:20 UTC | 87% | 40% |  |  |
| GJ10DA5544 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:07:23 UTC | 99% | 67% |  |  |
| GJ05RZ7229 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:16:53 UTC | 99% | 61% |  |  |
| CH | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:17:22 UTC | 100% | 43% |  |  |
| GJT1CH1809 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:20:02 UTC | 95% | 53% |  |  |
| GJ11CH3274 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:20:34 UTC | 99% | 50% |  |  |
| 11840E175 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:22:54 UTC | 44% | 42% |  |  |
| 6008AV5I89 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:24:11 UTC | 68% | 77% |  |  |
| CK2R20A | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:24:57 UTC | 58% | 52% |  |  |
| 1071957 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:26:02 UTC | 76% | 60% |  |  |
| GJD8DP4025 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:26:45 UTC | 95% | 51% |  |  |
| GJ18BV4436 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:27:29 UTC | 99% | 50% |  |  |
| GJ07DC9910 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:27:34 UTC | 99% | 66% |  |  |
| GJ07DC9910 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:27:37 UTC | 100% | 63% |  |  |
| GJ02BD0916 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:27:48 UTC | 89% | 49% |  |  |
| GJ1BED5755 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:28:49 UTC | 90% | 69% |  |  |
| GJ08BB4717 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:29:55 UTC | 95% | 65% |  |  |
| GJ2509012 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:30:16 UTC | 96% | 42% |  |  |
| GUT1CL4976 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:33:19 UTC | 76% | 66% |  |  |
| GJ02DM5177 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:34:42 UTC | 97% | 71% |  |  |
| GJ24A03Z61 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:35:00 UTC | 95% | 67% |  |  |
| UDUSER0 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:36:36 UTC | 52% | 49% |  |  |
| GJ08FA2872 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:39:32 UTC | 99% | 69% |  |  |
| GJ08DS2018 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:39:42 UTC | 99% | 67% |  |  |
| GJ24AU1711 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:40:07 UTC | 100% | 68% |  |  |
| GJ09BK5363 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:41:09 UTC | 94% | 68% |  |  |
| 0 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 12:42:42 UTC | 48% | 42% |  |  |
| T9857 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:43:33 UTC | 88% | 60% |  |  |
| T9857 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:43:35 UTC | 89% | 62% |  |  |
| GJ05CP8818 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:46:29 UTC | 93% | 61% |  |  |
| 611108381 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:49:12 UTC | 74% | 55% |  |  |
| GJ38BH4440 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:50:37 UTC | 98% | 67% |  |  |
| GJ08CS7500 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:52:12 UTC | 93% | 65% |  |  |
| GJ11C00238 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:53:00 UTC | 76% | 62% |  |  |
| GJ02BP4664 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:53:01 UTC | 89% | 71% |  |  |
| N021 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:53:04 UTC | 58% | 42% |  |  |
| G2C9023 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 12:53:06 UTC | 42% | 45% |  |  |
| GJ08DJ7061 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:53:54 UTC | 98% | 64% |  |  |
| 0J21EE5334 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:56:37 UTC | 78% | 66% |  |  |
| GJ08CC2606 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:58:54 UTC | 97% | 60% |  |  |
| GJ31BB8458 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:59:55 UTC | 70% | 69% |  |  |
| GJ31BB8458 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 12:59:57 UTC | 98% | 66% |  |  |
| 5101821375 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:00:46 UTC | 83% | 62% |  |  |
| GJ32B1782 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:03:47 UTC | 100% | 69% |  |  |
| 6J27CF9967 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:08:15 UTC | 97% | 68% |  |  |
| GJ08CG0446 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:08:18 UTC | 100% | 68% |  |  |
| GJ001144 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:08:49 UTC | 85% | 67% |  |  |
| 53277105634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:12:07 UTC | 74% | 68% |  |  |
| GOZTTD5634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:12:14 UTC | 81% | 68% |  |  |
| 53277T05634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:12:39 UTC | 77% | 63% |  |  |
| 0T1T05614 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:12:59 UTC | 58% | 55% |  |  |
| U2TTD5634 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:13:34 UTC | 73% | 62% |  |  |
| 11811551 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:15:18 UTC | 54% | 68% |  |  |
| GJ0GRF5715 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:16:24 UTC | 97% | 54% |  |  |
| GJD8DG6860 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:19:51 UTC | 97% | 61% |  |  |
| GJ08BB5872 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:26:03 UTC | 100% | 67% |  |  |
| GJOBFA3519 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:26:43 UTC | 90% | 58% |  |  |
| GJ080S7389 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:27:08 UTC | 96% | 53% |  |  |
| GJ09BG0198 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:28:42 UTC | 97% | 61% |  |  |
| GJ03KH7471 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:30:16 UTC | 100% | 71% |  |  |
| G30315063 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:31:12 UTC | 86% | 49% |  |  |
| GJOTWP4410 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:31:36 UTC | 88% | 69% |  |  |
| POOXMAI | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:32:47 UTC | 80% | 40% |  |  |
| 201T5427 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 13:35:10 UTC | 61% | 51% |  |  |
| GJ09BK2211 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:36:57 UTC | 99% | 69% |  |  |
| GJ08AJ1660 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:38:03 UTC | 94% | 66% |  |  |
| GJ08BS0726 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:38:38 UTC | 98% | 65% |  |  |
| 15253272283 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:40:16 UTC | 67% | 64% |  |  |
| RO | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:40:54 UTC | 83% | 54% |  |  |
| GJ18GB3393 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:41:36 UTC | 99% | 60% |  |  |
| GJ05CK8377 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:42:17 UTC | 100% | 53% |  |  |
| 6J1ISTDSS | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:42:31 UTC | 44% | 43% |  |  |
| GJ05CK8377 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:43:22 UTC | 100% | 52% |  |  |
| GJ05CK8377 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:43:41 UTC | 100% | 49% |  |  |
| GJ08CR5255 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:45:55 UTC | 100% | 62% |  |  |
| GJO8CS8617 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:46:47 UTC | 91% | 59% |  |  |
| GJ05CK8377 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:46:54 UTC | 100% | 46% |  |  |
| GJ05CK8377 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:47:47 UTC | 100% | 45% |  |  |
| GJ08CR3693 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:48:31 UTC | 99% | 67% |  |  |
| GJ27EA1963MER | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:48:46 UTC | 93% | 68% |  |  |
| UJZ70LZZT | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:50:47 UTC | 56% | 58% |  |  |
| GJ27BL2219 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:50:49 UTC | 100% | 64% |  |  |
| GJ08FA8771 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:51:15 UTC | 100% | 67% |  |  |
| MM240V2318 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 13:53:00 UTC | 54% | 47% |  |  |
| 48S34 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:53:19 UTC | 60% | 55% |  |  |
| GJ08BS3475 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:53:23 UTC | 99% | 64% |  |  |
| GJ02VV3741 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:55:42 UTC | 93% | 46% |  |  |
| GJ080J9117 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:57:57 UTC | 93% | 67% |  |  |
| GJ01HY3960 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:58:26 UTC | 98% | 65% |  |  |
| 03010H4922 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 13:59:37 UTC | 76% | 67% |  |  |
| 43070H4922 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 13:59:41 UTC | 83% | 65% |  |  |
| VEER | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 13:59:46 UTC | 100% | 64% |  |  |
| GJ01KL8534 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:04:04 UTC | 96% | 61% |  |  |
| GJ08AY5353 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:04:09 UTC | 97% | 65% |  |  |
| GJ02Z8001 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:07:16 UTC | 87% | 65% |  |  |
| GJ08DJ1519 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:07:41 UTC | 99% | 51% |  |  |
| PM | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:08:08 UTC | 69% | 47% |  |  |
| GJ089575 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:11:10 UTC | 100% | 52% |  |  |
| 212 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:11:21 UTC | 99% | 63% |  |  |
| GJO5NX6ZUO | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:13:16 UTC | 72% | 65% |  |  |
| G005BX6200 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:13:18 UTC | 92% | 63% |  |  |
| GJ08BN3961 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:13:27 UTC | 99% | 65% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:16:37 UTC | 61% | 46% |  |  |
| GJ08DJ94T6 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:20:08 UTC | 94% | 55% |  |  |
| 1880WAXI108GAGOL16657 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:20:24 UTC | 77% | 46% |  |  |
| GJ02CG0695 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:22:03 UTC | 91% | 60% |  |  |
| GJOZER8520 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:22:34 UTC | 90% | 54% |  |  |
| RJ27CN2115 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:22:43 UTC | 100% | 68% |  |  |
| RJ27CN2115 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:22:48 UTC | 98% | 69% |  |  |
| GJ11CL9596 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 14:23:32 UTC | 92% | 60% |  |  |
| 225 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:24:22 UTC | 100% | 47% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:25:57 UTC | 57% | 44% |  |  |
| GJ08FA7043 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:26:08 UTC | 99% | 67% |  |  |
| GJ08FA7043 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:26:12 UTC | 99% | 66% |  |  |
| GJ18HY2495 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:26:54 UTC | 83% | 40% |  |  |
| 0J08BH3123 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:27:10 UTC | 88% | 64% |  |  |
| CLNSFNCZAN | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:28:44 UTC | 46% | 57% |  |  |
| GJ08CR0399 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:28:47 UTC | 99% | 67% |  |  |
| GU090N2428 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:30:27 UTC | 88% | 58% |  |  |
| GJ08B55099 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:31:44 UTC | 91% | 49% |  |  |
| GJ02CL2606 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:31:58 UTC | 100% | 65% |  |  |
| GJ18BH5025 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:32:32 UTC | 92% | 71% |  |  |
| GJ08AP5548 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:32:39 UTC | 99% | 60% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:33:56 UTC | 41% | 45% |  |  |
| GJ18Z9008 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:39:25 UTC | 98% | 65% |  |  |
| GJ0BAU2000 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:40:00 UTC | 87% | 59% |  |  |
| I001R2202 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:40:20 UTC | 49% | 49% |  |  |
| GJ08CG0838 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:41:56 UTC | 99% | 66% |  |  |
| KGARRIGE | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:42:26 UTC | 96% | 65% |  |  |
| GJ02EC0673 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:44:03 UTC | 99% | 67% |  |  |
| GJ24AA3141 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:44:47 UTC | 100% | 69% |  |  |
| 0800058 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:45:24 UTC | 81% | 63% |  |  |
| GJ08CK1257 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:45:54 UTC | 96% | 60% |  |  |
| GJ38BK5747LIRYDIA | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:46:21 UTC | 88% | 65% |  |  |
| 6J06306507 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:46:29 UTC | 89% | 55% |  |  |
| J17BH1616 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:48:10 UTC | 93% | 52% |  |  |
| GJ08CG1885 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:50:21 UTC | 96% | 66% |  |  |
| 0302AN0204 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:51:40 UTC | 59% | 47% |  |  |
| GJ08CM2525 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:53:17 UTC | 94% | 67% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:55:36 UTC | 72% | 49% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 14:55:37 UTC | 56% | 45% |  |  |
| 109BH1705 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:55:38 UTC | 84% | 50% |  |  |
| 6J24K5941 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:57:46 UTC | 97% | 62% |  |  |
| GJ05C00314 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:58:36 UTC | 96% | 65% |  |  |
| VEIHGJ000SZ282 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 14:59:26 UTC | 59% | 53% |  |  |
| GJO820005 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:04:12 UTC | 84% | 64% |  |  |
| GJ01HZ | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:05:54 UTC | 55% | 43% |  |  |
| GJ05RK3423 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:05:57 UTC | 100% | 69% |  |  |
| GJ08BS8816 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:06:02 UTC | 99% | 66% |  |  |
| PNIADADAI | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:06:50 UTC | 60% | 53% |  |  |
| J24AM8512 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:07:12 UTC | 95% | 69% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 15:07:16 UTC | 77% | 49% |  |  |
| GJ06PB1417 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:09:22 UTC | 100% | 69% |  |  |
| GJ27C2445 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:11:43 UTC | 99% | 62% |  |  |
| GJ18EG0053 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:11:52 UTC | 93% | 66% |  |  |
| GJ16CN2656 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:13:07 UTC | 99% | 59% |  |  |
| DL3CCE4892 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:13:13 UTC | 100% | 64% |  |  |
| GJ33B9648 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:13:59 UTC | 89% | 68% |  |  |
| 10010000 | cam06 | 06 Timbavadi gate-Junagadh | 2026-09-05 15:20:01 UTC | 50% | 62% |  |  |
| GJ01WY5468 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:22:10 UTC | 96% | 65% |  |  |
| GJ388E2678 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:22:48 UTC | 93% | 68% |  |  |
| 4GJOBDN0552 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:24:48 UTC | 84% | 67% |  |  |
| GJ09BK6694 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:24:53 UTC | 98% | 67% |  |  |
| 6J0B75779 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:25:38 UTC | 73% | 58% |  |  |
| GJ08FA5789 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:26:13 UTC | 95% | 59% |  |  |
| GJ13CE9474 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:26:49 UTC | 100% | 63% |  |  |
| GJD8DN8714 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:26:59 UTC | 91% | 62% |  |  |
| GJ08F71 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:29:01 UTC | 93% | 52% |  |  |
| JO0CR4289 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:31:23 UTC | 63% | 64% |  |  |
| 30610 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:31:41 UTC | 74% | 52% |  |  |
| G008483551 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:32:08 UTC | 81% | 64% |  |  |
| GJ0BDJ1225 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:32:25 UTC | 93% | 67% |  |  |
| GJ08AY4962 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:32:31 UTC | 99% | 67% |  |  |
| GJ31D4258 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:32:40 UTC | 98% | 58% |  |  |
| GJ01HD9416 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:32:54 UTC | 98% | 60% |  |  |
| GJ01M04865 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:33:07 UTC | 85% | 63% |  |  |
| 6J02DP3070 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:33:33 UTC | 91% | 64% |  |  |
| GJ00BN7658 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:34:40 UTC | 93% | 55% |  |  |
| 1W0R369E | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:35:31 UTC | 72% | 45% |  |  |
| 1030BA10556M | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:35:40 UTC | 70% | 52% |  |  |
| GJ08BS2556 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:35:45 UTC | 100% | 63% |  |  |
| GJ08AW9773 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:37:11 UTC | 95% | 73% |  |  |
| GJ1BEA6111 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:38:09 UTC | 95% | 65% |  |  |
| BU | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:38:50 UTC | 48% | 48% |  |  |
| GJ02EA4178 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:39:11 UTC | 99% | 66% |  |  |
| TAULE | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:39:15 UTC | 43% | 62% |  |  |
| GJ08CM1606 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:41:28 UTC | 98% | 69% |  |  |
| GJ06PJ9208 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:42:30 UTC | 99% | 63% |  |  |
| GJ08DS99 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:42:58 UTC | 89% | 56% |  |  |
| GJORAU521 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:45:50 UTC | 93% | 67% |  |  |
| GJ08CK9844 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:46:42 UTC | 97% | 64% |  |  |
| GJ18BV7419 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:49:31 UTC | 99% | 61% |  |  |
| UDEF681 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:51:34 UTC | 68% | 66% |  |  |
| SA0 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:52:46 UTC | 45% | 40% |  |  |
| GJ02ZZ9071 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:52:49 UTC | 99% | 67% |  |  |
| GJ08CH6192 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:53:25 UTC | 99% | 50% |  |  |
| GJ38BK9016 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:55:36 UTC | 99% | 70% |  |  |
| GJ23CJ1397 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:56:19 UTC | 100% | 61% |  |  |
| GJ01V28588 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:56:28 UTC | 93% | 68% |  |  |
| GJ01N9901 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:56:33 UTC | 73% | 42% |  |  |
| GJ27AH0143 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 15:59:12 UTC | 96% | 65% |  |  |
| GJ08N3929 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:00:44 UTC | 84% | 51% |  |  |
| GJ08DD7164 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:00:57 UTC | 97% | 68% |  |  |
| GJ02EG2482 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:02:09 UTC | 96% | 64% |  |  |
| GJ02EK5592 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:02:48 UTC | 99% | 65% |  |  |
| GJ01RN9528 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:03:23 UTC | 97% | 67% |  |  |
| G102815900 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:03:57 UTC | 98% | 61% |  |  |
| 18600822 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:04:23 UTC | 89% | 62% |  |  |
| 0J18Z12256 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:05:32 UTC | 94% | 68% |  |  |
| GJ08002758 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:07:03 UTC | 98% | 60% |  |  |
| 0J0ZEG2248 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:08:44 UTC | 89% | 66% |  |  |
| MAHINDRA | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:09:05 UTC | 98% | 55% |  |  |
| GHA003594 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:10:20 UTC | 49% | 55% |  |  |
| 63085 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:13:15 UTC | 65% | 61% |  |  |
| GJ08CR8399 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:14:47 UTC | 99% | 64% |  |  |
| GJ18BJ1589 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:15:21 UTC | 98% | 63% |  |  |
| GJ24K2716 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:15:32 UTC | 100% | 68% |  |  |
| GJ19AF6960 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:15:55 UTC | 100% | 61% |  |  |
| GJ02EK4518 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:20:30 UTC | 99% | 66% |  |  |
| GJ02CP7649 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:20:34 UTC | 100% | 71% |  |  |
| GJ09A07721 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:20:47 UTC | 85% | 40% |  |  |
| GJ27EB4486 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:21:50 UTC | 98% | 65% |  |  |
| WO1L10283 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:22:05 UTC | 53% | 70% |  |  |
| ONDN13830 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:22:41 UTC | 49% | 61% |  |  |
| GJ08APB155 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:22:46 UTC | 97% | 66% |  |  |
| GJ08BF5628 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:23:07 UTC | 93% | 63% |  |  |
| GJ08884133 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:23:22 UTC | 95% | 67% |  |  |
| GJ08DG5226 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:23:35 UTC | 96% | 60% |  |  |
| GJ08FA7261 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:23:56 UTC | 99% | 41% |  |  |
| GJ09BH0493 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:25:18 UTC | 99% | 56% |  |  |
| GJ02EK8147 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:25:33 UTC | 99% | 41% |  |  |
| GJ02EC3821 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:27:06 UTC | 98% | 68% |  |  |
| GJ08CC4804 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:27:37 UTC | 99% | 67% |  |  |
| GJ08CR1596 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:30:17 UTC | 99% | 69% |  |  |
| 0GJ18BF01287IO1 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:31:15 UTC | 80% | 65% |  |  |
| GJ15CF3114 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:33:49 UTC | 100% | 67% |  |  |
| GJ08F8964 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:34:16 UTC | 100% | 65% |  |  |
| GJ02EC6965 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:36:37 UTC | 99% | 66% |  |  |
| GJ27BL3567 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:37:12 UTC | 93% | 46% |  |  |
| 10BAU6282 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:37:42 UTC | 81% | 62% |  |  |
| GJ18EF6486 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:37:57 UTC | 95% | 63% |  |  |
| GJ08CC4466 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:39:51 UTC | 97% | 69% |  |  |
| GJ080J7791 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:40:20 UTC | 96% | 54% |  |  |
| 27GG | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:40:41 UTC | 93% | 62% |  |  |
| RJ19UC9371 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:41:05 UTC | 99% | 62% |  |  |
| CJ08CM8185 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:43:16 UTC | 93% | 67% |  |  |
| 7GJ39CD4500 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:45:22 UTC | 94% | 69% |  |  |
| PCTONVN2 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:47:13 UTC | 50% | 43% |  |  |
| GJ08FA2583 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:47:27 UTC | 99% | 65% |  |  |
| 6J08BH2406 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:48:19 UTC | 96% | 64% |  |  |
| GJ08DJ5462 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:49:01 UTC | 88% | 63% |  |  |
| GJ08BN2519 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:49:03 UTC | 98% | 41% |  |  |
| GJ21CB9792 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:50:16 UTC | 98% | 58% |  |  |
| GJ02DM8359 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:53:40 UTC | 92% | 64% |  |  |
| GJ09BL5360 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:53:50 UTC | 94% | 50% |  |  |
| 0024A0964 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:58:00 UTC | 64% | 52% |  |  |
| GJ24AA0564 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:58:03 UTC | 98% | 66% |  |  |
| 188ND028 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 16:59:47 UTC | 61% | 65% |  |  |
| SIKOTAR | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:00:54 UTC | 100% | 62% |  |  |
| GJ05CJ4470 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:02:07 UTC | 100% | 67% |  |  |
| WJORYV6586 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:02:09 UTC | 69% | 57% |  |  |
| 61J8888253 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:03:22 UTC | 70% | 49% |  |  |
| GJ098N5958 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:03:41 UTC | 97% | 68% |  |  |
| GJ088B3899 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:04:13 UTC | 92% | 53% |  |  |
| GJ08CK1982 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:04:39 UTC | 99% | 62% |  |  |
| J081A163 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:05:25 UTC | 68% | 74% |  |  |
| GJ08DP3986 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:07:16 UTC | 94% | 70% |  |  |
| GJ08FB0316 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:11:03 UTC | 99% | 66% |  |  |
| GJ06EH8370 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:11:49 UTC | 99% | 65% |  |  |
| GJ0BCC1477 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:11:50 UTC | 95% | 65% |  |  |
| GJ18BE8884 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:11:59 UTC | 99% | 69% |  |  |
| GJ08AJ8299 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:15:01 UTC | 99% | 62% |  |  |
| 6J00001239 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:15:29 UTC | 62% | 61% |  |  |
| GJ02AT4012 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:15:36 UTC | 97% | 63% |  |  |
| GJ188E6135 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:15:51 UTC | 95% | 65% |  |  |
| GJ080D5884 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:16:22 UTC | 91% | 65% |  |  |
| GJ08DD5884 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:16:24 UTC | 99% | 67% |  |  |
| J08BN0682 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:17:27 UTC | 95% | 54% |  |  |
| GJ15CL8419 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:18:36 UTC | 98% | 67% |  |  |
| GJ15CL8419 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:18:38 UTC | 100% | 66% |  |  |
| GJ18BP0026 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:19:09 UTC | 98% | 62% |  |  |
| GJ06PG7144 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:20:13 UTC | 95% | 66% |  |  |
| P | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:21:18 UTC | 82% | 46% |  |  |
| GJ08AP5130 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:22:39 UTC | 100% | 59% |  |  |
| 108 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:24:25 UTC | 95% | 75% |  |  |
| 16Z995 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:25:42 UTC | 56% | 60% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:28:11 UTC | 73% | 62% |  |  |
| GJ02CP6769 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:29:42 UTC | 99% | 48% |  |  |
| GASV9616 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:31:07 UTC | 67% | 55% |  |  |
| 0001V9784 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:31:33 UTC | 91% | 60% |  |  |
| GJ38BJ2318 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:32:12 UTC | 100% | 68% |  |  |
| GJ23CA1055 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:32:51 UTC | 99% | 68% |  |  |
| GJ01KM0142 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:32:54 UTC | 95% | 68% |  |  |
| HEDPSHOE6040 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:33:05 UTC | 48% | 59% |  |  |
| LLST | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:36:18 UTC | 42% | 69% |  |  |
| NL | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:36:34 UTC | 49% | 54% |  |  |
| GJ01RD4319 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:37:57 UTC | 99% | 67% |  |  |
| GJ08DM6861 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:38:24 UTC | 99% | 66% |  |  |
| JUIN | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:38:32 UTC | 92% | 40% |  |  |
| GJ23CE5320 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:39:21 UTC | 100% | 67% |  |  |
| GJ01HV5808 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:40:10 UTC | 99% | 66% |  |  |
| AR11A7623 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 17:40:38 UTC | 100% | 44% |  |  |
| GJ08006737 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:41:17 UTC | 96% | 68% |  |  |
| GJO1WK6108 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:42:38 UTC | 95% | 70% |  |  |
| GJ23CB1067 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:42:41 UTC | 100% | 67% |  |  |
| GJ02DE631 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:49:58 UTC | 98% | 63% |  |  |
| 10BDG9213 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:50:06 UTC | 54% | 51% |  |  |
| GJ12FH1752 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:57:36 UTC | 100% | 47% |  |  |
| GJ33T5028 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 17:59:56 UTC | 94% | 45% |  |  |
| GJ08CH9511 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:01:16 UTC | 99% | 59% |  |  |
| GJ06RF2538 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:02:34 UTC | 98% | 64% |  |  |
| GJ08AP7144 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:02:43 UTC | 91% | 63% |  |  |
| GJ01RD0841 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:03:22 UTC | 95% | 58% |  |  |
| GJ24BF9309 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:05:53 UTC | 98% | 63% |  |  |
| GJ23CF1114 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:06:29 UTC | 95% | 66% |  |  |
| GJ27TD3437 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:09:58 UTC | 100% | 60% |  |  |
| GJ01KY7305 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:11:00 UTC | 99% | 64% |  |  |
| GJ02EK7139 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:11:05 UTC | 100% | 67% |  |  |
| GJ01WN6591 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:11:20 UTC | 97% | 68% |  |  |
| GJOBAY5007 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:11:33 UTC | 90% | 57% |  |  |
| GJ08DP0764 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:11:41 UTC | 98% | 62% |  |  |
| GJ18BA1802 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:12:28 UTC | 96% | 68% |  |  |
| GJ02CA5830 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:12:32 UTC | 97% | 65% |  |  |
| GJ0822731 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:13:07 UTC | 94% | 61% |  |  |
| GJ01WF5052 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:15:20 UTC | 97% | 62% |  |  |
| Q0080G6802 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:16:58 UTC | 82% | 53% |  |  |
| GJ01HU9227 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:19:28 UTC | 99% | 61% |  |  |
| GJ01WF7558 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:19:39 UTC | 98% | 69% |  |  |
| GJ090C4635 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:19:47 UTC | 88% | 62% |  |  |
| GJ08CK2987 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:20:26 UTC | 100% | 64% |  |  |
| GJ028P3066 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:20:56 UTC | 98% | 54% |  |  |
| GJ02CP4084 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:22:07 UTC | 99% | 66% |  |  |
| GJ19AF4200 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:24:14 UTC | 100% | 60% |  |  |
| GJ16003373 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:25:49 UTC | 92% | 58% |  |  |
| GJ24AM6763 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:29:05 UTC | 99% | 66% |  |  |
| GJ18ZT1189 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:29:09 UTC | 96% | 69% |  |  |
| GJOBAK2561 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:29:43 UTC | 93% | 62% |  |  |
| 138211129 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:30:28 UTC | 79% | 53% |  |  |
| 6A5590 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:31:05 UTC | 93% | 67% |  |  |
| GJ08DJ81 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:31:24 UTC | 99% | 64% |  |  |
| RJ24CA7520 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:31:41 UTC | 100% | 60% |  |  |
| BXZ534 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:33:00 UTC | 76% | 43% |  |  |
| AGRG87530 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:33:06 UTC | 65% | 44% |  |  |
| GJ11BR6534 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:34:00 UTC | 100% | 64% |  |  |
| GJ02DA1614 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:34:01 UTC | 96% | 48% |  |  |
| POLICE | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:34:19 UTC | 92% | 42% |  |  |
| GJ0BBN7383 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:35:43 UTC | 94% | 59% |  |  |
| GJ08CS3349 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:36:34 UTC | 99% | 55% |  |  |
| 0363202675 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:36:53 UTC | 73% | 47% |  |  |
| DL8CAN0402 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:38:12 UTC | 91% | 63% |  |  |
| GJ08BF7604 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:41:07 UTC | 95% | 68% |  |  |
| GJ08ER7283 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:43:33 UTC | 90% | 43% |  |  |
| GJ02CP5431 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:47:50 UTC | 99% | 66% |  |  |
| GJ08DS1993 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:48:32 UTC | 100% | 63% |  |  |
| 335 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:48:58 UTC | 80% | 55% |  |  |
| GJ08DJ6902 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:49:09 UTC | 99% | 58% |  |  |
| 1 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 18:49:23 UTC | 47% | 48% |  |  |
| GJ08DG7909 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:50:45 UTC | 99% | 68% |  |  |
| GJ08DG7909 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:50:47 UTC | 90% | 67% |  |  |
| GJ08DJ8906 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:51:33 UTC | 99% | 65% |  |  |
| GJ04CJ5188 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:52:52 UTC | 99% | 65% |  |  |
| GJ02CP4040 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:53:08 UTC | 99% | 58% |  |  |
| 6J23M9909 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:54:18 UTC | 94% | 46% |  |  |
| GJOBA | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:54:38 UTC | 73% | 62% |  |  |
| GJ18BC6316 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:55:00 UTC | 100% | 50% |  |  |
| J08CS9948 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:55:04 UTC | 96% | 62% |  |  |
| TURIESTRE | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 18:55:41 UTC | 57% | 45% |  |  |
| GJ08AE3405 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:56:06 UTC | 98% | 62% |  |  |
| GJYBEBGT | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:56:11 UTC | 85% | 46% |  |  |
| GJ05CS6086 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:58:29 UTC | 99% | 68% |  |  |
| GJ08DM3012 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 18:58:59 UTC | 99% | 64% |  |  |
| AR01R7002 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 18:59:51 UTC | 95% | 49% |  |  |
| GJ17CE4116 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:00:22 UTC | 100% | 64% |  |  |
| 6113AT1698 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:00:26 UTC | 89% | 66% |  |  |
| GJ13A71698 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:00:30 UTC | 94% | 69% |  |  |
| GJ02DE4237 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:01:20 UTC | 99% | 63% |  |  |
| GJ02DE4237 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:01:23 UTC | 99% | 68% |  |  |
| 6308C67002 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:01:26 UTC | 81% | 54% |  |  |
| GJ08DH6060 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:01:28 UTC | 90% | 64% |  |  |
| GJ06E07392 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:03:07 UTC | 99% | 59% |  |  |
| FCJIE016232 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 19:03:48 UTC | 53% | 47% |  |  |
| GJ16AV0592 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:04:38 UTC | 100% | 57% |  |  |
| GJ01NU6319 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:04:43 UTC | 95% | 68% |  |  |
| GJ08DJ9900 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:04:45 UTC | 97% | 68% |  |  |
| 2234 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:05:06 UTC | 100% | 67% |  |  |
| GJ35AA3671 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:05:11 UTC | 100% | 66% |  |  |
| GJ01KH7519316 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:05:43 UTC | 74% | 57% |  |  |
| ARTIOIIZZ | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 19:05:58 UTC | 74% | 56% |  |  |
| GJ08FA0432 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:06:13 UTC | 99% | 62% |  |  |
| G102B03285 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:06:20 UTC | 94% | 65% |  |  |
| GJ08DG3644 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:06:23 UTC | 93% | 61% |  |  |
| GJ24AF9826 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:07:20 UTC | 100% | 64% |  |  |
| TATA | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 19:08:14 UTC | 97% | 45% |  |  |
| GJ08DN4325 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:08:33 UTC | 92% | 62% |  |  |
| GJ08EA2166 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:09:23 UTC | 94% | 65% |  |  |
| GJ2411065 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:09:35 UTC | 89% | 66% |  |  |
| GJ10EH2105 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:10:56 UTC | 100% | 62% |  |  |
| WWWIAH10 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:12:53 UTC | 68% | 42% |  |  |
| GJ02EG9559 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:13:01 UTC | 100% | 63% |  |  |
| SJ01KF8753 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:16:31 UTC | 99% | 46% |  |  |
| GJ02ER3549 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:16:53 UTC | 99% | 68% |  |  |
| GROUN2001103062 | cam12 | 12 Tri Mandir Adalaj Tollnaka | 2026-09-05 19:17:01 UTC | 63% | 62% |  |  |
| GJ24A03957 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:19:05 UTC | 99% | 59% |  |  |
| GJ08BH4062 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:19:34 UTC | 93% | 52% |  |  |
| MH02DG2284 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:20:16 UTC | 88% | 66% |  |  |
| GJ12FB3366 | cam22 | 28 BK Mervada tran Rasta | 2026-09-05 19:24:22 UTC | 96% | 61% |  |  |
