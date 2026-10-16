# Handover: the player engineer (needs, activities, device, the player's job loop)

Written 2026-10-16 at combined build 0.40.8 (`claude/ship-integration` 980e6a9), for a fresh session taking over this area. Read it with `DEV_NOTES.md` ("Player needs and the device"), `plans/pillar2-plan.md` and `design-doc.md` ("The player").

## Role

- **Who:** the player engineer, Pillar 2. Workstream A3 (the player's needs and activities, the walking-speed rule, the placeholder device), then the player's side of B2 (the job loop).
- **Branch:** `claude/player-needs`. **Builds:** 0.28.x (0.28.1 to 0.28.8). The lead merges them into `claude/ship-integration` (0.40.x).
- **Section of the game file:** `// 15. PLAYER NEEDS & DEVICE`, which sits after section 14 (like 13 and 14, not at the end of the file). Plus small hooks elsewhere, listed under "Hooks" below.
- **Test script:** `player_check.py` (mine). Run all six checks every turn: cadet_test, deck_check, day_check, food_check, machine_check and player_check.

## What's built

### Needs
- `SHIP.player.needs = { hunger, energy, hygiene, fitness, social }`, 0 to 100, 100 = fully met. The key list is `NEED_KEYS`; section 14 declares `NEEDS` with the same list, so don't redeclare that name. The device labels hunger "Food".
- **Drain** per ship hour, awake / asleep (`NEED_DRAIN`):
  - hunger 4 / 2
  - energy 3.75 / 0
  - hygiene 2.5 / 1
  - fitness 0.6 / 0.3
  - social 1 / 0.25
- **Sleep:** asleep, energy rises 12.5 an hour (`SLEEP_GAIN`).
- **Activity gains** (`PLAYER_ACTS`), spread over the activity's ship minutes:
  - a meal at a mess seat +55 in 20 minutes
  - the grab shelf +25 in 3
  - a shower +80 in 10
  - a workout +30 in 30
  - a call home +40 in 15
- **Starting values:** a new game 60 / 100 / 60 / 70 / 70; a `v: 1` save 80 each.
- **Walking speed (the user's rule):** fitness under 25 → 80%; energy under 25 → 80%; both → 64% (`SLOW_BELOW`, `SLOW_SPEED`, `playerSpeed()`). `playerUpdate` sets `player.maxV = PLAYER_V0 * playerSpeed()` each frame, so at full speed it's exactly the old number. Nothing else is ever punished.
- **Time:** `playerUpdate(dt, t)` (main loop) drains by ship minutes since the last frame. A time skip (`SIM_ADVANCE`) drains the gap at once:
  - asleep if you chose Sleep (`sleeping`, section 13), or for any skip starting at night (the debug Day button);
  - awake otherwise.
- **The machines' effect:** `shipEffects(deck)` (section 17) multiplies drains (`drain[k]`) and gains (`restore[k]`). It's read once a ship minute by `playerFx()`; skips use the pure `shipEffectsAt(deck, from)`, which never runs the machines. **`fx.walk` is deliberately ignored** (the user's rule: only fitness and energy slow you).

### Activities (tap the thing)
- The item tap in section 11 asks `playerTap(item, itemPos, tapPoint)` first.
  - `ACT_TAP` maps the item's title to place types and an activity.
  - It then picks the nearest free place of those types within `ACT_NEAR` (2.4 m) of the item.
  - No match → the tap does what it always did.
- **The activities:**
  - shower: public washrooms only; anything private, by room or by a bed's name, is left alone;
  - servery: the galley's queue (`galleyJoin` / `galleyTurn`), then a mess seat;
  - mess table: sit and eat;
  - grab shelf;
  - treadmill, weights, rower, mats;
  - call-home booths;
  - shop shelves, then the counter: browse, then pay. Shopping restores nothing yet.
- **How it plays:** you walk to the place's walk-to tile; a stand-in `FullPerson(PLAYER_SPEC)` slides onto the spot and takes the pose (`poseOf(place)` from section 8b when it's there); your Walker waits hidden on the walk-to tile. Walking away stops it and keeps what you gained.
- **Places crew hold** (`heldBy`: a crew agent's `goalId`) are left alone ("In use: …"). If someone gets there first, you move once to the next free place of that kind.
- **Food** goes through `foodFrom(where, peek)`:
  - with section 16: `takePortion('player')`, and `galleyText` for the dish and the "Closed" text;
  - without it: the meal windows.

### The device (a PLACEHOLDER)
- **The button:** Device, under the clock. It gets an amber dot when a need is under 25.
- **The panel:** `#device`. Sections come from `device.addSection(id, title, render)`, where `render(el)` fills a fresh `el` on opening and every ship minute while open. Also `device.open()`, `close()`, `refresh()`.
- **My sections:**
  - `now`: time and day; what you're doing or a status line (`needsLine()`); "Carrying: …"; your job's progress; the first two ship notes.
  - `needs`: five bars, plus "Walking at N% speed".
- **Other sections:** section 17 adds `jobs` (take it, drop it).
- The user is designing the real device: replace the panel, and keep the data and `addSection`.

### The player's job loop (B2)
1. **Take a job** on the device (section 17's Jobs section).
2. **Tap the machine** (anything near its panel place): you walk to `panelPlace(machine)`. Parts you carry are fitted. Then:
   - the first visit with parts missing is a 3-minute look over that says what's needed;
   - with every part in, you repair for `JOB_TYPES[kind].work × (1 + 0.25 × (tier − 1))` minutes;
   - when done, `finishJob(id)` puts the machine right.
3. **Fetch** (main storage, Deck 5, room `r`): you walk to the nearest free `5-parts-N` place, look for 4 minutes, then `takePart` each needed part. You carry two at most (`CARRY_MAX`), so a three-part job takes two trips.
4. **Make** (machine shop, room `f`): only when a needed part has `SHIP.stores[part]` at 0 and isn't in `NO_MAKE`. You walk to a free `5-make-N` place; it takes 60 minutes and the part goes into your hands. Stores are never written by me.
5. **Pausing:** walking away pauses repairing and making. Progress lives in `SHIP.player.work = { job, fitted: [...], done, seen, make: { part, done } | null }`, and `SHIP.player.carry = [...]`.
6. **Keeping the job:** `touchJob(id)` on progress keeps the job yours past the 12-hour lapse.
7. **Putting parts back:** with no job, a tap in storage puts carried parts back (`returnPart`).
8. **Notice:** when a job you could take is posted and you're free, a "Your device: New job: …" toast (`jobNotice`). Jobs posted during a skip aren't announced.
9. **The crate prop:** carrying shows a crate in your hands. `player.holding` makes `Walker.update` call `animateActivity(this, 'stand+carry')`.

### Saving
- `SAVE_V = 2`. `player.needs`, `player.carry` and `player.work` go in through `SAVE_EXTRA` (section 13); my hook creates `save.player` if it's missing.
- `loadGame` accepts `v: 1` and `v: 2`. `needsLoad`, `carryLoad` and `workLoad` read defensively (clamped, strings only, junk → defaults).
- New game calls `playerNew()`. `?nosave` neither reads nor writes.

### Hooks outside section 15
- **Section 13:**
  - `SAVE_V = 2` and `SAVE_EXTRA` (the systems engineer's lines, copied exactly);
  - `loadGame` takes `v: 1`;
  - `playerNew()` in New game.
- **Section 11:** one line at the top of the item tap: `if (playerTap(...)) return`.
- **Section 12:** `playerUpdate(dt, t)` after the walkers.
- **Section 10:** `Walker.update` uses `animateActivity` once `player.holding` has been set, otherwise `animateRig` as before.
- **The header and the HTML:** the file map line, and the device's HTML and CSS.

## Functions other sections rely on (or I rely on)
- **Mine, used by others:**
  - `device.addSection(id, title, render)` and `device.refresh()` (section 17's jobs section);
  - `playerHolds()`: the place you're using, or null (meant for the schedules; not wired by them yet);
  - `SHIP.player.needs`, `.carry`, `.work`.
- **Theirs, used by me** (all guarded with `typeof`, so section 15 runs without them):
  - section 16: `takePortion`, `galleyText`, `galleyJoin`, `galleyTurn`;
  - section 17: `shipEffects`, `shipEffectsAt`, `myJob`, `takePart`, `finishJob`, `touchJob`, `returnPart`, `panelPlace`, `machineById`, `jobTier`, `JOB_TYPES`, `jobsBoard`, `jobCard`, `PLAYER_TIER`, `ENGINE_KINDS`, `NO_MAKE`, `MACHINE_KINDS`, `SHIP.stores` (read only);
  - section 8b: `poseOf`, `animateActivity`, `FullPerson`;
  - section 10: `placeSpot`, `PLACE_OF`, `DECK_CREW`, `CREW_SPEED`, `FACE_ANGLE`.

## State at 0.40.8: loose ends and weak spots
- **Crew don't avoid your place.** A crew member can walk onto the treadmill you're on. `playerHolds()` exists for the sim engineer, but isn't used yet.
- **The shower pose is just `stand`.** No shower or washing pose exists.
- **Shopping restores nothing.** Items come later.
- **Grab-shelf taps can serve a hot portion.** `takePortion` gives the servery's portion first if there is one. A `takePortion(who, where)` from section 16 would fix it.
- **Activities run in real ship time** (no time controls, by the user's decision): a workout is about 37 s, a meal 25 s, a repair 25 to 112 s.
- **Activity choice depends on item titles** (`ACT_TAP` regexes such as `/^booth/i`, `/table/i`). Renaming an item in the deck dressing can break a tap. The place-proximity check stops false matches, but not missed ones.
- **Talking to crew doesn't raise social.** "Company can come later" (design).
- **The device is a placeholder.** It'll be redesigned.

## Things I'd fix next
1. Crew stepping around `playerHolds()`: the sim engineer's side; a one-line check in `planDay` / `CrewAgent`.
2. Social from company: eating near friends, or talking (once per person per day).
3. Item kinds instead of titles for `ACT_TAP` (needs `place()` to record the kit kind on items).

## Gotchas
- **Name clashes across sections break the whole merged build.** My `NEEDS` and `ACTS` collided with sections 14 and 8b; they're now `NEED_KEYS` and `PLAYER_ACTS`. Before a push, grep the other branches for any new top-level `const` or `function` name.
- **Stand-ins in tests get shadowed.** Once the real functions are in the build (declared inside the game), `window.x` stand-ins are ignored. `player_check` tests the real ones when present (`typeof` in scope), and uses stand-ins only when they're missing. To set a known `shipEffects` result, write `playerFx`'s cache (`FX_MIN`, `FX_NOW`).
- **Merges:** expect conflicts only in the header build line, `GAME_BUILD`, the DEV_NOTES build table and the file map. Keep both sides of section bodies.
- **A merge-resolution regex once ate a `// =====` section line.** Anchor conflict markers to the start of a line (`(?m)^=======`).
- **`pkill -f player_check.py` kills your own shell.** The command line contains the same text. Kill by PID instead.
- **Run the heavy checks one after another, not in parallel.** Two at once made `deck_check` time out loading the page; that's not a game failure.
- **cadet_test pixels:** the device button sits in screenshots. Against a build without it, hide `#devBtn` in a copy to prove nothing else changed. Against 0.40.x it's ALL IDENTICAL.
- **Save hook:** machine_check builds a partial save; the hook must not assume `save.player` exists.
- **Tuning numbers** live at the top of section 15: `NEED_DRAIN`, `SLEEP_GAIN`, `NEEDS_FRESH`, `NEEDS_OLD`, `SLOW_BELOW`, `SLOW_SPEED`, `PLAYER_ACTS` (minutes and gains), `ACT_NEAR`, `CARRY_MAX`, `INSPECT_MINS`. Fetch is 4 min and make 60 (`PLAYER_ACTS.fetch` / `.make`).

## How to test
- **Setup:** see `DEV_NOTES` "Testing". Use `CADET_CHROME=/opt/pw-browsers/chromium`.
- **player_check:** `python3 player_check.py BUILD.html`, about 6 to 8 minutes. It ends `PLAYER CHECK OK`. It covers:
  - a week on paper: a normal day's lowest values are food 55, energy 40, hygiene 52, fitness 62 and social 39.5, never slowed;
  - the speed rule: 1, 0.8, 0.8, 0.64;
  - sleep and skips;
  - every activity tapped on the real decks, with its pose and gain;
  - held places, the closed servery and walking away;
  - the real galley queue, and the ship's effects through a set reading;
  - the job loop against the real jobs: inspect, fetch, pause, resume, finish (condition 100), making a part, the notice, two-part carrying, putting parts back, the crate flag;
  - saving: `v: 1` → 80, `v: 2` kept, junk clamped, `?nosave`.
- **The other five checks must stay green:** cadet_test ALL IDENTICAL against the build you started from, deck_check, day_check day 1, food_check and machine_check.

## Ideas and open questions for the user
- **Should talking to crew, or eating with company, raise social?** Today only calling home does.
- **Should shopping buy things** (snacks that restore a little hunger, small comforts), or stay a nice moment?
- **The device:** what do you want on it first, now that needs, jobs and notices all show there?
- **Should machine trouble slow you down?** The machines' `walk` effect is ignored for the player by your rule. Keep it that way?
