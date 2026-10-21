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
- EC1's check 037a149 on adb71aa: BIGEVENTS CHECK OK. 541ae52 on adb71aa and on EC1's own branch: OK.
- The party live (`party_probe.py`, on-copy, Day 14 19:20-19:56 in the bow lounge, 390x844): 25-35 in the lounge
  (the check's "at most 27 at once" counts the party's own goers; the live count adds the bar's staff and people
  passing), 241 draw calls at the default zoom, 325 at ZOOM_MIN 0.7 (EV4 measured 416 at a wider view; under 450).
  Shot `shots/party_390.png`.
- Mutants (037a149's check on adb71aa copies):
  - p1 party who .7 → 1: FAIL "party: a crowd of 80, over 60". Caught.
  - p3 supper .73 → .95: FAIL 74 over 60, 74 for 70 places, too few standing. Caught.
  - isTrad back to includes(): FAIL "the planted book-circle was not caught". Caught.
  - p2 party.stay [110, 120]: OK, not caught, and rightly so. Since 481a5b4a the party has 94 places (standing counts),
    so 45 goers staying all evening never fill it. Replaced by p4 (seats only plus stay [110, 120]): queued.

## EV4 storm adb71aa (f32d901 + 2228a05): PASS (the framed-menu shots follow)
Everything above. PR4's three S3-S7 fixes hold (Lap joinable, crowds by lead 23's rule per EC1's check, Day 14 dinner).

## EV4 storm ab58e7b (5f3fc3f ER2's fixes 3-4, f9eeb72 mess-only light + menu nit, 4311ffe Fridays merge, 2ec6f17/b9256d19 S2): PASS
- cadet_test off: 4311ffe→ab58e7b ALL IDENTICAL; adb71aa→5f3fc3f ALL IDENTICAL. 892af70/582cd21: comment and note only.
- check_fast OK in 245 s. events_check on (storm) OK; on (storm + SHORT_FRIDAY) OK. day_check 12 (storm + Fridays) OK, 13 OK.
  bigevents 541ae52 and a54ff25 on ab58e7b: OK.
- Code read: evDoubleExcept (pure: evAt at 16:00 of the day, the rule's except by id and event day); eventPlan and
  gatherings mark the address a meet break (act work); stayIn off 15:30-17:00 on the Friday (evRuleOff). Section 14's
  one line is PB's. stormSupperDim: the mess hall ('M') only; the galley keeps its light (EV4: intended, "the kitchen
  still running"; accepted).
- `s2_probe.py` (storm + Fridays on, a real save Day 12 15:00, 390x844):
  - whereIs: Marrow on the bridge to 15:25, sets off 15:30, at 7-lectern-2 15:35-16:50, back on the bridge 16:55;
    Vance on the bridge to 15:40, sets off 15:45, at 7-lectern-1 15:50-16:50, back 16:55. 53 planned at the address at 16:05.
  - live in the auditorium 16:01-16:19: 51-52 there, Marrow and Vance both, 145 draw calls. Shot `shots/s2_address.png`.
  - after a save and reload at 16:19 the plans are the same.
  - the supper's light, Day 13 18:27: mess .74 (still easing up), promenade .03, mess again .81. Mess-only, as decided.
    (The probe printed CHECK only because my threshold .8 caught the lamp mid-ease; no errors.)
