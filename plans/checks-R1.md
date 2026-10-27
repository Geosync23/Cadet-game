# R1 checks: 0.94.0 full round

- Commit: `9faaee80` (claude/staging-0.94.0)
- Game sha256: `04cc0cb65f2272c8f7afbeb438b94d972d80a8f59d42580515b86a1a380e0dbf` (matches)
- OLD: 19400976 (0.93.3), sha256 `ec93b94d...d085` (matches); not needed, no game FAIL
- Share: old CR1 + old CR4. Two lanes, each with its own CADET_WORK (/tmp/work-R1, /tmp/work-R1b), never more than two browsers at once.

| Check | Result | Key lines |
|---|---|---|
| player_check | PASS (rc 0, 558 s) | `PLAYER CHECK OK` |
| devmode_check | PASS (rc 0, 368 s) | `DEVMODE CHECK OK` |
| bubble_check | PASS (rc 0, 659 s) | `BUBBLE CHECK OK` |
| puzzle_check (build as is) | FAIL in the check, not the game (rc 1, 73 s) | `FAIL switch off: nothing of Step 5's registered: {... 'on': True}`; p4/p5/p9/board `not yet (no P5_STEP5 switch line in this build)` |
| puzzle_check (copy, P5_STEP5 line put back to off) | PASS (rc 0) | p4 550 fits / 385 cases; p5 355 fits / 102 cases; p9 and board ran; `PUZZLE CHECK OK` |
| social_check | PASS (rc 0, 31 s) | `SOCIAL CHECK OK` |
| talk_check | PASS (rc 0, 48 s) | `TALK CHECK OK` |
| arrows_pointer_check | PASS (rc 0, 177 s) | `arrows_pointer_check: OK` |
| dev_arrow_check | PASS (rc 0, 92 s) | `DEV ARROW CHECK OK` |
| day_check 4 | PASS (rc 0, 426 s) | `DAY CHECK OK` |
| day_check 11 | PASS (rc 0, 445 s) | `DAY CHECK OK` |
| day_check 6 | PASS (rc 0, 450 s) | `DAY CHECK OK` |
| day_check 8 | PASS (rc 0, 453 s) | `DAY CHECK OK` |
| day_check 12 | PASS (rc 0, 449 s) | `DAY CHECK OK` |
| day_check 13 | PASS (rc 0, 454 s) | `DAY CHECK OK` |
| appt_check | PASS (rc 0, 952 s) | `APPT CHECK OK` (its 4 FAIL lines are the planted self-test, each followed by "its part fails" ok) |
| saves_check | PASS (rc 0, 157 s) | `SAVES CHECK OK` |

## The puzzle_check FAIL, with proof

puzzle_check.py (line 764) expects the build to be off, looking for the line
`const P5_STEP5 = URL_FLAGS.has('p5s5');`. 0.94.0 switches Step 5 on (`const P5_STEP5 = true;`, game line 9471),
so its "switch off" test sees Step 5 on (`'on': True`), and it finds no off line to swap, so the Step 5 parts
(p4, p5, p9, board) never run. The game is fine; the check was written for a build with the switch off.
I made a copy with that one line put back to the off form and ran it: `PUZZLE CHECK OK`, with the off test and all
four Step 5 parts run. BM19 agreed and fixed puzzle_check.py on staging-0.94.0 (when the build is on, it makes its
own off copy), and confirmed the copy's result stands for this round.

## Extra checks taken on (asked by lead 41, BM19, R2 and R3)

These use the check files from staging f4914555 (test-only fixes; game unchanged, sha256 04cc0cb6...0dbf).

| Check | Result | Key lines |
|---|---|---|
| controller_check walk (run alone, lead 41) | PASS (rc 0, 127 s) | all 4 views walked four directions, with no #rot timeout; `CONTROLLER CHECK OK` |
| cadet_test OLD (0.93.3) vs BUILD (run alone, from R2) | PASS (rc 0, 55 s) | `ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)`; only j_steer1 6 px max 1; errors A [] B [] |
| saves_check (f4914555) | PASS (rc 0, 206 s) | shut and promo3 really ran (Day 18 before/after 22:00; promo3 to tier 3 senior); `SAVES CHECK OK` |
| ending_check (f4914555, from R3) | PASS (rc 0, 143 s) | `ENDING CHECK OK`, 0 FAIL |
| arrows_check endgo asis (from BM19) | PASS (rc 0, 249 s) | Days 31-36, settled go Day 35, oath; `ARROWS CHECK OK` |
| arrows_check endgo teachoff | PASS (rc 0, 255 s) | settled go Day 35; `ARROWS CHECK OK` |
| arrows_check endgo track | PASS (rc 0, 185 s) | settled go Day 35; `ARROWS CHECK OK` |
| arrows_check endgo change | n/a by design | the check skips change for go (line 764: "the change of mind ends in the endgame: endstay's"); 1 s, nothing run |

Result: R1 OK.
