# 0.99.91 round 09991b (candidate 2): share R2 (2026-11-11)

- Candidate 2: claude/staging-09991 844f3c23, build 0.99.91, game sha256 b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (matched). Check files from 844f3c23.
- OLD: 0.99.9 (published), main bfbcbdf, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matched). Build master BM28, lead 51.
- Share as round 09991; fresh_walk, p926 and perf_check with R4. pf_f1 proof: 0.99.6 vs the candidate with every 0.99.7 switch, TP998, EV999_BLINK_ON, the four 0.99.91 switches and MC9991_REW_ON false.

## Results

| Check | Result | Minutes |
|---|---|---|
| cadet_test 0.99.9 vs candidate (alone) | ALL IDENTICAL, every view 0 px; errors none; taps the same | 0 |
| day_check 0, 1, 5, 7, 21, 22 | all DAY CHECK OK | 6 to 7 each |
| arrows_check endgo | ARROWS CHECK OK | 10 |
| intro_check (whole) | OK | 54 |
| intro_check --dinner | OK | 2 |
| intro_check --firsts | OK | 0 |
| path_check | PATH CHECK OK | 1 |
| arc_check | ARC CHECK OK | 0 |
| lines_check | PASS (0 errors, 116 warnings) | 0 |
| lines_check --day | PASS (0 errors) | 5 |
| pf_f1_same 0.99.9 vs candidate | F1 23674 checks, 0 mismatches; no page errors; fingerprints 30 differ (OLD has none of the new switches, so by design; prints FAILED for that reason only) | 0 |
| pf_f1_same 0.99.6 vs all-off copy (incl. MC9991_REW_ON false) | F1 23674 checks, 0 mismatches; fingerprints 30 same; PF F1 SAME OK | 0 |

fresh_walk, p926 and perf_check: R4's (not run here).

## Result: OK (my share). No NEW FAIL.
