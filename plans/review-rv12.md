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
