# Handover: TB7 (traditions builder 7)

**Status (2026-11-11):** stood down by BM28 after 0.99.91 was published (main = claude/integration = cdd9efd). Nothing open.

## Role and branch
- TB7, briefed by lead 51 (session_01GKuymjp49y3M5hgRLecobm). Built piece C of `plans/patch-09991.md` on `claude/p9991-drills` (from main bfbcbdf; game commit 387d3541, head 3cef60e9), merged by BM28 into 0.99.91.
- Predecessor's note: `plans/handover-tb6.md` part 2.

## What was built: the Wednesday drill as a tradition
- The user (2026-11-10): "just click on the cheif and the event starts. the event is just the cheif talking about the relevant drill and danger. simple." TB6's plan, without the question and answers.
- Switch `TB9991_DRILL_ON` (section 13, preview `?drill9991`). With it off the game is identical to 0.99.9.
- With it on:
  - neither drill side job is posted ('drill' in 24c, 'pwrdrill' in 24v);
  - 14:50 Calder's toast and a direct arrow (setGoal, `drill: 'drill9991:<day>'`) to the muster line;
  - from 14:55 Calder is held at 5-muster-3; Zeke and Halloran walk in by lift (crewComeTo) to -2 and -4;
  - from 15:00 a star over Calder and the arrow on her (crew + tj);
  - a tap is the turnout. A Junior gets simNote('drill') and worksUse('m3d'); a Senior gets simNote('pwrDrill') and worksSideXp;
  - then her card `drill9991.talk` (six lines; Zeke's line for fire, Halloran's for pressure, her close), then a direct arrow to a free muster spot until 15:15;
  - 15:15 the all-clear, the holds let go; missed: the note with you: false and her word;
  - the Friday tea line says turnout.
- Code: section 24c, below the drill tea (DRILL9991_TALK, drill9991Frame, drill9991Tap, drill9991Card, drill9991Stand, drill9991GoalOff). Hooks: tradJoinTap, eventsTick, and tradJoinMinute (section 18, `&& !g.drill`, checked by its owner via RV35). Also the Dev career arrow (section 25).
- Words: `content/works/drill9991.lines` (stand-ins; bake with content_gen.py).

## Gotchas
- Arrows must be direct (setGoal), not guideAsk. Queue entries leave the arrow slot free for the needs arrow (fresh_walk stuck at Food), and the arrow checks run with the queue off.
- In probes, don't name a variable HOOK (it overrides the harness). Use shipNow(), not SHIP.time.min.
- join_check's reload step can flake while many checks run at once; rerun it on its own.

## How to test
- `plans/tb7-probes/drill.py` on a switched-on copy (Days 3, 10, 17; MISS=1 for a missed drill; SHOT=1 for phone screenshots).
- mech_check (m3d, m19, fx3 follow the switch), arrows_check week, arrows_d_check, fresh_walk to Day 3 16:30.

## Loose ends
- Backlog TB7-1: the Food arrow can point at a closed servery (old, section 15's).
- The drill's words are stand-ins, waiting for the user's own.
- Switching TB9991_DRILL_ON on is the lead's and the user's call.
