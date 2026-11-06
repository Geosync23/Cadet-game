# 0.99.8 round 0998b (candidate 2, P fixed): share R2 (2026-11-06)

- Candidate 2: claude/staging-0998 bbb7bb0, build 0.99.8, game sha256 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3 (matched). Check files from bbb7bb0.
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8. Build master BM27, lead 50. Candidate 1's record: plans/checks-0998-r2.md.
- All-off copy for the pf_f1 proof: every 0.99.7 switch line and the TP998 line set false.

## cadet_test OLD BUILD (alone)

exit 1, `DIFFERENCES FOUND`; `DIFF state ['mem', 'calls', 'tris']` only; errors none; taps the same; the same 15 views and
px counts as 0.99.7 and 0.99.8 candidate 1, and every NEW picture pixel-identical to candidate 1's (0 px in all 15): all
explained (hair caps, soles, tracker ring, Fonseca's bunk, the Day 2 crew from ~07:45: TRAD997's Spice supper move).

## Result: OK

Every check in R2 passes on 0.99.8 candidate 2; P (fresh_walk point 5) is fixed. Ran by R2, except fresh_walk and p926
(R4) and perf_check (R6).

| Check | Ran by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD (alone) | R2 | exit 1, all explained (above) | 1 | `DIFFERENCES FOUND`, errors none, taps the same |
| intro_check (whole) | R2 | exit 0 | 43 | `OK` |
| intro_check --dinner | R2 | exit 0 | 2 | `OK` |
| intro_check --firsts | R2 | exit 0 | 0 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 116 warnings)` |
| lines_check --day | R2 | exit 0 | 4 | `lines_check --day: PASS (0 errors)` |
| day_check 0, 1, 5, 7, 21, 22 | R2 | exit 0 each | 5 | `DAY CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 10 | `ARROWS CHECK OK` |
| pf_f1_same OLD BUILD 10 | R2 | F1 OK; fingerprints differ by design | 0 | `F1 checks 23674 mismatches 0 None`, `page errors [] []`, fingerprints 30/30 differ (prints FAILED) |
| pf_f1_same proof: OLD vs 0.99.8 c2 with every 0.99.7 switch and TP998 false | R2 | exit 0 | 0 | `fingerprints 30 differ 0 []`, `F1 checks 23674 mismatches 0`, `PF F1 SAME OK` |
| fresh_walk BUILD 3 | R4 | exit 0, all five points pass | | briefing to "Ready when you are." 08:52, then the clock 08:53; Day 2 solo meeting (arrow 08:31); booths arrow from 18:00 at the floor pin, never Booth 1, 'd2-booths:said' 18:16; errors []; **stuck [], long [] (P fixed)**: the 21:38 toast "Really missing people. Find some company: the mess or the bow lounge." JSON plans/fw-0998b-r4.json on claude/checks-0996-r4 |
| p926_check | R4 | exit 0 | | `P926 CHECK OK` |
| perf_check BUILD OLD (alone) | R6 | exit 0 | 67 | `PERF CHECK OK (2 skipped: switch not in this build; 0 waiting: not built yet)`; no spike; draw calls in all 26 scenes identical to 0998 c1 in every view, vs OLD within 1, none over budget (highest 311); memory flat 470/41/93 (a week 472/41/93) as OLD; file 8.84 MB, load 7.6-8.1 s. plans/checks-0998b-r6.md on claude/checks-0998-r6 (8e6e50d) |

