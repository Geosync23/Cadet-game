# 0.99.9 round 0999: share R2 (2026-11-07)

- Candidate: claude/staging-0999 8d8073a9, build 0.99.9, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matched). Check files from 8d8073a9.
- OLD: 0.99.8 (published), main 33c737b, game sha256 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3 (matched). Build master BM27, lead 51.
- Share as round 0998; fresh_walk and p926 with R4 (session_01GKuymmzABL4xHF9xBhM9fE, agreed by BM27). pf_f1 proof: OLD 0.99.6 vs the candidate with every 0.99.7 switch, the TP998 line and EV999_BLINK_ON false.

## cadet_test OLD BUILD (alone)

exit 0, `ALL IDENTICAL`: every view `differing px 0 max 0`, `errors A [] errors B []`, taps the same (as expected: the
blink is Day 4 14:08 only).

## Result: OK

Every check in R2 passes on 0.99.9. Ran by R2, except fresh_walk, p926 and perf_check (R4; perf via R6 after R6's restart).

| Check | Ran by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD (alone) | R2 | exit 0 | 1 | `ALL IDENTICAL` |
| intro_check (whole) | R2 | exit 0 | 47 | `OK` |
| intro_check --dinner | R2 | exit 0 | 2 | `OK` |
| intro_check --firsts | R2 | exit 0 | 0 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 116 warnings)` |
| lines_check --day | R2 | exit 0 | 4 | `lines_check --day: PASS (0 errors)` |
| day_check 0, 1, 5, 7, 21, 22 | R2 | exit 0 each | 5-6 | `DAY CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 12 | `ARROWS CHECK OK` |
| pf_f1_same OLD (0.99.8) BUILD 10 | R2 | exit 0 | 0 | `fingerprints 30 differ 0 []`, `F1 checks 23674 mismatches 0`, `page errors [] []`, `PF F1 SAME OK` (OLD is 0.99.8 now: the fingerprints match outright) |
| pf_f1_same proof: 0.99.6 vs the candidate with every 0.99.7 switch, TP998 and EV999_BLINK_ON false | R2 | exit 0 | 0 | `fingerprints 30 differ 0 []`, `PF F1 SAME OK` |
| fresh_walk BUILD 3 | R4 | exit 0, all five points pass | | long [], stuck [] |
| p926_check | R4 | exit 0 | | `P926 CHECK OK` |
| perf_check BUILD OLD (alone) | R4 | exit 1, then re-measured alone twice each: OK (backlog 32) | | two one-off frame-time spikes (the Line supper portrait js 1.95 -> 3.41 ms; Veyli parts chain trifold-folded-turned 1.34 -> 2.38 ms), neither repeated (both re-measures `PERF CHECK OK`); draw calls, gl and triangles identical to 0.99.8 in all 20 shared scenes; the blink scene 217 calls portrait; memory flat; load as OLD. plans/checks-0999-r4.md on claude/checks-0999-r4 (29d897b) |

Also for R3 (its share, taken over at R3's and lead 51's ask): sound_check proof runs, each alone: OLD 0.99.8 once, the
candidate twice (below).


## R3's sound_check proof runs (each alone, at R3's and lead 51's ask)

| Run | Build | Result | Key lines |
|---|---|---|---|
| 1 | OLD 0.99.8 (33c737b worktree) | exit 1 | `SOUND CHECK FAILED`; `hide while resuming: suspended` (hide OK); the FAIL: `live: after a stall the band plays nothing late, and plays on ([0, 14, 0, 0], ['jam', 8, 1])` |
| 2 | candidate 8d8073a9 | exit 0 | `SOUND CHECK OK`; `hide while resuming: suspended` |
| 3 | candidate 8d8073a9 | exit 0 | `SOUND CHECK OK`; `hide while resuming: suspended` |

R3's candidate FAIL (hide while resuming: running) didn't repeat in two alone runs; OLD fails a different timing line once.
One-off timing races in the check, not the build. Sent to R3, BM27 and lead 51.
