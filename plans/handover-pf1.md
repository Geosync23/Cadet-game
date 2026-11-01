# Handover: PF1, the performance seat for 0.99.6

Session session_01GKuymkwCZBPPLnKtstwj1r, for lead 49 (session_01GKuymjPvM7XFzxM7XqFREd). Read plans/perf-0996.md first: it
is the whole report (the user's question, the method, the numbers, the fix, the visual options, open questions).

## Branch and builds
- `claude/perf-0996`, made from `claude/integration` 0.99.5 (6475bb30, game 93aed54f...5164).
- 0.99.5-pf1.1 (67acc5b, game sha256 90dbc4f2...46a7): the report, F1, the visual switches (off), pictures, probes, the
  build-table row. Build lines unchanged (the build master's).

## What I own and built
- Section 1 (the performance engineer's): `PF_NOAA` (line 420), read from `?pfaa` / `#pfaa` as the renderer is made.
- Section 8b, my slot (just above "end of slot: Performance engineer"): `PF_PR_ON` (#pfpr, pixel ratio max 1.5),
  `PF_SH_ON` (#pfsh, 1024 shadow map), `PF_CAP_ON` / `PF_CAP` (#pfcap, #pfcap-30: a frame cap on the main loop's
  requestAnimationFrame; Dev mode's Speed wrapper sits outside it and still sees `loop`). All off: nothing runs.
- Section 17 (the systems engineer's; listed for their review): `FX_OF` and `shipEffectsAt`'s middle line (F1).
- plans/perf-0996.md, plans/perf-0996-visuals/ (pairs and small whole screens), plans/perf-0996-probes/ (scripts + README).

## Loose ends
- The user's answers (through the lead): Speed card screenshots (start, and after 30-45 min, mess at dinner), which
  visual options (if any), whether the calendar stalls (sim engineer, section 14 `shipDay`) are for 0.99.6.
- Switching an option on for everyone: change its `URL_FLAGS.has('pf..')` to `true ||` style or a plain `true`, as the
  project switches others; the pictures change only on phones with a pixel ratio over 1.5 (pr), and everywhere for sh.
  cadet_test runs at a pixel ratio of 1, so `#pfpr` alone would not show there; `#pfsh` would.
- Backlog 14/18d: not reproduced on 0.99.5; suggest closing or a tolerance (lead's call). Backlog 32 (perf_check spike
  re-sample) not started.

## Gotchas
- `pkill -f name` / `pgrep -f name` inside a Bash call kills that call's own shell when its command line contains the
  name (exit 144). Use pid files (plans/perf-0996-probes: run with `nohup ... & echo $! > x.pid`).
- `performance.memory` is rounded in this Chromium (it read 104 MB for days); use CDP `Runtime.getHeapUsage` after
  `HeapProfiler.collectGarbage`.
- `gl.finish()` doesn't wait for the GPU process: time drawing with a 1-pixel `readPixels` after render.
- Sound never runs under automation unless `?sound` (and Chromium's `--autoplay-policy=no-user-gesture-required`).
- With the real clock the headless loop runs about 2-3 frames a second (SwiftShader), so real-clock runs are only good
  for counting things (audio nodes, heap), not frame rates.
- `git checkout FILE` to drop a trial edit drops every uncommitted edit in that file: commit or stash first.

## How to test
- My changes: `bash check_fast.sh`, cadet_test vs 0.99.5 (ALL IDENTICAL), food_check, social_check, day_check 18,
  machine_check, perf_check NEW OLD; F1's proof: `plans/perf-0996-probes/fxverify.py`.
- The full round on six runners before merging (CLAUDE.md).
