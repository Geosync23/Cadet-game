# Handover: AV1, sound and screens for 0.99.7

Written by AV1 (session_01GKuymmkjHutWouc88NdLkn), 2026-11-06. Lead: lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Reviewer: RV33 (session_01GKuymoAK9gACR31MRd1CMX). GM1 (Lightdisc play): session_01GKuymmzSJiWGVamRuV5nSG. Reach them with the claude-code-remote `send_message` tool. Read first: CLAUDE.md, plans/handover-sd5.md and plans/handover-sd3.md (how section 27 works), this note, design-doc "Sound" (its last paragraph, "Music played aboard, and film night's film").

## What AV1 built (branch claude/p997-av, from claude/integration d7ad4c58 = 0.99.6)

| Note (the user's words in plans/patch-0997.md on claude/lead-49) | What | Switch (all off) |
| --- | --- | --- |
| 13 hear the Captain's song at late piano | Section 27, the `LIVE` block just before `ambTick`: while late piano is on (eventsOn) and someone sits at 4-music-1 with a 'play' pose, three piano pieces in turn (Waltz for the Wren, Slow stars, Thursday; a 5 s rest between), from a point a step east of the bench | `SND_LIVE` |
| 29 hear the music jam | Same block: the jam's band from the players' middle; parts = min(5, 2 + players in a play pose, the record cabinet left out): guitar strums, bass, hand drum, then tambourine, then a reed tune | `SND_LIVE` |
| 44 (music) no music in Lightdisc | `S.frame`: `disc` = SND_DISC and not run and no pause and PAUSE.disc(): the context keeps running, so the track carries on (ship time is frozen, so it doesn't change) | `SND_DISC` |
| 42 film night video | `REC_FILM` (section 4, beside REC_SHOW): recScreen (4e) gives the cloth a 128 x 64 CanvasTexture (`recFilmTex`); recShowTick (8c) calls `recFilmTick(lit, t)`; the film itself in 4e's Rec engineer slot (`REC_FILM_CV`, `recFilmScene`): lighthouse, whales, ship and ringed planet, sunset, credits (bars, no words), 14 s each with 0.8 s fades, redrawn at about 12 fps, no new draw call | `REC_FILM` |

How the live music is heard: gain = in the room (1 - max(0, d - 3) / 9) ^ 1.3; outside the room 0.35 x (1 - max(0, d - 2) / 9) ^ 1.5 and a 900 Hz lowpass; panned like S.fx; level x0.8 (piano) or x0.75 (jam) on BUS.ui (so Sound On/Off and Volume, not the Music app). The ship's music: a new gain `BUS.duck` after BUS.music (made in buildGraph only with SND_LIVE; TRIM.music is 1 so the chain is equal), set to 1 - 1.6 x gain. R3's own duck (Calder's question) keeps BUS.music. After a stall the live loop skips bars already begun (as SND_LONG). Levels (RMS at the master, hum muted): ship music about -24 dB, piano in the room -19 (before the x0.8), full band -19.

## Checks

- sound_check: `check_live` (switch-on copy: the real late piano and jam days found from eventsOn, played in the room, music ducked, nearer louder, muffled through a wall, nothing on Deck 3, quiet after the jam; off: SND.live undefined), `check_disc` (stand-in: PAUSE.disc = () => true; on: running, same track, a pause on top suspends; off: suspended). `SOUND_ONLY=live|disc`.
- perf_check: new scene "film night, auditorium Sat 20:40" (REC_FILM on, needs REC_SHOW.state 'film'). `PERF_SCENES='film night'`.
- cadet_test off vs 0.99.6: ALL IDENTICAL. check_fast OK. perf_check film night: 100 calls portrait (the address 103), about 1 ms game code. sound_check full OK.
- Screenshots of the film: the probe scripts were in the session scratchpad (not kept); to look again: flagSet('rec.filmMoved'), skipTo day 6 20:30, goToDeck(7), step 200 frames (the screen unrolls in 4 s), set `REC_FILM_CV.t0 = clock.elapsedTime - seconds` to pick a scene; az = 2.356 views the screen from the seats.

## Gotchas

- Late piano on Day 2: the Captain sits down at the piano about 15 minutes in; the music waits for her (by design).
- At the jam usually only the one at the piano bench has a 'play' pose; the others sit. Hence the band's floor of three parts.
- The record cabinet's place (4-music-records) gives a 'play' pose to whoever puts a record on: left out.
- In sound_check, wait with steps (live_wait), never a bare wait: the audio clock and the frames both need to move.

## Open for the user (proceeding on lead 49's defaults)

- Should the piano and the jam follow the Music app's Off? (Default: no, they are sounds in the room.)
- A soft film score for film night? (Default: none, the picture only.)
- A listen to the pieces' levels and feel at the switch-on.

## Review

RV33 PASS on 15fbf3f (2026-11-06; claude/review-rv33 plans/review-rv33.md). RV33's levels in the real game (whole mix, hum muted, pre-compressor): a ship's track about -50 to -60 dB; piano -44 mid-room, -36 beside; jam -33 beside, so louder than the ship's own music but still under the engine hum (about -31). Left as built (you're next to the players); worth a listen at the switch-on, and the LIVE level factors (0.8 piano, 0.75 jam in `frame()`) are the one knob. The 4, 4e and 8c lines are the rec engineer's: owner review per owners.md.
