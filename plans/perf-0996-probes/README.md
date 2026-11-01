# PF1's probes for plans/perf-0996.md (0.99.6)

Scratch measuring scripts, not checks. They expect three.js r128 in /tmp/cadet-work/three (as cadet_test), the container's
Chromium, and `/tmp/pf/names.json` (the game's top-level names; long.py's table sizes: make it with the snippet in
common.py's history, or drop SIZE_DAYS). Each reads `common.py` from /tmp/pf/scripts: copy this folder there first
(`mkdir -p /tmp/pf/scripts && cp plans/perf-0996-probes/*.py /tmp/pf/scripts/`). Run one at a time (timings are noisy otherwise).

- `long.py BUILD DAYS OUT.json`: the long run (skip to 07:30, an hour on two decks, the mess at 10:00): game code, heap, objects, save, listeners, table sizes.
- `long2.py BUILD DAYS OUT.json`: the same days with every frame of a ship hour timed, the night skip, deck changes, the save's write.
- `realtime.py BUILD HOURS OUT.json`: unbroken real-time hours in the mess, then a fresh page at the same moment.
- `reload.py BUILD SAVE.txt OUT.json`, `reload2.py`: a late save loaded against a fresh game skipped to the same day.
- `snap.py BUILD 5,40`: heap snapshots grouped by kind (`/tmp/pf/snap_dN.json`).
- `realclock.py BUILD MINUTES OUT.json sound|mute`: the real clock, sound on, audio nodes counted.
- `hitch.py BUILD DAY DAYS OUT.json`, `hitch2.py` (NAMES=..., BATCH=..., LIM=...): whole days frame by frame, the slow frames with the time in the named functions.
- `spike.py`, `spike2.py`: one hour change profiled. `soch.py`, `needs.py`: socialHour and crewNeeds timed.
- `fxverify.py BUILD`: F1's proof (every 7th shipEffectsAt answer against a fresh fxFrom).
- `vis.py BUILD OUTDIR [variants] [twice]`: the visual trade-offs' pictures and drawing work (ONLY=scene for one scene).
- `captest2.py BUILD`: the frame cap on a 120 Hz test clock. `trip.py BUILD`: deck round trips (backlog 14/18d).
