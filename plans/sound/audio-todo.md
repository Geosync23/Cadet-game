# Audio to-do

The sound designer (SD1, then SD2 from 2026-10-28) keeps this list. Newest decisions first in each part. Times are US Eastern.

## Waiting on the user

- **Mess hall soundscape** (the user, 2026-10-28, about 5:20 AM: "give me sample soundscapes for a busy mess hall"; reopens "no crowd chatter" for the mess): Wren Sounds: Mess hall, https://claude.ai/artifact/11WXFue17xQsVrShWejD21 (`plans/sound/messhall.html`). A murmur and cutlery, B clatter only (no voices), C fills and thins with the meal (recommended), D busy but cosy with the galley; each a quiet hour and a rush. Levels against the Commons hum (-20): averages 8-15 dB under, single clinks up to about the hum. In the game it would follow the people seated in the mess (an empty mess: nothing), in the room only. Pick saved to the page's store (collection `picks`, doc `mess`).
- **The room B door sound, the test fit:** no pick saved on Round 3; ask again. (Farewell song: B, the user via lead 43, 2026-10-28. Shop menu: no new sound, the lead's pick, the user can change it.)
- **Round 3 page (picked 2026-10-28, see Done)** (SD2, 2026-10-28, about 2:45 AM): Wren Sounds: Round 3, https://claude.ai/artifact/CzoYwmjJgVZoYDm2S1QTYs (`plans/sound/round3.html`). Answers save to the page's store (collection `picks`, one doc per item: `music:<id>`, `trad:<tradition id>`, `farewell`, `fx:<id>`, `general`; fields item, pick, note, at). Three parts:
  1. **Tradition music:** 14 samples (30-60 s, the v7 space style, no drums or noise), recommended: Year's end, Lantern walk, Harvest table (harvest and first-fruit suppers), Name on the beam, Farewell supper, Lap of the Wren, Crossing the Line, Veyli welcome, The goodbye (ending). Maybes: Midtour, Milestone tea, Sunrise stretch, Cup day, Storm lantern supper. Every other tradition listed with a switch, grouped by why it has no music (the crew's own music, talks, meals, garden, sport).
  2. **Veyli farewell song:** A (bronze and drone, recommended) or B (low pad only), each playable with stand-in singers. For the visit's farewell (Day 19, 09:00); could also play at Taavek's ramp.
  3. **Sounds for features since 0.93.0** (A/B/C each, recommendation marked): knock on your door (nights), the shielded reactor door, the dosimeter badge rack, inside the reactor room, a coil off and on, winding the coil, team "Next step" calls, team job done, promotions and the engine badge, room B, Calder's question, Basil, a booked shutdown, sensor calibration, the Tern landing (the old shuttle-bay item), the lathe, the bronze bar, the test fit, the HQ offer, Stay or Go, the clock's early-out question and Undo, the shop menu, save slots, Works tabs. Plus a list of new features that need no sound.
  Levels set offline against the Quarters hum (-19.5 momentary max): music samples about -21 to -25, the farewell song alone about -26 (the singers on top), feature sounds under the hum.

## For the listening pass (0.93.0)

- **Shuttle bay doors and the shuttle landing** (the activities page's Ship events: bayDoors, shuttle): left out of 0.93.0's activity sounds (lead 37, 2026-10-25): no clean hook yet for the diplomatic guests' arrival. Decide with the user whether they want it, then hook it to that event's arrival phase.
- **Not in 0.93.0's activity sounds** (lead 37's hard stop, 20:30 UTC): the **dryer** (the game has washers only, no dryer machine to read), the **cargo airlock** (nothing in the game cycles it yet), and the shuttle bay above. The B alternates (wrench, sealant gun, scanner pulses, water flush, two-note announcement) stay on the page, unused, since A is the pick.
- **Added late in 0.93.0 (FX20, a.4), worth a listen:** the galley at work while you're in it (a pan sizzling, now and then a knife, a burner or the oven; only with cooks at their stations), a running washer while you're in the laundry, the kettle at a kettle, the blanket after you lie down, a tile placed after the shuffle, the disc caught after a throw, the hinge's quiet swing after the oil, the trowel or the watering can at a garden bed, the mop for floor jobs, and a party popper when you join a celebration (a tradition named birthday, party, celebration or cake).

## Building (after the next release)

- **Sound in the game:** after 0.92.6 ships, on the user's go. The plan is `plans/sound/integration-plan.md`. It covers the decided sounds: hums, device and job sounds, doors, hatches, the lift and footsteps.
- **Activity sounds in the game:** approved; hooks and an estimate (about 4 to 6 builder hours) are in the integration plan. Round 2 is picked, so this is one more build turn.
- **Music in the game:** approved and built as `plans/sound/music-module.js`, ready to go in as one turn after the sound build (hooks, the Music app, a music check, about 3.5 to 5 builder hours; 21 tracks, rotating). Not in the game yet, by the user's word. The Music app is designed and mocked up on the Wren Music Player page.
- **design-doc "Sound" section:** on `claude/sound-sd1`; merge it with the sound build. Update it when music and activity sounds are picked.

## Pages

- Mess hall, for choosing (SD2): Wren Sounds: Mess hall, https://claude.ai/artifact/11WXFue17xQsVrShWejD21 (`plans/sound/messhall.html`).
- Picked (SD2): Wren Sounds: Round 3, https://claude.ai/artifact/CzoYwmjJgVZoYDm2S1QTYs (`plans/sound/round3.html`).

- Decided sounds: Wren Soundscape, https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC (`plans/sound/soundscape.html`).
- Approved activity sounds: Wren Sounds: Activities, https://claude.ai/artifact/5sjuT5XCJqCvMP68AipdZP (`plans/sound/activities.html`).
- Chosen: Wren Sounds: Round 2, https://claude.ai/artifact/1MXY7YxN9DGUChzUhAUyU7 (`plans/sound/round2.html`).
- Music player test: Wren Music Player, https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy (`plans/sound/music-player.html`).
- First versions of the music (before the sci-fi synth pass): Wren Sound Lab, https://claude.ai/artifact/Q6j5kSrYRvPxmSZdRB1DMg (`plans/sound/soundlab.html`).
- Old link kept: Wren Music Samples (`music.html`) now points to the Sound Lab.

## Done

- 2026-10-28, about 5:15 AM: **Round 3 picked** (design-doc "Sound", Round 3 picks). Tradition music for 8: beam, cup, farewell supper, the goodbye, harvest, lantern walk, Crossing the Line, Veyli welcome; none for lap, midtour, milestone, stretch, Year's end. Feature sounds: badge A, Basil A (none), bronze C, Calder B, calibrate A, clock confirm B, clock Undo A, coil A, HQ A (Mail), knock B, lathe B, promotion A, reactor door A, reactor room A, saves A (none), shutdown A, Stay or Go B, tabs A (none), team call A, team done B, Tern B, winding A. Farewell song B (low pad only). Shop menu: none (the lead's pick on SD2's recommendation; the user can change it). No pick yet: room B, the test fit.
- 2026-10-25, 2:02 PM: music v7. Station dawn, Wake cycle, First light and Systems online back to their earlier versions (noise layer silenced); seven ambient tracks given more shape (phrases, moving bass, more sequence, a build); the rest kept from v6.
- 2026-10-25, 1:50 PM: space music pass. All 21 tracks rebuilt as contemplative, planetarium-style space music: no noise layers, no drums (a soft pulse on working and midday), slow modal harmony, pads, sequences, chimes, swells and singing leads. Some renamed. Before/After on the player page.
- 2026-10-25, 1:33 PM: sci-fi synth pass. Festive voices (marimba-like pluck, music box, whistle, square lead, shaker) re-voiced as synths in every track, and the bounciest tempos slowed. A before-and-after list is on the Wren Music Player page.
- 2026-10-25, 1:24 PM: morning take 2: Systems online picked for mornings, the old morning tracks kept. Several tracks per time of day, rotating (least recently heard first): Wake cycle and Station dawn added for early morning, four new tracks (Promenade, Warm circuits, Porthole, Deep space). 21 tracks in all.
- 2026-10-25, about 1 PM: music on by default (Ship schedule); no music on arrival night (Day 0), it starts on Day 1; a Music app on the device (on/off, volume, Next, Ship schedule or choose a track), built into the module and mocked up on the player page.
- 2026-10-25, 12:55 PM: all music approved. The eleven samples grown into full ten-minute tracks (14 in all); the music module and its test page (Wren Music Player) built.
- 2026-10-25, 12:52 PM: Round 2 picked: clock in and out C (Lever and latch); tapping someone B (Bubble), louder, no mood range.
- 2026-10-25, 12:47 PM: all activity sounds approved (A as the default where there's a choice); no sound while on a call home.
- 2026-10-25: Soundscape mockup Versions 1 to 8. All core sounds chosen: tap A, Mail B, heads-up B, room doors C, hatches A, lift C, deck button B, soft footsteps, no chatter.
- 2026-10-25: The user's answers: sound on at Medium by default; crew doors near you make sound (quieter, capped); no night dip; music later.
- 2026-10-25: Integration plan written (`plans/sound/integration-plan.md`).
