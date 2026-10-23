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
