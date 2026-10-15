# Starship Cadet: dev notes 3

Read this first in any new session, together with **design-doc.md** and **starship-cadet.html** (build 0.14.0). The design doc is the source of truth for what the game is (update it when a design decision is made); these notes cover the build: what's in it, how the code works, the rules, testing and what's next.

This file replaces DEV_NOTES_2. The repo holds it with design-doc.md, the build, the deck plans in `plans/` and cadet_test.py. Git keeps every earlier version, so files keep stable names (no version suffixes).

**Deck 3 is complete (0.7.0, with the promenade dressed and review fixes) and signed off ("ok for now").** **Decks 6, 1 and 2 are built** (0.7.x, 0.8.x, 0.9.x by three architect sessions, merged as 0.10.0) and are waiting for the user's review. All six decks are now in the game. See TEAM.md and section 6e.

The nine small updates once listed here for the design doc (Chef Brennan, Deck 3's rooms and layout, two meals a day, no freight lift and the Cart bay, the one-floor lounge, the music room, the walk-in lift car, the spine behind glass, Pell on Deck 5) are now in design-doc.md.


## Current build: 0.24.0 (about 7,300 lines)

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
| 0.9.1 | Deck 2, turn 1: the shell (Deck 2 architect, branch `claude/deck2-command`; builds 0.9.x, merged by the lead). `DECKS[2]` from plans/deck2-plan.html Sketch 8 (52 × 22, `lift: [20, 11]`, seed 20219): the senior quarters round a looped carpeted corridor with fifteen locked bedrooms, the lobby ring, the Watch office and washroom, science off the four-wide corridor, the sensor array behind glass. Brass nameplates over the bedroom doors (new wall kit `brassPlate`, materials `D2`), science plates, lift panels, the deck directory, a bench and plants in the lobby, trunks and ladder behind glass. Calm mood light (`light`). Decks 3–6 pixel-identical to 0.7.4, day and night. |
| 0.9.2 | Deck 2, turn 2: the bedrooms. Fourteen furnished, locked bedrooms (the Captain's is turn 3): a new `d2Suite` layout that scales up Deck 4's officer cabin (double bed with headboard and two lamps, writing desk and leather chair, armchair, bookcase, frosted-glass en-suite, wooden wardrobe, rug, plant), with variants for the 3-wide cabins by the lift and the inner cabins; Vance's and the Envoy's corner cabins laid out by hand (the Envoy's with a futon, a sleeping screen and a Veyli tea table on the floor). A tap on a bed or desk says who lives there without walking (`see`). New kit `suiteBed`, `futon`, `suiteDesk`, `suiteChair`, `suiteShelf`, `suitePlant`, `suiteRug`, `ensuite`, `suiteWardrobe`, `lowTable`, `cushion`, `sleepScreen`. Decks 3–6 pixel-identical. |
| 0.9.3 | Deck 2, turn 3: the Captain's quarters and the senior corridor. The quarters (locked, 5 × 12 across the stern): the sleeping alcove behind a curtain at the port end, a dining table for eight by the door with a window seat under the stern windows and a sideboard, and the study at the starboard end with the Captain's desk, low bookshelves, a globe and a reading chair; the deck's one real lamp hangs over the table. A brass knocker on her door. The corridor: brass wall lamps, portraits of four of the Wren's captains along the gallery, consoles with flowers. New kit `diningTable`, `sideboard`, `captainDesk`, `alcoveCurtain`, `globe`, `consoleTable`; wall kit `portrait`, `brassSconce`, `knocker`. Decks 3–6 pixel-identical. |
| 0.9.4 | Deck 2, turn 4: science, the Watch office and the sensor array. Watch office (status board under the windows, the duty desk facing the lobby glass, lockers, coffee, lost property, the patrol rota), washroom, chart room (a chart table that glows from underneath, pigeonholes of rolled charts, a window seat), Survey lab (benches under the windows, an island, the sample scanner, the specimen shelf with the blue one), observatory (a brass telescope aimed out of the bow, a cushioned bench, star charts, beanbags), comms room (signal board along the windows, four headset desks), sample lab (fume hoods, glove box, centrifuges), and, locked: the specimen store (a sample that hums, `PULSES`), the probe bay (three probes nose to their launch tubes) and the sensor array behind glass (the dish turns, `SPINS`, its feed breathes blue, and the deck's second lamp lights it blue; signal racks, the comms mast). Benches, plants and notices in the science corridor. Deck 2 done. Decks 3–6 pixel-identical. |
| 0.9.5 | Deck 2 takes the bridge architect's hull fix (`hull.byFace: true`; the splitter edit is byte-for-byte the one in `claude/deck1-bridge` e928563, so the branches merge cleanly): one hull piece per facing instead of many. Fewer draw calls over the quarters zoomed out (660 → 607) and over the Captain's quarters (322 → 243); by the lift unchanged (283). Decks 3–6 pixel-identical. |
| 0.10.0 | All three new decks in one build: Deck 6 (0.7.1–0.7.4), Deck 1 (0.8.1–0.8.4) and Deck 2 (0.9.1–0.9.4), merged by the lead on `claude/ship-integration`. No changes beyond the merge. |
| 0.10.1 | 0.10.0 plus Deck 2's 0.9.5 (the hull fix on Deck 2). |
| 0.11.0 | Deck 6 review fixes (the Deck 6 architect, from 0.10.1). The engine room is open: the stair door `v,12,5` is a plain door, the catwalks are gone, a rail runs either side of the row of coils with a keep-clear marking round them, and open aisles run along both sides joined inside the door; the coils and housing are ordinary tap items and the coils fade like other tall furniture (each core is `noMerge`, so it keeps pulsing). The watch room moved from the 2 × 3 corner by engine control to the overlook's south end: 4 × 4 (`S`, cols 12–15, rows 7–10), a window onto the coils, glass onto the lobby, door `v,16,9`; two armchairs and a tea table at the window, the kettle, a lamp, the heater and the log shelf. Its old corner joined the lobby, with a bench under engine control's wall; the starboard junction hatch is now off the lobby. plans/deck6-plan.html updated to match (Sketch 3). Decks 1–5 pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.12.1 | Deck 1 scaled up after the user's review ("the ready room absolutely smothers the bridge"), from plans/deck1-plan.html Sketch 2: 22 × 12 (was 20 × 10), `lift: [8, 6]`, the bridge 85 standable tiles (was 54, +57%). The ready room is 3 × 4, aft of the bridge on the port side beside the lobby, its door on the bridge's aft edge; the washroom 3 × 2 mirrors it to starboard. The ring moves forward to (17, 6) and the rail back to a longer 130°–230° arc; the rear stations stand in two banks with aisles all round. Decks 2–6 pixel-identical, Deck 4 ALL IDENTICAL against 0.10.1. |
| 0.13.0 | The user's review fixes in one build: Deck 6 (0.11.0) and Deck 1 scaled up (0.12.1), merged by the lead on `claude/ship-integration`. |
| 0.14.0 | Deck 4 guest cabins (the Deck 6 architect, from 0.13.0). Six senior officers moved up to Deck 2, so the officers' corridor's 24 cabins are now 16 officers', 6 guest cabins and 2 spare. Guests: the lift-end column A, B, C, D (4-02, 4-04, 4-03, 4-01; two window, two inner) and the inner pair F, G (4-08, 4-07), so guests don't walk the corridor's length and officers keep 10 of the 12 window cabins. Spares: V and W (4-24, 4-23), the inner pair at the music-room end, which were already the spares. `DECKS[4].guests` (door tap text per cabin) and `spares`; room names, door plates ("Guest 4-02", "Spare 4-24") and `lockedRoom` follow them. `officerCabin` takes `guest` (fresh linen folded on the bed, a `travelCase` at its foot that doesn't block) and `spare` (`bedSingle` `stripped`, `deskSmall` `bare` with the screen off, no poster); materials `GUEST`, no `R()`. Walking tiles, collisions, paths, spots and crew routes are identical to 0.13.0; only those eight cabins' items, door texts and the two spares' posters differ (Deck 4 harness views differ only by renderer noise). Decks 1, 2, 3, 5 and 6 pixel-identical. plans/deck4-plan.html labels them G and S. |
| 0.15.1 | Pillar 1, workstream 1: ship time and saving (the sim engineer, branch `claude/sim-engineer`). New section 13. The ship day lasts 30 real minutes (`SHIP_RATE` 0.8 ship minutes a second); the game starts on Day 1, a Monday, at 06:00, in Bunk 1 (the tile is still `PLAYER_SPEC.start`, [7, 3]). The light follows the clock: night 21:00–06:00, an hour of dusk and of dawn centred on them. The HUD reads "Day 1, Monday 06:00". The game saves itself (localStorage `starship-cadet-save`) every ship hour, on deck change and when the page is hidden or closed, and resumes on the same deck, tile and facing at the same time. New game button (tap twice). The Night/Day button is a debug control, shown only with `?debug`: Night skips to 21:40, Day sleeps until 07:40. `?nosave` turns saving off; cadet_test.py loads with `?nosave&debug`. A test copy pinning the old clock (1 minute a second from 07:40, the old HUD text, no New game button) is ALL IDENTICAL to 0.14.0 with 0 pixels different; unpinned, only screenshots differ (state, paths, collisions, crew identical). Decks 1, 2, 3, 5, 6 pixel-identical day and night. |
| 0.16.1 | The crew roster, Pillar 1 workstream 2 (the crew designer, branch `claude/deck-plans-1-2-6`; builds 0.16.x). Section 9 gains `ROSTER` (all 75 crew), `ROSTER_GUESTS` (Envoy Saruth), the shared `HABITS` vocabulary and `rosterSpec(p)`, all fixed data written by `plans/crew-roster-gen.py`; new readable page `plans/crew-roster.html`. `CREW` and the walkers are untouched, so nothing in play changes. Assumes 6 berths per bunk room (see "The crew roster"). |
| 0.16.2 | The player is one of the 75 (the user's decision): `ROSTER` now holds the other 74 and `ROSTER_PLAYER` holds yours (a Works junior, bed `4-B1-2`, days off Sat and Sun). The last generated Works technician (Kai Lachance) made way; Tamsin Haddad moved from `4-B1-6` to his berth `4-B6-2`, so `4-B1-6` is the spare berth in your room. Nobody else changed. Bunk rooms: 6 berths each, as the user chose (three ordinary bunk beds per room, being built by workstream 3a). |
| 0.16.3 | Bunk 1 matches its furniture text (from 0.23.0): you move to `4-B1-4`, the top berth of the second bunk ("You lost the coin toss for the bottom one"), and Chloe Tran moves from `4-B1-4` to `4-B1-2`, above Tomas. `4-B1-6` stays the spare berth. Only those two beds change; plans/crew-roster.html refreshed. |
| 0.17.0 | Pillar 1, workstream 3a (the Deck 6 architect): `places` on Decks 4, 5 and 6, data only (nothing draws them). Deck 4: 122 (56 beds: 32 bunk berths `4-B<room>-<berth>` and 24 cabin beds `4-01`..`4-24`; 28 showers, counting each cabin's wash pod; 2 toilets, 4 basins, 6 laundry, 12 common-room, 6 music, 4 bench, 4 lift-wait). Deck 5: 31 (20 work stations, 3 tea-corner seats, the washroom, 4 lift-wait). Deck 6: 15 (7 `work:engine`, 4 benches, 4 lift-wait). `deck_check.py` checks places (255aa9f). Deck 4 ALL IDENTICAL; Decks 1, 2, 3, 5 and 6 pixel-identical. |
| 0.17.1 | Deck 4 Sketch 3, agreed with the user: the junior wing's bunk rooms are 5 × 4 with three bunk beds each (48 berths, was 32). Scrubbers 3 wide, utility door moved to `h,18,16`, plates and doors moved to match. Places redone: 138 (72 beds: berths `4-B1-1`..`4-B8-6` and the 24 cabins). One small shared line: a deck can give `floorSeeds` so its floor painter picks up the old random numbers at one column (Deck 4: column 21), and the officers' wing floor and everything built after the floor stay exactly as in 0.17.0. Deck 4 changes only in the junior wing (proof in the section below); Decks 1, 2, 3, 5 and 6 pixel-identical; deck_check OK. |
| 0.17.2 | Deck 4 bunk tap texts, text only: Bunk 1's third bunk is Lukas's with the ship's one empty berth above it (the player moves to `4-B1-4`, the top berth of the second bunk, which the text already calls "Your bunk"); Bunk 2's and Bunk 8's third bunks no longer say they're empty, since every other berth is taken. Built on 0.23.0. |
| 0.18.1 | Pillar 1, workstream 3b: `places` on Decks 1 and 3 (data only; nothing draws them). Deck 1: 30 places, Deck 3: 173. Each has the plan's `id`, `type`, `at`, `face`, `pose` and `room`, plus `xy` (the exact spot) and `walk` (the tile to walk to first). Every deck pixel-identical, Deck 4 ALL IDENTICAL against 0.14.0. |
| 0.18.2 | Places pass the official `deck_check` places check (from `claude/deck-architect`): 14 Deck 3 places held back until it accepts them (8 slide-in seats two tiles from the aisle, 6 store browsing spots of type `shop`). Deck 1: 30, Deck 3: 159. Every deck pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.18.3 | The 14 held-back Deck 3 places restored (the lead made `xy`, `walk` and `shop` official, and `deck_check` now applies the walk rule), plus the Captain's desk chair in the ready room (`1-ready-1`, `work:command`: its door is a closed door, which crew open). Deck 1: 31 places, Deck 3: 173. Every deck pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.19.1 | Pillar 1, workstream 3c (the command architect, branch `claude/deck2-command`): `DECKS[2].places`, 162 places on Deck 2's furniture (plans/pillar1-plan.md, "Places"): 15 beds (`2-<room letter>`), a shower, basin and toilet in every bedroom's en-suite, the public washroom, 44 lounge seats (armchairs, desk chairs, the Captain's table, cushions, window seats, beanbags), 24 `work:survey`, 10 `work:comms`, 8 `work:watch`, 1 `work:command`, 5 benches, 6 lift-wait. Data only: every deck pixel-identical, Deck 4 ALL IDENTICAL. Some places are boxed in by furniture until a layout fix (see the Deck 2 notes). |
| 0.19.2 | Deck 2 layout fixes so every place can be reached (agreed with the lead): S's and R's armchair 0.2 m further from the door; Vance's wardrobe 1 m along the wall and his chairs and coffee table 0.45 m toward the windows; the Captain's wardrobe moved to the stern wall, which opens her en-suite; the public washroom laid out by hand (two stalls and a basin along the far wall, no bench; the shared `washroom` template is unchanged). The Captain's window seat stays, and the two table seats it blocks are left out of `places` (6 table places). 159 places, all reachable (the place check in `claude/deck-architect` 06ec42e: OK). Only those rooms change on screen; Decks 1, 3, 4, 5 and 6 pixel-identical, Deck 4 ALL IDENTICAL. |
| 0.20.0 | Crowd rendering, workstream 5 (the performance engineer, from 0.14.0). New section 8b `crowd`: many crew drawn as a few skinned meshes, poses walk, stand, sit, lie and work, two levels of detail. `?crowd=40` demo: 40 made-up crew at dinner in Deck 3's mess hall. Section 8: `makeCharacter(spec, finish)` and `animateRig(..., rnd)` take optional extras (defaults unchanged); an unknown `dept` falls back to the Survey uniform. Main loop: `crowd.update(dt, t)`. The 9 crew stay on full rigs. Deck 4 ALL IDENTICAL against 0.14.0; Decks 1–6 pixel-identical; deck_check OK, same draw calls. See "Crowd rendering (0.20.x)". |
| 0.20.1 | The crowd demo with the real crew (the performance engineer, from 0.23.0). `?crowd=N` (up to 76) takes looks from `ROSTER` through `rosterSpec` (not Rina or Brennan, who are on Deck 3 as full rigs) and Deck 3's own places: servery queue, grab shelf, two galley stations, three walkers, the 44 mess seats, then the 22 benches. It sets 18:30 with `setShipNow`, and `?crowd` counts as `?nosave` (one change to `NOSAVE` in section 13). Round-table chairs face their table. `GAME_BUILD` and the header say 0.20.1. Deck 4 ALL IDENTICAL against 0.23.0, Decks 1–6 pixel-identical, deck_check OK with the same draw calls. |
| 0.21.1 | Pillar 1, workstream 4: the schedule engine (the sim engineer). New section 14 (after 13): `planDay(person, day)` and `whereIs(person, t)` per the plan's format, `shipDay(day)` planning everyone's day at once so no place is ever held twice, fixed work stations per person and shift, `peopleOn(deck, t)`, and `runDay` / `dayReport` to step a whole day with no drawing (about 30 ms a day). Reads `ROSTER` and `DECKS[n].places` when they're there, otherwise `STUB_ROSTER` and `stubPlaces(n)`. Sleeping (`sleepUntil`) plans the day you wake into. Nothing draws from it yet: cadet_test ALL IDENTICAL to 0.15.1 (renderer noise only), deck_check OK. With the real roster and the places pushed so far (a scratch build), 28 days check clean: everyone sleeps 6 hours or more in their own bed, eats twice and works their whole shift, no place double-booked, no gaps. |
| 0.21.2 | Going to sleep, and the lead's notes on places (the sim engineer). Tap your own bunk (4-B1-2, found by its place on Deck 4) from 20:00 to 05:30 and a small dialog asks "Sleep until 06:00?"; Sleep fades out, skips time with `sleepUntil` and fades back in to "Good morning". Earlier in the day the bunk says it's too early. Schedules: any place in a room with a bed place belongs to whoever sleeps there (en-suites, desks, armchairs), shared by roommates in a bunk room; the player is left out of the schedules. With every deck's real places (Decks 1–6, scratch build), 28 days clean and none of the 104 private places ever used by anyone else. cadet_test ALL IDENTICAL to 0.21.1 (renderer noise only), deck_check OK. |
| 0.23.0 | Pillar 1, first combined build (the lead, on `claude/ship-integration`): ship time and saving (0.15.1), the crew roster (0.16.2), places on every deck (0.17.0, 0.18.3, 0.19.2), Deck 4's bigger bunk rooms (0.17.1), crowd rendering with the `?crowd=40` demo (0.20.0) and the schedule engine (0.21.1). Merge fixes only: the HUD build line, `GAME_BUILD` and this table. Nothing draws the schedules yet (workstream 6). |
| 0.24.0 | Second combined build (the lead): 0.23.0 plus the player's berth moved to 4-B1-4 (0.16.3) and the crowd demo with real crew on real seats, the ship clock, and no saving under `?crowd` (0.20.1). Merge fixes only: the HUD build line, `GAME_BUILD` and this table. |
| 0.22.0 | 0.23.0 merged into `claude/sim-engineer` with 0.21.2 (going to sleep, private places by room), as the base for workstream 6. No other changes. |
| 0.22.1 | Pillar 1, workstream 6, turn 1: the crew follow their schedules on the deck (the sim engineer). The nine placeholder walkers and `Walker.think` are gone; everyone `whereIs` puts on your deck is a `CrewAgent` drawn by the crowd: walking the grid to their place, sitting, standing, working, lying in their own bunk (upper berths at 1.6 m), queueing at the servery, and arriving and leaving by the lift car. You find them mid-activity when you arrive (at their place, or partway there), and after a sleep. Crew open doors as they pass, and the 'closed' door of their own room or destination. Tap a crew member to talk (name, role, bio). You can't walk through anyone standing. The stubs are gone (the real roster and places cover everything). `DECK3_EVENING_MAX` caps Deck 3 in the evening (no cap yet). With crew switched off in both, cadet_test is ALL IDENTICAL to 0.22.0 (0.22.0 without its walkers); with crew, only the crew differ. deck_check OK. Four ship hours on Decks 3 and 4: nobody stuck, no one without a path, no place held twice. |

Deck 4's static screenshots are pixel-identical from 0.5.0 through 0.5.7. The only Deck 4 changes are the spine and lobbies (not in the harness views), and crew routes that shifted when Pell left and when the car and benches changed which tiles are walkable.


## Ship time and saving (section 13, the sim engineer, 0.15.x)

Section 13 sits after section 5 (lighting) and before section 6, not at the end: the clock drives the light, and the save has to be read before section 10 builds the first deck. Nothing in it calls `R()`.

- **Time.** `SHIP.time = { day, min }` (day 1 is a Monday; `min` is fractional ship minutes since midnight). `SHIP_RATE = 1440 / 1800`. `shipNow()` gives absolute ship minutes, `weekday(day)` 0 = Monday … 6 = Sunday, `hhmm(min)`, `clockText()` for the HUD, `setShipNow(abs)`. `tickShip(dt)` is the main loop's step: it does nothing while `document.hidden`, updates the HUD each ship minute and saves each ship hour. The ship doesn't run while the game is closed (no catch-up on load).
- **Jumps.** `skipTo(abs)` moves time forward only, calls every function in `SIM_ADVANCE` with `(from, to)` in absolute minutes, then updates the clock and saves. `sleepUntil(min)` skips to the next time `min` comes round (from 22:15 to 06:00 tomorrow; from 05:00 to 06:00 today). `SIM_ADVANCE` is the hook for the schedules (section 14) to advance everyone's state with no drawing; nothing is registered yet. There is no in-game way to sleep yet (a tap on your bunk is the obvious one, for later).
- **Light.** `nightAt(min)` is 0 by day and 1 by night: 1 from 21:30 to 05:30, easing (smoothstep) through dusk 20:30–21:30 and dawn 05:30–06:30, so it is .5 at 21:00 and 06:00. The main loop eases `nightT` toward it exactly as it used to ease toward `nightTarget`, so per-deck mood light (`applyLight`, `light` in a deck definition) is unchanged. On load `nightT` starts at `nightAt()` so a resumed game wakes in the right light.
- **The Night/Day button** is a debug control, hidden unless the URL has `?debug`. By day (`nightAt() <= .5`) it reads Night and skips to 21:40; by night it reads Day and sleeps until 07:40. Both are `skipTo` jumps, so they also exercise `SIM_ADVANCE`. Those are the old button's times, which keeps cadet_test's night shot comparable.
- **Saving.** localStorage key `starship-cadet-save`, JSON `{ v: 1, build, time: { day, min }, player: { deck, tile, facing }, ship: { decks: { n: { open: [door keys] } } }, crew: {} }`. `ship.decks` holds the doors unlocked per deck (`SHIP.decks[n].open`; only decks with any). Written by `saveGame()` every ship hour, at the end of `goToDeck`, on `visibilitychange` (hidden) and `pagehide`, and after any `skipTo`. `loadGame()` returns null (a fresh start) for no save, a `v` it doesn't know, a deck that isn't built, or anything malformed. Every read and write is in try/catch, so blocked or missing storage just means no saving.
- **Starting.** `START` is `{ deck, tile, face }` from the save, or `{ deck: 4 }` fresh. Section 10 builds `DECKS[START.deck]` and makes the player with `{ ...PLAYER_SPEC, deck: START.deck }` at `START.tile || PLAYER_SPEC.start`; a saved tile that's no longer free falls back to the nearest open one. A resumed game says "Welcome back. Day 3, Wednesday 22:15." instead of the wake-up toast. `GAME_BUILD` (section 13) holds the build number written into saves: bump it with the header's build line.
- **New game** (button, tap twice within 4 s): clears the save and unlocked doors, sets Day 1 06:00, rebuilds Deck 4 with `goToDeck`, puts you back on `PLAYER_SPEC.start` facing as at the start, and saves the fresh game.
- **URL flags.** `?nosave` turns saving and loading off; `?debug` shows the Night/Day button. cadet_test.py loads every build with `?nosave&debug` (builds before 0.15.1 ignore both), and deck_check.py uses the same loader.
- **Hooks in shared code (all small):** the HUD's clock text and the New game button (HTML); `nightTarget` gone from section 5; `updateClock` and the Night button in section 11 call into section 13; `goToDeck` ends with `saveGame()`; section 10 builds `START.deck` and places the player from `START`; the start toast picks welcome back on a resume; the main loop calls `tickShip(dt)` and eases toward `nightAt()`.
- **Testing 0.15.1.** cadet_test against 0.14.0 differs on purpose (the dawn light at 06:00, the clock text, the New game button). To prove nothing else changed, make a test copy that pins the old clock: `SHIP_RATE = 1`, `SHIP_START.min = 7 * 60 + 40`, `clockText` returning `'Ship time ' + hhmm(...)`, the HUD's first text back to "Ship time 07:40", and the New game button `display:none`. That copy is ALL IDENTICAL to 0.14.0, 0 pixels different. Saving was tested with an ad-hoc script: hourly and deck-change saves, a reload resuming deck, tile, facing and time, unknown `v`, junk and unbuilt-deck saves ignored, storage that throws, `?nosave` neither reading nor writing, New game, the hidden-tab pause, `sleepUntil` and the `SIM_ADVANCE` call.

## Schedules (section 14, the sim engineer, 0.21.x)

Section 14 sits right after section 13. Nothing in it calls `R()` or draws anything; every choice comes from `schedU(seed, day, k)`, a hash, so the same crew and places always give the same day, and adding a new decision (a new `k`) doesn't shift the others.

- **Interface.** `planDay(person, day)` gives `[{ from, to, act, deck, type, placeId, fromDeck?, tag? }, ...]`, back to back over the whole day, in absolute ship minutes (`shipNow()`'s units). `whereIs(person, t)` gives `{ deck, act, type, placeId, moving, fromDeck, until, tag }`. `moving` is true only during a lift ride (`act: 'commute'`, `deck` is the deck you're going to, `fromDeck` the one you left). `peopleOn(deck, t)` lists everyone there. `runDay(day, step, fn)` calls `fn(t, [{ p, w }])` every `step` minutes. `dayReport(day)` runs day_check's checks for one day. `schedPeople()` is everyone (the roster plus `ROSTER_GUESTS`).
- **Acts:** `sleep`, `wash`, `breakfast`, `dinner`, `work`, `leisure`, `gym`, `callhome`, `commute`, `off`. Tags say more: `queue` (at the servery before a meal), `grab` (grab-and-go), `tea` (a tea break, counted as work), `rest` (leisure in your own bunk or cabin), `laundry`, `inspection`, `drill`, `room` (washing in your room when every shower and basin was busy).
- **How a ship day is planned (`shipDay`).** Everyone is planned in one pass, in wake-up order (ties by id). Each person's day is built start to finish, taking places that nobody holds yet (`occ`: place → time ranges). When the showers, the servery or the grab shelf are busy, they wait a few minutes where they are, then fall back (shower → basin → their room; mess seat → lounge seat or bench → standing). The last five days are kept.
    - **Beds** are always the person's own (`person.bed`).
    - **Private places:** a place named after a bed (`4-05-wash`, `2-C-wash`) belongs to whoever sleeps there, and nobody else is offered it.
    - **Work stations** are fixed (`schedDesks`): in rank order, each person takes the next station of their type on their work deck, separately for the day and night shifts. Overflow goes to another `work:*` station on that deck nobody on the shift has, else `placeId: null`.
- **A day's shape (`schedFrame` and `schedBuild`).**
    - **Day shift (08:00–17:00):** wake about 06:15, then a wash and breakfast (06:00–08:00) before work; a tea break mid-shift for `tea-break`; then evening specials, dinner (17:00–20:30), leisure and bed about 22:45.
    - **Night shift (21:00–06:00):** after the shift, breakfast, a wash and about 7 hours' sleep through the day, then an evening like anyone's and back on at 21:00. Coming back after a night off: a normal night's sleep, then a four-hour nap in the afternoon.
    - **Days off:** later waking, then leisure.
    - Wake time always leaves 6 h 50 min after the previous bedtime.
    - No lunch, as the design says: two meals a day.
- **Variety, in layers:**
    1. **The rota.** `rota.offDays` gives the days off. A night-shift person's day belongs to the shift that starts that evening.
    2. **The weekday (`WEEK_SHAPE`).**
        - Monday: briefing, the day shift starts 10 minutes early.
        - Wednesday: a 15:00 drill; anyone at leisure musters at a `lift-wait` place for 15 minutes.
        - Thursday: bunk inspection; juniors in Deck 4 bunks spend 10 minutes at their bunk after washing.
        - Friday and Saturday: bedtimes 30 and 20 minutes later.
        - Sunday: anyone off duty lies in 30 minutes longer.
    3. **Jitter.** Waking 5–25 minutes either way, meal lengths, block lengths.
    4. **Habits.** All 18 in `HABITS`:
        - early-riser, late-sleeper, early-to-bed and night-owl move wake and bed times;
        - skips-breakfast, late-diner and lingers-at-meals change meals;
        - workaholic means 15–30 minutes early and late at work;
        - tea-break is a break mid-shift;
        - gym-regular and calls-home are in the specials below;
        - garden-lover, lounge-regular, quiet-corner, common-room and music weight leisure places (`HABIT_LEISURE`);
        - evening-shower moves the shower to before bed;
        - window-seat does nothing yet: no place says it's by a window.
    5. **Need (`schedWants`).** The gym, a call home and the weekly laundry (on the first day off). A habit's pull is raised when it hasn't happened in three days.
- **Leisure choice.** `LEISURE` plus the person's habit places. Places on the deck you're on count four times and the place you just left a fifth, so people don't hop decks every hour (about 5 lift rides a day each). `[bedDeck, 'rest']` is time in your own bunk or cabin. Juniors get Deck 4's common room; officers and up get Deck 1's observation room (`common-room` on Deck 1).
- **Stand-in data.** `STUB_ROSTER` (12 people) and `stubPlaces(n)` are used only where the real ones are missing: `ROSTER` from section 9, and each deck's `places` (a deck with none gets stub places named in the plan's scheme, with ids like `3-mess-seat-1`). Once the real roster and Deck 2's places are merged, the stubs go unused; delete them then.
- **Private places (0.21.2).** `owner` maps a place to the beds it belongs to. A place belongs to a bed when it's named after the bed (`4-05-wash`), or when it's in the same room (`room`) as one or more bed places: an en-suite, a desk or an armchair. Only the owners are offered it. A place with one owner never needs checking; a place shared by bunk-room mates is still checked for overlaps. Roster entries with `player: true`, or with the player's bed, are left out of `schedPeople()`.
- **Going to sleep (0.21.2, section 13).** `offerSleep(worldPos)` is called by the item tap in section 11 (one-line hook) before the item's own toast. If the tapped item is within 1.2 m of the player's bed place (`PLAYER_BED = '4-B1-2'` in `DECKS[4].places`, or tile [7, 1] while there are no places), it handles the tap:
    - From 20:00 to 05:30 (`bedtime()`) it opens the `#sleepAsk` dialog (styled like the lift panel). Sleep fades `#fade` out, calls `sleepUntil(WAKE_AT)` (06:00), fades back in and says "Good morning". Not yet or Escape closes it.
    - At other times it says it's too early.
    Note: Bunk 1's item text calls the bunk at [9, 1] "Your bunk", while the places put 4-B1-2 at [7, 1], with Tomas (4-B1-1). Sleep follows the places.
- **Sleeping.** `SIM_ADVANCE` gets a function that plans the day you skip into. There's nothing else to advance: `whereIs` is worked out from the plan, not stepped.
- **Numbers (real roster and the places pushed so far, Deck 2 on stubs):**
    - Over 28 days: nobody under 6 hours' own-bed sleep (counted from 18:00 the evening before), everyone eats twice and works their whole shift, nothing double-booked, no gaps, and each day joins the next exactly.
    - Unplaced (standing) moments: the Wednesday drill (Deck 1 has 4 `lift-wait` places), and a few when someone lingers where their place is wanted.
    - Peak headcounts per deck: Deck 3 about 64–73 at 17:45–18:20 (dinner plus the Commons in the evening), Deck 4 about 60 at 06:45, Deck 2 about 20, Deck 5 about 13, Deck 1 about 10, Deck 6 3.
    - Speed: planning a day takes about 11 ms; `runDay` at 1-minute steps about 30 ms; `dayReport` about 17 ms.
- **Testing it:** a scratch copy of the build with section 9's `ROSTER` block and the architects' `places` lists pasted in (not committed), then `dayReport(d)` for many days, the seams between days, and determinism (the same plans after clearing the cache and planning other days first).
## Places on Decks 4, 5 and 6 (0.17.x, the Deck 6 architect)
Pillar 1, workstream 3a; the format is in plans/pillar1-plan.md, "Places". Each of `DECKS[4]`, `DECKS[5]` and `DECKS[6]` has a `places` list, written as plain data just before `lockedRoom` (Deck 4) or `markings` (Decks 5 and 6).
- **Where they sit.** On the furniture that's there: the tile of a seat, bed, bench or stall, or the free tile in front of a bench, console or machine for someone standing at it. Seats and beds are reached from a tile beside them. Nothing was moved to make room for them.
- **`face`** is the way the person faces there: away from a seat's back, towards a console. For beds it points at the side you get in from.
- **Deck 4 bunks (0.17.1, Sketch 3):** each bunk room is 5 × 4 with three bunk beds, so berths 1–2 are the first bunk (lower, upper), 3–4 the second and 5–6 the third, both berths on the bunk's tile. The rooms number 1–8 as the game names them (a = Bunk 1 … h = Bunk 8, the night shift).
- **Wash pods:** every cabin's pod is one `shower` place (`4-xx-wash`); it stands for the pod's toilet and basin too.
- **The check:** deck_check.py checks every place: unique ids ship-wide, the agreed types, poses and faces, the room against the map, and that crew can reach it from the lift. Crew have keys, so 'closed' doors pass; hatches and walls don't.
- **Fixed in 0.17.1:** Deck 4 slept only 32 juniors in 0.17.0. Sketch 3 of plans/deck4-plan.html widened the bunk rooms to 5 tiles, so the bunk template fits three bunks: 48 berths.
- **`floorSeeds` (0.17.1, shared, inert unless a deck sets it):** the floor painter draws random numbers tile by tile, row by row, so a layout change shifts every later number: the floor grain and every piece of furniture and crew choice after it. `floorSeeds: { col, rows }` sets the random sequence to `rows[j]` when the painter reaches column `col` of row `j`. Deck 4 uses column 21 with the values 0.17.0 had there, so everything east of the junior wing, and everything built after the floor, is unchanged. If the junior wing changes shape again west of column 21, keep the values; if anything at column 21 or east of it changes, the values need measuring again (or dropping, if pixel identity isn't wanted).
- **0.17.1 proof (Deck 4, 0.17.0 against 0.17.1):** map cells changed only in columns 10–20; wall and door edges up to column 21; blocked tiles up to column 20; items, spots and closed doors in the officers' wing (columns 24 and on) identical; room tiles changed only in rooms a–h and l; 326 of 3000 collision probes changed, all at column 21 or west; all 9 test routes wholly in the officers' wing and east lobby identical. An officers'-wing view with crew hidden differs only where the shrunk scrubbers room shows over the wall at the top edge. The player still starts at (7,3) in Bunk 1. Crew start in the same places, but drift apart within seconds: the placeholder wander shares one random sequence between all crew, and the bunk rooms offer different spots, so cadet_test differs throughout (as expected; the new baseline needs the lead's sign-off).

## Crew on the deck (section 10, the sim engineer, 0.22.x)

- **Agents.** `DECK_CREW` holds a `CrewAgent` for everyone `whereIs` puts on the deck you're on. Each frame (`updateDeckCrew`, called from the main loop before `crowd.update`):
    - An agent asks `whereIs` where they should be: a place id; null (stand where you are); or, when their schedule has them on another deck, `'@lift'` (walk into the lift car and vanish).
    - When the goal changes they `retarget`: up from the seat to its walk-to tile, then a path (`crewPath`) to the new place's walk-to tile, then a short glide onto the exact spot, and the place's pose (`lie` for any bed).
    - Every quarter second, anyone due on the deck who isn't there arrives: out of the lift car when their ride ends, or straight at their place if they were missed.
- **Where a place is (`placeSpot`).** The walk-to tile is the place's `walk`, its own tile if open, or the open neighbour nearest the spot. The spot is `xy`, or the tile centre. Beds without `xy` use the middle of the nearest bunk, bed or futon item, since a bed covers two tiles. Upper berths (even-numbered `4-B<n>-<berth>`) lie at 1.6 m; everything else uses the crowd's default heights.
- **Arriving on a deck (`deckCrewFill`).** Called from `goToDeck`, at load, and after any time skip (`SIM_ADVANCE`). Everyone is placed mid-activity. If their current activity started less than a walk ago, they're partway along the path from where they were (their previous place on this deck, or the lift), and keep walking; otherwise they're at their place. People still riding the lift step out when the ride ends.
- **Locked doors.** `crewPath` is `findPath` with the 'closed' doors into the agent's rooms opened for the call: the room of their own bed and the room of the place they're going to. `crewNearDoor(d)` opens a door for any agent walking near it; for a 'closed' door, only for agents whose rooms it leads to. Hook: two lines in the main loop's door code. The player still can't pass.
- **Crew and you.** Crew don't block each other (they never share a place, so they only cross in passing). Standing crew push you out when you steer (`Walker.update`), and `occupiedBy` keeps your paths off their tiles. Tap a crew member (`tapCrew`, by screen distance to their body) and they stop for 6 seconds, facing you if they're on their feet; the toast gives their name, role and bio. The Crew button hides the crowd (`crowd.visible`); they carry on unseen.
- **Stuck.** `stuck` counts ship minutes an agent meant to move but didn't; `stuckMax` keeps the worst. `noPath` counts times there was no way to a place (the agent is then simply put there).
- **The old walkers.** `CREW` (section 9) stays as data; `crew` is an empty array for the code that still loops over it. The rig, the player's `Walker` and its R() calls are unchanged, so with crew off nothing else moves.
- **Draw calls (0.22.1, by the lift at 06:00):** Deck 4 with 52 crew, 319 (0.22.0 with its five walkers: 346); Deck 3 at 18:00 with 63 crew, about 307–325.
- **Next (0.22.2):** full rigs for story crew near you, and day_check.py.

## Deck 2 (builds 0.9.x, the Deck 2 architect)

Built from plans/deck2-plan.html (Sketch 8) on branch `claude/deck2-command`, alongside the Deck 1 architect (0.8.x). Everything for Deck 2 sits in one block in section 4d, between Deck 3 and Deck 6: the `// ---- Deck 2 kit ----` (materials `D2`, new pieces added to `KIT` and `WALL_KIT` with `Object.assign`, nothing calls `R()` at load) and then `DECKS[2]`. No shared engine code was changed.

- **Turn 1, the shell (0.9.1).** The plan's data went in as it was, with two fixes:
    - The plan listed `v,23,9` as Watch office glass, but that edge is between the lobby and the science corridor (both halls), so it would have walled off a row of the lobby. Dropped. The Watch office's glass is `v,23,6` and `v,23,8` either side of its door `v,23,7`.
    - The plan's Watch office plate was on `v,23,4`, which faces into the Second Officer's cabin. The plate is on `v,23,5` (now plain wall) instead.
    - **Bedroom plates** are brass plates on the header above each door (`nameplates`, wall kit `brassPlate`), not the teal plates beside it: Vance's and the Envoy's corner cabins have no wall beside their doors, and a plate over the door can't be mistaken for the neighbour's. Names: Capt. Marrow, Cdr. Vance, Works Chief, Infirmary Chief, Dr. Sato, Second Officer, Envoy Saruth, Chief Holt, Visitors, Senior Helm, Comms Chief, Counsellor, Watch Officer, Survey Deputy, Visitors. The six new officers are placeholders, by role.
    - **Mood light:** `sky #e9e6ff`, `sun #fff0dc`, `hemi .94`, `sunI .96`: a touch cooler in the shade and softer in the sun.
    - About 220 draw calls by the lift (empty shell).
- **Turn 2, the bedrooms (0.9.2).**
    - **`d2Suite(room, doorKey, o)`** furnishes a bedroom from its door. Bedroom doors are `closed`, and `roomFrame` only finds `door` and `open` edges, so `d2Frame` takes the door key instead (same frame: u along the door wall, v into the room). Layouts are drawn with the door in the left half and mirrored otherwise. Three layouts: hull cabins 4 × 5 (bed under the windows, desk on the far wall, en-suite in the front corner, wardrobe and armchair by the door, bookcase and plant at the back), the 3 × 5 cabins by the lift (V, H), and inner 4 × 4 cabins (`inner`, with a desk or `armchairs`). Options: `fab` (headboard, throw and armchair), `rug`, `papers`, `kettle`, `model`, `swans`, `trophy`, and `bed` / `desk` tap text.
    - **Corner cabins** X (Vance) and E (Envoy Saruth) are placed by hand, clear of the rounded stern corner.
    - **Taps:** every bedroom has one or two `see` items (bed, desk, the Envoy's tea table): tap them through the cutaway and the text shows without walking, since the doors stay shut. That's how the player sees into the bedrooms.
    - **Cost:** all bedroom kit uses shared `D2` materials and the rooms are `NO_FADE`, so they merge with the rest of the deck: about 250 draw calls by the lift, 290–310 over the quarters with walls down, about 540 zoomed right out (Deck 3 is 520–560 at that zoom). No glow sprites in bedrooms; the lamp shades are emissive.
- **Turn 3, the Captain's quarters and the corridor (0.9.3).**
    - **Captain's quarters `C`** (room-local 5 × 12, stern windows on the west wall at x 0, door `v,7,10` at z 5.5): wide `suiteBed` (`wide: true`) at (2.3, 1.2) with the en-suite and wardrobe by it, `alcoveCurtain` across z 3.0 (x 0.15–3.35, open on the door side), telescope at (.7, 4); `diningTable` at (2.3, 6.4) along the room with `light: true` (the deck's one real lamp; `LAMP_SLOTS` is 2), window seat on the stern wall, sideboard by the door; study: `captainDesk` at (2.25, 9.4) facing the room, low `suiteShelf`s along the south and east walls (tall bookcases hid the study from the usual camera), a globe and an armchair by the windows.
    - **Corridor:** `brassSconce` on ten wall edges (two flanking the Captain's door), `portrait`s on `v,7,7`, `v,7,13`, `v,9,8`, `v,9,13` (tappable: Varga, Moro, Brenner, Marrow; the three paintings are canvases drawn at load, no `R()`), `consoleTable`s (snug) under the gallery's east portraits.
    - About 255 draw calls by the lift, 330 over the Captain's quarters with walls down.
- **Turn 4, science, the Watch office and the array (0.9.4).**
    - **Kit:** `chartTable` (its top is `D2.chart`, a star chart drawn at load from a fixed hash), `chartRack`, `labBench` (`scope`, `centrifuge`), `labIsland`, `sampleScanner`, `specimenShelf`, `brassTelescope`, `commsDesk`, `signalBoard` (`D2.wave`), `fumeHood`, `gloveBox`, `probeCradle`, `launchTube`, `signalRacks` (`D2.rack`), `mastBase`, `sensorDish`, `humJar`; wall kit `starChart`. Reused: `controlBoard`, `desk`, `locker`, `dispenser`, `crate`, `coldShelf`, `windowSeat`, `stool`, `beanbag`, `clocks`, `msgBoard`, `notices`, and the `washroom` template.
    - **The dish** (`sensorDish` in `A` at (3.2, 10.5), turned to face the bow): a turntable group built, then merged on its own with `mergeMeshes(tt)` and marked `noMergeAll`, so it turns as a few meshes (`SPINS`, 0.12 rad/s). The feed's material and glow are made at dress time and breathe (`PULSES`). `light: true` adds the deck's second real lamp and tints it blue (`LAMPS[...].l.color`), so Deck 2 uses both `LAMP_SLOTS`. The humming sample in the specimen store pulses the same way.
    - **Locked rooms** F, P and A are `NO_FADE`; their taps are `see` items.
    - **Memory:** Deck 2's shared textures (rugs, portraits, charts, waveforms, rack lights) are made at load and upload on the first visit, then stay, like Deck 5's hatch textures. deck_check's Deck 4 round trips stay steady (496 geometries, 34 textures).
    - **Cost:** about 285 draw calls by the lift (Deck 3 326, Deck 4 332), 230–300 over the science rooms with walls down, 540–580 zoomed right out over the quarters.
- **0.9.5:** `hull.byFace: true` on Deck 2 (the shared splitter edit from the bridge branch, opt-in per deck; Decks 3–6 keep the old split).
- **Deck 2 is done (0.9.4, hull fix 0.9.5) and waiting for the user's review.**
- **Places (0.19.1, Pillar 1 workstream 3c).** `DECKS[2].places` lists 162 places, made from the furniture's real positions (a script logs every `place()` on Deck 2, then puts a place on each seat, bed and workstation) and stored as fixed data.
    - **Ids:** beds `2-<room letter>` for all fifteen bedrooms, visitors' rooms included. Everything else `2-<what>-<n>`: `shower`, `basin`, `toilet` (en-suites, numbered in placing order), `wctoilet` and `wcbasin` (the public washroom), `desk`, `armchair`, `cushion`, `windowseat`, `beanbag`, `captable`, `command`, `survey`, `comms`, `watch`, `bench`, `liftwait`.
    - **Types:** desk chairs and armchairs in bedrooms are `lounge-seat`; the Captain's desk chair is `work:command`. Rule proposed to the lead: a place in a room that has a bed place belongs to that bed's owner, so nobody is sent into someone else's cabin.
    - **Watch posts:** the roster puts 8 Watch crew on Deck 2 by day and the office has 4 work spots (duty chair, status board ×3), so four standing posts make up the rest: the lockers, the lobby by the office glass, outside the Captain's door, and the end of the science corridor at the array window.
    - **Locked doors:** every bedroom door is `closed`, so today's pathfinding can't take anyone to a bed. Raised with the lead (proposal: a walker may pass a `closed` door whose `sealed` room holds their own bed).
    - **Layout fixes (0.19.2):** some places were boxed in by furniture: S's and R's interiors, Vance's cabin, the Captain's en-suite, two of the Captain's table seats and two of the public washroom's three toilets. Fixed by moving S's and R's armchair, Vance's wardrobe and seating, and the Captain's wardrobe, and by laying the washroom out by hand (2 toilets, 1 basin). The Captain's window seat stays (the lead's call), so the two table seats behind it aren't places. 159 places, all reachable by the official place check.

## The crew roster (builds 0.16.x, the crew designer)

Pillar 1, workstream 2. Everything is in section 9, after `CREW`, between the `BEGIN ROSTER` and `END ROSTER` markers, plus two lines below them.

- **`ROSTER`:** 74 of the 75 crew in the format of plans/pillar1-plan.md "The roster". With you, that's 1 Captain, 1 XO, 4 Chiefs, 6 Senior Officers, 16 Officers and 47 Juniors; 60 on days, 15 on nights. Each entry has `id`, `name`, `story`/`provisional` flags, `rank`, `dept`, `uniform`, `role`, `shift`, `rota.offDays`, `bed`, `work: { deck, place }`, `habits`, `traits`, `looks`, `bio`, `life` and `seed`.
    - `dept` is the job's department: command, helm, comms, works, watch, survey, infirmary or galley. `uniform` is the uniform it wears, one of `makeCharacter`'s five `DEPT` keys (helm and comms wear command red, the galley wears works gold). `rosterSpec(p)` turns an entry into what `makeCharacter` takes.
    - Story crew keep `CREW`'s looks and bios exactly. The Works Chief (Chief Ines Calder), the Infirmary Chief and the six senior officers have provisional names.
    - Workplaces use the place types `work:command`, `work:helm`, `work:ops`, `work:comms`, `work:watch`, `work:survey`, `work:galley`, `work:infirmary`, `work:works` and `work:engine`.
    - Days off: two in a row, staggered round the week within each department (20–22 people off on any day).
    - Night shift: the 6 juniors in Bunk 8 (the night-shift room), the Second Officer, the Senior Watch Officer and 7 officers (in the quiet inner cabins).
- **`ROSTER_GUESTS`:** people who live aboard but aren't crew, so not in the 75: Envoy Saruth (bed `2-E`).
- **`ROSTER_PLAYER`:** you. You're one of the 75 (one of the 47 juniors, in Works) but aren't scheduled, so your entry is kept out of `ROSTER`. You sleep in Bunk 1, berth 4 (`4-B1-4`), the top of the second bunk, as Bunk 1's furniture text says (you lost the coin toss for the bottom one); Tomas has berth 1 under his taped star map, Chloe Tran berth 2 above him, and berth 6 is the one spare berth on the ship.
- **`HABITS`:** the shared habit vocabulary, each with what it does to a day. The schedule engine reads it.
- **Beds:**
    - Deck 2: the 12 senior crew, one per room (`2-C` Captain, `2-X` Vance, `2-O` Works Chief, `2-I` Infirmary Chief, `2-V` Sato, `2-T` Holt, `2-S`, `2-H`, `2-R`, `2-N`, `2-G`, `2-D`); visitor rooms `2-B` and `2-U` are empty.
    - Deck 4 cabins: the 16 officers in `4-05`, `4-06` and `4-09` to `4-22` (none in the guest cabins or spares).
    - Deck 4 bunks: the 47 juniors (you included) in 8 rooms × 6 berths (`4-B<n>-1` to `-6`), with `4-B1-6` spare. As of 0.14.0 the rooms hold 4 berths each (2 double bunks); the user chose bigger rooms with three ordinary bunk beds, which workstream 3a is building.
- **Fixed data:** `plans/crew-roster-gen.py` is seeded, so re-running it without edits writes exactly the same block. Edit it (names, habits, who's where) and re-run to change the crew; it rewrites the block in place and `plans/crew-roster.html`. Nothing in the roster calls `R()`.

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


## Crowd rendering (0.20.x)

Section 8b, by the performance engineer (Pillar 1, workstream 5). The player and close crew keep full `makeCharacter` rigs (16–17 meshes, about 15,000 triangles and 32 draw calls each with shadows). Everyone else goes through `crowd`.

**How it works.**

- `crowd.add(spec)` calls `makeCharacter(spec, finish)` with a `finish` that keeps the queued parts instead of baking meshes. The rig's joints stay ordinary Groups, kept out of the scene, and `animateRig` drives them exactly as it drives a full rig.
- Each person's parts are rebuilt at lower detail (`CROWD_DETAIL`: spheres, caps, cylinders and rings with fewer segments; boxes as they are) and packed once, in their joints' own space, at two levels: near (about 4,100 triangles) and far (about 2,100).
- Up to `CROWD_PER` people (12) share one `SkinnedMesh`. Their joints are its bones (17 slots a person); every vertex follows one bone, and the bone inverses are identity, so a bone's matrix is just the joint's world matrix. One material, `CROWD_MAT` (as `CHAR_MAT`, with `skinning: true`, which r128 still needs). So 40 people are 4 meshes: at most 8 draw calls with the shadow pass.
- A group's geometry is rebuilt only when someone joins, leaves or changes detail. Its bounding sphere is refitted every frame round its members, so a group off screen isn't drawn.
- Far detail: anyone more than `CROWD_FAR` (9) tiles from the camera's target, or everyone when zoomed out past `CROWD_FAR_ZOOM` (0.75), with half a tile of hysteresis.
- Without float vertex textures (rare on phones now), `CROWD_PER` shrinks so a group's bones fit the shader's uniforms.
- Nothing in the crowd calls `R()`: each person has their own random stream (`animateRig`'s new `rnd` argument), so adding crowd never shifts anything else. `CROWD_MAT` and the empty geometry are made on the first `add`, so a game with no crowd has none of it.

**Interface** (for the sim engineer):

- `const h = crowd.add(spec)`: `spec` is the roster's `looks` plus `dept` and `rank` (for the uniform).
- `h.set(pos, face, pose, walkPhase)`: `pos` is a world `{x, y, z}`; for `sit` and `lie`, `y` is the seat or mattress top (0 means a usual chair, 0.475, or bunk, 0.5). `face` is an angle like `Walker.face` (0 looks toward +z); for `lie` it's the way from head to feet. `pose` is `walk`, `stand`, `sit`, `lie` or `work`; changes blend over about half a second, except the first `set`, which snaps. `walkPhase` (gait cycles) is optional: leave it out and the gait follows how far `pos` moves each frame.
- `crowd.remove(h)`, `crowd.clear()`, `crowd.near(x, z, r)` (who's at a spot, for taps; the meshes themselves are never hit by the tap raycast), `crowd.visible`, `crowd.stats()`.
- `crowd.update(dt, t)` runs once a frame from the main loop, after the walkers.
- Sitting puts the hips just above the seat and the feet on the floor by leg IK, forearms on the table, a fork to the mouth now and then. Working: hands busy at bench height, head down. Lying: on the back, arms by the sides, centred on `pos`.
- Crowd people don't block walking. Who stands where is the sim's job (workstream 6).

**The demo.** `?crowd=40` in the address (any number up to 76) starts you on Deck 3 by the lift at 18:30 and puts that many of the real crew (from `ROSTER`, day shift first, not Rina or Brennan) on Deck 3's own places: the servery queue (stand), the grab shelf, two galley stations (work), three people walking the mess hall's aisles, the 44 mess seats, then the 22 benches. A line under the clock shows the crowd, draw calls and frame time. They leave when you leave the deck and come back when you return; the Crew button hides them. `?crowd` works as `?nosave`, so the demo never touches a save. Without the flag, `CROWD_DEMO` is `null` and nothing of the demo exists.

**Numbers** (headless, SwiftShader; frame times there aren't meaningful, so the demo's line is the one to read on a phone):

| Deck 3 | Draw calls | Triangles drawn (both passes) | Crowd JS a frame |
| --- | --- | --- | --- |
| By the lift, no crowd | 326 | 285,000 | |
| By the lift, 40 crowd | 329 | 364,000 | about 2 ms |
| In the mess hall, no crowd | 242 | 240,000 | |
| In the mess hall, 40 crowd | 246 | 401,000 | about 2 ms |

With the real crew and places (0.20.1, on 0.23.0):

| Deck 3 | Draw calls | Triangles drawn (both passes) | Crowd JS a frame |
| --- | --- | --- | --- |
| By the lift, no crowd | 326 | 285,000 | |
| By the lift, 40 | 328 | 345,000 | about 1.2 ms |
| By the lift, 70 | 331 | 443,000 | about 1.8 ms |
| In the mess hall, no crowd | 242 | 240,000 | |
| In the mess hall, 40 | 246 | 391,000 | about 0.8 ms |
| In the mess hall, 70 | 248 | 486,000 | about 0.8 ms |

Each group of 12 adds at most two draw calls, so the count isn't the limit; triangles are. Seat and bed heights for the sim: see the rule sent to the sim engineer (bunks: odd berths 0.5, even 1.6; mess seats 0.475; benches 0.48; lounge seats vary, so places may carry a `y`).

For comparison, 40 full rigs would add about 1,300 draw calls and 600,000 triangles. Memory is flat over Deck 3 and 4 round trips with the demo on (the four groups' bone textures stay, like kit).

**Testing a crowd turn:** cadet_test and deck_check as usual (the crowd is empty in both). For the demo, open the build with `?crowd=40`; the Game class in cadet_test.py loads `file://` paths, so a script that adds the query to the `goto` is enough.


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
- **Scaled up (0.12.1, plan Sketch 2).** The bullets above give Sketch 1's positions; these replace them. 22 × 12, `lift: [8, 6]` (car rows 4–6, trunks row 3, ladder row 7, ladder hatch `h,7,8`), hull `bowFrom: 15`, world x −12…10, z −6…6. Standable tiles: bridge 85 (was 54), observation room 50 (was 40), ready room 12, washroom 6 (was 4).
    - **Rooms.** O cols 1–5; lobby cols 6–9 rows 2–8; k rows 0–1 and u rows 9–11 over cols 6–9; R cols 10–12 rows 0–3 (door `h,11,4`, plate `h,12,4`); w cols 10–12 rows 8–9 (door `v,10,8`); c cols 10–15 along the starboard edge (floor hatch `h,14,10`, painted at tile (14, 9)); B everything forward, with the vestibule cols 10–12 rows 4–7 inside the bridge doors (`v,10,5`, `v,10,6`).
    - **Command ring** `ring: [17, 6, 2.0]`, rail `arc: [17, 6, 2.4, 130, 230]`. Column 13 stays clear behind the rail, rows 3 and 8 either side of it. Captain's chair (16.8, 6), blocking its own tiles and the two behind it inside the rail; seats at z 4.85 and 7.15; helm and ops (19.4, 5.45 / 6.55) with seats at x 18.5; column 20 stays open in front of the viewscreen.
    - **Rear stations** against the bridge-side walls of R and w, facing the bow: Watch (13.4, 1.5), Survey (13.4, 2.5), Comms (13.4, 8.5), Works (13.4, 9.5) beside the floor hatch; seats at x 13.92.
    - **O:** table at z 6, seats z 4–8, briefing screen at 2.5, window seat at z 6, tea at z 8.9, plants at z .6 and 11.4. **R:** desk (1.5, 2.1) facing the door, chair (1.5, 1.3), visitors at x .6 and 2.4 (the door tile stays clear), aquarium (.36, .9), shelf (2.72, .9). **w:** basin (2.5, .32) and toilet (2.62, 1.45, facing west) down the far wall, reached from the middle.
    - **Draw calls (0.12.1):** 299 by the lift (0.10.1: 315), about 378 zoomed right out (was 364), 210–330 in room views.
- **Mood light:** `light: { sky #d4e2ff, sun #dfe8ff, hemi .96, sunI .9 }`, a little cooler and dimmer than the decks below.
- **Kit:** the Deck 1 block sits just above `DECKS[1]`: materials in `BRG`, pieces added with `Object.assign(KIT, ...)` (and `WALL_KIT`). Nothing there calls `R()`.
- **Doors cost a lot of draw calls on every deck** (about 120 of Deck 1's 256): each leaf is a box with six material groups. Grouping the four edge faces and the two leaf faces would cut that by two thirds with identical pixels, but changes the call counts the tests compare, so it's left for the lead.

## Places on Decks 1 and 3 (0.18.x, Pillar 1 workstream 3b)

The bridge architect's places, for the sim engineer's schedules (see plans/pillar1-plan.md, "Places"). Data only: nothing in the game reads or draws them yet.

- **Where:** `places: [...]` in `DECKS[1]` (just before its `dress`) and `DECKS[3]` (just after its `curves`). One place per line.
- **Fields:** the plan's `id`, `type`, `at: [c, r]`, `face`, `pose` and `room`, plus two more:
    - `xy: [x, z]`, the exact spot in tile units. A seat can sit off its tile's centre, and one tile can hold two seats (the mess benches seat four along 3.6 m), so `at` alone would stack people.
    - `walk: [c, r]`, the tile a person walks to before taking the place. It's `at` when that tile is walkable; otherwise the nearest tile in the same room, within 2.5 m, that can be reached from the lift. 122 of the 203 places need one: seats, booths, benches, toilets. Some can't be reached from a tile next door: the mess benches against the hull, which you slide into from the table's end, and the middle booths in the lounge.
- **How they were made:** a script logged every `place()` call's real position and rotation, and put seats where each kit piece draws them (the long tables' benches at ±.62 m, the round tables' chairs at .8 m, booths, bar stools, high tables, sofas, benches, planter islands), plus a few spots by hand: the servery queue, the galley pass and the lift waits. The output is kept as fixed data, so it only changes when someone means it to. If furniture moves, regenerate it or fix the lines by hand.
- **ids:** `<deck>-<what>-<n>`. Deck 1: `1-command-1` is the Captain's chair, `-2` the first officer's seat, `-3` the guest seat; `1-helm-1`, `1-ops-1`, `1-watch-1`, `1-survey-1`, `1-comms-1`, `1-works-1`; `1-conf-1..10` (the conference table), `1-tea-1`, `1-window-1..4`, `1-toilet-1`, `1-basin-1`, `1-lift-1..4`. Deck 3: `3-mess-1..44`, `3-queue-1..4` (in queue order, trays first), `3-grab-1`, `3-galley-1..8` and `3-galley-pass`, `3-infirmary-1..4`, `3-visit-1..2`, `3-toilet-1..4`, `3-basin-1..2`, `3-wbench-*`, `3-bench-*`, `3-garden-*` (bench seats), `3-tend-*` (beds and racks), `3-gym-*`, `3-callhome-1..4`, `3-lounge-*`, `3-store-1`, `3-shop-*`, `3-lift-1..6`.
- **Types beyond the plan's list:** `work:command` (the command ring), `work:store` (the crew store counter) and `shop` (browsing the shelves and the drinks fridge). The conference seats are `common-room`.
- **Counts:**
    - Deck 1 (31): `work:command` 4, helm 1, ops 1, watch 1, survey 1, comms 1, works 1, `common-room` 11, `lounge-seat` 4, toilet 1, basin 1, `lift-wait` 4.
    - Deck 3 (173): `mess-seat` 44, `servery-queue` 4, `grab-shelf` 1, `work:galley` 9, `work:infirmary` 4, `lounge-seat` 34, `bench` 22, `garden` 23, `gym` 9, `callhome` 4, `shop` 6, `work:store` 1, toilet 4, basin 2, `lift-wait` 6.
- **Ready room (0.18.3):** `1-ready-1`, the Captain's desk chair (`work:command`), walk tile (10, 1). Its door `h,11,4` is a closed door, which crew can open; `deck_check` counts closed doors as passable for crew.
- **Left out:** the infirmary's four patient beds (no type for them yet), and showers (none on these decks).
- **Held back in 0.18.2, back in 0.18.3:** `deck_check` didn't yet take `walk` or `shop`, so 14 Deck 3 places sat out one build. The lead has since made `xy`, `walk` and `shop` part of the plan, and `deck_check` (from `claude/deck-architect`) checks the walk rule.
- **Check:** every place is checked the way the plan says: `walk` is walkable, in the place's room, reachable from the lift, and equal to `at` or within 2.5 m of `xy`. ids are unique ship-wide, and `face`, `pose` and `room` are valid. The script is in the session scratchpad. `deck_check.py`'s own place check comes from the Deck 6 architect.

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
    - **Review fixes (0.11.0):** the user couldn't get into the engine room ("the back room, going left on screen; stuff is in the way") and found the watch room too small.
        - **Engine room `E`, now walkable:** `v,12,5` is a door; the catwalks are removed; `overlookRail` at z 4.85 and 7.15 (7.6 long) either side of the coils; `markings: [[3, 4, 8, 4]]`. The coils block room-local rows 5–6, x 1–8; rows 1–4 and 7–10 and column 9 (inside the door) are clear. `E` is no longer `NO_FADE`, so the coils fade when they'd hide you; `driveCoil`'s core mesh is `noMerge` so the fade's material copies don't stop it pulsing.
        - **Watch room `S`, 4 × 4 at the overlook's south end:** room-local armchairs at (.9, 1.1) and (.9, 2.9) facing the window (`'e'`), tea table (.7, 2.0), kettle (3.55, .35), lamp (3.6, 3.6), heater on the south wall, log shelf on the north wall. 13 of its 16 tiles are free. The overlook is now rows 1–6 with one bench.
        - **The old corner (cols 22–23, rows 8–10) is lobby** now, with a bench at lobby-local (7.0, 7.3) and the fourth coolant riser moved to (7.65, 9.65).
- **Deck 1's empty shell draws 593 calls.** Bring that down before dressing it, without changing the hull output on Decks 3, 4 and 5.
- **Plans:**
    - plans/deck6-plan.html and plans/deck1-plan.html are agreed.
    - plans/deck2-plan.html is agreed at Sketch 8 (approved by the lead for the user, 2026-10-15). It's 52 × 22 on Deck 3's outline, with the lift at [20, 11].
        - Aft of the lift: a looped carpeted senior corridor, and 15 bedrooms (12 crew plus 3 visitor rooms), each with its own door. The Captain's quarters across the stern are the biggest bedroom (60 tiles).
        - Forward of the lift: science, off a four-wide corridor. The sensor and comms array is a sealed room in the nose (106 tiles).
        - The lift's stern door opens to the quarters and its bow door to science.
        - Open, with defaults until the user says otherwise: the six invented officers are placeholders, and the 15th room is a visitors' cabin.

**7. The Living Ship (next big phase, agreed 2026-10-15).** Crew and simulation as one phase. It replaces the old step 7 (machines, supplies and the shared job list), which is now Pillar 2. The full design is in **design-doc.md** ("The living ship", "Crew simulation", "Social life", "Ship-wide events" and "Milestones"): no fail state, a 30-minute ship day, all 75 crew with varied routines, ship systems the crew tend, relationships and gossip, and ship-wide events as the main missions. Built in four pillars, each reviewed when it's done:
1. Foundation: clock, rota, the 75-crew roster, simulation of crew on other decks.
2. Ship systems and jobs.
3. Social.
4. Events, starting with the ion storm.


## Agreed ideas waiting for their milestone

- **You first arrive by shuttle** in the Deck 5 bay. The Tern is there with its ramp down, ready for it. Until the arrival is built, the game starts with you waking in Bunk 1. Still to decide: which milestone builds it, and who meets you off the shuttle.
- **Hygiene is a fourth need,** and showers restore it (milestone 2).
- **Uniforms get grubby.** You drop yours at the laundry and take a clean one from your locker. A water recycler fault on Deck 3 means weak showers on Deck 4.
- **Hover hand carts** carry supplies from Deck 5's cargo hold up the main lift to Deck 3's cold store and wherever else they're needed. A job for step 7; the carts charge in Deck 5's Cart bay.
- **Shifts will move crew between decks.** Pell then sleeps in Bunk 2 and works on Deck 5.


## Open questions

They're all in one place now: the "Open questions" section at the end of design-doc.md.


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

The character spec, uniforms and badges are unchanged; see section 8 and design-doc.md ("Setting & names").

Other files: design-doc.md (the design, the source of truth), plans/ (deck plans), TEAM.md (who's working on what), cadet_test.py and deck_check.py (tests), archive/design-doc-v4.pdf (the old design doc, for reference only).
