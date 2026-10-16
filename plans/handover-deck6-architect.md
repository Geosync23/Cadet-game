# Handover: the Deck 6 architect

Written at the end of Pillar 2 (combined build 0.40.8, `claude/ship-integration` 980e6a9) for whoever takes this area over. Read it alongside `DEV_NOTES.md` (the build table, and my section "Places on Decks 4, 5 and 6"), `plans/pillar2-plan.md` and the deck plan pages.

## 1. Role, branch, builds and ownership

- **Role:** Deck 6 architect. I built Deck 6 (Pillar 0), then places on Decks 4, 5 and 6 (Pillar 1, workstream 3a), then the utility rooms on Decks 4, 5 and 6 and the gym machines (Pillar 2, A5a).
- **Branch:** `claude/deck-architect`. Push only there; the lead merges it into `claude/ship-integration`.
- **Build numbers:** 0.17.x (Pillar 1 places) and 0.30.x (Pillar 2; last was 0.30.10). Bump both the header line (`build 0.30.x`, near the top of the file) and `GAME_BUILD` (section 13), and add a DEV_NOTES row each turn.
- **Report:** to the lead after every push: branch, commit, build, files, what changed, tests, judgement calls, questions.

**What I own in `starship-cadet.html`:**

- **Decks:** `DECKS[4]`, `DECKS[5]` and `DECKS[6]`, including their `places`, `machines` and `service` lists, `dress()`, rooms and doors. Exception: the officers' corridor cabins on Deck 4 were laid out long ago; take care with the cabin generator.
- **Kit:** the `UTILITY ROOMS KIT` block just before `DECKS[4]` (the `UT` materials and every utility-room piece), plus the gym `treadmill`/`rower` kit's `place` option and the `beltTex` texture.
- **Shared, inert engine bits I added** (keep them inert):
  - `floorSeeds` (0.17.1) and `still` floors (0.30.1), both in the floor painter in `buildDeck`.
  - Service hatches (0.30.1): `hatchPassable` and the `who` argument on `edgeBlocks`/`edgeOpen`/`findPath`/`innerBlocks`/`collide`.
  - The `MOVERS` list (0.30.6/0.30.7).
- **Not mine:** `crewPath` / `crewPose` / `placeBusy` / `BUSY` are the sim engineer's (section 10). I added the `who` lines to `crewPath` once, at the lead's request.

**Test script I own:** `deck_check.py`. The others (`cadet_test.py`, `day_check.py`, `machine_check.py`, `player_check.py`) belong to other sessions; I only run them.

**Plan pages I keep:** `plans/deck4-plan.html`, `deck5-plan.html` and `deck6-plan.html`. Each has a "Utility rooms" section showing what was built.

## 2. What I built, and the formats other sections rely on

### Places (Pillar 1, still the base format)

`{ id, type, at: [c, r], face, pose, room, xy?, walk?, anim?, y?, machine?, stock? }` in each deck's `places` list.

- **Beds** are `4-B<room>-<1..6>` (48 bunk berths) and `4-01`..`4-24` (cabins).
- **`machine: '<id>'`** marks a machine's service place. The schedules never hand those out as desks.
- **Type `storage`** (0.30.8, Deck 5) covers places for Works errands, which the planner never hands out as work stations:
  - 5-parts-1..4 face the storage shelves. Each has `stock: [...]`, the part names the systems engineer uses.
  - 5-make-1/2 are at the lathe and fabricator.
  - 5-hold-1/2 are in the cargo hold.
  - 5-cart-1/2 are beside the cart docks.

### Service hatches (0.30.1)

To open a built utility room to the player and Works crew:

1. Give its doorway `'hatch'` in `doors`.
2. Add the key to the deck's `service: [...]`.

What it does:

- `hatchPassable(key, who)` is true only there, and only for the player (`who.isPlayer`) or Works crew (`who.dept` or `who.p.dept` is `'works'`).
- Pathing and collisions take an optional `who`. Without it, nothing changes, so every older call site behaves as before.
- A service hatch loses its locked-door tap text, and opens slowly when the player is near.
- Every other hatch, such as the spine ladder's, blocks everyone.

### `still: true` floors (0.30.1)

The room's floor draws no random numbers, like the lift. Use it on any room that used to be `void`, or the whole deck's later random sequence shifts (see Gotchas).

### Machines (0.30.2 on)

`machines: [{ id, kind, at, room, face, panel }]` per deck.

- `at` is the machine's tile in front of its panel.
- `face` is the way the machine's front faces, toward the panel.
- `panel` is where the tech stands. Each machine has exactly one place `<id>-svc`: type `work:works`, pose work, with `machine: '<id>'`, on the panel tile, facing the machine.
- There are 29 machines: 7 on Deck 4, 18 on Deck 5 and 4 on Deck 6.
- Kinds were agreed with the systems engineer: e.g. `heatpump`, `lights` (the tier-1 closets), and `airplant` (5-scrubber-1/2, ship-wide).
- Wall-mounted machines (valve stations, conduit boxes) have `at` equal to `panel`.

### Gym machines (0.30.6)

- Kit pieces given `place: '<id>'` push a ticker onto `MOVERS`. Each frame it is ticked with `placeBusy(place)` (section 10).
- The treadmill belt scrolls and its console brightens; the rower seat slides. At rest nothing moves.
- Deck 3's gym furniture line passes `place: '3-gym-1'..'3-gym-4'`. That is the one line of `DECKS[3]` I touched; the places themselves are the bridge architect's.

### Cart dock hook (0.30.10)

The `cartDock` kit, given `dock: n`, keeps its parked cart as one group and calls `cartDockLive(cartGroup, n)` if that function exists. Section 17 (B3) hides the cart while it's out.

### What's in the rooms

- **Deck 4:**
  - air scrubbers (s): 2 scrubbers, a duct and a filter rack;
  - heating plant (t): a heat exchanger, 2 heat pumps piped to it, and a tank;
  - junior closet (k) and officers' closet (y): light and power cabinets;
  - junior stores (u): shelves.
- **Deck 5:**
  - air plant (a): an electrolyser, 2 oxygen-cell banks, and 2 airplant stacks on the Fan-hall wall;
  - manifold room (n): the valve wall, 2 pumps and a tank;
  - battery room (y): 4 banks and the charge controller;
  - utility closet (u): a cabinet;
  - cart bay (m): 2 docks with carts;
  - cargo hold (c): racks and crates;
  - pipe galleries (g, h): valve stations.
- **Deck 6:** the 2 power junctions (j, J) and the 2 crawlways (c, C), with cable trays and inspection boxes.

## 3. Republishing the user's playable link

The link is https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y. I own it, and republish only when the lead asks and names a build. Version 11 is 0.40.8.

1. **Get the file:** `git fetch origin claude/ship-integration`, then `git show <commit>:starship-cadet.html > <scratchpad>/pub/starship-cadet.html`. Publish it exactly as in the repo, with no edits and no URL flags.
2. **Check the build:** `grep -o "build 0\.[0-9.]*\|GAME_BUILD = '[^']*'"` must show the build the lead named, twice.
3. **Smoke test:** load it with `cadet_test.py`'s `Game` class (see Testing). Check `GAME_BUILD`, the room ("Bunk 1"), the deck and the clock ("Day 1, Monday 06:00"), and that there are no errors.
4. **Publish:** use the Artifact tool, publishing with `url` = the link above, `file_path` = that file, and a `label` like "Build 0.40.8". If this conversation hasn't read the artifact yet, do a plain `read` first. Keep the file's own `<title>`.
5. **Verify:** read it back with `path: "index.html"`. The repo file must sit inside the host's wrapper byte for byte (find the first 200 characters, then compare the whole length).
6. **Report:** tell the lead the version number, and that the link stays private (the user shares it from the page's Share menu).

## 4. State at 0.40.8: loose ends, weak spots, next fixes

- **Fixed but worth knowing:** 0.30.1 to 0.30.10 are all in 0.40.8. `byFace` on Deck 6's hull came from the performance engineer and is in too.
- **Tier locks don't exist yet.** Service hatches let the player and Works crew into every utility room. `hatchPassable` is the single place to add them later.
- **The cargo hold's shuttle-bay hatch (v,10,12) is sealed on purpose.** Opening it would let crew routes to the shuttle bay cut through the hold. If B3 wants it open, check the routes first.
- **The Fan hall (Deck 5, F) stays locked.** Its hatches into the air plant and manifold room (h,38,5 and h,38,11) are sealed, not service hatches. The air plant and manifold room are reached through the pipe galleries.
- **Curved bow corners have tiles that are "in the hull" but too close to stand on** (Deck 5 a/n, Deck 4 x/y). Machines can sit on them, but panels can't. Check `STAND`, not just the map.
- **Draw calls:** Deck 5 is 324 by the lift (the carts are unmerged so they can hide). day_check peaks are within 450.
- **What I'd do next:**
  - Give the Deck 6 crawlways a second inspection point each (15 tiles long, one box each).
  - Give machines a visible state hook, like `cartDockLive`, so B1's worn and broken states can show (a flickering screen, a red light).
  - Add a `hoverCart` kit piece for carts on the move, if B3 wants one. I offered it.

## 5. Gotchas: what broke before, and merge traps

- **The random sequence.** `R()` is one seeded sequence per deck build. Anything that draws a different number of random numbers shifts everything after it: floor grain, then furniture, then crew choices. So:
  - shared kit made at load never calls `R()`;
  - new furniture goes **last** in `dress()` and uses no `R()`. The old `shelving` kit calls `R()`, so use `utilShelf`;
  - a room that loses `void` must get `still: true`;
  - when a layout changes west of a column, `floorSeeds` restores the old sequence east of it. Deck 4 uses column 21.
- **Name clashes in the single file.** My `let BUSY = []` clashed with section 10's `const BUSY = new Set()` and stopped the whole game loading. It's now `MOVERS`. Before adding a top-level name, grep for it.
- **Coplanar faces flicker on phones.** A piece whose back sits exactly on a wall's inner face (0.1 in from the tile edge) is coplanar. Pull it 0.02 in, or make it overlap.
- **Tall things in the camera's way.** Overhead pipes and trays must be `tall: true` so they fade. The fade tests each piece's **centre**, so lay long runs in short pieces (about 2.5 to 3 tiles).
- **deck_check vs reality.** A room behind a service hatch is "shut" unless the check walks as the player (`findPath(..., player)`). work:works and storage places use the Works flood fill. Other place types can't be behind a service hatch.
- **Merge traps:**
  - Every merge of `claude/ship-integration` conflicts on the two build lines; keep mine.
  - DEV_NOTES build rows can conflict too; keep both sets, in number order.
  - After merging, grep that `MOVERS`, `hatchPassable`, the `who` in `crewPath`, `machine:` on every `-svc` place, and Deck 6's `byFace` all survived.
- **Renderer noise.** Some text edits nudge a few pixels by 1 level in the headless renderer. cadet_test reports "ALL IDENTICAL (apart from renderer noise)". Differences above 1 level are real.

## 6. Testing my area

Environment:
- `CADET_WORK=<scratchpad>`, with three.js at `<scratchpad>/three/package/build/three.min.js`.
- `CADET_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.
- Run from a scratch folder, because the scripts write PNGs to the current directory.

Every turn:

- `python3 cadet_test.py OLD.html NEW.html`: Deck 4; screenshots must be identical unless Deck 4 changes on purpose.
- `python3 deck_check.py NEW.html`: all six decks.
- `python3 day_check.py NEW.html 1`: two days when schedules could change.
- `python3 machine_check.py NEW.html` and `python3 player_check.py NEW.html`.

Containment proofs, which I wrote as scratch scripts. They're easy to rebuild with `cadet_test.py`'s `Game` class and its direct-eval hook:

- **All six decks, pixel by pixel:** load, `crewNearDoor = () => false`, click `#crew` to hide crew. For each deck, take a day, night and `setZoom(.55)` wide shot. Compare two builds.
- **Deck structure:** dump MAP, EDGES (type plus `+svc`), BLOCKED, ITEMS, CLOSED_DOORS, ROOM_TILES and the seed after the build. Check that every change touches only the rooms meant, and that 400 sample routes outside those rooms are identical, with and without `who = player`.
- **Room screenshots:** set `wallsMode = 'down'; wallsLow = true`, move the player and the target to a tile, `setZoom(1.3)`. Also shoot in `'auto'`, so the tall-piece fade shows.

## 7. Ideas and open questions for the user

- **Tier access:** should utility rooms be locked by tier (Tier 1 closets, Tier 2 plant rooms, Tier 3 batteries and junctions), as the old tap texts said? The hook is ready.
- **Visible wear:** machines in poor shape could show it (a dim screen, a dripping pipe, a red light). That needs a small agreed hook with the systems engineer.
- **The cargo hold's shuttle-bay hatch:** open it when the shuttle starts flying cargo runs?
- **More life in the utility rooms:** a radio left on in the heating plant, a mug on the breaker cabinet, a sign about the oxygen cells. Cheap touches that make Works rooms feel lived in.
