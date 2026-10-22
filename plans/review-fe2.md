# Review: fresh-eyes batch 2 (RV8)

Reviewer RV8 (session_01Q6uHYWus4ncyEgqWEYhJh5), for lead 29. Base for all: claude/arrows-c 6610dc7. Probes in
plans/review-rv8/ (run: `python3 p_x.py GAME.html DIR_WITH_cadet_test.py OUT`).

## CP4: claude/fe2-tracked 251d9788 (items 24 and 41): PASS

What changed: section 15b's Tracked only (trkItems marks `later`, trkFollowKey, TRK_SAID / trkSaid, trkTap, the panel's
and the device app's rows), interactions_check's new part, a build-table row. Nothing else.

- **24, a row for tomorrow.** Real taps at 390x844, Day 2 18:00: tapping "Breakfast, Tomorrow" in the Tracked panel sets
  no arrow, the panel stays open and the row reads "Tomorrow · the mess, Deck 3 · That's tomorrow: track it on the day".
  The same tap in the device app: no arrow, the device stays open, same words. On the base the same tap set an arrow to
  the mess hall for now and closed the panel. Today's rows still set their arrow.
- **41, the row the arrow follows.** With the round's arrow put up the way the round guide does (no Tracked tap), the
  job board row is lit with "ARROW" in the panel and "The arrow points here" in the device app; a tracked row still says
  "Tracking". No arrow: nothing lit.
- interactions_check: OK on the tip; on 6610dc7 with the tip's check, exactly the three new lines FAIL.
- check_fast on the tip: QUICK CHECK OK (161 s).
- cadet_test strictly alone, 6610dc7 vs tip: ALL IDENTICAL, no errors.
- Word note (not blocking, writer's call): "Tomorrow · ... · That's tomorrow: track it on the day" says tomorrow twice;
  "track it on the day" alone after the existing "Tomorrow ·" would do.

## DS1: claude/fe2-player 88df5899 (game commit 418ff167; item 27): PASS

What changed: one line in section 15's actBegin (the description is left out when the words already hold it),
player_check's new lines, a build-table row. Nothing else.

- Real screen tap on Deck 3's Long table at 390x844, Day 2 18:05, no tray (p_seat.py): the card reads "Seats eight. The
  engineers take this one ... You sit down. To eat, queue at the servery ..." once; card 694-826 px of 844, inside the
  screen. On 6610dc7 the description was there twice (card 672-826).
- player_check: OK on the tip; on 6610dc7 with the tip's check, exactly "the table's words should show once" FAILS.
- check_fast on the tip: QUICK CHECK OK (148 s). cadet_test strictly alone vs 6610dc7: ALL IDENTICAL, no errors.
- Note (not blocking): player_check runs at 900x760, so its "card fits the screen" line is not the phone size the user
  asked about; my phone-size tap above covers it for this review. The card fitted on the base too (bottom 826 of 844);
  the change makes it 22 px shorter. #25 (showering outside the cubicle) was not changed (DS1: not a bug, lead 29's call).

## FX2: claude/p5-fix2 421838e4 (commits d59e8e9f, 493b84ea, 421838e4; items 29 and 40): FIXES NEEDED (item 29)

Reviewed against 31477c3c (FX2's merge of arrows-c 6610dc7, whose other parent already holds integration 0.64.16 and
FX2's earlier Day 0 tray fix 191d1853). So the branch brings 0.64.16 and 191d1853 along as well as batch 2: the build
master should know. What batch 2 changed: section 15b's ixTap / ixTeaAnywhere / BUSY_TILE (tea), the intro's arrow
lines (introArrowClear, introArrowTick, introTick), intro_check part 13b, player_check's tea part, the build table.

- **40, tea (PASS).** Day 1 tea with Zeke, 390x844, real screen taps (p_tea.py). With every Tea corner place taken: a tap
  on the Armchair or the Tea table gives "Tea and biscuits" standing in the corner (tea day set); on 31477c3c the
  Armchair said "In use" and the table did nothing. With a seat free: the same on both (you sit in it).
  player_check: OK on the tip; on 31477c3c with the tip's check, exactly the tea line FAILS (the three-taken case; with
  two taken the base already gave tea at the standing spot).
- **29, the Clock in arrow (FIXES NEEDED).** The fix holds while you stand at the Deck 5 lift (intro_check 13b: OK on
  the tip, FAILS on 31477c3c), but a real walk does not: Day 1 08:30, Tracked "Clock in" tapped on Deck 4, ride to Deck
  5, walk from the lift towards the clock (p_clock4.py). As you step from the lift lobby (room '@') into the Works bay,
  15b's trkDoneCheck counts you as arrived (any tile in the clock's room) and takes the arrow down, 5.6 m from the clock
  and not clocked in; Zeke's arrow takes over at once (08:35 "clear clock:in <- trkDone < trkDoneCheck"). It came back
  only at 08:50 as the intro's own first-time "Clock in" arrow. So from the player's side it still switches itself off
  on Deck 5. Suggested: trkDoneCheck leaves a 'clock:' goal alone (15's clock reminder already takes it down once you
  punch), and 13b walks into the bay (not just goToDeck) and then punches with a tap on the clock.
- check_fast on the tip: QUICK CHECK OK (149 s).
- cadet_test strictly alone, 31477c3c vs tip: run 1 and 2 "ALL IDENTICAL apart from renderer noise" (6-46 px, max 1 level,
  every shot), run 3 ALL IDENTICAL (0 px). Base vs a padded copy of base: 0. Tea hunks alone: 0. Intro hunks alone: one
  run with a_start's speech bubble a few px to the side (14812 px), two reruns 0. So: noise, nothing from the change.
- Side note (both builds, not FX2's): my skip to Day 1 08:30 leaves the intro on step 'bunk', and at 08:55 a "Put your
  bag in your wardrobe" arrow shows though the bag is stowed. Likely my probe's skip; not filed.

## FX3: claude/p5-fix3 3b7b13db (fix 15; items 33, 38 and the Cart dock 1 stop): PASS WITH FIXES (the check only)

Reviewed against its parent 2cdc1dfc. Not on arrows-c 6610dc7: the branch is integration b9f053ba + FX3's fixes 10-14
+ fix 15, so it brings fixes 10-14 along (the build master should know). What fix 15 changed: 15b's ixJobStep (the lathe),
new ixPinTap, one line in 15's playerFloorTap, the dock clause in 15's choreRayTap, an interactions_check part, the
build table.

- **33, the pin on the machine you need.** "Make a bracket at the lathe" with the pin on the lathe (was "... in the
  machine shop", the room's middle). At 390x844 with the crew on, a real tap at the pin made the part from three of four
  camera turns; on the fourth, Chief Calder and two crew stood in front of the lathe and the tap opened her card (a person
  in front takes the tap, as FX3 says; the same on 2cdc1dfc). Note: MAKE_AT's first place (5-make-1) is always the one
  pointed at, even when someone is using it and 5-make-2 is free.
- **38, the job board pin.** "Turn it in at the job board": at 900x760 (FX3's check) a tap at the pin opens the board
  from all four turns (on 2cdc1dfc only one of four). At 390x844 from where the check stands you, two turns have the
  board off screen (only the edge arrow), so there's no pin to tap; the two on screen open it. Not a regression.
- **Cart dock 1.** Standing in the Cart bay (room 'm'), a real click on Cart dock 1 does the cart stop from every turn
  ("Done here. 7 stops to go"); on 2cdc1dfc three of four turns gave the dock's machine card instead (p_dock2.py).
- **Check (the fix needed):** the new part's Cart dock line passes on 2cdc1dfc too, so it doesn't prove the dock
  change: it stands you 1.5 m from the dock's spot, which is in the machine shop on the other side of the wall, and calls
  playerTap with the last click's ray instead of clicking the dock. Suggested: stand in the Cart bay and click the dock
  on screen (as p_dock2.py does); that fails on 2cdc1dfc. The lathe and board lines do fail on 2cdc1dfc (lathe 3 of 4,
  board 3 of 4).
- interactions_check OK on the tip; check_fast QUICK CHECK OK (151 s); cadet_test strictly alone vs 2cdc1dfc ALL
  IDENTICAL.

## Second round

- **FX2 ffdbb8c (trkDoneCheck leaves a 'clock:' goal alone): PASS.** p_clock4.py: the tracked Clock in arrow stays
  on the clock from Deck 4, across the Works bay and through Calder's briefing to 09:16. 13b FAILS on 421838e (Zeke's
  arrow from the bay) and passes on ffdbb8c. check_fast OK. cadet_test alone 421838e vs ffdbb8c ALL IDENTICAL.
- **DS1 1dd4f560 (check only):** player_check also measures the card at 390x844. Fine.
- **CP4 f59b471e (item 38: the pin at the item's middle, a tap on the pin is the item's tap): PASS, one note.**
  Its check part FAILS on 251d9788 and passes on f59b471e. check_fast OK. cadet_test alone 251d9788 vs f59b471e
  ALL IDENTICAL. Tested with FX3 3b7b13d as lead 29 asked (scratch build: FX3's file plus CP4's 38 change; applies
  cleanly, names_check OK). p_board.py: a real click on the pin opens the board from every turn where it's on screen
  (900x760 crew hidden: 4 of 4, icon and anchor; 390x844 crew on: 2 of 2 on screen, the other two turns show only the
  edge arrow). FX3's interactions_check on the combined build: OK in 2 of 3 full runs. In the first run, turn 1's click
  on the pin neither opened the board nor fell through (the pin still under the point afterwards). It didn't happen
  again in eight more runs (2 full, 6 of FX3's part alone), so it's 1 in 9 and I couldn't reproduce it. Note for CP4: if it shows up again, the
  pin acts on 'click' after stopping 'pointerdown'; if the pin moves between press and release no click comes, and
  the press was already swallowed.

## Third round

- **CP4 016fc65e (the pin acts on release, as a deck tap does): PASS.** On FB1 228de58 + CP4's 38 change (scratch build,
  applies cleanly, names_check OK), p_board2.py, 10 press-3-frames-release taps per camera turn, three runs at once:
  900x760 crew hidden 40/40 twice, 390x844 crew on 20/20 (the other two turns have the board off screen). check_fast OK;
  cadet_test alone f59b471e vs 016fc65e ALL IDENTICAL. Note: like a deck tap, the release must come within HOLD_MS
  (240 ms, real time) of the press; a check that holds the press over many rendered frames on a slow runner could miss.
  **The earlier 1-in-9 miss** (on the click version): not reproduced in 12 more runs, 3 of them with every pointer event
  and ixGoalTap logged (each showed down, up, click, ixGoalTap, playerTap true, the board open). In the test harness the
  pin can't move between press and release (animations off, frames stepped by hand), so bobbing doesn't explain that
  miss; its cause stays unknown. The click path it went through is gone in 016fc65e.
- **FB1 claude/fe-cartdock 228de58 (a52aad0 + 228de58, on FX3 3b7b13d): PASS.** choreThingTap: carrying for a haul or a
  delivery, anything within 1.5 m of the next stop does the stop; other registered kinds only a machine. jobTap's no-job
  stow goes to the nearest main-storage spot. FB1's three parts with real taps: OK on 228de58; on 3b7b13d the stops part
  FAILS (24 taps: Washer 1 started a load at the linen drop, the store's drop pin started the gym weights, Cart dock 2
  did nothing); on a52aad0 only the put-back part FAILS (4 turns). check_fast OK; cadet_test alone 3b7b13d vs 228de58
  ALL IDENTICAL. Note: "anything in reach" would also take a lift panel or a door within 1.5 m of a stop; FB1 measured
  none today (the docks, Folding table, Laundry drop sign, the Till). 776c4ff not pushed yet when this was written.
