# Review log: RV24 (reviewer, from RV23), 2026-10-27

Lead: lead 42 (session_01GKuymjnCHnpwDqB94PVwmV). My session: session_01GKuymnJuoJTWnmYunbN7EP. Notes-only branch `claude/review-rv24`
(from claude/review-rv23). Build master BM19 (session_01GKuymncYhRTKs8t4byNfdj) merges PASSes into claude/staging-p5s6.
Cap rule: at most 5 seats working at once; read only until RV23 says it has gone idle.

## Verdicts
| Branch | Verdict | Sha |
|---|---|---|
| claude/devmode-j1 (DM1): Dev mode J1, 12 career and night jumps | PASS (1 note) | d9b7b3c |
| claude/devmode-j0 (DM1): Dev mode J0, Jump to tab, runner with Stop, Day 40, ranks | PASS | eef5b56 |
| claude/sound-r3 (SD2, SD3 now): event music turn 1, farewell song A | PASS | 64077a69, dc3014b6, a09b32b7 (mess hall) |
| claude/pad-wave-b (PB1): controller wave B, props mid-visit, every job stop, beam floor, court edge | PASS | 177793b6 |
| claude/pad-wave-a (PA1): controller wave A, landings, clock x, Dev card, X, B, Saves on Back | PASS | 818ec0b |
| claude/pad-wave-c (SD2): controller wave C, sound hook, pad words, Saves hint | PASS (should cleared in a29a0f48) | 336b00c2, a29a0f48 |
| claude/p5s6-promo4 (W8): S6-7, S6-9, MA6-2, refit, DM rows, RV24's fixes | PASS (should 1 fixed in 9063aafe) | 6f13b61a, 9063aafe |
| claude/p5s6-deck (DA6): S6-5 nights 1-2, keepsakes to room B, door fix | PASS (frames should cleared in 4a84e153) | 2df6bfce, 5c27b740, 4a84e153 |
| claude/m24-pick-pointer (AS1): night 3's pick ring | PASS | 5f649b45 |
| claude/escort-seated-check (PZ6, test only) | code read OK (glance, lead 42); run later | 775c3ca |

## W8 claude/p5s6-promo4 bd138090 (S6-7 clue by casePoint, S6-9 turn 1 Calder's question, worksEscort change); base 62a8ac0b
Code read (no runs yet):
- 28f cq*: settle 22:00 the eve of the first Friday from Day 26 for tier 4 'specialist' (weekday 0 = Monday, so 4 = Friday: right);
  notice 18:20, arrow 18:35, story from 18:40 with Calder near, 19:05 she takes a tea seat (crewComeTo) and the arrow shows the other,
  ask on sitting or after 3 min; missed: follow escort 19:30-22:00 and 10:00-21:00 later days. Saved via cqClean; Record line; DM 'cq'.
- To check live: on Day 26 the Four weeks aboard tradition (18:40-19:30) seats its crowd on the tea corner's lounge seats
  (5-tea-1, -2, -3 are the only ones), and on later Fridays Works tea does the same. Calder's crewComeTo to "her" seat and the
  arrow's "your" seat may be taken by Torres/Pell: overlap on a seat, or the player can't sit (the 3-minute fallback keeps it moving).
- worksEscort skip of p5nEscort ("mine"): doesn't check worksDay(t) === c.d like the rest of worksEscort (a stale cur from an earlier
  day would also skip it); minor.
- mtCasePoint: seeded with schedU, no R(); closed unpicked retries in 10 min; false falls back to the stand-in. Reads fine.

## DA6 claude/p5s6-deck 88377cfa + 31ad2f0e (S6-5 night 2 the reactor; night 1's arrow); base a2ef6416 (RV23 handed both over)
Code read (no runs yet):
- 28c night 2: permit card on the bridge, badge from the rack, "Going in" card on Deck 6, a side job at the reactor console, "Coming out"
  card, badge back (trained, Mail); the Watch's word if the badge isn't back 30 min after you're out. Door: m23DoorOpen in doorOpenFor
  (permit, told, badge out; once out, only while you're still inside). m23night no longer has j.machine (stops tapped like a chore's,
  ixSideOwn in 15b). 31ad2f0e: m23:n1 level 1 arrow to night 1's next stop after the night's clock-in.
- Possible should: m23DoorOpen is false from n.to + 60 even if you're still inside and not out (stuck behind the shielded door?).
- Plan: cadet 31ad2f0e vs a2ef6416; mech m23 (ON); controller m23 deck6; m23_door.py (door and path at each step, shots at 390x844).

## W8 eee654d4 (S6-9 turn 2), reviewed together with bd138090 at lead 42's word
- Read: Calder waits in the tea corner from 18:30 (cqEscort 'wait' to CQ.stand '5-tea-3', a place id where others pass { deck, room }:
  check live she gets there); the seats' guests stand (cqSeatsClear: crewScene wait in room 't' till 19:30), which answers my seat
  worry above; Works app tab 'Your career' (order 90, show() once answered; worksView filters tabs by show: off, no tab has show).
  Backlog W8-1: Calder misses her own Four weeks aboard in the plain game (her plan is on Deck 3).

## PZ6 claude/escort-seated-check 775c3ca (test only, from staging c477e525)
- promo_beats_check parts seated (actStart 'sit', real) and blocked (you on the seat's own tile; fails on 6f1915cb). PZ6-1: no known
  real-play path to the escort bug. Note: RV23's probes used placeSpot (the seat's own tile), so the original repro was the probe's
  placement; the fix stays (harmless, and a guard). Queued: seated blocked on 775c3ca and on 6f1915cb.

## W8 runs (tips bd138090, eee654d4, d18aafc8; then 5d2c2361)
- cadet ALL IDENTICAL: eee654d4 vs 62a8ac0b; d18aafc8 vs 8e0778ef. promo_beats (ON) cq cq2 mt mt3 mt4 t4test OK (eee654d4); t4carry
  t4before t4test t4passed cq cq2 OK (d18aafc8). PZ6's seated + blocked on eee654d4 ON: OK (Calder walks to you sat at 3-lounge-24, 3-mess-9).
- p4_play (Tier 4 offer, seated in the lounge) on d18aafc8: 22.2 m -> 2.6 m by 08:37, pu4.offer plays. n6_play: briefing skipped,
  Calder 09:31 -> 5.3 m 09:43, night.on plays (after the 09:30 test was due: Day 22 coherence is item 3); clock-in/engine room/clock-out arrows.
- cq_play.py (ON eee654d4, Dev 'cq' preset via devmodeSetCareerTo): stand: Calder at 5-tea-3 from 18:35, story 18:40, 19:05 "Budge
  up", she sits 5-tea-1, arrow 'Sit with Calder' 5-tea-2, ask 19:08 (3-min fallback), Record, Mail, "Your career" toast. sit: actStart
  at the arrow's seat at 19:05 left me on 5-tea-3 (Torres still getting up); ask 19:08 by the fallback. miss (Deck 3): notice 19:30,
  Calder 23.9 m -> 3.7 m, ask 19:45 standing. No page errors.
- MUST (sent 15:5x): end:find arrow has no deck, guideGoal needs g.deck: never shown (goalNow stayed the mysteries board).
- shoulds: story with Calder alone at 18:40; seat guests leave the corner at 19:05; the arrow's seat taken as it appears; Dev 'cq'
  preset starts the nights on Day 26 (toast + Mail "Your nights"); worksEscort `mine` without the day check.

## DA6 runs (tip 0f859eca, base 40f3bdac)
- cadet ALL IDENTICAL apart from renderer noise (beside another browser: re-run alone); mech m23 (ON) OK.

## AS1 claude/m24-pick-pointer 5f649b45 (base 40f3bdac): PASS
- cadet ALL IDENTICAL (1-level renderer noise beside another browser: re-run alone pending); arrows_check (claude/arrows-step6's) step6
  asis OK: night 3's swap reached by arrows, 740 min due, 0 missed, 0 stuck; controller m24 OK. AS1's arrows-step6 ee18d663: code read OK.

## DA6 S6-5 runs (tip 0f859eca): interactions OK; controller m23 deck6 OK; m23_door.py: door shut before permit / badge / the Watch
  told, open (10-tile path) once told, open while out but inside, shut once outside; late-badge word at 31 min; no page errors.

## W8 618c2901 (fixes): cadet identical vs 40f3bdac (noise; re-run alone); promo_beats cq cq2 t4eve t3carry t4test t4passed OK;
  devmode set t4beats OK; cq_play stand: story 18:45, "Budge up" 19:05, guests by the opening, ask 19:08, Record with the nights.

## DA6 2df6bfce: PASS (sent 17:2x)
- cadet identical (abf496f3 clean vs 40f3bdac; alone run of 2df6bfce pending); deck_check ON OK; d2b_look.py: home 2-B, all three
  keepsakes on Deck 2 room B, tappable, 147 calls; should: frames not made out on the west wall at 390x844. Door fix read (inside R: open).

## W8 6f13b61a: PASS (sent ~17:30)
- 618c2901 cq_play miss: "Calder wants a word" leads from 19:30 (deck 3), she asks 19:45 (MUST fixed). 6f13b61a: promo_beats cq cq2 OK;
  cq_play sit: arrow 5-tea-1, Calder at 5-tea-2, ask 19:06. shoulds: the ask opens while you walk to the seat (PLAYER_PLACE is set at
  actStart); Basil's later steps only on paper (my probe takes no job). AS1's skiptea confirms the fix independently.
- Alone cadet re-runs pending: 6f13b61a, 5c27b740, 5f649b45 vs 40f3bdac.
- Still to do: AS1 arrows-step6 75f6262c (test only); PZ6 775c3ca run; Day 22 coherent play on merged staging (RV23's item 3);
  Tier 3 offer live (optional).
- DA6 4a84e153: PASS (17:4x, lead 42's priority): frames moved above the armchair (DECK2_HOME.menu 1.55, .cert 2.1); DA6's 390x844 shot and crop read; alone cadet: 6f13b61a and 5c27b740 ALL IDENTICAL.
- W8 9063aafe: cqSat (the question once seated, not mid-walk): code read OK, PASS carries (17:4x).
- W8 9063aafe: PASS (cq cq2 OK; cadet vs d0d381e0 identical, 1-level noise partly beside another browser). Sent 17:5x.
- AS1 5f649b45 "alone" re-run: identical with 1-level noise (the Day 22 probe ran beside it: not truly alone; merged already).

## Day 22 coherence (RV23's item 3), reported to lead 42
- Arrow follower (AS1's step6 asis): briefing attended, Tier 4 test passed, night 1 clocked in, 0 missed, 0 stuck: the beats fit.
- Skipping the briefing (n6_play): Calder's night word at 09:43 after the 09:30 test was due (test waited ~13 min). Acceptable.
- d22_play.py (scratch merge staging d0d381e0 + W8 6f13b61a, one 4d conflict: keep both) stalled at 08:47 in my probe; stopped for the round.

## Idle (lead 42, 17:47: the round is on, cap BM19 + 4 runners). Skipped on the lead's word: PZ6 775c3ca run, arrows-step6 runs.

## Controller update (lead 43, 2026-10-28 02:23): I review it
- Read plans/controller-audit.md (claude/controller-audit 199fa2b). Builders: PA1 wave A (claude/pad-wave-a: chat/shop landing, clock
  Undo, Dev card, Take a seat/Lift on X, cards put away by B), PB1 wave B (claude/pad-wave-b: props mid-visit, every job stop on
  this deck, beam floor, court edge; register part_promo3). Base claude/staging-pad b3247d6, PAD_ON off. Wave C later.
- Per item: cadet identical (PAD_ON off) vs b3247d6; controller_check all parts on a PAD_ON copy (the check makes its own copies;
  I leave out `reach`, which has never finished, unless the lead wants it); a live pad play at 390x844 of what changed.
  Verdicts to the builder, lead 43 (session_01GKuymjoDoY2kA9yCK12NG1) and BM20 (session_01GKuymiwDEgkwGmjJ2nokvg).
- Lead decisions: pad Undo window lands on the close cross; Dev card on the screen edge with #dev; sound on first pad press
  (wave C); no on-screen keyboard.
- Baseline running: controller_check on b3247d6, all parts but reach (base_ctrl*.txt in /tmp/rv24/pad).

## Controller runs
- Baseline b3247d6, controller_check all parts but reach: all OK except idle (8 problems: device-page DOM hash -1556429587 ->
  978430068, incl. its own no-pad-twice steadiness line). Re-run alone: OK once. idle is an old intermittent FAIL.
- Wave C 336b00c2: PASS. cadet identical vs c62a292b; sound_check OK; controller all-but-reach OK but idle (2 problems; re-run: the
  same hash pair, in PAD_ON-off cases too: old). pad_look wavec: the four lines read well with the pad, revert after a touch; Saves
  hint present. Scratch merge A 818ec0b + C: saves savesland words sound OK (build-table conflict only).
- Wave A 092245c -> 8d511a1 (MUTANTS) -> 818ec0b (Saves lands on Back): cadet identical vs b3247d6 (noise beside another browser);
  pad_look wavea: chat lands on Say hello, shop on the first goods, the clock's highlight on the x after a punch, the Dev card on the
  edge with #dev and A opens the panel; savesland OK. Full run on 818ec0b going.
- Wave C a29a0f48 (SD2-1 tipWords): words OK, the tip card reads 'Walk with the left stick, and press A on anything to use it.'; PASS carries.
- Wave A 818ec0b: PASS. cadet ALL IDENTICAL alone vs b3247d6; controller all-but-reach 48 OK, idle FAIL (old hash pairs). Waiting for wave B.
- Wave B 177793b6: PASS. cadet identical vs b3247d6; controller all-but-reach 48 OK, idle old (hash pairs). pad_look waveb: "Your job:
  A pipe drips..." beside a held team job; cabin spots offered mid-visit; "Paint your name" from 1.9 m, 177 calls. Scratch merge
  staging-pad 56e98a56 + C a29a0f48 + B: 13 wave parts + m23 OK (controller_check end block conflict: keep both). PB1-1 noted (cake).
- All three controller waves PASS: A 818ec0b, B 177793b6, C a29a0f48. Idle after.
- Sound r3 turn 1 (64077a69): mine (lead 43); findings to SD3 session_01GKuymir9eBj7X6kLtwLRmq + lead. Farewell song changes to A in SD3's next turn. Priority: EV1 visit-on, DM1 J0, then sound.
- Sound r3 64077a69: PASS. cadet identical vs e158dcff; sound_check OK incl. check_r3music (right track only in the right room and time) and check_r3_off; timing not measurable (frozen page clock), eventsOn cached per day.
- Dev mode J0 eef5b56: PASS. cadet identical vs e158dcff; devmode_check all OK (jumps part); dev_arrow OK; dm_look.py by taps: Jump to
  tab, Set career Day 38 (Tap again), progress + Stop, 18 s, Day 38 06:00 Engine Specialist with milestones kept. Rep "New" from Day 26:
  same on the base (per-rank reputation).
- Sound r3 dc3014b6 (farewell song A): PASS (SOUND_ONLY=r3 OK).
- Sound r3 turn 2 a09b32b7 (mess hall): PASS. cadet identical; sound_check OK incl. r3mess (silent empty, ~3 clinks/s at 44/50, off outside the mess).
- Dev mode J1 d9b7b3c: PASS. cadet identical (noise); devmode_check beats + jumps OK; dev_arrow OK; dm_jump.py: briefing Day 22 08:20 with its arrow, Night 2 Day 23 20:50 (no arrow yet at 20:50: note).
