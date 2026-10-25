# RV16 review: sound core for 0.93.0 (SD1, claude/sound-core)

Reviewed: e7c82903 (turn 1, 0.93.0-s.1) and e04419ce (turns 2-5, 0.93.0-s.5, game sha256 19d809c0...), against
claude/integration 5898c190 (0.92.6, sha256 10f654de... checked).

## Verdict: PASS (small notes below, none blocking)

## Code (diff against 5898c190)
- One sealed block, section 27 `const SND = (() => { ... })()`, plus one hoisted wrapper `function sndFx` (a second
  global name, unique in the file; fine, but the brief said only SND). No `R()` anywhere: every random is Math.random.
- Draws nothing: no DOM, no three.js. The only screen change is the Settings rows (Sound On/Off, Volume) through the
  device's own blocks.
- Save untouched: preferences in their own key `starship-cadet-sound` ({ on, vol }), never written under ?nosave.
- Silent in checks: no AudioContext unless allowed (`?sound`, or not webdriver/?mute/?nosave); before that, S.frame
  returns at once and S.fx only logs (with ?soundlog).
- Hook lines outside the block: SND.frame(run) in loop(); Settings act and view; sndFx in finishJob,
  deviceNotify('jobs') and deviceLockedTap. All read-only; nothing in SND changes ship state or time.
- Doors: open fires when a door's openness rises past 0.04, close when it falls past 0.96; lift doors skipped; a
  WeakMap per door object, so a deck change can't make a burst (checked).
- Settings view calls SND.settingsBlocks() (a const near the end of the file): safe because the device only draws an
  app when opened, after load (device_check OK); keep it that way.

## Checks
- check_fast: QUICK CHECK OK.
- cadet_test 5898c190 vs s.5 (alone): ALL IDENTICAL.
- sound_check: SOUND CHECK OK.
- My probe with real frames (?nosave&debug&sound&soundlog, plans/rv16/sound_probe.py):
  - a context starts on a real click and runs;
  - Deck 3 at lunch, 1200 frames: 58 crew door events, never the same door open-open or close-close (no double fires);
  - deck change: no sounds at all;
  - a real lift ride: liftPress, liftDoorsClose, liftRide, liftArrive, each exactly once;
  - pause: suspended, resume: running; Sound Off: suspended, SND.fx returns false, key not written under ?nosave;
  - no page errors.

## Notes for SD1 (priority next, none blocking)
1. The lift has no doors-opening sound at the end: liftArrive (clunk, settle, chime) plays, but liftDoorsOpen is
   registered and never called (the plan has the doors open after the chime). One line in the ride watcher at
   r.t >= RIDE.light (or after liftArrive's return time) would do it, or say it's left out on purpose.
2. Phones (iPhone): a context can start "suspended", or become "interrupted" after a call or a hidden tab, and Safari
   only lets it resume inside a tap. S.frame resumes outside one. Suggest the gesture handler also does
   `if (ctx && ctx.state !== 'running' && S.prefs.on) ctx.resume()`. Cheap, and it saves "the sound stopped and never
   came back" reports.
3. sound_check's door and lift parts check a sound is there but not that it's there once: add "doorOpen exactly once,
   doorClose exactly once" for the hand-driven door, and an exact list for the lift. The plan asks for it, and it's what
   catches a double fire later.
4. Footsteps play during any scripted move of the player that isn't an activity (the plan says none in a scripted
   move). Probably rare; leave it unless the listening pass hears it.

## Re-check: s.6 66cee7e4 and s.7 6cea352d (game sha256 a8c32381...): PASS
- s.6: SND.actTick / SND.musicTick, called once a second inside S.frame while sound runs (only after the context is
  running, so never in checks). cadet_test 5898c190 vs s.6 alone: ALL IDENTICAL.
- s.7 takes notes 1-3: liftDoorsOpen once at r.t >= RIDE.light + 0.05; the tap handler also resumes a stopped context
  (not while hidden); sound_check requires the door's open and close once each and the exact five-sound lift list.
  Note 4 left for the listening pass.
- cadet_test 5898c190 vs s.7 alone: ALL IDENTICAL (renderer noise only). sound_check: OK. Real-frame probe: no door
  fired twice in a row, no burst on a deck change, lift = liftPress, liftDoorsClose, liftRide, liftArrive,
  liftDoorsOpen (once each), no page errors.
- player_check's 3 FAILs (the reserved job's bracket at the Lathe) are old: the same 3 lines fail on plain 0.92.6
  5898c190 (run side by side with s.6). Worth a backlog row if it isn't on the known-old list.
