# SD5's probes (0.99.5 sound: the user's notes 4, 9, 17)

Run with `CADET_CHROME=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome` (see plans/handover-sd3.md "Tools").

- `hidden.py BUILD` (note 9): hide the page with no frames after; the sound should be suspended.
- `mess_count.py BUILD` (note 4): who the mess hall sound counts across Day 2, every 20 min.
- `mess_rec.py BUILD OUTDIR` (note 4): 10 s recordings of the murmur alone at 0, 1, 3, 24, 39 crew, with MESS_SCALE off and on, plus levels.json (RMS dB).
- `long_audio.py` / `long_audio2.py BUILD MINUTES` (note 17): a real-time session, rooms changing every 45 s, pause every 3 min; every 15 s: dropouts (ctx.playbackStats), live sources, nodes, heap, compressor, peak; long_audio2 adds late starts, param moves in the past and frame stalls. Run two side by side for an A/B.
- `cost.py BUILD HOLD_MIN` (note 17): the audio thread's CPU (from /proc) per part: hum, music, the mess at the rush, then held.
- `param_growth.py plain|hold MIN`, `zombie.py`: the two ruled-out theories (param events, finished node chains).
- `athread2.sh PID LOG`: the audio thread's CPU every 10 s for one renderer.
