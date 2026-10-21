# Turn reviews: PR6

Turn reviewer 6, from 2026-10-21 ~10:00 UTC; takes over from PR4 (plans/handover-reviewer-4.md, claude/review-4 539a2fb).
Reports to lead 23 (session_01XXiKm9iPgm565SZ4n1knmU). Overnight mode: questions to the lead, never the user. Pushes only to claude/review-6.
Stands in for owners 4d (props) and 8b (performance); PB reviews 13, 14 and 10.

Queue:
1. Crossing the Line turns L1-L6 from EV5 (session_012DBTAAiTTNJYugQL4YLScJ, claude/line-update). Plan: claude/event-plan-line ee590ed; its review: claude/event-plan-review-2 plans/event-line-plan-review.md.
2. The storm leftovers PR4 hands over (EV4 session_01MqpjPG6mDFe5avrDxcNWTU, claude/storm-update; ER2 does the build reviews).

Method (PR3/PR4's): section.py --diff; build lines untouched; cadet_test off against the turn's base (ALL IDENTICAL); check_fast alone;
the area's checks off and on (events, bigevents, day_check on the event days, lines, bubble, food if meals move); a live probe on a real
save at 390x844 and 360 wide, with reloads; mutants planted to prove the checks catch them; draw calls under 450. One browser check at a time.

Setup: `pip install playwright`; three and acorn in /tmp/cadet-work (npm pack three@0.128.0, acorn@8.12.1); probes load plans/review-6/pp.py.

## EV2 storm S8 (claude/storm-s4s8 5cb698a, base af568f9): PASS
- From PR4: cadet_test off ALL IDENTICAL; check_fast OK; code read OK.
- PR6 `s8_banner.py` on an on-copy, a real save Day 12 13:55 (evFrom 0): at 14:00 the Captain's banner (#devAddr) runs
  from y 206 (390x844: to 423; 360x780: to 447), below the Device/pause buttons (bottom 116) and Tracked (bottom 198). No page errors.
  Shots `plans/review-6/shots/s8_banner_390.png`, `_360.png`: readable, nothing covered.
- Nit (PR4's): the top is set once, when the banner shows; no re-layout on rotation.

## Storm head adb71aa (f32d901 + 2228a05), base 74c216e
- cadet_test 74c216e→adb71aa off: ALL IDENTICAL.
- check_fast on adb71aa: QUICK CHECK OK in 237 s.
- events_check on: EVENTS CHECK OK. day_check on, Days 13 and 14: DAY CHECK OK both.
- PR4's fix 1 (`lap_d15.py`, on-copy): the Monday Day 15 Lap of the Wren is in eventsOn(15) at 20:30, TRAD_JOIN and
  joinable:true (inTraditions:false there is the raw identity test on the dressed copy, expected; evIsTrad is what the game uses).
- PR4's fix 3 (food_check on, 11 4): no Day 11-14 FAIL; the Day 14 dinner wait is gone (carts wait 2 that day).
  Only Days 28 and 31 fail, as on S1 (known).
- Props (`props_probe.py`, on-copy, Day 13 18:23 in the mess): 56 in the mess, Brennan in, Lukas out; FEEL_S.lamp .85;
  lanternMess on; at most 220 draw calls. Shot `shots/props_supper.png`: lanterns on the long tables, full supper, readable.
  The mess-only dimming (lead 23's call) is not pushed yet: re-check FEEL_S.lamp outside the mess when it lands.
- EC1's 037a149 on its own branch: BIGEVENTS CHECK OK.
- Gotcha (PR6): bigevents_check finds cadet_test.py from its own file name; a renamed copy dies with a SyntaxError.
  Keep copies as `<dir>/bigevents_check.py` next to a cadet_test.py.
