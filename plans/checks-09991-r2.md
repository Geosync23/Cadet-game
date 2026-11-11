# 0.99.91 round 09991: share R2 (2026-11-11)

- Candidate: claude/staging-09991 4d8869ec, build 0.99.91, game sha256 475bac8605fe9e26d2cd6035bcbd924dff315bac7eecdd39be12ff287f5b453e (matched). Check files from 4d8869ec.
- OLD: 0.99.9 (published), main bfbcbdf, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matched). Build master BM28, lead 51.
- Share as round 0999; fresh_walk, p926 and perf_check with R4 (plans/round-09991.md). pf_f1 proof: 0.99.6 vs the candidate with every 0.99.7 switch, TP998, EV999_BLINK_ON and the four 0.99.91 switches (TP9991_SD_ON, EV9991_SIM_ON, TB9991_DRILL_ON, CR9991_RESULTS_ON) false.

## cadet_test OLD BUILD (alone)

exit 0, `ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)`: i_tap3 236 px max 1 (the software
renderer's one-level rounding, which the check allows), every other view 0 px; errors none; taps the same.

## The rest (two lanes)

| Check | Result | Minutes |
|---|---|---|
| day_check 0, 1, 5, 7, 21, 22 | all DAY CHECK OK | 7 to 8 each |
| arrows_check endgo | ARROWS CHECK OK | 10 |
| intro_check (whole) | OK | 60 |
| intro_check --dinner | OK | 3 |
| intro_check --firsts | OK | 1 |
| path_check | PATH CHECK OK | 1 |
| arc_check | ARC CHECK OK | 0 |
| lines_check | PASS (0 errors, 116 warnings) | 0 |
| lines_check --day | PASS (0 errors) | 5 |
| pf_f1_same 0.99.9 vs candidate | F1 23674 checks, 0 mismatches; no page errors; fingerprints 30 differ (OLD has none of the four new switches, so by design; prints FAILED for that reason only) | 0 |
| pf_f1_same 0.99.6 vs all-off copy | F1 23674 checks, 0 mismatches; fingerprints 30 same; PF F1 SAME OK | 0 |

fresh_walk, p926 and perf_check: R4's (handed over, not run here).

## Result: OK (my share). No NEW FAIL.
