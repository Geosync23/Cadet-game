# Optimization pass: measurements (OP1, the planner)

Measured on **0.64.7** (`claude/integration` 6ea5acf), 2026-10-21, in a Claude Code cloud container (4 cores, 15 GB, Chromium with SwiftShader software rendering, the checks' own launch flags). Scripts are in `plans/opt-probes/`. Times are from this container's CPU; a mid-range phone runs game code roughly 4 to 5 times slower (plans/perf-p4-plan.md), and its GPU draws far faster than SwiftShader, so drawing and shader times here are **not** phone times.

## 1. Page load

### Wall time, a fresh page until the game is ready (`Game(...)` in cadet_test.py, 900×760, one browser alone, 3 runs each)

| Build | Open | Reload |
| --- | --- | --- |
| 0.64.4 (319f541) | 8.2 / 7.7 / 7.7 s | 8.1 / 7.6 / 7.9 s |
| 0.64.5 (75aa54a) | 7.4 / 6.9 / 7.4 s | 7.2 / 7.2 / 7.0 s |
| 0.64.7 (6ea5acf) | 7.6 / 7.5 / 7.4 s | 6.9 / 7.2 / 7.2 s |

The build didn't get slower to open between 0.64.4 and 0.64.5. The 14 s → 16-18 s seen in the test container came from other checks running at the same time (two or three browsers on four cores), not from the game.

### Where the 7 seconds go (0.64.7, phone portrait 390×844; real-time marks around the game's own script; `opt-probes/gl_split.py`)

| Phase | 390×844 | 900×760 |
| --- | --- | --- |
| HTML, three.js and parsing the game script, until it starts running | 0.30 s | 0.32 s |
| The game script at load: textures, shared kit, day plans, Deck 4 built | 3.14 s | 2.96 s |
| The first frame (`loop()` + `renderer.render`) | 3.49 s | 4.14 s |
| **Total** | **6.98 s** | **7.46 s** |

- **The first frame is almost all shader compiling** (software here): 2.75-3.04 s waiting in `getShaderInfoLog` (30 shaders) and 0.53-0.63 s in `getProgramInfoLog` (15 programs). Texture uploads (39) and buffer uploads take under 0.05 s. On a phone's GPU this part is far shorter, but each new kind of material still compiles once, the first time it's drawn (also after each deck change: TS1 saw the first `step(30)` after a deck change take 2-5 s here).
- **The game script at load** (CPU profile, `opt-probes/load_prof.py`; the profiler slows things ~15%):

| What | Time | Section |
| --- | --- | --- |
| `grain()`: random noise on every texture pixel (`R()` per pixel, keeps textures deterministic) | 1.00 s | 2 |
| `buildDeck` for Deck 4 (incl. `mergeMeshes` 0.29 s, `hullDist` 0.08 s, the shadow stand-ins list) | 1.32 s | 4b, 4c, 4a |
| The day's plans at load (`shipDay`, `schedBuild`, `nat`, `take`, `introLay`, ...) | about 0.44 s | 14 |
| The crowd's first packing (`crowdPack`, `rebuild`) | 0.06 s | 8b |
| Garbage collection | 0.27 s | |
| Dialogue data: `JSON.parse` of VOICE / LINES / TALKS, plus CONVOS and TRADITIONS literals | 0.08 s (measured in node: 41 + 15 + 8 + 12 + 5 ms) | 22 |

- **File:** 5.47 MB (51,407 lines), 1.63 MB gzipped. Section 22 (the dialogue, generated) is 2.05 MB of it (37.5%); next 4d (deck definitions) 0.44 MB, 20 0.24, 15 0.23, 17 0.22, 9 0.22, 18 0.20 MB. The dialogue blocks are already `JSON.parse` strings (perf-p4 item 4 is done), so parsing the file costs only ~0.3 s.

## 2. Draw calls, triangles, memory (perf_check.py on 0.64.7, 7 min 27 s)

| Scene | portrait 1.5 | portrait wide 0.7 | landscape 1.15 | crew |
| --- | --- | --- | --- | --- |
| arrival: shuttle bay 17:40 | 180 calls / 280 GPU draws, 0.54 ms | 343 / 462, 0.47 ms | 149 / 235, 0.41 ms | 0 |
| arrival: Works bay door 17:46 | 156 / 243, 0.53 ms | 262 / 382, 0.67 ms | 156 / 222, 0.33 ms | 0 |
| Sunday dinner, mess 18:30 | 217 / 316, 1.92 ms | 351 / 505, 1.99 ms | 171 / 257, 1.72 ms | 72 |
| **junior common room, Sun 20:30** | 202 / 343, 0.62 ms | **433 / 617**, 0.95 ms | 186 / 281, 0.56 ms | 9 |
| Sowing morning, garden 10:00 | 218 / 359, 0.85 ms | 371 / 538, 1.73 ms | 208 / 316, 0.78 ms | 33 |
| Tiles night, bow lounge | 214 / 312, 1.63 ms | 345 / 498, 2.23 ms | 168 / 253, 1.41 ms | 53 |
| quiz night, bow lounge | 264 / 412, 1.73 ms | 396 / 599, 1.73 ms | 218 / 353, 1.44 ms | 61 |
| breakfast rush, mess 07:10 | 212 / 307, 1.04 ms | 343 / 493, 1.38 ms | 166 / 248, 0.63 ms | 22 |

("calls" = the picture, the 450 budget's number; "GPU draws" adds the shadow pass; ms = game code a frame, drawing skipped.)

- **But 6 of the 8 scenes measure the wrong room** (EV4's find, backlog 18b on claude/storm-update; confirmed here with `opt-probes/perf_room.py`). `SCENE_JS` passes the room's middle tile (column, row) to `nearestOpen(x, z, who)`, which wants world coordinates, so you stand wherever is nearest that point. Where you actually stand, and the numbers with the fix (`cellPos(i, j)` first), portrait 1.5 / portrait wide 0.7:

| Scene | Stands in now | Now | With the fix (the right room) |
| --- | --- | --- | --- |
| arrival: shuttle bay | Machine shop | 180 / 343 calls | Shuttle bay: 112 / 189 |
| arrival: Works bay door | Fan hall | 156 / 262 | Works bay: 173 / 279 |
| **Sunday dinner, mess** | Bow lounge | 217 / 351, 2.2 ms | **Mess hall: 261 / 418 calls, 2.0-3.0 ms, 69 people** |
| junior wing | Cabin 4-05 | 202 / 433 | Junior common room: 199 / 305 |
| Sowing morning, garden | Gym | 218 / 371 | Hydroponics garden: 189 / 286 |
| Tiles night, bow lounge | Bow lounge (right) | 214 / 345 | 260 / 345 (a different tile of the same room) |
| quiz night, bow lounge | Bow lounge (right) | 264 / 396 | 310 / 396 |
| **breakfast rush, mess** | Bow lounge | 212 / 343 | **Mess hall: 248 / 409** |

- **Headroom, corrected:** the busiest real scene is the mess hall at Sunday dinner zoomed out, **418 of 450**, then breakfast in the mess 409 and quiz night 396. The "433" was Cabin 4-05, not the junior common room (305). Every perf_check baseline since the scenes were added has measured these rooms; the build table's perf numbers should be read with that in mind.
- **Memory:** flat. Geometries/textures/JS heap 548/43/228 MB → 548/43/228 → 550/43/228 over deck round trips (the +2 is known since 0.64.6 and perf_check flags it); a week of play 548/43/228 → 550/43/228.
- **The JS heap: 95 MB after opening, 229 MB after visiting every deck once, then flat** (heap snapshots, `opt-probes/deck_heap.py`, `deck_heap2.py`; `performance.memory` doesn't update often enough to show the steps). Right after opening: 48 MB of raw arrays (mostly geometry kept on the CPU side after upload), 16.5 MB of object arrays, 11.5 MB of strings held outside the heap (the script's own text and the dialogue). After every deck: raw arrays 129 MB (+81), object arrays 56 MB (+40), the rest about the same. GPU geometries come back to 548 on Deck 4 every time, so the extra ~134 MB is kept on the JavaScript side for decks you've already left (or kit made on first visit), not leaked: it stops growing after one visit to each deck. perf-p4's "105-125 MB after load" (0.60.3) compares with the 95 MB after opening; perf_check's 228 MB is the after-every-deck number. What exactly holds the 134 MB needs a retainers walk (the load seat's turn 1).

### Deck changes (`goToDeck`, then the first drawn frame; phone portrait; `opt-probes/deck_heap.py`)

| Deck | 1 | 2 | 3 | 4 | 5 | 6 | 7 (rec) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Build, first visit | 360 ms | 904 | 1,058 | 824 | 384 | 207 | 445 |
| Build, second visit | 186 | 682 | 1,102 | 783 | 389 | 122 | 325 |
| First frame after it | 2.5-3.3 s | 0.6-1.0 | 2.6-3.0 | 3.0-3.5 | 3.0-3.5 | 2.8-2.9 | 1.7-1.9 |

The build is the game's own code (×4-5 on a phone: Deck 3 about 4-5 s). The first frame after a change is the software renderer uploading the new deck's geometry and compiling shaders, and costs as much on the second visit as on the first, so it's mostly uploads; a phone's GPU does that far faster.

### Test browsers keeping compiled shaders between launches (`opt-probes/shader_cache.py`)

A persistent browser profile (Chrome's GPU shader disk cache, with and without `--enable-gpu-shader-disk-cache`): open 10.3-11.2 s against 11.5 s with a fresh profile, a deck change and frame 2.2-2.9 s against 2.4-3.4 s (another check running alongside). Within the noise: SwiftShader doesn't reuse them. Not worth doing.

## 3. Game code a frame (CPU profile, `opt-probes/sim_prof.py`)

### Sunday dinner, standing in the mess hall, 69 people, 900 frames, drawing skipped: 2.59 ms a frame with the profiler on (`opt-probes/sim_prof_mess.py`; perf_check with item 0's fix: 1.95-3.04 ms)

| Part of the main loop (inclusive) | ms a frame | Section |
| --- | --- | --- |
| `crowd.update` (posing everyone on screen, chunks), which includes each person's `update` (1.04 ms: rig, activity) | 1.13 | 8b, 8 |
| `updateDeckCrew` (the scheduled crew on the deck) | 0.47 | 8c / 10 |
| walkers' `update` | 0.27 | 10 |
| `playerUpdate` | 0.17 | 15 |
| `writeWalls`, `shipFeelFrame`, `crewNearDoor`, `drawScreen`, `tickShip`, `doorLeavesSync` | 0.07, 0.06, 0.05, 0.04, 0.04, 0.03 | 4b, 8b, 8c, 2, 13, 4a |
| galley, events, social, lines, the day plan | 0.01-0.02 each | 16, 18, 20, 22, 14 |

Self time: three.js 22% (0.64 ms: the bones' matrices, 69 people × about 21 bones), 8b 19%, `(program)` 10%, the loop body 7%, 8 (`animateRig`) 6%, 8c 4%, 14 4% (`whereIs`, `walkGap`, `planWhere` asked every frame), 10 4%, 15 3%, **`getBoundingClientRect` 3% (0.095 ms a frame)**, 18 3%, GC 3%. Everyone is on screen in the mess, so everyone is posed every frame (0.27.27 poses only the people on screen; standing in the bow lounge, as the old scene did, cost 1.25 ms). **Layout reads every frame** (`getBoundingClientRect`, `matchMedia`; sections 11, 15, 19: the HUD placing itself) are cheap on a desktop but force the browser to lay the page out again on a phone when a style changed in the same frame.

(The first profile, standing in the bow lounge because of the scene bug, gave 1.25 ms a frame: crowd 0.47, deck crew 0.27, walkers 0.20.)

### Skipping 8 ship days on paper (`skipTo(1440 * 8)`): 1.4 s

Planning (14) 281 ms, machines (17) 225, events (18) 199, social stories (20c) 170 (`storyHour` alone 159), social (20) 125, galley (16) 115, Lightdisc (23b) 44.

### day_check's crew logic, Deck 3, one ship day: 30.9 s, of which **74% is GPU buffer uploads**

`bufferSubData` 17.4 s + `bufferData` 5.6 s, all inside the ~50 frames day_check draws (one by the lift and one over the crowd each ship hour). The crowd's chunk buffers (section 8b, 0.27.28's reuse) upload "from the lowest slot changed since the last draw to the end"; after a ship hour of skipped frames that's nearly the whole buffer: 2-15.6 MB per drawn frame, 269 MB over the day (`opt-probes/buf_prof.py`). The crew logic itself (`updateDeckCrew` 5.2 s, walkers 2.3 s, `findPath` 0.27 s) is the rest.

**In play** (Sunday dinner, every frame drawn, 600 frames; `opt-probes/buf_play.py`): 31 KB uploaded in a typical frame, but spikes up to 4.4 MB in one frame (a chunk rebuilt from an early slot). On a phone a multi-megabyte upload is a visible hitch; after a time skip (sleeping, a meal skip) the first frame uploads everything that changed meanwhile.

## 4. Each check's run time

(Two lanes side by side, each in its own CADET_WORK, as the build master runs them; a check alone is roughly 10-30% faster.)

| Check | Took | Result |
| --- | --- | --- |
| player | 36 min 39 s | PLAYER CHECK OK (the longest check) |
| intro | 11 min 09 s | OK |
| day1 | 7 min 46 s | DAY CHECK OK (one day; a release runs Days 0-8) |
| interactions | 7 min 35 s | INTERACTIONS CHECK OK |
| perf | 7 min 26 s | PERF CHECK: 1 problem (the known +2 geometries) |
| mech | 5 min 10 s | MECH CHECK OK |
| events | 5 min 02 s | EVENTS CHECK OK |
| bubble | 4 min 49 s | BUBBLE CHECK OK |
| devmode | 4 min 13 s | DEVMODE CHECK OK |
| device | 4 min 01 s | device_check: OK |
| deck | 3 min 09 s | DECK CHECK OK |
| disc | 2 min 34 s | ALL OK |
| tiles | 2 min 25 s | ALL OK |
| join | 2 min 21 s | JOIN CHECK OK |
| cadet | 1 min 34 s | DIFFERENCES FOUND (vs 0.64.6: differences as the 0.64.7 release round explained (First Light Cocoa moves the crew)) |
| clothes | 1 min 25 s | ALL OK |
| path | 1 min 24 s | PATH CHECK OK |
| puzzle | 1 min 11 s | PUZZLE CHECK OK |
| food | 1 min 06 s | FOOD CHECK OK |
| career | 1 min 03 s | CAREER CHECK FAILED (known: backlog row 12) |
| machine | 0 min 52 s | MACHINE CHECK OK |
| social | 0 min 30 s | SOCIAL CHECK OK |
| talk | 0 min 28 s | TALK CHECK OK |
| leave | 0 min 26 s | LEAVE CHECK OK |
| arc | 0 min 22 s | ARC CHECK OK |
| lines | 0 min 04 s | lines_check: PASS (0 errors, 6 warnings) |
| **all of them, one after another** | **1 h 54 min** | |

- **check_fast alone: 270 s** (QUICK CHECK OK; deck 192 s, device 231 s, machine 53 s, leave 24 s), about the same as each inside the lanes, so two lanes cost little on this box. A third browser does: a page opened while two lanes ran took 11.5 s against 7.5 s alone.
- intro_check whole, alone: 11 min 09 s (BM11's reload fix took it from over 2 hours).
- **player_check is a third of the round** (36 min 39 s); day_check is 7 min 46 s for one day, and a release runs Days 0-8 (about an hour). Then interactions, perf, day, events, mech, bubble, devmode and device, 4-8 min each.
- Not timed here: bigevents_check (on the events branch), and the build master's smoke and newgame checks.

## 5. What this means

- **For the player:** opening the page costs about 3 s of game script on this machine (~10-14 s on a mid phone, by the 4-5× rule), a third of it painting texture noise; the busiest frames spend ~2 ms (8-10 ms on a phone) in game code before drawing; multi-megabyte crowd uploads make occasional hitches.
- **For the checks:** every page open costs ~7.5 s alone (about half shader compiling in software), more when lanes share the box; drawn frames after skipped ones pay for the crowd's catch-up uploads; and every turn runs all its checks whatever it touched.
