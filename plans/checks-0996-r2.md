# 0.99.6 full round: share R2 (2026-11-01)

- Candidate (NEW): claude/staging-0996 f3dbd11 (lead 49's GO; BM24's GO named b97cb98, which differs only in plans/round-0996.md), build 0.99.6, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matched). All four picture options off (they are URL flags only: pfpr, pfsh, pfcap, pfaa).
- OLD: 0.99.5, claude/integration 6475bb30, game sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matched).
- Setup: playwright (pip) with CADET_CHROME=/opt/pw-browsers/chromium; three.js r128 and acorn 8.12.1 by npm pack in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b); numpy, pillow; 4 cores. cadet_test alone first, then two lanes (two browsers). Check scripts from the candidate commit.
- Handed over (agreed between runners, lead copied; I started none of them): perf_check BUILD OLD to R4 (alone on its machine); arrows endgo, pf_f1_same OLD BUILD 10 and p926_check to R6 (plans/checks-0996-r6.md on claude/checks-0996-r6).
- intro_check (whole) and day_check 22: I restarted the lane scripts mid-run to drop the handed-over checks; those two runs carried on untouched but their exit codes weren't recorded. Judged by the last line (OK / DAY CHECK OK) and no FAIL, PROBLEM or Traceback anywhere in either log.

## Result: OK

| Check | Ran by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD (alone) | R2 | exit 0 | 1 | `ALL IDENTICAL`: every view `differing px 0 max 0`, `errors A [] errors B []`, taps the same (as BM24 expected) |
| intro_check (whole) | R2 | OK (exit not kept, above) | 80 | `OK` |
| intro_check --dinner | R2 | exit 0 | 3 | `OK` |
| intro_check --firsts | R2 | exit 0 | 1 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (112 as in 0.99.5) |
| lines_check --day | R2 | exit 0 | 7 | `lines_check --day: PASS (0 errors)` |
| day_check 0 | R2 | exit 0 | 9 | `DAY CHECK OK` |
| day_check 1 | R2 | exit 0 | 9 | `DAY CHECK OK` |
| day_check 5 | R2 | exit 0 | 9 | `DAY CHECK OK` |
| day_check 7 | R2 | exit 0 | 10 | `DAY CHECK OK` |
| day_check 21 | R2 | exit 0 | 10 | `DAY CHECK OK` |
| day_check 22 | R2 | OK (exit not kept, above) | 10 | `DAY CHECK OK` |
| weekend_check | R2 | exit 0 | 17 | `WEEKEND CHECK OK` |
| arrows_check endgo | R6 | exit 0 | 11 | `ARROWS CHECK OK`; endgo:track settled day 35 'go', missed 0, stuck 0 |
| pf_f1_same OLD BUILD 10 | R6 | exit 0 | | `fingerprints 30 differ 0 []`, `F1 checks 23674 mismatches 0 None`, `page errors [] []`, `PF F1 SAME OK` |
| p926_check | R6 | exit 0 | | `P926 CHECK OK` |
| perf_check BUILD OLD (alone) | R4 | exit 1, then re-measured alone twice: OK | | `PERF CHECK: 2 problem(s) (2 skipped: switch not in this build; 0 waiting: not built yet)`, both one-off frame-time spikes (below) |

No FAIL in this share apart from perf's one-off spikes, so nothing needed a run on OLD.

## perf_check BUILD OLD (R4, alone, 65 min; plans/checks-0996-r4.md on claude/checks-0996-r4 f13df99)

- Two problems, both frame-time spikes: `the Line ceremony, bow lounge Sun 14:45 trifold-folded: js 1.23 -> 2.32 ms` and
  `Veyli vessel: the parts chain, shuttle bay Sun 13:30 landscape: js 1.35 -> 2.56 ms`.
- Each re-measured alone twice (PERF_SCENES), both times `PERF CHECK OK`: Line ceremony trifold-folded NEW 2.59 / 1.63 vs
  OLD 2.36 / 1.74; Veyli shuttle bay landscape NEW 1.38 / 1.49 vs OLD 1.84 / 1.52. Not repeated: noise (backlog 32), not a FAIL.
- Draw calls, triangles and particles identical to OLD in every scene and layout (picture options off, as expected).
- Memory: a week 470/41/93 -> 472/41/93, round trips 470/41/93 flat, as OLD (backlog 14 not showing). Load 7.5-7.7 s (OLD 7.4-7.9).
- The 2 skipped: Step 6 scenes, P5_STEP6 not in this build (same on OLD).
