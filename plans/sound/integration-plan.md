# Sound in the game: integration plan

SD1 (sound designer), 2026-10-25. Plan only: nothing here has been built, and the game file has not been touched.

The sounds are the ones the user approved in the soundscape mockup, Version 3 (`plans/sound/soundscape.html`, https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC): the deck hums, the device beeps, the doors and hatches, the lift, and soft footsteps. There is no crowd chatter (the user dropped it). Line numbers below are from the `claude/lead-36` build this branch started from. They will drift, so search for the function names rather than trusting the numbers.

## In one paragraph

All sound is made live by the browser (Web Audio), exactly as in the mockup, so the game needs no sound files. The sound code sits in one sealed block, `SND`, with about 30 small hook lines in existing sections telling it "a door opened here" or "the deck changed". Sound never draws on the game's random numbers (`R()`), never changes anything on screen except two rows in the Settings app, and stays completely off during the checks. So `cadet_test` stays pixel-identical and every check runs silent. The estimate is about 8 to 11 builder hours over 6 turns, plus review, two listening passes with the user, and two full rounds of checks.

## Where each sound hooks in

| Sound | Hook point in `starship-cadet.html` | Notes |
| --- | --- | --- |
| Deck hum | `goToDeck(n, at)` (~43210): cross-fade to that deck's hum. Also checked once a second against the player's room, for the garden. | Deck 1 Bridge hum; 2 Bridge hum (a touch warmer); 3 Commons; 4 Quarters; 5 Quarters hum made deeper (a workshop); 6 Engineering; R Commons. The hydroponics garden room on Deck 3 (floor `'garden'`) uses the Garden hum. Optional: about 2 dB softer at night, following `nightT`. |
| Room doors | The door loop in `loop()` (~43377): `d.open += ...`. Play "open" when `d.open` starts rising from about 0, and "close" when it starts falling from about 1. | Every room door uses room door **C (Cabin)**, the user's pick (2026-10-25). Only doors within about 7 tiles of the player play, quieter with distance and panned left or right by screen position. |
| Hatches | Same loop; `d.svc` (a service hatch, already "heavier" in the code). | Every hatch uses hatch **A (Bulkhead)**, the user's pick (2026-10-25). |
| Lift (**C, Smooth**, the user's pick) | `startRide(n)` (~43286) and `updateRide(dt)` (~43292), using the `RIDE` times. | At the start: the deck button press (**B, Two-step**, the user's pick: the Mail B bell made short, two quick rising notes over a soft press), then the lift doors closing. From `RIDE.shut` to `RIDE.light`: the ride. At about `RIDE.light`: the clunk and settle, then the chime, then the doors open (they already open from `d.force` there). The game's whole ride is only 1.8 s against 3.6 s in the mockup, so the ride sound is squeezed to fit and the chime rings on as the doors open. The lift door loop must not also fire the room-door sound (check `d.e.type === 'lift'`). |
| Device open / close | `deviceFire('open')` and `deviceFire('close')` (~10479): register with `deviceOn('open', ...)` and `deviceOn('close', ...)`, the hook the device already offers. | No edits inside the device code. |
| Device tap | `deviceDo(action)` (~10251 describes it): the soft tick (tap A, the user's pick). | One line at the top of `deviceDo`. |
| Mail arrived | `deviceNotify({ app, ... })` (~10472) when `app === 'mail'`, plus a check in the main loop when `mailUnread()` goes up (Mail is queued with an `at` time, so it lands later). | Mail B (the soft bell), the user's pick. |
| Heads-up | Where a heads-up goes on screen: `DEVICE_SKIN.heads(h)` with a non-null `h` (~10795, fed from `HU_Q`, ~10391). | Heads-up B (the rising pad), the user's pick. |
| Job done | `finishJob(id)` (~16715) when it returns true. | The four-note rise. |
| Job posted | Only when the device shows a new job badge for the player, through `deviceNotify({ app: 'jobs' })`. Never for every job the sim posts. | Machines post jobs all day, so tying this to `SHIP.jobs.push` would be noise. |
| "Not now" | The places that refuse you: `deviceLockedTap`, the tap text on sealed rooms and hatches, carrying with full hands, "too early to sleep". | One line each. The first turn lists them all with a `grep`. |
| Footsteps | `playerUpdate(dt, t)` (~12760): add up the distance walked and play a step every half stride, using the floor of the player's tile. | Floors from the tile's `st.floor` (~3130-3200): `plate` and grating get plating; `wood` and the promenade get planks; `carpet`, `corridor`, `lobby` and `warm` get carpet; `garden` gets the garden path. Crawl tiles are quieter and slower. No steps when sitting, riding, or in a scripted move. |

Crew footsteps and crew doors far from the player stay silent, and there is no crowd sound, as the user decided.

## The setting: sound on/off and volume (saved)

- Two new rows in the Settings app (`deviceApp({ id: 'settings' ... })`, ~11506), in the same On/Off button style: **Sound: On / Off** and **Volume: Low / Medium / High**.
- Saved in its own small key, `starship-cadet-sound` (`{ on, vol }`), not in the game save. The save format and the save budget stay as they are, and `player_check`'s saving tests don't change. The setting also survives starting a new game, as a preference should.
- Default: on, Medium. (Open question for the user.)

## Starting, pausing, stopping

- **First tap.** Browsers only allow sound after a tap. The `AudioContext` is made on the player's first real tap or key press anywhere (`pointerdown` or `keydown` with `isTrusted`). Until then `SND` does nothing at all. On iPhone the same tap also sets `navigator.audioSession.type = 'playback'` where it exists.
- **Pause.** `pauseSet(on)` (~11964) and `freezeSync()` (~8711, which also covers a game of Tiles): suspend the audio while frozen and resume after. The hum fades out over 0.3 s rather than cutting off.
- **Hidden tab.** It already calls `pauseSet(true)` (~12007), so suspending on pause covers it.
- **Sound off.** The context is closed and nothing is made, so there is no CPU cost at all.

## Keeping our rules

- **Never `R()`.** All randomness in `SND` uses `Math.random()`. The game's `R` (line 326) is the seeded stream every deck is built from. The mockup used a variable called `R` for its mixing routes; in the game that is renamed (`SND.route`), because a second `R` would break everything.
- **No name clashes.** The game already has `liftDoors` (~43263) and `DOORS`, and the mockup had functions with the same names. Everything goes inside one sealed block (`const SND = (() => { ... })()`), so only the name `SND` is added to the game.
- **Pixels.** Sound draws nothing: no DOM, no three.js objects, no draw calls. The only visible change is the two Settings rows, which only show up when the device is open on the Settings app. Deck regressions stay pixel-identical; only a check that screenshots the Settings app would change, and that change is expected.
- **Plans and sim.** Hooks only read state (door openness, the deck, the floor). They never change it, schedule anything, or touch ship time.
- **Checks run silent.** `SND` stays off when `navigator.webdriver` is true (Playwright sets it), and with `?nosave` or `?mute` in the URL. The checks never hear or start audio, even though Playwright's clicks count as real taps. `?sound` overrides this for the new sound check only.

## Phone cost

- **CPU.** Web Audio runs on its own thread, apart from the frame loop. The hum is about 8 oscillators and a few filters, the same as the mockup, and costs well under 2% of one core on a recent phone. Each door, step or beep is a handful of nodes that live for under 2 s. A cap of 12 one-shot sounds at once (oldest dropped) keeps a busy corridor cheap.
- **Frame rate and draw calls.** Unchanged: no rendering work.
- **Memory.** Three small noise buffers made once at start-up (about 2 MB in total at 48 kHz, counting the echo for big rooms; they could be shortened to cut that).
- **Battery.** Playing any sound keeps the phone's audio hardware awake, which is a small, steady drain (roughly like playing quiet music). It is suspended while paused or hidden, and costs nothing with sound off.
- **Size.** The file is about 4.5 MB today. Sound adds about 25 to 30 KB (about 0.6%).

## How much code

- The `SND` block: about 380 to 450 lines. That is the mockup's engine (hums, the tone and noise helpers, doors, lift, beeps, footsteps), less the crowd and the page controls, plus the deck and floor tables, the voice cap and the settings.
- Hooks in existing sections: about 30 lines, spread over sections 10 (doors, lift), 12 (main loop), 13 (pause), 15 (player, footsteps), 17 (jobs) and 19 (device, settings).
- A new check, `sound_check.py`: about 200 lines.
- Docs: a "Sound" section in DEV_NOTES, rows in its hook register, and a short "Sound" part in design-doc's "Art, camera & controls".

## Turn-by-turn build plan

Each turn makes small exact edits, bumps the build number, adds a row to the DEV_NOTES build table, runs the quick tests and `cadet_test` (decks pixel-identical), then commits and pushes.

1. **Engine and setting.** The `SND` block with the hum, beep, door, lift and step makers (still silent everywhere); first-tap start; suspend on pause, Tiles and hidden; off under webdriver, `?nosave` and `?mute`; the sound key and the two Settings rows. Check: `cadet_test` identical, device_check sees the new rows.
2. **Hum.** Deck hums on `goToDeck`, the garden room, the cross-fade, the night dip. Check: a deck tour with `?sound`, logging the hum per deck.
3. **Device and job sounds.** Open, close, tap, Mail, heads-up, job done, job posted (badge only), "not now".
4. **Doors and the lift.** The door loop sounds with distance, pan, type and the voice cap; the lift timeline fitted to `RIDE`.
5. **Footsteps.** Distance-based steps, floor lookup, crawl and sitting rules.
6. **Check and docs.** `sound_check.py`, DEV_NOTES and design-doc updates, a playable artifact for the user's listening pass, then the full round across six runners.

## Checks to add

`sound_check.py`, run with `?sound&soundlog`. In that mode `SND` records each sound it would play (name, time, volume) into `SND.log`, and plays it into a silent Offline context instead of the speakers. It checks:

- **Hooks fire.** Walk through a room door, a hatch and a crawlway; ride the lift 4 to 3; open and close the device; take and finish a job; get Mail; get a heads-up; tap a sealed hatch. The log must hold the expected sounds in order, each exactly once (no double fires from the door loop).
- **Hum per deck.** Each deck in the tour logs its own hum, and the garden room switches to the Garden hum.
- **Steps per floor.** Steps on plate, carpet, planks and garden tiles log the right surface, at about 1.8 a second while walking, and none while sitting or riding.
- **Never `R()`.** The game's `seed` is the same before and after a burst of 200 sound events.
- **Silent by default.** With no `?sound`, under webdriver, no `AudioContext` is ever made (the constructor is wrapped to count calls).
- **Levels.** Each sound is rendered offline, the same way as the mockup's measurement. No one-shot is louder than the Quarters hum, and footsteps are at least 8 dB under it.
- **Pause.** After `pauseSet(true)` the audio is suspended; after resume it runs again.

Add `sound_check` to the full round. It is quick (about 2 minutes) and fits in the lightest runner's share.

## Risks

- **Nobody can listen in a test.** The checks prove the sounds fire and the levels are right, but not that they sound good in the game. The user's ears are the real test, so plan for at least one tuning round.
- **Too many doors.** Crew walk through doors all day, and a busy corridor could chatter with door sounds. The radius, the distance falloff and the voice cap handle this; the radius may need tuning after a listen.
- **The 1.8 s lift ride** is half the length of the mockup's. The lift sounds will feel rushed unless the squeeze is done carefully. The ride itself must not be lengthened, since that would change the game.
- **iPhone silent switch and first-tap rules.** Some phones will be silent until the switch is flipped. The Settings row can say so.
- **Low-end phones.** Many sounds at once on an old phone could crackle. The voice cap and a Low volume help; worst case, a "fewer sounds" setting.
- **Name clashes and `R()`.** Covered by the sealed block and the seed check, but a mistake here would break every regression. That is why the seed check is in `sound_check`.
- **Screenshots of the Settings app** change by two rows: an expected diff on device screens only.

## Honest estimate

| Part | Time |
| --- | --- |
| Builder: 6 turns (engine 2 h, hum 1 h, UI 1.5 h, doors and lift 2 to 3 h, footsteps 1 h, check and docs 1.5 to 2.5 h) | 8 to 11 hours of session work |
| Lead review of the branch | about 1 hour |
| User listening passes and tuning (likely 2 rounds: door radius, lift squeeze, levels) | 1 to 2 hours of builder time, plus the user's time |
| Full round of checks (six runners, about 30 min each time), at least twice: after the build and after tuning | about 1 to 1.5 hours of wall time |
| **Total** | **about 1.5 working days end to end, one builder** |

It is a contained job: one sealed block and a few dozen hook lines, with no changes to the sim, the save or the art. Most of the uncertainty is in tuning to the user's ear, not in the code.

## All sounds chosen

The user's picks (2026-10-25, 12:05 PM Eastern): device tap **A** (soft tick), Mail arrived **B** (soft bell), heads-up **B** (rising pad). Then (via lead 36): room doors **C** (Cabin) and hatches **A** (Bulkhead). Everything else on the page is locked as it is: the deck hums, open and close panel, job posted, job done, "not now", the archway cue and the soft footsteps.

Final picks (via lead 36, 2026-10-25): lift **C** (Smooth: quieter parting doors, a gliding ride with a rising rush of air and no rail joints, a soft settle, three falling chime notes) and deck button **B** (Two-step). Nothing is left to pick. The builder takes exactly the chosen versions from the mockup (`DOORS.roomC`, `DOORS.hatchA`, `LIFTS.C`, `PRESS.B`, `SFX.tapA`, `SFX.mailB`, `SFX.headsB`) and can leave the rest out.

## Open questions for the user

1. Sound on by default, at Medium? Or off until you turn it on?
2. Should crew doors near you make sound, or only doors you walk through yourself?
3. Night: should the hum dip a little at night?
4. Music: the design doc says "Music later, with sound". Is music part of this job, or later?
