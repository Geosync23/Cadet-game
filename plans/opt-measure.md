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

- **Headroom:** the junior common room zoomed out is at 433 of 450. Quiz night zoomed out 396.
- **Memory:** flat. Geometries/textures/JS heap 548/43/228 MB → 548/43/228 → 550/43/228 over deck round trips (the +2 is known since 0.64.6 and perf_check flags it); a week of play 548/43/228 → 550/43/228.
- **The JS heap is 228 MB after a forced collection.** perf-p4 measured about 105-125 MB at 0.60.3 and 141-150 MB at 0.27.25. What fills it hasn't been broken down yet (a heap snapshot is turn 1's job, see the plan).

## 3. Game code a frame (CPU profile, `opt-probes/sim_prof.py`)

### Sunday dinner, the mess, 72 people, 900 frames, drawing skipped: 1.25 ms a frame with the profiler on (perf_check: 1.72-1.99 ms)

| Part of the main loop (inclusive) | ms a frame | Section |
| --- | --- | --- |
| crowd: `crowd.update` (posing, chunks) | 0.47 | 8b |
| crowd: the people's own `update` (rig, activity) | 0.39 | 8b |
| `updateDeckCrew` (the scheduled crew on the deck) | 0.27 | 8c / 10 |
| walkers' `update` | 0.20 | 10 |
| `playerUpdate` | 0.09 | 15 |
| `writeWalls`, `doorLeavesSync`, `drawScreen`, `tickShip` | 0.05, 0.04, 0.03, 0.03 | 4b, 4a, 2, 13 |
| galley, events, social, lines, intro ticks | 0.01 each or less | 16, 18, 20, 22, 21 |

Self time: `(program)` (V8 internals, inline-cache misses) 22%, three.js 17% (matrix updates), 8b 14%, the loop body 6%, 10 6%, 14 5% (`whereIs`, `walkGap`, `planWhere` asked every frame), 8c 4%, 8 3%. **Layout reads every frame:** `getBoundingClientRect` 0.042 ms and `matchMedia` 0.012 ms a frame (sections 11, 15, 19: the HUD placing itself); cheap on a desktop, but a forced layout on a phone when a style changed in the same frame.

### Skipping 8 ship days on paper (`skipTo(1440 * 8)`): 1.4 s

Planning (14) 281 ms, machines (17) 225, events (18) 199, social stories (20c) 170 (`storyHour` alone 159), social (20) 125, galley (16) 115, Lightdisc (23b) 44.

### day_check's crew logic, Deck 3, one ship day: 30.9 s, of which **74% is GPU buffer uploads**

`bufferSubData` 17.4 s + `bufferData` 5.6 s, all inside the ~50 frames day_check draws (one by the lift and one over the crowd each ship hour). The crowd's chunk buffers (section 8b, 0.27.28's reuse) upload "from the lowest slot changed since the last draw to the end"; after a ship hour of skipped frames that's nearly the whole buffer: 2-15.6 MB per drawn frame, 269 MB over the day (`opt-probes/buf_prof.py`). The crew logic itself (`updateDeckCrew` 5.2 s, walkers 2.3 s, `findPath` 0.27 s) is the rest.

**In play** (Sunday dinner, every frame drawn, 600 frames; `opt-probes/buf_play.py`): 31 KB uploaded in a typical frame, but spikes up to 4.4 MB in one frame (a chunk rebuilt from an early slot). On a phone a multi-megabyte upload is a visible hitch; after a time skip (sleeping, a meal skip) the first frame uploads everything that changed meanwhile.

## 4. Each check's run time

(Two lanes side by side, each in its own CADET_WORK, as the build master runs them; a check alone is roughly 10-30% faster.)

TABLE_CHECKS

## 5. What this means

- **For the player:** opening the page costs about 3 s of game script on this machine (~10-14 s on a mid phone, by the 4-5× rule), a third of it painting texture noise; the busiest frames spend ~2 ms (8-10 ms on a phone) in game code before drawing; multi-megabyte crowd uploads make occasional hitches.
- **For the checks:** every page open costs ~7.5 s alone (about half shader compiling in software), more when lanes share the box; drawn frames after skipped ones pay for the crowd's catch-up uploads; and every turn runs all its checks whatever it touched.
