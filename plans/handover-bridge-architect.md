# Handover: the bridge architect (Decks 1 and 3)

Written at the end of Pillar 2, against combined build 0.40.8 (`claude/ship-integration` 980e6a9). Read `DEV_NOTES.md` sections "Deck 1, the Bridge (0.8.x)", "Places on Decks 1 and 3 (0.18.x)" and "Pillar 2 on Decks 1 and 3 (0.31.x)" alongside this; they hold the detail. This note is the map.

## Role, branch, builds

- **Role:** architect of Deck 1 (the Bridge) and, from Pillar 1, Deck 3's places and Pillar 2 rooms. Deck 3's shell, rooms and dressing were built earlier (0.5.x–0.6.x) by the first lead; I've owned `DECKS[3]` since 0.18.
- **Branch:** `claude/deck1-scale`. (The brief named `claude/deck1-bridge`; the work has lived on `deck1-scale` since the 0.12 rescale, and the lead merges from there.)
- **Builds:** 0.8.x (Deck 1 built), 0.12.x (Deck 1 scaled up), 0.18.x (places on Decks 1 and 3), 0.31.1–0.31.5 (Pillar 2, workstream A5b). The lead folds them into 0.40.x.

## What I own in `starship-cadet.html`

All inside section 4 (decks):

| What | Where (search for) |
| --- | --- |
| Deck 1 kit: materials `BRG`, pieces via `Object.assign(KIT, …)` and `WALL_KIT`, `bridgeViewscreen` | `const BRG = {`, just above `// DECK 1: BRIDGE` |
| `DECKS[1]` | `DECKS[1] = {` |
| Deck 3 kit (A5b): `till`, `basketStack`, the utility kit and helpers `pipeX`, `pipeZ`, `statusLights`, wall kit `relayBox` | `// ---- Deck 3 kit (A5b` |
| `DECKS[3]`: its `places`, `machines`, `service`, rooms and `dress` | `DECKS[3] = {` |
| `grabShelf` in shared kit (the `o.live` hook only) | `grabShelf(g, o = {})` |

Plus the plan pages `plans/deck1-plan.html` and `plans/deck3-plan.html` (each has a "Utility rooms (built in 0.31.3)" section with a sketch).

**Not mine, but I put one line in:** section 14's `schedData` skips places that have `machine` (`if (!p.machine)`), so a machine's panel spot is never handed out as a desk. The sim engineer knows.

## What I built, and what other sections rely on

**Deck 1, the Bridge.** 22 × 12 tiles. Lobby, bridge with the command ring and viewscreen, observation room, ready room (locked, Captain only), washroom, and three service rooms: utility closet `k`, relay room `u`, sub-floor crawl `c`.

**Deck 3 utility rooms (0.31.3).** Water recycler `R`, galley plant `g`, irrigation `i`. Each has machines, pipes and a floor you can stand on (`still: true`, so the floor draws no random numbers). The hatches into them are listed in the deck's `service` list, so the player and Works crew can pass them and nobody else can. Deck 1's `k`, `u` and `c` are done the same way, plus one new hatch, `v,10,10`, between the relay room and the crawl.

**Activity furniture (0.31.1–0.31.2).** A till on the store counter and a basket stack by the store door. The store is staffed: `3-store-1` (storekeeper, behind the till) and `3-shop-7` (shopper paying, in front). The three treadmill places carry `y: 0.16`, so runners stand on the belt. The rower is `anim: 'row'`.

**Shared formats other sections rely on** (if you rename or move any of these, tell the owner first):

- **Places** (sim engineer, section 14; performance engineer, 8 and 8b): `{ id, type, at, xy?, walk?, face, pose, anim?, y?, machine?, room }`. 36 places on Deck 1 and 192 on Deck 3. Ids follow `<deck>-<what>-<n>`. The full list of id families is in DEV_NOTES "Places on Decks 1 and 3".
- **Machines** (systems engineer, section 17): `{ id, kind, at, room, face, panel }`.
  - Deck 3 has 12: `3-oven-1`, `3-oven-2`, `3-range-1`, `3-galleyplant-1`, `3-chiller-1`, `3-recycler-1`, `3-filter-1`, `3-pump-1`, `3-uv-1`, `3-lights-1`, `3-nutrient-1`, `3-irrigation-1`.
  - Deck 1 has 5: `1-relay-1`, `1-relay-2`, `1-junction-1`, `1-lights-1`, `1-databus-1`.
  - Each machine has a `<id>-panel` place (`work:works`, `machine: '<id>'`) standing on its panel tile.
  - The ids match the systems engineer's old stand-ins on purpose. A deck's real machine replaces the stand-in with the same id.
- **Grab shelf** (galley engineer, section 16): `grabShelf` with `live: true` hands its top two rows (wraps and rolls) to `galleyShelfRows(g, ys)`. That function must stay a function declaration, so it exists when Deck 3 is built at load.
- **Cold store** (systems engineer, B3 restock carts): `3-cold-1` [36,1] and `3-cold-2` [37,1], type `storage`, facing the north shelves. Section 17's `COLD_AT` names them. The cart route is lift → galley back door `h,38,9` → galley → cold store door `h,36,3`, and the cart parks on row 2.
- **Gym places** (Deck 6 architect's moving treadmill belts and rower seat, via `placeBusy(id)`): `3-gym-1..3` (treadmills) and `3-gym-4` (rower). Keep these ids.

## State at 0.40.8

- All checks pass on the combined build, per the lead.
- **Stale line in DEV_NOTES:** the "Pillar 2 on Decks 1 and 3" section still says some machine kinds aren't in `MACHINE_KINDS`. That's no longer true: since 0.33.2 every kind I use is registered. Fix the line next time DEV_NOTES is touched.
- **Weak spots:**
  - The cold store is tiny: 2 × 2 tiles you can walk on. A cart, two unloaders and a passer-by will jostle. If restocks look crowded, widen it into the galley plant's side, which would need a plan change and user sign-off.
  - Deck 3 is the busiest deck for draw calls: day_check peaks around 417 of the ~450 budget. Any new Deck 3 kit should reuse existing materials (the utility kit does) or merge meshes.
  - The machine panel places sit behind service hatches. Crew who aren't Works can't reach them, which is correct, but any new code that hands out places must skip `machine` places too, as `schedData` does.
  - Some places use `walk` tiles up to 2.5 m away (booths, hull benches). They look fine in the crowd, but a full rig sliding in can clip a table edge.
- **What I'd fix next:**
  - Turn on `hull.byFace` for Decks 3–6 (fewer draw calls). It changes their hull-piece tables, so it needs its own regression pass and the lead's OK.
  - Doors: group each leaf's six materials into two (identical pixels, about a third of the door draw calls). This is shared code, so it's the lead's call.

## Gotchas (things that broke before)

- **Random numbers.** Kit made at load must never call `R()`. If it does, every deck after it shifts and the regressions stop being pixel-identical. Utility floors use `still: true` for the same reason.
- **"Pixel-identical with crew hidden" isn't quite enough.** Hidden crew still open doors. My comparison script also stubs `crewNearDoor = () => false`. Without that, doors on other decks can differ for no real reason.
- **Panels handed out as desks.** Before the `if (!p.machine)` line, Works crew who'd run out of desks were sent to machine panels behind hatches, and day_check failed with "no way to their place".
- **The hull splitter bug.** It made Deck 1 cost 589 draw calls empty; it's fixed by `byFace` on Deck 1 only (see DEV_NOTES "Deck 1").
- **Merge traps.** Almost every merge from `ship-integration` clashes on two lines, the HUD build line and `GAME_BUILD`, plus the build table in DEV_NOTES. Keep your build number in both lines and keep both sides' DEV_NOTES rows, in order. Watch for a row the lead already copied across, which leaves a duplicate.
- **Deck_check is strict about place types.** A new type has to be in its `TYPES` list (or match `work:…`). In 0.18.2, 14 places had to sit out a build for this.
- **Machine kinds.** A kind the registry doesn't know is quietly dropped. Check `MACHINE_KINDS` in section 17 before inventing one.

## How to test my area

Set `CADET_CHROME=/opt/pw-browsers/chromium`. Then, each turn:

1. `python3 cadet_test.py OLD.html NEW.html` should print **ALL IDENTICAL** (OLD is the current `ship-integration` build).
2. `python3 deck_check.py NEW.html` should print **DECK CHECK OK**. On Decks 1 and 3: no unreachable tiles or items, no bad places, no bad machines, and machines 5 and 12. Deck 1 by the lift is about 309 draw calls, Deck 3 about 331.
3. `python3 day_check.py NEW.html` should print **DAY CHECK OK**, with every deck's peak under about 450 (Deck 3 is the tightest).
4. `machine_check.py`, `food_check.py` and `player_check.py` should all print OK. They belong to other sessions, but my data feeds them.
5. **Other decks pixel-identical:** screenshot every deck you didn't touch in both builds, with crew hidden and `crewNearDoor` stubbed (see above), from the lift, zoomed out, rotated, walls down and at night. Zero differing pixels is the bar. If they differ, find out why before moving on.

## Ideas and open questions for the user

- **Deck 1 feels quiet.** Only about 10 crew work there. A shift handover at the command ring, or the Captain's evening walk through the observation room, would give it life without new rooms.
- **The ready room is locked to everyone but the Captain.** Should the player ever get in, for example when summoned for a talk? That would be a nice progression moment.
- **Utility rooms are reachable but plain to visit.** Do you want the player to be able to tap the machines for a line of text about each (as with furniture), or only see them through the job board?
- **The cold store size** (see "Weak spots"): fine for now, but worth a look once restock carts are visible.
