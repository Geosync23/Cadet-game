# Review log: RV24 (reviewer, from RV23), 2026-10-27

Lead: lead 42 (session_01GKuymjnCHnpwDqB94PVwmV). My session: session_01GKuymnJuoJTWnmYunbN7EP. Notes-only branch `claude/review-rv24`
(from claude/review-rv23). Build master BM19 (session_01GKuymncYhRTKs8t4byNfdj) merges PASSes into claude/staging-p5s6.
Cap rule: at most 5 seats working at once; read only until RV23 says it has gone idle.

## Verdicts
| Branch | Verdict | Sha |
|---|---|---|

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
