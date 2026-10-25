# RV12 review notes

Reviewer RV12 (session_013JmdoWWEDQde8y1bwrMGnY), branch claude/review-rv12 (notes only), under lead 32.

## FX6 tray-seat arrow (LEAD31-14, 0.92.2), on claude/mess-taps (base FX7 980c2591)
- Status: waiting for FX6's sha (~21:45 UTC). Baseline interactions_check and arrows_check week running on 980c2591.
- Known so far: the hunger arrow comes from needGoal('hunger') (NEED_FIX hunger: servery-queue, grab-shelf); it is
  cleared only when an act with def.need hunger starts (eat) or Food is back over WARN_REARM, so after the queue hands
  you a tray it still points at the servery.

## FX8 day0-sim claude/fx8-day0-sim 87e3174a (on 54efee21): PASS (2026-10-23 ~22:00 UTC)
Game sha256 69d845c6...; base 54efee21 2dbb11b8.... Handed over from RV10 (its runs counted, not repeated).
- Diff: section 14 only (tradLeave reads DAY0_LEAVE; tradMeal cuts the table seat at it, kept; day0Trickle re-plans each
  diner alone against everyone else's bookings, keeps the old plan up to the stand-up minute, appends the new plan's
  steps after the table, restores bookings old-before/new-after; falls back to the old plan if the re-plan doesn't stand
  them within 2 min). events_check 1a two lines; design-doc Meal traditions; build-table row. Does what it says.
- RV10 (its container): events_check 54efee21 FAILS the new filler line at 18:20 and 19:10 (volkov-maeve bed, ...);
  87e3174a OK; day_check 0 OK; check_fast OK; cadet_test 54efee21 vs 87e3174a ALL IDENTICAL. Its paper probe: others
  changed none, no diner changed before standing, no gaps, same twice, first steps after the table gym/lounge/call
  home/shop/garden/bench/lift/toilet, stand-up 2-48 min after.
- RV12 live look (RV10's trickle_live.py, goodnight 18:40 on Deck 3, 72 on deck): the non-diners who change goal
  18:40-18:45 are the same people to the same places on both builds (pell, navarro-mateo, zamora-quinn, esposito-yara,
  salo-saad); only diners differ: old to @lift (bunk), new to gym-14, lounge-4, bench-18, gym-5, callhome-1, lift-1.
- intro_check --evening: OK on both; logs identical (goodnight at the same minute) except the overheard chatter after
  19:50, which follows from the diners' new evenings.
- Planted fault (p1: the kept table seat starts a minute later after the splice): events_check 2 FAILs "changed diners'
  plans before it" at 18:20 and 19:10. The filler line is proven by the old build (RV10).
- Cost: Day 0 rebuild timed from Python (time_probe2.py), 3x5 rebuilds: 65-240 ms new vs 66-308 ms old, plain or with
  a goodnight; the 42 extra planner runs are lost in the noise of a busy 4-core box. It rebuilds once, at the goodnight.
- Notes (not blocking): the re-plan's steps before the table can differ from the old plan (others booked first); only
  the steps after are used, as designed. DAY0_LEAVE is a top-level const read inside schedBuild; no planner run comes
  before its line at load (all checks load clean).

## FX6 tray-seat claude/tray-seat f90140bb (LEAD31-14) + FX7 mess-taps 9c4e02b5 (test only): PASS (~23:00 UTC)
Game sha256 b7b7b6e4... (only b7a8a22e changes the game; ed1ee8d7 reverted by 1d4e0dac; 62deb7b3 merges mess-taps
9c4e02b5; f90140bb test only). Base: mess-taps 980c2591 game 9d0119cd....
- Diff: section 15 only. needGoal('hunger') with a tray on Deck 3 -> nearest mess-seat not heldBy (else nearest),
  label "A seat for your tray", NEED_GOAL.tray; needGoalTick re-aims when the tray comes or goes; sitting to eat clears
  it as before (actBegin). Trays are dropped every frame off Deck 3 (playerUpdate), so the re-aim can't churn. design-doc
  Small comforts. Does what it says.
- 9c4e02b5 / f90140bb (test only): the counter taps recheck "on the counter, someone near, not on them" before each
  click; part (3)'s seat tap waits (up to 20x15 frames) for the seat to be on screen and clear; if it never is, no tap
  and part (3)'s second line FAILs (never a silent pass).
- interactions_check (full, game b7b7b6e4): OK. Mess part alone with f90140bb's code (plans copy of lines 1-56 + the
  LEAD31-9 block): fix OK (counter 8/8); 980c2591 game FAILs both new lines (arrow stays "Food", here on 3-grab-1);
  planted f1 (no re-aim in needGoalTick) FAILs both; f2 (right label, points at a servery-queue) FAILs both; f3
  (counter fix in tap() removed) FAILs the counter line, 9 tried 0 joined; 54efee21 (before FX7's fix) FAILs all of
  LEAD31-9's lines, counter 0/8. Same results earlier with b7a8a22e's and ed1ee8d7's test code.
- arrows_check week: OK on the fix; FAILs on 980c2591's game with the same check ("stuck from Day 9 16:50 at Food").
- cadet_test 980c2591 vs fix: ALL IDENTICAL (one run; FX6's one-off bubble offset not seen; FX6 reports the same wobble
  comparing mess-taps with itself under load, so renderer timing, not this change).
- check_fast: QUICK CHECK OK in 401 s.
- Notes (not blocking): without the fix the tray arrow could even point at a grab shelf, and a tap there eats a snack
  with the tray still in hand (seen on 980c2591); the fix removes that path. The seat pick reads live heldBy only, so
  it can point at a seat kept for a tradition; tapping it moves you to a free one nearby (actBegin), so harmless.
- Counter-tap fragility (lead's ask, with RV10): with the recheck the counter part was 8/8 or 9/9 in every run here
  (8 runs), and the planted counter fault is still caught; the earlier 1-of-9 miss was the point going stale, not the fix.

## FX9 needs-pace claude/p923-fx9 fb3a5d1a (0.92.3 items 3, 4, 5, 18): PASS (~05:35 UTC 2026-10-24)
Game commit 0e9243f9, sha256 fd28b42c...d5a4 (fb3a5d1a and de1e97e9 test/docs only); base 0.92.2 364c80cb ca2f908d....
- Diff: section 15 constants only: NEED_DRAIN fitness [1.4,.35], social [4.5,.5], leisure [2.4,0], hunger asleep 6;
  WORK_LEISURE 3; t:gym words "most days"; design-doc and tips-plan. Crew needs untouched. The design-doc sums check
  (fitness 25.2 a day, social 76, leisure 38.4 a day off / 62 a shift day, hunger 48 a night).
- Finding (fixed in fb3a5d1a): no check failed on the old rates (the normal paper week was re-planned to pass, the
  neglect week passes on both). FX9 added four paper lines: on 364c80cb all four FAIL (fitness 12, social 50, leisure
  12.8, hunger 16), on fb3a5d1a PLAYER CHECK OK (25.2, 76, 38.4, 48). The base run doubles as the planted fault.
- player_check OK; arrows_check (all parts) OK; devmode_check OK; intro_check (whole) OK.
- cadet_test vs 364c80cb: a_start..i_tap0 identical; i_tap1..j_steer2 (7 shots, not only i_tap1 as reported) differ
  by the firm warning/marker ("Missing people"/call booths instead of "Bursting"). A copy with only social reverted to
  [3,.25] is ALL IDENTICAL, so every difference is the social rate, as intended.
- check_fast: FX9's OK (not rerun here: the game change is constants only; the full round runs it).
- Note for the lead/user (design, not a defect): a "normal" day now needs the gym, a call home and three chats daily
  to stay above 30 on paper; a 0.92.2-style day (gym or call on alternate days) runs social and fitness low.

## AC3 arrows-c aee83840 (0.92.3 item 6, the clock-in tip + Clock in tracked, Days 1-3): PASS (~06:45 UTC)
Game sha256 9262e4a7...; base 364c80cb. (Items 16 and 26 were reverted in this branch: net nothing.)
- Diff: section 15b slot (clockFirstTick, tipFront, clockFirstDrop) + one call in guideTick (GUIDE_ON true since
  0.92.0). Days 1-3, first time in the Works bay from 08:00 before clocking in: Clock in tracked (not with Teaching
  arrows Off), the tip to the front; Day 1 waits for Zeke's opener or 09:15; stale clock-in tips dropped; the arrow goes
  the frame you punch in.
- Findings, both fixed in aee83840: (1) no check lines at first; AC3 added arrows_check part clockin (in the default
  parts); (2) the career's one-off bay tip held back only on Day 1 (a missed Day 1 could double it on Day 2): now any day.
- clockin part: OK on the fix; on 364c80cb 4 of 5 lines FAIL (there the career tip queues behind the "walk" tip, the
  user's complaint). Planted faults all caught: h1 no clockFirstTick call (4 FAIL), h2 no instant arrow clear (the
  clocked-in line), h3 no Day 1 wait for Zeke (the Day 1 line), h4 arrow despite Teaching arrows Off (the Day 3 line).
- cadet_test vs 364c80cb ALL IDENTICAL; intro_check (whole) OK; check_fast OK (350 s).
- AC3 reports arrows_check week guide FAILs m6 the same on 364c80cb (pre-existing in 0.92.2); not rerun here.

## FX12 claude/p923-fx12 da1825d2 (0.92.3 items 19 and 27, trays): PASS (~08:05 UTC)
Game sha256 44a5cc8e...; 123a778d's game (d643c0da...) plus one toast string ("over to the mess hall").
- Item 19: on 0.92.2 every mid-meal get-up path already kept the tray (actEnd(true) is the only way out mid-meal;
  'out' comes only when done); it vanished off Deck 3 (playerUpdate, silent) and wasn't drawn on the way to another
  activity. Fix: TRAY_TRAVELS = true (section 15), the tray drawn while walking/waiting with one, the hunger arrow's
  seat on any deck (off Deck 3: any public sit place) and re-aimed on a deck change.
- Item 27: section 18 Traditions slot pyoMinute/pyoTray + one call in eventsTick: finishing at a bed during
  Pick-your-own gives the servery's own tray ("the fruit and greens you picked"), a toast and an arrow to a free mess
  seat (cleared when the tray's gone); walking away early gives none; once a day (not saved, as trays).
- New lines FAIL on 364c80cb: interactions mess part (4) (3 lines), events part 12 (2 lines). Planted faults caught:
  TRAY_TRAVELS false, the hold line reverted, no pyoMinute call, no pyo arrow, and (after FX12's fix in da1825d2) the
  once-a-day rule removed. Finding fixed in da1825d2: the once-a-day line had judged after the tradition ended
  (passed trivially); now it picks again at 06:25 and checks it's inside the window first.
- events_check (whole) OK; interactions_check (whole) OK; arrows_check week OK; food_check 1 7 OK; cadet_test vs
  364c80cb ALL IDENTICAL; check_fast FX12's OK on da1825d2 (string change only since my runs).
- For the lead (not a defect): TRAY_TRAVELS is on while the design doc says "to confirm with the user". Off-deck the
  seat can be any public sit place (an auditorium or garden seat included); sitting there eats it, harmless.

## AC3 arrows-c 4928271f (item 6 follow-up for the round's mech_check m3d FAIL on 0dd4e2e2): PASS (~10:35 UTC)
- Diff: one condition in clockFirstTick: `m < CAREER.missBy` (12:30). The help (tip + Clock in tracked) now only from
  08:00 (CAREER.clockIn) till the shift counts as missed; "near 09:00" read as the clock-in window the career already
  uses. After 12:30 want is false, so a waiting clock-in tip is dropped too. (An arrow set before 12:30 and never
  punched stays to the shift's end through Tracked's own clock row, clockRemindTick: as before this change.)
- Tested as the fix applied to the candidate 0dd4e2e2 (game 4e653844... -> f18e8540...).
- mech_check m3d: FAILs on 0dd4e2e2 ("no arrow left": Clock in at the time clock), OK with the fix.
- arrows_check clockin OK; intro_check --firsts (13, 13b: Day 1 Clock in arrow, tracked till you punch) OK;
  intro_check --p923 (#7 Zeke's clock-in first, Day 1 lines) OK; cadet_test 0dd4e2e2 vs fix ALL IDENTICAL (renderer
  noise only).

## FX12 p924-fx12 (0.92.4 item A, the user's tray rules): in progress
- b513e0cc (game e5937be9-diff; TRAY_TRAVELS false, trayKeep, actEnd's "leave your tray" toast, trayGo for
  Pick-your-own): FIXES NEEDED, test only: its interactions_check.py deleted FX8's 0.92.3 #22 block (Rina's health
  check by a real tap + RV11's two lines). FX12 restoring; also moving the off-Deck-3 Pick-your-own arrow to a mess seat.
- On b513e0cc's game: servery line and queue tiles all in room M (probe), so a served tray is never cleared at once.
  Mess part + events part 12 OK; on 3866c8f3 the new lines FAIL; planted faults caught: k1 TRAY_TRAVELS true, k2 never
  left behind out of the mess, k3 Pick-your-own tray not travelling, k4 no "leave your tray" word. cadet_test ALL
  IDENTICAL, food 1 7 OK, arrows week OK. To rerun on the new sha (game changes in needGoal).

## FX9 go-walk claude/p925-fx9 84e14d89 (0.92.5 item 1, the walk after the toilet): PASS (~18:30 UTC)
Game sha256 c0ed76be...534d; base 3866c8f3.
- Diff: one line in section 8b animateRig's leg loop (runs every frame, unconditionally): leg.knee.rotation.z = 0.
  Nothing else in the game sets knee z (grep), so only HOLDS.go's knees turn them in, now from straight each frame
  (L(0, target, s)); full blend unchanged (0.256). player_check: knees read after a toilet visit, walking and after
  sitting while bursting.
- player_check: OK on the fix ([0,0],[0,0]); FAILs on 3866c8f3 ([0.256,0.256] both): the base is the planted fault.
- cadet_test vs 3866c8f3 ALL IDENTICAL (crew rigs too); check_fast OK (243 s).
- ceee5664 (game 553603f9...): PASS (~18:45 UTC). FX8's #22 block restored exactly (git diff 3866c8f3 --
  interactions_check.py: only the mess parts (1) and (4)). Game change since b513e0cc: needGoal's seat deck
  (sd = TRAY_TRAVELS ? here : 3), so a Pick-your-own tray off Deck 3 is pointed at a mess seat. events part 12 OK on
  ceee5664, its new line FAILs on b513e0cc (4-bench-2); mess + Rina parts OK; cadet_test vs 3866c8f3 ALL IDENTICAL.
  b513e0cc's game runs above (planted faults, food, arrows) stand: the only game change since is that line.

## DV1 promo-arrows 81e9065c: not mine after all (lead 34, 19:18 UTC): RV13 had already reviewed and PASSed it
(the shelf top-up point covered: at most 2 free parts on test day). Nothing run here.

## FX13 simflight 9fa1e1ae (sim flight landing prototype, standalone, a light look for lead 34): PASS with nits (~20:55 UTC)
- starship-cadet.html untouched (git diff 3866c8f3 empty). New: simflight-proto.html (285 lines), tools/
  simflight_proto_check.js, plans/simflight-plan.html, screenshots.
- Read: rules (fnew/fstep) plain numbers at a fixed 60 steps/s, no Math.random/R; drawing apart; colours through col();
  instanced rings; 6 draw calls flying; three r128 from cdnjs; tips once (localStorage in try/catch); Leave/Done/Again.
- SIMFLIGHT CHECK OK twice (run with the paths pointed at a worktree copy): soft/hard/miss from scripted pilots, each
  the same twice; touch drag, mouse, keys; tips once; no page errors. Screenshots look right (rings, lit bay, result).
- Nits (not blocking, a prototype): (1) coplanar faces in the hull: the top and bottom blocks share the side blocks'
  top (y = 26) and bottom (y = -18) planes over a 1-wide strip, and the back plane (z = BAY_Z + 140); same colour, so
  no visible flicker, but against the "no coplanar surfaces" rule (e.g. make the top/bottom blocks a little lower /
  shorter). Thin seams between the blocks show in the shots. (2) The check hard-codes /home/user/Cadet-game for the page
  and the shots folder; deriving both from __dirname would let it run from any checkout.
- a7f3822c: both nits fixed (top/bottom hull blocks y 8-25.6 and -17.6-0, z +0.4 to +139.6: no shared planes; the mouth edges at y 0 and 8 unchanged; the check's paths from __dirname). Read, fine.
- 7bf86392 (round 2, the user's notes; light look): game untouched; left/right turned round only in input() (camera looks along +z, so screen right is -x; rules and pilots unchanged); prettier view (sky dome, nebula, planet, new Wren/Tern, beacons, ring halos), 17 draw calls, no random calls, colours through col(). SIMFLIGHT CHECK OK twice; shots look good. Nit: the drag-right line passes on a 5 px move (291 -> 296 of 390), since the camera follows: thin margin.
- 6d5611ee: the nit taken: FL.screenVx() (vx along the camera's right vector; the page's only change), the three steering lines need > 3 m/s the right way; FX13 planted the unflipped steering: all three FAIL. Read, fine.

## FX9 lift-flash claude/p925-fx9c 8777fc44 (game 91cc7716's, 0.92.5 item 21): PASS (~23:00 UTC)
Game sha256 67dc4eee...f8cb; base integration ba836359 (2aa6427f...).
- Diff: one line at the end of updateDeckCrew: each newcomer (not in `here`) gets h.set at x+lx+hx, y, z+lz+hz, face,
  heldPose: the same call as CrewAgent's per-frame update (l.55984), so the first drawn frame is where it is. day_check:
  a per-deck "arriving" line (first drawn spot within .1). Backlog FX9-1 row (separate).
- day_check 1 OK: 0 of 560 arrivals drawn elsewhere; on ba836359 FAILs on every deck (29/29, 59/60, 196/196, 167/168,
  40/40, 5/5, ...), all "drawn at 0.0,0.0": the base is the planted fault.
- cadet_test vs ba836359: j_steer1 and j_steer2 differ (FX9 reported j_steer2 only): looked at both: walkers' leg
  phase only (one walker in j_steer1; one at the right and an arm at the left edge in j_steer2), same spots: the jump
  from the origin used to count as walking and advance their stride. Explained. check_fast OK (260 s).

## FX11 p925-fx11 c97fbef0 (0.92.5 #17 follow-up: an auditorium seat has no timer, the user's): PASS (~23:10 UTC)
Game sha256 b8faa999...; base 23432122 (RV11 PASSed items 2, 3, 14, 17 there).
- Diff: PLAYER_ACTS.recSeat gets until: () => false (as plain sit); the leisure gain still only over its first 15
  minutes (actUpdate caps m at mins - done). recSeatHold/REC_AUD_SHOWS (built this patch, never released) and their two
  calls removed; the seat's toast "Stay as long as you like; walk away to get up."
- disc_check: ALL OK; on 23432122 the three #17 lines FAIL (up at 16:50, 10:37, 16:50): the base is the planted fault.
- cadet_test vs 23432122 ALL IDENTICAL (renderer noise only); check_fast OK.

## FX13 tiles-ladder claude/p925-fx13b 5e1d82d5 (0.92.5 item 20): PASS (~00:40 UTC 2026-10-25)
Game sha256 515233c1...; base integration ba836359. (ae8c8bc9 replaced by 5e1d82d5 at lead 34's ask: tladLead.)
- Diff: 4d deck architect slot: 9 standing ring spots 3-ladder-1..9 (event-tagged), the stools' anim play; trad file:
  where pool @tiles-ladder first (lounge seats overflow), no tilesNight boards, anim talk; section 18 slot: tladMinute
  (live only, Deck 3 while on: two at the stools via crewComeTo, 10-minute games, winner stays by a level-weighted
  hash k 335, queue from the settled ring, host first; nothing saved, plans unchanged), tladJoin (eventJoin + a Play /
  Watch card; MEETING_SCRIPTS written at runtime, as rec.talent and FLC already do), tladAgain, tladLead (ev.lead like
  friLead: host 20 min early, others 15 when eventFree; the planner caches cleared once at load, as section 18's end).
- join_check (run alone; side by side two runs timed out at its save/reload page.goto, line ~143, not the ladder):
  OK on the fix; on ba836359 5 ladder lines FAIL; plants caught: t1 no tladMinute (nobody plays, you never sit), t2
  no tladJoin (no Play/Watch card), t3 ring spots untagged (ring empty, all in lounge seats), t4 no tladLead (host
  not at the table by 15:02, ring empty).
- events_check OK, day_check 6 OK, tiles_check ALL OK, cadet_test vs ba836359 ALL IDENTICAL, check_fast OK (249 s).

## FX12 claude/p925-fx12 91b97ee9 (= 20860227 + 0.92.4 merged; 0.92.5 items 4, 9, 10): all OK but arrows week: FIXES NEEDED (blocking), ~00:55 UTC
Games: 20860227 cfb237c9...; 91b97ee9 84ece11c... (diff 20860227..91b97ee9 = 0.92.4's game changes + the one resolved hold line).
- Read: late piano Tue+Thu 21:40-22:25 with a new .trad field to-bed (evArrive/eventPlan: off to bed 20 min before
  bedtime); evBdaySlot inside eventsOn after evBudget (the day's list stored first for the galley/shift recursion; pure
  per day) moves the birthday to the quarter hour 17:00-21:30 with the fewest weekly traditions within an hour, only
  weekly ones dropped; birthdays redone (head chair 3-bday-head, ring 3-bday-1..8, DECK_DRESS.birthdayTable, bubbles
  via lineFor live only, a cake tap gives a slice in hand eaten over 5 min, once a party; the servery cake hidden).
- events part 13 OK; on 3866c8f3 it FAILs (piano two nights running, the birthday within an hour, no head, no cake).
  Plants caught: b1 evBdaySlot off, b2 to-bed ignored, b3 whereFor off (park-noor at the head), b4 no slice in hand.
  Also OK on 91b97ee9.
- events_check OK, day_check 1 OK, food 1 7 OK, check_fast OK, cadet_test 91b97ee9 vs ba836359 ALL IDENTICAL.
  FX12: intro_check OK.
- arrows_check week (no 'guide'): FAILs on 20860227: Day 9 "m6" not learned; stuck from Day 9 10:39 at "! Burst pipe,
  Deck 4" (the arrow up 3+ hours from 10:34); OK on 3866c8f3. Reproduced (DV1 had no repro with the queue on). DV1
  digging (lead 34/35's call).
- DV1 claude/m6-day9 e823a74f (on 91b97ee9, arrows_check.py only, game unchanged): the follower closes Dev mode's
  sheet (#dmSheet, opened by a pin tap under the top-left place-and-clock card in the #dev page) and the Ship health
  panel if left open, as a player would. PASS: arrows_check week on 91b97ee9 and on 20860227 with it: ARROWS CHECK OK,
  m6 learned Day 9, stuck 0 (before: stuck 10:39 at the burst pipe). No game bug (the normal game has no Dev sheet).
- So FX12 91b97ee9 + DV1 e823a74f: PASS (~01:45 UTC).
