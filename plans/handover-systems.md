# Handover: the systems engineer (Pillar 2, Half B)

Updated 2026-10-16 at 0.33.31 (final for this session) (claude/ship-systems; the predecessor's note below, then this session's additions). First written 2026-10-16 at combined build 0.40.8 (`claude/ship-integration` 980e6a9) by the systems engineer session (session_0134zewqwGV9hdGK6PqsaZ36). Read it with `DEV_NOTES.md`, which has the full detail under "Machines and wear (section 17)" and "The job list and supplies, on paper", and `plans/pillar2-plan.md` ("Machines and jobs").

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

- **0.33.20–0.33.22:** the food-cart fixes.
    - `cartWaiting` is true only for your own run;
    - a run that has already arrived when it reaches the list is history;
    - the galley alone counts the meals on their way (the lead's decision);
    - machine_check 5f proves the crew take every food run in live play.
- **0.33.23:** handing jobs in at the board: `jobStepDone`, `turnInJob`, `j.workDone`, `jobStops` done marks, and `TURN_IN` (switched on by the interactions engineer's 0.37.3).
- **Pillar 3, C7 (0.33.24–0.33.27):**
    - event wear by system and machine kind (`eventWear`);
    - event jobs from section 18's `eventMod('jobs')` (`eventStopOf`, `postEventJob`); finishing one yourself calls `eventMine('jobs')`;
    - favours for the social engineer (`favourPost`, `favourAccept`, `favourDecline`, `favourTurnIn`, `favoursOf`, `myFavours`);
    - `cartTrays` for the galley's event trays;
    - storm blackouts (`blackoutHour`, `blackoutAt`, `deckLook().dark`, scored as `eventScore('blackout', minutes)`).

  The storm's own `stormTrays` is dropped in the events engineer's 0.34.12 (the lead's decision): the galley's `cartTrays` is the one tray run.
- **0.33.28:** `traysArrivedAt(day, to)` for the galley's bridgeHungry score:
    - a crew run gives its drop-off end;
    - yours gives `j.dropAt`, recorded by `jobStepDone` on a `drop` step.
- **0.33.29:** event jobs carry `eventJob: <spec id>` for section 18's `eventTakeJob`. One the player volunteered for at a meeting (`SHIP.event.mine['wants:<id>']`) is claimed for 'you' as it's posted. It's claimed directly, since `claimJob` would re-enter `jobsHour`.

- **0.33.30:** machine_check's runs measure ordinary wear with events off (`events: True` to opt in). New case 4c runs with the ion storm on: comms wear harder, and the real crew keep the sensor array from getting past faulty.
- **0.33.31:** the diplomatic visit's `coldCabins` thread (`coldCabinsHour`).
    - **Assumption to confirm:** guests aboard is read as `eventMod('effect', 'guests')`. That's my proposal; the events engineer hadn't confirmed it at handover. If they signal guests differently, it's the one line in `coldCabinsHour`.

**Final state (this session's end, 0.33.31):** everything in section 17 is pushed and reported, and all checks pass. Open items:
- confirm the guests signal above with the events engineer (session_01GW9QtevJxaMQzzCGPBHaxb);
- otherwise nothing.

Leads during this session, in order: session_0158BCCswtdujm3t5d2LXsFz, session_01WHXNp9A1WHAD2EHJw384Qp, session_015QoyPWBdMPM4ywf5W2jMMs (current).

Other sessions I worked with:
- galley engineer: session_01AVGVnj4Q1jFmVoD6xi5asT;
- interactions engineer: session_01GGbtSiy4tDygCzrSUBDMYa;
- social engineer: session_01DzZ669spGpdSdVMYzUog2N;
- events engineer: session_01GW9QtevJxaMQzzCGPBHaxb.

**Gotchas from this session:**
- `jobsHour` must never call anything that runs `machinesNow` (`claimJob`, `jobsBoard`, `openJobs`): that re-enters the hour loop.
- `deckLook` is cached on `MACH_REV`, so anything that changes within an hour (blackouts) must be in its cache key.
- machine_check's stand-in events: `eventNow` must count the day on, as section 18's does, or event job keys (which hold the event's start day) repost daily. `SHIP_EVENTS` is keyed by id from 0.41.5; the test handles a list or an object.
- A job the player holds lapses after 12 ship hours with no progress. Tests that jump a day must check before that.
- With `TURN_IN` on (from the interactions engineer's 0.37.3), `finishJob` only does the work. machine_check turns it off at the start; 5g turns it on itself.

**Test files I own:** machine_check.py. Sections 5c–5h cover cart runs, looks, tapping machines and Mail, chores and `openJobs`, live food runs, turning jobs in, and events and favours. Run every check one at a time. day_check takes about 4 minutes; the rest take 1–2 minutes each.

  Leads: session_015QoyPWBdMPM4ywf5W2jMMs since 2026-10-16 15:15.

**Known outside section 17:** the galley-plant reach problem (from 0.33.16) was fixed by the player engineer's squeeze-past (0.28.12). player_check is all OK from 0.41.4 on.

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

## This session (2026-10-16/17, session_01TqLepvhqDZRwFj7ZuLb6Xa): 0.33.32-0.33.39

Leads: session_015QoyPWBdMPM4ywf5W2jMMs, then session_01PxXKwc5mkC7tV5MPi3p7PP (current; report to them after each push: files, what changed, checks, memory %). Build master: session_012K7RZ3oSX2vpBb1rR66MBh. Social A (reputation, reads repair / jobAbandoned / jobUnclaimed): session_012pK2XVi5UhqEd28fakYk68. Reviewer 1: session_01HK4m33sUiLuVim8VWaCPMs (reviewed ae58e43: PASS, plans/reviews/ship-systems-ae58e43.md on claude/reviews; reviewing f211129). Section 15 has a new owner (player engineer 3, via the lead).

- **0.33.32-33, the user's bug "the job board never has any jobs":** `CREW_LEAVE` (3 ship hours) was only 5 real minutes. Now `leaveEnd` holds a small job to the end of the shift its wait runs out in, at most `HOLD_MAX` (6) at once (`j.released` for the ones let go), and nothing on the player's days off (`playerShiftOn(d)`, Sat/Sun, the sim engineer's). Day 1's first two chores post at 06:00. machine_check 5i: a week, weekday shifts ~4.4 jobs for you, no empty hour, nothing held Sat/Sun.
- **0.33.34-35, the working garden (with the galley engineer):** machine kind `growlight` (real `3-growlight-1/2` with panels from decks 0.38.6); `gardenAt(t)` -> { water, feed, light } 0-1, pure, 1 at worn or better (`min(1, machWorks/85)`); `gardenCarry({ at, crates, title })` -> 'garden@<min>', `carryWaiting(id, t)`, `carryArrivedAt(id)`; your drop calls the galley's `galleyCarryLand(id)` once. Pickup `3-crates-1`. machine_check 5j.
- **0.33.36-37, Pillar 4 for onboarding (session_01KaHzfqSqF8B4bkNFrH1tsx):** `jobReserve(kind, day, at, slot, { until })`, `jobReserved(slot)`, `jobRelease(slot?)`; `heldForYou(j)`; reserved jobs have a `make` stop (`RESERVE_MAKE` 'bracket', `makeMins` 30, the player engineer's 0.28.24 does the make step). Slots: 1 Mon 08:00 shadow, 2 Mon 13:00, 3 Tue 07:45; onboarding calls them from `introBegin`, `jobRelease()` from `introEnd`. `simNote('job', { id, step, reserved, ... })`: take / stop (k, tag) / done / turnin / drop / lapse.
- **0.33.38:** merged decks 0.38.8 (real washers `4-washer-1..4`). Fixed crew "two jobs at once": busy until a job's route ends (`j.end > t`), not just while claimed.
- **0.33.39, for social A:** `simNote('repair', { who, machine, state, ... })`, `simNote('jobAbandoned', { machine, dept: null })`, `simNote('jobUnclaimed', { machine, dept: null })`. All section 17 notes queue in `SIM_Q` and go out via `simFlush()` after `machinesNow`'s hours or at the end of a player action, never inside `jobsHour` (social's handlers read the schedules).

**Open / known:**
- player_check fails one line on decks 0.38.8 and later: "a washer tap should find its stub machine" (section 15's test assumes stand-in washers). Told the player engineer (session_012J4ctzJgFRBaUFU5sJvega).
- Still on call for Pillar 4: the "asked for you" mark for reputation beyond reserved jobs (social A has `repAskedFor(dept)`; the board could show it on jobs for departments that think well of you). Not asked yet.
- `jobUnclaimed` fires when a held job's wait ends, even if the crew are too busy to take it that hour.

**Gotchas added:** machine_check runs must only move the clock forward inside one case (going back = New game, which wipes the jobs). Run player_check with a timeout of 20 minutes (it takes ~10). A `pkill -f` pattern can match your own shell command and kill it.

## 0.60.7 session (2026-10-18, session_016Mv2wxrtkGgAwcst4GWADY): 0.33.40-0.33.42

Lead 10: session_014hkEBULoSV9EKZZSwMWyPd. Branch `claude/systems-0607` (from live 0.60.6a, c8685cf). Brief: `plans/brief-0607.md` on `claude/lead-pillar1`; plan: `plans/plan-0607.html` on `claude/plan-0607` ("Around the ship", "Stores and the lift").

- **0.33.40, the Works crew at work:** `HOLD_MAX` 3; `shareOut` (every third new small job by id hash to the crew at once while `SHARE_KEEP` 2 others are held; `SHARE_ON` for tests); `placeFreeFor` (chore stops at real places when nobody's plan or job is there); deliveries carried (`hold: 'carry'` from pickup through the drop); `SHOW_JOBS` (Day 1 08:00 Bea's vent at `4-lift-1`, Day 2 13:00 her box of tools from `5-hold-1` to `5-bench-1`; `j.crew`); `showJob(day)` for onboarding. machine_check 5l.
- **0.33.41, the right shelf:** `SHELF_NAME`, `shelfOf`, `shelfStock`, `shelfLine`, `shelfTapped`, `shelfNeed`/`shelfWant`, `shelfWrong`, `shelfGlowTick` (one amber box, Deck 5, made on first use); the machine shop's 15:00 top-up. Small edits in section 15 (`jobTap`: stock card with no job at all, `shelfWrong` before fetching) and 15b (`ixChoreTap`'s fetch, `ixShelf` for the arrow and label). player_check and interactions_check tap the part's own shelf now.
- **0.33.42, the Wednesday delivery:** no late delivery in week 1; crates (`CRATE_PARTS` 8, `CART_CRATES` 4); held for you till 14:00 (`DELIVERY_KEEP`); `cartLoadHold`/`cartUnloadShelves` (`j.onCart`); `holdCratesLive(group, k)` for the deck architect's crates (asked of them through the lead); section 15's `cartEnd` for the delivery (second trip, 10-minute unload). machine_check 5m; player_check's cart run checks the shelves after the unload.

**Gotchas:** a chore's pickup can be at a shelf place (`5-parts-1`), so the shelf's stock card only shows with no job at all. Don't run two player_checks writing to the same file (a killed run keeps writing into it). Under load player_check takes over 30 minutes; run it alone. day_check day 3 fails on live 0.60.6a too (two diners in one mess seat), not section 17.
