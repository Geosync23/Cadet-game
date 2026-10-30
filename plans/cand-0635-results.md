# 0.63.5 candidate results (build master 8, session_01YGy9FDmcbkySMJpVPYJaAo)

Branch `claude/p5-cand-s5`, base 0.63.4 final `claude/p5-cand-s4` aa4f42c. Second runner CR2 (session_018xWmWkrtNWudZUgXygkW1u, notes claude/p5-cand-s4-checks plans/cand-0635-cr2.md). Reviewers R6, then R7. Every run with its own CADET_WORK.

## Pieces
- BM8 4e0c385 (check-only, R6 PASS): mech_check, two state leaks between parts. TPARTS' reset restores the part's starting works (W0) before machinesNew, so every run's machine catch-up reads the same works (run 1 read the fresh game's, later runs the last run's tier-2 works: teamPlan's week-2 pick scrubber vs washer). M12 never reset the machine clock, so its first run continued from the part before (a real 4-washer-3 job posted beside the staged one); now `MACH_HOUR = null; MACH_SEEN = -1` like every other part. X3 found the same independently (claude/x3-mechcheck-fix 0a3d86e, R6 PASS, not taken: same lines).
- X2/X3 `claude/crew-pt1` 79959ff (R6 PASS): X2's crew pieces 0.71.3-0.71.6 (game tip 6c26c72) + X3's interactions_check fix (the tap at the Deck 3 lamp stop hit Sol Bakshi standing in front of it; the check now taps crew-free floor within JOB_REACH).

## Trial s5a = 1e70683 (aa4f42c + 4e0c385 + 79959ff)
Merge clean (build lines auto), NAMES OK (3263), parses, verify_merge 0, bake unchanged (9565 lines / 48 meetings).
- BM8: cadet_test vs 0.63.3 + X2 6c26c72 alone (label 0.63.5) ALL IDENTICAL (X2's mornings change every shot vs 0.63.4, so compared against X2 alone); mech, career, machine OK; lines PASS (0 errors, 2 warnings); puzzle, social, interactions, day 0-3 OK.
- CR2: smoke, newgame, day 4-8, intro --week, device, food, clothes, deck, tiles, join, arc, path, disc, events, bubble OK.
- FAIL leave_check 'the Works crew don't use the clock' [2,1,2,1,2,2,1,2,2,1,1] (7 of 11 clock in and out; 3/4 wanted). Placed: 2bc08d5 + 6c26c72 alone fails identically; 0.63.4 passes. Cause (X3): clock-OUT at 17:00, all Deck 5 day crew at one clock with wait 6. → X3 0.71.7.
- FAIL player_check 'held booths' (expects 'In use…', gets 'Every booth is busy, so you join the line.': 0.71.4's queue) and 'job loop: carrying parts should show the crate (player.holding)'. Placing on 2bc08d5 + 6c26c72 alone. → X3 0.71.7.
- Follow-up tried and dropped: the same W0 restore in M8/M13/M14/M15/FC/FF's resets fails m8 ('a crew-only team job runs and puts the machines right'): those parts' expectations were tuned to the state they get today. Left as a known fragility (DEV_NOTES).

## Candidate ee9f9ed = 1e70683 + X3 claude/crew-pt1 6a4e153 (0.71.7, R7 PASS: the Works crew's 17:00 clock-out waits up to 20 minutes, was 6)
Merge clean, verify_merge 0, parses, NAMES OK, bake up to date. Re-runs of what it can touch (own CADET_WORK each):
- BM8: leave OK (was FAIL), cadet_test vs 0.63.3 + 6a4e153 alone ALL IDENTICAL, interactions OK, day 0-3 OK.
- CR2: day 4-8, events, food, deck OK (claude/p5-cand-s4-checks 43a2580).
- player_check's two FAILs placed: 0.63.3 + 6c26c72 alone fails the same two lines (X2's). X3: the booth line is the check's (it now accepts joining the line and leaves it after); the crate line likely the left-over queue too. Waiting on X3's hash.

## Final: ee9f9ed + X3 claude/crew-pt1 84fb217 (player_check only, R7 PASS; merged with git so only X3's two hunks came in, the base's 0.73.0 energy checks stay)
- X3: PLAYER CHECK OK on 1e70683 + 6a4e153 + 84fb217's player_check (same game file).
- BM8: player_check on the final (own CADET_WORK, TMO 2700): see the last line below.
