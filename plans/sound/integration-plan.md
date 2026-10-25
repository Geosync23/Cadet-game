# Sound in the game: integration plan

SD1 (sound designer), 2026-10-25. Plan only: nothing here has been built, and the game file has not been touched.

The sounds are the ones the user approved in the soundscape mockup, Version 3 (`plans/sound/soundscape.html`, https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC): the deck hums, the device beeps, the doors and hatches, the lift, and soft footsteps. There is no crowd chatter (the user dropped it). Line numbers below are from the `claude/lead-36` build this branch started from. They will drift, so search for the function names rather than trusting the numbers.

## In one paragraph

All sound is made live by the browser (Web Audio), exactly as in the mockup, so the game needs no sound files. The sound code sits in one sealed block, `SND`, with about 30 small hook lines in existing sections telling it "a door opened here" or "the deck changed". Sound never draws on the game's random numbers (`R()`), never changes anything on screen except two rows in the Settings app, and stays completely off during the checks. So `cadet_test` stays pixel-identical and every check runs silent. The estimate is about 8 to 11 builder hours over 6 turns, plus review, two listening passes with the user, and two full rounds of checks.

## Where each sound hooks in

| Sound | Hook point in `starship-cadet.html` | Notes |
| --- | --- | --- |
| Deck hum | `goToDeck(n, at)` (~43210): cross-fade to that deck's hum. Also checked once a second against the player's room, for the garden. | Deck 1 Bridge hum; 2 Bridge hum (a touch warmer); 3 Commons; 4 Quarters; 5 Quarters hum made deeper (a workshop); 6 Engineering; R Commons. The hydroponics garden room on Deck 3 (floor `'garden'`) uses the Garden hum. |
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

**Crew doors near you make sound** (the user, 2026-10-25): any door or hatch that opens or closes within the same ~7-tile radius plays, whoever opened it. A door the crew opened plays about 6 dB quieter than one you walk through, and crew doors have their own cap: at most 2 at once and no more than 1 new one every 0.4 s (others are skipped, not queued), so a busy corridor doesn't pile up. Crew footsteps stay silent, and there is no crowd sound, as the user decided.

## The setting: sound on/off and volume (saved)

- Two new rows in the Settings app (`deviceApp({ id: 'settings' ... })`, ~11506), in the same On/Off button style: **Sound: On / Off** and **Volume: Low / Medium / High**.
- Saved in its own small key, `starship-cadet-sound` (`{ on, vol }`), not in the game save. The save format and the save budget stay as they are, and `player_check`'s saving tests don't change. The setting also survives starting a new game, as a preference should.
- Default: **on, at Medium** (the user, 2026-10-25).

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
2. **Hum.** Deck hums on `goToDeck`, the garden room, the cross-fade (no night dip: the user, 2026-10-25). Check: a deck tour with `?sound`, logging the hum per deck.
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
- **Crew doors.** With crew walking through a door near you, crew door sounds are quieter than yours, never more than 2 at once, and at most 1 new one per 0.4 s.

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

## Activity sounds: approved (the user, 2026-10-25, 12:47 PM Eastern)

All the activity sounds on Wren Sounds: Activities (`plans/sound/activities.html`, https://claude.ai/artifact/5sjuT5XCJqCvMP68AipdZP) are approved. Where the page offers an A and a B and the user didn't pick, **A is the default**:

- Ratchet and wrench: A, the ratchet (the wrench B stays available for heavier bolts if wanted).
- Seal a joint: A, the torch.
- Diagnostic scanner: A, the sweep.
- Toilet flush: A, the vacuum flush.
- Ship-wide announcement: A, the three notes.

**Calling home:** the ring and connect, and the hang-up. **No sound while you're on the line** (the user's call; the on-the-line loop is dropped).

**Round 2, chosen** (the user, 2026-10-25, 12:52 PM Eastern; `plans/sound/round2.html`, https://claude.ai/artifact/1MXY7YxN9DGUChzUhAUyU7): **clock in and clock out: C, Lever and latch** (a ratchet, a latch clunk and a spring snapping back; it ratchets up for clocking in and down for clocking out). This replaces the activity page's small time-clock sound. **Tapping a crew member: B, Bubble**, made louder to sit about level with Mail (about -25 against Mail's -24 and the hum's -20), with **no mood range**: the same sound for everyone.

**Where they hook in** (one more build turn, now that Round 2 is picked): `actStart(kind, ...)` for the player's activities (shower, toilet, eat, sit, lie, gym, call, browse and pay, cart moves, hobbies); the work steps (`wsFinish`, and the `turn`, `hold` and `wait` steps) for repairs and chores; the laundry machines; the rec deck activities; the time clock (`careerStarted` and clocking out); tapping a crew member (the talk start); and the ship events (the ion storm phases, the diplomatic shuttle, announcements). The same rules as the rest: never `R()`, nothing on screen, silent in the checks, under the hum. Estimate: about 4 to 6 more builder hours (the sounds already exist; most of the work is the hooks and a sound_check pass over a day of activities).

## Music: approved, built, ready to go in (the user, 2026-10-25, 12:55 PM Eastern)

All the music is approved: the three full tracks (Morning, Evening, Late night) and the eleven samples, which are now full tracks too, plus seven more added since (below). That makes 21 tracks of about ten minutes each, all made live, each evolving through 18 to 40 sections with a new tune and lead instrument on every pass, so nothing loops audibly. Tradition music stays on hold (`plans/sound/audio-todo.md`).

**The module:** `plans/sound/music-module.js` (about 480 lines, 47 KB). It is self-contained: its own small mixer, room echo and noise buffers, and one function, `createWrenMusic({ ctx, dest, shipTime })`. It can be pasted into the SND block or loaded as it is. It is **not in `starship-cadet.html`** yet. **Test page:** Wren Music Player (`plans/sound/music-player.html`, https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy) runs the same module against a pretend ship clock with a speed slider.

**The schedule** (ship time; while you're clocked in, the working set plays instead):

| Time of day | Ship time | Tracks (rotating) |
| --- | --- | --- |
| Late night | 00:30 to 05:00 | Nebula, Deep space, Night watch, Station dawn |
| Early morning | 05:00 to 07:30 | Station dawn, Wake cycle, First light |
| Morning | 07:30 to 11:00 | Systems online, Orbit rise, First light, Long view |
| Midday | 11:00 to 14:00 | Zenith, Still point, Promenade |
| Afternoon | 14:00 to 17:30 | Slow orbit, Long view, Warm circuits, Terminator line |
| Evening | 17:30 to 21:00 | Evening star, Terminator line, Porthole |
| Night | 21:00 to 00:30 | Night watch, Quiet stars, Porthole, Evening star |
| Working (on shift) | whenever you're clocked in | Clockwork stars, Steady state, Rounds, Warm circuits |

**21 tracks** (the user, 2026-10-25, 1:24 PM: "several tracks for each time of day and we rotate"):
- The first 14.
- Three ambient sci-fi synth tracks from morning take 2: Systems online (the user's pick for mornings), and Wake cycle and Station dawn (early morning).
- Four new ones so every time of day has 3 or 4: Promenade (happy lo-fi, midday), Warm circuits (chill lo-fi with a synth echo, afternoon and work), Porthole (warm lo-fi, evening and night), Deep space (ambient synth, late night).

**Version 7** (the user, 2026-10-25, 2:02 PM: "the first 4 tracks I want the old. The rest go for new except how some are too ambient. Give a little more shape.").
- **Back to their earlier versions:** Station dawn, Wake cycle, First light and Systems online (the take 2 synth tracks and First light from the sci-fi pass). Their soft "air" layer was filtered noise, so it is silenced: no noise anywhere (checked again: zero noise sources in all 21).
- **More shape:** Long view, Still point, Porthole, Night watch, Quiet stars, Nebula and Deep space now have:
  - clear four-bar phrases: a call, a held high note, an answer and a resting note on the home note;
  - a bass that moves to the fifth;
  - the sequence in more sections;
  - a Build section in every pass.

  They are still calm, with no noise and no drums.
- **Unchanged from v6:** the other ten.
- The module keeps the v6 versions as `V6` for the player page's before-and-after list. The builder drops `V6`, `OLD_TRACKS` and the unused old definitions when pasting into the game.

**Space music pass** (the user, 2026-10-25, 1:50 PM: "many tracks have background white noise. Kill it ... too happy and cutesy ... contemplative. Space music! Like a planetarium's music."). All 21 tracks are rebuilt in one style (`space()` in the module):
- no noise layers at all (checked: none of the 21 makes a single noise source in ten minutes; the hum is the only noise-like sound);
- slow suspended and modal harmony (Lydian, Dorian, Mixolydian, suspended major, one Aeolian), each chord held two bars;
- long wide pads, a quiet high shimmer, gentle echoing sequences, soft FM chimes, deep bass swells and slow singing leads that glide into their notes;
- no drums: the working and midday tracks have only a very soft low pulse;
- 48 to 74 beats a minute, lots of space and echo.

Some tracks have new names to fit (same slots): Morning became Orbit rise, Tea break Long view, Midday Zenith, Lunch break Still point, Afternoon Slow orbit, Golden hour Terminator line, Evening Evening star, Lights out Quiet stars, Late night Nebula, Shift start Clockwork stars, Steady work Steady state, and On your rounds Rounds. The versions before this pass are kept as `OLD_TRACKS` for the player page's before-and-after list (`play(key, { classic: true })`). The builder drops `OLD_TRACKS`, `MI_OLD` and the old track definitions when pasting into the game, which makes the module much smaller.

Earlier, superseded: **Sci-fi synth pass** (the user, 2026-10-25, 1:33 PM: "No steel drums, no kalimba. Sci-fi synth, that's what we want."). In the module, the festive voices are re-voiced for every track:
- the marimba-like pluck is now a glassy synth pluck;
- the music box is now a crystal FM bell;
- the whistled flute is now a warm synth lead;
- the square "cute" lead is now a rounded pulse lead;
- the shaker is now a soft noise tick.

The bounciest tracks are slower: Morning 92 to 84, On your rounds 112 to 96, Shift start 100 to 90, Midday 96 to 88, Promenade 98 to 88. Systems online and Station dawn were already all synth and are unchanged. The old voices and tempos are kept in the module only for the player page's before-and-after list (`play(key, { classic: true })`); the builder can drop them (`MI_OLD`, `was`) when pasting into the game.

**Rotation:** never the same track twice in a row; of the rest, the one heard least recently plays next (never heard first, ties at random). The module counts plays in `heard`; the game saves it with the music settings so the rotation carries on across days.

**How it plays.**
- It picks a track from the set by the rotation (below) and plays it through.
- Then it waits through a quiet gap before the next track: 1 to 3 minutes, which can be changed (`gapMin`/`gapMax`).
- When the time of day changes, or you clock in or out, it waits for the end of the current section (at most 30 seconds) and cross-fades over 6 seconds into the new set.
- A jump in ship time (sleeping through the night) changes over straight away.
- One ship hour is 100 real seconds, so most times of day last 4 to 6 real minutes. A ten-minute track usually hands over at a section end before it finishes. That is by design: the tracks are made to be heard in part.

**Defaults and rules (the user, 2026-10-25).**
- **Music is on by default, in Ship schedule mode,** at Medium volume.
- **No music on arrival night (Day 0): music starts on Day 1.** The module does this itself from `shipTime().day` (option `firstDay`, default 1). Sound effects and the hum still play on Day 0.

**The Music app (the user, 2026-10-25, 12:58 PM: "a music app ... choose which track to play or turn off and control volume").** A new device app, `deviceApp({ id: 'music', title: 'Music', ... })`, next to Hobbies and Tiles in the app list, in the same blocks as the other apps (text, buttons, list). It replaces a Settings row for music; Settings keeps only Sound On/Off and Volume. The app has:
- **Now playing:** the track's name and a line saying why it's playing ("Ship schedule: music for the evening", "work music while you're on shift", or "Your choice: Tea break, on repeat"). On arrival night it says "Quiet tonight. Music starts tomorrow, your first full day aboard."
- **On / Off, and Next:** in Ship schedule, Next is another track from the same set; with a chosen track, it moves to the next one in the list.
- **Volume:** Low / Medium / High (0.45 / 0.7 / 1).
- **What plays:** Ship schedule (the default) or Choose a track. Choose a track shows every track grouped by Work, Early morning, Morning, Midday, Afternoon, Evening, Night and Late night (`music.LIST`). A chosen track repeats, with the usual quiet gap, until you change it or go back to Ship schedule.
- **Saved per player,** apart from the game save, in the sound key: `starship-cadet-sound` = `{ on, vol, music: { on, vol, mode, heard } }`. It carries over to a new game.
- **Mockup:** the Music app on the Wren Music Player test page works against the pretend clock.
- **Hooks:** the app's `act(verb, arg)` calls `music.setEnabled`, `setVolume`, `setMode` and `next`, then saves the key. Its `view()` reads `music.state()`. The device redraws an open app when it's told to (`deviceFire`); the builder confirms the call for a live "Now playing" line. A redraw on the app's own taps is enough to start with.


**Levels.** At High, every track's loudest moment is 3 to 7 dB under the Quarters hum (-22.8 to -26.8 against -19.9). At Medium it is about 3 dB lower again.

**Hooks** (all reading only):
- Create it on the first tap, with SND: `createWrenMusic({ ctx: SND.ctx, dest: SND.musicBus, shipTime })`.
- `shipTime = () => ({ min: shipNow() % 1440, onShift: <the time clock's clocked-in state> })`. Clocking in is in section 13 (`careerStarted`, the "Clocked in" toast); the builder confirms the exact field.
- `music.update()` from `loop()` each frame. It costs almost nothing between bars.
- `music.pause()` / `resume()` with `pauseSet()` and `freezeSync()` (pause and Tiles).
- `music.setEnabled()` / `setVolume()` from the Settings rows.
- Same rules as all sound: never `R()` (the schedule uses Math.random; tunes use each track's own seeded numbers), nothing on screen except two Settings rows, off under webdriver, `?nosave` and `?mute`.

**Phone cost.**
- Each bar starts 10 to 30 short-lived notes. The audio thread handles them in well under 3% of a core on a recent phone; the frame loop is untouched.
- Memory: the module's own buffers are about 1.5 MB. They could share SND's buffers to save that.

**Build turns (after the sound build).**
1. Paste the module into SND (or load it) and add the hooks.
2. Add the Music app (about 70 lines in section 19's style) and its saved choices.
3. Add a music part to `sound_check.py`, with a fake ship clock:
   - each time of day plays from its own set, and the working set plays while on shift;
   - no track repeats back to back over 50 picks, and each set cycles through all its tracks before repeating;
   - a change waits for a section end of at most 30 s;
   - a sleep jump changes at once;
   - Off and pause go quiet;
   - Day 0 is silent and Day 1 starts music;
   - a chosen track plays and repeats, Next moves through the list, and Ship schedule returns to the time of day;
   - every track is under the hum;
   - `seed` is unchanged;
   - no AudioContext is made under webdriver.
4. Run the full round.

**Estimate:** 3.5 to 5 builder hours (module and hooks 2 to 3, the Music app 1.5 to 2), plus a listening pass with the user (about an hour of tuning), plus a full round of checks (about 30 minutes across six runners).

## Decided (the user, 2026-10-25, 12:25 PM Eastern, via lead 36)

1. **Sound is on by default, at Medium.** The Settings rows can turn it off or change the volume.
2. **Crew doors near you make sound,** within the ~7-tile radius, quieter than your own (about 6 dB) and capped (at most 2 at once, 1 new one per 0.4 s) so busy corridors don't pile up. See "Where each sound hooks in".
3. **No night dip.** The hum stays the same day and night.
4. **Music: by time of day, not by room** (the user, 2026-10-25, 12:40 PM). Three full tracks of about 10 minutes (Morning, Evening, Late night) and eleven samples (work music, and alternates for early morning, midday, afternoon, evening and night) are on the Wren Sound Lab page (`plans/sound/soundlab.html`, https://claude.ai/artifact/Q6j5kSrYRvPxmSZdRB1DMg), not chosen yet. Tradition music is on hold: only some traditions get it, and the user decides which (`plans/sound/audio-todo.md`). Music is its own later job and is not in this plan's estimate.

**When:** sound is built after the next release (after 0.92.6 ships), when the user gives the go. Until then this plan, the mockup page and design-doc's "Sound" section (on branch `claude/sound-sd1`) are the record.
