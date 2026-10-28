# 0.96.0 full round: the five shares (lead 44, 2026-10-28)

Cap 5 (the user): BM20 + four runners. Candidate = claude/staging-pad tip that BM20 names (controller A+B+C, Diplomatic
visit on, sound update ON, PAD_ON true, SND_R3_ON true, build 0.96.0). OLD = 0.95.0, claude/integration b5199dc3.
Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM20 + lead at once). Notes in
plans/checks-0960-rN.md on your own branch claude/checks-0960-rN. Known old: backlog 12 (career "Relied on" before
Day 5), events_check farouk-olu reading corner (FX24-2), backlog 14 / perf one-off spikes (re-measure).
Note: sound_check now FAILs on OLD by design ("no SND_R3_ON line"); OLD runs don't apply to it.

| Share | Seat | Checks |
|---|---|---|
| R1 | AS1 | player_check, devmode, bubble, puzzle, social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, dev_arrow, day_check 4, 11 |
| R2 | fresh | intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend |
| R3 | fresh | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, day_check 6, 8 |
| R5 | BM20 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories, promo_beats, arrows endstay/endgo, day_check 12, 13, 16, 17, 18, 19, 27 |

Not in the gate: controller_check reach (BM20 runs it detached; non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).
