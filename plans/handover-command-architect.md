# Handover: the command architect (Deck 2)

Written 2026-10-16 at build 0.40.8 (`claude/ship-integration` 980e6a9), by session_014DMHpLuFyNknrAcZZGGNhU. Read it with CLAUDE.md, DEV_NOTES.md (the "Deck 2" section and the 0.9.x, 0.19.x and 0.32.x rows) and plans/deck2-plan.html.

## Role, branch and builds

- **Role:** Deck 2, Command & Science. I built it, then gave it places (Pillar 1) and utility rooms and activities (Pillar 2).
- **Branch:** `claude/deck2-command`. The lead merges it into `claude/ship-integration`.
- **Build numbers used:** 0.9.1–0.9.5 (the deck), 0.19.1–0.19.2 (places), 0.32.1–0.32.2 (activities, utility rooms).
- **What I own:**
  - In `starship-cadet.html`, one block in section 4d, between Deck 3's block and Deck 6's. It starts at the `// DECK 2: COMMAND & SCIENCE` header and holds:
    - `// ---- Deck 2 kit ----`: the `D2` materials, kit added with `Object.assign(KIT, …)` and `Object.assign(WALL_KIT, …)`, and `d2Frame` / `d2Suite`;
    - `DECKS[2]` and the line after it that fills `closedDoors` from `sealed`.
  - `plans/deck2-plan.html`, including its "Utility rooms" section.
  - The "Deck 2" section of DEV_NOTES.md, and my rows in its build table.
  - One shared edit, made byte-for-byte as the bridge architect's: the hull-run splitter's `HULL.byFace` option (0.9.5). Deck 2 opts in with `hull.byFace: true`.

## What's on Deck 2

- **Layout:** 52 × 22 on Deck 3's outline, lift at [20, 11]. The senior quarters are aft of the lift, round a looped carpeted corridor; science is forward, off a four-wide corridor; the sensor array is in the nose.
- **Bedrooms:** 15, all locked.
  - 12 are crew cabins, furnished by `d2Suite` from the door key, with three layouts: 4 × 5 hull cabins, 3 × 5 cabins by the lift, and 4 × 4 inner cabins.
  - Vance's and the Envoy's corner cabins are laid out by hand.
  - The Captain's quarters (5 × 12): a curtained bed, a table for eight under the deck's warm lamp, and her study.
  - Bedroom taps are `see` items (bed, desk), readable through the cutaway without walking.
- **Corridor:** brass plates over the doors, wall lamps, four portraits of past captains, consoles.
- **Science:** the Watch office, chart room, Survey lab, sample lab, observatory and comms room; the specimen store and probe bay (locked); the sensor array behind glass.
  - The array's dish turns (`SPINS`), and its feed glows and fades (`PULSES`). The deck's second lamp, tinted blue, lights it. `LAMP_SLOTS` is 2 and Deck 2 uses both.
  - The specimen store's jar glows and fades too.
- **Utility rooms (0.32.2):** the lab gas plant `g`, utility closet `u` and cable crawl `n`.
  - Floors are `still: true`, so they draw no random numbers.
  - Their hatches are listed in `DECKS[2].service`, so the player and Works crew can pass.
- **Mood light:** `light: { sky #e9e6ff, sun #fff0dc, hemi .94, sunI .96 }`.
- **All kit uses shared `D2` materials.** Nothing calls `R()` at load.

## Update: the answers pass (0.32.3–0.32.7, session_01EhJv6dqovqhQyruMveFuRR, now retired)

- **Door plates (27):** officers' plates read name over rank from `ROSTER` (`d2Plate`, by bed id, at dress time; `brassPlate` takes `sub`). The Envoy and Visitors plates keep their text. Room names and tap texts still say roles.
- **Observatory night (25):** 11 places in the observatory carry `event: 'observatory-night'`; the seven new ones (`2-obsnight-1..7`) are type `event`, which deck_check.py now accepts. The sim engineer schedules the evening.
- **Window seats (21):** `window: true` on the seven window-bench seats and two spots by the observatory glass.
- **Lived-in touches (31):** signs in the gas plant and crawl, a calendar nook in the closet, two mugs (`d2Mug`, `d2Sign`, `d2Nook`).
- **Machine wear (2/3):** drawn centrally by the performance engineer (section 8b, 0.27.9). Deck 2's only part is optional `look` overrides on its `machines` entries where the default spot is hidden. My 0.32.4 lamps were withdrawn in 0.32.5.
- **Kit names (0.32.5):** Deck 2's `cableTray` and `relayRack` clashed with other decks' (the last definition wins), so they're `crawlCableTray` and `lightRelayRack` now. Check a new kit name isn't already used.
- **Seats (0.32.6–0.32.7):** every sit place has `xy` and `y` from the performance engineer's measurements, checked in `?seats`. Their re-measure of 0.32.7 found all 89 Deck 2 seats right. The en-suites got a toilet (they had none; seat top 0.42 at the cubicle's local (.24, .2), facing -x). Far-side stools face their tables. If furniture moves, re-measure its seats in `?seats`.
- **Gotcha:** rooms named by a symbol (`+` lobby, `-` senior corridor, `=` science corridor) trip up scripts that match `room: '[A-Za-z]'`. That's how the benches missed 0.32.6.
- **Plates:** `d2Plate` prefers the crew designer's `plate: { rank, name }` (0.16.6) when present.
- Places: 175. Draw calls by the lift: 282; day peak 374.
- **Merge note:** 0.32.5's rename means that on `claude/deck2-command` alone, deck_check fails on Deck 6 (the bridge architect's tray-on-legs wins there). With the bridge architect's `floorCableTray` rename (`claude/deck1-scale` 5dfed37) merged too, every check passes.
- **Branch head when I retired:** `claude/deck2-command` at 0.32.7 (9baf976). Pillar 3 deck work moves to the merged deck architect (`claude/decks-p3`).
- Testing extras kept in my scratchpad (not in the repo): a pixel compare of every deck day and night with crew hidden, and a plate-texture dump. Rebuild them from cadet_test's `Game` class if needed.

## Shared formats other sections rely on

- **`DECKS[2].places`, 168 entries:** `{ id, type, at: [c, r], face, pose, room }`, plus optional `anim` and `machine`.
  - **Bed ids** are `2-<room letter>`: 2-C, 2-X, 2-O, 2-I, 2-V, 2-S, 2-E, 2-T, 2-B, 2-H, 2-R, 2-N, 2-G, 2-D, 2-U. The roster points at these. Never rename them.
  - **Other ids** are `2-<what>-<n>`. The schedules and saves may hold them, so keep them stable.
  - **Private places:** every place inside a bedroom (desk, armchair, en-suite shower, basin and toilet) belongs to that bed's owner, through the 0.21.2 `owner` rule (same room as a bed place).
  - **Free time:** 6 public seats in the chart room and observatory are `common-room`, because the `quiet-corner` habit looks for `common-room` on Deck 2. Two chart-room window seats stay `lounge-seat`, for Deck 2 workers' tea breaks.
  - **Watch posts:** 4 `work:watch` places are standing posts with no furniture (lockers, the lobby glass, the Captain's door, the array window). The roster puts 8 Watch crew on Deck 2 by day.
  - **Service spots:** 9 `work:works` places, one on each machine's panel tile, each carrying `machine: '<id>'`. The planner skips them as desks.
- **`DECKS[2].machines`, 9 entries:** `{ id, kind, at, room, face, panel }`.
  - **Kinds must exist in `MACHINE_KINDS`** (section 17). `machineList()` silently drops any other kind, and once a deck has machines of its own, its stand-ins go too.
  - **The ids:** 2-gasplant-1 `gasplant`, 2-extractor-1 `scrubber`, 2-breaker-1 `powerjunction`, 2-junction-1 `junction` (the light relays), 2-repeater-1, 2-feed-1, 2-racks-1 and 2-racks-2 `relay`, and 2-array-1 `array` (the dish).
  - 2-gasplant-1, 2-junction-1 and 2-array-1 keep the old stand-in ids, so saved wear carries over.
- **`DECKS[2].sealed`** (door → room) builds the locked doors' tap text. The crew's locked-door rule uses it too: a person may pass a `closed` door into the room of their own bed or of the place they're going to.

## State at 0.40.8: loose ends and weak spots

- **Borrowed machine kinds:** the extractor runs as a `scrubber`, the breakers as a `powerjunction`, and four `relay`s add a lot of comms weight. The systems engineer may want dedicated kinds; that's a one-word change per machine.
- **Machines face away from the camera:** their service side faces the aisle, so the default view shows their backs.
- **The Captain's table:** two west seats can't be reached because the window seat is behind them (the lead's call: keep the seat). They aren't places.
- **The Envoy's cushions:** five are drawn, but only four are places (two share a tile).
- **No `xy` or `walk` on places:** the cushions and the paired bench seats would benefit from exact spots.
- **The cable crawl** is a standing floor with low trays. Crouching comes later.
- **The sensor array** stays locked to the player (tier 3). Crew can reach its three service spots through its closed door.
- **Door plates still show roles, not names** ("Second Officer", "Comms Chief"…), though the roster has named the six senior officers. The portraits' past captains (Varga, Moro, Brenner) are invented.
- **The plan page's data block is out of date.** plans/deck2-plan.html is still Sketch 8's data. The build differs in a few places:
  - no `v,23,9` glass;
  - the Watch office plate is on `v,23,5`;
  - bedroom names are brass plates over the doors;
  - the washroom is laid out by hand.
- **The public washroom** is hand-laid (2 toilets, 1 basin). The shared `washroom` template boxed in toilets in a room only 2 tiles wide; the template itself is unchanged.

## What I'd do next

- **Door plates:** put the roster's names on them.
- **Exact spots:** add `xy` and `walk` where seats sit off the tile centre.
- **Machine kinds:** dedicated kinds, if the systems engineer wants them.
- **Machine faces:** turn them, or add a decal on their camera-facing side, so they read from the default view.
- **The plan page:** refresh its data block to match the build.

## Gotchas (things that broke, and why)

- **`roomFrame` only sees `door` and `open` edges.** Locked bedrooms have `closed` doors, so its templates put furniture against the wrong wall. That's why `d2Frame(room, doorKey)` exists.
- **`std()` makes a new material on every call,** and every distinct material is another draw call after merging. Use `D2` materials in Deck 2 kit. (`KIT.plant` and `KIT.rug` make their own materials; my `suitePlant` and `suiteRug` don't.)
- **Never call `R()` in kit made at load.** A void room turned into a real room must have a `still: true` floor; without it, every later floor tile's grain on Deck 2 shifts.
- **Furniture boxes in doorways easily.** `place` blocks every tile within the footprint plus 0.08 m. In 0.19.1, cabins S, R and X, the Captain's en-suite and two washroom toilets were unreachable; 0.19.2 fixed them. Run the place check after any furniture move.
- **Regenerating places:** place tiles depend on furniture positions. I generated them with a scratch script that logged every `place()` call on Deck 2 (wrap `place` through cadet_test's `__sc` hook and rebuild the deck). That script isn't in the repo. If furniture moves, check the affected places by hand, keep ids stable, and run deck_check.
- **Merge traps:**
  - The HUD build line, `GAME_BUILD` and the DEV_NOTES build table are where branches collide; the lead combines them.
  - The Deck 2 block sits between Deck 3 and Deck 6 on purpose, away from where others append.
  - Shared edits must be byte-for-byte the same on both branches (the `byFace` fix was).
- **Scripting in Python:** watch the quoting when a script writes DEV_NOTES. Apostrophes inside a single-quoted string broke one push (0.19.2), so its notes needed a follow-up commit.
- **Test runs sometimes time out** at load (Playwright's 30-second `page.goto`). Just rerun.
- **Lift tests:** the first panel press of a run spends its time walking from Bunk 1, so press twice.

## How to test my area

- **`deck_check.py`:** must say DECK CHECK OK. At 0.40.8, Deck 2 has 168 places (basin 16, bed 15, bench 5, common-room 6, lift-wait 6, lounge-seat 36, shower 15, toilet 17, work:command 1, work:comms 10, work:survey 24, work:watch 8, work:works 9), 9 machines, no bad entries, and 282 draw calls by the lift.
- **`day_check.py` (day 1):** must say DAY CHECK OK. At 0.40.8, Deck 2 has up to 19 crew, nobody stuck, and peaks at 374 draw calls (budget 450).
- **`cadet_test.py`** (Deck 4, old build against new): ALL IDENTICAL for a Deck 2-only change. If places or types change, crew plans shift, so the crew shots differ; the crew-off shot (`g_nocrew`) must stay at renderer noise (max 1).
- **Other decks pixel-identical** with crew hidden, by day and by night. I used a small screenshot script (`goToDeck(n)`, crew off, fixed camera targets, a pixel compare that counts differences of 2 or more). It isn't in the repo.
- **`machine_check.py`:** Deck 2's machines run, and the save round trip passes. At 0.40.0 it failed on `3-recycler-1` (faulty within two days), which isn't Deck 2's.
- **By eye:** walls down over the quarters and the science side, by day and by night. You should see the lamp over the Captain's table and the blue light on the array.

## Ideas and open questions for the user

- Should the door plates show the senior officers' names now that the roster has them?
- The second visitors' cabin (U) could become a senior lounge, as the plan once suggested.
- The observatory could host an "observatory night" event, since off-duty crew sneak in there.
- Crawlways: crouch-walking when the game supports it.
- Should the player ever get inside a bedroom: a tour on promotion, or an invitation to the Captain's table?
