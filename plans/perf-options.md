# Smoother play: the speed options, parked for later

Written by lead 49 on 2026-11-01, from PF1's measurements (`plans/perf-0996.md`, its pictures in
`plans/perf-0996-visuals/` and its probes in `plans/perf-0996-probes/`, all on branch claude/perf-0996 and merged into
0.99.6). **The user's decision (2026-11-01, about 9:45 AM Eastern, via lead 49): "None for now but please document these
techniques in detail we will return to them."** So in 0.99.6 every option below is built and switched **off**; the game
looks and runs as 0.99.5 unless a preview word is in the link. This page is the full record, so whoever picks it up
later doesn't have to measure again.

## 1. Why this exists

The user (2026-11-01): "It gets worse the longer I play." Reloading doesn't help ("still slow after reopening"). They
play on a Samsung TriFold, folded (phone screen) and unfolded (a large, very sharp screen); both can be slow.

PF1 found **nothing in the game that piles up** (details in `plans/perf-0996.md`, "The numbers"):
- 40 ship days in one session: game code per frame 0.6-0.9 ms throughout; worst frames, draw calls (158-160), scene
  objects, page elements, listeners, timers and sound all flat. The heap grows 27 to 40 MB, mostly the browser compiling
  more of the game's code as more features run; no kind of game object accumulates.
- 12 ship hours of unbroken real-time play: cost follows how many crew are in the room, not how long you've played.
- A real Day 29 career save (Engine Specialist, 14 crew know you), and the same save after reloading the page: as fast
  as Day 1 in the same scene. The save stays small (largest 131 KB by Day 280; budget 250 KB) and takes 1-6 ms to write.

So the likely cause is **the phone heating up and slowing its graphics chip** ("thermal throttling"). It stays slow
after a reload because the phone is still hot. The game currently asks a lot of the chip on every frame and never lets
it rest:
- `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` (section 1): every frame is drawn at 2 device pixels per CSS
  pixel. Unfolded that is about 1584 x 2160 = 3.4 million pixels a frame.
- `antialias: true` (section 1): edge smoothing, several samples per pixel.
- A 2048 x 2048 soft (PCF soft) shadow map, redrawn every frame (sections 1 and 5).
- The main loop asks for the next frame straight away (`requestAnimationFrame(loop)`, section 12), so it draws at the
  screen's own rate: 120 a second on a 120 Hz screen, even when nothing on screen moves.

Not yet confirmed on the real phone. **The one reading that would settle it:** on the Dev link, Dev panel, Speed tab,
in a busy place (the mess at dinner), screenshot the card at the start and again after 30-45 minutes. If "Frames a
second" drops while "Game code a frame" stays about the same, it's the phone warming. If game code goes up too,
something in the game grows after all, and the card's numbers say where to look.

## 2. The four options (all built, all off)

"Drawing work" below is the time to draw one frame in the test browser's software graphics (SwiftShader), median of 7.
It stands in for the graphics chip's work, so the options can be compared; it is **not** a phone's time.

Scenes: Sunday dinner in the mess (67 crew), the Captain's address in the auditorium (48), quiz night in the bow lounge
(55). Views: the phone view 390x844 on a 3x screen; the TriFold unfolded (792x1080 CSS at pixel ratio 2 = 1584x2160);
folded (412x960 at 2.625, drawn at 2 today).

### Option 1: frame cap 60 (`PF_CAP_ON`, preview `#pfcap`; `#pfcap-30` for 30)
- **What it does:** the main loop draws at most 60 frames a second (or the number after `pfcap-`). Code, section 8b
  slot: wraps `requestAnimationFrame` for the main loop only; a frame runs once at least 1/60 s (less 3 ms) has passed,
  so a 60 Hz screen keeps every frame. Ship time is unaffected (it runs on real time).
- **What you see:** nothing in a still picture. On a 120 Hz screen, movement updates 60 times a second instead of 120.
  Most games run at 60 or 30.
- **Gain:** half the frames on a 120 Hz screen, so half the work and heat per second (checked: 600 of 1,200 frames in
  10 s). No change on a 60 Hz screen.
- **PF1's view:** recommended first. The most likely help for "worse the longer I play", and nothing looks different.

### Option 2: sharpness 1.5 (`PF_PR_ON`, preview `#pfpr`)
- **What it does:** `renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5))` then `renderer.setSize(...)`, once
  before the first frame. 44% fewer pixels than at 2.
- **What you see:** the 3D ship very slightly softer at the edges. The HUD, cards, Mail and the device are page text
  and stay fully sharp.
- **Gain (drawing work, dinner / address / lounge):** phone view -22% / -26% / -33%; **unfolded -28% / -41% / -35%**;
  folded -23% / -23% / -32%. Unfolded, every frame is about twice the work of the phone view (2,224 vs 1,195 for
  dinner), so this is where it saves most.
- **Pictures:** `open-dinner-pr15.jpg`, `open-lounge-pr15.jpg`, `open-address-pr15.jpg`, `fold-*-pr15.jpg`,
  `<scene>-pr15.jpg` (left: today, right: with the option, 1:1 pixels).
- **PF1's view:** recommended second; hard to see at arm's length.

### Option 3: shadow map 1024 (`PF_SH_ON`, preview `#pfsh`)
- **What it does:** `sun.shadow.mapSize.set(1024, 1024)` instead of 2048: the shadow pass draws a quarter of the texels.
- **What you see:** shadow edges a little softer and blockier.
- **Gain:** phone view -5% / -6% / -1%; unfolded -2% / -11% / 0%. With option 2 (`#pfpr.pfsh`): -24% / -30% / -33%.
- **Pictures:** `open-<scene>-sh1024.jpg`, `<scene>-sh1024.jpg`.
- **PF1's view:** small gain; only worth it alongside the others.

### Option 4: no edge smoothing (`PF_NOAA`, preview `#pfaa`)
- **What it does:** the renderer is made with `antialias: false` (section 1, read as the renderer is made, so it can't
  be changed without a reload).
- **What you see:** stair-steps on slanted edges: lamp shades, rails, sofas, table edges.
- **Gain:** -30% / -34% / -33% in software graphics, but phone graphics chips smooth edges far more cheaply, so the real
  gain is likely much smaller.
- **Pictures:** `<scene>-noaa.jpg`.
- **PF1's view:** not recommended: the most visible change and the least certain gain.

### Measured and not offered
- Plain (not soft) shadows: 0-2%.

## 3. How to try them

- Preview words go in the link after `#`, joined with a dot: `#pfcap`, `#pfpr`, `#pfsh`, `#pfaa`, `#pfcap.pfpr`.
  (claude.ai passes a plain hash through; the game reads hash words the same as `?query` switches, section 1's
  `URL_FLAGS`.) If a dotted hash doesn't reach the page, publish a trial copy with the switches forced on instead.
- **The trial link** (lead 49, 2026-11-01; PF1's build 67acc5b = 0.99.5 + F1, with options 1 and 2 forced on, Download
  my save enabled): https://claude.ai/artifact/KENCSJbbssDyUv5K2sYF5H. A trial page only; never a release.
- **The choice page shown to the user** (pictures, the trial link, an answers form): https://claude.ai/artifact/UhTjVkZarAfucJdXWhN6U9.

## 4. How to switch one on later (for everyone)

Each is one line in the build. In section 8b's performance slot:
`const PF_PR_ON = URL_FLAGS.has('pfpr'), PF_SH_ON = URL_FLAGS.has('pfsh'), PF_CAP_ON = URL_FLAGS.has('pfcap');`
Change the chosen one's `URL_FLAGS.has('...')` to `true`. Option 4 is section 1's `PF_NOAA` line.
Then, as for any switch-on: check_fast; cadet_test (with options 2, 3 or 4 on, every picture differs: look and explain
it, don't expect identical); perf_check alone against the previous build; and the full round.

**A setting the player controls** (for example "Smoother play" in Settings, saved per device) is a possible middle way:
nobody's picture changes unless they turn it on. That is new game code (a Settings row, saving the choice, applying the
pixel ratio and the cap live, the renderer's antialias needing a reload): a builder, a review and the round.
**Automatic** variants are also possible: cap only while the phone is unfolded, or lower the sharpness only when frames
start coming late. Neither has been built or measured.

## 5. Also found, not the long-play slowdown: stalls that come with the calendar

Single long frames when the crew's day is planned again in one go (desktop times; a phone may be 4-5 times slower):

| When | Worst frame | What takes the time | Where (owner) | Idea |
|---|---|---|---|---|
| Every midnight (23:59, 00:00) | 49-114 ms, then 35-48 ms | the galley asks for tomorrow's plan (`galleyTick` -> `shipDay(d + 1)` -> `schedBuild`), then the crew on the deck plan theirs | section 14 `shipDay` (sim engineer), section 16 `galleyTick` (galley engineer) | the plan is pure (same whenever made), so make it in pieces over the quiet frames of the evening before |
| A ship-wide event begins or ends (e.g. Day 17 11:00, the diplomatic visit) | 290-386 ms | `evChanged()` clears every cached day plan (`SHIP_DAYS.clear()`), and the social hour asks for today's again at once (`socialHour` -> `planWhere` -> `shipDay` 256 ms, `schedBuild` 145 ms) | section 14 (sim engineer); the call from section 20 `socialHour` (social engineer) | event times are known in advance: plan the after-change day in pieces before it starts, or keep the days the event doesn't touch |
| Other rebuilds (Day 16/17 15:59 `worksCareerTick`; 05:49 `galleyTick`) | 50-107 ms | the same rebuild from other callers | as above | as above |

Already fixed in 0.99.6 (F1, section 17, same answers, reviewed by RV31; the systems engineer, its owner, still to look):
`shipEffectsAt` kept its 8-day cache only until `MACH_REV` changed (nearly every ship hour), so during the diplomatic
visit every ship hour cost 15-49 ms. Now cached on the hour's record: 15 of 16 hours over 10 ms down to 4.

The user hasn't been asked again about the calendar stalls; lead 49 asked on 2026-11-01 whether they go in 0.99.6 or later.

## 6. Status

| Item | Built | On in 0.99.6 | Decision |
|---|---|---|---|
| Option 1 frame cap 60 | yes (PF1) | no | parked, the user 2026-11-01 |
| Option 2 sharpness 1.5 | yes | no | parked |
| Option 3 shadow map 1024 | yes | no | parked |
| Option 4 no edge smoothing | yes | no | parked (not recommended) |
| A player setting / automatic variants | no | - | idea only |
| F1 shipEffectsAt cache | yes | yes (always; same answers) | done |
| Calendar stalls | no | - | asked the user |
