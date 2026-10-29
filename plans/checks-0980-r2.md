# 0.98.0 full round: share R2 (2026-10-29)

- Candidate (NEW): claude/staging-pad 7a2ae7d2d5913acb4c05e5a746ca80bb560ccf26, game sha256 22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f (matched BM20's).
- OLD: 0.97.0 610ad7f1 (claude/integration), sha256 0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores.
- Two lanes (two browsers) for everything but perf_check, which ran alone afterwards. All detached (nohup), no time limit.

## Result: OK

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| intro_check (whole) | exit 0 | 34 | `OK` |
| perf_check NEW OLD | exit 0 | 53 (alone) | `PERF CHECK OK (2 skipped: switch not in this build; 0 waiting: not built yet)`; draw calls lower in NEW (below) |
| cadet_test OLD NEW | exit 1, as expected | 1 | only `mem` and `calls` differ (below); all 15 screenshots 0 px different |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | exit 0 | 7 | `lines_check --day: PASS (0 errors)` |
| p926_check | exit 0 | 13 | `P926 CHECK OK` |
| day_check 0 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 1 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 5 | exit 0 | 2 | `DAY CHECK OK` |
| day_check 7 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 21 | exit 0 | 4 | `DAY CHECK OK` |
| day_check 22 | exit 0 | 4 | `DAY CHECK OK` |
| weekend_check | exit 0 | 9 | `WEEKEND CHECK OK` |
| arrows_check endgo | exit 0 | 10 | `ARROWS CHECK OK` (ways asis, teachoff, track, as in 0.97.0) |

No FAIL in this share, so nothing was run on OLD apart from the OLD halves of cadet_test and perf_check.

## cadet_test OLD NEW: the expected difference

BM20's expectation for this candidate: only `mem` and `calls` differ (draw calls fall by design, RB1's render turn), renderer
noise at most 1 level. That is what came out:

- `DIFF state ['mem', 'calls']`
- state_end OLD -> NEW: geometries 453 -> 422, textures 34 -> 36, draw calls 173 -> 142; place the same (Junior corridor, Deck 4).
- Every screenshot (a_start ... j_steer2, 15) `differing px 0 max 0`; no script errors in either; the taps the same.

## perf_check NEW OLD

- Draw calls: in all 127 scene views NEW is lower or equal to OLD, never higher (e.g. Bread day portrait 283 -> 253,
  the big jigsaw portrait 173 -> 113); highest in NEW 357 (budget 450).
- Memory flat: OLD round trips 521/40/93 three times, a week 521 -> 522; NEW round trips 506/41/93 three times, a week 506 -> 507.
- No PROBLEM lines, no frame-time spike. The two Step 6 scenes are skipped in both builds (P5_STEP6 not in this build).
