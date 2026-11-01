# 0.99.5 full round: share R2 (2026-10-31 to 11-01)

- Candidate (NEW): claude/staging-0995 e00bfabd8cefbfd66c5c71f2a22676c763a7eb8d, game sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matched BM23's GO; lead 48 confirmed that's the intended file, its earlier 5733867d superseded).
- OLD: 0.99.4, claude/staging-0994 596712bc, sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores. cadet_test strictly alone first, then two lanes (two browsers), then perf_check alone (nothing else running), its re-measures alone too. Check scripts from the candidate commit.
- OB2's intro probes: OB2 committed no probe script (BM23 confirmed); covered by intro_check whole, --dinner and --firsts. Nothing extra run.

## Result: OK

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| cadet_test OLD BUILD (alone) | exit 1, only the expected differences | 1 | `DIFFERENCES FOUND`: Oona's speech-bubble line only (below) |
| intro_check (whole) | exit 0 | 51 | `OK` |
| intro_check --dinner | exit 0 | 4 | `OK` |
| intro_check --firsts | exit 0 | 1 | `OK` |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail; 112 as in 0.99.4) |
| lines_check --day | exit 0 | 9 | `lines_check --day: PASS (0 errors)` |
| p926_check | exit 0 | 17 | `P926 CHECK OK` |
| day_check 0 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 1 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 5 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 7 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 21 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 22 | exit 0 | 6 | `DAY CHECK OK` |
| weekend_check | exit 0 | 12 | `WEEKEND CHECK OK` |
| arrows_check endgo | exit 0 | 11 | `ARROWS CHECK OK` |
| perf_check BUILD OLD (alone) | exit 1, then re-measured: 3 of 4 OK, no spike repeated | 69 + 4 x 3 | one-off frame-time spikes (below); draw calls the same or 1 apart; memory flat |

No FAIL in this share apart from perf's one-off spikes, so nothing else needed a run on OLD.

## cadet_test OLD BUILD

As BM23 expected: a_start to e_night, i_tap0-4, j_steer2 `differing px 0 max 0`; f_noshadow 24189, g_nocrew 24550,
h_crewback 24742 px, all inside Oona's speech bubble (looked at: OLD "The washer's fixed. Clean socks for everyone." ->
NEW "Water tastes right again. I didn't know it tasted wrong until it didn't.", JB2's change); j_steer1 6 px max 1
(noise). No state difference, `errors A [] errors B []`, taps the same. Nothing NEW.

## perf_check BUILD OLD

- Whole run (alone, 69 min): exit 1, one problem only: `PROBLEM lantern supper, the mess Sat 18:30 portrait: js 2.04 -> 3.09 ms a frame`.
  `PERF CHECK: 1 problem(s) (2 skipped: switch not in this build; 0 waiting: not built yet)`.
- Draw calls: in 127 scene views, 117 the same, 10 one apart (Sowing / harvest morning +1 in three views; garden
  picnic -1 in seven); highest in NEW 312 (budget 450).
- Memory: round trips 470/41/93 three times in both; a week 470 -> 471 (OLD) and 470 -> 472 (NEW): no round-trip growth
  (backlog 14 not showing).
- Re-measured alone (`PERF_SCENES='lantern supper'`), OLD -> NEW ms a frame:
  - 1: portrait 2.68 -> 2.33 (the first spike didn't repeat), but `PROBLEM ... trifold-folded-turned: js 2.27 -> 3.52`, exit 1
  - 2: `PERF CHECK OK` (trifold-folded-turned 2.02 -> 2.69, portrait 2.28 -> 2.99, under the line)
  - 3 and 4 (taken because the same scene showed twice): both `PERF CHECK OK`; trifold-folded-turned 2.13 -> 2.09 and 2.34 -> 2.27
- Each spike was in a different view and none repeated; in other measures NEW was the faster one in the same views; draw
  calls and triangles in that scene are the same in both builds. One-off spikes: noise (backlog 32's kind), not a FAIL.
