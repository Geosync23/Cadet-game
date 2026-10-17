# Handover: adversarial reviewer 1c

- **Role:** adversarial reviewer for Pillar 4, added to share reviewer 1b's queue (session_018XY1NbMBxo2SLDPxooe5yx). Report to the lead (session_01KPJMYjXAPkNUcrQ8VRkhLE) with send_message; send each verdict to build master 2 (session_01F8ph7FKqViF3heRn94YgBr) too, and fixes to the owning seat (ids in TEAM.md on claude/lead-pillar1). Never contact the user. Never change game code.
- **Since 14:00 (the user's cost call): the only reviewer.** Review in depth only changes that alter game behaviour or saves; wording, content-only and test-only changes get a quick skim (does it break a check?) or none.
- **Branch:** `claude/reviews-3`, notes only, under `plans/reviews/`. Style: verdict PASS / PASS WITH FIXES / FAIL, a severity per finding, a concrete fix, proven on a merge where it matters (1b's notes on claude/reviews are the model).

## Done (2026-10-17)
| Item | Note | Verdict |
| --- | --- | --- |
| Roster claude/deck-plans-1-2-6 d53cf40 (0.16.15 kin/lost/hobbyNoun) | roster-d53cf40.md | PASS WITH FIXES: talent-theme hobbyNoun for quist-ilse, jovanovic-petra, juarez-nell |
| Arrival claude/arrival 0ea5048 (0.42.20-21 tour, dinner, bed arrow) | arrival-0ea5048.md (+ arrival-0ea5048-tour_probe.py) | PASS WITH FIXES: HIGH, a follower hears 19/61 tour lines (overlapping places, out of order, pacing); MEDIUM, leftover lines over the dinner and the Chief |
| Player claude/player-needs 4776216 (0.28.29-0.28.35) | player-4776216.md | PASS WITH FIXES: MEDIUM, joining the line at tap time stalls the counter; lows on the tray, lie-to-sleep, the strip |
| Player 7959655 (0.28.36-0.28.37) | player-7959655.md | PASS: joins on arrival (probe), reviewer 1b's four fixes in; lows on the tray, null dish and strip still open |
| Roster d53cf40..cadfbdd (0.16.16-0.16.20) | roster-cadfbdd.md | PASS: talent crafts fixed; Kovac's lift and breakfast lows sent to the lead |
| Roster 1348dfd (0.16.21) | roster-1348dfd.md | PASS: Kovac's two lines reworded |
| Player 9c18045 (0.28.38-0.28.40) | player-9c18045.md | PASS: lows fixed, the real-line and someone-in-the-way cases pass |
| Social A a033f17..752d964 (0.36.79-0.36.81) + c345a96 (0.36.82) | social-752d964.md | PASS: the truncated-aff low fixed in 0.36.82 |
| Sim 13a6fe9 (0.26.38 farewell friends) | sim-13a6fe9.md | PASS: day_check 161/35 OK, no doubles |
| Sim 7ca2249 (0.26.39 arrival-dinner seats held) | sim-7ca2249.md | PASS on the 0.60.3 combine: you 3-mess-10, Torres 12, Calder 9; intro_check, day_check 0 OK |
| Arrival 7cca991 (0.42.22-0.42.24, for 0.60.4) | arrival-7cca991.md | PASS: Tern start, ramp, tap-to-ask; low: the pilot on setTimeout |
| Arrival claude/arrival-0603 046a019 (0.42.21b, for 0.60.3) | arrival-0603-046a019.md | PASS: 27/27 core tour lines in order; reviewer 1's three fixes. Test on arrival-0603 + sim + content 910e88e baked with content_gen (archive content/ + content_gen.py, run it on the merged html) |

**Open loose ends:**
- Arrival is mine now (the lead's split); onboarding engineer 2 is session_0163dcLt17oTCdR8po9HRo2p. Reviewer 1's remaining arrival lows (health kind, missed health check, seek-ask Mail fallback, standing at Dinner with Torres, double health booking) will come later on claude/arrival (0.42.23+).
- **Galley 40166d6 + sim bfcd864 fail player_check's job loop (5) and food_check (4) together**, with or without the player branch; each alone is OK. Reported to the lead, the build master, galley engineer 3 and sim engineer 4.
- **Combine check for 0.60.3** (combine-0603-jobloop-food.md, merge: galley 7282327 + sim 236810f + f16a110 cherry-picked + player 9c18045): the job loop and food_check's old 4 are fixed. Two new: player_check's "squeeze past" (sim 0.26.36 unblocks shared tiles always, so you walk through the chef; sent to sim engineer 4), and food_check's "galleyJoin / galleyTurn" (a test assumption since sim 0.26.34; sent to galley engineer 3). **Rechecked with sim 0.26.37 (e4d6ace):** player_check OK (squeeze past back). food_check's galleyJoin case passes with a0e5b2f's check; that check needs galley 0.29.35 (7464b97) code, so the two go together in 0.60.3.
- **I now hold reviewer 1b's queue too** (sim, galley, social A/B, arrival, player, roster). Their final note: plans/handover-reviewer-1.md on claude/reviews (5394712). Its open items:
  1. The arrival-dinner seat: FIXED by sim 0.26.39 (sim-7ca2249.md); it was **reproduced on the 0.60.3 combine** (lemaire-nils in Torres's 3-mess-12, Torres takes your 3-mess-10, you get 3-mess-8; arrival-0603-046a019.md addendum). Should-fix sent to sim engineer 5 (hold the 3 seats on Day 0) and onboarding 2 (assert your seat).
  2. A 2-day jump sends 4 section-17 notes that hour-by-hour doesn't (social_check --long); the sim seat owns it.
  3. Social save rule: <= 30 KB every day to 140, < 40 KB to 280, measured daily from the arrival.
  4. Sim lows: crewMakeWay lists per frame; the step-aside spot can be another station's tile; the breakfast tray return makes crew late to the lift; a crewHold in the line blocks the counter.
  5. Social B lows: no test of v:2 from an arrival start or STORY_CAP 0; an untagged pre-0.39.22 snapshot with a reordered roster.
  6. linesFill could add {home} {family} {hobby} {since}; events_check day 231 double on 4e72597; section 18 New-game reset.
- **Sessions now:** sim engineer 5 session_01Do3HU5Rh96tgUsPTUbsF8a (sim 4 and player 4 are inactive); onboarding 2 session_0163dcLt17oTCdR8po9HRo2p; social A session_012pK2XVi5UhqEd28fakYk68; galley 3 session_018cicfPQZQXbxmtn6ygmL84; crew designer 3 session_01TDCn9auvCBML52hyjWGY6x.
- **Tools from 1b:** name_check.py on claude/reviews (`--branches OLD NEW` on re-reviews). Give each parallel browser job its own CADET_WORK.

## How I test (fresh container)
- `pip install playwright`; three r128 unpacked at /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- Merge the way the build master does: start from a branch that already carries the latest ship-integration (e.g. galley), merge the others in, resolve build lines by keeping either.
- **Gotchas:**
  - Run one browser test at a time: two at once made page loads time out (60 s).
  - Never wait with `pgrep -f "<pattern>"` in a loop: it matches its own command line and never ends. Use `pgrep -f "[p]attern"`.
  - In a probe that `exec`s cadet_test.py, don't name anything `HOOK` (it replaces cadet_test's own, and the game never starts).
  - player_check skips its real-line test when `lineSpot` exists, so walk the real line with a probe on a combined build.
- Probes live in the scratchpad; the tour one is saved next to its note.
