# Handover: the sim engineer

Written at build 0.40.8, brought up to date at 0.26.18, 0.26.31 and 0.26.37 (sim engineer 4: see the first "Start here") (Pillar 3, 16 October, by the second sim engineer, session_01R6RBwwBM9aorpsqDCrztDU), so a fresh session can take over. **Start with the Pillar 3 section at the end:** it has the work in progress. The detailed notes are in DEV_NOTES.md, in four sections: "Ship time and saving", "Schedules", "Crew on the deck" and "Every room in use". This page is the short version, plus the things that only live in my head.


## Start here: 0.26.32 to 0.26.37 (sim engineer 4, session_01EJUGywZv9BpcUezjXES9AC, 17 October)

Read this first, then sim engineer 3's section below it. **Builds on `claude/sim-engineer`:** 0.26.32 f9a145c, 0.26.33 7a11c73 (+6e87e6b row), 0.26.34 236810f, 0.26.35 7c1feea, then 0.26.36 and 0.26.37 (see DEV_NOTES' rows for their hashes and tests). Same ownership: sections 10, 13, 14, 17, `day_check.py`, `machine_check.py`. Lead session_01KPJMYjXAPkNUcrQ8VRkhLE (report only to it, by send_message); reviewer 1 session_018XY1NbMBxo2SLDPxooe5yx; build master 2 session_01F8ph7FKqViF3heRn94YgBr.
Read this first, then sim engineer 3's section below it. **Builds on `claude/sim-engineer`:** 0.26.32 f9a145c, 0.26.33 7a11c73 (+6e87e6b row), 0.26.34 236810f, 0.26.35 7c1feea (the Tern start: 0.60.4 only), 0.26.36 f16a110 + 0.26.37 e4d6ace (for 0.60.3, always together: 0.26.37 corrects 0.26.36). DEV_NOTES' rows have the tests. Same ownership: sections 10, 13, 14, 17, `day_check.py`, `machine_check.py`. Lead session_01KPJMYjXAPkNUcrQ8VRkhLE (report only to it, by send_message); reviewer 1 session_018XY1NbMBxo2SLDPxooe5yx; build master 2 session_01F8ph7FKqViF3heRn94YgBr.

### What I built (each has a DEV_NOTES row with its probes and tests)
- **0.26.32 (reviewer 1's 0.26.29 fixes):** named intro seats held in `occ.res` as `'intro:<id>'` before anyone is planned; the repair note's `t` is `Math.max(t, SIM_AT)` in the hour loop; a meal tradition's diners are planned right after hosts, then its seat holds are dropped (their bookings keep their seats); `trayLate` (served early into a full mess: no tray till seated).
- **0.26.33:** someone in the food line leaves it `LINE_LATE` after their plan has moved on (an empty galley serves nobody), counted in `LINE_LOG.left`.
- **0.26.34:** `lineCatchUp` (a deck entered mid-meal plays the line forward: served, waiting, or partway); lift arrivals mid-meal go through the line (no tray outside the mess); an appointment with `occ` (section 18 occasions via section 19's apptAdd) keeps its host the whole `len`; `Number.isFinite` for a note's `t`.
- **0.26.35:** `SHIP_START_ARRIVAL` = 5-tern-aisle-1 [5, 7], face 0. Only with decks-p3's walkable Tern and onboarding's INTRO_START move (0.60.4). day_check prints where leavers wait in the bay.
- **0.26.36 (blocks 0.60.3):** the cook steps aside. `sharedTile(t)` (a walk tile two places share, e.g. 3-galley-2 on 3-range-1's panel [39,4]); `occupiedBy(player)` ignores crew settled on one; crew whose place is on the tile you're heading for (`player.goal`) or using (`PLAYER_PLACE`) step beside it (`asideTile`, goal '@aside') and go back after. `crewMakeWay(tile, mins)` -> release() for any other tile (player 0.28.40 uses it as a fallback).
- **0.26.37 (blocks 0.60.3):** introLay's `free()` also refuses `occ.res` holds for someone else or an event, and no fallback to the named place when no alt is free (Torres took Calder's 3-mess-9).
- **0.26.36 + 0.26.37 (0.60.3):** the cook steps aside. `sharedTile(t)` (a walk tile two places share, e.g. 3-galley-2 on 3-range-1's panel [39,4]; Deck 3 has 27, most of them seat pairs); the player's `goTo` frees its goal tile when it's shared and no other walker is on or heading for it (passing through, you still squeeze past); crew standing at their place (`spot.onTile`) on the tile you're heading for (`player.goal`) or using (`PLAYER_PLACE`) step beside it (`asideTile`, goal '@aside') and go back after. Seated diners never get up for it. `crewMakeWay(tile, mins)` -> release() for any other tile (player 0.28.40 uses it as a fallback).
- **0.26.37 also:** introLay's `free()` also refuses `occ.res` holds for someone else or an event, and no fallback to the named place when no alt is free (Torres took Calder's 3-mess-9).
- Answered (no code): night-shift honorees already get their events since 0.26.31 (traditions engineer 2 was on an older base).

### Loose ends and asks waiting
- **FIRST (the lead, for 0.60.4): a time jump sends notes that hour-by-hour never sends (section 17).** Social A traced it: from the arrival, a 2-day jump's job pass sends 4 extra notes, all stamped 2460 (the jump's last hour): jobUnclaimed for 3-growlight-2@26, 3-oven-1@21, 4-washer-2@12, and repair 3-range-1@18. A jump must give the same notes as stepping hour by hour. Reproduce (about a minute): social A's social_check 8c9b52f `--long` on a merge of claude/social 0.36.78 + social-stories 7d8be10 + this branch; the arrival-jump line prints the differing notes. Look at machinesNow's catch-up job pass at the end of a skip (jobs posted or claimed in the last hour of the jump, and `SIM_AT` stamping).
- **After 0.60.4: garbage per frame (the performance engineer, session_01XAkY9U3mmstHQT2yAMTocA).** At Sunday dinner the game makes about 183 KB a frame, behind most of the remaining slow frames. Section 10's `crewNearDoor` is about 40 KB a frame: every door checks every crew member every frame, and `d.rooms.some(rm => a.rooms.has(rm))` makes a closure each time. Fix, same behaviour: once a frame, collect the unsettled crew and their x/z into a reused array, then a plain loop instead of the closure. updateDeckCrew and CrewAgent.update add about 15 KB (for...of over Sets/Maps, Set.add). Section 14's `whereIs` and `shipDay` add about 15 KB a frame: cache whereIs per person per ship minute (cleared when the minute changes). They're pure for a person and minute, but check that the jobs, appointments, escorts and visits that whereIs asks first are covered. The performance engineer has alloc.py (CDP HeapProfiler sampling over 1,500 frames) and will re-measure a fix.
- **Social B2's farewell friends** (session_014A3w2gK8FBNWs66YC3LfME): plan `farewellCrew(leaver, d)` to the shuttle bay 14:30-15:00. Written but **not pushed or tested** in my scratch `b34.html`: a `'@gather-<venue>'` pool in schedData (crowd places' `gather`), a `farewell` gathering in `gatherings()`, and the leavers' own bay spots held in occ.res (`'leave:<id>'`). Redo it on the current head; test with day_check 35 on a merge with claude/social-stories. Couples side by side at gatherings: not started.
- **Long-table check** (the lead): traditions 0.34.49 + decks 0.38.23 (14 seats, trestle tiles blocked while the decor is out). Confirm nobody paths through the blocked tiles and no seat is used twice on Sunday-table / harvest days (dayReport's double list, and a walk probe).
- **Social A's purity failure** ('affBand, moodOf or purity wrong'): rerun social_check 6353c2d on sim + ship-events + social and send the FAIL line to social A (session_012pK2XVi5UhqEd28fakYk68). They couldn't reproduce it.
- **Reviewer 1's open should-fix:** breakfast tray returns make about 36 crew up to 6 min late for the lift; the plan doesn't time the walk to the tray return (changing it moves every day's plans). Lows: per-frame string building in mealStep/lineTick; a crewHold on someone in the line blocks the counter.
- **Day 231** store-till double booking: still not reproduced; check on the next combine. **2.9 ms recheck:** the performance engineer was asked to recheck on a combine with 0.26.34.

### Gotchas from this round
- `pkill -f name` kills your own shell if the name is in its command line: use `ps aux | grep -E "[n]ame" | awk '{print $2}' | xargs -r kill`.
- player_check (and events_check) find cadet_test.py from their own file name: run a peer's copy as `player_check.py` in a folder that also has `cadet_test.py`.
- A test hook's `var` (window.__sc's eval) is declared in the eval's own scope, so it can't stand in for a game function; assign to an existing binding instead (e.g. `lineTick = () => {}`).
- cadet_test once showed 1-level pixel noise on every shot (even crew-off); a rerun was identical. Rerun before chasing it.
- Merges: in this period the only conflicts with peers were the build lines; resolving every conflict to my side is only safe after checking that.

## Start here: 0.26.30 and 0.26.31 (sim engineer 3, session_01517opwS4UAxYZKNwJytaEK, 17 October)

Read this first, then sim engineer 2's section below it. **Last build: 0.26.31 (bfcd864) on `claude/sim-engineer`.** You own sections 10, 13, 14 and 17, plus `day_check.py` and `machine_check.py`. The lead is session_01KPJMYjXAPkNUcrQ8VRkhLE (report to it only, by send_message; never the user). Reviewer 1b (session_018XY1NbMBxo2SLDPxooe5yx) reviews each build. Push only to `claude/sim-engineer`; never merge `claude/ship-systems`.

### What I built (DEV_NOTES rows 0.26.30 and 0.26.31 have the details and test numbers)
- **The real food line (section 10).**
  - `LINE`: who stands in it, front first. Crew ids, and 'player' when section 15 joins. Crew join on reaching its back.
  - Spots `LINE_AT`, front first: (33,6) = 3-queue-4 at the servery's south end, up column 33 to 3-queue-1, then (32,3), then west along the row-2 aisle. 15 spots; past them, stand where you are.
  - `lineTick` serves the first `LINE_COUNTER` (1) after `galleyServeMins(t)` (section 16, galley 3: 0.6, or 1 in a rush; fallback `LINE_SERVE` 0.6) when `galleyCanServe(t)`. 'player' at the front is skipped: galley 3's `galleyTurn`/`takePortion` serve you and call `lineLeave('player')`.
  - API (agreed with galley 3, session_018cicfPQZQXbxmtn6ygmL84, and player 3, session_016EJg9DempByUCWwpszyWmV): `servLine()`, `lineJoin(id)`, `lineLeave(id)`, `lineSpot(id)` -> `{ x, z, face (radians), at, front }` or null, `lineFront(id)`.
  - Galley 3's 0.29.31/32 (`claude/galley-food`) uses them, and its galleyTick drops 'player' from LINE when section 15 isn't queueing. Player 3's a2fe957 (`claude/player-needs`) follows lineSpot. Neither has been trial-merged with mine by me: the lead / build master combine them.
- **Trays (section 10, `CrewAgent.mealStep`, `served`, `trayBack`).**
  - A tray is handed over at the counter, only if the next seat is in the mess hall (`trayTo`).
  - After the meal, the tray goes to the tray return (`TRAY_AT` [33,2]/[33,1], by idHash), dropped on arrival. No waiting spots; crew pass through each other.
  - While carrying one in the mess hall, the path avoids every non-mess tile (`messOnly()`).
  - Anyone already in the line stays until served. Anyone on the way when the meal's time ends keeps going for `LINE_LATE` (12) minutes.
  - `withHold` (14) no longer plans trays. Crew no longer use `galleyHold`.
  - Meal traditions (act dinner at a seat, tag ev-<id>, no queue) get no line and no tray.
- **Planned walk (section 14, schedBuild's `meal()`).** A sit-down meal starts with a placeless segment, tag 'queue', the walk to the line: `LINE_WALK` = 4 min + 0.55 per manhattan tile from the last place on Deck 3 (or the lift) to (33,4). Then the queue stop, only if free at once (a wait would split the meal into two for the galley's counting). Then the seat. Grab-and-go when under 15 + walk minutes are left. Result: diners sit on time (median 0). Grab-and-go is 15-21 a day (was 7-15).
- **Someone in your seat (section 10, `elsewhere`).** If you or a settled crew member is in someone's mess seat, lounge seat or bench (`ALT_SEAT`), they take the nearest free one of that kind (`seatsBeside`), kept while their plan's place stays the same. A visit arrives there too.
- **`crewHold(p, placeId)` (10)** keeps someone put whatever their plan says (for Tiles' opponent). It returns a release function and is cleared with the deck. The Tiles session hasn't been told directly: the lead was asked to pass it on.
- **Section 17, day 0:**
  - `machUse`, `choresHour` and `cartClaim` used `h % 24`, which is negative on day 0, so the arrival's wear was NaN and 40 machines read broken. Now `(h % 24 + 24) % 24`.
  - `machinesNew()`, called from `newGameStart` before `introNewGame`, resets machines and jobs at once.
- **Gatherings for night workers (14).** `gatherings` returned nothing for anyone on a night shift tonight. Now they get section 18's events (eventFree keeps them clear of the shift), but not Deck 1's routines.
- **day_check** has a servery-line line per deck, and fails on: a tray outside the mess hall, standing still a ship minute with a tray, anyone giving up on the line, a walk back with a tray over 12 minutes.

### Loose ends and asks waiting
- **Onboarding** (session_01KaHzfqSqF8B4bkNFrH1tsx): `SHIP_START_ARRIVAL` should start at place 5-tern-aisle-1 once the deck architect's bigger Tern lands; they'll send the tile.
- **Tradition capacity:** the mess hall's 44 seats cap the Sunday table (up to 50 want) and harvest supper (57 want). A deck architect or traditions call; told the lead.
- **Section 20 (social A)** uses `h % 24` too (around lines 15551-15663), so day-0 hourly checks never match. Told the lead.
- **Day 231 store-till double booking:** not reproduced on a trial merge with ship-events f4adcde (dayReport(231) clean). If events_check on the integration build still shows it, run it there and trace with planDay for 3-store-1 14:30.
- **The performance engineer** (session_01XAkY9U3mmstHQT2yAMTocA) saw 2.9 ms game code per frame once at Sunday dinner (was 1.4). They're rechecking on the combined build. If it's real, look at `lineTick`/`mealStep`: `whereIs` per agent per frame, plus `seatsBeside` when someone's seat is taken.
- **Seated diners show no tray on the table:** the crowd draws held props only when standing or walking. That's the performance engineer's, if the user wants it.

### Gotchas from this round
- The order in `CrewAgent.update` matters. mealStep's goal first, then the seat-taken check (`elsewhere`), then `crewHold`, then retarget. When the seat check ran before mealStep, served diners walked into seats still in use.
- `lineSeg(w)` is any meal segment with type servery-queue or tag 'queue' (the walk-in has no place).
- Identity test for a plan change: a copy with `LINE_WALK = [0, 0, ...]` and the grab rule back at 18 was ALL IDENTICAL to 0.26.29. Use the same trick (switch the change off in a copy) for any crew difference.
- events_check must run from the repo folder (it builds cadet_test's path from its own name), so copy builds into that folder.

## Start here: 0.26.19 to 0.26.29 (the second sim engineer, session_01R6RBwwBM9aorpsqDCrztDU, 17 October)

The rest of this note (below) was written at 0.26.18 and still holds. This part is what changed since, for **sim engineer 3** (session_01517opwS4UAxYZKNwJytaEK). The last build is **0.26.29 (a7673e0)**. I'm on call for questions until I'm archived.

**You now own section 17 as well** (machines, jobs, parts, washers): the systems engineer retired; read `plans/handover-systems.md`. So: sections 10, 13, 14, 17, plus `day_check.py` and `machine_check.py`.

### What I built (all in DEV_NOTES' build table, 0.26.19 to 0.26.29)
- **The notes bus and flags (section 13, Pillar 4).**
  - Functions: `simNote(kind, data)`, `onSim(kind, fn)` (returns an unsubscribe function), `simNotes(kind, since)`, `flag(key)`, `flagSet(key, v)` (null clears).
  - Saved as `save.notes` and `save.flags`.
  - A note's data is deep-copied through JSON; a note that can't be copied is dropped.
  - **Contract:** a payload never has its own `kind` (the note's kind wins). A number `t` is when it happened, and the ring is kept in time order.
  - Section 17 queues its notes with `simLater` and flushes them with `simFlush`. During the hour loop `SIM_AT = MACH_HOUR * 60` stamps each note with its hour.
  - The repair note is `{ who, machine, state, job (service | repair | overhaul), deck, id, t }`; the job note carries `job` too.
  - `skipTo` runs `machinesNow()` before the SIM_ADVANCE listeners, so section 17's notes are queued before social A's `socialTo` catches up.
- **Day 0 and the arrival (sections 13, 10, 14; with onboarding, section 21).**
  - `SHIP_START_ARRIVAL` and `newGameStart(arrival)`. The New game button offers Monday or the arrival.
  - Section 21 boots the first launch from its own first frame (the lead's decision: the TDZ at load).
  - `introPlan` / `introLay` lay section 21's `introBeats` over the plans:
    - a named seat (`where.placeId`) starts `INTRO_EARLY` = 5 minutes early (Calder at 3-mess-9 at 18:25);
    - a beat given by room or tile takes the first place nobody has then (`alts`, picked in introLay against occ).
  - The escort's lead / follow / wait is walker mode `escortPlan` (CrewAgent.escortStep, ESC_WAIT/GO/NEAR). Visits are `crewComeTo(p, placeId, onArrive, { until })`.
  - `shiftTick` sends `simNote('shiftStart', { late })` once a day (flag 'shiftSent'). Also `apptKept` / `apptMissed`.
- **Crew coming and going.**
  - `crewStay` / `crewLeaving` / `crewArriving` / `crewState` come from the crew designer's `aboard: [from, to]`. ROSTER_RESERVE entries carry `replaces`.
  - Leavers are off at `ROTA_OFF` 15:00 and wait in the shuttle bay from 14:30 (`ROTA_WAIT`). They stay at social A's 14:00 farewell spot when they were there.
  - Arrivals come on at `ROTA_ON` 17:40 and take the leaver's bunk and desk.
  - Guests keep their own 10 minutes (`guestTrim`).
- **Seating by friendship:** `seatMates` / `affinityPlan`. **Event routines** (storms): `evDay` / `evRule`.
- **Gatherings:**
  - Hosts are planned first, 5 minutes early.
  - `clear(70)` keeps errands off a gathering, and dinner moves before or after one.
  - **Meal traditions** (section 18's `meal: 'dinner' | 'breakfast'`) *are* the meal:
    - an act 'dinner'/'breakfast' block at its seat, tag `ev-<id>` (the galley's portion rule needs no change);
    - shipDay holds as many of its seats as are coming (`occ.res`);
    - latecomers join while `min` minutes are left.
- **Small fixes:**
  - nobody lingers at a desk past their shift while the desk's other shift is on (`deskTwin`);
  - the bed check counts doubles by time on transfer days;
  - cadet_test hides `.nf` floats.

### Loose ends and asks waiting
- **Social B's idea (optional, not started):** couples share leisure places.
- **Galley 3** (session_018cicfPQZQXbxmtn6ygmL84) has my answers on meal-tradition segments and the long breakfast. MEALS stays 06:00-08:00 except for the tradition's diners.
- Onboarding: jobs reserved right after `newGameStart` are wiped when the machines restart on the clock rewind. Onboarding works round it by reserving at Monday 05:00. Worth a proper fix in section 17 someday.
- **social_check's time-jump test fails on this branch alone** (my branch has an older section 20). It passes on a full merge (social A, the build master).

### Gotchas
- `pgrep` / `pkill` match their own command line: use `ps` with `grep`.
- Run at most two browser checks at once. Give each copy of the build its own filename (copies collide as `_run_<name>.html`).
- When you resolve a trial merge, resolve hunk by hunk. `git checkout --theirs` takes the *whole file* and throws away the other side.
- Most other branches carry an older copy of sections 13/14/17. To test against a peer's data, trial-merge their branch into yours in a scratch worktree, not the other way round.
- On days off the crew take every job (`playerShiftOn`): a job test that lands on a weekend finds nothing for you.

### How to test
From a scratch folder, set `CADET_CHROME=/opt/pw-browsers/chromium`, then run:
- `cadet_test.py OLD.html NEW.html` (must be identical);
- `day_check.py B.html 1` and `day_check.py B.html 35` (day 35 is a crew-change Sunday; there's an arrival-on case for days 0 and 1);
- `machine_check.py`, `player_check.py`, `social_check.py` and `events_check.py`.
A plan-diff helper (load two builds and compare `JSON.stringify(planDay(p, d))` per person and day) shows exactly whose day changed.

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
