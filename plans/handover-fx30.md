# Handover: FX30 (builder for 0.99.6, for lead 49)

**Role:** a builder for the 0.99.6 update. Reports to lead 49 (session_01GKuymjPvM7XFzxM7XqFREd); reviewer RV31
(session_01GKuymjTDn3pTeDxiqrxE7F). **Branch:** `claude/fix-0996`, made from `claude/integration` 6475bb30 (0.99.5,
game 93aed54f...5164). The build-number lines are untouched (the build master's).

## What I built (one commit each, everything switched off: the game is identical until the build master switches it on)

| Commit | Game sha256 | What | Switch |
|---|---|---|---|
| 6c14bc2 | 69ac3948...c645 | P5-1: the first "Follow the line" case (p5Stage, 24k) retried each ship hour instead of given up for good after one failed set-up. `p5Ready` (24k's Puzzles slot) dry-runs the set-up first (the pump at cond 40 for a moment, the same seeded suspects and readings, put back exactly); not fair yet: nothing booked, try again next hour. RV31 PASS. | `P5_RETRY_ON` |
| be3a51f | a11a6788...69cd | JB2-2: the gym locker job. Finding: a tap on 3-gym-1's own treadmill frame, or the floor, already started the repair. The puzzle is that the only tappable treadmill, the "Treadmills" item, stands on 3-gym-2 next to the stop, so a tap on it started a run there (that's what the arrows walker hit). The gym has no lockers to move the stop to, so the tap is fixed: `fixThingTap` (15b's Interactions slot, first in PLAYER_TAPS): with a fix or odd job yours (j.fix), a tap on a thing ixTap would use for the stop's place (same kind of place, same room, within IX_NEAR of the spot) does the job's step (ixChoreTap). Other things and other jobs as before. RV31: FAIL for switching on (too wide), replaced by 6701201. | `FIXTAP_ON` |
| 6701201 | 24850dc3...d25f | JB2-2 narrowed after RV31's FAIL for switching on (be3a51f's rule reached 75 stops: toilets, washers, kettles): `FIXTAP_ROWS = { 'oj-d3gym-locker': 'Treadmills' }`, only that job and only that thing; the stop stays at 3-gym-1 (lead 49's OK). RV31's fixtap_reach/fixtap_click OK, interactions whole and arrows week OK on and off. Sent to RV31. | `FIXTAP_ON` |
| 042f57e | f535ed24...ca6e | P5-1 follow-up (RV31's note C, lead 49's ask): (1) the dry run calls machinesNow first and leaves out the pump's own ordinary job (open, unclaimed, unreserved) as jobReserve does, so a bearing job on a faulty pump no longer holds the case up; (2) `p5Unstick`: a save at `case.p5.first` 'none' with p5 not learned and no p5 case open goes back to waiting once (`case.p5.reset` = 1); 'none' after that, or with p5 learned, stays. RV31 PASS. | `P5_RETRY_ON` |

Each: cadet_test vs 0.99.5 ALL IDENTICAL with the switch off; check_fast OK.

## Tests and probes (all in the repo root, next to the other checks)
- `p5retry_probe.py BUILD.html` (about 1 min): makes its own P5_RETRY_ON copy. Off: 3-recycler-1 low at the opening
  gives 'none' (the bug; the old path also leaves the pump at cond 40 and a booked-then-released job). On: waits,
  nothing booked, the pump untouched; a later hour stages creserve29:3-pump-1 seal; the bearing case; the stuck save.
- `fixtap_probe.py BUILD.html` (about 2 min): makes its own FIXTAP_ON copy; real screen clicks in the Deck 3 gym.
- `caserate_probe.py [CASE_TO=61] BUILD.html ...`: the JB2-3 measurement (below). Not a check: it only prints numbers.
- puzzle_check whole OK off and on (P5-1 and the follow-up; about 3 min each). interactions_check whole OK off and on
  (86 min each when run 4 at once), arrows_check week OK off and on (JB2-2).
- Setup in a fresh container: `pip install playwright numpy pillow`, three r128 and acorn in `$CADET_WORK`,
  `CADET_CHROME=/opt/pw-browsers/chromium` (testing-guide section 2). cadet_test writes screenshots in the current folder:
  run it from /tmp.

## JB2-3: how often head-scratcher cases come (caseRate NOT changed; numbers for the lead to ask the user)

Measured with `caserate_probe.py` (CASE_TO=61) on 0.99.5 (6475bb30, 93aed54f) and 0.99.4 (596712bc, a01d1a4c), in the
real game: the real crew doing their jobs and the real machines wearing, Days 5-61 (8 ship weeks) an hour at a time. A
diligent player: promoted on the plan's days (junior to Day 9, officer to 15, senior to 22, specialist from 23), each
head-scratcher kind's ladder row open from its plan day (p3 Day 5, p1 12, p2 15, p4 17, p5 18, p9 19, p6 22, p7 23, p8
25), each row's tool given on its day. The staged training cases (p3's, p1's, p5's first and so on) are left out: these
are the roll cases only. A case is taken as solved 3 ship hours after it's posted. Event days have no cases by design
(caseOffer's eventDay): Days 7, 12-14, 17-19, 22, 28-30, 35 in both.

| Days 5-61 | 0.99.5 | 0.99.4 |
|---|---|---|
| repairs offered to the case engine | 50 | 65 (0.99.5 has 23% fewer) |
| rolled a case | 17 | 19 |
| a fair case posted | **8** (about 1 a week) | **10** (about 1.25 a week) |
| rolled but no fair case (a plain fault) | 9 | 9 |
| roll cases as junior, officer, senior (Days 5-22) | 0 (7 offers) | 0 (9 offers) |
| cases by week from Day 19 (19-25, 26-32, 33-39, 40-46, 47-53, 54-60) | 0, 1, 1, 3, 2, 1 | 2, 0, 1, 2, 1, 4 |

Days 5-40 alone (the first run): 0.99.5 22 offered, 4 posted; 0.99.4 34 offered, 3 posted. On paper (puzzle_check's
paper run, Days 5-33, RV30's numbers): 6 offers vs 10.

What it means in plain words: with fewer repairs (the washers last 20 loads, not 12), the engine sees about a quarter
fewer chances, and over eight weeks that came out as 8 surprise head-scratchers instead of 10. The bigger thing, in both
builds: before Day 23 (a Specialist) almost no surprise cases come at all (0 in 18 days on both), so a player's early
head-scratchers are only the training ones. From Day 23 it's about one a week on 0.99.5. The counts are small, so the
week-to-week numbers jump around; the totals are the fair comparison.

The question for the user (through the lead): is about one surprise head-scratcher a week from Day 23, and almost none
before, often enough? If not, caseRate (24k: junior .1, officer .2, senior .25 (.33 on a Tier 3 machine), specialist
.33) could rise; the user hasn't decided, so nothing is changed.

## Loose ends
- JB2-2's narrowed version 6701201 waits for RV31's re-review. P5-1 and its follow-up 042f57e: RV31 PASS.
- Switching on: `var P5_RETRY_ON = false;` (24k, Puzzles slot) and `var FIXTAP_ON = false;` (15b, Interactions slot)
  to true, the build master's step, with the full round.
- FIXTAP_ON covers only the rows in FIXTAP_ROWS (just the gym locker). Another row that needs it goes in the list,
  with its own probe and RV31's fixtap_reach.py (claude/review-rv31, plans/rv31-probes/) to show nothing else changes.
- Owners: P5_RETRY_ON's code is in section 24k (the Puzzles seat, seat H); FIXTAP_ON's in 15b (the Interactions
  engineer). Both are edits in another seat's section: the owners review.

## Gotchas
- A check that moves the ship clock backwards replays every machine (machinesNow resets): set the clock first, then
  the conditions (BM23's bb45099). My probes do it in that order.
- lineShare reads an open job's cause: a machine under cond 50 with an open job whose cause is on another line (or none)
  reads full. That was RV31's note C.
- Running four long checks at once on 4 cores: page loads can time out (puzzle_check did once); just re-run.

## Open questions for the user (through the lead)
- JB2-3: are head-scratchers coming often enough (numbers above)? caseRate stays as it is until the user decides.
