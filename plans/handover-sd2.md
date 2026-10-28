# Handover: the sound designer (SD2)

Written 2026-10-28 (about 6:20 AM Eastern) by SD2 (session_01GKuymmLXWRnb63aGVFaScn), for a fresh session taking over sound. Lead: lead 43 (session_01GKuymjoDoY2kA9yCK12NG1). Reviewer: RV24 (session_01GKuymnJuoJTWnmYunbN7EP). Report with send_message, priority "next", and say your memory % each time. Read first: `CLAUDE.md`, `plans/handover-sound.md` (SD1's note: how section 27 works), this note, `plans/sound/r3-build-plan.md`, `plans/sound/audio-todo.md`, design-doc "Sound".

## Your job now: the sound update, turns 2 to 4

Branch **`claude/sound-r3`** (from `claude/staging-pad` e158dcff). Turn 1 is done (64077a69). Build turns 2-4 from `plans/sound/r3-build-plan.md`. Everything stays behind `const SND_R3_ON = false;`, which sits just before `const SND = (() => {` in section 27. With it off, cadet_test must be ALL IDENTICAL against the base. Each turn:
- small exact edits;
- a sound_check part, run on a copy switched on (`r3_copy(path)` in sound_check.py);
- cadet_test (switch off), the full sound_check, check_fast;
- push, then report to lead 43 and RV24.

Don't touch the build-number lines. Stay out of section 26 (controller) and section 18's visit lines (EV1 is changing them).

- **Turn 2, the mess hall** (the user's picks, 2026-10-28). The background is D without voices: the galley behind the counter (extractor, sizzle, a pan set down, the hatch, an "order up" bell) and the clatter (trays, cups, plates, cutlery, chairs). On top go the voices "warm": the warm low hum of talk.
  - Every layer follows the number of people in the mess hall: the crew there (`DECK_CREW` in that room) plus you.
  - An empty mess is completely silent. It plays only while you're in the mess hall (Deck 3, room name "Mess hall") and fades as you leave.
  - The working sound code is on the published page: `plans/sound/messhall.html` (version 2) on `claude/sound-sd2`; its source is in SD2's scratchpad as mess_base.js + mess2.js. Lift `voice2`, `CLINK`, `VOWELS`, `VOICES`, the galley part of `messScene2` and `VOICE_OPTS.warm`, then drive the density from the real count instead of `MESS_STATE.n`.
  - Levels on the page: an empty mess is silent; full, the background averages about 7 dB under the Commons hum and the voices add about 1 dB.
  - Do it like section 27's existing room ambience (`ambSet`/`ambLoop`/`ambTick` in the activity slot: the galley's cooks and the laundry), as a new loop read once a second. Never `R()`; use `Math.random`.
- **Turn 3** (watchers, section 27 only) and **turn 4** (five one-line hooks in owners' sections): the plan lists each moment and the user's pick (A/B/C). The sound recipes are on `plans/sound/round3.html` (`FEATURES` in its script): copy the picked option's `play` into section 27's FX table (`Object.assign(FX, {...})` in the activity slot) and call it via `S.fx(name)`, or `sndFx(name)` from other sections.

Picks (design-doc "Sound", "Round 3 picks"):

| Moment | Pick |
| --- | --- |
| Knock on your door | B |
| Reactor door | A |
| Badge rack | A |
| Inside the reactor room | A |
| Coil off and on | A |
| Winding the coil | A |
| Team "Next step" call | A |
| Team job done | B |
| Promotions | A |
| Calder's question | B |
| Basil | none |
| Booked shutdown | A |
| Calibration | A |
| The Tern landing | B |
| The lathe | B |
| The bronze bar | C |
| HQ offer | A (the Mail bell, already plays) |
| Stay or Go | B |
| Early clock-out question | B |
| Clock Undo | A |
| Saves app | none |
| Works tabs | none |
| Shop menu | none |
| Room B door | not picked yet (lead 43 is asking) |
| Test fit | not picked yet (lead 43 is asking) |

## What SD2 built (all pushed)

| Branch | Tip | What |
| --- | --- | --- |
| `claude/sound-sd2` | 12960d21 | Design pages and notes. Round 3 page `plans/sound/round3.html`, https://claude.ai/artifact/CzoYwmjJgVZoYDm2S1QTYs (answers in its store, collection `picks`). Mess hall page `plans/sound/messhall.html`, https://claude.ai/artifact/11WXFue17xQsVrShWejD21 (docs `mess`, `mess-voices`). audio-todo and design-doc "Sound" record every pick. |
| `claude/pad-wave-c` | a29a0f48 | Controller Wave C (sound from the first pad press, pad words, the Saves hint, tips in pad words). RV24 PASS; merged by BM20 into staging-pad (e158dcff). |
| `claude/sound-r3` | 64077a69 | The sound update, turn 1: event music (below). |

### Turn 1 (event music), in short

- Nine `SPACE` event tracks inside `createWrenMusic`, added only when `SND_R3_ON`: beam, cup, farewellsup, goodbye, harvest, lantern, line, veyli, farewell. They are reshaped like the comet.
  - Veyli has its own form with `sDrone` and `sBronze`.
  - The farewell song is 8 bars, about 40 s, played once.
  - Levels (`MLV`) are matched to the comet's offline. The farewell song sits about 6 dB under, so the voices are on top.
- `r3EventMusic()` (music slot, after `S.music = null`) picks the event track from where you are. The music slot's frame code asks it after `cometMusicOn()`. `S.r3Event` is exposed for sound_check.

## Gotchas

- **Test runs.** Run heavy checks one or two at a time. Three at once made cadet_test's first frame differ and deck_check time out loading; both passed when run alone.
- **Work folders.** check_fast needs `$CADET_WORK/three` and `$CADET_WORK/acorn` links in its own work folder. Setup: `npm pack three@0.128.0` into /tmp/cadet-work/three, `acorn@8` into /tmp/cadet-work/acorn, and `pip install playwright numpy pillow`. Use `CADET_CHROME=/opt/pw-browsers/chromium`.
- **The visit under skipTo.** In a fresh `?nosave` game the diplomatic visit doesn't start, but the Line does. check_r3music stands in for `eventNow` for the visit cases (as the comet check stands in for `cometMusicOn`).
- **`SOUND_ONLY=r3`** runs only those sound_check parts while building.
- **The pop-up queue.** A toast can wait in section 15b's queue behind another. Tests can set `window.cadetPopupsNow = true`.
- **Reading button text.** Device buttons are uppercased by CSS: read `textContent`, not `innerText`.
- **Offline loudness.** Extract `createWrenMusic` from the game into a page and render with an OfflineAudioContext (`/tmp/cadet-work/lv.html` + lv.js did this; rebuild from this note if gone).

## Open questions for the user (lead 43 has them)

- The room B door sound and the impeller test fit: not picked yet.
