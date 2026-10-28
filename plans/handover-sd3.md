# Handover: the sound designer (SD3)

Written 2026-10-28 by SD3 (session_01GKuymir9eBj7X6kLtwLRmq). Lead: lead 43 (session_01GKuymjoDoY2kA9yCK12NG1). Reviewer: RV24 (session_01GKuymnJuoJTWnmYunbN7EP). Report with send_message, priority "next", with your memory %. Read first: `CLAUDE.md`, `plans/handover-sd2.md` (the sound update's plan and gotchas), `plans/sound/r3-build-plan.md`, this note.

## State

Branch **`claude/sound-r3`** (from `claude/staging-pad` e158dcff). The sound update is built, all behind `const SND_R3_ON = false;` (section 27, just before `const SND`). Off: cadet_test ALL IDENTICAL vs e158dcff at every turn.

| Commit | What |
| --- | --- |
| 64077a69 | Turn 1 (SD2): event music |
| dc3014b6 | The farewell song switched to A (drone and bronze bar); `MLV.farewell` 1.39 |
| a09b32b7 | Turn 2: the mess hall (`MESS_SND`) |
| f58803b1 | Turn 3: the watcher sounds (`R3`: FX, `R3.watch` each frame, `R3.tick` once a second, `R3.actPick`; the reactor door in the door watcher) |
| cacfba97 | Turn 4: six one-line hooks (28a knock, 28d Next step and done, 24x calibration, 18 vessel slot bronze bar, 15 clock Undo); design-doc "Sound" Round 3 picks (from claude/sound-sd2, updated) |

## Where things are (section 27, the activity slot, before `ambTick`)

- `MESS_SND` (turn 2): `M` = { n, full, room, scene, clinks, at(n) }; `S.r3Mess` for checks. `ambTick` calls `MESS_SND.tick()`.
- `R3` (turns 3-4): helpers (lv, held, whine, ticks, chips, pad, chime), the FX (names `r3...`), the reactor-room throb loop, `W` (the watchers' last values), `watch`, `tick`, `actPick`. `S.r3` for checks. `ambTick` calls `R3.tick()`; `S.act` asks `R3.actPick(A)` first on 'begin'.
- sound_check parts: `r3music`, `r3off` (SD2), `r3mess`, `r3fx`, `r3hooks`. Run only these with `SOUND_ONLY=r3`.

## Loose ends

- Waiting on RV24's review of all four turns, and the owners' review of the turn 4 hook lines (player engineer: 15, 28a; Works career engineer: 24x, 28d; traditions engineer: 18's vessel slot).
- The room B door: no pick yet (lead 43 is asking the user). When picked: the recipe is on `plans/sound/round3.html` (`roomb`, B or C); it plays the first time you open your Deck 2 room B door (24u's move, Day 25).
- Not checked in a real playthrough (stood in for in sound_check): the knock, the team calls, calibration, the bronze bar, the coil steps on a real Tier 4 job and night 3, the Tern landing, Calder's question, Stay or Go. The full round at the switch-on should play through them.
- Levels: the feature sounds use the page's levels as they are (same bus and trim as the page). Worth a listen at the switch-on.

## Gotchas (new since SD2's note)

- `pip install playwright` gets a newer Playwright than the browser here: always set `CADET_CHROME=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`.
- npm pack folders must be `$CADET_WORK/three/package` and `$CADET_WORK/acorn/package` (tar without strip).
- Test a snapshot copy (`cp starship-cadet.html /tmp/cadet-work/snap.html`) so you can keep editing while the round runs; check_fast reads the real file, so don't edit it while that runs.
- In sound_check, after a deck change (`R3_AT`), wait about 700 ms real time before driving doors: the door watcher skips frames while the deck loads. Drive a door by setting `d.open` and `d.force` each step and stand at `cx + 0.5`, as the core check does.
- The music parts' randomness makes one offline render vary by a few dB: compare the energy mean of several (the lv harness: extract `createWrenMusic`, render with an OfflineAudioContext, `play(key)` then `tick(1e9)`).
- `S.fx` swallows errors in a sound; to test a recipe call `SND._.FX[name](SND.ctx.currentTime + 0.05, {})` directly.
