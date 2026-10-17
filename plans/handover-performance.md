# Handover: performance engineer (crowd rendering and activity poses)

Written at 0.40.8 (merged up to claude/ship-integration 980e6a9), brought up to date at 0.27.18 (on ship-integration d89a3f5 / 0.41.7) and again at 0.27.22, 0.27.27 and 0.27.32 by the second performance engineer (session_01XAkY9U3mmstHQT2yAMTocA; claude/crowd-render abe6d2b, on ship-integration 0.60.2 / 142b503). Plain notes for whoever picks this area up.

## Performance engineer 3 (session started 2026-10-17, reports to lead session_01KPJMYjXAPkNUcrQ8VRkhLE)
- **0.27.33 done** (73b8998): stand-ins built a slice a frame (`shadowStep`, `SHADOW_JOB`, `SHADOW_STEP`); see its DEV_NOTES row. Sent to reviewer 2b. Scratchpad probes (not committed): sseq.py (stand-ins bit-for-bit vs an old build), ssi2.py (per-slice timing using `Performance.prototype.now.call(performance)`, since the test harness fakes `performance.now`), shots.py (54 shots, all decks, mid-build and done), midb.py (leave a deck mid-build, memory flat).
- **Waiting:** build master 2's final 0.60.3, then the phone-like measurement against 0.60.2.

## Read first: state at handover (2026-10-17 ~13:40, the second performance engineer)
- **Branch:** `claude/crowd-render`. The last build is 0.27.32 (abe6d2b); handover notes are on top of it. All of 0.27.25–0.27.32 passed review by reviewer 2b (session_01F93LiFWtciyCLNV34qPsjP; notes in plans/reviews/ on claude/reviews-2). None of them are in the 0.60.3 candidate (claude/cand-0603 f0f8a7c). I recommended merging abe6d2b into 0.60.4; the only conflicts are the two build lines.
- **First job for the next performance session: 0.27.33, stand-ins built over a few frames on a deck change** (the plan is below, under Slow frames, "Next job"). The lead approved it on 2026-10-17. The picture must be identical at every moment.
- **0.60.3 candidate 2, measured** (CPU slowed 4×, an hour in the mess, game code only, two runs). Figures are 0.60.2 → 0.60.3 → 0.60.3 + crowd-render:
  - Sunday dinner, average frame: 6.5–6.8 → 6.8–7.2 → 4.5–4.9 ms.
  - Sunday dinner, frames over 16.7 ms an hour: 51–62 → 44–60 → 10–12.
  - Sunday dinner, frames over 33 ms an hour: 6–13 → 9 → 1–2.
  - Breakfast, average frame: 4.1 → 5.2–5.4 (45 crew, against 26) → 3.0–3.2 ms.
  - Breakfast, frames over 16.7 ms an hour: 18–20 → 43–48 → 4–6.
  - Load at 4×: about 11.5–12 s for all three. perf_check: PASS; the file grows 2.96 → 3.29 MB.
  - Sent to the lead and to build master 2 (session_01F8ph7FKqViF3heRn94YgBr).
- **Waiting on others:** section 10/14 garbage (`crewNearDoor`, `whereIs`/`shipDay`) is with sim engineer 4, now handing over, for after 0.60.4. Re-measure it with alloc.py's method (below) when their successor asks.
- **Watchdog role:** continue it. For each combined build, run perf_check NEW OLD, plus the phone-like runs if the lead wants numbers for the user.

## Role, branch, builds
- **Role:** making many crew cheap to draw (Pillar 1, workstream 5) and giving them activity poses and props (Pillar 2, A2). I also cut Deck 6's draw calls.
- **Branch:** `claude/crowd-render`. Lead merges it into `claude/ship-integration`.
- **Build numbers:** 0.20.x (crowd), 0.27.x (activities and Pillar 3 pieces, last was 0.27.32; next is 0.27.33). Bump the header build line and `GAME_BUILD` together, and add a row to the DEV_NOTES build table.
- **Owned in `starship-cadet.html`:** `// 8. CHARACTER KIT` and `// 8b. CROWD`, plus `// 7. GRID` (findPath) since 0.27.29 and `// 12. MAIN LOOP` since 0.27.31, both by the lead's decision (the picture must stay identical). Plus the one NOSAVE line in section 13 (see the demos below).
- **Owned in DEV_NOTES:** the rows for 0.20.x and 0.27.x, and the sections "Crowd rendering (0.20.x)" and "Activities (0.27.x)". Those sections give the detail. This page is the short version.
- **Test scripts:** I own `perf_check.py` (the phone-speed watchdog, below) and `path_check.py` (findPath against findPathScan). I also use `cadet_test.py`, `deck_check.py`, `day_check.py`, `events_check.py` and `player_check.py`.

## What I built, and what other sections rely on
**Crowd (8b).** Each crew member is a `makeCharacter` rig built at lower detail (`CROWD_DETAIL`). Each joint's parts are packed into one piece of geometry (`crowdPack`). Up to `CROWD_PER` people (12, or fewer on GPUs without float vertex textures) share one `THREE.SkinnedMesh` (`CrowdChunk`), with each joint as a bone. So 40 crew cost about 3 draw calls, and 70 cost about 6. The real cost is triangles. There are two levels of detail: people further than `CROWD_FAR` (9 m, scaled by `CROWD_FAR_ZOOM`) use the coarser mesh.
- `crowd.add(spec)` takes the same spec as `makeCharacter` and returns a handle (a `CrowdPerson`). Pose it each frame with `h.set(pos, face, pose, walkPhase)`, as section 10's agents do.
- `crowd.remove(h)`, `crowd.clear()`, `crowd.near(x, z, r)` (who's at a spot, for taps), `crowd.update(dt, t)` (once a frame), and `crowd.stats()`, which returns `{people, chunks, perChunk, verts, tris, far}`.
- `FullPerson` (section 10) borrows `CrowdPerson.prototype.set/update` for the full-detail person you're talking to. Don't change those two methods without checking it.

**Poses (8b).** A pose is a string:
- `base`: walk, stand, sit, lie or work.
- Or an activity from `ACTS`: row, run, lift, call, browse, pay, play, water, cook, wash, fold, drink, read, talk.
- Or a composite `'base:act'`, such as `sit:call`, `lie:lift` or `sit:row`.
- Plus an optional held thing from `HOLDS`: `+cart`, `+cartfull` or `+carry`.

The functions:
- `poseOf(place)` returns a place's pose. It uses the place's `anim`, else `ACT_OF_TYPE`, else its plain pose. Sections 10 and 15 call it.
- `parsePose(pose, y)` returns `{base, act, cart}`. Here `cart` is a HOLDS key.
- `CROWD_ANIMS` is the set of activities that actually animate. Section 10 checks it, so an unknown activity falls back to the plain pose.
- `animateActivity(o, pose, dt, t, sk, y)` poses any rig: a crowd person, a FullPerson, or the player's Walker. Section 15 uses it for `'stand+carry'`. With `'stand'` and no activity, it moves exactly like `animateRig`.
- Rules: a seated-capable activity (`ACT_SEATED`) sits when `y >= 0.3`. A standing pose with `y < 0.3` treats y as floor height. `row` always sits. An unknown pose stands.

**Props.** `PROP_KIT` (a dumbbell, receiver, basket, guitar, pan, cart and so on) is built lazily from `part()`. For a crowd person, props are packed into the chunk mesh on 4 extra bones (`PROP_BONE`: R hand, L hand, C chest, B body), so they cost 0 extra draw calls. A full rig gets cloned meshes instead, through `rigProps`.

**Deck 6 draw calls (0.27.3).** The old hull split cut the engine room hull into 234 pieces. `byFace: true` in a deck's `hull` entry makes one piece per facing. That brought the engine room from 504–581 draw calls down to 86–275. Decks 1 and 2 now carry `byFace` too (added by their owners); Decks 3–5 still use the old split, left alone until the user decides.

**Demos** (these never save; the NOSAVE line is in section 13):
- `?crowd=40` (or any number) puts that many crew in the plaza.
- `?poses` lines up every pose with its prop, east of the lift. Lying poses go on the benches to the west.

## Added since 0.40.8 (builds 0.27.7 to 0.27.17)
All in sections 8 and 8b unless named. The DEV_NOTES rows have the detail.
- **More held things** (`HOLDS`): `+tray`, `+toolbox`, `+datapad`, `+device`. A HOLDS entry can take `one` (only one arm holds: 1 left, -1 right), `bone` (the prop rides a hand, R or L), `hx` (wrist) and `look` (head bend).
- **Crouch:** `crouch` is a base pose that walks like `walk`, with the hips 0.2 lower. animateRig reads `g.crouch` (0 unless crouching).
- **Coarse third detail** for crowds over `CROWD_MANY` (70): people beyond `CROWD_FAR2` (16) use `CROWD_DETAIL[2]`, about 1,100 triangles each. It's packed on first use (`packOf`), and `?crowd=` / `#crowd-` goes up to 151. A normal day reaches 67 people on Deck 3, so an event pushing a deck past 70 turns it on.
- **Machine looks** (`machineFx`): reads systems' `machineLook(id)` twice a second, and draws blink lamps, drips, dim plates and flicker glows in at most 4 instanced meshes. Optional `look` placement sits on machine entries. On Deck 3 the garden wilts (`GD.leaves`). Also lamp stutter (`machineFx.lamps(t)`, one line in section 12 after applyLight) and shower spray (one instanced mesh; `placeBusy` showers; thin and patchy when `shipSystems()` water or heat is low). `#looks` forces everything on.
- **Seats:** on a seat higher than 0.62, the feet rest on the ring. `?seats` / `#seats` puts a labelled stand-in on every seat place. All 267 seat places were fixed by the architects from my measurements (place `y`, `xy`, and numeric `face` in degrees, which sim 0.26.11 added to placeSpot).
- **Debug switches from the hash** (section 13): `URL_FLAGS` also reads `#tok.tok-value`, and `urlFlag(name)` returns a switch's value. `#crowd-120`, `#poses`, `#seats`, `#looks`, `#nosave` work on the playable link, which never gets a ?query.
- **The device pose (C11):** `deviceHook()` listens to section 19's `deviceOn('open'|'close'|'phosphor')` and sets `player.deviceOut`. One shared line in section 10's Walker adds '+device' when your hands are otherwise empty. The prop is drawn unlit on a full rig (+1 draw call while open), tinted by `devicePhosphor()` (`DEVICE_SKIN.ink`, else `--crt-ink`), and rebuilt on a phosphor change (`devicePropRecolour`).
- **Chatter bubbles (C5):** `bubbleSay(who, text, secs)`, `bubbleClear()` and `bubbles.hidden`. DOM only, at most 2 on screen, 120 to 220 px wide, kept on screen. The social engineer drives them from section 20.
- **Plain clothes for guests:** `dept: 'civilian'` with `outfit` draws a top in that colour, no badge, no pips.
- **Gym:** `punch` and `stretch` activities.
- **The widest zoom (0.27.18, sections 6 and 5):** `ZOOM_MIN` is 0.55, or 0.7 on a tall screen (`fitZoomMin`, also on resize). `placeCam` moves the camera's near and far planes out with the view's reach; at the old 0.45 they sliced the deck on tall phones. `placeSun` grows the shadow square with the view (`SHADOW_K`); it's 1 at the usual zooms. Before and after shots are in plans/shots/zoom-*.png.

## Added in 0.27.19 to 0.27.22 (the second performance engineer)
- **The storm's look and feel (0.27.19, 8b):** `shipFeel(kinds, len)` (section 18's `eventFeel` calls it; its stand-in steps aside) and `shipFeelFrame(t, dt)` (main loop, the machineFx line after applyLight). `FEEL_MOODS.<event id> = { phases: { <phase>: 0-1 }, a, b, light, bg }`: add an entry for the nebula drift and so on. The sky shader has `uWash`, `uT`, `uA`, `uB` (off at 0, so normal play is unchanged). Emergency lighting reads section 17's `blackoutAt(shipNow())`. `feelLook(t0)`: crew look up at a jolt (in `CrowdPerson.update`, via `lookOff`). `FEEL_S.gather`: an event's gathering on this deck, now; with more than `CROWD_GATHER` (40) on the deck the coarse crowd starts at `CROWD_GATHER2` (12). Reduced motion (`FEEL_CALM`): no shake, soft dips instead of flickers.
- **Draw calls, the same picture (0.27.20-0.27.22, section 4c, at the lead's request for the zoomed-out job):** `packGroups(geo, mats)` (neighbouring faces with one material become one group: door leaves, walls, headers, sills, void blocks); each hull piece merged (`mergeMeshes(p.g)`); `DOOR_LEAVES` (one InstancedMesh per leaf material, `doorLeavesSync()` each frame; the leaves are invisible boxes for taps); `tallCombine()` / `tallSync()` (tall furniture drawn per material for the whole deck; a fading room shows its own meshes and is skipped by the deck-wide one).
- **Numbers now:** desktop 1280×760, widest 0.55: D2 325, D3 356, D4 470, D5 299; zoom 1.0: 179-241. Phone portrait 390×844: D4 383 at the widest 0.7 (871 at 0.27.18), 210 at 1.5. day_check day 1 peaks about 170-250.
- **Gotchas found:** `renderer.info.render.calls` (the budget's number) counts the main pass only, not the shadow pass. The window glass is merged into the hull decor bucket and so casts a faint shadow although its `castShadow` is false; marking it noMerge changes the picture, so it's left alone. Big `push(...array)` spreads overflow the stack on Deck 5: use loops. My `until pgrep -f` wait loops matched their own command line and never ended: wait on a background command instead.

## The end-of-Pillar-4 optimization pass (0.27.25 to 0.27.27; plan: plans/perf-p4-plan.md)
Items 3, 1, 2 and 2b of the plan are done. Item 4 (dialogue as JSON.parse) was done by the dialogue owner; I measured 621a432 (the join('') follow-up): no change in size or load time. Items 5 (does the host gzip), 6 (cache painted textures) and 7 (smaller shadow map on phones; the user decides) are not started.
- **0.27.25, shadow stand-ins** (`shadowStandIns()`, section 4c, called after the hull decor merge in `buildDeck`). Still things that cast shadows (staticRoot children and TALL_ALL meshes per 10×10 cell, WALL_DECOR per wall run, hull pieces and CURVES per piece) are copied, position only, into a few meshes (`SHADOW_PROXY`, one per bucket and face side, material `SHADOW_PROXY_MAT[side]`). The originals get `castShadow = false` and `userData.shadowProxy`. The proxies are shown only during the shadow pass: `renderer.shadowMap.render` is wrapped, and a proxy with `vis` shows only when that object's chain is shown (fading rooms, dropped walls); `follow` copies a moving piece's matrix. Why not layers: r128's shadow pass tests layers against the main camera. The proxies' arrays are released after upload (`onUpload`). Reset in `unloadDeck`. GPU draws (every pass), portrait usual / zoomed: Sunday dinner 478/818 → 312/490, junior common room 657/1,076 → 338/613. The main-pass number (the budget's) is unchanged. JS heap +9 MB, accepted.
- **0.27.26, freezeStill()** (4c, after shadowStandIns): the staticRoot, TALL and WALL_DECOR subtrees stop recomputing their matrices (`matrixAutoUpdate = false`). Kept moving: noMerge subtrees, SPINS targets and their ancestors, STEAM puffs (freezing them changed 8 shots on Decks 3 and 6). Gain was small (scene matrix update 0.35 → 0.33 ms), which is why 2b followed.
- **0.27.27, posing only who's on screen** (8b, `crowd.update`): see the DEV_NOTES row. `CROWD_POSE_EVERY` (10) and `CROWD_POSE_MARGIN` (4 m). Always posed: talking/esc agents, `fresh`, dirty chunks, and everyone after the camera turns (`az` moves) or zooms. Crowd posing at Sunday dinner 1.07 → 0.41 ms (desktop). The sim can't tell: a fingerprint of crew positions, poses and `R()` matches across builds (scratchpad probe simeq.py: skipTo Sunday 18:20, Deck 3, six zooms × 150 frames, md5 of `[R(), DECK_CREW.map(a => [pos, pose])]`).
- **How I measure:** `perf_check.py` (js = game code per frame, the best of 3 batches, counted after one drawn frame so the ship time doesn't drift). Chrome's CPU throttle gave no steady numbers headless, so phone times are desktop × 4 to 5. Don't run perf_check at the same time as other checks: load times jump (6.8 → 9.7 s seen) and js gets noisy. For a crowd micro-benchmark, time `crowd.update(1/30, 10)` 100 times in the page.
- **Reviews (reviewer 2b, session_01F93LiFWtciyCLNV34qPsjP):** 0.27.25, 0.27.26 and 0.27.27 PASS (notes on claude/reviews-2). 0.27.28 PASS (it mirrored the GPU buffers: 0 mismatches). 0.27.29 to 0.27.32 PASS.

## Slow frames (0.27.28 to 0.27.30, the lead's "find the spike source")
- **Method:** a scratch combine (a local worktree, never pushed: 0.60.2 + sim + galley + my builds; build lines resolved to mine). A CPU profile of only the frames over 4 ms: CDP Profiler at 100 µs, aligned to the page by a named busy marker function (`MARKFN`), 3,000 frames with drawing skipped (one ship hour), in the mess at Sunday dinner (6*1440+18*60+25) and Tuesday breakfast (1440+7*60+5). Garbage: `HeapProfiler.startSampling` over 1,500 frames, by function. The scripts are in the scratchpad (pspike.py, spike.py, alloc.py, fpstat.py, rbwhy.py, arrive.py) and are not committed: re-create them from this description if needed.
- **Found (dinner / breakfast, share of slow-frame time):**
  - crowd group rebuilds 21% / 31% (fixed in 0.27.28);
  - findPath 35% / 13% (fixed in 0.27.29);
  - garbage collection 2–20%;
  - arrivals (crowdPack) 2–9% (halved in 0.27.30);
  - section 22's linesTick is never more than 0.2 ms.
  - Not the once-a-minute planner: only 5 of 105 slow frames fell on a ship-minute change.
- **0.27.28** `CrowdChunk.rebuild` reuses its arrays and buffers and uploads from the first changed slot. The `pv`/`pi` pending range is reset in `onBeforeRender`. Gotcha: in r128, vertex attributes upload in projectObject before onBeforeRender, and the index uploads after it in renderBufferDirect. Without pv/pi, two rebuilds between draws lost the first one's upload (cadet_test showed it).
- **0.27.29** findPath is a heap ordered by (f, first-push order), which is exactly the old scan's pick. The old search is kept as `findPathScan`. `path_check.py` must pass after any change to section 7, free, edgeOpen or edgeBlocks.
- **0.27.30** `CROWD_KEPT` (packed bodies by look, the last 40 to leave) and fewer per-frame allocations in 8b. Garbage at dinner: 196 → 183 KB a frame.
- **Result (0.27.27 → 0.27.29, combine with sim bfcd864):** frames over 4 ms dinner 36/31 → 17/19, breakfast 53/32 → 17/7; 99th percentile 4.1–4.8 → 2.4–3.2 ms. Worst frames now mostly follow garbage collection, which makes them noisy.
- **0.27.31** the main loop's wall cut: posts, `HRUN_EDGES` and the void blocks no longer allocate. Garbage at dinner: 183 → 168 KB a frame. **0.27.32** `loop()` uses index loops (its for…of made about 600 iterator results a frame) and no per-item closures. Garbage at dinner: 168 → 151 KB a frame.
- **Phone-like measuring (works):** `Emulation.setCPUThrottlingRate` at 4 is steady on hour-long runs (3,000 frames with drawing skipped; two runs agree within 2%). It wasn't steady on perf_check's short batches. At 4×, report frames over 16.7 ms and over 33 ms (not over 4 ms), the 99th percentile and the worst frame. For load time, set the throttle before `goto` by patching playwright's `Page.goto`, and time cadet_test's `Game()`. 0.60.2 → my 0.27.32 at 4×: dinner 6.85 → 3.3 ms a frame, frames over 33 ms 9–12 → 2 an hour; breakfast 4.25 → 2.05 ms; load 11.5 → 12.3 s (the shadow stand-ins). The scripts (phone.py, phoneload.py) are in the scratchpad; re-create them from this.
- **Left (2026-10-17):**
  - Section 10's `crewNearDoor`, about 40 KB/frame (a closure per crew member per door per frame), and section 14's `whereIs`/`shipDay`, about 15 KB. Sent to sim engineer 4 (session_01EJUGywZv9BpcUezjXES9AC, near handover) for after 0.60.4. Don't touch sections 10 or 14 yourself: they're changing for 0.60.3.
  - What's left in 8b is number boxing in `animateActivity` (about 15 KB/frame); it would need restructuring.

- **Load time:** unchanged by 0.27.25–0.27.32: about 12 s at 4× slower CPU and about 7 s at normal speed, alternating 0.60.2, 0.27.25 and 0.27.32 over 6 runs each. An earlier "+0.8 s" was one low run of 0.60.2. Always alternate builds when measuring load.
- **Next job, proposed to the lead (0.27.33): stand-ins built over a few frames.** `shadowStandIns()` (4c, called in `buildDeck`) costs, on a desktop, D1 20 ms, D2 95, D3 175, D4 63, D5 28, D6 9: about 15–20% of a deck change (130–850 ms), so perhaps 0.7 s on a phone for Deck 3. Plan:
  - Keep the two passes, but fill a few buckets per frame after the deck appears.
  - A bucket's originals keep `castShadow = true` until its proxy mesh exists, then switch: the same depth, so the shadows are the same at every moment.
  - Keep the `onUpload` array release.
  - Check: cadet_test identical, the 48-shot all-deck comparison, deck_check memory flat over round trips, and that `unloadDeck` mid-build leaves nothing behind.
  - Measure with scratchpad ssi.py (wrap `shadowStandIns`/`freezeStill`, time each `goToDeck`).

## Standing role: phone-speed watchdog (Pillar 4, from 2026-10-17)
- For each combined attempt the build master (now build master 2, session_01F8ph7FKqViF3heRn94YgBr; first was session_012K7RZ3oSX2vpBb1rR66MBh, claude/integration-test) sends, run `perf_check.py NEW.html OLD.html` (mine, ~5 minutes) and tell the lead PASS or the regressions with the commit that caused them.
- Its SCENES are stand-ins until Pillar 4's moments exist: switch them to the arrival steps (Deck 5 ramp 17:40 on Day 0, Works door, Bunk 1, dinner with Calder), Sowing morning (day 6 garden), Sunday roast, Tiles night (Tuesday 20:00 bow lounge), talent night and the lantern walk (promenade) as each lands.
- Baseline 0.41.10: all under 450 on phones; the junior common room zoomed out (portrait 0.7) is the tightest at 428.
- On call for Pillar 4's performance rows: two-person bubbles, the device hand-over and bag props, sigh/laugh/listen/play poses, lantern instancing (plans/pillar4-plan.md on ship-integration, Parts 4-6).

## Waiting (at 0.27.27)
- **Trays:** done. Sim 0.26.34 (236810f, sim engineer 4) passes my probe: 0 person-frames with a tray outside the mess in all 14 breakfast samples.
- The rest of the optimization plan (items 5 to 7) waits for the lead and the user.

## Waiting (at 0.27.22)
- Desktop widest Deck 4 is 470, a little over 450; everything else, and every phone view, is under. The next cuts, if wanted: hide the smallest wall pieces (light switches, small plates) below about zoom 0.65, or merge wall decor that never drops. Wall decor batching per wall run was tried and saved only 7 calls (most pieces are alone on their wall stretch).
- The user may want the zoom-out limit (0.55 desktop, 0.7 tall screens) widened now that it's cheaper; the near/far planes and shadows already follow the zoom.
- The garden view is done (0.27.23): `gardenView` (8b) draws `GARDEN_PLOTS` (recorded by `raisedBed`/`trellis` with `o.live`) as instances scaled by `SHIP.galley.garden.beds`. Root vegetables and the third bean bed have no place in the garden yet. The user kept 0.27.18's zoom limit (2026-10-16).

## Waiting for me (at 0.27.17; shipFeel done in 0.27.19)
- ~~**shipFeel(kinds, len)**~~ (done) for the events engineer (section 18). The kinds are 'jolt', 'lightsDip' and 'flicker' on the current deck; their stand-in, `eventFeelFrame`, shows the baseline and steps aside once shipFeel exists. Also the occasional flicker while `eventMod('effect', 'flicker')`, then emergency lighting, 'look up' at a jolt, and the address pose. The lead calls this when the storm switches on.
- **Review the device engineer's CRT skin for phone cost** when they send their branch (claude/device).
- **The 450 budget at gatherings:** the festival waits for a real-phone sign-off from this role (plan, "Gatherings").

## Draw calls when zoomed out (measured at 0.27.18, by the lift, desktop 1280×760)
The 450 budget holds at the usual zoom, but zoomed out a whole deck is in view and every object is drawn. The shadow square adds about 25 draw calls of that.

| Zoom | Deck 2 | Deck 3 | Deck 4 | Deck 5 |
| --- | --- | --- | --- | --- |
| 0.55 (new widest) | 712 | 648 | 1008 | 628 |
| 0.85 | 464 | 443 | 558 | 474 |
| 1.0 | 366 | 404 | 424 | 402 |

On a phone in portrait (390×844), Deck 4 is 871 at 0.7 and 468 at its usual 1.5; the 468 was the same before 0.27.18. Options, for the user: accept the higher cost while zoomed out (it's brief); raise ZOOM_MIN to about 0.85 (desktop) or 1.2 (portrait) to stay near budget; or thin the decor at low zoom (hide small items, merge per room). That last is the real fix, and the next performance job.

## Gotchas found since 0.40.8
- cadet_test sometimes shows `i_tap1` with 78 pixels one level off along a hull edge, even for DOM-only changes. It's run-to-run renderer noise, and the test labels it so.
- A 4-sided shower streak once moved that same edge; 3-sided didn't. If i_tap1 differs by more than one level, look again.
- Seat heights come from the place's `y`, never from SEAT_Y by type: the same type ranges from 0.18 (cushions) to 0.80 (bar stools). My probe scripts measure seat tops by raycasting (scratchpad b11/fit.py, which isn't committed); re-create the probe if needed.
- The player's Walker pose line in section 10 is shared with the player engineer (holding, crouch, deviceOut). Keep each addition inert while its field is undefined.

## State at 0.40.8: loose ends and weak spots
- The `HOLDS` arm poses (`sx/ex/sz/lean`) and the props were tuned by eye from screenshots only. Nobody has checked them on a real phone.
- When a busy activity and a held thing meet, the activity wins and the hold arms fade out (`busy`). Sitting or lying drops the held thing. That's fine for now, but it's a rule other sections should know.
- The level-of-detail switch is a hard cut at 9 m. You can sometimes see a "pop". A small hysteresis (switch at slightly different distances going out and coming back) would fix it.
- The crowd's bounding sphere is refit every frame for every chunk. That's cheap at 12 per chunk, but it's the first thing to profile if the crew count goes past 100.
- The `?poses` lineup artifact still shows build 0.40.2. Republish it if the poses change.
- Next I'd fix: the pop hysteresis, a far-LOD version of props (or hiding props past `CROWD_FAR`), and a phone check of the frame time with a full day's crew.

## Gotchas
- **Determinism:** never call `R()` in shared kit made at load, or in the crowd. Each person carries its own random stream (`o.rnd`), and `animateRig` takes it as `rnd`. One stray `R()` shifts every later random draw, and the regression stops being pixel-identical.
- **r128 skinning:** `CROWD_MAT` needs `skinning: true`, and the bone inverses must be identity. Otherwise people vanish or explode.
- **Seat height:** use the place's y when it's above 0, else `CROWD_SEAT` (sit .475, lie .5). In 0.27.0 a refactor used .5 while getting out of bed, and the regression caught it.
- **Prop orientation:** props are modelled for a forearm held level (forward is −y, up is +z), not for a hanging hand. The pan once stood upright because of this.
- **Seated-by-type places stay plain `sit`** (except call booths and the gym). Without this rule, the music beanbags mimed a keyboard.
- **Merge traps:** on every combined build, the conflicts were only the build lines and the DEV_NOTES table rows. Keep every row. The Deck 6 `hull` line also clashed once with the architect's `service`/`machines` entries, so keep both. I first wrote a `placeSpot` hook that clashed with the sim engineer's `crewPose`, and the lead kept theirs. Check section 10 before adding hooks.
- **Draw-call budget:** 450 per deck, set as `BUDGET` in `day_check.py`. Day 1 peaks at 0.27.6 were D1 377, D2 374, D3 388, D4 422, D5 397 and D6 305. Deck 4 has the least headroom.
- **Tuning numbers in 8b:** `CROWD_DETAIL` (segment counts for the two levels of detail), `CROWD_FAR`/`CROWD_FAR_ZOOM`, `CROWD_SEAT`, `CROWD_PER` (worked out from the GPU), `HOLDS`, and the speeds and amplitudes inside each `ACTS` entry.

## How to test
Set `CADET_CHROME=/opt/pw-browsers/chromium` first. Then:
- `python3 cadet_test.py OLD.html NEW.html`: good is ALL IDENTICAL on decks you didn't touch. If it isn't, find out why before going on.
- `python3 deck_check.py`: good is all OK (reachable, crew present, draw calls and memory within limits).
- `python3 day_check.py`: good is OK, with every deck's draw-call peak under 450. Also run day 7 when touching Deck 6.
- `python3 player_check.py`: good is all pass. It covers the `+carry` pose.
- By eye, open `?poses` and `?crowd=70`, and check that nobody is floating, sinking or holding a prop backwards.

## Ideas and open questions for the user
- Would you like the crew to carry more things (trays, tools, a datapad) now that held things are cheap? Each new one is a prop and a line in `HOLDS`.
- Should we test on a real phone? I can only measure draw calls and triangles here, not real frame times.
- Should crowds bigger than 70 be planned for (for example, a festival on the plaza)? If so, the next step would be a third, very coarse level of detail.
