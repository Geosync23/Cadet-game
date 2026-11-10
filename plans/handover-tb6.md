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

---

# Handover, part 2: piece C of 0.99.91, drills as traditions (TB6, 2026-11-10, for lead 51)

TB6 is near its memory limit (about 55-60%), so this is the plan for a fresh builder. Lead 51:
session_01GKuymjp49y3M5hgRLecobm; patch page plans/patch-09991.md on claude/lead-51. Branch claude/p9991-drills from main
bfbcbdf (0.99.9, game 583d99ba...bd16). Switch to add: `TB9991_DRILL_ON` (section 13, next to TRAD997_ON;
`false || URL_FLAGS.has('drill9991')`), off = cadet_test ALL IDENTICAL vs 0.99.9.

The user's words: "All the drills at work dont make sense. let's make them like ship traditions. just click on the cheif
and the event starts. the event is just the cheif talking about the relevant drill and danger. simple."

## What exists (section 24c, after the inspection; and 24-m19)
- Junior drill, row m3d: `drillDue(d)` (junior, Wednesday, on shift, row open), `drillKind(d)` (fire / pressure / power
  by week from Day 3). The 'drill' side job (`jobKindAdd('drill', ...)`, posted at 14:00's hour, found 14:50, claimed
  for you): `drillStops(kind)` on DECKS[5].drill places (5-drill-ext, -hatch, -door, -breaker); the extinguisher prop
  (`drillExtShow`, HOLDS extinguisher); `drillGoal` arrows; the WORK_TICK at 14:50 (toast, arrow, first-time worksBrief)
  and 15:15 (`drillClose`: all-clear toast, Calder's fast/ok/slow line, `worksUse('m3d')`, `simNote('drill')`).
  `drillCalendar` (Calendar line), the Friday tea line after a fast drill (DRILL_TEA tick).
- Senior drill, m19 'pwrdrill' (Senior Officer and up): `pdrillDue`, `pdrillCalls` (pick three calls in order),
  PDRILL_ANS (Zeke, Halloran, Calder answer), `pdrillClose` (worksSideXp).
- The crew: section 14's shape.drill (900): off-duty crew muster 15 min at their lift lobby. Leave it.
- Muster places already there: 5-muster-1..6 (Works bay, room w, row 4, facing north).

## The plan sent to lead 51 (build on it unless the lead says otherwise)
- Switch on: neither side job is posted (an early return in both `post` functions), so no stops, no stopwatch.
- 14:50: the toast stays ("Drill at 15:00: the fire drill. Muster at the Works bay."), arrow to Calder (a crew goal).
- 15:00-15:15: Calder held at 5-muster-3 (crewHold, runtime only, as TB6's lab997Frame / spiceFrame995 hold), the
  tradition star over her and "Tap Chief Calder to join the drill"; Zeke and Halloran held at 5-muster-2 and -4.
  Easiest: a small one-off joinable entry, or a direct tap hook (tapCrew -> a `drill9991Tap(a)` before tradJoinTap)
  plus the marker; reuse TB6's `t997Card(e, hid, M, go)` shape (script id 't932.join' so join_check's card handling knows it).
- The card: ~6 Calder lines for the week's kind (what the drill is, the danger, what you do), one question with three
  answers and her replies, a closing line; one line from Zeke (fire) or Halloran (pressure). Then you stand at the
  muster line to 15:15. Stand-in words under drill9991.<kind>.* (a writer replaces).
- Kept (you tapped): `worksUse('m3d')` as before (senior: `worksSideXp(1, 'pwrdrill')`), `simNote('drill', { kind, you: true, mins: 0 })`
  so the Friday tea line still fires (it reads `drillTimeWord(mins)`: mins 0 = 'fast'; say "good turnout" if you reword).
  15:15: the all-clear toast; holds released.
- Checks: mech_check's m3d / m19 drill parts and fx3 (briefing) expect the side jobs: make them follow the switch.
  Run day_check on a Wednesday (Day 3), interactions, career/promo checks, devmode/dev_arrow, check_fast; probe the
  three kinds (Days 3, 10, 17) at phone size.

## Gotchas from TB6's work
- A probe file named inspect.py shadows Python's module: don't.
- Harness probes run with the intro off; for Day 3 (the first drill, in week 1) also run once with the intro on
  (plans/tb6-probes/spice_fresh.py shows how: intro_check's paper run to the day).
- Moving or adding a planned thing reshuffles the planner's shared places for that whole day (cadet_test crew drift on
  that day is expected; prove it by undoing just that change). Holds (crewHold) don't touch the planner.
