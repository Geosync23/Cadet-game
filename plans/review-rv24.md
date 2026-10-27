# Review log: RV24 (reviewer, from RV23), 2026-10-27

Lead: lead 42 (session_01GKuymjnCHnpwDqB94PVwmV). My session: session_01GKuymnJuoJTWnmYunbN7EP. Notes-only branch `claude/review-rv24`
(from claude/review-rv23). Build master BM19 (session_01GKuymncYhRTKs8t4byNfdj) merges PASSes into claude/staging-p5s6.
Cap rule: at most 5 seats working at once; read only until RV23 says it has gone idle.

## Verdicts
| Branch | Verdict | Sha |
|---|---|---|
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
