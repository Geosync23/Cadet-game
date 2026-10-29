# 0.97.0 full round: share R2 (2026-10-28/29)

- Candidate (NEW): claude/staging-pad b9b7e3d7bdee47016477770349c5bfa7e8fc84e1, game sha256 0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f (matched BM20's).
- OLD: 0.96.0 fe11cd66 (claude/integration), sha256 332925003934b49686c080515e154131a07f7fe7a3c14fbe0f6f7684933a129e (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores.
- Two lanes (two browsers) for everything but perf_check, which ran alone afterwards (BM20's ask).

## Result: OK

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| intro_check (whole) | exit 0 | 53 | `OK` |
| perf_check NEW OLD | exit 1, then re-measured OK twice | 65 + 2x3 | one frame-time spike, did not repeat (below); memory flat: round trips 521/40/93 -> 521 -> 521, a week 521 -> 522 |
| cadet_test OLD NEW | exit 0 | 1 | `ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)` |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | exit 0 | 11 | `lines_check --day: PASS (0 errors)` |
| p926_check | exit 0 | 17 | `P926 CHECK OK` |
| day_check 0 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 1 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 5 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 7 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 21 | exit 0 | 7 | `DAY CHECK OK` |
| day_check 22 | exit 0 | 4 | `DAY CHECK OK` |
| weekend_check | exit 0 | 8 | `WEEKEND CHECK OK` |
| arrows_check endgo | exit 0 | 11 | `ARROWS CHECK OK` (ways asis, teachoff, track) |

## perf_check: the spike (noise, backlog 32's kind)

Whole run: `PROBLEM lantern supper, the mess Sat 18:30 trifold-folded-turned: js 2.04 -> 3.2 ms a frame`, the only
problem; draw calls, triangles and crew the same in OLD and NEW.

Re-measured alone twice (`PERF_SCENES='lantern supper' python3 perf_check.py NEW OLD`), trifold-folded-turned OLD -> NEW:
- re-measure 1: 1.97 -> 2.67 ms, `PERF CHECK OK`
- re-measure 2: 1.92 -> 1.9 ms, `PERF CHECK OK`

The spike didn't repeat, so it doesn't count (the guide: a one-off spike is noise). No FAIL in this share.
