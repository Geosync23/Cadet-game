# Handover: B4 (Step 5 puzzles seat, S5-6)

- **Role:** builder for Pillar 5 Step 5 piece S5-6 (P4, P5, P9 and the old-mysteries board), hired by lead 39
  (session_019V68fz33UFv4cK5Z4iCDvi). My session: session_01LV8Q8UV6aJPTgmQ6ub1z8G. Spec: `plans/p5-step5-spec.html` on
  claude/p5-specs (EP2, session_01Hos4fCBxgEXxP8nR9E2iMq). Reviewer RV20 (session_01PyJwfvfQVu4oXTYDMGkacw), notes on
  claude/review-rv20.
- **Branch:** `claude/p5s5-puzzles`, from `claude/p5s5-skeleton` 5957d244. Build-table rows `0.93.4-c.1` to `c.6`. The two
  build-number lines untouched.
- **Turns (all behind `P5_CASES5`, off = identical: cadet_test ALL IDENTICAL vs 5957d244 every turn, check_fast OK):**
  1. 38818701 P4 Which gauge is lying? 2. 55b2e6a8 P5 Follow the line (RV20 PASS on 1+2). 3. fd54ba5d the old-mysteries
  board. 4. 4e5c878f SW3's keys, teachers in person, SW3's five mysteries. 5. a064de76 P9 The clash. 6. (this note's
  commit) the board free-standing (pad-pickable), controller_check part `s5cases`, P5's power stage checked.

## What I own and built (24k's slot, unless said)
- **Shared:** `caseSayInPerson(by, lines)` (near you: bubbles now; else they walk over to a seat by you with section 10's
  `crewComeTo` and 20's `seekSpot`; a toast after 40 ship minutes, `caseComeTick`). Used by every first case and Torres.
- **P4** `CASE_KINDS.p4`, `p4Decoys/p4Clues/p4Text/p4Title/p4View/p4Tick/p4Stage`, `P4_GAUGE` (gauge name by part),
  `P4_BAND`. Each decoy's own gauge reads normal (kills it); the cause's own gauge is stuck (flat all day, kills nothing:
  the trap); the scanner's "third reading" at the panel (kills nothing: the machine really is off). First case: slot 28,
  3-chiller-1's `sensor` (display stuck at 3 degrees), Torres. Flag `case.p4.first`.
- **P5** `CASE_KINDS.p5`, `p5Line/p5Steps/p5Flow/p5Pick/p5Clues/p5Text/p5View/p5Wrong/p5Tick/p5Stage`, `P5_FIRST`,
  `P5_BAND`. Readings are section 17's `lineShare` from recorded conditions (no machinesNow inside jobsHour). Full at X
  kills X and above; low kills below. Never on a traced job (24i's). Power: line 'power' (B2's, claude/p5s5-mech-a,
  behind P5_M19), tool 'tester', only once `W.tr.m19`. First case: slot 29, 3-pump-1's seal, Calder. Flag `case.p5.first`.
- **P9** `CASE_KINDS.p9` (fits nothing: its own cases), `p9Find/p9Clues/p9Text/p9Sus/p9Tick/p9AskTick/p9Stage`,
  `p9Settle(day)`, `p9PlanRule(d, occ, pl, a, b, p)`, `p9State`. A load cause `clash` is pushed onto FAULT_CAUSES.washer
  with the switch. The clash: one person's weekly Deck 4 wash overlapping the same fixed calendar item (devDay) twice in
  the last fortnight, nobody else's (new game: Mateo Navarro, Wednesdays, Brennan's tasting table). Clues: trip log
  (board; kills parts), laundry rota (panel; kills other people), the calendar (the why). Who/when ride on the trip log's
  clue (`p9Of`) because caseClean keeps only the engine's fields. Called right: fetch skipped, reset at the panel, then
  the ask in person (level 1 arrow; beside them). The move is real: `SHIP.works.side.p9 = { ask, moves, set }`;
  B3's 24w calls `p9Settle(d + 1)` in its 22:00 settle and `p9PlanRule` first in `sdPlanShut` (section 14's one hook),
  both by name. Slot 38. Flag `case.p9.first`.
- **The board** (`MYS_*`, `mysState/mysOrder/mysJob/mysStops/mysStepDone/mysDone/mysTake/mysView/mysAct/mysOpen/mysTick`):
  Deck 5's `// P5 places` block (section 4d): `wallFixed('w', 'mysBoard', 's', 3.0)` and the `WALL_KIT.mysBoard` kit (a
  corkboard on two legs, made at load, no R()). Section 15b: one `ixTap` line calling `mysOpen`. A hidden device page
  `oldcases`; side job kind `mysc` (three looks at machine panels, a choose at the job board). From Day 21 for a Senior.
  `SHIP.works.side.mys = { seen, taken, done, days }`; flag `mys.word`.

## Words
SW3 (closed) wrote content on claude/p5s5-words (keys in content/works/keys-p5.md). The code reads SW3's keys; extra
keys still stand-ins in code for the next writer: `case.p4.flat`, `.moving`, `.tap`, `case.p5.head`, `case.p9.log`, `.wash`,
`.cal`, `.sus`, `.go`, `.another`, `mys.N.clue.1-3`, `mys.N.sus.1-3` (sus.1 the answer), `mys.head`, `.call`, `.not`,
`.oncur`, `.arrow`, Torres's flag `mys.point` (his pointer to the board on Day 21; SW3's `mys.word` lines are his words at the board); bank kind `p9.move` exists (SW3). The board's clue places are in `MYS_CASES`.

## Tests
- `python3 puzzle_check.py BUILD.html [p4 p5 p9 board]`: the Step 5 parts run on a copy with P5_STEP5 on; "not yet"
  until built. With no part named, the old check then all four.
- `python3 controller_check.py BUILD.html s5cases`: the board by pad (ring names it, A opens, D-pad to Take, A) and a
  P4 case's Fault notes by pad (a suspect, Call it).
- deck_check and interactions_check on a switched-on copy (sed the P5_STEP5 line to `true`).

## Loose ends
- **P9's planner side**, checked on a local merge with B3's claude/p5s5-mech-b 5ad090ff: at Day 23 22:05 the settle
  writes side.p9.set[24]; Day 24's plan loses Mateo's 18:49 wash from the clashing hour, the same when planned again. But
  take() found no other laundry slot that evening, so the wash is skipped that week, not moved: a true move needs a
  second section 14 hook after schedBuild (lead 40: not now; backlog B4-1). The words say so: case.p9.ask/.answer/.skip (stand-ins); SW3's p9.move bank lines promise an hour and stay unused.
- **P9's shutdown form**: `p9ShutClash(booking)` (for B3's planning screen, step 4) and `p9ShutTick` (the notice once per
  booking). Checked with B3's sdAffected stood in; to check on a merge with B3's screen (sdAffected's real tags for a
  laundry visit and a tradition: P9_ROUTINE matches 'laundry', 'tradition', 'class', 'club'). Reviewer now RV21
  (session_01AmTyMHLr5UuCY9zo3nQcwS); lead 40 (session_01NXybH7NNqM8M4ngiyidq6m).
- Later roll cases: P4 and P5 post on real faults at the Senior rate; P9 and the board have only their staged ones.
- Traced power repairs read with the pipe kit (section 17's traceFor): B2 asked lead 39 whether to gate it on the tester.

## Gotchas
- A `//` comment inside a one-line expression ate the rest of the line once (P9's trip times): names_check caught it.
- caseClean drops unknown case fields: keep extra data in a clue's `src` (kept whole).
- Wall pieces from `placeWall` fade with the near wall and can't be picked by the pad or tapped: use `wallFixed` (stands
  on the floor) for anything on a south or east wall.
- Don't edit the game file while a check is reading it (check_fast reads it at each step).

## Open questions for the user
None from B4.
