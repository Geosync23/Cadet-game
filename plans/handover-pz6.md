# Handover: PZ6 (Step 6 puzzles seat, S6-8)

- **Role:** builder for Pillar 5 Step 6 piece S6-8 (P6, P7, P8 and the T4 band), hired by lead 41
  (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). My session: session_01GKuymjrmdGE4vaHHHGkvYF.
  Reviewer RV23 (session_01GKuymoDm1XbC5G8TvaCNLr); build master BM19 (session_01GKuymncYhRTKs8t4byNfdj);
  W6 (session_01GKuymmTEpqHLycbYTJwRQn) owns section 28's helpers, 24u, the ladder rows (p6/p7/p8 registered inert by
  W6) and the switch lines. Later: review S6-7's clue-choice call into the case panel (24k).
- **Spec:** `plans/p5-step6-spec.html` on claude/p5-specs (S6-8: "In 24k's slot: CASE_KINDS.p6, p7, p8. CASE_BANDS.T4
  exists; its rate and cap too"). The puzzles' designs are the Pillar 5 plan's (plans/pillar5-plan.md on
  claude/p5-design, "P6-P8"), fitted to the case engine. Overnight: the user's answers all "recommended".
- **Branch:** `claude/p5s6-puzzles`, from `claude/staging-p5s6` 64e296df. Build-table rows `0.94.0-c6.N`. The two
  build-number lines untouched.

## Turns (all behind `P5_CASES6`; off = cadet_test ALL IDENTICAL vs 64e296df, check_fast OK)
1. P6 Does it add up? (and the shared `caseAtWork`, `caseFirstShow`, `caseFirstFreeze`; puzzle_check's Step 6 parts).
2. P7 Faded labels (the grid; a one-line `K.act` hook in caseAct).
3. P8 Swap testing (the test rig).
4. controller_check reach for the new kinds; this note; review fixes.

## What I built (24k's slot, after the old-mysteries board)
- **Shared:** `caseAtWork(now)` (your day shift, or a night from section 28's `p5NightAt`), `caseFirstShow(c, j, kid, fb)`
  (a kind's first case shown at work with the row's teacher's word, `train.<kid>.word`, in person; on a night held
  to the night's end), `caseFirstFreeze(j, kid, sus, clues, flag)` (P4's frozen first case, solved in the T4 band).
- **P6** `CASE_KINDS.p6`, `p6Pick/p6Ring/p6Clues/p6Text/p6View/p6Title/p6Card/p6Wrong/p6Fits/p6Stage`, `P6_BAND`,
  `P6_SLOT = 39`. Suspects: the cause and 3-4 other machines on its line (P5's `p5Pick`), or the four battery banks
  (`5-battery-1..4`, cause `cell`, only once `worksStage('m19') >= 2`). Each has a feed (2-6, key 892); the leak is 1,
  or 2 from a feed of 4+. Clues: `m0` the line's meter on the job (sent, came; kills nothing), then a ring of pair
  meters `p0..`, each at its first machine's panel (pair i = suspect i and i+1 in the line's order): adds up kills
  both, short kills the rest. Fewest is always 2. Flag `case.p6.first`.
- **P7** `CASE_KINDS.p7`, `p7State/p7Rooms/p7Lay/p7Clues/p7Text/p7Grid/p7View/p7Act/p7Fits/p7Sus/p7Tick/p7Stage`, `P7_BAND`,
  `P7_SLOT = 40`, `P7_FIRST = '4-junction-1'`. Panels of kind lights or relay, cause `relay`. Suspects: the chatterer is
  the cause, the others `'r:<letter>'`. The layout (rooms, who feeds what, the chatterer) rides on clue `f0`'s
  `src.lay`, the grid on `src.grid` (n*n of '.', 'y', 'n'). Facts `x0..`: sketch (panel, by Pell), drill (panel log),
  flips (in the room). `y0` (four relays only): "X isn't Y", kills nothing. `SHIP.works.side.p7 = { labelled }`.
- **caseAct** (24k, mine): an unknown verb goes to the kind's `act(c, verb, arg)`.

## Words
Stand-ins, baked (content_gen.py), lines_check PASS: content/works/cases.lines (the P6 keys: works.mech.p6, next.p6,
next.wait.p6, case.title.p6, case.title.p6.power, case.p6.line {a} {b} {n}, case.p6.pair {machine} {other} {n} {a} {b},
case.p6.short {n}, case.p6.adds, case.p6.head {n}, case.hint.p6.1, case.wrong.p6 {part} {machine}, chief.p6.title/.1/.2);
calder.lines and reyes-alejandro.lines (`== work`, flag train.p6.word). P7: case.title.p7, case.p7.flick/.sketch/.drill/
.flip/.not ({a} {room}), .head, .flicker, .relay, .relabel, case.wrong.p7, case.hint.p7.1, chief.p7.*; calder and
torres-zeke train.p7.word. Room names read lowercased ("the bunk 2" reads oddly: the head writer may want articles). lines_check only knows its PLACEHOLDERS list:
units go inside the number ("17 kW").

## Tests
- `python3 puzzle_check.py BUILD.html p6 [p7 p8]`: Step 6's parts on a copy with `P5_STEP6 = P5_STEP5 && true`; the
  off test on the build itself (Step 6 is behind ?p5s6). With no part named: the old check, Step 5's parts, then Step 6's.

## Gotchas
- Don't edit the game while check_fast runs; killing it leaves its workers running (kill them by pid, not `pkill -f`
  with a pattern that matches your own shell).
- caseClean keeps only the engine's fields: P7's layout and grid, P8's picks ride in a clue's `src`.

## Open questions for the user
None yet.
