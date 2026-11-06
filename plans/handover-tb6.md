# Handover: TB6, hosted traditions (0.99.7 playtest patch)

Role: build notes 18, 43, 50, 51, 52 of plans/patch-0997.md (on claude/lead-49; the user's words there). Lead: lead 49
(session_01GKuymjjreuZtZeDMBX79xn). Reviewer: RV33 (session_01GKuymoAK9gACR31MRd1CMX). SC1 (social, note 39):
session_01GKuymk1xmJCgzW4Ee8Drz8. Build master: BM25 (claude/staging-0997).

## Branch and builds
- Branch claude/p997-traditions, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8).
- Batch A: 53bf2ce, game 84d3f8f164fd7a6a26227bdecf30491cf4ad7f44ca55ddeac7b03ccc03504447. RV33 PASS (2026-11-06 09:50 UTC).
- Batch B (RV33's "should"): Open lab's talk, see below. Commit and sha256 in the build table row "p997-traditions B".
- One switch: `TRAD997_ON` (section 13, after TRAD995_ON; `false || URL_FLAGS.has('trad997')`, `?trad997` previews).
  Off: cadet_test vs 0.99.6 ALL IDENTICAL. Build-number lines untouched.

## What's built (DEV_NOTES "Hosted traditions"; design-doc has each, with two open questions for the user)
- 50 Open lab: Sato hosts (held at 2-open-lab-2), her card (t997Card, script id t932.join), you at the island,
  lab997Say: every third bubble Sato's (LAB997_SATO, 10), the crowd's every other turn quiet, the crowd round its 12 lines
  (3 `here` + LAB997_CROWD 9) before any repeats; her wrap line.
- 51 Spice shelf supper: Tuesday 19:15-20:00, not a meal (at load: at, meal, galley tie). Cause of "doesn't work": on a
  fresh save the first one (Day 2 18:15) sat under the call-home meeting (d2-booths 18:00-19:00) and Zeke's knitting
  (d2-knit, from 18:30); harness probes ran with the intro off. Brennan's card, then a seat with tasting plates.
- 52 Teach me your thing: per teacher pose (TEACH997), four coaching bubbles, a result toast and flag teach997.<hobby>.
- 18 Inspection: insp997Moment (walker held at your bunk's 4-inspect-<room>, three checks, verdict, notice); the Mail
  starts "Passed." / "Not passed this week." No penalty (open question for the user).
- 43 Bread day: the loaf (LOAF997_DISH in SHIP.player.tray, trayGo), PROP_KIT.loaf / HOLDS.loaf in 8b, LOAF997_ON on the
  table while you eat it (trayOnTable hook). Not saved.

## Shared lines touched outside my block (owners review)
tradJoin (t997Join line), eventsTick (t997Frame), 24c inspectWalkDo and inspectRun, section 15's hold line and
trayOnTable, 8b after HOLDS.slice. Section 13: the switch line.

## Agreed with others
- SC1 (note 39): +4 friendship for the host at the tradition's end when you joined, from the simNote('tradition') bus
  (ev.host); appointments (appt-*) left out, so Teach me isn't doubled. Nothing to call from my side.
- Merge (RV33's test merge with CL1 5c93e8c, EV1 dad2b9b, GM1 9175156): only one-line neighbour conflicts in the switch
  lines, tradJoin and eventsTick; keep all lines, mine after GM1's.

## Found, not mine
- EV1-1 (a seated host stands for the rest of a tradition after your tap): section 10's crewWayOn keeps your seat's walk
  tile clear while you sit; the bow window sofa puts 3-lounge-25 and -26 on one open tile. Suggested to the lead:
  `ps && ps.onTile && ps.pose !== 'sit' && ps.walk`. Repro: plans/tb6-probes/seated_tap.py BUILD reading-corner walsh-esme 3 L.

## How to test (plans/tb6-probes/, each switches a copy on itself; give it the plain build)
spice_fresh.py (ON=1 END=1215 [INTRO=1: a fresh save, the intro run on paper to the day] BUILD 2 1160), hosted.py
(BUILD open-lab 9 2 L sato 1040 1060 1112), teach.py, bunk_inspection.py (not inspect.py: that name shadows Python's
module), bread.py (SHOT=1 for screenshots). Gotcha: a long background run can be cut off when the session's processes
stop; check the logs end with the check's OK line.

## Open questions for the user (in design-doc's Open questions)
- Should not passing the inspection cost anything (default: no)?
- The supper's new time, Tuesday 19:15-20:00 (default).
- Words are stand-ins under t997.*, teach997.*, inspect997.* for a writer.
