# Starship Cadet: dev notes 3

Read this first in any new session, together with **design-doc-v4.pdf** and **starship-cadet.html** (build 0.8.4). The design doc is the source for what the game is; these notes cover the build: what's in it, how the code works, the rules, testing and what's next.

This file replaces DEV_NOTES_2. The repo holds it with the design doc, the build, the deck plans in `plans/` and cadet_test.py. Git keeps every earlier version, so files keep stable names (no version suffixes).

**Deck 3 is complete (0.7.0, with the promenade dressed and review fixes) and signed off ("ok for now").** Plan pages for Decks 1, 2 and 6 are in `plans/` (Deck 2 is being reworked). Building them falls to the deck architect when the lead says go; see TEAM.md.

Nine small updates for the design doc when it's next edited:

- Mother Fen is now Chef Auda Brennan, who runs the galley and mess hall.

- Deck 3 gains three rooms along the starboard side of the promenade: a gym, a small crew store, and call-home booths for recorded messages home. Its layout is a central promenade from the garden (stern) to the lounge (bow), with the lift in a plaza halfway along.

- Two meals a day, not three: breakfast and dinner. Each is served over a window, not at a set time. Breakfast 06:00 to 08:00 catches the night shift coming off at 06:00 and the day shift before 08:00. Dinner 17:00 to 20:30 catches the day shift coming off at 17:00 and the night shift before 21:00. The galley also keeps a grab-and-go shelf for anyone running late. Remove the line about crew asking you to join them at lunch.

- There is no freight lift. Supplies leave Deck 5's cargo hold on hover hand carts and go up the main lift (a job in step 7). Deck 5's `m` is now the Cart bay.
- Deck 3's bow lounge is one big room on one floor, not two levels.

- Deck 4's bow nook is now the music room: a soundproofed room at the end of the officers' corridor, with a door.

- The lift car is a walkable room on every deck.
- The spine's trunks and ladder can be seen behind glass beside the lift.
- Pell works on Deck 5 for now, until shifts move people between decks.


## Current build: 0.7.4 (about 4,650 lines)

Two decks, joined by a working lift. Deck 4 (Quarters) plays as before. Deck 5 (Operations) is built and dressed: the Works complex, storage, machine shop, shuttle bay with the shuttle Tern, the door gear and the fan. Pell works there.

| Build | What it added |
| --- | --- |
| 0.5.1 | Step 6c turn 1, Deck 5's shell. `DECKS[5]` straight from the plan. Steel, haul, bay and grate floors; hazard bands at doorways; the landing pad. Inner glass walls (`'glass'`) and service hatches (`'hatch'`). Sealed rooms with tap text. Fixed: a sealed door's tap always walked you to its north side, so doors with the locked room to the north said nothing. |
| 0.5.2 | Turn 2, the lift panel and ride. Point lights padded to `LAMP_SLOTS` on every deck so changing decks doesn't recompile shaders. |
| 0.5.3 | Turn 3, the Works complex dressed: job board, tool wall, benches, lockers, tea corner, washroom, storage aisles, machine shop. Fade groups for storage aisles. |
| 0.5.4 | The lift car as a room you walk into, on both decks (asked for mid-step; replaced turn 2's tap-the-door ride). |
| 0.5.5 | Turn 4, the shuttle bay: shuttle, bay doors, booth, door gear and fan (both turning, `SPINS`). Pell moved to Deck 5. Step 6c done. |
| 0.5.6 | Deck 4's dead space round the lift filled. Spine rooms for the trunks and ladder behind glass; benches, plants and a deck directory in the lobbies. Tap text for things behind glass. |
| 0.5.7 | The trunks and ladder redrawn to fit the one row beside the car, and carried through Deck 5's spine so they line up deck to deck. |
| 0.5.8 | The hull no longer follows you: hull walls facing the camera stay low, the far ones stay up. The Walls button cycles Auto, Down and Up for inner walls. Stars: a drifting two-layer sky round the ship, and window stars and nebula sliding aft. |
| 0.5.9 | Windows are real openings onto the sky (the painted nebula and stars behind the glass are gone). Deck 4's bow nook became the music room: a stage round the bow windows with drums, guitars, amps and a mic, a grand piano, beanbags, a record cabinet, soundproofing panels, an instrument rail and a gig poster. Double doors from the corridor (`v,44,9`, `v,44,10`). |
| 0.6.0 | The main lift has one wide door on each side instead of two narrow ones: paired lift edges share one pair of leaves, with no post or corner block between them (`liftJoint`). No freight lift: Deck 5's cargo hold and Cart bay tap text changed. |
| 0.6.1 | The lift car is 2 × 3, big enough for a hover cart: it takes over the trunks row, keeps the ladder row, and each side is one three-tile door. Choosing a deck walks you to the panel on the car's back wall, where you reach out and press it before the ride starts. |
| 0.6.2 | Deck 3, turn 1: the shell. `DECKS[3]` from plans/deck3-plan.html: map, hull, doors, windows, floors (new `deck`, `gym` and `garden`), sealed service rooms, the lift and ladder, plaza benches and plants, name plates and the deck directory. Rooms are walkable and named but not furnished yet. The deck directory now marks whichever deck it's on. |
| 0.6.3 | Deck 3, turn 2: the mess hall (44 seats: four long tables of eight, three round tables of four), the serving line, the galley and the walk-in cold store. A new edge type, `pass`: the serving counter through the mess–galley wall. |
| 0.6.4 | Curved inner walls (`curves` in a deck definition), and Deck 3, turn 3: the bow lounge, with a curved bar round the galley door, two planted glass screens on one arc, booths, high tables, and a window end with a sofa, armchairs, two quiet corners and a telescope. |
| 0.6.5 | Deck 3, turn 4: the hydroponics garden (grass, grow racks under pink light, raised beds, trellises, fruit trees, a pond with benches, a stepping-stone path, a herb wall, a big tree and ground cover everywhere), the infirmary and exam room, public washrooms (all toilets), the gym, the crew store and the call-home booths. The lounge's glass screens are shorter, so the way round them is open. |
| 0.6.7 | Deck 3, turn 5: crew. Chef Brennan works the galley (haunts `K`, `M`, `G`; spots at the ranges, ovens, prep island, dish pit, pass, her stool and the mess floor). Rina is on duty in the infirmary (haunts `I`, `X`; spots at the desk, beds, cabinet, supplies and exam room). Both are `deck: 3`, which leaves five crew on Deck 4. Step 6d done. |
| 0.6.8 | The promenade dressed (asked for at review): two planter islands down the middle with a tree, flowers, a bench facing each lane and lamp posts at the ends; the route-map kiosk where the promenade leaves the plaza; benches and potted plants by the garden doors. New `deck_check.py`. |
| 0.6.9 | Review fixes. Planter islands smaller (two columns each, cols 29–30 and 35–36) with no lamp posts. Snug collision (`snug: true` in `place`): benches by the lifts on Decks 3 and 4 and by the garden doors push you off their real outline, not whole tiles. Lift doors sink into the floor instead of sliding out past the frame. |
| 0.7.0 | Planter islands longer (2.48 m, three columns each, the same width) and their trees taller (trunk 1.9 m, crown raised 0.6 m; trunk thickness and crown size unchanged). |
| 0.7.1 | Step 6e, Deck 6, turn 1: the shell. `DECKS[6]` straight from plans/deck6-plan.html (36 × 12, `lift: [19, 6]`, seed 60661, `hazard`, no windows): lobby, overlook, watch room, the locked engine room, engine control and reactor seen through glass, sealed junctions and crawlways, plates, lift panels, the deck directory, the foot of the trunks and the bottom of the ladder behind glass. No new kit or engine changes. Deck 4 ALL IDENTICAL against 0.7.0. |
| 0.7.2 | Deck 6, turn 2: the engine room, seen through the overlook glass: the drive housing across the stern with its glowing mouth, three drive coils down the middle (copper windings, a cage, a core whose glow breathes, one coil after another), copper feeds between them, catwalks either side and a landing by the stair door. The overlook gets a rail along the window, two benches facing the coils and the first-week board. New engine list `PULSES` (glow on the game clock). New kit `driveCoil`, `driveHousing`, `pipeRun`, `catwalk`, `overlookRail`; materials `ENG`. Deck 4 ALL IDENTICAL. |
| 0.7.3 | Deck 6, turn 3: the reactor (a ribbed shield drum with glowing ports, the core showing through a ring on top, conduits, and the coolant loop on stands with spokes to the drum; its green glow breathes slowly) and engine control (the board along the reactor window, two chairs, the mimic panel of the ship's power). Radiation signs either side of the reactor door. New kit `reactorDrum`, `controlBoard`; wall kit `mimicPanel`, `trefoil`; `ENG.mimic` and `ENG.trefoil` are canvas panels drawn at load (no `R()`). Deck 4 ALL IDENTICAL. |
| 0.7.4 | Deck 6, turn 4: the watch room (two mustard armchairs on a rug, the kettle by the junction hatch, a real lamp, a panel heater, a shelf of engine logs), coolant risers with valve wheels and steam in the lobby's corners, a bench facing the lift, and Deck 6's mood lighting (`light` in a deck definition tints the hemisphere and sun; Deck 6 runs warm and dim). Deck 6 done. Decks 3, 4 and 5 pixel-identical to 0.7.0, day and night. |
| 0.8.1 | Step 6e, Deck 1, turn 1: the shell. `DECKS[1]` from plans/deck1-plan.html (20 × 10, `lift: [8, 5]`, seed 10109): lobby, bridge, observation room, washroom, the locked ready room, sealed closet, relay room and crawl; plates, lift panels, the deck directory, the trunk head (new `trunkHead`, brass plate) and the top of the ladder behind glass; cooler mood light. Hull pieces split by facing (`hull.byFace`, Deck 1 only): the empty shell went from 589 draw calls to 256. Decks 3–6 pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.8.2 | Deck 1, turn 2: the viewscreen and the bridge floor. `bridgeViewscreen` lays a screen strip just inside the bow hull (bearings −60° to 60°), split over the hull pieces so it drops with them; its starfield (nebula, a ringed planet, stars from a fixed hash) drifts slowly. New floor `bridge` (blue-grey carpet tiles) and a deck hook `floorArt`, which Deck 1 uses to inlay the command ring (a shaded well, brass step edge, teal light line). Decks 3–6 pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.8.3 | Deck 1, turn 3: the command ring. The command rail (a `bar` curve, 140°–220° behind the ring), a brass step strip and a light line round the well, the Captain's chair with a seat either side, helm and ops consoles with their seats, and four rear stations with labelled screens (Watch and Survey on the ready room wall, Comms on the washroom wall, Works by the floor hatch, which is painted into the floor). New kit `commandChair`, `bridgeConsole`, `rearStation`; screens from `stationScreen`. Decks 3–6 pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.8.4 | Deck 1, turn 4: the observation room (a racetrack conference table for ten, the briefing screen on the lobby wall, the window seat across the stern, the Captain's tea, a lamp, plants), the locked ready room (desk facing the door, the Captain's chair, two visitors' chairs, a bookshelf and the Admiral's aquarium) and the washroom (compact toilet and basin). The viewscreen's strips merge to two draw calls per hull piece. Deck 1 done. Decks 3–6 pixel-identical, Deck 4 ALL IDENTICAL. |

Deck 4's static screenshots are pixel-identical from 0.5.0 through 0.5.7. The only Deck 4 changes are the spine and lobbies (not in the harness views), and crew routes that shifted when Pell left and when the car and benches changed which tiles are walkable.


## How decks work (section 4)

Unchanged from DEV_NOTES_2 in outline:

- `SHIP` holds state that outlives a deck.
- 4a is the current deck: per-deck `let` tables, replaced by each build.
- 4b is the shared kit, made once at load.
- 4c is `buildDeck(def)` and `unloadDeck()`. A build reseeds the random generator with `def.seed`, and unloading frees everything made after the build's id watermark.
- 4d holds the deck definitions in `DECKS`.

**Deck definition fields:**

- **Required:** `num`, `name`, `seed`, `lift` (the car's centre in tile units), `map`, `doors`, `rooms`, `windows`, `closedDoors`, `hull` and `dress(d)`.
- **For the lift:** `blurb` (subtitle in the lift panel) and `arrive` (toast text on arrival).
- **Optional:**
    - `hazard` paints hazard bands at doorways onto steel floors.
    - `markings` gives keep-clear outlines: `[i, j, w, d]` in tiles.
    - `plates` and `sconces`, plus Deck 4's `cabins`.
    - `lockedRoom(r)` gives tap text for locked rooms.
- **Deck 5 also has:**
    - `sealed`: door key → room letter. Its `closedDoors` are built from the rooms' `tap` text.
    - `workLights`: wall lights listed in data and placed by its `dress`.

**Door types** in `doors`:

| Type | What it is |
| --- | --- |
| `door` | Slides open for anyone nearby. |
| `closed` | Shut; tap text comes from `closedDoors`. |
| `hatch` | A shut service hatch with hazard leaves. Counts as closed everywhere. |
| `glass` | An inner window: wall-textured sill, pane and header, lowering with the cutaway like a wall. |
| `lift` | Walkable lift doors. Opens for anyone near, unless a ride holds it with `d.force`. |

Two types are generated, never listed: `open` (between two `hall` rooms) and `hull`. An edge between two solid (void) rooms doesn't exist, so a door listed there does nothing.

**Room flags:**

| Flag | Meaning |
| --- | --- |
| `name` | Shown in the HUD. |
| `floor` | Floor type (below). |
| `hall` | Hall rooms join each other with no wall. |
| `void` | A solid block with hatch texture. |
| `tap` | Text for sealed rooms. |
| `pad: [i, j, w, d]` | The shuttle pad marking. |
| `spine` | The floor draws nothing from the random sequence. |

**Floor types:** `warm`, `wood`, `tile`, `plate`, `corridor`, `lobby`, `carpet`, `mess`, `steel` (diamond plate), `haul` (plate with lanes), `bay` (darker plate), `grate`, `lift` (ribbed rubber), `deck` (the promenade's pale planks, with guide stripes and an inlaid light line along the walls, for hall rooms), `gym` (flecked rubber), `garden` (green pavers). `carpet` only suits hall rooms: it draws a guide stripe wherever the next tile isn't a hall.

**Ship frame.** Every deck is placed so its lift centre sits at `LIFT_AT` (world −4, 0). The car and ladder therefore sit at the same world spot on every deck:

| Piece | Rows | World position |
| --- | --- | --- |
| Lift car `@` | 2 × 3 | x −5…−3, z −2…1 |
| Ladder row `Z` | the row below the car | z 1…2 |

The trunks run up behind the car's back wall. A deck with room above the car (Deck 4) shows them behind glass in a `Y` row there.


**Changing decks.** `goToDeck(n, at)`:

1. Hides the crew and unloads the current deck.
2. Builds deck `n` and indexes its room tiles.
3. Places you at world point `at` if that tile is free (a ride passes where you stood in the car), otherwise at the nearest open tile to the lift.
4. Activates the crew whose `deck` is `n`.
5. Refreshes what taps can hit and updates the HUD.


## Cutaway and sky (0.5.8)

- **Hull pieces.** Each room's hull run is split again wherever the outline turns to face a new way (bow, stern, either side). Each piece in `HULL_RUNS` has `face`, its outward axis. A piece is low when `face · camera > 0`, which on screen means the lower and right walls are low and the upper and left walls stay up, in every Walls mode. Hull edges follow the nearest piece facing their way.
- **R() is still drawn once per window span**, even when a span crosses pieces. Splitting must never change the count, or every later texture shifts.
- **Walls modes.** `wallsMode` is `'auto'`, `'down'` or `'up'` (`wallsLow` is true in `'down'`). Up keeps inner walls and solid spine blocks at full height; tall furniture still fades.
- **Sky.** `SKY` is a screen quad just inside the far plane, with additive stars, so it only shows where nothing else drew. It has its own random sequence, lives in the scene (not a deck), and costs one draw call. Two layers drift aft on screen at different speeds, with slight parallax as the camera moves. Night brightens it (`uK`). With reduced motion it drifts at a quarter speed.
- **Windows** (0.5.9) have nothing behind the glass, so you see the sky through them. `nebulaTex` and `starTex` are still drawn at load, and `R()` is still called once per window span, to keep the random sequence.

## Curved inner walls (0.6.4)

- **A deck lists them in `curves`.** Each has an `arc`, `[cx, cz, r, a0, a1]` in tiles and degrees (0 points to the bow, 90 to starboard), or `pts`, `[[x, z], ...]` in tiles, for a smooth Catmull-Rom line. `out` (1 or −1) names the customers' or front side; `it` makes it tappable at its middle.
- **Kinds:**
    - `wall`: full height, wall texture, end posts. It joins `RUNS` (with `curve` set) and drops with the cutaway like an inner wall. Tested, not used yet.
    - `glass`: a planted base 0.8 m high with a glass screen and a brass rail to 2.1 m.
    - `bar`: a counter 1.1 m high with a wooden top overhanging the `out` side, a brass foot rail and an amber under-glow.
    - `planter`: a low planted wall 0.7 m high.
- **Built by `buildCurves(def)`,** after `dress`, into `deckRoot`. `curveStrip(P, y0, y1, o0, o1, mats)` makes any strip along a line, like `hullStrip` does for the hull.
- **Walking:** tiles whose centres are within the curve's half-width + 0.3 of the line are added to `BLOCKED`, and `collide` pushes walkers off each segment in `CURVE_SEGS`.
- **Not yet:** curved walls don't replace grid edges, so a room's shape is still its tiles. Rounding a room's corner (the promenade's corners at the plaza, say) would also need the floor painter to repaint the sliver of tile left outside the curve with the neighbouring floor, and the two grid edges to stop drawing while still blocking. That's the next step when we want it, and the bridge's command ring will want it.
- **Materials:** `curveWallMat` (the wall texture, repeating along the curve) and `CURVE_MAT`. No `R()`.

## The bow lounge (0.6.4)

- **Bar end:** the curved bar (`arc: [41, 5.6, 2.6, -90, 90]`, `out: -1`) encloses the galley door, with two `backBar` units against the aft wall and `barTaps` on top. Eight `barStool`s face it at radius 3.12. Two `highTable`s to port, three `booth`s along the aft wall to starboard.
- **The glass screens** are one arc (`[40, 11, 7]`), −45° to −16° and 16° to 45°, leaving the way from the promenade doors to the windows open.
- **Window end:** rug, navy sofa facing the bow, coffee table, two rust armchairs, a lit floor lamp; quiet corners (tea table and two olive armchairs) at z 6 and 16; the telescope.
- New kit: `booth`, `backBar`, `barTaps`, `barStool`, `highTable`. Materials in `LNG`. Every lounge tile can be reached.

## Deck 3, turn 4 (0.6.5)

- **Garden `G`:** floor `garden` is now grass (it draws from Deck 3's random sequence, which is fine on a new deck). Grow racks along both hulls, raised beds (greens, herbs, tomatoes, flowers), two citrus trees on moss, trellises, a pond with benches round it, a stepping-stone path from the promenade doors, garden lamps, a big tree, bushes, ground cover and drifting pollen. The herb wall is by the door.
- **Infirmary `I` and exam room `X`:** four curtained ward beds under the port windows, the front desk by the wide doors, a medicine cabinet; the exam bed and its desk.
- **Washrooms `w`:** `furnish('w', 'washroom', { toilets: true })`. The washroom template takes `toilets` for public washrooms.
- **Gym `F`:** treadmills and the rower facing the starboard windows, weights by the store wall, mats in the corner, a mirror.
- **Crew store `S`:** shelves both sides, the counter, a drinks fridge and a window display.
- **Call-home booths `B`:** four cubicles under the starboard windows, a waiting sofa, clocks for home time zones and the message board.
- **Lounge screens** are now `[40, 11, 7, -38, -23]` and `[40, 11, 7, 23, 38]`.
- **New kit:** `raisedBed`, `growRack`, `trellis`, `citrusTree`, `bush`, `pond`, `bigTree`, `groundCover`, `stepStone`, `moss`, `gardenLamp`, `pollen`, `medBed`, `medDesk`, `medCabinet`, `examBed`, `treadmill`, `rower`, `weightRack`, `weightBench`, `gymMats`, `shopShelf`, `drinksFridge`, `shopDisplay`, `callBooth`; wall kit `herbWall`, `gymMirror`, `clocks`, `msgBoard`. Materials `GD`, `MED`, `GYM`, `SHOP`, and `LEAF_GEO` with `leaf()` for low-poly foliage. None call `R()` at load.
- **Cost:** about 180–290 draw calls in normal views (the garden is the most triangles, about 270k); zoomed right out over the garden, about 440. Watch this on phones.
- Every walkable Deck 3 tile and every item can be reached. Deck 4 is pixel-identical to 0.6.4.
- **0.6.6:** Mother Fen is renamed Chef Auda Brennan ("Chef Brennan" in tap text). Update the design doc to match.

## The promenade (0.6.8)

- **Planter islands** (`planterIsland`, 2.48 × 1.34, `snug`) sit on rows 10–11 at cols 28–30 (lemon tree, `fruit`) and 34–36 (marigolds). Trees: a 1.9 m trunk with the crown at about 2.5 m (0.7.0). No lamp posts (taken out at review, 0.6.9). Rows 9 and 12 stay clear as lanes, and so does every column with a door: the mess doors (25, 26, 31, 32), gym (27), store (33), galley back door (38) and booths (38). Each island has its own fade group (`'=:a'`, `'=:b'`), so only the one you're behind fades.
- **Route kiosk** (`routeKiosk`) at col 24, rows 10–11 (blocked with `block`), screens on both faces. Its canvas stars come from a fixed hash, not `R()`.
- **Garden-door end:** a bench on each wall and four small potted plants (the `plant` kit, not `bush`, which draws from `R()` and would reshuffle the garden).
- **Materials** in `PROM`. Nothing calls `R()`, so Deck 3's garden, lounge and infirmary are pixel-identical to 0.6.7, and Deck 4 is ALL IDENTICAL.
- **Cost:** about 30 more draw calls on a normal promenade view (338 → 368 at 1200 × 800).

## Snug collision (0.6.9)

- `place(..., { snug: true })` still adds the piece's tiles to `BLOCKED`, so paths and the crew brain avoid them as before. It also records the piece's real footprint in `SNUG` (tile → boxes), and `collide` pushes walkers off those boxes instead of the whole tile. You can walk right up to a bench against a wall.
- Used on the lobby benches on Decks 3 and 4, the garden-door benches and the planter islands. Worth using for any thin piece against a wall.
- 0.6.9 against 0.6.8 on Deck 4: only 21 of the 3000 collision probes move, all beside the two lobby benches; everything else is ALL IDENTICAL.

## The music room (0.5.9)

- Room `n` on Deck 4, no longer a hall. Kit: `MUS` materials, `pianoSlab`, and `KIT` pieces `grandPiano`, `pianoBench`, `drumKit`, `guitarStand`, `amp`, `micStand`, `stageLight`, `beanbag` and `recordCabinet`, plus `WALL_KIT` pieces `acoustic` and `instrumentHooks`. None of them call `R()`.
- The stage is an extruded slab following the bow curve, an inset in from the hull. Its tiles are added to `BLOCKED`, and stage pieces are raised by the stage height after `place`.
- One stage light is a real lamp, within `LAMP_SLOTS`. The Captain's haunts already favour `n`, so she visits.
- 0.5.9 against 0.5.8: the random seed matches. Paths, the Captain's late goals, and screenshots showing windows or the bow differ as expected. Every room tile and every music-room item can be reached; the 96 unreachable items are locked cabins, the same as 0.5.8.

## The lift (section 11)

- **The car** is room `@` on each deck's map (2 × 3, mid-spine, big enough for a hover cart). `buildDeck` fits every car with a panel and handrail on its north wall and a light strip on its south wall.
- **Lift doors sink into the floor** (0.6.9): `leaf.position.y = 1.1 - open * 2.3`, hidden once fully open, so they never stick out past the frame. Other doors still slide.
- **Lift doors** are one wide door per side: lift edges in a line (three per side now) share a single pair of leaves, built on the first edge, and the corners between them have no posts (`liftJoint`). A door object carries its own `cx`, `cz` and `span`.
- **Lift doors** are walkable, so you can walk straight through the car. Crew sometimes cut through it.
- **Opening the deck list:**
    - Tap a lift door or the car panel (an item with `lift: true`) and `enterLift()` walks you to `panelTile()` (the car's back row, east column), faces you to the panel, then opens the deck list. If someone's standing there, you go to the nearest free car tile instead.
- **Pressing:** choosing a deck calls `pressPanel(n)`. You walk back to the panel if you'd moved, then `player.press` plays a 0.8 s reach with the right hand (`g.reach`, blended in `animateRig`). At the top of the reach `startRide(n)` fires. Moving cancels the press.
    - From out in the lobby the panel is usually hidden by the cutaway, so tap the doors.
- **The panel** lists Decks 1–6, with unbuilt decks greyed and your deck marked. Escape, "Stay here" or a tap outside closes it.
- **A ride** (`RIDE`, about 1.8 s, on the game clock):
    1. The doors close.
    2. The view fades to black.
    3. `goToDeck(n, at)` runs behind the black, keeping your facing.
    4. The view fades in and the doors open.
    5. The doors go back to proximity behaviour, and the arrival toast shows.
- **Taps and pointer input are ignored during a ride.**
- **`LAMP_SLOTS = 2`.** Each deck is padded with dark point lights under the floor up to this count, so changing decks never recompiles shaders. Raise it if a deck needs more real lamps.


## The spine

- **Deck 4:** rows 6–7 are `Y` (Spine trunks) and rows 11–13 are `Z` (Spine ladder). They're glassed onto both lobbies and the corridors. A hatch at `h,20,14` leads down the ladder (tier 2). The lift sign (row 7) and call panel (row 11) stay on solid wall either side of the lift doors.
- **Deck 5:** one `Z` row (9). The car's back wall faces the Works bay; there's no `Y` row.
- **`spineTrunks` and `spineLadder`** each fill exactly one row beside the car (on Deck 4 the trunks sit in row 7, just above it), placed with their back to the car (`'n'` for both). That's why they line up. Decks with more spine room add their own fittings around them, as Deck 4 does with `trunkJunction` and `harnessRack`.
- **Tap text** is shared from `SPINE_IT`.
- **`#` rooms are still solid spine** wherever a deck has spine beyond those rows.


## Kit added in 0.5.x (4b)

- **`WM`, the Works materials:** steel, paint, screens, hazard (texture), hull, cockpit, engine, nav lights, door steel, light strip, tool board and more. They're made once at load. Repeated pieces share these so merged meshes stay few; for example, all work lights share `WM.lightStrip`.
- **`KIT` additions:**
    - Works complex: `workbench`, `lathe`, `fabricator`, `weldBench`, `counter`, `aisleSign`, `tarpHeap`.
    - Shuttle bay: `shuttle`, `bayDoors`, `doorGear`, `bigFan`, `boothConsole`.
    - Spine: `spineTrunks`, `spineLadder`, `trunkJunction`, `harnessRack`.
- **`WALL_KIT` additions:** `workLight`, `jobBoard` (static cards in `o.cards` for now), `toolWall`, `carPanel`, `handrail`, `deckDirectory`.
- **`gearGeo(r, teeth, depth, holes)`** makes an extruded gear. Teeth of the same pitch mesh at any size (big gear 0.9/24 teeth drives small 0.45/12 at twice the speed).
- **Turning parts.** Push `{ o, ax, w }` onto `SPINS` and the loop turns `o.rotation[ax]` by `w` radians per second on the game clock. Mark spinning meshes with `noMergeAll(o)` so merging leaves them alone. `SPINS` is reset with each deck.
- **Fade groups.** `place(..., { fadeGroup: 'r:Lights' })` puts tall pieces in their own fade group instead of the whole room's. Storage aisles use it.
- **Pieces against the hull that must lower with the cutaway** go in `WALL_DECOR` with their hull edge, so they hide when the hull run is cut. The bay doors do this with `v,1,6`. Don't do it for things you watch through glass (the door gear): its hull run wraps round to the near side and would hide it just as you walk up.
- **`placeOnEdge(kind, key, toward, { it })`** now takes tap text, like `placeWall`.
- **Taps:**
    - `item.see` shows the text without walking, for things behind glass.
    - `item.lift` opens the lift.
    - Sealed doors and lift doors use `reachableSide(e)` and `doorSides(e)`.


## Crew

- **Chef Brennan and Rina are `deck: 3`** (0.6.7). Rina keeps her bunk on Deck 4 in the story, but has no `home` until shifts move people between decks. 0.6.7 against 0.6.6: Deck 4's crew paths and crew screenshots differ as expected; the crew-hidden shot differs only by a door still closing behind crew who had just walked past.
- **Pell is `deck: 5`** with Works haunts and favourite spots (benches, job board, tea corner, lathe, storage counter). The game still starts with you on Deck 4, where seven crew wander.
- **The room brain adds `j`, `=` and `+` weights on every deck.** On Deck 5 there's no `j`, which is harmless (that pick just fails and retries). Room letters are per-deck, so `home` and `haunts` only make sense for the walker's own deck.


## Rules that keep it working

Phones:

- Never let two surfaces share a plane. Overlap solids, or keep faces at least 0.005 apart. The job board's screen sat 0.005 behind its frame's face and vanished; check plane depth against box faces.
- Keep the canvas opaque, keep the camera depth range tight, and snap the camera to whole pixels.
- Avoid per-pixel noise on large surfaces.
- Pass every colour through `col()`.
- 1 unit = 1 tile.
- Only one deck is in memory at a time.

Determinism:

- Shared kit made at load must not call `R()`. It would shift every later kit texture.
- New floor types on an existing deck must not draw from the floor loop's `R()` (see `lift` and `spine` in the floor painter). Otherwise every later tile's grain changes.
- New kit used on Deck 4 should avoid `R()` too.
- Regressions must come out pixel-identical. When they don't, find out why before moving on.

Extrude geometry:

- `ExtrudeGeometry` bevels widen a shape by `bevelThickness` on each extruded face. Put decals and windows outside that.


## Testing

**cadet_test.py** now clicks Walls until it's back to Auto after the walls shot, so it works with builds before and after 0.5.8. It compares two builds on Deck 4 (deck data, paths, collisions, crew, taps, screenshots).

- **Setup in a fresh container:**

  ```
  pip install playwright
  mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three
  npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
  ```

  `CADET_WORK` (default `/tmp/cadet-work`) sets where three.js and the test copies live. `CADET_CHROME` points at a Chromium binary when Playwright's own browser isn't installed (in Claude Code cloud sessions, `/opt/pw-browsers/chromium`).

- **Run:** `CADET_CHROME=/opt/pw-browsers/chromium python3 cadet_test.py OLD.html NEW.html` from a scratch folder (screenshots land in the current folder). It takes about a minute. The old build comes from git, for example `git show HEAD~1:starship-cadet.html > old.html`.
- **Screenshot noise (0.7.0).** In cloud containers the software renderer sometimes rounds a few dozen pixels one colour level differently between runs, even comparing a build with itself. The test treats a difference of at most 1 as noise and says so ("apart from renderer noise"); anything bigger fails. It also keeps toasts out of screenshots (they fade on real-time timers) and turns off CSS transitions; toast text is still compared.
- **When crew changes are expected,** compare the crew-hidden shot, or make a test copy with the crew change reverted and expect ALL IDENTICAL. That's how Pell's move was proven.

Deck 5 and the lift were tested with small ad-hoc scripts that reuse cadet_test.py's `Game` class:

```
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
```

They checked:

- Every item's approach tile and every room tile can be reached from the lift lobby (skip `lift` and `see` items).
- Rides down and back: the deck, the tile you're on, your facing, the fade and the door states.
- Taps on sealed doors, hatches and glass-backed items.
- Draw calls and `LAMPS.length`.
- `SPINS` angles advance.
- Memory across round trips: Deck 4 must come back to the same counts each time. The first Deck 5 visit uploads shared kit (hatch textures, sill and pane geometry), which then stays, like any kit.

**Screen-space tap tips:**

- Project a door's edge centre at y ≈ 0.08. The cutaway may have lowered the door, and a tap at head height goes past it.
- Things in locked rooms can be hit through a lowered door; that's the test spot, not a bug.

**deck_check.py** (0.6.8) does that: `CADET_CHROME=/opt/pw-browsers/chromium python3 deck_check.py BUILD.html` visits every deck in `DECKS` and checks every room tile and every tappable item can be reached from the lift, lists the rooms nobody can get into yet (locked cabins, sealed rooms; not failures), flags any room you can only partly get into, lists the active crew and draw calls, and checks Deck 4's memory over round trips. Run it on every turn alongside cadet_test.py.


## Working method

- Edit the build in place and never rewrite the whole file. Make small exact-string edits, each matching once.
- Work a deck one turn at a time. Each turn ends with a tested build, a bumped build number, a line in the build table above, and a commit pushed to the repo. Git is the save point: earlier builds come back with `git show <commit>:starship-cadet.html`.
- When a deck's turns are all done, stop for review: a playable link, screenshots, a summary and the test results.
- Keep these notes current as you go, so any new session can pick up from them.


## Deck 1, the Bridge (0.8.x)

Built from plans/deck1-plan.html (agreed) by the bridge architect, in parallel with Deck 2 (0.9.x). Builds 0.8.1 onward.

- **Shell (0.8.1).** `DECKS[1]`: 20 × 10, `lift: [8, 5]`, seed 10109. Rooms: `+` Bridge lobby (hall), `B` Bridge (plate for now), `O` Observation room (wood, windows), `w` Bridge washroom, `R` Ready room (locked, windows, `NO_FADE`), and sealed `k` Utility closet, `u` Relay room, `c` Sub-floor crawl. `sealed` maps each shut door to its room's tap text, as on Decks 5 and 6. The ladder hatch is `h,7,7`.
- **Hull pieces by facing (`hull.byFace`).** In `buildDeck`, the hull run splitter wrote piece numbers back into `part[]` while still comparing facings against it, so a run was split almost everywhere: Deck 1's small round hull came out as 128 one-segment pieces (589 draw calls for an empty shell). A deck whose `hull` has `byFace: true` compares the facings themselves (`fc[]`) and gets one piece per facing (Deck 1: 10 pieces, 256 calls). Decks 3–6 don't set it and keep their old pieces exactly (Deck 6 has 234, Deck 4 119). Turning it on for them would save draw calls but changes their hull-run table, so it needs its own regression pass.
- **Viewscreen (0.8.2).** `bridgeViewscreen(rk, a0, a1, y0, y1)` (Deck 1 block) walks the hull segments on the bow ellipse between bearings a0 and a1 (0 dead ahead, measured on the ellipse), keeps those belonging to room rk's hull pieces (matched by segment midpoint against `hr.edges`), and adds a `hullStrip` per piece to that piece's `g`: the picture from y .55 to 2.35, just inside the hull's inner face, with bezels above and below. Being in the piece's `g`, it squashes with the hull for the cutaway and shows as a lit band at knee height. The picture, `BRG.sky`, is a 1024 × 256 canvas drawn at load (stars from a fixed hash, not `R()`); its texture offset is pushed onto `SPINS` as `{ o: { rotation: offset }, ax: 'x' }`, so it drifts with no engine change. No lamp. The tap target in front of it is `tapSpot`, an empty kit piece.
- **Bridge floor (0.8.2).** New floor type `bridge` in the floor painter (blue-grey carpet tiles; it draws the same one `R()` per tile as other floors). New deck hook `floorArt(g, PX)`, called after hazards and before wall shading: Deck 1 paints the command ring from `ring: [15.4, 5, 2.0]` (tile centre and radius): a darker well shaded under its edge, a brass step edge, a teal light line outside it, a faint inner circle.
- **Command ring (0.8.3).** Tile coordinates (B starts at column 10, so room-local x is tile x − 10). Ring centre (15.4, 5), the step edge at r 2.0: a brass `curveStrip` (−.01 to .03 m) and a teal light strip just outside it, built in `dress` into `staticRoot`. The rail is the plan's `bar` curve at r 2.2, trimmed to 140°–220° so the tiles at its ends stay open (the plan's 120°–240° sealed the aft pocket off). Captain's chair (15.2, 5), seats at z 3.85 and 6.15; helm (17.45, 4.45) and ops (17.45, 5.55), each .9 wide so it blocks one row and column 18 stays reachable; their seats at x 16.55. The ring's centre sits on a tile line, so the chairs pass explicit `block` tiles.
- **Rear stations (0.8.3).** Watch (11.45, 3.4) and Survey (13.45, 3.4) against the ready room wall, its door (column 12) left clear; Comms (11.45, 6.6) on the washroom wall; Works (12.4, 8.5) against the washroom's east wall, facing the floor hatch at tile (13, 8) (painted by `floorArt` from `floorHatch`; the real hatch is the edge `h,13,9` behind it). Row 7 is the way round the south of the ring, so nothing stands in it. The plan put two stations in front of the glass beside the bridge doors; they moved so the glass stays clear.
- **Observation room, ready room, washroom (0.8.4).** O (room-local x = tile x − 1): `confTable` at (2.5, 5), 4.8 long along z, blocking column 3 only; ten seats (`commandChair` small, `noBlock`) at x 1.35 and 3.65, z 3–7; `briefingScreen` on the lobby wall (`placeWall('O', ..., 'e', 2.0)`); `windowSeat` (3.6 long) across the stern; `teaSideboard` at (4.67, 7.9); a floor lamp, the deck's one real lamp, at (.55, 2.45); two big plants. R (locked, `NO_FADE`, every item `see`): `readyDesk` at (1.6, 1.5) facing the door, the Captain's chair behind it, two visitors' chairs, `readyShelf` on the east wall, the `aquarium` (the Admiral) on the west wall. w (2 × 2): `compactToilet` in the far corner, `smallBasin` by the door; the door tile stays clear.
- **Draw calls.** Deck 1 by the lift: 315 (Decks 3–5: 326–332). Zoomed right out over the whole deck: about 364, of which doors are about 130 (see below). The cabins' `bookshelf` makes a material per book (about 40 calls), so the ready room has its own `readyShelf` on five shared materials. Each hull piece's viewscreen strips are merged (`mergeMeshes`) into two calls.
- **Deck 1 is done and waiting for the user's review** (0.8.4).
- **Mood light:** `light: { sky #d4e2ff, sun #dfe8ff, hemi .96, sunI .9 }`, a little cooler and dimmer than the decks below.
- **Kit:** the Deck 1 block sits just above `DECKS[1]`: materials in `BRG`, pieces added with `Object.assign(KIT, ...)` (and `WALL_KIT`). Nothing there calls `R()`.
- **Doors cost a lot of draw calls on every deck** (about 120 of Deck 1's 256): each leaf is a box with six material groups. Grouping the four edge faces and the two leaf faces would cut that by two thirds with identical pixels, but changes the call counts the tests compare, so it's left for the lead.

## Known issues

- 0.5.8 against 0.5.7: paths, collisions, crew, taps and the random seed match; screenshots, hull runs and draw calls differ as expected. Later regressions compare against 0.5.8.
- From the default camera, the cutaway lowers the near-side lift doors, so you only see them slide from the far side.
- Rooms whose door faces away from the camera have their furniture at the camera end, so it's often faded. Rotate to see it.
- The tea corner is tight: everything is reached from its doorway tile.
- Washers, showers, the wash pod, the fabricator and the lathe are props until machines arrive in step 7. The job board's cards are static.
- A deck's plan must keep its flat sides on the map's top and bottom edges.
- A room needs to be deep enough for its template; bunk rooms need at least 4 tiles of depth.


## Next

**6d. Deck 3, the Commons.** The plan is agreed: plans/deck3-plan.html, 52 × 22, `lift: [20, 11]`. Built one turn at a time:

1. **The shell (done, 0.6.2).** Every room is walkable and named. Sealed: galley plant `g` (hatch `h,39,3`), water recycler `R` (hatch `v,17,14`), irrigation room `i` (hatch `h,3,17`), and the ladder hatch `h,20,13`.
2. **The mess hall, galley and cold store (done, 0.6.3).**
    - **Mess hall** (room-local, 12 × 9): long tables at (2.6, 1.0), (7.4, 1.0), (2.6, 4.0), (7.4, 4.0); round tables at z 6.9. Rows 2, 5 and 8 and columns 27–28 are left clear as aisles. The line runs down the galley wall (column 34) from north to south: drinks, tray return, trays and cutlery, the servery against the pass, grab-and-go; tile (34, 8) stays clear for the staff door. Customers queue in column 33.
    - **Galley:** ranges on the bow wall, ovens beside the cold store door, the prep island in the middle, the dish pit by the back door, Brennan's stool.
    - **Cold store:** three frosted shelf units along the hull, a chest freezer and crates.
    - **`pass` edges** (`v,35,4`–`v,35,6`) are glass edges with no pane: the sill (1 m) is the counter, open above, header on top. They block walking. `passShelf` puts a steel top through the wall and a heat lamp under the header.
    - New kit: `longTable`, `roundTable`, `servery`, `trayStack`, `trayReturn`, `drinksStation`, `grabShelf`, `ovenStack`, `prepIsland`, `dishPit`, `coldShelf`, `chestFreezer`; wall kit `menuBoard`, `passShelf`. Materials in `MESS`. None call `R()`.
3. **Curved inner walls, then the lounge (done, 0.6.4).** See "Curved inner walls" and "The bow lounge" above.
4. **The infirmary, exam room, garden, washrooms, gym, crew store and call-home booths (done, 0.6.5).** See "Deck 3, turn 4" above.
5. **Crew (done, 0.6.7).** Chef Brennan works the galley; Rina works in the infirmary. Deck 4's crew routes changed when they left.

**6e. Build the rest of the ship: Decks 6, 1 and 2 (next, agreed 2026-10-15).** The user's priority is getting the whole ship built. Crew, machines, supplies and jobs come after.

- **Who:** the deck architect session builds; the lead session reviews and merges (see TEAM.md).
- **Scope:** shell, rooms, dressing and furniture only. No crew, no shifts, no machines, jobs or supply runs, which are step 7 and later. Rooms that will later need crew (the engine watch room, the bridge stations) get furniture but no people.
- **Order:** Deck 6 (Engineering), then Deck 1 (Bridge), then Deck 2 (Command & Science, once its plan is final). After each deck: stop for the user's review and sign-off (CLAUDE.md).
- **Decisions:**
    - **Bridge command ring:** faked for now with a rail, a painted step edge and a curved step strip; no engine change. A real sunken floor can come later.
    - **Access:** the lift reaches Decks 6 and 1 from day one. Locking by tier or story comes later with the story work.
    - **Mood lighting per deck:** yes, warmer and dimmer on Deck 6, cooler on the bridge, as long as Decks 3, 4 and 5 stay pixel-identical.
    - **Bridge washroom:** keep it.
- **Progress, Deck 6:**
    1. **The shell (done, 0.7.1).** Every open room (lobby, overlook, watch room) is reachable; E, K and R are locked and stay solid (`NO_FADE`). About 230 draw calls by the lift.
    2. **The engine room (done, 0.7.2).** Room-local, `E` is 10 × 12 with the stern hull at x 0. Drive housing at (.55, 6) against the stern (`'w'`, 8.6 long); coils at x 2.6, 5.1, 7.6 on z 6, phases 0, −2.1, −4.2; copper feeds at y 2.4 between housing and coils; catwalks at z 3.1 and 8.9 (8.4 long) and a cross landing at x 9.35 by the stair door (`v,12,5`). All `see` taps. Overlook `O`: rails at x .2 either side of the stair door, benches at (2.3, 2.5) and (2.3, 7.5) facing the window.
        - **`PULSES`** (new): `{ m, key, base, amp, w, ph }`; the main loop sets `m[key] = base + amp * (.5 + .5 sin(t w + ph))`. Reset with each deck, like `SPINS`. Pulsing materials are made in the kit at dress time (owned by the deck, freed on unload), so each coil has its own phase. Don't pulse a material that a fading tall piece clones: `E` is `NO_FADE`, so its pieces never get cloned.
    3. **The reactor and engine control (done, 0.7.3).** Reactor `R` (room-local 9 × 12): `reactorDrum` at (4.4, 6), loop radius 3.0. Engine control `K` (5 × 4): `controlBoard` at (4.45, 2) against the reactor glass (`'e'`), chairs at x 3.4 facing it, `mimicPanel` on the north wall at 2.5. `trefoil` signs on `h,26,3` and `h,26,4`, in the alcove by the reactor door.
    4. **The watch room, lobby and mood lighting (done, 0.7.4).** Watch room `S` (2 × 3): armchairs at (.55, .55) and (.55, 2.45) facing each other, the kettle (`dispenser`) at (1.55, .4), a lamp (the deck's one real lamp) at (1.6, 2.6); tiles (0, 1) (the door) and (1, 1) (in front of the junction hatch) stay clear. Lobby: `coolantRiser` in its four corners, a bench at (2.5, 9.55).
        - **Mood lighting** (new): a deck definition may carry `light: { sky, sun, hemi, sunI }`. `applyLight` multiplies the hemisphere and sun colours by `sky` and `sun` and their intensities by `hemi` and `sunI`, after the day–night blend. Only uniforms change, so no shader recompiles; decks without `light` run exactly the old code. Deck 6: `sky #ffd2a6`, `sun #ffc48c`, `hemi .8`, `sunI .78`.
    - **Deck 6 is done and waiting for the user's review** (0.7.4).
- **Deck 1's empty shell draws 593 calls.** Bring that down before dressing it, without changing the hull output on Decks 3, 4 and 5.
- **Plans:**
    - plans/deck6-plan.html and plans/deck1-plan.html are agreed.
    - plans/deck2-plan.html is agreed at Sketch 8 (approved by the lead for the user, 2026-10-15). It's 52 × 22 on Deck 3's outline, with the lift at [20, 11].
        - Aft of the lift: a looped carpeted senior corridor, and 15 bedrooms (12 crew plus 3 visitor rooms), each with its own door. The Captain's quarters across the stern are the biggest bedroom (60 tiles).
        - Forward of the lift: science, off a four-wide corridor. The sensor and comms array is a sealed room in the nose (106 tiles).
        - The lift's stern door opens to the quarters and its bow door to science.
        - Open, with defaults until the user says otherwise: the six invented officers are placeholders, and the 15th room is a visitors' cabin.

**7. Machines, supplies and the shared job list,** anchored on the Works bay job board. Comes after the ship is built (6e).


## Agreed ideas waiting for their milestone

- **You first arrive by shuttle** in the Deck 5 bay. The Tern is there with its ramp down, ready for it. Until the arrival is built, the game starts with you waking in Bunk 1. Still to decide: which milestone builds it, and who meets you off the shuttle.
- **Hygiene is a fourth need,** and showers restore it (milestone 2).
- **Uniforms get grubby.** You drop yours at the laundry and take a clean one from your locker. A water recycler fault on Deck 3 means weak showers on Deck 4.
- **Hover hand carts** carry supplies from Deck 5's cargo hold up the main lift to Deck 3's cold store and wherever else they're needed. A job for step 7; the carts charge in Deck 5's Cart bay.
- **Shifts will move crew between decks.** Pell then sleeps in Bunk 2 and works on Deck 5.


## Open questions

From design doc v4:

- Who is the Works Chief?
- How long is a ship day in real time?
- Should the player ever move to the night shift?
- How does diagnosis look on screen?
- Can the player be passed over for certification, or only delayed?
- Should the player customise their character at the start?
- What triggers the first story events?


## File map

The script is split into numbered sections:

1. Setup
2. Textures
3. Materials and helpers
4. Deck: ship state, current deck (4a), shared kit including `WM` and `gearGeo` (4b), `buildDeck` / `unloadDeck` and the floor painter (4c), deck definitions `DECKS[4]`, `DECKS[5]` and `DECKS[3]` (4d)
5. Lighting
6. Camera
7. Grid, pathfinding and collision
8. Character kit
9. Crew data
10. Walkers (the starting deck is built here)
11. Interaction and UI: taps, `goToDeck`, the lift (`enterLift`, panel, `startRide`, `updateRide`)
12. Main loop: rides, doors, `SPINS`, steam, cutaway and fades

The character spec, uniforms and badges are unchanged; see section 8 and the design doc.
