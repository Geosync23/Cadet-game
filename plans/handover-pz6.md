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
4. controller_check part s6cases; DEV_NOTES, design-doc, this note. Turns: 3046fb5, e3804ce, fd1f27f, then turn 4.

## Loose ends
- Drive-coil (coil module) P8 cases wait for S6-4's real Deck 6 coils (none to work on yet); puzzle_check expects
  them only when the build has coils. DA6 (S6-4): the coils will be '6-coil-1..3' (panels '6-coil-N-svc'); P8's
  fits needs only panelPlace and a 'coil winding' cause, so check them on a merge with DA6's turn.
- F3's old once-only pointer "Cross out what was tried" can point at a P6 pair (it's P3's wording); harmless, once ever.
- Roll cases: P6-P8 post on real faults at the Specialist's rate (.33, at most 2 open) once their rows open.
- S6-7's call into the case panel: built for W7 as `casePoint` (below); W7's 28e calls it on Day 26.

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
- **casePoint({ by, seed, onPick(clueId, isKey), onClose })** -> bool, for W7's 28e (mentoring): a practice P4 case on
  paper in Fault notes' point mode (`CASE_UI.point`; caseView and caseAct each have one line for it), three choices,
  one key; never posted or saved; behind P5_STEP6. `casePointView`, `casePointPick`; a deviceOn('close') hook.
- **P8** `CASE_KINDS.p8`, `p8Bad/p8Sid/p8Of/p8Word/p8Clues/p8Kills/p8Text/p8Sus/p8Runs/p8Pending/p8View/p8Act/p8Tick/p8Fits/
  p8Stage`, `P8_BAND`, `P8_SLOT = 41`, `P8_RIG = '5-shop-4'`, `P8_RUNS = 3`, `P8_MINS = 10`. Parts cartridge or coil
  winding. Suspects: the bad one is the cause, the others `'k:<n>'`. Clue `g0` (the rig, at P8_RIG) keeps `bad` and
  your picks `sel`; runs `r0..r2` have `at: null` (never picked up by walking) and start as the frozen plan
  (`src.plan`); a real run replaces a plan clue's src with `{ run, mask, count, t }` and honest kills, and `p8Tick`
  collects it when `t` passes. Verbs `case:p8` with `sel.<i>` or `run`.

## Words
Stand-ins, baked (content_gen.py), lines_check PASS: content/works/cases.lines (the P6 keys: works.mech.p6, next.p6,
next.wait.p6, case.title.p6, case.title.p6.power, case.p6.line {a} {b} {n}, case.p6.pair {machine} {other} {n} {a} {b},
case.p6.short {n}, case.p6.adds, case.p6.head {n}, case.hint.p6.1, case.wrong.p6 {part} {machine}, chief.p6.title/.1/.2);
calder.lines and reyes-alejandro.lines (`== work`, flag train.p6.word). P7: case.title.p7, case.p7.flick/.sketch/.drill/
.flip/.not ({a} {room}), .head, .flicker, .relay, .relabel, case.wrong.p7, case.hint.p7.1, chief.p7.*; calder and
torres-zeke train.p7.word. P8: case.title.p8, case.p8.* (cart, module, rig, run, one, none, go, head,
pick, wait, runit, gorig, rigname, running, out), case.hint.p8.1, case.wrong.p8, chief.p8.*; torres-zeke and
halloran-emeka train.p8.word. Room names read lowercased ("the bunk 2" reads oddly: the head writer may want articles). lines_check only knows its PLACEHOLDERS list:
units go inside the number ("17 kW").

## Tests
- `python3 puzzle_check.py BUILD.html p6 [p7 p8]`: Step 6's parts on a copy with `P5_STEP6 = P5_STEP5 && true`; the
  off test on the build itself (Step 6 is behind ?p5s6). With no part named: the old check, Step 5's parts, then Step 6's.
- `python3 controller_check.py BUILD.html s6cases`: the Day 25 19:00 preset (on paper), P6-P8 in Fault notes by pad,
  then casePoint's choice. `puzzle_check.py BUILD point`: casePoint.
- Also done for lead 41: claude/team-turn-fix (backlog MA6-1, a team job's turn by tap and pad).
- Results, every turn: cadet_test ALL IDENTICAL vs 64e296df (off), check_fast OK, puzzle_check p6 p7 p8 OK.

## Gotchas
- Don't edit the game while check_fast runs; killing it leaves its workers running (kill them by pid, not `pkill -f`
  with a pattern that matches your own shell).
- caseClean keeps only the engine's fields: P7's layout and grid, P8's picks ride in a clue's `src`.

## Open questions for the user
None yet.

## arrows_check part step6 (taken over from MA6 for lead 42, 2026-10-27; handed on to N6 at ~70% memory)
- **Branch:** `claude/arrows-step6` (MA6's claude/p5s6-mech-a 99040a2 + staging-p5s6 8e0778ef; test only). Run:
  `python3 arrows_check.py BUILD.html step6 [asis|teachoff|track]` (it makes its own P5_STEP6-on copy; ~25-30 min a way).
  Debugging env: `S6_UNTIL=<day>` (stop at noon, state at 09:20/12:00), `S6_DEBUG='<regex on clockText>'` (the
  follower's actions), `S6_WATCH='<regex>'` (state each advance step: deck, room, goal, ns[22], ACT, DIALOGUE, sleeping).
- **Check gaps fixed (none were game bugs):** (1) "drop this job" presses the board's Drop it; (2) after dropping, the
  follower takes the row of the test its arrow names ("Tier N test"), not the first Take it; (3) no skipping while
  `sleeping` (the game wakes after a real-time 850 ms fade; the skips outran it, so you lay "asleep" till 22:55);
  (4) awake in bed with a non-sleep arrow due, the follower gets up; (5) an open scene (DIALOGUE) is read through at once
  (Calder's walk-down stayed open all night 1, unread, so the welcome slipped a day); (6) the welcome's record is the
  pu4Welcome occasion `.met` (24u's pu4Welcomed), not flag 'pu4.welcome' (never set).
- **State (last runs, staging 8e0778ef + the branch):** asis, teachoff and track all reach the briefing, the Tier 4
  test, sleep by day, nights 1-3 clocked in, the welcome, the badge and the move to 2-B; all three fail only night 3's
  coil swap. Mentoring and Calder's question: "not yet" (W8's pieces).
- **Night 3, a real game gap, fixed separately:** `claude/m24-pick-pointer` (28d's m24Beats: a forced pointAsk through
  Works > Team to the next crew member to pick, and at the bridge to Book the slot; the world arrow stays). With it, the
  follower should pick, book and run the swap. NOT YET: on m24-pick-pointer (WIP 1 commit, not for merge) controller_check m24
  is OK but arrows step6 asis still fails night 3 (m24:pick led, no pick made). Next: S6_WATCH='Day 24.*2[1-2]:' and
  S6_DEBUG to see whether the ring (POINT_Q 'p:m24:pick') shows and whether FOLLOW's pointer handling presses through
  Device > Works > Team > the crew button; fix the ring or the follower, then mech m24, cadet vs 40f3bdac, check_fast,
  and send to RV24 + BM19 + lead 42.
- **AS1 took over (2026-10-27):** night 3 fixed on `claude/m24-pick-pointer` 5f649b45 (the ring's Team tab step had no
  `open`, so it stayed on the tab and never reached a name). With it, on staging 40f3bdac: asis, teachoff and track all
  OK (every Step 6 beat, missed 0, stuck 0). Sent to RV24, BM19, lead 42. Fresh machine setup: `pip install playwright
  numpy pillow`, three and acorn into /tmp/cadet-work (DEV_NOTES), `CADET_CHROME=/opt/pw-browsers/chromium`, a CADET_WORK each run.
- **AS1, MA6-2 and W8's beats (2026-10-27):** the M20 setup line is gone; a direct MA6-2 line checks that a sensor array
  lesson untaken by Day 21 doesn't hold Day 22's Tier 4 test (it says when the case didn't arise). Mentoring's record is
  28e's `mt.steps.done`; Calder's question's arrows are 28f's `end:tea/sit/find` (in S6_RX), `have` is `cqTick`. On a local
  merge of staging 40f3bdac + m24-pick-pointer 5f649b45 + p5s6-promo4 23a0e29c: asis, teachoff, track all OK, every beat
  through Calder's question (Day 26 18:40). Before W8's promo4 is in staging, the MA6-2 line is skipped (no ladderTestDue).
- **AS1, way 'skiptea' (RV24's ask):** Day 26 18:20-19:35 on Deck 3, not following (the tea missed), then on to 22:00;
  checks Calder's end:find arrow led and she asked. On staging + m24-pick-pointer + promo4: before W8's 618c2901 FAIL
  (end:find never led; she still found you), with 6f13b61a OK. In the default ways for step6 (not the endings).
- **Left:** (a) done (see above); (b) drop the M20 setup line in part_step6
  ("the setup counts Step 5's sensor array lesson as done") once W8's d18aafc8 (MA6-2's fix) is in staging, and add a
  line that checks MA6-2 directly (a Tier 3 lesson missed on Day 19 must not block the Tier 4 test on Day 22);
  (c) W8 is adding a Day 22 evening arrow (16:45-22:55 had none; lead 42 passed it on); (d) send shas to lead 42 and RV24.
