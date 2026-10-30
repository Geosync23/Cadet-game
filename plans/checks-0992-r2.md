# 0.99.2 full round: share R2 (2026-10-29/30)

- Candidate (NEW): claude/staging-0992 60d477e8619a373f8d7e6b27a59236f64d5d2427, game sha256 27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matched BM21's).
- OLD: 0.99.1 bc4579aa (claude/integration), sha256 8e4ac5459ca78df284390d9438c09b7118ce5448d4c0093dbf9b894bf19e2d9d (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores. Two lanes (two browsers), detached, no time limit.
- My container restarted onto a slow host this round (about 2.5x slower: load ~9 on 4 cores with only my two browsers). With lead 46 and BM21, five not-started checks were handed over, each agreed before it started and skipped in my scripts, so nothing ran twice: day_check 0, 1, 5 and arrows endgo to BM21 (R5); perf_check to R4.
- The changes: title music C's melody sooner; New game's hand-over keeps the terminal up (intro_check goes through it).

## Result: OK

| Check | Run by | Result | Minutes | Key lines |
|---|---|---|---|---|
| intro_check (whole) | R2 | exit 0 | 72 (slow host) | `OK` |
| perf_check NEW OLD | R4 (alone) | exit 1, then re-measured OK twice | 71 + 2 re-measures | one frame-time spike that didn't repeat (below); draw calls identical; memory flat |
| cadet_test OLD NEW | R2 | exit 0 | 1 | `ALL IDENTICAL` (as BM21 expected) |
| path_check | R2 | exit 0 | 2 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail) |
| lines_check --day | R2 | exit 0 | 7 | `lines_check --day: PASS (0 errors)` |
| p926_check | R2 | exit 0 | 25 (slow host) | `P926 CHECK OK` |
| day_check 0 | BM21 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 1 | BM21 | exit 0 | 7 | `DAY CHECK OK` |
| day_check 5 | BM21 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 7 | R2 | exit 0 | 10 | `DAY CHECK OK` |
| day_check 21 | R2 | exit 0 | 10 | `DAY CHECK OK` |
| day_check 22 | R2 | exit 0 | 10 | `DAY CHECK OK` |
| weekend_check | R2 | exit 0 | 18 | `WEEKEND CHECK OK` |
| arrows_check endgo (default ways) | BM21 | exit 0 | 13 | `ARROWS CHECK OK` |

BM21's four: plans/checks-0992-r5.md on claude/handover-bm21. R4's perf_check: plans/checks-0992-r4.md on claude/checks-0990-r4 (a1ab5bf9).
No FAIL in this share, so nothing was run on OLD apart from the OLD halves of cadet_test and perf_check.

## perf_check NEW OLD (R4, alone)

- Whole run: `PERF CHECK: 1 problem(s) (2 skipped: switch not in this build; 0 waiting)`; the only problem:
  `PROBLEM the Line supper, the mess Sun 18:30 portrait-wide: js 2.11 -> 3.14 ms a frame`.
- Re-measured alone twice (`PERF_SCENES='Line supper'`), portrait-wide NEW/OLD: 2.1/2.56 ms and 2.83/2.35 ms, both `PERF CHECK OK`
  (corrected 2026-10-30: R4 first sent these the wrong way round; perf_check prints OLD first).
  The spike didn't repeat, so it doesn't count (a one-off spike is noise, backlog 32's kind).
- Draw calls identical NEW/OLD in every scene. Memory flat: week 470/41/93 -> 471/41/93; round trips 470/41/93 three times.
