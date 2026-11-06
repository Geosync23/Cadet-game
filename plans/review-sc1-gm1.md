# Review: GM1 (claude/p997-games 9175156), by SC1 for lead 49 (2026-11-06 ~09:50 UTC)

Game sha256 f8936885533aa382d80a180a459a0798cc8d07352605fef30eec2fa5f2b2e441 (matches). Switch GAMES997_ON. Notes 12, 40,
41, 44 (plans/patch-0997.md on claude/lead-49). Probes in /tmp (tn.py, tut.py, wso.py, wsolead.py), run at 390x844
from a fresh game (?nosave&debug; skipTo, then playing frames as a player would).

## Checks
- cadet_test, switch off, vs 0.99.6 (f6ff5ec1): ALL IDENTICAL (one shot, j_steer1, 6 px 1 level off, run under load: the
  test's own renderer-noise rule; RV33 had it clean).
- Switch on (a copy): tiles_check ALL OK, join_check OK, disc_check ALL OK, events_check OK, interactions_check OK.
- check_fast: QUICK CHECK OK on the build (342 s) and on the switched-on copy (336 s).

## Probes (switch on)
- **12 + 40 Tiles night, Day 2.** Before 20:00 a tap on Rina does nothing (it starts at 20:00, fine). At 20:01, tap
  Rina: card "Tiles night: three rounds, winners play winners. Play at a board, or watch first?"; Play. Round 1 20:05:
  you're seated against Ravi, the other 12 at 6 boards; round 2 against Saad, round 3 against Lukas (sensible: you lost
  each, so the others on 0 wins). The Tiles app lists the round, the boards and the results ("Ravi beat you."). Works.
  Note: round 1 you sat at 20:05 and the board opened at 20:15 (Ravi walking over: 10 of the round's 25 minutes).
- **41 tutorial.** 12 steps; every term (mark, dock, step, jump, hold, launch, home rows, rings, spark) explained the
  first time; reads well. Step 10 waits for a launch, which needs a tile in your hold; a newcomer often has none yet
  and, unlike step 8, it doesn't say "Can't yet? Press Next."
  Phone layout: the longer step box scrolls the device body 179-202 px (0.99.6: 140), so at 390x844 Ravi's top row is
  wholly out of view while step 1 says "Ravi's are the outlined ones at the top" (shots tut-old-0 / tut-on-0).
- **44 Winner Stays On, Day 7.** The Calendar's tracker points to the Stands; in the stands the arrow says "Tap Emeka
  to watch from the stands"; tap: joined, seated. After a game ends (12:10) the card "Fancy a go?" / Play the next game;
  12:30 you're on court against the winner; lost 1-3; back to the stands. With AV1 (15fbf3f) merged and SND_DISC on:
  during the game PAUSE.on false, PAUSE.disc() true, so SND.frame keeps the music running.
  **Problem:** the card's speaker and the re-ask tap are Pell, else tradLeader(e). Pell is at none of the first 7 Winner
  Stays On days (Days 7-63, on paper), and tradLeader arrives 20-50 minutes after the start (Day 7: Bo at 12:17, the
  card came at 12:10 from "Bo Mbeki", not on the deck). And w997Tap accepts only Pell or tradLeader, so tapping the
  person the arrow named (Emeka) never asks again; "Tap me when you fancy a game" can't be done until Bo turns up.

## Verdict
FIXES NEEDED: 1 must (the WSO card's speaker and tap), 1 should (the tutorial's phone layout), 2 small notes.

## Re-review: 98e612e (game b939eb9, sha256 866743ed...13260): PASS (2026-11-06 ~11:20 UTC)
- MUST fixed: Day 7, the "Fancy a go?" card now from Raman (at the court; tradLeader still Bo, not there yet); after a
  lost game, tapping a watcher (Erik) offers another go. Words no longer name Pell.
- SHOULD fixed: 15 short steps; at 390x844 the whole board (both of Ravi's rows) in view on every step, the step box
  630-771 inside the device body (358-776); better than 0.99.6 (which hid half a row).
- Small: the launch step says "Can't yet? Press Next."; round 1's walk left as is (GM1's call).
- cadet_test off vs 0.99.6 ALL IDENTICAL; switched on: tiles_check ALL OK, join_check OK, disc_check ALL OK,
  events_check OK, interactions_check OK; check_fast QUICK CHECK OK on the build (412 s) and on the switched-on copy (414 s).
