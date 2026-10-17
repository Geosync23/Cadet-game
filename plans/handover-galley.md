# Handover: the galley (Pillar 2, A4, and the galley side of B3)

Written 2026-10-16 by the galley engineer, at combined build 0.40.8 (claude/ship-integration 980e6a9). Read with DEV_NOTES.md, "Galley and food (section 16)", which has the full detail. This page is the short version: what's there, what to watch out for, what's next.

## Role, branch, files

- **Role:** galley engineer. Food and cooking, simulated: the galley rota, the cold store, cooking, the servery, the grab-and-go shelf, plates, queues, and the galley's half of food restocking by hover cart.
- **Branch:** `claude/galley-food`. **Builds:** 0.29.x (0.29.0 to 0.29.10).
- **In the game file:** section 16, `// 16. GALLEY & FOOD`, after section 14 and before section 17. Plus one line in the main loop: `galleyTick();` after `tickShip(dt);`.
- **Test script:** `food_check.py` (mine). The others I run every turn: cadet_test, deck_check, day_check, player_check, machine_check.

## What's built

1. **The rota.** `galleyDay(person, day)` gives a galley worker's day, or null for anyone else. The roles come from ROSTER's `rota.team` (chef, early, late) and `rota.cover` (the deputy).
   - **Chef Brennan:** up about 04:30, cooks 04:50–08:00, eats 08:00, cleans to 09:30, free to 14:30, cooks to 20:30 (eats at 16:30), tea on her stool.
   - **Her deputy (Dlamini):** cooks on Fridays and Saturdays.
   - **Early hands:** 05:30–13:30. **Late hands:** 13:00–21:15.
   - The work is cut into 15–30 minute stints that move between the stations. No station is held by two people at once.
2. **The food (`SHIP.galley`),** worked out a ship minute at a time on any deck (`galleyStep`, `galleyAdvance`).
   - **Cold store:** 300 meals.
   - **Cooking:** pots of 10 portions, 20 minutes each, cooked only to what the crew's plans still need; trays of 8 for the grab shelf.
   - **Eating:** the crew take a portion 2 minutes into their queue stop.
   - **Plates:** 110 aboard; they come back when the meal ends and are washed at 3 a minute.
   - **Leftovers** go to the grab shelf at 08:30 and 20:45.
   - **Waiting:** anyone who finds nothing waits, and gives up 30 minutes after the line closes.
   - **Deliveries:** the cold store is fed only by hover cart (`FOOD.restock = 'carts'`).
3. **On Deck 3 (`galleyShow`).** Four instanced meshes, no shadows, never tapped, at most 4 draw calls:
   - food rising and falling in the servery's five pans, with steel covers when they're empty;
   - dirty plates stacking in the dish-pit sink;
   - rolls and wraps on the grab shelf.

## Functions other sections rely on

| Function | Used by | Returns / does |
| --- | --- | --- |
| `galleyDay(p, d)` | section 14 (schedules) | `{ role, wake, bedBy, blocks: [{ from, to, placeId, task }], meals }`, in minutes of the day; null for non-galley staff |
| `galleyHold(p, t)` | section 10 (CrewAgent) | where someone waiting for food stands: `3-queue-1..4` in waiting order, then null; undefined if they aren't waiting |
| `takePortion(who)` | section 15 (player) | true or false: a hot portion and a plate, else a grab item |
| `galleyJoin(who)`, `galleyTurn(who)` | section 15 | the player queues at tile [33, 2]; `turnAt` is a minute plus about 45 s per person ahead |
| `galleyText(what)` | section 15 | tap text for `'servery'`, `'grab'`, `'dish'`, `'cold'`. "Closed..." means the line is shut |
| `galleyCooks(t)` | section 17 (oven wear) | how many are cooking or baking at minute t |
| `galleyShelfRows(g, ys)` | grab-shelf kit (4b) | a function DECLARATION, so it exists when Deck 3 is built at load |
| `galleySave()`, `galleyLoad(o)` | the save, via `SAVE_EXTRA` / `SAVED.galley` | SHIP.galley as plain JSON, and back |
| `galleyReport(day, days)` | food_check.py | days replayed from a fresh galley, with each day's figures |

Section 16 itself calls `cartClaim(t, cold, { replay })` (section 17) on the hour, and `shipEffectsAt(3, m).cook` for oven speed.

## State at 0.40.8

- Everything in the brief is done and tested. Nothing is open.
- **Weak spots and next fixes:**
  - **Serving isn't modelled.** The servery is self-serve, so the hand at the pass is for show.
  - **Prep and clean are for show too.** They don't change cooking.
  - **Grab items never go stale.**
  - **No spoilage.** Section 17 offers `shipEffectsAt(3, t).spoil` from the cold store's chiller, and it's unused. Spoilage would be a small per-day loss in `galleyStep`.
  - **One dish per meal per weekday (`MENU`).** There are no favourites or variety.
  - **Waits only happen when something breaks** (an empty cold store, a slow oven), because the cooks cook to the plans' numbers. That's on purpose, but you rarely see a queue.
  - **The player's queue spot is a fixed tile, [33, 2].** If Deck 3's furniture moves, check that it's still free (food_check checks it).
  - **The DEV_NOTES build table** has my rows in two places after the merges, so it could use a tidy.

## The answers pass (2026-10-16 night, builds 0.29.11–0.29.17)

All four of the galley's rows are built and shipped in combined 0.41.4 (claude/ship-integration c7598df). Details are in DEV_NOTES, section 16.

- **Spoilage (row 7):** reads section 17's `chillerAt(t).spoil` (the share lost per hour), else `shipEffectsAt(3, t).spoil`. The 09:00 and 21:00 checks bin the spoiled food (bags by the dish pit) and send Mail.
- **Menus (row 10):** `galleyMenu(day)`: a weekly cycle, a crew favourite on Wednesdays, a Friday treat with a pudding, and a Sunday dinner voted for by the crew. Shown on the menu board's canvas and in its tap text. A harvest morning (section 18) adds a garden salad.
- **Queues (row 11):** `galleyBusy(day)`: a rush after the 17:00 shift change, and the odd slow oven. Waits stay within 25 minutes, only inside those windows.
- **Cakes (row 17):** `galleyCake(day)`: ROSTER birthdays (the player's too), or section 18 events with `cake: true` (Founding Day). Baked at 15:00, on the servery from 19:30 to 21:30, with a noon Mail that gives the gathering time. There's one cake a day, the galley's; section 18 hides its own when ours is out.
- **Your cart run:** carts are `[arriveAt, meals, hour]`. While section 17's `cartWaiting(hour)` is true (the run is claimed by 'you'), the meals wait. `galleyCartLand(hour)` lands them when you unload; a second call for the same hour returns 0.
- **Who counts meals on their way:** only the galley (the lead's decision). When it asks `cartClaim`, it passes the cold store plus everything in `S.carts`. Without that, a held run set off a new run every hour (0.29.17). Section 17 takes that figure as given (0.33.22).
- **food_check's live-vs-report test** runs with `cartWaiting` off, because the test doesn't run the job list.
- **Still open on other sections:** crew don't claim meals runs (the systems engineer's). player_check had pre-existing failures on 0.41.4 (grab, sitting, the stores cart run; the player and systems engineers').

## Pillar 3 and the working garden (builds 0.29.18–0.29.25)

The full detail is in the DEV_NOTES build table, rows 0.29.18 to 0.29.25.

- **Event hooks (C7).** Once an hour the galley reads section 18's `eventMod('galley', key, t)` into `S.ev` (it uses `eventModAt` first if that exists). Keys:
  - `menu`: a dish id from `GALLEY_EV_DISH`, or a dish name.
  - `cook`, `grab`, `extra`: multipliers and extra portions.
  - `batch`: a number or `{ meals, label, at }`, a dinner away from the mess, from 15:00.
  - `trays`: trays for the bridge at 18:00, sent through section 17's `cartTrays`.
  - `herbs`: the batch takes 4 units of garden herbs.
- **Threads scored** (live only, once per minute per thread, through `galleyScore`):
  - `spoiled`: meals binned while an event runs.
  - `bridgeHungry`: hours from 12:00 until `traysArrivedAt` says the trays reached the bridge (stops at 18:00 without it).
  - `dinnersLate`: minutes a batch is late (150 minutes of cooking from 15:00, longer with worn ovens).
  - `noHerbs`: a batch cooked without herbs.
- **Test stand-ins.** `GALLEY_TEST` holds them: eventMod, cartTrays, traysArrivedAt, gardenAt, gardenDay, gardenCrew, gardenCarry, carryWaiting. Use it instead of reassigning other sections' functions, because some of those are consts.
- **The garden.**
  - Crops: `GARDEN_CROPS` (greens, herbs, beans, tomatoes, roots). Growth: `gardenCond(d)`, which is water × feed × light from section 17's `gardenAt` times tending hours from section 14's `gardenDay`.
  - Picking: at 10:45 if `gardenCrew(d)` has someone on duty; harvest mornings pick everything ripe at 11:30.
  - Carrying: each pick becomes one section 17 `gardenCarry` job. The crates are held while `carryWaiting` is true, and `galleyCarryLand(id)` lands them when the player unloads.
  - Storage and cooking: produce sits in `S.cold.produce` and is used first, up to half of each pot. Cart claims count it.
  - Mail and texts: a thin harvest sends a Mail; `galleyText('garden')`; fresh-produce lines at the servery and on the menu board.
  - Numbers: about 28 meal units a day with the machines as new, about 23 with the real machines' wear.
- **The other sections' garden pieces:** systems 0.33.34 (gardenAt, gardenCarry, growlights), the deck architect's 0.38.6 (3-gardenwork-1..5, 3-crates-1), the crew designer's 0.16.11 (three gardeners), sim 0.26.20 (gardenDay, gardenCrew).
- **Possible next steps:**
  - a garden view (crops on the beds), with the performance engineer;
  - wiring galleyText('garden') to a tap in the garden (the player engineer);
  - tuning yields once the user has played it.

## Gotchas

- **`InstancedMesh.setColorAt` in r128** sizes the colour buffer from the mesh's *current* `count`. Set the colours before setting `count = 0`, or every instance is black (the fix in 0.29.0).
- **Coplanar faces.** The pans' food top is at y .98. Food mounds start at .978 and are at least .008 tall; covers span .972 to .988; plates start at .914 in a sink whose top is .91.
- **Merge traps.**
  - Section 16's comment rules (`// ====`) end in `=======`. A merge script that splits conflicts on the first `=======` cuts there. Split only on whole lines (`^=======$`).
  - Sections 16 and 17 both sit after 14; keep 16 first.
  - Merges usually conflict only on the header build line and `GAME_BUILD`.
- **The old hook shape broke things.** `galleyShift` (removed in 0.29.4) made 0.26.1's planner miss staff dinners. The planner reads `galleyDay` only.
- **Stale state.** `galleyHold` must call `galleyAdvance(t)` first: tests step time without drawing, and the galley only advances on drawn frames. Without it, three waiters once shared one queue spot.
- **Determinism.**
  - Replays (`galleyReport`) start from a fresh state and must never touch live state.
  - `cartClaim` is passed `{ replay: true }` in replays.
  - The rota and `galleyCooks` must never read the machine effects, because oven wear reads them and that would be a loop.
- **The events cursor.** `E.k` is shared between the live galley and the report. It resets when time goes back, and galleyReport resets it.
- **Tuning numbers.**
  - `FOOD`: pot size and time, hot line 50, grab shelf 16, cold store 300, plates 110, wash rate 3, how far ahead of a meal cooking starts (70 min), closing times, slack.
  - `GALLEY_SHIFTS`: the shift times. `GALLEY_AT`: the stations. `MENU`: the dishes.
  - Section 17's `cartClaim`: carts set off from 09:00 when under 250, urgently when under 90; at most 150 a run.

## Testing

`python3 food_check.py BUILD.html [DAY] [DAYS]` (defaults 1 and 7; about 2 minutes). Good looks like:

- Each day: food ready at 06:00 (about 30 portions) and at 17:00 (38–50); nobody waits; everyone who comes to eat gets food (about 150 a day); no dirty plates or plates out at midnight; the cold store never runs dry (it dips to about 134–150).
- The same days twice; the live galley matches the report; no station double-booked; galley staff at the rota's stations: all.
- On Deck 3: pans, covers and the grab shelf follow the numbers; draw calls under 450.
- Carts: a week fed only by cart with no shortage, and with no carts on days 2 and 3 the store runs dry at day 3's dinner.
- With an empty cold store: about 11 people wait, the first 4 in distinct queue places.
- The player's queue and `takePortion` work, and save and load work.
- It prints "Food reaches the cold store by: hover cart only (cartClaim)".

Also run cadet_test (Deck 4 must stay identical), deck_check, day_check (Deck 3 peak about 388), player_check and machine_check. Run them one after another: cadet_test and deck_check write the same temporary file name.

## Ideas and open questions for the user

- **Spoilage:** should food in the cold store spoil when its chiller falters? (Section 17 already provides the number.)
- **Menus:** favourites, Friday treats, or a crew vote on Sunday dinner?
- **A job for the player:** should the player be able to help in the galley (wash up, carry a crate), or is the galley crew-only?
- **Queues:** should queues happen more often? A slow oven or a big event (Envoy Saruth's formal dinner) would make the galley visibly busy.
- **The grab shelf:** should it empty overnight (stale food binned), so the morning bake matters?

## Pillar 4: the traditions' meals (builds 0.29.26–0.29.28, on 0.60.0)

Full detail in the DEV_NOTES build table, rows 0.29.26 to 0.29.28. All inert until the traditions engineer's ties (claude/ship-events 0.34.29+) are combined; food_check stands in with `GALLEY_TEST.tradTies`.

- **`galleyTies(d)`** folds section 18's `tradTies('galley', d)` by meal: `{ breakfast?, dinner? }`, each `{ ids, dish, until, side, extra, batch, honorees, taste }`.
- **Long breakfast:** `until: '10:00'` -> `galleyServeEnd(d, meal)` and `galleyClose(d, meal)` replace the fixed 08:00/08:30; `galleyPlan(role, d)` keeps the chef and early hand on. Pancakes on Saturday (Tuesday got the spiced beans).
- **Suppers:** first fruits on the tables; the harvest supper all from the garden, with a pie (`galleyCake(d).pie`); a farewell supper serves the first honoree's favourite. A cake whose tradition has decor `cake` (four weeks aboard) isn't the galley's.
- **Tasting table:** the vote is section 18's tally (`tallyOf`, `tallyVote`; one vote engine, the lead's ruling in 0.29.29). `galleyTasting(d)` cooks and serves (the tasters from the plans' `ev-<id>` segments) and reads the tally; `galleyVote(choice)` is a thin call to `tallyVote`. 20 tastes, two each; Sunday's `side: 'tasting'` gets the winner. Two small plates on the tray slide.
- **0.29.29 also:** `galleyFresh()` clears the day caches when `evSig()` changes; `galleyBirthdays` uses schedPeople + aboard() + birthdayOf; lateMeal has `dish`; the crossover supper's note.
- **Late meals:** `simNote('lateMeal', { who, meal, late, how, deck: 3 })`, live only, once per person and meal a day (`galleyLate`, `galleyLateBy`, `LATE_WAIT`).
- **Waiting on:** the sim engineer (do meal-tradition segments keep act 'dinner'/'breakfast'? if so the galley feeds them unchanged). The dialogue engineer agreed the lateMeal payload (+ dish); writers' cue keys `cue:lateMeal`, `cue:lateMeal.you`. Head writer 2 is session_01HNrh3xCtczeZM5NVFrE6pa.
- **Trial merges** with claude/ship-events conflict only on the header build line and `GAME_BUILD`.
- **Tests:** needs `pip install playwright`, three r128 in /tmp/cadet-work/three (see cadet_test.py's header), and `CADET_CHROME=/opt/pw-browsers/chromium`.

## The food queue (builds 0.29.31-0.29.32, on 0.60.2)

- **The user's report (0.60.1):** too slow, and a queue number that wasn't real. Fixed: "ahead" is the people really in the line; serving pace `GALLEY_SERVE` (0.6 ship min a person, a minute in a rush, yours a minute after the last ahead). No numbers on screen anywhere (sections 15 and 19 removed theirs).
- **The live line is section 10's** (sim engineer 3, 0.26.30: `servLine`, `lineJoin`, `lineSpot`, `lineFront`, `lineLeave`); section 15 (player engineer 4, 0.28.34+) walks you up it. Section 16 gives `galleyServeMins(t)`, `galleyCanServe(t)`, `galleyLeave(who)`; `galleyJoin` / `galleyTurn` / `takePortion` use the line when it exists. Both section 15 and 16 call `lineJoin`/`lineLeave` for the player (idempotent); the reviewer asked the lead to name one owner.
- **Open:** the tasting table has 25 tasters now and 20 tastes at two each (about 10 get one): ask whether it should be one each, or a bigger batch. The welcome tea for new crew (traditions engineer 2, 234a454) will get `cake: true`; next build: put a mess gathering's cake out at its start when that's before 19:30. galleyFresh misses one-off events and tradition flags (reviewer's low note).
- **Latest:** see the DEV_NOTES build table's last galley row for the hash and tests.
