# 0.99.0 full round: share R2 (2026-10-29)

- Candidate (NEW): claude/staging-099 a4c9febe2264f02adf812602de5614a5f3130889, game sha256 041a699c00cb28607d97ef4f8add5594b47b6e204294f9b93aab7e82adad4ee2 (matched BM21's).
- OLD: 0.98.0 37b858b4, sha256 81c07a059437fd391370af0133b9fff8c35ae56ad4d31718151b7274acce59b1 (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores.
- Two lanes (two browsers) for everything but perf_check, which ran alone afterwards. All detached (nohup), no time limit. Title screen ON: every check got past it.

## Result: OK

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| intro_check (whole) | exit 0 | 35 | `OK` |
| perf_check NEW OLD | exit 1, then re-measured OK twice | 54 (alone) + 2x3 | one frame-time spike that didn't repeat (below); draw calls lower in NEW; memory flat |
| cadet_test OLD NEW | exit 1, as expected | 1 | only the expected differences (below) |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | exit 0 | 7 | `lines_check --day: PASS (0 errors)` |
| p926_check | exit 0 | 13 | `P926 CHECK OK` (the reading corner part passes, FX24-2's) |
| day_check 0 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 1 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 5 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 7 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 21 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 22 | exit 0 | 5 | `DAY CHECK OK` |
| weekend_check | exit 0 | 9 | `WEEKEND CHECK OK` |
| arrows_check endgo | exit 0 | 11 | `ARROWS CHECK OK` (ways asis, teachoff, track, as in 0.97.0 and 0.98.0) |

No FAIL in this share, so nothing was run on OLD apart from the OLD halves of cadet_test and perf_check.

## cadet_test OLD NEW: the expected differences

Expected (BM21, plans/round-0990.md): RB1 turns 3-4 only, draw calls / memory / triangles down, and the user-approved corner
pixels (d_wallslow about 8 px, i_tap2 about 1 px). What came out:

- `DIFF state ['mem', 'calls', 'tris']`
- state_end OLD -> NEW: geometries 453 -> 414, textures 34 -> 36, draw calls 173 -> 142; place the same (Junior corridor, Deck 4).
- d_wallslow `differing px 8 max 18`, i_tap2 `differing px 1 max 24`; the other 13 shots `differing px 0 max 0`.
- No speech-bubble shift; no script errors in either; the taps the same.

## perf_check NEW OLD

- Draw calls: in all 127 scene views NEW is lower or equal to OLD, never higher; highest in NEW 312 (budget 450).
- Memory flat: OLD round trips 521/40/93 three times, a week 521 -> 522; NEW round trips 470/41/93 three times, a week 470 -> 471.
- The two Step 6 scenes are skipped in both builds (P5_STEP6 not in this build).
- The whole run's only problem: `PROBLEM weekend: Bread day, the galley Sun 07:25 landscape: js 1.42 -> 2.6 ms a frame`.

Re-measured alone twice (`PERF_SCENES='Bread day' python3 perf_check.py NEW OLD`), landscape OLD -> NEW:
- re-measure 1: 1.8 -> 1.5 ms, `PERF CHECK OK`
- re-measure 2: 1.94 -> 1.88 ms, `PERF CHECK OK`

The spike didn't repeat, so it doesn't count (a one-off spike is noise, backlog 32's kind). No FAIL in this share.
