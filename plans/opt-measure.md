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

## 5. After the review (ER2, round 1)

### Shaders within one run (`opt-probes/compile_probe.py`, `keep_probe.py`; phone portrait; another check not running)

- **`renderer.compile(scene, camera)` right after `goToDeck`:** the first frame falls to 37-144 ms (from 0.9-3.7 s), but the compile itself takes 0.7-2.4 s, so the total is the same; it compiles one extra program per deck (things not yet drawn). It moves the wait, it doesn't remove it.
- **Keeping every compiled program** (one extra `usedTimes` on each WebGLProgram once it exists, so three r128 never deletes it when a deck's materials are disposed): 22 programs after one lap, then no more. First frames after each change over a second lap of all seven decks: **6.3 s, against 9.2 s** without (Decks 5, 1, 6 and 7 at 10-30 ms instead of 0.5-2 s; Decks 3, 2 and 4 still 1.5-2.9 s, so their first frame is something else: uploads, the crowd or shadows).

### Affected checks, a lower bound (`opt-probes/affected_estimate.py`)

The last 20 non-merge commits that changed the game on `claude/integration`, mapped section by section through the DEV_NOTES "run it whenever" rules (condensed in the script), with check_fast's own four on top and this file's check times: **4.2 checks and 28 minutes a turn on average**, against 22 checks and 106 minutes for all of them. One turn (0.64.7's, sections 13 and page) runs everything; a turn touching section 15 costs about 45 minutes because of player_check. The map from real runs (coverage) can only add checks, so this is the least. Whether those picks would have caught every real failure isn't measured here: it needs the build table's failures per merge, which is turn 1's replay.

## 6. What this means

- **For the player:** opening the page costs about 3 s of game script on this machine (~10-14 s on a mid phone, by the 4-5× rule), a third of it painting texture noise; the busiest frames spend ~2 ms (8-10 ms on a phone) in game code before drawing; multi-megabyte crowd uploads make occasional hitches.
- **For the checks:** every page open costs ~7.5 s alone (about half shader compiling in software), more when lanes share the box; drawn frames after skipped ones pay for the crowd's catch-up uploads; and every turn runs all its checks whatever it touched.

## 5. Turn 1, the render seat (RN1, 2026-10-21, on 0.64.8)

### Crowd uploads (#3): parked

- **The byte counts in section 3 above were too high.** `buf_prof.py` and `buf_play.py` added `d.byteLength` for each `bufferSubData` call, but three r128 on WebGL2 calls `bufferSubData(target, offset, array, srcOffset, count)`: the whole array is passed, only `count` is sent. Counted right (`opt-probes/buf_true.py`, `buf_play_true.py`):
  - day_check, Deck 3, Day 1 (drawn frames only): 115 MB over the day, not 269; at most 8.4 MB in one frame (17:49, over the crowd), not 15.6.
  - Sunday dinner, standing in the mess hall (70 people, 390×844, 600 drawn frames): 36.4 MB in all, median 31 KB a frame, p95 31 KB, max 1.69 MB (not 4.4).
- **The time wasn't uploads either.** Here `gl.finish()` returns at once, so the software renderer's queued drawing is billed to the next call that has to wait for the GPU process. With a real wait after each drawn frame (`gl.readPixels` of one pixel, ~600-900 ms a frame on Deck 3), the day's `bufferSubData` calls take **30 ms** in all and `bufferData` 0.3 s, against 15.6 s and 11 s without the wait. In isolation, 20 uploads of 4 MB take 15 ms. So day_check's ~31 s on Deck 3 is drawing about 50 frames, and nothing in the crowd's uploads can shorten it.
- **Any timing of a single frame needs that wait** (a first frame after a deck change, a shader compile): otherwise the drawing lands in whichever frame syncs next.
- Parked by lead 23 (plan item 3): fixed slots would change section 8b's buffer layout to save about a millisecond in a rare frame on a phone.

### Shaders kept across deck changes (#4): built

- **The plan's 9.2 → 6.3 s was partly drawing time.** `keep_probe.py` timed the first frame without a wait, so a kept program (no compile, so no sync) left its drawing to be billed to a later frame. With a real wait after each frame (`opt-probes/keep_true.py`, 390×844, three laps of decks 3, 5, 2, 1, 6, 7, 4):

| | lap 1 | lap 2 | lap 3 |
| --- | --- | --- | --- |
| plain: first frames after the 7 changes | 13.9 s | 12.4 s | 11.1 s |
| kept | 11.8 s | 10.9 s | 10.6 s |

- Plain keeps 16-18 programs alive and rebuilds the ones its unload deleted on every change (2-5 a change); kept, they stop at **22** after the first lap at 390×844 and at 844×390 (`opt-probes/keep_shots.py`). The rest of the first frame here is SwiftShader uploading and drawing the new deck. On a phone each saved compile is the part that costs (tens to hundreds of ms of hitch on arrival); uploads are far faster there.
- Proof: cadet_test ALL IDENTICAL; every deck's third-lap shot identical at both sizes; memory after each lap the same as before.

### The trifold's sizes (the user's phone: Samsung Galaxy Z TriFold)

- **Published (the panels):** cover screen 6.5", 1080 × 2520 px, 21:9 (Wikipedia, "Samsung Galaxy Z TriFold"; SamMobile's pre-launch report said 1080 × 2560); inner screen 10", 1584 × 2160 px, about 269 ppi (Samsung's developer emulator page, SamMobile, 91mobiles).
- **Not published: its browser size.** No device database lists the TriFold's CSS viewport or pixel ratio (searched 2026-10-21). perf_check's `TRIFOLD` sizes are **derived** from Samsung's foldable defaults (Galaxy Z Fold7: cover 2.625 device px per CSS px, inner 2.0): **folded 412 × 960** (960 × 412 turned), **open 792 × 1080** (1080 × 792 turned). The browser's own bars take some height off. The Dev Speed card (#8) should show `innerWidth × innerHeight` and `devicePixelRatio`, so the user's phone can confirm them; then change the one `TRIFOLD` table in perf_check.py.
- Sources: https://en.wikipedia.org/wiki/Samsung_Galaxy_Z_TriFold, https://www.sammobile.com/news/samsung-galaxy-z-trifold-display-specs-features/, https://developer.samsung.com/galaxy-emulator-skin/galaxy-z.html, https://www.91mobiles.com/samsung-galaxy-z-trifold-price-in-india?ty=specs

### The busy event scenes, switched on (perf_check's new scenes; RN1, 2026-10-21)

Measured on local merges, not pushed: claude/opt-render (0.64.8 + #4 + TS2's room fix) with claude/storm-update, claude/fridays and claude/patch-crew (T1: the first rotation on Day 21); the Line scenes on claude/line-update as it stands (be75d10), because its game code clashes in five places with the newer storm update (for the build master and the Line builder). Draw calls in the picture (the 450 budget) / every GPU draw with shadows; people on the deck. Every view is in the scene's own room.

| Scene (switches) | portrait 1.5 | portrait wide 0.7 | landscape 1.15 | TriFold folded / turned | TriFold open / turned | game code ms | people |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Captain's address, auditorium Fri 16:10 (SHORT_FRIDAY) | 174 | 209 | 171 | 174 / 172 | 167 / 157 | 1.2-2.0 | 49 |
| after the address, rec lift lobby 16:52 (SHORT_FRIDAY) | 204 | 274 | 232 | 208 / 236 | 192 / 199 | 0.6-1.3 | 15 |
| Friday dinner, the mess 17:20 (SHORT_FRIDAY) | 203 | 361 | 237 | 210 / 253 | 187 / 176 | 1.3-2.2 | 49 |
| lantern supper, the mess Sat 18:30 (EVENTS_ON) | 260 | **417** | 293 | 267 / 309 | 244 / 233 | 1.5-2.7 | 62 |
| storm all-clear party, bow lounge Sun 19:30 (EVENTS_ON) | 271 | 363 | 252 | 277 / 258 | 244 / 234 | 1.4-2.2 | 63 |
| the Line ceremony, bow lounge Sun 14:45 (EVENTS_ON, EV_LINE_ON) | 309 | 396 | 285 | 312 / 286 | 270 / 263 | 1.2-1.6 | 57 |
| the Line supper, the mess Sun 18:30 (EVENTS_ON, EV_LINE_ON) | 262 | **419** | 294 | 269 / 310 | 246 / 234 | 1.6-2.0 | 70 |
| first new crew off the Tern, shuttle bay Sun 17:40 (patch-crew T1; the Tern moment T2 not in yet) | 113 | 191 | 138 | 113 / 145 | 104 / 106 | 0.4-0.7 | 1 |

- **All under 450.** The busiest are the two suppers in the mess zoomed out: the Line supper 419 (31 to spare), the lantern supper 417. That's the mess hall headroom of item 13 (Sunday dinner 418): the user's answer to question 7 is to watch it and act only when something new goes in there. The Line supper is becoming seated sittings (EV7); re-measure then.
- **The TriFold** (sizes derived, see above): folded it draws about what a phone in portrait does; open, a little less (the camera's view takes in the same room). Turned (landscape) folded is the heaviest TriFold view: 309-310 in the suppers.
- Game code a frame stays 1.2-2.7 ms here in every event scene (Sunday dinner 2.0-3.0).
- **Day 21:** with only T1, the scene measures an empty shuttle bay at 17:40 (just you). The row stays as is: with T2 (the Tern moment) it measures the arrival itself; on a build without a Day 21 rotation it prints WAITING.

### Faster deck builds (#10): built

- Profile of building Decks 3, 2 and 4 (`opt-probes/build_prof.py`, three builds each, with Deck 5 between): `mergeMeshes` about 40% (its traverse pushing into plain arrays, `toNonIndexed` and `applyMatrix4` through getX/setXYZ), `tallCombine` 10%, `hullDist` 7% (every tile and wall end measured to every hull segment), the floor painter, three's own shape constructors.
- After: `mergeMeshes` counts then fills exact typed arrays with three's sums done inline; `tallCombine` copies whole arrays; `hullBeyond` skips far segments. Best of 5 builds (`opt-probes/merge_bytes.py`):

| Deck | 1 | 2 | 3 | 4 | 5 | 6 | rec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| before (ms) | 103 | 486 | 599 | 451 | 278 | 88 | 266 |
| after | 47 | 264 | 346 | 270 | 160 | 47 | 191 |

- Every mesh's bytes, the standing tiles, the map, the trimmed walls, the tall pieces and the seed are identical on all seven decks; cadet_test ALL IDENTICAL.
- What's left in a build: three's BoxGeometry/CylinderGeometry making Float32BufferAttributes from plain arrays for each furniture piece (~15%; caching shapes would mean changing the kit), the floor painter (canvas and grain: #6), `place` and the decks' `dress`.

### Faster texture painting (#6): the grain loop built; the rest parked

- **Where the "1.0 s of grain" goes** (`opt-probes/grain_load.py`, `grain_split.py`, at load, 390×844): 17 `grain()` calls on 1.05 M pixels, 700-750 ms in all, of which **`getImageData` 735 ms** and the loop 26 ms (`putImageData` ~0). Reading a canvas back makes the browser finish drawing it on the graphics chip and copy it back (the first call 144 ms, then 12-53 ms each). A phone's browser does the same readback.
- **Built:** the loop with `R()` inlined on a local seed and an exact modulus (x mod (2³¹−1) = (x mod 2³¹) + ⌊x / 2³¹⌋, less m if that reaches m; 50 M steps checked equal in node). Warm, 1.9× the old loop at 4096×2048 (`grain_bench.py`); at load, all 17 calls' pixels and the seed after them are identical to the old build. It saves about 25 ms here, because the loop was never the cost.
- **Parked (the user's answer, 2026-10-21: don't change the look of the game):** drawing the texture canvases on the CPU (`getContext('2d', { willReadFrequently: true })`) removes the readback: page open 6.5 → 4.7 s here, grain 762 → 32 ms (`opt-probes/wrf.py`). But 101 of the 106 textures at load come out with different pixels (CPU and GPU draw gradients and edges differently), so it changes the look. Not built; kept here on record. Nothing else can remove the readback with the pixels kept: the grain needs the drawn pixels.

### Lighter busy frames (#7): measured, proposed to park (RN1)

Sunday dinner in the mess hall, 69 people, 900 frames, drawing skipped, profiler on (`opt-probes/prof_mess2.py`): 2.37 ms a frame.
- The crowd's posing (`crowd.update` → each person's `update`) 1.2 ms. three.js inside it: `updateMatrixWorld` 0.29 ms, `multiplyMatrices` 0.07, `setFromEuler` 0.13 (rig, activity, legs, arms). A rig is 21 objects, 20 of them bones the skinning uses (`opt-probes/rigcount.py`): nothing to skip. Everyone is on screen in the mess, so posing only those in view (0.27.27) already applies.
- `updateDeckCrew` 0.47, the walkers 0.28, `playerUpdate` 0.14; `whereIs` + `planWhere` + `walkGap` 0.09 together.
- HUD layout reads (`opt-probes/layout_reads.py`, 390×844 and 844×390): about 3 a frame on average, already spread over frames (`trkPlace`, `hudFit`, `hits`, the button-overlap checks), plus one `matchMedia` a frame (`floatsTick`); `getBoundingClientRect` 0.05 ms a frame in all.
- So the plan's three pieces could save at most ~0.15-0.2 ms (about 7%), across four or five owners' sections and with caches bound by the planner rule. A phone runs this frame's game code in roughly 10-12 ms of the 16.7 ms a smooth frame allows.

### The memory walk (#5): measured; one fix proposed (RN1)

- **After a real garbage collection** (CDP `Runtime.getHeapUsage`, `opt-probes/heap_tour.py`): the JavaScript heap itself is 21.5 MB after load and 30-36 MB after a tour of every deck; the plan's 95 → 229 MB was `performance.memory`, which counts garbage not yet collected. What grows is the **array storage** (shapes' number arrays, outside the heap): on Deck 4, 56.8 MB after load, **134.6 MB after one tour, the same after a second**.
- **Who holds it** (two heap snapshots of one page, each array buffer's shortest path from the roots, summed by the game variable it hangs from; `opt-probes/heap_walk2.py`), after load → after the tour:

| Held by (section) | MB |
| --- | --- |
| `BENCH_BAR` (4b: the gym bench's bar) | 0 → 35.3 |
| `EV_DECOR` (18: the day's decorations) | 0 → 20.0 |
| `TERN` (4d: the shuttle's ramp) | 0 → 7.2 |
| `CROWD_KEPT` (8b: bodies kept for coming back, by design) | 0.3 → 5.7 |
| `REC_SIGNS` (17), `REC_SHOW` (4e) | 0 → 4.2 each |
| `DRILL_EXT` (4d: the drill's extinguisher) | 0 → 2.4 |

  Each is a small handle to one object on a deck (a bar, a group, a hinge, an extinguisher, or the deck's root itself). Through `.parent` links, the handle keeps **that whole unloaded deck's tree, shapes and all**, until its own deck is built again. That's why it stops growing after one tour.
- **Option B, tried in a scratch copy only** (`opt-probes/detach_test.py`): `unloadDeck` (4c) also takes the old deck's tree apart (each object's `parent` = null, `children` = []), so a stale handle holds only itself. Two tours, then Deck 4: array storage **134.6 → 61.3 MB**, heap 36.3 → 25.1 MB. No object of an unloaded deck ever comes back into a scene. No errors.
- **The risk:** code that reads a stale handle's `.parent` after a deck change. There are 15 `.parent` reads in the game; they all allow for a missing parent, or run only on their own deck (`galleyShow` rebuilds `GV` when `deckRoot` changes, `recShowTick` only on the rec deck, `recPoolsSet` returns early either way).
