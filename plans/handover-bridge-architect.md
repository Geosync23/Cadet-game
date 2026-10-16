# Handover: the bridge architect (Decks 1 and 3)

Updated at retirement, after the answers pass (my last build 0.31.13, `claude/deck1-scale` 5b6ffeb, accepted into the combined build after 0.41.4). For Pillar 3, one deck architect owns every deck; this note is the map to Decks 1 and 3. Read it with `DEV_NOTES.md`: the sections "Deck 1, the Bridge (0.8.x)", "Places on Decks 1 and 3 (0.18.x)" and "Pillar 2 on Decks 1 and 3 (0.31.x)", plus build rows 0.31.1–0.31.13, which hold the detail.

## Role, branch, builds

- **Role:** architect of Deck 1 (the Bridge). From Pillar 1 I also owned Deck 3's places, and from Pillar 2 its utility rooms. Deck 3's shell, rooms and dressing are the first lead's work (0.5.x–0.6.x); I've owned `DECKS[3]` since 0.18.
- **Branch:** `claude/deck1-scale`.
- **Builds:**
  - 0.8.x: Deck 1 built.
  - 0.12.x: Deck 1 scaled up.
  - 0.18.x: places on Decks 1 and 3.
  - 0.31.1–0.31.5: Pillar 2 (activity furniture, utility rooms, cold store).
  - 0.31.6–0.31.13: the answers pass.

## What I owned in `starship-cadet.html`

All of it is inside section 4 (decks):

| What | Where (search for) |
| --- | --- |
| Deck 1 kit: materials `BRG`, pieces via `Object.assign(KIT, …)` and `WALL_KIT`, `bridgeViewscreen` | `const BRG = {`, just above `// DECK 1: BRIDGE` |
| `DECKS[1]` | `DECKS[1] = {` |
| Deck 3 kit (A5b): `till`, `basketStack`, the utility kit (`recyclerTanks` … `relayBank`, `cabinet`, `dataBus`, `floorCableTray`), helpers `pipeX`, `pipeZ`, `statusLights`; wall kit `relayBox`, `wallCalendar`, `handSign`, `radioShelf`, `mugRail` | `// ---- Deck 3 kit (A5b` |
| `DECKS[3]`: its `places`, `machines`, `service`, rooms and `dress` | `DECKS[3] = {` |
| `grabShelf` in shared kit (the `o.live` hook only) | `grabShelf(g, o = {})` |

There are also the plan pages `plans/deck1-plan.html` and `plans/deck3-plan.html`. Each has a "Utility rooms (built in 0.31.3)" section with a sketch. The sketches' machine `face` values predate 0.31.11's correction, so trust the game file.

**Not mine:**
- Section 14's `schedData` (the sim engineer's) skips places with `machine`, so panels are never desks. Event places are its own handling since sim 0.26.11.
- `deck_check.py` accepts a numeric `face`. Both the Deck 6 architect and I added this; the lead keeps one version.

## What's on the decks

- **Deck 1, the Bridge.** 22 × 12 tiles: lobby, bridge (command ring, viewscreen), observation room, ready room (locked; access is a Pillar 3 progression item), washroom, and three service rooms: closet `k`, relay room `u`, sub-floor crawl `c`.
  - A Ship health board is in the bridge vestibule. It's the Deck 6 architect's `healthBoard` kit, placed with `placeOnEdge('healthBoard', 'h,10,4', 's')`.
- **Deck 3 utility rooms.** Water recycler `R`, galley plant `g`, irrigation `i`. They have machines, pipes, `still: true` floors (no random numbers), and lived-in touches: calendars, a radio shelf, signs and a mug rail (Deck 1's rooms have them too).
- **Activity furniture.** A till and baskets in the store; the store is staffed (`3-store-1` behind the till, `3-shop-7` paying).
- **Hull.** Both decks are `byFace` (Deck 3 since 0.31.6: 17 hull pieces, not 126).

## Shared formats other sections rely on

If you rename or move any of these, tell the owner first.

- **Places** (sim, performance, player): `{ id, type, at, xy?, walk?, face, pose, anim?, y?, window?, event?, machine?, room }`.
  - **`face`:** a letter, or degrees from south toward east (0 S, 90 E, 180 N, 270 W). To face a table at (tx, tz) from (x, z), use `atan2(tx - x, tz - z)` in degrees.
  - **`y`:** the seat top in metres. All 142 seats on Decks 1 and 3 were measured by the performance engineer (0.31.12, 0.31.13).
  - **Window seats** (`window: true`):
    - Deck 1: `1-window-1..4`, `1-walk-2..4`.
    - Deck 3: mess seats `3-mess-1, 3, …, 15` and `3-lounge-10..12`.
  - **Event places** (type `event`):
    - `1-handover-1..6`, at the aft of the command ring: the 06:00 and 18:00 shift handover.
    - `1-walk-1..5`, in walking order through the observation room: the Captain's evening walk.
    - The sim engineer lists these per event (`'1|@handover'`, `'1|@walk'`); free time never uses them.
  - **Cold store:** `3-cold-1`/`-2`, type `storage`, unloading spots for the restock carts (section 17's `COLD_AT`).
  - **Gym:** `3-gym-1..3` (treadmills, `y` .16) and `3-gym-4` (rower) are read by `placeBusy(id)` for the moving belts. Keep these ids.
- **Machines** (systems, performance): `{ id, kind, at, room, face, panel, look? }`.
  - Deck 3 has 12: ovens, range, galleyplant, chiller, recycler, filter, pump, uv, lights, nutrient, irrigation.
  - Deck 1 has 5: relay ×2, junction, lights, databus.
  - Each has a `<id>-panel` place (`work:works`, `machine: '<id>'`).
  - **`face` is the way the machine's front points**, towards its panel (corrected in 0.31.11; it had been the wall behind).
  - **`look`** puts the fault lamp, drip, glow and screen-dim on the piece's real front. The performance engineer's `machineFx` draws them; check with `?looks`.
- **Service hatches** with tiers: `service: [{ key, tier }]`.
  - Deck 3: galley plant 1, recycler 2, irrigation 2.
  - Deck 1: closet 1; relay room, crawl hatch and `v,10,10` all 3.
- **Crawl tiles:** Deck 1 `crawl: [...]`, the crawl's 5 walkable tiles. Deck 3 has no crawlways.
- **Grab shelf:** `grabShelf` with `live: true` hands two rows to the galley's `galleyShelfRows(g, ys)`. It must stay a function declaration.

## State and loose ends at 0.31.13

- All checks pass. `food_check`'s dinner-rush queue line failed on sim 0.26.11 itself (the real 18:00 handover moves the day-1 queue); the galley engineer is making that test robust.
- **Kit name clashes:** I scanned every KIT/WALL_KIT name. Only `cableTray` (Deck 6 vs Deck 2) was left, and the lead has the command architect renaming Deck 2's to `crawlCableTray`. Re-scan after any merge (the snippet is in "How to test").
- **Weak spots:**
  - **Deck 3 draw calls:** the busiest deck in day_check, peaking at about 402 of the ~450 budget. New Deck 3 kit should reuse existing materials.
  - **Cold store:** only 2 × 2 walkable tiles. Watch it once restock carts are visible.
  - **Panel places:** they sit behind service hatches. Any new code that hands out places must skip `machine` places.
- **What I'd do next:**
  - Group each door leaf's six materials into two. It's shared code, and doors cost about a third of a deck's draw calls.
  - Machine `look.screen` dims for pieces with screens (only the recycler has one now).

## Gotchas (things that broke before)

- **Kit names are global.** `Object.assign(KIT, …)` lets the last definition win silently, on every deck. Three of my pieces were overridden or did the overriding: `cableTray`, `relayRack`, `calendar` (fixed in 0.31.8 and 0.31.11). Pick distinctive names and scan for clashes.
- **New places aren't automatically inert.** Adding 11 event places to schedData's lists shifted every crew member's day: cadet_test differed with crew shown, and food_check failed. Places nobody schedules must stay out of the schedule's lists. Check `cadet_test` with crew against the base.
- **Random numbers.** Kit made at load must never call `R()`. Utility floors use `still: true`.
- **"Pixel-identical with crew hidden" needs one more stub.** Hidden crew still open doors, so also stub `crewNearDoor = () => false`.
- **Machine `face` and default spots.** Effects use the front direction and the panel tile. Real pieces rarely line up with `at`, so give each machine a `look`, measured from the piece's placement and size, not from hit boxes or raycasts. The deck's furniture is merged into shared meshes, so raycasts slip through.
- **Merge traps.** Nearly every merge clashes on the HUD build line, `GAME_BUILD` and DEV_NOTES rows. Keep your number, keep both sides' rows in order, and take the other side's `SHIP_RATE` and engine lines.
- **deck_check is strict.** New place types go in its `TYPES` list, and `face` must be a letter or a number.

## How to test the decks

Set `CADET_CHROME=/opt/pw-browsers/chromium` and run the checks one at a time (several browsers at once can fail to start):

1. **`cadet_test.py BASE.html NEW.html`:** expect ALL IDENTICAL (crew included) against the current integration build.
2. **`deck_check.py`:** expect DECK CHECK OK. Decks 1 and 3 have 5 and 12 machines; draw calls by the lift are about 313 and 332.
3. **`day_check.py`:** expect DAY CHECK OK, with every deck's peak under about 450.
4. **`machine_check.py`, `food_check.py`, `player_check.py`:** expect OK.
5. **Other decks pixel-identical:** screenshot each deck in both builds with the crowd hidden and `crewNearDoor` stubbed, from the lift, zoomed out, rotated, walls down and at night. Zero differing pixels is the bar; find the cause of any difference.
6. **Kit-name clash scan:** list the methods inside every `Object.assign(KIT|WALL_KIT, {` block and flag any name defined twice. A short Python regex over lines matching `^  name(g` works.
7. **`?looks`** shows every machine effect at once, and **`?seats`** (the performance engineer's) shows a stand-in on every seat.

## Questions answered by the user, and still open

- **Answered:**
  - Deck 1 is livened up (handover, Captain's walk).
  - Machines can be tapped and operated (systems and player own that).
  - The ready room stays locked until Pillar 3 progression.
- **Open:**
  - Should the cold store grow once carts run? That would need a plan change and the user's sign-off.
  - Should Deck 1 get the observatory-night style gatherings in its observation room too?
