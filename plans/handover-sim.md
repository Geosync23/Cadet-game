# Handover: the sim engineer

Written at build 0.40.8 so a fresh session can take over. The detailed notes are in DEV_NOTES.md, in four sections: "Ship time and saving", "Schedules", "Crew on the deck" and "Every room in use". This page is the short version, plus the things that only live in my head.

## Role, branch, builds

- **Role:** the ship's clock, saving, the crew's daily plans, and the crew walking about on the deck you're on.
- **Branch:** `claude/sim-engineer`. My builds:
  - 0.15.1: time and saving;
  - 0.21.x: schedules;
  - 0.22.x: crew on deck and day_check;
  - 0.26.1 to 0.26.7: Pillar 2 A1, "every room in use".
  - Combined builds come from the lead on `claude/ship-integration`.
- **Sections I own in `starship-cadet.html`:**
  - **13. SHIP TIME & SAVE.** It sits after section 5, not at the end, because the clock drives the light and the save is read before the first deck is built.
  - **14. SCHEDULES.** Right after 13.
  - **10. WALKERS.** The crew agents: from `CrewAgent` down to `crewDetail` / `FullPerson`.
- **Test scripts I own:** `day_check.py`. I also added the `?nosave&debug` loader to `cadet_test.py`, and the crew line in `deck_check.py`.

## What's built, and what other sections rely on

### Time (section 13)

- `SHIP.time = { day, min }`. Day 1 is a Monday, and `min` is fractional.
- `SHIP_RATE = 1440 / 1800`: one ship day is 30 real minutes.
- Helpers:
  - `shipNow()` gives absolute ship minutes, which is the unit everything else uses;
  - `setShipNow(abs)` sets the clock;
  - `weekday(day)` gives 0 for Monday;
  - `hhmm(min)` formats a time;
  - `nightAt(min)` gives the light, from 0 for day to 1 for night.
- Jumps:
  - `skipTo(abs)` only goes forward, and calls every function in `SIM_ADVANCE` with `(from, to)`;
  - `sleepUntil(min)` skips to the next time `min` comes round.
- `offerSleep(worldPos)` handles a tap on your bunk (`playerBed()` = `ROSTER_PLAYER.bed`), with `WAKE_AT = 360`.

### Save (section 13)

- Stored in the browser under `starship-cadet-save`, in a format with `v: 1`. It holds the build, the time, the player (deck, tile and facing) and the unlocked doors.
- Other sections add their own parts: the player's needs, food and machines.
- `saveGame()` runs every ship hour, on a deck change, when the tab is hidden, and after a skip. `loadGame()` returns null if the save is anything odd.
- `GAME_BUILD` must match the build line in the HUD.
- URL flags: `?nosave` turns saving off; `?debug` shows the Night/Day button. Every check loads with both.

### Plans (section 14)

- `planDay(person, day)` gives back-to-back segments `{ from, to, act, deck, type, placeId, fromDeck?, tag?, anim?, hold? }`.
- `shipDay(day)` plans everyone at once, in wake-up order, sharing an occupancy map (`occ`) so no place is double-booked. The last 10 days are cached in `SHIP_DAYS`.
- `whereIs(person, t)` gives `{ deck, act, type, placeId, moving, fromDeck, from, until, tag, anim, hold }`. It asks section 17's `jobWhere` first, guarded by `JOB_WHERE_BUSY`.
- `planWhere(person, t)` is the plan alone. **Anything that builds plans must use `planWhere`, not `whereIs`.** That covers `dayReport` and section 17's `jobRun`. Using `whereIs` there loops back on itself.
- Who and where:
  - `schedPeople()` is everyone except the player;
  - `peopleOn(deck, t)`;
  - `runDay(day, step, fn)`;
  - `dayReport(day)` does the checks for day_check;
  - `roomsInUse(d0, days)`;
  - `jobVisits()`.
- Needs:
  - `crewNeeds(p, t)` gives hunger, energy, hygiene, fitness and social (0–100), read off the plans;
  - `needsEst(p, d)` is a cheap start-of-day estimate used to steer the plans.
- Hooks into other sections:
  - `shiftBlocks(p, d)` reads `galleyDay` (section 16) for galley staff, and `rota.hours` for the storekeepers;
  - `galleyRotaOn()`;
  - `shipEffectsAt(deck, t)` (section 17) makes people avoid broken things.

### Crew on deck (section 10)

- `DECK_CREW` holds a `CrewAgent` for each person on the deck you're on. `updateDeckCrew(dt)` runs from the main loop.
- `deckCrewFill()` / `deckCrewClear()` run on a deck change and after a skip. People arrive in the middle of what they're doing.
- Pathing:
  - `placeSpot(id)` gives the walk-to tile and the exact spot;
  - `crewPath()` opens 'closed' doors only into the agent's own rooms, and service hatches only for whoever `hatchPassable` allows;
  - `crewNearDoor(d)` is used by the door code.
- Shared with other sections:
  - `placeBusy(id)` says whether someone is settled at that place, or it's the player's place (`PLAYER_PLACE` from section 15's `playerHolds()`). Section 17's machines use it.
  - `galleyHold(person, t)` (section 16) gives the servery queue spot. A guard sends people to stand if their spot is already taken.
- Poses:
  - `crewPose(agent)` gives the pose string: the plan's tag first, then reading, talking or drinking in a lounge, then `poseOf(place)` (section 8b);
  - `heldPose(agent)` adds `+cart`, `+cartfull` or `+carry`.
- `tapCrew` / `crewAtScreen`: tap someone and they stop and face you.
- Full rigs: the `FULL_MAX` (3) story crew within 4.5 tiles get a `FullPerson`, a full character model that borrows `CrowdPerson.prototype.set/update`. If section 8b renames the crowd's fields, `FullPerson` breaks.

## State at 0.40.8

- **Rooms in use:** 56 of 59 place types are used over a week. The three unused:
  - Deck 2's `work:command` desk, in a locked room;
  - Deck 5's storage, which isn't in the plans but jobs do visit it;
  - Deck 6's `lift-wait`, because engine crew only leave at the end of a shift.
- **Weak spots:**
  - One person's fitness stays very low. The gym is often full in the evening, so only about 2 in 5 of the visits she wants actually happen. More gym places, or a morning gym slot, would fix it.
  - The `window-seat` habit does nothing, because no place says it's by a window.
  - Hunger only sits around 70–75 in the evening, since there are two meals and no lunch, as designed. Fine on paper, but worth watching if the player can see crew needs.
  - The Wednesday drill leaves a few people standing, because Deck 1 has only 4 `lift-wait` places.
  - The ship doesn't run while the game is closed (no catch-up on load), and crew state isn't saved. Plans are rebuilt from the clock, so this is fine for now.
- **Next, if it were mine:**
  - Gym capacity or timing.
  - Check that Bunk 1's item text ("Your bunk. You lost the coin toss…") points at the same berth as `ROSTER_PLAYER.bed`. At 0.21.2 they disagreed, and I haven't re-checked since the roster moved.
  - Give `lift-wait` on Deck 6 a reason to be used.
  - Cut day_check's run time (about 4–6 minutes) by skipping the drawn frames when only plans changed.

## Gotchas

- **No `R()` in section 14 or in kit made at load.** Every choice uses `schedU(seed, day, k)`, a hash. Add a new choice with a new `k`, and the old ones don't shift. Calling `R()` breaks the pixel-identical regressions.
- **Name clashes**, because everything is one file of global names:
  - `BUILD` → `GAME_BUILD`;
  - `roomLocked` → `schedRoomLocked`;
  - `galleyRota` → `galleyRotaOn`.
  - grep before naming anything.
- **Merge traps:**
  - Section 17 once arrived with its own `planWhere`, missing fields, which silently replaced mine. At a merge, check for duplicate function names (`grep -c "function planWhere"` should give 1).
  - `jobRun` must use `planWhere`, or it loops forever.
- **Pathing bugs that came back more than once:**
  - A walk-to tile must be in the same room as the place, and reachable from the lift. Otherwise someone tries to reach an en-suite through a wall.
  - Agents set off from the place's walk-to tile, never from the furniture tile.
  - Agents can always leave the room they're in, even if it's locked.
  - Tap checks skip whoever is lying in the player's own bunk.
- **Galley timing:** free time ends at the stint's start minus the walk. An early arrival lingers first, then works, or stints overlap. The dish-pit "double-booking" check compares times, not just place ids.
- **Where the tuning numbers live (all in section 14):**
  - `WEEK_SHAPE`, `LEISURE`, `HABITS` (section 9 data), `HABIT_LEISURE`, `PLACE_ANIM` and `SOCIAL_TYPES`;
  - the needs rates, in `crewNeeds` and `needsEst`;
  - the toilet, tea and shop chances, in `schedBuild`.
  - Section 10 has `FULL_MAX`, `FULL_NEAR` and `FULL_FAR`, and the stand-still time on a tap (6 s).
- **The test harness:**
  - Don't `pkill` broadly: it kills the shell.
  - Run player_check and deck_check alone; they time out under parallel load.
  - Keep scratch scripts in the scratchpad, not the repo.

## How to test

- `python3 day_check.py BUILD.html 1` and `... 7`. Good looks like:
  - Schedules: 0 short sleep, 0 missed meals, 0 short shifts, 0 double-booked, 0 gaps.
  - "Plans the same twice: True".
  - Every deck: worst stuck under 10 ship minutes, nobody sharing a place, nobody in someone else's bed, no "no path", nobody missing.
  - Draw-call peaks under 450 (they were about 370–420, with Deck 6 about 305).
  - "Deck 4 the same twice: True".
  - Ends "DAY CHECK OK".
- `cadet_test.py OLD.html NEW.html`: ALL IDENTICAL against the last build, unless crew changed on purpose. Then compare with crew off in both.
- `deck_check.py`, `player_check.py`, `food_check.py` and `machine_check.py`: all OK. My changes can upset player_check (saving), food_check (galley rota and queue) and machine_check (`placeBusy`, jobs).

## Ideas and open questions for the user

- Should the ship keep going while the game is closed? Plans are built from the clock, so catching up is cheap. The open question is whether the player should miss things.
- Should crew needs be visible, for example in the tap toast ("Tomas looks tired")? The numbers already exist.
- What is a window seat? If a few places get marked as by a window, the habit starts working.
- Should the gym get a morning slot, or more equipment, so the fitness-minded crew actually go?
- A lunch? The design says two meals, and hunger is fine with two, but the galley is quiet from 10:00 to 16:00.
