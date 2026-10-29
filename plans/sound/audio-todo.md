# Audio to-do

The sound designer (SD1) keeps this list. Newest decisions first in each part. Times are US Eastern.

## Waiting on the user

- **Tradition music** (the user, 2026-10-25, 12:40 PM): only some traditions get music, and the user decides which. The old "Tradition night" waltz is on hold until then; it isn't on the Sound Lab page.

## For the listening pass (0.93.0)

- **Shuttle bay doors and the shuttle landing** (the activities page's Ship events: bayDoors, shuttle): left out of 0.93.0's activity sounds (lead 37, 2026-10-25): no clean hook yet for the diplomatic guests' arrival. Decide with the user whether they want it, then hook it to that event's arrival phase.
- **Not in 0.93.0's activity sounds** (lead 37's hard stop, 20:30 UTC): the **dryer** (the game has washers only, no dryer machine to read), the **cargo airlock** (nothing in the game cycles it yet), and the shuttle bay above. The B alternates (wrench, sealant gun, scanner pulses, water flush, two-note announcement) stay on the page, unused, since A is the pick.
- **Added late in 0.93.0 (FX20, a.4), worth a listen:** the galley at work while you're in it (a pan sizzling, now and then a knife, a burner or the oven; only with cooks at their stations), a running washer while you're in the laundry, the kettle at a kettle, the blanket after you lie down, a tile placed after the shuffle, the disc caught after a throw, the hinge's quiet swing after the oil, the trowel or the watering can at a garden bed, the mop for floor jobs, and a party popper when you join a celebration (a tradition named birthday, party, celebration or cake).

## Building (after the next release)

- **Title screen music:** the user picked C, Ship's log (2026-10-29, on Title Music Picks). Set as `SND_TITLE = 'C'` on `claude/title-music-c` (SD3).

- **The sound update (Round 3 and the mess hall):** built on `claude/sound-r3` behind `SND_R3_ON` (off) by SD2 and SD3, 2026-10-28: event music (turn 1), the farewell song A (the user's later answer), the mess hall (turn 2), the watcher sounds (turn 3, with the test fit B), six one-line hooks (turn 4), and your new quarters' home chime C (the user's room B door pick, through lead 43; the first time you open room B's door after the move). Next: review, merge, then the switch-on and a listening pass.

- **Sound in the game:** after 0.92.6 ships, on the user's go. The plan is `plans/sound/integration-plan.md`. It covers the decided sounds: hums, device and job sounds, doors, hatches, the lift and footsteps.
- **Activity sounds in the game:** approved; hooks and an estimate (about 4 to 6 builder hours) are in the integration plan. Round 2 is picked, so this is one more build turn.
- **Music in the game:** approved and built as `plans/sound/music-module.js`, ready to go in as one turn after the sound build (hooks, the Music app, a music check, about 3.5 to 5 builder hours; 21 tracks, rotating). Not in the game yet, by the user's word. The Music app is designed and mocked up on the Wren Music Player page.
- **design-doc "Sound" section:** on `claude/sound-sd1`; merge it with the sound build. Update it when music and activity sounds are picked.

## Pages

- Decided sounds: Wren Soundscape, https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC (`plans/sound/soundscape.html`).
- Approved activity sounds: Wren Sounds: Activities, https://claude.ai/artifact/5sjuT5XCJqCvMP68AipdZP (`plans/sound/activities.html`).
- Chosen: Wren Sounds: Round 2, https://claude.ai/artifact/1MXY7YxN9DGUChzUhAUyU7 (`plans/sound/round2.html`).
- Music player test: Wren Music Player, https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy (`plans/sound/music-player.html`).
- First versions of the music (before the sci-fi synth pass): Wren Sound Lab, https://claude.ai/artifact/Q6j5kSrYRvPxmSZdRB1DMg (`plans/sound/soundlab.html`).
- Old link kept: Wren Music Samples (`music.html`) now points to the Sound Lab.

## Done

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
