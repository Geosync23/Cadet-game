# 0.99.4 full round: share R2 (2026-10-31)

- Candidate (NEW): claude/staging-0994 8976965effdbff3473a85f31b4deb7c7f3a4a669, game sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matched BM22's; `STORIES2_ON = true`).
- OLD: 0.99.3, claude/integration 57eceec4, sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matched).
- Setup: playwright (pip), three.js r128 + acorn 8.12.1 in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b), CADET_CHROME=/opt/pw-browsers/chromium; 4 cores. cadet_test strictly alone first, then two lanes (two browsers), detached, no time limit. Check scripts from the candidate commit.
- Handed over, agreed before it started (nothing ran twice): perf_check BUILD OLD to R4 (R4 offered when its share finished; BM22 suggested it). R4 reports it to BM22 and the lead.

## Result: OK (my part; perf_check is with R4)

| Check | Run by | Result | Minutes | Key lines |
|---|---|---|---|---|
| cadet_test OLD BUILD | R2 (alone) | exit 0 | 1 | `ALL IDENTICAL` |
| intro_check (whole) | R2 | exit 0 | 44 | `OK` |
| path_check | R2 | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | R2 | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | R2 | exit 0 | 0 | `lines_check: PASS (0 errors, 112 warnings)` (warnings never fail; 112 as in 0.99.0) |
| lines_check --day | R2 | exit 0 | 8 | `lines_check --day: PASS (0 errors)` |
| p926_check | R2 | exit 0 | 15 | `P926 CHECK OK` |
| day_check 0 | R2 | exit 0 | 6 | `DAY CHECK OK` |
| day_check 1 | R2 | exit 0 | 3 | `DAY CHECK OK` |
| day_check 5 | R2 | exit 0 | 5 | `DAY CHECK OK` |
| day_check 7 | R2 | exit 0 | 5 | `DAY CHECK OK` |
| day_check 21 | R2 | exit 0 | 5 | `DAY CHECK OK` |
| day_check 22 | R2 | exit 0 | 6 | `DAY CHECK OK` |
| weekend_check | R2 | exit 0 | 10 | `WEEKEND CHECK OK` |
| arrows_check endgo | R2 | exit 0 | 12 | `ARROWS CHECK OK` (ways asis, teachoff, track, as in earlier rounds) |
| perf_check BUILD OLD | R4 | see R4's report | | |

No FAIL in this share, so nothing needed a run on OLD (apart from cadet_test's OLD half).

## cadet_test OLD BUILD

ALL IDENTICAL: all 15 shots `differing px 0 max 0`, no script errors in either build (`errors A [] errors B []`), the
taps the same (`['Very hungry', 'Missing people', 'Missing people', 'Your bunk', 'Your bunk']`). That's as expected:
cadet_test plays Day 0 on Deck 4, and the new stories play on Days 21-26 and 30. It matches BM22's own cadet run.
