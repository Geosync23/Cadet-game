# Handover: the sound builder for 0.99.5 (SD5)

Written by SD5 (session_014zyJYPA1T75TkyU4en5qbs), 2026-10-31. Lead: lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN). Reviewer: RV28 (session_014zyJYQKwGvytfCGdrWMoiZ). Reach them with the claude-code-remote `send_message` tool (the plain SendMessage tool does not reach them). Read first: CLAUDE.md, plans/handover-sd3.md (how section 27 works, tools and gotchas), this note, design-doc "Sound".

## What SD5 built (branch claude/p995-sound, from claude/staging-0994 8976965e)

The user's notes (2026-10-31), all in section 27:

| Note | What | Switch |
| --- | --- | --- |
| 9 "audio keeps playing when I choose another window on Android" | `hideNow` beside `S.frame`: suspend at once on visibilitychange (hidden), pagehide, freeze. Cause: the suspend only ran from the main loop, and a hidden page draws no frames. | none (lead 47: plain fix) |
| 4 "Mess hall murmurs should scale with the population inside" | `MESS_SND`: `voicesAt` none below two crew; `levelAt` 0.25 (two crew) to 1 (half full) on gain `lvg` ahead of the lowpass (so the echo follows); smoothed 0.5 s, to silence about 1 s; nobody talking 5 s, the scene stops (`M.quiet`). `M.forceN` is a sound_check-only hook. | `MESS_SCALE = false`, on only after the user's pick on Mess Hall Murmur, https://claude.ai/artifact/E4ykNVcBpJjPxLgZxu3oWf (answers in its db, collection `answers`, doc `note4`) |
| 17 "popping and crackle after some play" | After a stall the loops (`every`, `voice2`, `startWalk`) restart from now; the music's `cur.tick` looks 2 s ahead (was 0.5) and drops bars already begun (not on a track's first tick: the title starts part-way). | `SND_LONG = false` (lead 47: the build master switches it on in the 0.99.5 candidate) |
| 17, the option | start()'s latencyHint 'playback' (a bigger output buffer; measured 32 -> 72 ms output latency here, about 0.1-0.2 s on a phone) | `SND_BUF_ON = false`, the user decides on the listening page (v2 has a note and an answer, field `buf`) |

## Measurements (plans/sd5-probes/, README there)

- Note 17 A/B, 8.5 min real-time each, side by side, same stalls: late starts 1573 -> 7 (worst 4 s -> 9 ms), param moves in the past 6430 -> 0.
- Ruled out by measurement: finished node chains left to GC (no render cost after they end), setTargetAtTime streams on long-lived params (flat), growth of loops / tracks / heap / live sources over 30 min, clipping (compressor 0 dB).
- Device dropouts (ctx.playbackStats underruns) are this container's CPU (steady, not growing; same with SND_LONG on). The sound's audio-thread cost (desktop core): hum 8%, + music 13%, + mess at the rush 13%. On a phone the remaining crackle risk is CPU. Built as an option, off: `SND_BUF_ON` (commit f3836dc, game 8415e2d0...d78a).
- Note 4 levels (murmur alone, RMS): 1 crew -57 dB -> silent; 3 crew -53 -> -64; half full and the rush -45 -> -46.

## Checks

sound_check new parts: `check_hide`, `check_mess_scale` (switch-on copy), `check_long` (switch-on copy, 4 stalls of 1.2 s, late starts counted; the off run is printed for the record). `r3mess` reads `SND.r3Mess.scale`. `check_buf`. `SOUND_ONLY=hide|mess_scale|long|buf`. Set CADET_CHROME in the same shell as the check (a backgrounded group loses an export: every part then fails with "Executable doesn't exist"). On this branch: sound_check OK, cadet_test vs 8976965e ALL IDENTICAL, check_fast (see the build-table row).

## Gotchas

- `pkill -f <pattern>` with the pattern in your own command line kills your own shell (exit 144). Use the pid.
- In the test harness (virtual clock) the once-a-second sound ticks only run when you step frames: wait with `wait_for_timeout` + `g.step(2)` in a loop, never a bare wait.
- DECK_CREW is refilled by the game every frame: don't empty it to fake an empty room; use `SND.r3Mess.forceN`.
- Two browsers at most; the audio-thread CPU probe reads /proc for threads named `AudioOutputDevi`.

## Open for the user

- Note 4: the pick on Mess Hall Murmur (then `MESS_SCALE = true` by the build master).
- Note 17: whether to turn on the bigger output buffer (`SND_BUF_ON`), on the same page.
