# Handover: the sound designer (SD1, section 27 SND and the music)

Written 2026-10-26 by SD1 (session_012DnJzEerXDa6SScxbQZ1q5), for a fresh session taking over sound. Lead at the time: lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX). Report with send_message, priority "next", never "now"; say your memory % in each report.

Read with: `design-doc.md` ("Sound", marked built in 0.93.0), `plans/sound/integration-plan.md`, `plans/sound/audio-todo.md`.

## Role

- Design every sound and the music (Web Audio synthesis only, no audio files), get the user's picks on review pages, then build them into the game.
- Section 27, `const SND = (() => { ... })()`, just before "12. MAIN LOOP". FX20 built the activity sounds slot and FX22b the music slot inside it; both are now mine to look after.

## Branches

| Branch | Tip | What |
| --- | --- | --- |
| `claude/sound-sd1` | this note | Design pages and plans: `plans/sound/` (soundscape, activities, round2, music-player, soundlab, morning2, music redirect, `music-module.js` v7, `morning-take2.js`, integration-plan, audio-todo) |
| `claude/sound-core` | 6cea352d | The core, 0.93.0-s.1 to s.7 (s.7 = RV16's notes). Merged by the build master |
| `claude/sound-comet` | b6569d19 | Comet track and swell for FX25 (0.93.2), from `claude/event-swap` 9ab920c |

Review pages (the user's picks are on them): Soundscape https://claude.ai/artifact/PP6pDpiZw8jzaNoLygCTgC, Activities https://claude.ai/artifact/5sjuT5XCJqCvMP68AipdZP, Round 2 https://claude.ai/artifact/1MXY7YxN9DGUChzUhAUyU7, Music Player (v7) https://claude.ai/artifact/2eiwTWnoSjg9SWcwi3k6Cy, first music versions https://claude.ai/artifact/Q6j5kSrYRvPxmSZdRB1DMg.

## The user's decisions (all approved)

- Device tap A, Mail B, heads-up B, room doors C (Cabin), hatches A (Bulkhead), lift C (Smooth), deck button B (Two-step). Footsteps all soft, close to the carpet ones. No crowd chatter, no background beeps.
- Sound on by default at Medium. Crew doors near you sound (quieter, capped). No night dip in the hum.
- Activities: all approved, A by default; nothing while on the line in a call home. Clock in/out C (Lever and latch). Tap someone B (Bubble), louder, no mood range.
- Music v7: 21 tracks of contemplative planetarium-style space music, by time of day with rotation; no noise, no drums. Music app on by default in Ship schedule mode; silent on arrival night (Day 0).
- Comet track: approved (FX25's request).
- Held: tradition music (only some traditions get it; the user picks which). Not started.

## How SND works (shared formats)

- **Silence:** `ALLOWED = URL_FLAGS.has('sound') || !(navigator.webdriver || URL_FLAGS.has('mute') || NOSAVE)`. Starts on the first trusted pointerdown/keydown; resumes on a tap (Safari). `SND.frame(run)` in loop() (after `const run = !freezeSync();`) suspends with pause, Tiles, a hidden tab or Sound Off.
- **`sndFx(name, o)`**: hoisted wrapper with try/catch, safe to call before section 27 has run. Other sections call this, never SND directly. Options `{ x, z, crew, vol, surface, d, long, layer }`. Silent beyond about 7 tiles, quieter with distance, panned by camera angle. 12-voice cap; crew sounds 6 dB quieter, max 2 at once, 1 per 0.4 s.
- **Watchers inside SND (no game edits):** hum by deck (`DECK_HUM`, garden floor gets the garden hum, checked every 0.5 s real time); Mail when `mailUnread()` rises; heads-up when `DEV.hu` changes; lift stages from `ride`/`RIDE`; doors from `DOOR_OBJS[k].open`; footsteps from player movement (a step per 0.62 tiles, 0.42 crouched; floor from `deckDef.rooms[roomAt(...)].floor`). Device: `deviceOn('open'/'close')` and a capture click on `#device button`.
- **Hooks in the game:** `finishJob` → `sndFx('jobDone')`; `deviceNotify` app 'jobs' → `sndFx('jobPosted')`; `deviceLockedTap` → `sndFx('no')`; Settings view/act use `SND.settingsBlocks()` / `SND.settingsAct(verb, arg)`.
- **Saved:** localStorage `starship-cadet-sound` (`S.prefs`: on, vol Low/Medium/High = 0.45/0.7/1; `prefs.music` for the music slot). Not in the game save.
- **Slots:** `// ---- SND: activity sounds ----` (`Object.assign(FX, {...})`, `S.actTick` once a second) and `// ---- SND: music ----` (`createWrenMusic`, `S.music`, `S.musicTick`). Also `S.whenReady`, `S.onFrame`, `S.bus.music`.
- **Music module** (`createWrenMusic`, same code as `plans/sound/music-module.js` v7): `space()` builds a track from a `SPACE` def; `SHAPED` / `phraseTune`; `MLV` levels per track; `SETS` by time of day plus working; least-recently-heard rotation; Day 0 silent; `setMode`, `next`; a time-of-day change cross-fades at a section end (at most 30 s).
- **Event tracks (comet branch):** `setEvent(key)` / `eventOn()`. In schedule mode an event beats the time-of-day set; a track the player chose in the Music app beats the event. The music slot's onFrame asks `cometMusicOn()` (FX25's) each frame and calls `S.music.setEvent('comet' or null)`. FX25 calls `sndFx('cometTurn', { long: 22 })` at 21:30 (a 20 s swell, measured -28.6 against the hum's -19.6).

## Next job: the Veyli farewell song (held)

Lead 37: wait until the visit build starts (after 0.93.2). Then make it a one-off event track in the music module like the comet: a `SPACE` entry (time 'Event'), add to `SHAPED`, an `MLV` level, and an `xxxMusicOn()` from the visit builder read in the music slot next to `cometMusicOn()` (make the slot pick whichever event is on). It sits under the crew's singing for about 40 s, so keep it low and sparse in the voices' range, and check its loudness offline against the hum like the comet.

## Rules and gotchas

- Never call `R()` in SND (Math.random only); the crew's planner must stay untouched. cadet_test must be identical against the base.
- Don't change the two build-number lines; the build master does.
- Routing names are `ROUTE`/`BUS`, never `R`.
- The seed check in sound_check drives only SND's watcher, no game frames (game frames call R()).
- Hum checks run on real time: tests must wait in real time.
- player_check has 3 known-old FAILs (the reserved-job bracket), also on plain 0.92.6.
- interactions_check can pass the 28-minute limit; rerun before calling it a FAIL.

## How to test

- Setup: `pip install playwright numpy pillow`; `CADET_CHROME=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`; three@0.128.0 in `/tmp/cadet-work/three` and acorn@8 in `/tmp/cadet-work/acorn` (names_check needs it).
- `python3 sound_check.py starship-cadet.html` (all sound, activity, music and comet checks), `python3 cadet_test.py OLD NEW` (must be identical), `bash check_fast.sh` before any push, then the full round as plans/testing-guide.md says.

## Open questions for the user

- Which traditions get music (held).
