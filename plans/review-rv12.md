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
