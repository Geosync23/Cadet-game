# 0.99.7 round 0997b (candidate 2): share R2 (2026-11-06)

- Candidate 2: claude/staging-0997 c052cc8, game sha256 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9 (matched). Check files from c052cc8.
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8. Build master BM26, lead 50. Candidate 1's record: plans/checks-0997-r2.md.
- Setup as candidate 1 (two browsers at most; own CADET_WORK /tmp/work-r2, /tmp/work-r2b).

## cadet_test OLD BUILD (alone)

exit 1, `DIFFERENCES FOUND`; `DIFF state ['mem', 'calls', 'tris']` only; `errors A [] errors B []`; taps the same.
Every NEW picture is pixel-identical to candidate 1's NEW picture (0 px in all 15 views), so the differences and their
causes are exactly candidate 1's (plans/checks-0997-r2.md, pictures in plans/checks-0997-r2-cadet/):

| View | px | What differs |
|---|---|---|
| a_start | 8424 | hair (CH_HAIR), soles (CH_SOLE) |
| b_wander10s | 7273 | the same |
| c_rotated | 6133 | the same |
| d_wallslow | 7085 | the same |
| e_night | 2600 | the same; Fonseca 0.1 m over in a bunk (CH1) |
| f_noshadow | 5760 | hair, soles |
| g_nocrew | 665 | the player's hair and soles |
| h_crewback | 10617 | hair, soles |
| i_tap0 | 9027 | hair, soles; tracker ring (TP1); Pell 0.2 m (TRAD997: the Spice supper move, by design) |
| i_tap1 | 23361 | hair, soles, tracker ring; crew elsewhere from Day 2 ~07:45 (TRAD997), bubbles follow |
| i_tap2 | 20920 | the same |
| i_tap3 | 57102 | the same |
| i_tap4 | 8679 | the same |
| j_steer1 | 32167 | the same |
| j_steer2 | 13637 | the same |

## Result: FAIL (p926_check item 15, NEW, run by R4); perf from R6 pending

| Check | Ran by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD (alone) | R2 | exit 1, all explained (above) | 1 | `DIFFERENCES FOUND`, errors none, taps the same |
| intro_check (whole) | R2 | exit 0 | 48 | `OK` |
| intro_check --dinner | R2 | exit 0 | 2 | `OK` |
| intro_check --firsts | R2 | exit 0 | 0 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 116 warnings)` (K fixed; warnings never fail) |
| lines_check --day | R2 | exit 0 | 4 | `lines_check --day: PASS (0 errors)` |
| day_check 0, 1, 5, 7, 21, 22 | R2 | exit 0 each | 5-6 | `DAY CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 12 | `ARROWS CHECK OK` |
| pf_f1_same OLD BUILD 10 | R2 | F1 OK; fingerprints differ by design | 0 | `F1 checks 23674 mismatches 0 None`, `page errors [] []`, `fingerprints 30 differ 30` (prints FAILED) |
| pf_f1_same proof: OLD vs candidate 2 with every 0.99.7 switch false | R2 | exit 0 | 0 | `fingerprints 30 differ 0 []`, `F1 checks 23674 mismatches 0`, `PF F1 SAME OK` |
| fresh_walk BUILD 3 | R4 | exit 0; points 1, 2, 4, 5 pass; 3 partly | | Day 1: arrow to the Works bay 08:20, briefing 08:50-08:53 to its end, then the clock 08:53; Day 2: solo meeting arrow 08:31, scene 08:45; booths arrow 17:46, booth used 17:45 and 18:08, but Leila's scene not in the record (the player had called home at 12:32): for BM26/TP1 to judge; page errors none; stuck none. json: plans/fw-0997b-r4.json (R4's notes) |
| p926_check | R4 | **exit 1, NEW** | | item 15 (Spice shelf supper): "Brennan at the spice shelf by 18:40 (None)", 0 lines, 0 bubbles, no guess card; OLD d7ad4c58 `P926 CHECK OK` (Brennan 18:20, 7 lines). TB6 moved the supper after dinner (TRAD997_ON): the check or the game, for BM26 and TB6 |
| perf_check BUILD OLD (alone) | R6 | running (started 16:26) | | |

