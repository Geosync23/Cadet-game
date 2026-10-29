# Where things live: a map of the game file

Started by the ways-of-working engineer WW1 (2026-10-20). **Whoever moves code, or adds a section, updates this page in the same commit.** Owners of each section: `plans/owners.md`.

## Finding your way in a minute

- `python3 tools/section.py`: every section with its first and last line and size.
- `python3 tools/section.py 19` (or `DEVICE`, a word of its heading): print a section with game line numbers. `--head 40` for its first 40 lines.
- **A line number to a section:** `python3 tools/section.py --where 23456`. Use it on browser errors (`starship-cadet.html:23456`), grep hits and old notes that say "around line N". Line numbers drift with every build; section ids don't.
- **Which sections a change touches, and whose they are:** `python3 tools/section.py --diff A B` (for a branch: `--diff $(git merge-base origin/claude/integration HEAD) HEAD`).
- **Who uses a function or table outside its section:** `node tools/shared.js --min 1 | grep -A1 ' NAME '`.
- Plain grep still works: `grep -n "^function NAME\|^const NAME\|^let NAME" starship-cadet.html`.

**The file's order is not the sections' number order.** Sections were added where they had to load (a section must come after what it reads at load). Today's order: page, 1, 2, 3, 4 (4a-4e), 5, **13, 14, 19, 15, 15b, 15r, 16, 17, 22, 18, 20, 20c, 21, 21b, 23, 23b, 24 (24a ... 24p, then 24u-24x), 28 (28a-28f)**, 6, 7, 8, 8b, 9, 10, 8c, 11, 25, 26, 27, 29 (29a-29c), 30, 12. A section heading is a column-0 line `// 19. DEVICE` or `// 24a ROUNDS`, between two `// ====` or `// ----` rule lines.

## Each seat's slot (from step 2)

One labelled, empty block per seat at the end of its main section, where that seat adds new top-level code (just above the end line), so two seats never add lines at the same spot. Find yours with `grep -n "slot: <seat>" starship-cadet.html`. Added with `tools/add_slots.py` (comment lines only; the game is unchanged).

| Seat | At the end of section |
|---|---|
| Deck architect | 4d |
| Rec engineer | 4e |
| Sim engineer | 14 |
| Device engineer | 19 |
| Player engineer | 15 |
| Interactions engineer | 15b |
| Galley engineer | 16 |
| Systems engineer | 17 |
| Dialogue engineer | 22 |
| Traditions engineer | 18 |
| Events engineer 2 | 18 (its slot is right after the Traditions engineer's) |
| Social engineer | 20c |
| Onboarding engineer | 21b |
| Games engineer | 23b |
| Puzzles seat | 24k |
| Works career engineer | 24p |
| Later promotions (Works career engineer, Pillar 5 Steps 5-6) | 24u |
| Power and relays (mechanics seat A, M19) | 24v |
| Shutdowns (mechanics seat B, M18) | 24w |
| Sensor array (mechanics seat A, M20) | 24x |
| Engine Specialist (Works career engineer, Pillar 5 Step 6's shared helpers) | 28 |
| Night shift (player engineer, M22) | 28a |
| Monday briefing (mechanics seat A, M21) | 28b |
| Engine work (mechanics seat B, M23) | 28c |
| Leading a team (mechanics seat A, M24) | 28d |
| Mentoring (Works career engineer, M25) | 28e |
| End of the career (Works career engineer) | 28f |
| Performance engineer | 8b |
| HUD seat | 11 |
| Fridays builder | 18f (its own section, after 18; the slot is at its end) |
| Comet builder | 18 (its slot is right after the Line builder's; FX25, 0.93.2) |
| Vessel builder | 18 (its slot is right after the Comet builder's; VB1 and VB2, A Veyli vessel needs help, `EV_VESSEL_ON`; VB2's V-5 code below the marker line near its end) |
| Storm Saturday (FX26, 0.93.2) | 18 (right after the Storm builder's slot) |
| Vessel sky (VB2, A Veyli vessel needs help V-5) | 18 (right after the Appointments builder's slot; VB1's 'Vessel builder' slot is after the Comet builder's) |
| Dev mode engineer | 25 (its own section, after 11; the slot is at its end) |
| Controller engineer | 26 (its own section, after 25; the slot is at its end) |
| Ending offer (the ending engineer) | 29a (section 29, after 27, before the main loop) |
| Ending goodbye (the ending engineer) | 29b |
| Endgame (the dialogue engineer, the Works career engineer) | 29c |
| Title screen (the title seat) | 30 |

No slot for the crew designer (section 9's roster is generated). A new feature (Dev mode, step 3) gets its own section and slot from its plan page; another slot for a seat: ask the lead.

## Where to look, by topic

| You want to change ... | Section | Start with |
|---|---|---|
| The page around the game: CSS, on-screen panels' HTML, the HUD build label | `page` | the `<style>` block, `#hud`; the build number is on two lines: the header's `build 0.64.2` line (`page`) and `GAME_BUILD` (`13`), set by the build master |
| Seeded random, colours, the renderer | `1` | `R()` (never at load for shared kit), `col()` (every colour) |
| Textures, materials, box/cylinder helpers | `2`, `3` | `tex`, `box`, `std`, `cyl`, `M` |
| The ship's state, deck names on screen | `4` | `SHIP`, `deckWord` (the rec deck is "R"), `deckIn`, `REC_DECK` (the rec deck's switch) |
| The deck in memory: rooms, edges, doors, hull, locks | `4a` | `roomAt`, `ROOMS`, `EDGES`, `YOU_LOCKS`, `youLock` |
| Furniture and room kit | `4b` | `KIT`, `place`, `placeWall`, `mergeMeshes` |
| Building and unloading a deck, the floor painter | `4c` | `buildDeck`, `unloadDeck` |
| A deck's map, rooms, dressing (Decks 1-6) | `4d` | `DECKS[n]`; the places for traditions, the Tern, Pillar 5 come after the decks |
| Step 6's Deck 6 machines and places (S6-4) | `4d` (Deck architect slot) | `DECK6_P5`, `deck6P5Places()` (called once from section 13 after the switches, `P5_DECK6`), `deck6P5Dress()` (the last line of `DECKS[6].dress`), `deck6WatchName()`, kit `coilPanel`, `reactorConsole`, wall kit `dosiRack`, `watchBoard`; ids `6-coil-1..3`, `6-reactor-1`, `6-coil-N-svc`, `6-reactor-1-svc`, `6-coil-team-1..3`, `6-dosi-rack`, `6-watch-board`; the rack `dosiOut()`, `dosiUse()`, `dosiTap`; Deck 2's suite as yours `deck2Mine()`, `deck2P5Places()` (`2-B-wardrobe`, `2-B-keepsake`, `2-B-rug/-desk/-shelf/-ledge`, `DECKS[2].wardrobes/homeKeepsakes/cabinSpots['2-B']`) |
| The rec deck's map and dressing | `4e` | `DECKS[7]`, `RK`, `REC_ROUTES` |
| Day and night light, mood lighting | `5` | `applyLight` |
| The clock, saving and loading, the notes bus, new game | `13` | `shipNow`, `SAVED`, `SAVE_EXTRA`, `saveGame`, `simNote` / `onSim`, `flag` / `flagSet`, `newGameStart`, `GAME_BUILD` |
| The crew's days: plans, places, meals, shifts, appointments, guests | `14` | `planDay`, `planWhere`, `schedU`, `playerShiftOn`, `schedPeople`, `apptList` |
| Your device: apps, skin, tips | `19` | `deviceApp(def)`, `deviceShow`, `tipShow`, `DEVICE_SKIN` |
| Your needs, activities, Mail, carrying, the job loop's player side | `15` | `ACT`, `actStart` / `actEnd`, `PLAYER_ACTS`, `mailSend`, `PAUSE` |
| Using what the crew use, the job board, the goal pointer | `15b` | `setGoal`, `clearGoal`, `ixTip` |
| The rec deck's activities (tap and do) | `15r` | |
| Galley, food, the garden's crops | `16` | `galleyServeMins`, `GARDEN_CROPS` |
| Machines, wear, faults, jobs, supplies, ship health, the lines (water, heat, air) | `17` | `machineById`, `machineList`, `jobKindAdd`, `JOB_KINDS`, `jobMake`, `jobFinish`, `MACHINE_LINKS`, `placesOf` |
| The crew's words (never by hand) and the dialogue engine | `22` | edit `content/`, run `python3 content_gen.py`; engine: `lineFor`, `LINES`, `VOICE` |
| Ship traditions, meetings, occasions, Mail the evening before, joining in | `18` | `SHIP_EVENTS`, `eventsOn`, `eventPlan`, `OCCASIONS`, `occasionAdd`, `eventMod` |
| Friendships, affinity, news, favours, chat cards, the crew seeking you out | `20` | `relAdd`, `relTier`, `newsAdd`, `memAdd`, `CHAT`, `socP` |
| Social stories (arcs, moments, keepsakes) | `20c` | |
| The arrival (Day 0-1, the escort, tea) | `21` | `introOn`, `introArrived`, `introSkip` |
| Clothes, the hamper, the washers | `21b` | `uniformState`, `hamperHeld` |
| Tiles; Lightdisc | `23`; `23b` | `SHIP.tiles`; `DISC` |
| Your Works career: the ladder, training, teachers, xp, tools | `24` | `WORK_MECH`, `CAREER_LADDER`, `worksText`, `worksDay`, `worksXp`, `worksTabAdd`, `toolWear` |
| A Works mechanic | `24a`-`24x` | rounds 24a, uniform 24b, drill 24c, hauling 24d, tuning 24e, incidents 24f, scanner 24g, team jobs 24h, tracing 24i, workshop 24j, cases 24k, favour cases 24l, tool upkeep 24m, logbook 24n, leak hunting 24o, the first promotion 24p, rewiring 24q, irrigation 24r, the lift roof 24s, off shift 24t; Pillar 5 Step 5 (S5-1, 2026-10-26): the later promotions 24u, power and relays 24v, shutdowns 24w, the sensor array 24x (in the file in this order: a-d, m, n, g, i, j, t, s, k, e, f, h, l, o, q, r, p, u, v, w, x; 24y and 24z free, Step 6 gets section 28) |
| Pillar 5 Step 6, the Engine Specialist | `28`-`28f` | shared helpers 28 (`P5_NIGHTS`, `P5_LEAVE`, `p5NightOf`, `p5NightAt`), the night shift 28a, the Monday briefing 28b, engine work and the reactor 28c, leading a team 28d, mentoring 28e, the end of the career 28f (W6's first turn, 2026-10-27; the promotion and the move are 24u's, the cases 24k's slot, the deck work 4d's) |
| The camera, zoom | `6` | |
| Walkable tiles, pathfinding, collision | `7` | `free`, `cellPos`, `findPath` (must match `findPathScan`: path_check) |
| Characters: bodies, uniforms, walking | `8` | `makeCharacter`, `L` |
| The crowd, poses, props, speech bubbles | `8b` | `poseOf`, `ACTS`, `bubbleSay` |
| The roster (made by `plans/crew-roster-gen.py`) | `9` | `ROSTER`, `ROSTER_PLAYER` |
| The crew moving on the deck | `10` | `DECK_CREW`, `placeSpot`, `PLACE_OF` |
| Rec deck moves, the auditorium's show | `8c` | `recMoveStep`, `recShow(state)` |
| Taps, toasts, the lift, the clock on screen | `11` | `tap`, `toast`, `goToDeck`, `updateClock` |
| The main loop: rides, doors, spins, cutaway, fades | `12` | |
| Dev mode: the hidden testing panel (`#dev`), its save, Undo, Mark, the Dev clock, Take me to | `25` | `DEVMODE` (13), `devmodeHold`, `devmodeRun`, `devmodeSkipTo`, `devmodeMove` |
| The ending: the offer, your answer, the goodbye, the end page, the endgame (`EV_ENDING_ON`) | `29` (29a-29c) | `SHIP.end`; the crossing back itself is section 18's |
| The title screen, the crew terminal (`TITLE_ON`) | `30`, and the page (`#title`, its first script `tiEarly`, the `#title` CSS after the bubbles) | `titleHold()` in 13's `freezeSync` and `saveGame`; `SND.title(on)` (27) |

## Outside the game file

- `content/`: the crew's words (the writers' guide is `content/README.md`); `content_gen.py` bakes them into section 22.
- Checks: one `*_check.py` per area (see CLAUDE.md "Files" and DEV_NOTES "Testing"), `cadet_test.py` (two builds compared), `names_check.js` (names, keys, registrations, "Deck 7"), `check_fast.sh` (the quick check), `.github/workflows/quick-check.yml` (the GitHub check: check_fast on every push to a claude/ branch or main).
- `tools/`: `section.py`, `shared.js` (this map's helpers), `add_slots.py` (the seats' slots); `resolve.py`, `fixrate.py` (old build-number clash helpers); `kitdup.py`, probes.
- `plans/`: deck plans, pillar plans, `handover-<role>.md` notes, `owners.md`, `map.md`, `backlog.md`, `roadmap-after-recdeck.md`.
