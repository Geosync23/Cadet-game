# Handover: FX20 (builder), 2026-10-26

Written at about 58% memory, as agreed with lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX). A fresh seat can pick up from here.

## Current job: the bunk inspection walked for real (0.93.2)

The user: "Bunk inspection doesn't do anything. A supervisor should come by." Branch `claude/inspection`, from `claude/integration` b957b92d (0.93.1). HUD `0.93.2-i.N` (i.2 now). Reviewer RV18 (session_01PMfvrCN6StPzwVSPGX7ijH). Words: SW2 (session_017dLaLFBnRUQin3PQEQq6so), CS1 checks.

### What's built (all behind `var INSPECT_ON = false`, defined beside the inspection places in section 4's Deck 4 data, so the planner sees it)
- `inspectWalker(d)`: from the calendar only (the planner may not read live state): Calder in week 1 (Day 4 is the first inspection Thursday; the m3i row's fixed day is 4) if she's on shift, else an officer/senior/chief on a day shift that day, by the week's rota (schedU(864, week, 864)).
- Section 4 data: with the switch on, a stand spot per junior bunk, `<bed>-stand` (event places, the tile in front of the bunk, two per tile offset ±.22).
- Section 14 (planner):
  - schedFrame: on inspection Thursdays the walker wakes by 05:30, the day-shift juniors 05:30-06:00 (spread).
  - morning(): the walker goes to Deck 4 and straight to `4-inspect-a`, then a..h, `INSPECT_STEP` (3) minutes each from 06:30 (tag `inspect`, anim `look`; `inspect` added to `STOPS` so it never stretches). A junior stands at their stand spot until `inspectPass(room)` + 1. If that's within 30 minutes they stand first and wash after (`stood`). Otherwise there's the old 10-minute tidy.
- Section 24c: `inspectOfficer` returns the walker when on. `inspectWalkerAt(d)` gives the room the walker is in (heading to its door spot). `inspectWalkTick` says the words:
  - the arrival line in your room, then your result in person (inspectRun(d, true), 2.6 s later);
  - a line per other room while you're in it;
  - a heads-up toast if they reach your room and you're elsewhere;
  - a "done" toast after Bunk 8.
  The 07:00 Mail is as before.
- Words, placeholders now (worksText keys, variant by week): `inspect.walk.arrive`, `inspect.walk.room.b`..`h`, `inspect.walk.away`, `inspect.walk.done`. SW2 is writing `content/works/inspect-walk.lines`: bake it with `python3 content_gen.py`, then `content_gen.py --check`.
- `day_check.py`: on an inspection morning with the switch on (run on a switched-on copy), the walk in order a..h between 06:25 and 07:00, at least 25 juniors standing, and no stand spot used twice.

### Measured
- Day 4 walker Calder, Day 11 Dahl Mira; route 06:29-06:54. 30 of 55 juniors stand: the night shift's Bunk 8 sleeps (by design), and some juniors are already at early work stints.
- Live (scratch probe): Calder in Bunk 1 by 06:30; "Morning. Let's see." then the result in person (simNote here: true); Tomas's training as before.

### Checks to finish (running at handover, commit 707aec47)
- check_fast; cadet_test switched off vs b957b92d (must be ALL IDENTICAL).
- On a switched-on copy (`sed 's/^var INSPECT_ON = false;/var INSPECT_ON = true;/'`): day_check 4 and 11, player_check (3 known reserved-job FAILs exist on 0.92.6 too: compare), interactions_check.
- Then push, and send the sha to lead 37 and RV18 (and SW2's words when they land).

### Loose ends / ideas
- The juniors stand facing out of their bunk; their pose is `stand` (no salute anim exists).
- `inspect.walk.done` fires 4 s after the walker enters Bunk 8 while you're on Deck 4.
- A design-doc line (Thursday inspection: now walked by the duty officer) goes in with the switch-on decision.

## Earlier work (done, reviewed)
- 0.92.6 item 10, odd jobs (`ODD_ON`, claude/p926-fx20, RV15 PASS).
- 0.93.0 activity sounds (claude/sound-act 7e63f194, RV17 PASS). plans/sound/audio-todo.md lists what's left for the listening pass (dryer, airlock, shuttle bay).

## Gotchas
- In section 27 (sound) the core's `S.actTick = null` and `S.whenReady` come after the activity slot. Install from `S.onFrame` once.
- Use `pgrep -f "[n]ame"` in wait loops, or the loop matches itself.
- Each parallel check needs its own CADET_WORK with `three` and `acorn` links.
