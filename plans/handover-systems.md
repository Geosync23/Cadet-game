# Handover: the systems engineer (Pillar 2, Half B)

Written 2026-10-16 at combined build 0.40.8 (`claude/ship-integration` 980e6a9) by the systems engineer session (session_0134zewqwGV9hdGK6PqsaZ36). Read it with `DEV_NOTES.md`, which has the full detail under "Machines and wear (section 17)" and "The job list and supplies, on paper", and `plans/pillar2-plan.md` ("Machines and jobs").

## Role, branch, builds

- **Job:** Half B of Pillar 2, "the ship needs looking after":
  - B1, machines and wear;
  - B2, the job list, the crew doing jobs, the board and the device;
  - B3, supplies and hover carts.
- **Branch:** `claude/ship-systems`. **Builds:** 0.33.0–0.33.15, all merged into the combined builds 0.40.x.
- **I own:**
  - Section **`// 17. MACHINES & JOBS`** in `starship-cadet.html`. It sits after sections 15 (player) and 16 (galley).
  - **`machine_check.py`**.
- **Shared one-liners I added** (all inert without section 17):
  - `SAVE_EXTRA` in section 13 (now used by sections 15 and 16 too);
  - `jobBoardLive(t)` in the `jobBoard` kit (4b);
  - `worksTick()` in the main loop (12), after `galleyTick()`.
- **Shared one-liners other sessions added for me:**
  - the `whereIs` overlay and `planWhere` (section 14, the sim engineer);
  - `cartDockLive(group, dock)` in the `cartDock` kit (the Deck 6 architect);
  - the `'+' + w.hold` pose suffix (section 10, the sim engineer);
  - the cart prop (section 8b, the performance engineer).

## What's in section 17

- **The machine registry.**
  - `machineList()` reads `DECKS[n].machines`. A real machine is `{ id, kind, at, room, face, panel }`, optionally with its own `tier`.
  - `STUB_MACHINES` fills in stand-ins. A stand-in drops out once its deck has a real machine with its id or in its room. At 0.40.8 only these are still stand-ins: the lift, the four washers, the main fan, the bay door gear, the reactor and the three drive coils.
  - `MACHINE_KINDS` holds about 36 kinds. Each has its system, `life` in days, `time` (the share of wear from time), `use` (what wears it), `scope` (where its effects reach), `w` (weight in its system), `tier` and `part`.
  - **A machine of an unknown kind is silently left out.** `machine_check` fails on that, so add the kind first.
- **Condition and wear.**
  - `SHIP.machines[id] = { cond 0–100, state, lastService }`. The states run healthy 75+, worn 50+, faulty 25+, failing 10+, broken.
  - Always read it through `machinesNow()`. That runs each ship hour up to the current one: the hour's jobs (`jobsHour`), then its wear (applied at the hour's start). It's lazy, with a fast path when already up to date.
  - Wear comes from the schedules (`machUseDay`). Each counter is measured against an average day (`machNorm`, days 1–7). That average is worked out a day at a time in the background after load and kept in the save.
  - It's deterministic: the same however time moves.
- **Systems and ship health.**
  - `shipSystems()` covers 10 systems, including transport.
  - It applies the dependencies: power feeds everything, water feeds food and waste. They only bite once the feeding system is below 75.
  - `shipHealth()` blends them. A machine counts by how well it works (`machWorks`), not by its raw condition.
- **Effects** (the shared interface). Both functions return `{ deck, restore{5 needs}, drain{5 needs}, walk, cook, lift, spoil, mood (0 to -30), health, notes[{machine, kind, state, stage, text}] }`:
  - `shipEffects(deck)` is "now": it runs the machines first.
  - `shipEffectsAt(deck, t)` is pure: it reads an 8-day hour-by-hour record, and with no record it says all is well.
  - **Never call either from inside `shipDay` planning.** The plans feed the wear, so that's a loop.
  - Readers: the player's needs (section 15) every ship minute; the galley's cook time and replays (`shipEffectsAt`); the device notes.
- **Jobs (`SHIP.jobs`).**
  - **Posting:** worn → `service` (found 2–24 hours later); faulty → `repair`; failing → urgent repair; broken → `overhaul`. Plus `restock` runs.
  - **Claims:** hourly, by Works crew (by `CREW_TIER`) and engine crew (reactor and coils). Each claim is a run of planDay-shaped segments: parts shelf (`shelvesFor`, by the shelves' `stock`), the machine shop if a part must be made, the lift, the panel place (`panelPlace`: the place with `machine: id`), then back to the desk.
  - **On the deck:** `jobWhere(person, t)` lays these segments over `whereIs`. Claiming reads `planWhere`, never `whereIs`.
  - **Easy jobs wait for you:** `CREW_LEAVE` (3 hours) for jobs at your tier.
- **Your side:**
  - `jobsBoard()`, `claimJob`, `dropJob`, `myJob`;
  - `takePart` and `returnPart`;
  - `touchJob` (progress keeps a job yours past `YOU_KEEP`, 12 hours);
  - `finishJob`;
  - `machineInfo`.
  - The repair activity itself is the player engineer's (section 15).
- **Shown:**
  - The live Works bay job board (`drawJobBoard`, redrawn by `worksTick`).
  - The device's Jobs section (`jobsSection`).
  - Docked carts hide while they're out (`cartsOut`).
- **Supplies.** `SHIP.stores` (`STOCK` levels), `SHIP.hold`, and a Wednesday 10:00 delivery. `NO_MAKE` parts (filters, membranes, cells and so on) leave a job waiting for the delivery; any other part can be made in the machine shop (60 minutes).
- **Food by cart.** `cartClaim(t, cold, { replay })` is the one rule section 16 and the job list share:
  - a run when cold < 90 at any hour, or < 250 on the day shift;
  - each carries up to 150, never past the cap, and lands 40 minutes later;
  - a live call takes the meals from the hold and queues the run for the job list (`cartPost`);
  - the galley lands the meals, and section 17 never writes the cold store;
  - cart run segments carry `hold: 'cart' | 'cartfull'` for the crowd's cart.
- **Saving:** `ship.machines`, `machineHour`, `machineNorm` (per build), `jobs`, `stores` and `hold`. `machinesLoad` refuses junk, and an old save gets fresh machines.

## The answers pass (0.33.16–0.33.18, 2026-10-16, a fresh systems session)

The user's answers 1–8 and 22 (`plans/answers-pass-plan.md`), all in section 17 and machine_check (DEV_NOTES has the detail):
- **0.33.16:** jobs left for you. A small job at your tier waits `CREW_LEAVE` minutes of the day shift (`leaveEnd`); machine_check reports 3.7 a day. Daytime food runs that aren't urgent wait an hour for you (the cart run as your job), and `jobStops(j)` gives the stops for your walk.
- **0.33.17:** `machineLook`, `deckLook`, `shipHealthRows`, `shipMoodAt` (pure) and `chillerAt` (pure).
- **0.33.18:**
    - `machineUse` (tapping machines);
    - tier locks (`hatchTier`; section 4 takes `{ key, tier }` service entries);
    - late deliveries and Stores' Mail (`suppliesHour`, `SHIP.short`).

- **0.33.19:**
    - 0.41.2 merged in;
    - tier locks use the Deck 6 architect's `e.tier` (crew tiers stay `CREW_TIER`, agreed with the lead);
    - `cartWaiting(h)` and `galleyCartLand` for the galley;
    - `cartsOut` counts your cart;
    - the `CHORES` table (lamps, vents, calibrations, deliveries, rounds, small faults; the crew's filters and seals), tuned to about 5.9 jobs a day left for you;
    - `openJobs(forWho)` for the interactions engineer (session_01GGbtSiy4tDygCzrSUBDMYa).

  Leads: session_01WHXNp9A1WHAD2EHJw384Qp, since 2026-10-16 04:20.

**Known outside section 17:** player_check's job loop fails since 0.33.16. The galley plant's panel on Deck 3 (tile 39,1) can only be reached through Brennan's station tile 39,4 (`3-galley-2`). It's a layout or player-walking fix, reported to the lead.

## State at 0.40.8: loose ends and weak spots

- **The crew are too good.** About 7–12 jobs a day get done, and nothing ever gets past worn, so the player rarely meets a real fault. The lead parked this for the user. The levers are `CREW_LEAVE`, the `found` delay of service jobs, `CREW_TIER`, and how many Works crew are free.
- **No visible faults yet.** `shipEffects` notes ("Showers run weak", "The lights flicker and dim") show only as text on the device. Cheap on-deck signs were designed but never built: flickering lamps, a dripping pipe, weak shower spray, dim garden lights.
- **Stand-ins remain** for the lift, the washers, the fan, the door gear, the reactor and the coils. Their `at` and `panel` are a room's middle tile and they have no panel places, so crew can't walk to them; their jobs happen with the tech standing still. The architects should add real entries with panel places.
- **Cart runs with nobody free** (nights) go unseen: the job is closed without a run. Only the night Works officer (Navarro) covers night jobs.
- **Two restock runs at once** use the two docks; a third would share one. That's rare.
- **Job ids are `machine@hour`.** A machine re-faulting in the same hour after a player fix would reuse the id. That's harmless today.
- **The first read after load** still plans days 1–7 if it comes before the background warm-up has finished (within the first ~0.6 s).

## Gotchas (things that broke, and why)

- **Fixed per-use numbers broke when the schedules changed.** In 0.26.1 extra washing wore the recycler out in two days. That's why wear is now measured against an average day. Don't go back to fixed `per` numbers.
- **Re-entry:**
  - `whereIs` → `jobWhere` → `machinesNow` → `jobsHour` must never call `whereIs`. Use `planWhere`. Section 14 also guards it with `JOB_WHERE_BUSY`.
  - `shipEffects` inside planning is the same kind of loop.
- **Duplicate `planWhere`.** Both sections once defined `planWhere`, and the later one won silently, losing fields section 10 needs. There is exactly one now, in section 14.
- **Panel places aren't in the schedules' own list** (`schedData` skips places with `machine`). `panelPlace` reads `DECKS[n].places` directly.
- **Time going backwards** (New game, or `day_check` resetting each deck) resets the machines: `MACH_SEEN`. That's intended.
- **`machine_check`'s fake save** must have the full save shape (`player`, `ship`, `crew`), or other sections' `SAVE_EXTRA` hooks crash.
- **`deck_check.py`:** the Deck 6 architect's version lets `storage` places be reached through service hatches. The older one flags `5-cart-1/2` as unreachable.
- **Merges:** the usual conflicts are the build line, `GAME_BUILD` and the DEV_NOTES build-table rows; keep every row. Watch for anyone re-adding `cart: true` (it's `hold` now) or a second `planWhere`.
- **Tuning numbers** all live at the top of their blocks in section 17:
  - wear: `MACHINE_KINDS` (`life`, `time`), `machFresh` (70–100 at start), `MACHINE_FX`, `MACHINE_SEV`, `MACH_WORKS`;
  - jobs: `JOB_TYPES` (minutes, how far a job restores), `CREW_TIER`, `CREW_LEAVE`, `YOU_KEEP`, `JOB_FETCH`, `JOB_MAKE`;
  - supplies: `STOCK`, `NO_MAKE`, `DELIVERY`;
  - food carts: `CART_MEALS`, `CART_DAILY`, `CART_URGENT`, `CART_RUN`.

## How to test

`CADET_CHROME=/opt/pw-browsers/chromium python3 machine_check.py BUILD.html [DAYS]` takes about 15–30 seconds. "Good" is MACHINE CHECK OK, which means:
- **Every machine's kind is known.** Real machines without a panel place are listed, but that's not a failure.
- **With no repairs over 14 days**, ship health falls steadily, roughly 98 → 16–19. Nothing goes faulty in the first two days, something breaks by day 14, but the slow kinds don't.
- **It's the same every way:** run twice, in one jump, at odd minutes, and with the caches cleared.
- **An ideal crew** keeps health at 90 or more. **The real Works crew** keeps everything at worn or better and health at 85 or more, never runs a shelf below 0, does nobody's job twice at once, keeps every job inside its person's work block, and `jobWhere` agrees with the jobs.
- **Your side** works: one job at a time, the 12-hour lapse, `touchJob`, `returnPart`.
- **`cartClaim`** is pure in replays, never over the cap, and never misses an urgent run.
- **The save** round-trips.

Also run every turn: `cadet_test.py` (ALL IDENTICAL, since section 17 draws nothing on Deck 4), `deck_check.py`, `day_check.py` (with jobs on; day 3 is a good extra), `player_check.py` and `food_check.py`.

## Ideas and open questions for the user

1. **How many faults should you meet?** Today the crew catch nearly everything early. Should there be more for the player: slower rounds, a longer wait before the crew take easy jobs, or crew busy with other work?
2. **Visible faults on the deck:** flickering lights, drips, weak showers, wilting plants, a "Ship health" status board on the bridge and in the Works bay. Worth a small next step?
3. **Help with cart runs** as a player job: push the food cart yourself. It was designed and is simple to add.
4. **Supplies running short as a story beat** (a late shuttle, filters rationed)? The stock and delivery numbers are easy to change.
5. **Should ship health and faults affect crew mood visibly** (grumbling, chatter) once Pillar 3 (social) starts? The `mood` numbers are already there to read.
