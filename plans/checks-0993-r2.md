# 0.99.3 full round: share R2 (2026-10-30)

- Candidate (NEW): claude/staging-0993 df74ce0fbf33f40bb2cee71369ef589871a1eb94, game sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matched BM21's).
- OLD: 0.99.2 d180a704 (claude/integration), sha256 27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores. Two lanes (two browsers), detached, no time limit. The host was a little slow (p926 17 min against 13).
- Handed over, agreed before it started and skipped in my scripts (nothing ran twice): perf_check to R4, at lead 46's request.
- The change: intro_check (whole) has CH1's part 20 (--dinner) and CH2's call-home steps; both ran.

## Result: OK

| Check | Run by | Result | Minutes | Key lines |
|---|---|---|---|---|
| intro_check (whole) | R2 | exit 0 | 49 | `OK` (part 20, a reload mid-dinner, and the call-home card after eating both in the log) |
| perf_check NEW OLD | R4 (alone) | exit 1, then re-measured OK twice | 71 + 2 re-measures | two frame-time spikes that didn't repeat (below); memory flat |
| cadet_test OLD NEW | R2 | exit 0 | 1 | `ALL IDENTICAL` (as BM21 expected) |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | R2 | exit 0 | 9 | `lines_check --day: PASS (0 errors)` |
| p926_check | R2 | exit 0 | 17 | `P926 CHECK OK` |
| day_check 0 | R2 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 1 | R2 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 5 | R2 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 7 | R2 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 21 | R2 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 22 | R2 | exit 0 | 6 | `DAY CHECK OK` |
| weekend_check | R2 | exit 0 | 12 | `WEEKEND CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 14 | `ARROWS CHECK OK` |

R4's perf_check: plans/checks-0993-r4.md on claude/checks-0990-r4 (7661d266).
No FAIL in this share, so nothing was run on OLD apart from the OLD halves of cadet_test and perf_check.

## perf_check NEW OLD (R4, alone)

- Whole run: `PERF CHECK: 2 problem(s) (2 skipped: switch not in this build; 0 waiting)`:
  - `Sowing / harvest morning, garden 10:00 landscape: js 1.51 -> 2.85 ms a frame`
  - `Captain's address, auditorium Fri 16:10 trifold-folded: js 1.65 -> 3.03 ms a frame`
- Re-measured both alone twice (`PERF_SCENES='Sowing|Captain.s address'`): both runs `PERF CHECK OK`. As R4 reported them, NEW/OLD:
  Sowing 1.35/1.42 and 1.63/1.40 ms; Captain's address 1.34/2.46 and 1.66/2.20 ms. Neither spike repeated, so they don't
  count (one-off spikes are noise, backlog 32's kind).
- Memory flat: a week 470/41/93 -> 471/41/93; round trips 470/41/93 three times.
