# 0.98 optimization plan: working notes (OP1, paused 2026-10-29 ~00:45 UTC, 8:45 PM ET Oct 28, on the lead's word)

**Plan page:** plans/opt-098-plan.html, published privately at https://claude.ai/artifact/N6veQ6xkcMh5WTg6E8rCJX (answers kept in its `answers/opt-098` store). Resumed and finished 2026-10-28 ~9:15 PM ET.

Scope (lead 44, the user's correction): **game speed on phones only** (loading, busy-scene frames, memory/battery, draw
calls). Test-speed work dropped, except a measuring method strong enough to prove the gains through the noise.
Also a turn in the plan: fix the two long-standing check failures (career_check "Relied on" before Day 5, backlog 12;
events_check's reading corner FX24-2).

Measured on claude/integration fe11cd66 (0.96.0), one browser, a quiet 4-core container. Probes in `plans/opt098-probes/`.

## So far

- **File:** 8.29 MB (75,756 lines), 2.45 MB gzipped (0.64.7: 5.47 / 1.63). Section 22 (dialogue) 3.07 MB = 37%;
  18 0.62, 4d 0.47, 15 0.28, 17 0.27, 20 0.25 MB (`sizes.py`).
- **Opening, 390x844** (`plans/opt-probes/gl_split.py`, 3 runs; the first run cold): 8.3 / 7.5 / 5.8 s wall.
  Script parse 0.37-0.78 s; the game script at load 1.9-2.9 s; the first frame 3.5-4.5 s, almost all shader compiling
  (getShaderInfoLog 3.0-3.4 s for 30 shaders, getProgramInfoLog 0.3-0.9 s for 15 programs: software here).
- **Load CPU profile** (`plans/opt-probes/load_prof.py`): grain 650 ms (its getImageData readbacks, as in 0.64.x),
  buildDeck 481 ms (mergeMeshes 94), the day's plans in section 14 ~0.35 s (nat, shipDay, take, schedBuild...),
  section 18 at load 156 ms self (eventPools, eventsOn, eventPlan), 17 45, 20 41. First frame: 200 calls, 273k tris,
  381 geometries, 32 textures, 15 programs, 1,994 objects, heap 109 MB.
- **Sunday dinner in the mess, portrait wide 0.7** (`frame_probe.py`): 418 calls, 523k tris, 67 people, 18 programs.
  Game code only (what perf_check measures): median 2.70 ms (10-90%: 2.04-3.67).
  **Drawn frame: game code 2.85 ms, renderer.render's own JavaScript 6.20 ms (5.6-9.7)**, then SwiftShader's drawing
  (~600 ms, not a phone number). So three.js's per-frame CPU work is about twice the game code and **perf_check
  never measures it** (it skips rendering). Profile of 300 drawn frames: three.js 5.17 ms a frame self, of which the
  main picture 3.49 and the shadow pass (sm.render, 4b) 0.91; 8b 0.58, 8 0.43, GC 0.34, 10 0.21, 14 0.17, 18 0.17.

## Leads to follow when resumed

1. **The render's CPU side** (biggest, not watched today): the shadow pass every frame (2048 map, PCFSoft, crew cast),
   ~420 objects culled/sorted/uniformed each frame. Ideas, all pixel-identical by construction: skip three's sort
   where order is fixed, matrixAutoUpdate off for more still things, fewer objects (merge more same-material
   statics), shadow casters culled earlier. Measure each with the A/B method below.
2. **Loading:** grain's readbacks. Idea: R() is a Lehmer generator, so the seed after a grain is
   seed * 16807^(pixels) mod (2^31-1): computable without the loop. So the pixel work can be deferred/batched (all
   canvases drawn first, then all read back; or textures not on the first deck grained later), same seeds, same pixels.
   Measure what batching saves. Also `renderer.debug.checkShaderErrors = false` (stops the forced sync after each
   compile; no pixel change) and the load-time plans in 14/18.
3. **Battery (questions for the user, they change smoothness or sharpness, not the game):** the loop draws at the
   screen's own rate (120 Hz phones draw twice as often); pixel ratio up to 2 with antialiasing and a 2048 soft shadow
   map. Options: a 60 fps cap; a "battery saver" setting (off = today's look).
4. **Memory:** re-run `plans/opt-probes/heap_tour.py` on 0.96.0 (RN1's #5 fix is in).
5. **Not yet measured:** the lantern supper, the Line supper, the Veyli engine lights, the Captain's address
   (`frame_probe.py BUILD 'lantern|Line supper|engine lights|address' wide`); deck-change times; memory tour.

## The measuring method (to prove gains through the noise)

Two pages (old and new) open in one browser, the same scene, batches alternated A B A B ... 15-20 times; report the
median of the paired differences and how many pairs went each way (a sign test), not two separate runs. Include the
drawn frame's render() JavaScript, not only game code. Pixel proof: cadet_test ALL IDENTICAL plus the scene shots.

## After the user's answers (28 Oct, ~10:45 PM ET)

- **Turn 1 dropped.** `opt098-probes/nodebug_proof.py` (OLD vs NEW, no ?debug, 10 alternating rounds): first picture
  2.95/2.98/2.90/3.23/3.05/3.14/3.03/3.24/2.89/3.18 s OLD vs 2.89/3.07/3.05/2.91/3.04/3.07/2.98/3.17/3.12/3.23 s NEW;
  6 of 10 pairs faster, median difference about 0.03 s: noise. The earlier 0.25-0.3 s (gl_split, 3 runs) always ran OLD
  first (backlog 32's order effect). three r128 reads each program's uniforms right after linking, which syncs anyway.
  Pixels after 60 frames identical.
- **Turn 2 parked.** In the mess, every still mesh casting its own shadow is either noMerge (moves or changes) or added
  after the build (event decor, frozen): about 10 safe draws, ~0.1 ms, against rebuilding stand-ins when decor changes.
- **Turn 6 widened** (the user's backlog list): FX24-2 + FX12-1 + TQ1-1 share the planner's walk estimate (walkLead,
  WALK_DETOUR 1.6; the commute minutes C). First step: measure planned vs real arrivals (lift to room at evening
  gatherings; same-deck moves; toilets), then one calibrated change. A first narrow FX24-2 draft (take()'s `longLead`,
  `tradWalkMin()` = 10, the generic tradition take in leisureUntil) is kept aside, not committed.
- SD3-2 proposed to SD3 (section 27's owner).
