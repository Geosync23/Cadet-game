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
