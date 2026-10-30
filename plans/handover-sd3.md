# Handover: the sound designer (SD3)

Written by SD3 (session_01GKuymir9eBj7X6kLtwLRmq), first 2026-10-28, refreshed 2026-10-30 at about 68% memory (handing over). Lead now: lead 46 (session_01GKuymiks9CC1WYr2may5nM). Build master: BM21 (session_01GKuymkAoLNTFXef9RgiYLn). Reviewers lately: RV25 (session_01GKuymnnpKvNH4Ki69KEzwG), RV26 (session_01GKuymjwVsweGh8p9EbTGHU), RV27 (session_01GKuymijhhErJ9V47wTGYrJ). Title seat: TB1 (session_01GKuymo2ikX7y7GA88GPXQP). Report with send_message, priority "next", with your memory %. Read first: `CLAUDE.md`, `plans/handover-sound.md` (SD1, how section 27 works; on claude/sound-sd2), `plans/handover-sd2.md`, this note, design-doc "Sound".

## What SD3 built (all reviewed and passed; nothing open)

| Branch | Tip | What | State |
| --- | --- | --- | --- |
| `claude/sound-r3` | e748f560 (+ notes) | The sound update: event music (SD2's turn 1), the farewell song A, the mess hall, the watcher sounds, six hooks, the room B home chime; sound_check r3 parts | Switched on in 0.96.0 (`SND_R3_ON = true`) |
| `claude/sound-098` | fb603947 | The event-music pick asked 4 times a second (backlog SD3-2) | RV25 PASS, in 0.98 |
| `claude/sound-099` | 7529b1e4 | The home chime kept across a reload, only your own opening, cleared by New game (SD3-1) | RV25 PASS, in 0.99 |
| `claude/title-music-099` | 19798c3a | Three title candidates (`SND_TITLE`), the title hook, the listening page `plans/sound/title-music.html` | RV26 PASS, in 0.99 |
| `claude/title-music-c` | febdf8ab | The user's pick C (Ship's log) | RV26 PASS, in 0.99 |
| `claude/title-music-0992` | bc6c6029 | C's melody in at about 4 s after the wake tap (the user: "Melody should be in at 5 seconds"): form Hum 1, Entry 4 (melody), Log 4 (sequence + melody), Rest 4, a 47 s loop | RV27 PASS (merged with TB1's ced89283 by RV27 for checking); for BM21 in 0.99.2 |
| `claude/mess-sound-0993` | 2348a5e6 | The mess hall: only the low murmur (the user: the white noise way too loud, the plate clinks not working). `MESS_BG = false` parks the galley's extractor and sizzle and the whole clatter; code kept, off | RV27 PASS; for BM21 in 0.99.3 |

## Where things are (section 27)

- `const SND_TITLE = 'C';` and `const SND_R3_ON = true;` just before `const SND = (() => {`.
- The music slot: event tracks in `SPACE` (time 'Event', never on the Music app list), `shaped` forms (`TRACKS.x.form = () => [sec(label, prog, bars, parts, e), ...]`), levels in `MLV`. `r3EventMusic()` picks event music (cached 0.25 s in `R3EV`). The title: `S.title(on)` sets `S.titleOn`; `S.frame` keeps sound running while `S.titleOn` (the ship is held under the title); `titleTick()` in the music slot's frame code loops `title + SND_TITLE` (next copy 4 s before the last ends), hushes `S.bus.hum`, and fades on the hand-over; `S.titleSnd` for checks.
- The activity slot: `MESS_SND` (the mess hall; `MESS_BG` false since 0.99.3: the murmur only), `R3` (feature sounds, watchers, `actPick`, `homeDoor` with its localStorage note `starship-cadet-sound-home:<SAVE_KEY>`).
- sound_check parts: `r3music`, `r3off`, `r3mess`, `r3fx`, `r3hooks`, `r3home`, `title`. `SOUND_ONLY=<regex>` runs some.

## Loose ends

- Not heard in a real playthrough (stood in for in sound_check): the knock, the team calls, calibration, the bronze bar, coil steps on a real Tier 4 job and night 3, the Tern landing, Calder's question, Stay or Go. Levels rest on the design pages' recipes.
- A pad-only player: a pad press may not count as a gesture for audio in Chromium, so the title music may wait for a first touch or key (TB1's note).

## Tools and gotchas

- Setup: `pip install playwright numpy pillow` installs a newer Playwright than the browser: always `CADET_CHROME=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`. `npm pack three@0.128.0` and `acorn@8` into `/tmp/cadet-work/three` and `/tmp/cadet-work/acorn`, untarred so the files sit under `package/`.
- Test a snapshot copy so you can keep editing while the round runs; check_fast reads the real file.
- Offline loudness: extract `createWrenMusic` (brace-match from `  function createWrenMusic(opts) {`, prefix `const SND_R3_ON=true;`), render with an OfflineAudioContext, `M.play(key, {fadeIn})` then `T.tick(1e9)`. Single renders vary a few dB (random parts): compare the energy mean of several. `T.bars[i].sec.label` and `.mel` give section and first-note times.
- Real-output probe (title): a copy with the test hook (`window.__sc = src => eval(src);` before the last `})();`), `?title&debug&sound`, Chromium with `--autoplay-policy=user-gesture-required`, tap the gate, then an AnalyserNode on `SND.bus.master` and `SND.titleSnd.list[0].where()` each 0.5 s. RV27 has its own at `plans/rv27-probes/tm_level.py` on claude/review-rv27.
- In sound_check, wait about 700 ms real time after a deck change before driving doors (the watcher skips frames while the deck loads); drive a door with `d.open` and `d.force` each step, standing at `cx + 0.5`. `S.fx` swallows errors: call `SND._.FX[name](SND.ctx.currentTime + 0.05, {})` to test a recipe.
- perf_check never starts sound (?nosave), so it can't measure section 27's cost.
