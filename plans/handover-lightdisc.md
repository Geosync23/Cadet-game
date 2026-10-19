# Handover: Lightdisc engineer (and the rec deck's owner after DA6)

Session: session_013LcEsgjMTDMMeiACKLj2bB. Lead: lead 14 (session_01RHtJv7GJDi4qosgU8Gb2b8). Never contact the user or start sessions.

## Branch and builds
- `claude/lightdisc-proto` (this session may push only here). It holds the prototype page and the rec deck build.
- `lightdisc-proto.html` (ba6b4ac): the standalone prototype the user approved. Its check is `tools/lightdisc_proto_check.js` (Node Playwright).
- Game builds 0.82.0 to 0.82.5 sit on DA6's rec deck (`claude/recdeck-build`, merged up to 0.80.10 842b64d). See the DEV_NOTES build table rows 0.82.x.
- DA6 (the rec deck architect, session_01WUAfx9EuiZa71hJcWp4VSz) handed the rec deck over at 0.80.10. Their note is `plans/handover-recdeck-architect.md`, and its map of the deck code still holds.

## What I own and built
- **Section 23b, LIGHTDISC** (after 23 Tiles):
  - The rules are pure: `ldNew`, `ldStep`, `ldPaper`, `ldClone`. The stream is plain state in `g.rs`. There is no DOM, no R() and no Math.random. Fixed 60 Hz.
  - Seeds: schedU key 830 picks a game's seed; 831 picks a level for crew with no personality (35/40/25); 832 adds variety when choosing an opponent.
  - Tuning (0.82.2, the user's call for shorter games): `LD_UP` 1.1, `LD_CAP` 13.5, misjudging `2.6 *` the speed.
- **The flow:**
  - `discAsk` (taps on 'Lightdisc court' and 'Ask someone to play' in recTap) → `discFind` (anyone off or at leisure ship-wide, 06:00-21:30).
  - `crewComeTo` brings them to `7-disc-2`; you get the `disc` activity on `7-disc-1`.
  - `discTick`, then `discBegin`, and at the end `discOver` (record, social, leisure, fitness +10, energy -3, news for beating Rina).
  - `discEnd(again)` handles Again, Quick game, Done and Leave.
- **The view:**
  - `discViewOn` / `discViewOff` / `discFrame`, called from the main loop before the render.
  - The perspective `DISC.cam` replaces the flat camera while a game is on. `discFit` fits it as the prototype does. It eases in as a dolly-zoom.
  - The overlay is `#ld`. `body.ld-on` hides the HUD, toasts and tips.
  - `PAUSE.disc` freezes the clock for the game and its result.
- **The players:**
  - `discPose(rig, a, T)` gives the ready stance, side steps, forehand and backhand, and the fist pump.
  - You are drawn by the activity's stand-in `ACT.body`; section 15 hides `player.obj` during activities. That was the cause of "the characters stay still".
  - The opponent is a `FullPerson` made for the game. Their crowd body is hidden meanwhile.
- **The scoreboard:** `REC_BOARD.tex` is set in `WALL_KIT.recScoreboard`; `discBoard` redraws it.
- **Saved:** `SHIP.disc` (`discLoad` reads it defensively, so older saves load).
- **The rec deck, 0.82.5 (the user's notes):**
  - the REC DEC gantry sits east of the lift
  - the signpost's boards sit off the post's face
  - fitness from the activities (`also.fitness`)
  - walking into the float room starts floating (`recRoomIn`, from the main loop's room change)
  - one water material (`RK.poolWater`, opaque); the fast river adds only its foam

## How to test
- Python Playwright: `pip install playwright numpy pillow`.
- three.js: `npm pack three@0.128.0` into `/tmp/cadet-work/three` (DEV_NOTES "Testing").
- Environment: `CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work`.
- `disc_check.py BUILD [GAMES]` covers:
  - rules, balance and save
  - the ask-and-play flow and the frozen clock
  - draw calls (under 200; about 129 now)
  - frame-rate equality: a live game at 60, 30 and 20 fps, copied with `ldClone`, matches the same game on paper
- `cadet_test.py OLD NEW` against fe1d705: Decks 1-6 must be ALL IDENTICAL.
- Also run `deck_check`, `player_check` and `interactions_check`.
- Probe pattern: reuse cadet_test's `Game`; `skipTo(... 19*60)`; `goToDeck(7, null)`; `discAsk()`; step until `DISC.g`; `DISC.g.p[0].ai = LD_LEVEL.sharp` gives you the autopilot.

## Gotchas
- Don't put a `//` comment in the middle of a line you're replacing. It swallowed the rest of a line once (a549b48 didn't load; fixed in 5aa4310).
- Kill test runs with `pkill -f "[n]ame"`. A bare pattern matches the shell running the pkill and kills it (exit 144).
- The container can restart and lose background runs. Rerun them.

## Open / for later
- Crew v crew games on the court (Winner Stays On) and pick-up games need the crew's habits (R7). `ldPaper` is ready for off-screen results.
- Lightdisc chat lines: `LD_TALK` holds stand-ins until the writers' `disc.<kind>` lines arrive.
- Held sideways (landscape), the game view is a little far.
- The court's gate leaves stay as DA6 left them.
