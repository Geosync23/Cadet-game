# Handover: CR1 (career and the first promotion, the 0.99.7 playtest patch)

**Role:** builder for lead 49 (session_01GKuymjjreuZtZeDMBX79xn); reviewer RV32 (session_01GKuymkDX3gviqiGJcKLWuS); build master BM25 (session_01GKuymnYTNkfxgLvtfFRg7w); JB3 (job places, session_01GKuymmiCEm3CMMrMTdWMEo) shares boardTopUp.
**Branch:** claude/p997-career, from claude/integration d7ad4c58 (0.99.6). Latest game commit: 93eb0e4, game sha256 310416c6...d261 (after the 0.99.7 round's fixes; BM26 merges it on top of 2e034d2). Lead now: lead 50 (session_01GKuymmoEriV3ugms2s3hsn); build master BM26 (session_01GKuymkyzjd6auLTCEZK5CN).
**Notes (plans/patch-0997.md on claude/lead-49):** 25, 48, 49, 55, 56. All built.

## What's built (24p's slot, "CR1 (lead 49 ...)" down to the end line)
Four switches, FALSE on the branch (the build master switches them on): `CR_DAY8_ON, INC_REDO_ON` (one var line), `CART_FIRST_ON`, `BOARD_NEW_ON`.
- **49 + 55 (CR_DAY8_ON):** the Tier 2 test from Day 8, the same afternoon as Making it safe (13:00-16:00) when it's learned by 12:30. PROMO.jobAt/until and t2's `day` and m6's `needs` are getters. crTestDay, crTestOpen, crReady, crCheckRows; PROMO_BEATS' morning words skipped that day. Robustness (RV32): crCatchUp (second lesson a day while behind, Days 2-7), crBigFirst (m6 first from Day 8), crCarryPark (a carried lesson waits), CR_M6_NEEDS (m6 needs Rounds only). Checklist: day row "Reached", never a false Done.
- **56 (INC_REDO_ON):** incRetake (15b ixBoard.doable), crLessonName (board words "Your Make it safe training job: take this one", only that job), crBoardArrow (level 2), CR_PUT (incidents you put back; not saved).
- **48 (CART_FIRST_ON):** cartFirstStops (garden crates: Cart bay dock first and last), cartFirstHold (15b ixHold), the 15b label words, IX_STOP entries; the crew skip the dock stops; 24d haul hold: no cart before the dock.
- **25 (BOARD_NEW_ON):** boardNewPost replaces FX19's boardTradePost call in boardTopUp; boardNewKinds (newest learned first, fresh = last 5 workdays); boardNewAdd(e) for other seats' kinds (JB3 decided not to use it: its jobs aren't ladder-taught). Defers to FX19 from Day 8 until the test is passed.
Words: content/works/career-0997.lines. Docs: design-doc (first promotion; job list sections; Open question on 25's mix), DEV_NOTES "The 0.99.7 career notes", build table rows p997-career, turn 2, turn 3; backlog CR1-1 (Tier 3/4 checklists' false Done), CR1-2 (tea corner round stop: JB3 fixed behind JB3_TEA_ON), CR1-3 (needs arrow over a lesson's meeting; TP1 has it).

## How to test
- `python3 cr1_check.py BUILD` (about a minute; parts check day8 slip catch redo cart mix; flips its own switches).
- The rest on a copy with the four var lines set true: career_check (follows CR_DAY8_ON), arrows_check promo + week, day_check 7/8/9, promo_sight, promo_beats, dev_arrow, intro_check (whole), interactions, food.
- Off proof: cadet_test 0.99.6 vs the branch file: ALL IDENTICAL.
- RV32's walker: plans/rv32-probes/fresh_walk.py on claude/review-rv32 (run from the repo; CADET_CHROME=/opt/pw-browsers/chromium).

## Gotchas
- Many checks in parallel on 4 cores give Page.goto 30 s timeouts: not the game. Run at most three at once; check_fast alone.
- career_check and promo_sight read the switch; on the branch (off) they check 0.99.6's timeline.

## The round's fixes (after RV32's PASS)
- crCarryPark checks Making it safe can open that day (mech_check #15). Dev mode's table and beats follow CR_DAY8_ON (DM_CAREER, devmodeCareerFor, DM_BEATS). crTestOpen without the playerShiftOn re-ask. mech_check, devmode_check, arrows_d_check follow the switches (lead 50: test the build as it ships; never switch CR_DAY8_ON off inside a check). CL1 shortened cr.ready and cr.ready.mail for lines_check's 90 characters (keep theirs).

## Loose ends / open for the user
- 25's mix amount (design-doc Open questions).

## For the next CR seat: lead 51's results-meeting bug (2026-11-10, not started by CR1: memory over the limit)
The user on 0.99.9: "the promotion/ test results/ meeting with calder for your results doesn't work. I skipped to it in dev mode ... I walk into Calder's office on time and nothing happens." Asked: reproduce on main bfbcbdf (normal play, and every Dev jump to the test/results day), fix behind CR9991_RESULTS_ON on claude/p9991-results (off = identical vs 0.99.9).
Unchecked first lead (same trap CR1 hit in the 0.99.7 round): Dev mode's landing day reads as excused, so `playerShiftOn(d)` is false for it. `promoSummonsDay()` (24p) picks the first day after the test where `playerShiftOn(d)`; if a Dev jump lands on the result day, that day may be skipped (summons booked a day later, or the booked occasion's day disagrees with promoPlan), so walking into the office at 08:15 meets nothing. Also check: the summons occasion (OCCASIONS.promoSummons, script promo.result with PROMO_BEATS_ON, at PB_TIMES.summonsAt 08:15) is booked at all after a Dev jump (promoSummonsTick books it at 06:00; a jump that lands after 06:00 without ticking that minute may miss the booking), and that DM_BEATS 'promo' (Day 9 with CR_DAY8_ON, at summonsAt - 10) lands with SHIP.occasions holding promoSummons for that day. Probe: tools like /tmp/cr1-ct/beatdbg.py (arrows_check's Page, devmodeRun + DM_BEATS) print SHIP.occasions, promoSummonsDay(), playerShiftOn(d) right after the jump; then walk the player into room 'o' on Deck 5 at 08:15 and watch DIALOGUE / r.met.
