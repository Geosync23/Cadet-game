# Sound + music build (0.93.0): shared brief

Lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX), 2026-10-25 ~18:15 UTC. **The user said go** (2:1x PM Eastern) after approving music v7, and expects a playable build in about 3-4 hours (target: playable ~22:00 UTC / 6 PM Eastern). Work fast, in parallel, and keep it small.

## Base and sources
- Base game: `claude/integration` **5898c190** (0.92.6, game sha256 10f654de56f76598c0747530fe5d05185fcc6eb5e91398584d462aafc8ebf266).
- Design and code to copy: `claude/sound-sd1` (179f4f5): `plans/sound/integration-plan.md` (hooks, rules, checks: follow it), `plans/sound/audio-todo.md`, `plans/sound/music-module.js`, page sources (`soundscape.html`, `activities.html`, `round2.html`, `music-player.html`). Only the chosen versions go in (picks listed in integration-plan.md).
- design-doc "Sound" section is on claude/sound-sd1 (merge it with this build).

## Who does what (three builders at once)
| Seat | Branch | Job | HUD while building |
| --- | --- | --- | --- |
| SD1 session_012DnJzEerXDa6SScxbQZ1q5 | `claude/sound-core` (or its own branch if refused) | Plan turns 1-5: the sealed `SND` block (engine, first-tap start, pause/hidden/Tiles suspend, silent under webdriver/?mute/?nosave, `starship-cadet-sound` key, Settings rows Sound On/Off + Volume), hums, device + job sounds, doors/hatches/lift, footsteps; `sound_check.py` core parts. **Turn 1 first and push it fast (~40 min)**: the two other builders start from it. | `0.93.0-s.N` |
| FX20 session_01FdWDetSihcXZYe2Tp8Kgjy | `claude/sound-act` | Activity sounds (approved Activities page + Round 2: clock in/out C, tap someone B louder, no on-the-line loop): the sound makers inside SND's activity slot, hooks per integration-plan "Where they hook in", its part of `sound_check.py` (a separate function/section). | `0.93.0-a.N` |
| FX22b session_01Lzi6Fe2HQJsVbaJBFxXtyx | `claude/sound-music` | Music: `music-module.js` into SND's music slot (drop OLD_TRACKS/MI_OLD/old defs; keep v7 tracks), time-of-day + working set, Day 0 silent, rotation `heard` saved with the music settings in the sound key (not the game save), the Music app on the device (Settings keeps only Sound On/Off and Volume), its part of `sound_check.py`. | `0.93.0-m.N` |

## Avoiding merge pain
- SD1's turn 1 leaves three marked slots inside the SND block: `// ---- SND: activity sounds ----`, `// ---- SND: music ----` (each with an empty function or object the core calls, e.g. `SND.music = null` set by the music slot), and one public call `SND.fx(name, opts)` (opts: `{ x, z, crew, vol }`) that plays any named one-shot. Activity builder registers its sounds by name for `SND.fx`. Music gets `SND.ctx` and a music bus `SND.bus.music` under the master volume.
- SD1 also exposes one place where the Settings app rows live; FX22b adds the Music app as a new `deviceApp`, not inside Settings.
- `sound_check.py`: SD1 makes the file with a `checks = [...]` list; the others add their own functions and one list entry each. The build master merges.
- Stay inside your slot plus your hook lines. Hook lines are one line each: `SND.fx('shower')`-style calls, guarded only if needed.

## Rules (from CLAUDE.md and integration-plan.md)
- Never `R()` (Math.random only), no DOM/three.js/draw calls except the Settings rows and the Music app, never change sim state, ship time or the save format.
- Silent in every existing check (webdriver). `cadet_test 0.92.6 vs yours` must be ALL IDENTICAL (device screens with Settings/Music app the only expected diffs; say so if any).
- Small exact-string edits; DEV_NOTES build-table row per turn; `bash check_fast.sh` before every push; plus the checks your hooks touch (device, player, interactions, day 1, events for ship-event hooks).
- Report each push to lead 37 (send_message, priority "next", never "now"): commit, game sha256, checks run, anything odd. When done, the reviewer and then BM18 take it.

## After the builders
- Reviewers: RV16 session_01ELg87ZGa4f9GTgTJMx39W5 (core), RV17 session_01CBbf1dZKv1LCrACof9HgyP (activities + music).
- BM18 (new): merges core → activities → music onto `claude/staging-0.93.0` from 5898c190, sets HUD 0.93.0, adds `sound_check` to the lightest runner share, runs the full six-runner round, sends the go/no-go to lead 37. Then the user's listening pass.
