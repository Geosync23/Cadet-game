# 0.99.1 full round: share R2 (2026-10-29)

- Candidate (NEW): claude/staging-0991 f77c26d9525395a290e2b902fedcbf09f4849364, game sha256 8e4ac5459ca78df284390d9438c09b7118ce5448d4c0093dbf9b894bf19e2d9d (matched BM21's).
- OLD: 0.99.0 6d5684ba (claude/integration), sha256 041a699c00cb28607d97ef4f8add5594b47b6e204294f9b93aab7e82adad4ee2 (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores.
- Two lanes (two browsers) for everything but perf_check, which ran alone afterwards. All detached (nohup), no time limit.
- The change: the title screen starts asleep ("TAP TO WAKE THE TERMINAL"); every check got past it.

## Result: OK

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| intro_check (whole) | exit 0 | 35 | `OK` |
| perf_check NEW OLD | exit 0 | 53 (alone) | `PERF CHECK OK (2 skipped: switch not in this build; 0 waiting: not built yet)` |
| cadet_test OLD NEW | exit 0 | 1 | `ALL IDENTICAL` (as BM21 expected) |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | exit 0 | 7 | `lines_check --day: PASS (0 errors)` |
| p926_check | exit 0 | 13 | `P926 CHECK OK` |
| day_check 0 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 1 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 5 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 7 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 21 | exit 0 | 5 | `DAY CHECK OK` |
| day_check 22 | exit 0 | 4 | `DAY CHECK OK` |
| weekend_check | exit 0 | 9 | `WEEKEND CHECK OK` |
| arrows_check endgo | exit 0 | 10 | `ARROWS CHECK OK` (ways asis, teachoff, track) |

No FAIL in this share, so nothing was run on OLD apart from the OLD halves of cadet_test and perf_check.

## perf_check NEW OLD

- Draw calls the same as OLD in all 127 scene views (highest 312, budget 450).
- Memory flat and the same in both: round trips 470/41/93 three times, a week 470 -> 471.
- No PROBLEM lines, no frame-time spike. The two Step 6 scenes are skipped in both builds (P5_STEP6 not in this build).
