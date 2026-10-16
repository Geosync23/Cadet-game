# Handover: performance engineer (crowd rendering and activity poses)

Written at 0.40.8 (merged up to claude/ship-integration 980e6a9), brought up to date at 0.27.18 (on ship-integration d89a3f5 / 0.41.7) and again at 0.27.22 by the second performance engineer (session_01XAkY9U3mmstHQT2yAMTocA; claude/crowd-render, on ship-integration 7dd0aa4 / 0.41.8). Plain notes for whoever picks this area up.

## Role, branch, builds
- **Role:** making many crew cheap to draw (Pillar 1, workstream 5) and giving them activity poses and props (Pillar 2, A2). I also cut Deck 6's draw calls.
- **Branch:** `claude/crowd-render`. Lead merges it into `claude/ship-integration`.
- **Build numbers:** 0.20.x (crowd), 0.27.x (activities and Pillar 3 pieces, last was 0.27.23; next is 0.27.24). Bump the header build line and `GAME_BUILD` together, and add a row to the DEV_NOTES build table.
- **Owned in `starship-cadet.html`:** `// 8. CHARACTER KIT` and `// 8b. CROWD`. Plus the one NOSAVE line in section 13 (see the demos below).
- **Owned in DEV_NOTES:** the rows for 0.20.x and 0.27.x, and the sections "Crowd rendering (0.20.x)" and "Activities (0.27.x)". Those sections give the detail. This page is the short version.
- **Test scripts:** I don't own any. I use `cadet_test.py`, `deck_check.py`, `day_check.py` and `player_check.py`.

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
