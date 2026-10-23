# RV10 reviews: the user's late tweaks for 0.92.0 (cut-off 07:00 UTC)

Reviewer RV10 (session_01XeJ6bvySekD1V8Sfh1tzgb), lead 31. Probes in plans/review-rv10/ (each takes GAME.html,
a folder holding cadet_test.py, an output folder).

| What | Commit (base) | Verdict |
|---|---|---|
| DV1 Dev career arrow | claude/dev-career-arrow 9f51257a (arrows-c f8ed8521), sha 5be2df87 | PASS |
| FX7 Tiles partner sits | claude/tiles-sit 0a58748e (breakfast-back 0cd37b1b) | PASS |
| FX6 hygiene cooldown | claude/hygiene-cool cbd41548, then 50fd3f2a (breakfast-back 0cd37b1b) | FIXES NEEDED, then PASS |
| FX5 call-home booth arrow | claude/booth-arrow 771c9ff2 (3 commits + arrows-c 8ab6089f), sha b8d67573 | PASS |
| FX5 Day 0 table to the goodnight | claude/day0-table 153084a1 (integration-next b842fa43), sha f2329b62 | PASS |

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

## FX5 day0-table, 153084a1: PASS
- The Day 0 seat split past 19:00 gets kept: 1; lead() no longer cuts it for the next walk. kept_probe.py: kept seats only
  on Day 0 (48) over Days 0-28; each still ends at its planned minute.
- events_check: Day 0 table before the goodnight 45 on b842fa43 (FAIL), 48 after; other Sundays identical.
- intro_check booth line: a mutant without the move line FAILS it. Full intro_check base vs fix: identical output, 0 FAILs,
  up to a 50-minute limit (includes the Day 0 dinner). day_check 1 and 7 OK, check_fast OK, cadet_test ALL IDENTICAL.

## 0.92.1
| What | Commit (base) | Verdict |
|---|---|---|
| AC3 join notices kept + cadetPopupsNow hook | claude/arrows-c 54169e4c (integration 685af944) | PASS |
| FX4 save trim | claude/fx4-save-trim 06a989e6 (integration 685af944) | PASS |
| FX7 gym bike tap | claude/bike-tap 9328dc76 (integration 685af944) | PASS |
| FX5 Day 0 trickle | claude/day0-trickle 0e392cf3, then de475883 (integration 685af944) | FIXES NEEDED, then PASS |
| CP5 controller follow-up 2 | claude/controller-follow2 f293d672 (integration 685af944; off) | PASS |

- AC3: arrows_check queue lines fail on 685af944, OK after; join_check OK (alone); check_fast OK; cadet_test identical.
  join_probe.py (real tap on Mira, Gym club, then four pop-ups): base drops the join notice, AC3 keeps it, both sizes.
  Pop-up timing runs on the test's virtual clock (performance.now): step frames, don't wait real time.
- FX4: career_check's three lines fail on base (Day 120 4673 bytes) and pass after (2816); callers only read this or
  next week; puzzle_check, check_fast OK; cadet_test identical. Nothing on screen.
- FX7: bike_probe.py (touch, both sizes, four turns, floor/saddle/bars): 47-48 of 48 vs 42-43 on base; 28 other Deck 3
  places identical on both builds; interactions_check 32/32 (alone), player_check, check_fast OK; cadet_test identical.
- FX5 trickle: events_check new lines fail on base, OK after; day_check 0, check_fast OK; cadet_test identical. But the
  live goodnight re-plans the day from its start: trickle_probe.py shows ~6 non-diners on Deck 3 get a different place for
  the activity under way at that minute (goodnights 18:20, 18:40, 19:10; none at 19:45); trickle_live.py at 18:40: Lukas
  gym-13 -> gym-14 mid-workout, Esme lounge-31 -> 33, Zofia garden-6 -> tend-12 (they walk). Options sent to FX5.
- CP5: controller_check lift 4 FAILs on base, OK with both mutants caught; pick (CTL_MUT=CP1) and day OK; check_fast OK;
  cadet_test identical with PAD_ON off and on.
- FX5 trickle de475883: no whole-day re-plan; day0Trickle patches only the diners. trickle_probe.py at 18:20/18:40/19:10:
  no non-diner's plan changes; live at 18:40 Lukas, Esme, Zofia stay put. events_check, day_check 0, intro_check --evening,
  check_fast OK; cadet_test identical. Diners with an hour or more go to their bunk and come back for their evening.

## Gotchas
- Four browsers at once on 4 cores makes devmode_check and tiles_check flaky (timing); run two at a time.
- Teleporting the player (player.obj.position) doesn't move them for taps; use playerTap or real floor taps to walk.
- The morning (06:00) showers are full of crew; test at 14:00 (skipTo).
