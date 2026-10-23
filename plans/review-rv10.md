# RV10 reviews: the user's late tweaks for 0.92.0 (cut-off 07:00 UTC)

Reviewer RV10 (session_01XeJ6bvySekD1V8Sfh1tzgb), lead 31. Probes in plans/review-rv10/ (each takes GAME.html,
a folder holding cadet_test.py, an output folder).

| What | Commit (base) | Verdict |
|---|---|---|
| DV1 Dev career arrow | claude/dev-career-arrow 9f51257a (arrows-c f8ed8521), sha 5be2df87 | PASS |
| FX7 Tiles partner sits | claude/tiles-sit 0a58748e (breakfast-back 0cd37b1b) | PASS |
| FX6 hygiene cooldown | claude/hygiene-cool cbd41548, then 50fd3f2a (breakfast-back 0cd37b1b) | FIXES NEEDED, then PASS |
| FX5 call-home booth arrow | claude/booth-arrow 771c9ff2 (3 commits + arrows-c 8ab6089f), sha b8d67573 | PASS |

## DV1, 9f51257a: PASS
- Diff only adds lines (section 25's slot + one line in devmodeQuick); nothing runs without #dev.
- dev_arrow_check fails on the base, OK on the commit. check_fast OK. devmode_check OK on base and commit (one run with
  four browsers at once failed "the ship ran under a Dev action's fade": load timing; two at a time both OK).
- cadet_test base vs commit, Dev off: ALL IDENTICAL.
- Real taps (320x640, 390x844): Set career Day 2 / 5 / 8 and the Day 9 test-job beat; labels match the game's rules
  (PROMO.from 8). With both arrows at the lift the game's arrow points and the DEV label sits below; the arrow takes no taps.
- Notes: label cut with "..." at 320 wide; at the Day 9 beat the DEV arrow says clock in first, the game's goes to the job.

## FX7, 0a58748e: PASS
- tiles_check new line fails on the base (partner on 4-common-6, 1.91 m away), ALL OK on the commit (first runs under
  heavy load both stopped on a "Quick game" click timeout, base too). check_fast OK. cadet_test ALL IDENTICAL (noise).
- Real screen tap on Deck 4's Tiles table at 19:00: Sol sits on 4-common-8 across the board; at 14:00 Femi already seated
  plays you. Note: the partner's pose on the stool is sit:read.

## FX6, cbd41548: FIXES NEEDED
- player_check new part fails on the base, OK on the commit. cadet_test ALL IDENTICAL (noise).
- Real play: the rec deck's changing-room rinse (played automatically after every swim/kayak, +20 in 3 min) starts the
  full 6-hour cooldown: hygiene 30 -> rinse 49.9 -> Deck 4 shower stays 50. A shower walked away from after a minute
  also locks showers for 6 hours. During a cooldown the end toast still says "Clean, and smelling of the ship's one
  soap" with no gain (the "still fresh" words are in the start toast only).

## FX6 fix, 50fd3f2a: PASS
- Only a full shower starts the cooldown (at half its time, or 40 from short ones, lapsing after 6 h); the rinse never does;
  its own end lines. player_check + interactions_check OK, check_fast OK, cadet_test ALL IDENTICAL (noise).
- Real play: rinse 30 -> 49.9 with no cooldown, then a Deck 4 shower -> 100; a cooling shower ends "A warm rinse...".

## FX5, 771c9ff2: PASS
- Day 0 call arrow and the Tracked "The call booths" row keep to a free booth until the call begins; a tap at the booth's
  pin with someone under it is the booth (ixPinBooth). intro_check --firsts: FX5 lines fail on 8ab6089f, OK after;
  interactions_check OK (alone); check_fast OK; cadet_test vs 8ab6089f ALL IDENTICAL.
- Real taps at both sizes, incl. Calder in Booth 1 with the arrow on Booth 2 at 320 wide: on 6caeb176 the pin tap opened
  her card 3/3; on 771c9ff2 the first tap starts the call.
- Two interactions_check runs at once (base + FX5) both stalled at "near your job, but not it"; alone it passes.

## Gotchas
- Four browsers at once on 4 cores makes devmode_check and tiles_check flaky (timing); run two at a time.
- Teleporting the player (player.obj.position) doesn't move them for taps; use playerTap or real floor taps to walk.
- The morning (06:00) showers are full of crew; test at 14:00 (skipTo).
