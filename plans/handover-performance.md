# Handover: performance engineer (crowd rendering and activity poses)

Written at 0.40.8 (merged up to claude/ship-integration 980e6a9). Plain notes for whoever picks this area up.

## Role, branch, builds
- **Role:** making many crew cheap to draw (Pillar 1, workstream 5) and giving them activity poses and props (Pillar 2, A2). I also cut Deck 6's draw calls.
- **Branch:** `claude/crowd-render`. Lead merges it into `claude/ship-integration`.
- **Build numbers:** 0.20.x (crowd), 0.27.x (activities, last was 0.27.6). Bump the header build line and `GAME_BUILD` together, and add a row to the DEV_NOTES build table.
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
