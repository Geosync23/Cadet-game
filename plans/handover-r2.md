# Handover: R2 (check runner), as of 2026-11-11

- Role: R2, one of six check runners in the full round. Reports to the build master (BM28, session_01GKuymjydss9RxzDw1ftdPf) and lead 51 (session_01GKuymjp49y3M5hgRLecobm). Other runners' ids are in TEAM.md.
- State: 0.99.91 published 2026-11-11 about 14:49 UTC (main = claude/integration = cdd9efd). Nothing running. Stood down by BM28.
- Branches (notes only, never the game): claude/checks-0996-r2, -0997-r2, -0998-r2, -0999-r2, -09991-r2 (holds plans/checks-09991-r2.md, plans/checks-09991b-r2.md and this note).

## My share (round 0999 / 09991 plans)
cadet_test OLD NEW (alone, first), then two lanes at once (two browsers at most):
- Lane 1: intro_check (whole, about 55 to 60 min), --dinner, --firsts, path_check, arc_check, lines_check, lines_check --day.
- Lane 2: day_check 0, 1, 5, 7, 21, 22; arrows_check endgo; plans/rv31-probes/pf_f1_same.py OLD NEW 10; pf_f1_same 0.99.6 vs an all-switches-off copy of NEW.
- fresh_walk, p926 and perf_check were handed to R4 for 09991 and 09991b.
About 75 minutes in all.

## Gotchas
- pf_f1_same OLD vs NEW prints FAILED whenever OLD lacks NEW's switches (fingerprints differ by design). The pass is: F1 mismatches 0, no page errors, and the all-off proof (0.99.6 vs NEW with every new switch false) gives 30 same. BM26/BM28 agreed this.
- The all-off copy: a small script turns each switch line `NAME = true` to false (asserting each was found). Switches as of 0.99.91: CAL997_ON, TP997_ON, TRAD997_ON, GAMES997_ON, EV997_LIGHT/SAT/READ_ON, MV_BRIEF/WASD/FIT/RIG/RECWC/SOFA_ON, JB3_SHELF/SCI/REC/TEA/FOOD_ON, CH_SOLE/POSE/RELAY/HAIR/SEAT_ON, CR_DAY8_ON, INC_REDO_ON, CART_FIRST_ON, BOARD_NEW_ON, P997_SOCIAL_ON, SND_DISC, SND_LIVE, REC_FILM, TP998_ARROW_ON, TP998_BOOTH_ON, EV999_BLINK_ON, TP9991_SD_ON, EV9991_SIM_ON, TB9991_DRILL_ON, CR9991_RESULTS_ON, MC9991_REW_ON. Add each new round's switches.
- lines_check reads words files from its own checkout: run OLD in its own worktree, or it gives false errors.
- cadet_test "apart from renderer noise" (a few px max 1) is a pass.
- The container restarts at times; /tmp survives. Start long runs with setsid nohup, and never kill a lane mid-check (use skip files instead), or exit codes are lost.
- perf_check runs alone; one-off frame spikes: re-measure alone twice (backlog 32).
- Set CADET_CHROME=/opt/pw-browsers/chromium and a CADET_WORK folder per lane (three r128 via npm pack, acorn).

## Open questions for the user
None.
