# 0.99.4 full round: the five shares (lead 47, 2026-10-31; crew stories stage 2 + Tomas)

Same shares as plans/round-0990.md (lead 46), plus the story days. Cap 5: BM22 (R5) + four runners R1-R4 (all fresh on
the new account; the old seats can't be reached). Candidate = the claude/staging-0994 tip that BM22 names (0.99.3 +
ST1's crew stories stage 2 at the commit RV28 passed, STORIES2_ON switched on, build 0.99.4). BM22 sends the commit and
game sha256 in its GO; your file must match it.
OLD = 0.99.3, claude/integration 57eceec4 (game sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9).
Expected cadet differences: only where the new stories play (story beats, Mail, Calendar rows, planner hooks on Days
21-26 and 30); anything else is NEW and goes to BM22 + lead at once.
Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM22 + lead at once). Notes in
plans/checks-0994-rN.md on your own branch claude/checks-0994-rN. Known old: backlog 14 / perf one-off spikes
(re-measure alone twice).

| Share | Seat | Checks |
|---|---|---|
| R1 | fresh | player_check, bubble, puzzle, social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, 25, 26, arrows endstay |
| R2 | fresh | intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend, arrows endgo |
| R3 | fresh | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, title_check, day_check 6, 8, 23, 24 |
| R5 | BM22 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories, promo_beats, day_check 12, 13, 16, 17, 18, 19, 27 |

Not in the gate: controller_check reach (non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).
Sessions: lead 47 session_014zyJYM4mt9ZDCD5H9JZDtN; BM22 session_014zyJYNgBPdEPHLxTGrM889; R1-R4 in TEAM.md.
