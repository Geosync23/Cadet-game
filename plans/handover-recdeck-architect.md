# Handover: the rec deck architect (DA6)

**Role:** rec deck architect, hired by lead 13; reports to lead 14 (session_01RHtJv7GJDi4qosgU8Gb2b8) since lead 13 handed over. RA1 (session_01KAGCZigadF4uRyQQafjkHW, claude/recdeck-anim) owns the player's poses, props, rec kit and the mover (section 8c). Phase 1 of the rec deck (plans/recdeck-plan.html v3 on `claude/recdeck-plan`): build the deck and its animations, usable by the player only.
**Branch:** `claude/recdeck-build` (from `claude/p5-cand-s2` a9fad20 = 0.63.1). Builds 0.80.0 to 0.80.6.

## What I built (turn by turn, all in DEV_NOTES' build table and its section "The rec deck")

| Build | Turn | What |
| --- | --- | --- |
| 0.80.0 | R1 | `DECKS[7]` shell: map, doors, hull, double-height walls (`tall: 1.6`), floors without R() (`recFloor`), the R button (`DECK_ORDER`, `deckLabel`, `deckWord`), `open: [6, 24]`, service hatches, kit hire, changing rooms, washroom. `playerOnly` keeps it out of the crew's sim. |
| 0.80.1 | R2 | Auditorium (rake, 76 seats as `rec:seat` places, stage, truss, lectern, piano, screen housing) and foyer (REC DEC neon, poster). |
| 0.80.2 | R3 | Lightdisc court (lines, net, side fields, static scoreboard) and the stands (33 seats). |
| 0.80.3 | R4 | Pool and the water shader (`recWater`, `recWaterMesh`). |
| 0.80.4 | R5 | River hall (loop, island, wave gate, dock, kayaks, rack) and the climbing wall with the bell. |
| 0.80.5 | R6 rooms | Float room, and the four service rooms' insides from existing kit. Machines are TODO. |
| 0.80.6 | R6 activities | Section 15r: swim, kayak, climb + bell + lowered, float, sit, watch; the changing-room chain with rec kit and a tip; closed before 06:00. |
| 0.80.7 | Merge + v4 | RA1's 0.81.0 merged (poses, kit, mover are theirs; 15r uses `actStart(kind, place, { move })`); walls 1.3×; pool 4 lanes; 2 belays on a rail; Ask someone to play panel by the court gate. |

## Where the code is

- `// 4e. THE REC DECK` (after section 4d's dressing code): `recFloor`, the kit (`KIT.rec*`, `WALL_KIT.rec*`), `REC_SEATS`, `REC_STANDS`, `RIV`, `REC_WALL`, `recWater`, `recMats()` (the deck's materials, made in its `dress`, freed with it), `DECKS[7]`.
- `// 15r. THE REC DECK'S ACTIVITIES` (just before section 16): `recTap` (on `PLAYER_TAPS`), `recGo`, `recStart`, `recAfter`, `recFrame` / `recMove` (own requestAnimationFrame), `recKitWear`, `recLookSpec`.
- Section 8c (RA1's): the poses, props, `playerKit`, `recChange`, `recTowel`, `REC_MOVES` and `recMoveStep`.
- Shared code touched (all no-ops on Decks 1-6): `H` is a `let` (+ `WALL_K`), `writeWalls`' `ts`/`HK`, `buildDeck` sets them; the floor painter's `st.rec` branch; the lift panel, HUD, Maps and goal arrow use `DECK_ORDER`/`deckLabel`/`deckWord`; `playerOnly` filters in `schedData`, `placesOf`, `apptPlaces`, the job finder's where lookup and the blackouts; deck_check.py accepts `rec:` place types (a `rec:seat` up to 4.5 m from its aisle).

## Judgement calls (not in the plan)

- `v,19,10` and `v,21,10` are solid wall, not glass, so the lift's call panels sit beside the doors as on every deck.
- The court's gate is `h,14,13` (the plan's `h,10,13` is filled by the benches); the court rail is `pass` (sill, no pane).
- The concourse's two benches went (the stands are right behind that glass).
- The float room's padding is waist high (full-height panels hid the room from the camera).
- Seats are reached from the aisle beside their row and the body glides along the row into the seat.
- Rec kit is not saved; walking away mid-chain leaves you in rec kit (tap the Lockers), leaving the deck puts the uniform back.

## Loose ends / for later phases

- **Machines (R10, systems engineer):** none in `DECKS[7].machines`; a TODO comment in `dress` lists the plan's ids. Service rooms have kit and tap text only.
- **Lift `playerOnly`** when crew come (R7): then places need real types; the seats are `rec:seat`.
- Lightdisc (R9): the court's tap says "coming soon" (`recTap`); the scoreboard texture is static.
- The film screen is only its housing (rolled up); the house lights don't dim; no stage lights' pools.
- The camera doesn't follow your kayak round the loop.
- RA1's `?recposes` lineup is still in the build (dev only).

## How to test

cadet_test (ALL IDENTICAL on Deck 4), deck_check (Deck 7 everything reachable; 153 calls by the lift), a zoomed-out pixel compare of Decks 1-6 against 0.63.1 (identical; script was ad hoc: `goToDeck(n)`, zoom .55, screenshot both builds), player_check and interactions_check for 15r. Probe pattern: reuse cadet_test's `Game` class, `goToDeck(7, null)`, `recTap({ t: 'Pool', x: '' }, p, p)` with `p` a `THREE.Vector3`, step, read `ACT.kind/phase` and `REC.kit`.

## Gotchas

- Waiting loops with `pgrep -f "<pattern>"` match themselves; read the log instead.
- `relayBoard` is a WALL_KIT piece, not KIT.
- Never put a `//` comment in the middle of a line you're replacing: it swallowed `A.z = p.z` once (NaN positions).

## Next: Lightdisc on the court (the user's go, via lead 14, 2026-10-18)

Brief (lead 14): integrate the approved prototype (`claude/lightdisc-proto` ba6b4ac, `lightdisc-proto.html`; spec in plan v5 section 4 on `claude/recdeck-plan` 7ab0d82) as 0.80.8+. Live on the 3D court, game-view camera, thumb-drag controls, rules, crew levels, How to play, results saved. Like Tiles you need an opponent: **Ask someone to play** brings one crew member down to the rec deck to play you, the one exception to player-only (they walk down, play, leave; no other crew behaviour). The ship clock **pauses** while you play, and the game says so clearly. Tests: a new disc_check (seeded games replay the same, same timing at different frame rates, save round trip), cadet_test identical on other decks, player_check. The prototype engineer is session_013LcEsgjMTDMMeiACKLj2bB.

Prototype pointers (from its engineer): the game logic is its section 5 (`newGame`, `step`, `discStep`, `hit`, `point`, `aiMove`, `planAll`), pure and seeded, and ports as is; `LD.paper()` works a game out on paper; `fitGameView()` fits the camera; the fixed-step loop is the `acc`/`DT` loop in `frame()`; its check is `tools/lightdisc_proto_check.js`.

Where it plugs into the rec deck:
- **Taps:** `recTap` (section 15r) answers 'Lightdisc court', 'Scoreboard' and 'Ask someone to play' with a toast; replace that with the game's entry.
- **The court:** room `C`, deck x 4-17, z 13-18 (13 × 5); baselines drawn at deck x 4.6 (stern, orange) and 16.4 (bow, cyan), sidelines z 13.3 and 17.7, net at x 10.5 (`recCourt`, room-local). You play from the bow end. The gate onto the court is `h,14,13`; the panel is a wall piece on `h,15,13` facing the court (`recPlayPanel`).
- **The scoreboard** is a static canvas in `WALL_KIT.recScoreboard` (on the stern wall, centre y `H - .72`, 2.8 × 1.22); make its texture redrawable for live scores.
- **The net and side fields** are `RK.net` / `RK.field` (additive, their opacity breathed by `PULSES`); a wall flash can reuse `RK.field`.
- **The opponent exception:** `DECKS[7].playerOnly` keeps the deck out of the schedules (`schedData`, `placesOf`, `apptPlaces`, the job finder, the blackouts). The opponent has to come through some other route than the day plans (Tiles' way of fetching an opponent is the model).
- **Pausing:** the clock's freeze is section 13's `FREEZE` / `freezeSync` (Tiles uses it).
