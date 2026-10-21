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
