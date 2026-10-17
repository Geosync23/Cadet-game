# Handover: the sim engineer

Written at build 0.40.8 and brought up to date at 0.26.18 (Pillar 3, 16 October, by the second sim engineer, session_01R6RBwwBM9aorpsqDCrztDU), so a fresh session can take over. **Start with the Pillar 3 section at the end:** it has the work in progress. The detailed notes are in DEV_NOTES.md, in four sections: "Ship time and saving", "Schedules", "Crew on the deck" and "Every room in use". This page is the short version, plus the things that only live in my head.

## Role, branch, builds

- **Role:** the ship's clock, saving, the crew's daily plans, and the crew walking about on the deck you're on.
- **Branch:** `claude/sim-engineer`. My builds:
  - 0.15.1: time and saving;
  - 0.21.x: schedules;
  - 0.22.x: crew on deck and day_check;
  - 0.26.1 to 0.26.7: Pillar 2 A1, "every room in use";
  - 0.26.8 to 0.26.12: the answers pass (time, feelings, habits, window seats, held things, Deck 1 routines, event hooks, event seats held);
  - 0.26.13 and 0.26.14: Pillar 3 appointments, doors and guests.
  - 0.26.15 to 0.26.18 (the second sim engineer): guests from the real data, the storm routines (C7), joined up with section 18, seating by friendship.
  - Combined builds come from the lead on `claude/ship-integration`.
- **Sections I own in `starship-cadet.html`:**
  - **13. SHIP TIME & SAVE.** It sits after section 5, not at the end, because the clock drives the light and the save is read before the first deck is built.
  - **14. SCHEDULES.** Right after 13.
  - **10. WALKERS.** The crew agents: from `CrewAgent` down to `crewDetail` / `FullPerson`.
- **Test scripts I own:** `day_check.py`. I also added the `?nosave&debug` loader to `cadet_test.py`, and the crew line in `deck_check.py`.

## What's built, and what other sections rely on

### Time (section 13)

- `SHIP.time = { day, min }`. Day 1 is a Monday, and `min` is fractional.
- `SHIP_RATE = 1080 / 1800` since 0.26.8: 18 ship hours take 30 real minutes, so a whole day is 40.
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

## Pillar 3 (0.26.13 and 0.26.14) and what's left

The details are in DEV_NOTES, under "The answers pass", "Pillar 3: appointments and doors" and "Pillar 3: guests". The plan is `plans/pillar3-plan.md` on `claude/lead-pillar1`, rows C3, C7, C8 and C10.

### Built

- **Appointments (C3, the crew side):**
    - `apptReply(p, a)` answers from the person's real day (`planWhere`): yes, `later` with a time, or no.
    - `apptWhere` lays an accepted appointment over the plan, first in `whereIs`: the person leaves in time for the lift and the walk, then waits `APPT_WAIT` (15) minutes.
    - `apptTick`, run from section 13's clock, sets `kept` or `missed`. The sim engineer owns those two statuses; the device engineer (session_014TpEMbWarRFJM8BHC9WM8c, 0.35.6) sets 'yes' and reads the rest.
    - `SHIP.device` is saved by the device in `save.device`.
- **The device engineer's open question:** which place to meet at. I answered: any free placeId. Take the seats in the room the player picked from `schedData().shared`, and skip any that `shipDay(d).occ` holds at that time. A helper for this, say `apptPlaces(room, at, len)`, would be a good small first build for you.
- **Doors (C10):**
    - `doorOpenFor(room, who, t, deck)` is true from 15 minutes before an accepted appointment in that room to 15 after, for the player and the crew in `with`.
    - Section 4's `edgeBlocks` asks it for 'closed' doors (one inert line), and section 10's `crewNearDoor` slides the door open for you.
    - The room's inside must be walkable. The Captain's quarters is.
- **Guests (C8):**
    - `guestPeople()` adds `GUESTS` to `schedPeople()`.
    - `guestTrim` handles arrival and departure at 10:00 by the Deck 5 lift, with the guest 'away' (deck 0) outside their stay.
    - `GUEST_LEISURE` and `GUEST_REST` hold the template weights.
    - `dayReport` judges only whole days aboard.

### Loose ends with guests (do these first)

The crew designer's real data arrived after 0.26.14 (0.16.8 and 0.16.9, `claude/deck-plans-1-2-6` 6c895ba), and it differs from what 0.26.14 assumes:

1. **`arrive` and `leave` are days of the year (1–364), not ship days.** Map with `(d - 1) % 364 + 1` in `aboard`, `aboardAllDay` and `guestTrim`. A stay might cross the year end, where `leave` is less than `arrive`.
2. **Event guests have `arrive` and `leave` as null, plus `event` and `stay` (days).** Section 18 sets their day. Until it does, `aboard` must treat them as away; today `!p.arrive` reads as "always aboard". Fix that before merging 0.16.9.
3. **`GUEST_TEMPLATES`** (section 9) replace my `GUEST_LEISURE`. Each is `{ label, day, evening, meals, wake, bed }`.
    - `day` and `evening` are `[deck, type, weight]` lists.
    - `['cabin', w]` means the guest's own cabin, which is my rest option.
    - `['work', w]` means the entry's own `work` place.
    - Survivors also have `first` (days) and `firstDay` (the infirmary for the first days). Delegates have `formal: true`, for the events' formal dinners.
    - Skip types with no places, as LEISURE does.
4. **Draw calls:** 60 guests a year means 1–2 aboard at a time, so draw calls aren't a worry. Still, run day_check on a day with a guest aboard.

### Still to do: event routines (C7)

The events engineer is now session_01GW9QtevJxaMQzzCGPBHaxb (section 18, `claude/ship-events`, 0.34.8 492c03c). I asked for:
- `eventOn(d)`: the event and phase in force on ship day d, with the minute each phase starts. Plans are cached per day, so `eventNow()` (today only) isn't enough.
- The routines as data.

Agree the field names with them. What exists in 0.34.7 and later:
- `eventNow(t)` and `eventMod(kind, key, t)`;
- `SHIP_EVENTS[id].routines[phase]`;
- `SHIP.event.startDay` and `eventDueDay()`.

The ion storm's routine keys (from the lead):
- `eventMod('routine', rule)` with these rules:
    - `doubleShift` for dept:command and dept:helm;
    - `patrol` for dept:watch;
    - `closed` for '3|Bow lounge' and 'type:callhome';
    - `stayIn` for everyone, with shares .4 and .5;
    - `rush` for type:callhome, at [600, 1080] on the resolution day.
- `eventMod('needs', 'sleep' | 'social')`, for `crewNeeds` and `needsEst`.
- The party gathering in the event's moments: the bow lounge, day 3 at 19:00, for 120 minutes, who .7. Fill it from the deck architect's `gatherSpots('bow-lounge')` (0.38.0, `claude/decks-p3`). Venues are type 'event' places with `gather: '<venue>'`, in fill order: leads first, then their own room nearest, then the spill rooms.

The details are on that branch, in DEV_NOTES "Ship-wide events" → "The ion storm (0.34.8)".

How I'd fit them into section 14:
- **Gatherings:** `gatherings(p, d, F)` is the slot. Return `{ at, dur, where: [[deck, key]], tag }` entries for the person. `leisureUntil` already stops for them, as for section 18's `eventPlan`.
    - A gathering of 70+ needs every spot from `gatherSpots`. One way is a pool key per venue in `schedData`, as `'n|@<event>'` does for `event` places.
    - Hold the venue's spots in `occ.res`, as 0.26.12 does for event seats.
- **Rules:**
    - `closed`: drop the places in that room or type from `take`'s pools for the day (filter in `take`, by `pl.room` and `pl.type`).
    - `doubleShift`: lengthen `F.workEnd` in `schedFrame` for that department.
    - `stayIn`: weight `[bedDeck, 'rest']` up, by the share.
    - `rush`: pull the call-home special forward into the window.
- **Caches:** an event changes the plans of days already planned. Clear `SHIP_DAYS` and `SCHED_DATA` when the event starts or changes phase. Section 18 already clears them once at load.
- **Testing:** day_check on an event day (set `SHIP.event` by hand), dayReport over the event's days, and the draw calls at the party, which must stay under 450.

### Gotchas from this round

- **One-minute checks break when schedules move.** food_check's rush test once looked at the single minute 17:35, and the Deck 1 handover moved the queue by 10 minutes. When a check fails after a schedule change, compare with a copy that has the change switched off. If that copy is identical, the check is too narrow.
- **Merging the bridge architect's branch:** keep section 14's `EVENT_ONLY` line in `schedData`, not their `!p.event` or `p.type !== 'event'` filter. Theirs also hides the event places from the per-event lists.
- **Running checks in parallel times out.** machine_check and the scratch tests fail to load when three browsers run at once. Run at most two together, and rerun a "failed to start" alone.
- **edgeBlocks (section 4) runs at load**, before section 10's helpers exist, so it works out the edge's tiles inline rather than calling `edgeTiles`.

### Seating by friendship (asked by the social engineer after the handover)

The social engineer (session_01DzZ669spGpdSdVMYzUog2N, section 20, `claude/social`) has two affinity functions:
- `affinity(a, b)` is live. It drifts each hour from the plans, so section 14 must not plan from it: that would be a loop.
- `affStart(p, q)` is pure. It comes from roster data and a seed only.

My answer to them:
- **Seat from `affStart`,** through an `affinityPlan(a, b, d)` they'll provide.
- **A weekly snapshot is unsafe,** because days get planned before their first hour runs and are re-planned after a reload. That happens through tomorrow's `shiftBlocks`, the sleep skips, the week-back needs, and day_check planning d+3 first.
- **Where it goes:** in `take()`'s loop over `pool`, for mess-seat and lounge-seat only.
    - First, seats within about 2 tiles of an already-planned person with affinity ≥ 30.
    - Skip seats next to anyone at ≤ −30.
    - `occ` must then store who holds a place: `[from, to, personId]`. `isFree` reads only the first two fields, so that's compatible.

## Update at 0.26.18 (the second sim engineer)

The "Loose ends with guests", "Still to do: event routines (C7)" and "Seating by friendship" items above are **done**. Details in DEV_NOTES: "Pillar 3: guests", "Pillar 3: event routines" and "Seating by friendship"; build rows 0.26.15–0.26.18.

- **Guests (0.26.15, 0.26.17):** `guestStay(p, d)` (days of the year; event guests via section 18's `eventGuestDays`); `GUEST_TEMPLATES` drive free time and hours; survivors use the ward's `patient-bed` places (deck architect 0.38.4) when present.
- **Event routines (0.26.16, 0.26.17):** `evDay(d)` slots from `eventRoutines(t)` and `eventMod('needs', …)`; doubleShift (day to 20:30, night to 07:15: shared desks), patrol, closed (room keys like '3|L'), stayIn, rush (`callOwed`). The party comes only through section 18's `eventPlan` (one path, the lead's decision); section 14 fills `gather` pools from the front and plans an event's host first. `doorOpenFor` also honours `occasionDoorOpen`.
- **Seating (0.26.18):** `seatMates` / `seatNear` with `affinityPlan`; `occ` entries `[from, to, personId]`, `occ.who`.
- **Testing tips:** a storm starts on its own in a new game on day 10 (party day 13), so day_check 12 and 13 are the storm days. Give each concurrently running check its own copy of the build (the checks copy to `_run_<name>.html`; same names collide). Never `pkill -f` a pattern that appears in your own command line, and `cd` inside backgrounded chains applies only to that chain.
- **Next likely work (lead):** the diplomatic visit (event guests arrive through `eventGuestDays`; delegates' `formal` dinners via `eventPlan`), and tuning after the user plays the check-in build.
