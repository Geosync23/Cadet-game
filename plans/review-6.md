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
- Framed menu (`menu_probe.py`, Day 21 09:00 on Deck 4, the trace planted, 390 and 360): on-copy, framedMenu shown, 157
  calls, kept through a save and reload; off copy, never shown (155 calls). Shot `shots/menu_on_390.png` is from the
  bunk room's door (the frame is small at that distance; EV4's own shots are close-ups).

## EC1 bigevents_check turns 9-13 (ac32382, e3f1da9, 037a149, 541ae52, a54ff25): PASS
- OK on EC1's own branch (037a149, 541ae52) and on the storm heads adb71aa and ab58e7b (037a149, 541ae52, a54ff25).
- Mutants: p1 party who 1 → "crowd of 80, over 60"; p3 supper .95 → over 60, over places; isTrad by identity → "the
  planted book-circle was not caught"; p4 the party on its 34 seats with stay [110, 120] → "36 there at once (19:07)
  for 34 places"; g30 a Captain's beat 30 minutes off the party → "guard: gathering party ... meets ['mutCap']". All caught.
  g10 (10 minutes off) is excused by the 15-minute rule, as designed; only "two of the Captain's scenes on Day 14" fails.
  p2 (stay [110, 120] with 94 places) is rightly OK.
- Note: the 15-minute excuse is any Captain's beat, not the gathering's own (the meetings' rule too).
- Gap (for the Line, not these turns): nothing checks that Saruth stays away from the Line ceremony (the Line plan says
  bigevents_check does); a mutant is queued with L2.

## DB2's section 18 hook (claude/devmode-2 d2612749, one line in eventsOn): OK (section 18 stand-in)
- After evBudget, before EV_DAYS.set; DEVMODE declared at ~9004 (before eventsOn's first run); section 25's helpers are
  function declarations; without #dev, one false test. Ends capped at 23:30 (DM_LATEST on from + len).
- Nit sent: a Dev start uses the plain SHIP_TRADITIONS entry, not that day's dressed copy (evTable), so on a dressed
  day outside eventDay (the storm's Monday Lap) it would replace the dressed version.

## EV6 storm 829f242c (the lantern supper in seated sittings, the user's change): supper PASS; food_check open
- cadet_test off 582cd21→829f242c: ALL IDENTICAL. check_fast OK (239 s). day_check 13 on OK. events_check on OK
  (lanternSupper 18:00-19:45 went 51/59, places 48).
- `sit_probe.py` (on-copy, Day 13 from 17:40, 390x844): the mess 5→48 at most (18:52), 45 at 18:59; trays held
  standing 0 throughout; 199-236 calls; lamp .85; Brennan in, Lukas out. Code read: standing diners gone (trayTo plain
  again; day_check's standMeal allowance gone), `seated` keeps eventPools off the crowd spots, stay [45, 60].
- bigevents 3f9a458: FAILs only the old "mess over 44 needs standing places" rule, dropped in EC1's ef9d7fc/12901c9.
- food_check on (11 4): FAILs dinner waits on Days 12 (43), 14 (26), 15, 17 (43), 20, 21 (26), 24 (46), 25, 27, 28,
  31 (51), 32 and the carts and chiller weeks. adb71aa failed only 28 and 31. EV6 saw the same list on 582cd21, so it
  started before this change. Bisect running: 582cd21, 4311ffe (the Fridays merge), ab58e7b.
  (ab58e7b's PASS above did not include a food_check; my miss.)

## EV5 Crossing the Line L1-L3 (5c3c003, 94254b4/9188428): findings so far
- cadet_test off: 347c573→5c3c003 ALL IDENTICAL; b071f0e→9188428 ALL IDENTICAL.
- events_check on: OK. day_check on, Days 6 and 7: OK.
- `line_probe.py` (on-copy, a real save Day 7 14:10, evFrom 0, 390x844):
  - paper: nobody but the ceremony in the bow lounge 14:35-15:10 (PB's evClosed find doesn't show on Day 7);
    Saruth at 3-tend-16, never at the ceremony; the 10 front spots all first-timers; the four lead spots Marrow,
    Brennan, cruz-tove, walsh-esme; 39 planned at the ceremony (plan "45 or more is fine"; EV5 counted ~43).
  - live in the lounge: horn toast at 14:30, ribbons on at 14:34; crowd 4 (14:29), 6 (14:38), 13 (14:43), 37 (14:47),
    41-43 (14:52-15:01); 214-236 calls.
  - **Marrow arrives late**: walking the promenade at 14:38 (23.5, 9.5), 14:43 (31.8), 14:47 (39.8), at the glass
    (50.5, 10.5) only by 14:52-14:56. The oath is at 14:40. eventMeetPlan gives a named cast 5 minutes' early start:
    she leaves her quarters at 14:35. The crowd arrives 14:43-14:52 too.
  - reload at 15:02: 43 still there, the event on (the panel's state not read by my probe: untested).
  - ribbons gone by 16:05. Line supper 18:26-18:44: 45-47 in the mess, 219 calls, pudding apple crumble.
  - plaque on at 19:41 (calls 237), gold fading (.21). Certificate: trace 'lineCertificate' saved, but not shown on
    Deck 4 thirty steps after goToDeck(4): re-checking (may be my probe's timing).
- food_check bisect (off, 11 4; "bad" = more than the 2 old busy days): 5f3fc3f on = baseline; 4311ffe on/off, the
  Fridays branch 7a0e5f7 on/off = 14-15 busy days. Bisect on the Fridays branch (first-parent 675588c..7a0e5f7):
  first bad 4ee3fdc0, the merge of integration 0.64.7: its game change is LADDER_ON, MUG_ON, FLC_ON switched on.
  Handed to FD1 (session_01YJhagf6oyF6SeT5XGvrL5H, lead 24's call); PR6 stops here. Not the storm's or the supper's.
- L2/L3 9188428, the rest: day_check 8 on OK; check_fast OK (240 s); lines_check PASS (0 errors, 51 warnings).
  food_check on 6 3: only the garden FAILs (on the base too, EV5's note) and an empty "crew late meals: []".
  EC1's 3f9a458 on 9188428: OK (cast on lead-1/lead-2, 10 of 10 front first-timers, Tomas 2-watch-6, supper 55
  meaning to go, at most 45 at once, 70 places). Mutant Saruth pull 1: FAIL "Saruth is at the Line's ceremony" (caught).
  Mutant the Line supper's everyone .85 → 1: no change (55 again), an inert mutant, not a check miss.
- The container restarted at about 14:25; the queued runs on 0032351 were dropped. L4/L5 is reviewed on EV7's head
  4306fd1 (L5b-L5d: PB's evClosed fix, the seated Line supper, the oath's early 25 and the crowd's lead, the story
  flags at the panel's end, jobs held to 13:45).

## EV7's Line head 4306fd1 (L5b-L5d on L1-L5; storm b991877 merged in)
- cadet_test b991877→4306fd1 off: run 1 DIFFERENCES only in a_start (13097 px: Esme Walsh's "Planted mine in a
  straight line" bubble a few pixels apart; every other shot 0); run 2 ALL IDENTICAL. A third run at the end.
- Code read (24020ef, 0aae259, 4306fd1): evClosed checks a gather closure every 10 minutes through the stay (PB's
  fix); the Line supper seated (stay [45, 60], seated, pudding: true; lineStandTray gone); the oath's cast early 25
  (eventMeetPlan reads g.early); the ceremony crowd's lead (lineLead: standing easy 10 minutes before the horn, others
  10-20 when free, hash 1190; pure); lineMoment sets its story flag in onEnd; jobs held to 13:45 (825); Brennan's offer,
  the dunking pose (looks only), the goal pointer to Tomas.
- `tomas_probe.py` (on-copy, Day 6 19:10): the moment opens at the mess (3-mess-5); saved and reloaded with the panel
  open, no story flag set, and it's offered again at the next minute. Fix confirmed (it was the L4 finding).
- The dinner waits (FD1, 15:22): FLC_ON. First Light Cocoa shifts Day 1's evenings, machine wear drifts, and by Day 11
  range-1 and oven-2 are faulty; food_check's 4-week forecasts after its Day 11 visit held that state. A check-only fix
  (fresh machines before 4b/4c/4e): claude/food-waits 0f808c3, PB-reviewed, to integration via BM12. Not the builders'.

## EV6 storm S10 ab3e2fb7 (EVENTS_ON = true): HOLD (15:40)
- The game diff is the one line; EV6's proof: the line back to false is ALL IDENTICAL to db60020a; its full round is in
  the build table (plans/storm-s10-round/ on the branch).
- Held for three FAILs new with the switch on: devmode_check "the excused days" (careerOff(8) true before the jump; OK
  off), career_check, mech m17 (off runs pending). Asked EV6 for the causes; I re-run just those three on and off.
- S10's three re-run (dc0ebe0b, on = the build, off = EVENTS_ON false): devmode_check on OK twice, off OK (EV6: the
  earlier FAIL was a random gs giving a sick Day 8, 1/28; a check fix for DB2: a fixed gs or accept it);
  career_check FAILs "Relied on before Day 5" on AND off (backlog row 12, old); mech m17 FAILs on ("the paper part
  differs after the rides": movers 14, waiting 78 in the first pass), OK off (EV6: the storm's extra wear leaves crew
  repair jobs on Day 18 in the first pass only; a check fix for its owner: crew job visits left out, or SHIP.jobs and
  the machines reset alike for both passes). **S10: PASS**, with those two check fixes owed (not the game's).
- 4306fd1, the rest: check_fast OK (237 s); events_check on OK; day_check 7 OK; interactions_check on OK; bigevents
  2de5554 OK; the Saruth mutant FAIL "Saruth is at the Line's ceremony" (caught).
- `line_probe.py` 390: Marrow at the glass (50.5, 10.2) by 14:34 and settled at lead-1 from 14:38; the lounge 20
  (14:29), 30 (14:34), 35 (14:38-14:47), 43-44 (14:52-15:01); 216-237 calls; the ceremony's thanks toast; nobody
  strays in 14:35-15:10; Saruth away; the 10 front spots first-timers; 40 planned (tag at 14:50).
  Reload at 15:02: 44 still there. Ribbons gone by 16:05. Supper 45-47 in the mess, 202 calls, apple crumble.
- `cert_probe.py`: the certificate on in Bunk 1 at 19:42 (155 calls), kept through a reload.

### Verdict: EV5/EV7's Crossing the Line L1-L5d (head 4306fd1, c9fa161): PASS WITH NOTES
1. (EV7, open) the Line supper's `who: [['everyone', .85]]` matches nobody (evDressed reads by person id): fix it or drop it.
2. (lead's call) 35 in the lounge at the oath's 14:40, 44 from 14:52, 40 planned to go; the plan said "45 or more is
   fine". EV7's own run had 42 at 14:40: within reach; not blocking.
3. The 360 probe and a third off cadet_test are still queued.
