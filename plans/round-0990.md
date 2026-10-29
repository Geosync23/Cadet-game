# 0.99.0 full round: the five shares (lead 46, 2026-10-29; balance + backlog + title screen + render turns)

Cap 5 (the user): BM21 + four runners. Candidate = claude/staging-099 tip that BM21 names (0.98.0 + SD3-1, EV2 seated
dinner, BB1 backlog, TB1 title on + music C, RB1 turns 3-4, OP1 nights day-arrow, BAL2 balance; build 0.99.0).
OLD = 0.98.0, claude/integration 37b858b4 (game sha256 81c07a05...59b1).
Expected cadet differences: RB1 turns 3-4 only (draw calls / memory down; the user-approved corner pixels, 1-8 px in
14 of 267 shots). Title screen is ON: checks that start a game must get past it (title_check covers the screen itself).
Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM21 + lead at once). Notes in
plans/checks-0990-rN.md on your own branch claude/checks-0990-rN. Known old: backlog 14 / perf one-off spikes
(re-measure). Should now PASS (fixed in 0.98/0.99, so a FAIL here is NEW): career "Relied on" before Day 5 (backlog 12,
check fixed), events farouk-olu reading corner (FX24-2), arrows step6 sleep-by-day p5n:bed:22 (BM20-1, OP1 nights
day-arrow fix), controller day bunk ring (RB1 222ec28 check fix).

| Share | Seat | Checks |
|---|---|---|
| R1 | AS1 | player_check, bubble, puzzle, social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, arrows endstay |
| R2 | fresh | intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend, arrows endgo |
| R3 | DM2 | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, title_check, day_check 6, 8 |
| R5 | BM21 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories, promo_beats, day_check 12, 13, 16, 17, 18, 19, 27 |

Not in the gate: controller_check reach (BM21 runs it detached; non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).

perf_check is noisy on shared machines (0.96.0 bisect): a perf FAIL is re-measured alone twice before it counts.
