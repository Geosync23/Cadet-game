# AR1's play tools (2026-10-22)

Used for plans/arrows-pillar5-plan.html. They play build 0.64.15 in Chromium the way a player would and log what the
player is told (toasts, Mail, tips, the arrow's label, the training state, the board, your job). Not checks: no PASS/FAIL.
Setup as DEV_NOTES "Testing" (playwright, three r128 in /tmp/cadet-work/three, Chromium at /opt/pw-browsers/chromium).

- harness.py: class G boots the game in Dev mode (#dev), signs the manifest, installs the logger; g.run_min(m, hook)
  runs the real game loop until the ship clock has moved m minutes (the game caps a frame's time step, so it counts
  by the clock); g.ev(js) runs inside the game's scope; g.shot(path).
- bot.py DAY: Dev mode's Set career to the end of DAY-1, then plays DAY with a follow-the-arrow bot that cheats
  (teleports, does job steps on paper). Use it for the order of events only.
- shift.py DAY [shift|none] [minutes]: an honest tracked shift: goes where the arrow points and taps the thing it
  points at, presses the clock screen's and the board's own buttons. Env START=minute of day (default 450 = 07:30),
  CLOCKIN=1 clocks in first. It sets SHIP.player.track to a stale id first, as in a real game (Dev mode's Set career
  switches tracking off, which hides arrows a real player would see, and shows ones a real player wouldn't).
Note: Dev mode's clock skip marks skipped workdays as excused (careerOff), so an afternoon reached by skipping may
behave as a day off (no clock-in, no logbook).
