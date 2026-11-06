# 0.99.8 round 0998: share R2 (2026-11-06)

- Candidate: claude/staging-0998 d7f5bd6, build 0.99.8, game sha256 298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462 (matched). Check files from d7f5bd6 (p926 with TB6's fix N, 3afefab3).
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8. Build master BM27, lead 50. Earlier records: plans/checks-0997-r2.md, plans/checks-0997b-r2.md (claude/checks-0997-r2).
- Setup as before (two browsers at most; own CADET_WORK /tmp/work-r2, /tmp/work-r2b). All-off copy for the pf_f1 proof: every 0.99.7 switch line and the TP998 line set false.

## cadet_test OLD BUILD (alone)

exit 1, `DIFFERENCES FOUND`; `DIFF state ['mem', 'calls', 'tris']` only; `errors A [] errors B []`; taps the same. The same
15 views and pixel counts as 0.99.7 (a_start 8424, b_wander10s 7273, c_rotated 6133, d_wallslow 7085, e_night 2600,
f_noshadow 5760, g_nocrew 665, h_crewback 10617, i_tap0 9027, i_tap1 23361, i_tap2 20920, i_tap3 57102, i_tap4 8679,
j_steer1 32167, j_steer2 13637), and every NEW picture is pixel-identical to 0.99.7 candidate 2's (0 px in all 15).
So all explained as in 0.99.7: hair caps and soles (CH1), the tracker ring (TP1), Fonseca's bunk (CH1), the Day 2 crew from
~07:45 (TRAD997, the Spice supper move). TP998's two changes don't show in cadet's views (Day 2 18:00 and later).

## Result: FAIL: fresh_walk point 5 (NEW, BM27's P; run by R4); perf from R6 pending

| Check | Ran by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD (alone) | R2 | exit 1, all explained (above) | 1 | `DIFFERENCES FOUND`, errors none, taps the same |
| intro_check (whole) | R2 | exit 0 | 47 | `OK` |
| intro_check --dinner | R2 | exit 0 | 2 | `OK` |
| intro_check --firsts | R2 | exit 0 | 0 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 116 warnings)` |
| lines_check --day | R2 | exit 0 | 4 | `lines_check --day: PASS (0 errors)` |
| day_check 0, 1, 5, 7, 21, 22 | R2 | exit 0 each | 5 | `DAY CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 12 | `ARROWS CHECK OK` |
| pf_f1_same OLD BUILD 10 | R2 | F1 OK; fingerprints differ by design | 0 | `F1 checks 23674 mismatches 0 None`, `page errors [] []`, `fingerprints 30 differ 30` (prints FAILED) |
| pf_f1_same proof: OLD vs 0.99.8 with every 0.99.7 switch and TP998 false | R2 | exit 0 | 0 | `fingerprints 30 differ 0 []`, `F1 checks 23674 mismatches 0`, `PF F1 SAME OK` |
| p926_check | R4 | exit 0 | | `P926 CHECK OK`; item 15: Brennan at the shelf 19:20, 7 lines, 7 bubbles, guess card held 3 min |
| fresh_walk BUILD 3 | R4 | **point 5 FAIL, NEW (BM27's P)** | | points 1-4 pass: briefing, Works bay arrow, 08:45 solo meeting, Day 2 booths arrow from 18:00 at the floor pin (never Booth 1), 'd2-booths:said' traced 18:16, errors []. Point 5: `long = [[2738, 'The call booths'], [3929, 'The call booths, Deck 3']]`: the Social marker keeps leading to booths that give nothing after the day's call (TP998_BOOTH_ON). In 0997b the same walk had long []. JSON plans/fw-0998-r4.json on claude/checks-0996-r4 |
| perf_check BUILD OLD (alone) | R6 | running (started 20:03) | | |

