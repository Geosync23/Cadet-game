# 0.97.0 full round: the five shares (lead 44, 2026-10-28; Dev mode update J0-J5)

Cap 5 (the user): BM20 + four runners. Candidate = claude/staging-pad tip that BM20 names (0.96.0 + the Dev mode update
J0-J5 from claude/devmode-j2 86958252, build 0.97.0). OLD = 0.96.0, claude/integration fe11cd66.
Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM20 + lead at once). Notes in
plans/checks-0970-rN.md on your own branch claude/checks-0970-rN. Known old: backlog 12 (career "Relied on" before
Day 5), events_check farouk-olu reading corner (FX24-2), backlog 14 / perf one-off spikes (re-measure).
Known old adds: none new from 0.96.0.

| Share | Seat | Checks |
|---|---|---|
| R1 | AS1 | player_check, bubble, puzzle, social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, arrows endstay |
| R2 | fresh | intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend, arrows endgo |
| R3 | DM2 | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, day_check 6, 8 |
| R5 | BM20 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories, promo_beats, day_check 12, 13, 16, 17, 18, 19, 27 |

Not in the gate: controller_check reach (BM20 runs it detached; non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).

perf_check is noisy on shared machines (0.96.0 bisect): a perf FAIL is re-measured alone twice before it counts.
