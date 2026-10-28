# Handover: FX26 (builder, 0.93.2 storm Saturday and the Captain's stage fix)

**Role:** builder for lead 37, then lead 38. **Branch:** `claude/storm-sat`, from `claude/integration` b957b92d (0.93.1).
**Final:** 402899bd (0.93.2-w.5, game sha256 c799f15e...), RV19 PASS (plans/review-rv19.md). Done; idle.

## What I built (build-table rows 0.93.2-w.1 to w.5)
- **The Captain on the stage (not switched).** 8b's body (CrowdPerson, shared by FullPerson) reads a height of .3 and up
  as a seat's, so anyone *standing* on the rec deck's .55 stage stood on the deck floor with their legs in it.
  `DECKS[7].floorY(x, z)` (section 4e) gives the stage's height under a point; `CrowdPerson.set` keeps it as `fy` and a
  standing or walking body stands on it. The bubbles (8b `place()`) and the address speaker stand-in (18f `friSpeaker`)
  pass `fy`. Only deck 7 has floorY: every other deck is the old expression. Seats on the stage were already right.
- **The storm's Saturday (Day 13), behind `STORM_SAT_ON`** (section 18, beside `EV_STORM_ON`; slot 'Storm Saturday'
  after the Storm builder's; data in the storm update's block after `S.dayDress`):
  - you're called in 09:00-17:00 (`playerCalledIn` / `playerOnDuty`; your rota `playerShiftOn` unchanged, so lessons and
    career beats don't move); the Works day crew work too (`isWorkDay` + `stormCalledIn`);
  - the board, the device's Jobs list and the arrows show only storm jobs (`stormBoardHide`); seven storm repairs in
    three waves, held 90 minutes for you; Calder's Mail Friday 18:00 (placeholder words, key
    `event.ionStorm.mail.stormSat`);
  - the lantern supper is that day's dinner (pull 1 for everyone, sittings 35-50 minutes; no Dinner row that day);
  - Storm stories by torchlight: `content/traditions/storm-stories.trad` (k 474, never on its own rhythm: the storm's
    dayDress adds it), Oduya hosts (tap to join, `TRAD_JOIN`), `spare: 1`, its talk (`stormStoriesFrame` via FX17's
    `tradTalk`, the room's chatter hushed), the look (`DECK_DRESS.stormTorches` + `stormSupperDim`'s low light).
- **Shared fix:** section 15's actEnd titles a joined tradition's (`tj:`) end toast with its name, not its id; ixSide's
  "The company helped." without a leading space. The owner (player engineer) should look at merge.
- **leave_check:** its sample day off is Sunday Day 14 (Day 13 is now the call-in).

## Loose ends (lead 38: to the 0.93.3 backlog)
- The join toast shows twice, and its "About 44 minutes" ignores a late join (pre-existing, every joinable tradition).
- Only four listener asides at the storm stories: one repeats about 3 times in 30 minutes.
- `stormSatDay()` is cached per page (fixed for the game: from the calendar and the skips decided at load).
- Seen, not changed: from some front-row spots the black band along the stage's edge hides the head of someone walking
  along its foot (before too).

## Gotchas
- Checks that freeze or overload the machine time out on page loads (`Page.goto: Timeout`); interactions_check takes
  over an hour in this container (same pace on the old build). Pausing other check lanes (`kill -STOP`) for a clean
  check_fast works, but a check in flight then times out: rerun it.
- `stormSatDay`, `stormCalledIn`, `playerCalledIn` are function declarations and read section 18's consts inside
  try/catch: the planner calls `isWorkDay` before section 18 has run.

## How to test
Switch-off copy: `sed 's/^const STORM_SAT_ON = EV_STORM_ON; /const STORM_SAT_ON = false;/'`; cadet_test vs b957b92d
identical both ways. day_check 13, food_check, bigevents_check (the supper's seats), join_check, events_check,
fridays_check. Shots: plans/fx26-shots/.
