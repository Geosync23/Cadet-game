# RV30 reviews (0.99.5 playtest patch)

RV30 session_014zyJYNFR7ewWJGvEQNUAHr, branch claude/review-rv30. Lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN). Base for every review:
claude/staging-0994 8976965e (game a01d1a4c...bc4a). Probes in plans/rv30-probes/.

## SD5 sound, claude/p995-sound d26a11a (game d785aea6...30ff, verified): FIXES NEEDED (small)

Notes 9 (suspend on hide, no switch), 4 (MESS_SCALE, off), 17 (SND_LONG, off in branch).

Passing:
- sha256 matches. Diff read: every MESS_SCALE / SND_LONG line is behind its switch; hideNow is the only unswitched change.
- cadet_test vs 8976965e, alone: ALL IDENTICAL. names_check OK. sound_check (SD5's own, whole): SOUND CHECK OK.
- Note 9, real game loop (hide_loop.py; this container's browsers never really hide a tab, tried another tab, a
  minimised window under Xvfb and a CDP freeze, so the hide is played and no frame is drawn after it): 0.99.4 keeps playing
  ("running") for all three of visibilitychange, pagehide, freeze; SD5 suspends at once for all three; back, the sound
  follows the pause (paused: stays off till Resume; pagehide/freeze: plays on).
- Note 4, MESS_SCALE on (mess_day.py, real crew Day 2, 12 times): empty and 2 people (you + one): no scene; 11 people
  level 0.52, 15: 0.66, 21: 0.86, 40-49: 1; emptied: gain to 0 then the scene goes. As designed.
- Note 17, SND_LONG (stall_real.py, real loop, mess at the rush with music, 6 stalls of 1.2 s): off: 42 late starts (worst
  1.50 s), 1604 gain moves in the past; on: 0 and 0. Music and mess still playing.

Fixes:
1. Note 9 race (hide_loop.py "race 2"): if the page hides while ctx.resume() is still in flight (Resume tapped, any tap's
   gesture() resume, then away at once), hideNow sees state 'suspended' and returns; the resume then finishes and the sound
   plays on hidden with no frames to stop it. Probe: "hidden while the resume was in flight: sound running, paused True".
   Fix: in hideNow suspend whenever ctx exists and isn't 'closed' (drop the 'running' test). Tested in this Chromium: resume()
   then suspend() at once ends 'suspended'.
2. SND_LONG music lookahead 2 s (music_x.py): at a hand-over the old track's notes already queued play on under the fade:
   now up to 2.1 s after the fade starts (0.7 s with it off). That changes the Music app's skip/off (2 s fade), every
   time-of-day / event cross-fade (pendingChange at a section end: bars past the change point are queued 2 s deep, not
   0.5) and after a sleep jump. design-doc says "It doesn't change how anything sounds". Fix suggested: never queue past a
   pending change point (tick to min(now + 2, change.at + 0.45) while a change is pending), so section-end hand-overs are
   as 0.99.4; or the lead accepts it and the design-doc line is corrected.
3. sound_check check_long can't fail on the bug: its own off run prints late starts [0, 0, 0, 0] too, so a build where
   SND_LONG did nothing would pass. Count gain moves in the past as well (stall_real.py: off 1604, on 0) and require the off
   run to show some when the build has it off.
