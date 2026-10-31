# Handover: JB2 (patch 0.99.5, the user's notes 14, 15, 18: jobs)

- **Role:** jobs builder for lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN). Reviewer **RV28** (session_014zyJYQKwGvytfCGdrWMoiZ; lead 47's final word: RV28 had already started; RV29 was asked by mistake and told to disregard). SW4 (session_014zyJYNzWwbPhLN9wtKdEWj) polishes the stand-in words on a branch from c6dc9ac: answer its questions. My session: session_014zyJYMCGakWaNzvpk6S3h5.
- **Branch:** `claude/p995-jobs` from claude/staging-0994 8976965e. Game commit **ec18eec**; game sha256 `ed43ee2cbbabe369bde2b864bafdb70859529caa41e6b85704852e315100d293`. Later commits: checks, design-doc, build-table row, this note. Sent to RV28 for review (waiting).
- **Round 2 (RV28's FIXES NEEDED: W1 bake, F1 scanner job, J1 tour words):** fixed on this branch with SW4's words merged (build-table row 0.99.5-jb.2); re-review by **RV29** (session_014zyJYM3D7UBkZN49CsZVuA): **PASS on 1e056bd** (2026-10-31 ~10:50 UTC). RV29's small non-blocking note: after the tour's last stop Zeke says "Ticked... Right, onward." just before "That's the tour" (the same order as 0.99.4's lines); left for a later polish (skip the per-stop line on the last stop). Game sha256 ef0941da2c2cd5300d6b5d5278201ac60dba60490394fee6903861e93db37d04.
- **Lead's decisions:** the 40-minute cap is on the work (holds + fetch + make), not the walk; turning in from the device is not in this patch (the lead offers it to the user separately). Morning rounds keep marks with a plain reading. Washer life 20 (crew too). P3/P9 cases left on washers. machine_check repairs-share band widened to 40-65% (option A).

## What I built (all in section 17's systems slot, the "JB2" block at its end, plus small edits)
- Switches: `var JOBCAP_ON, SPREAD_ON, CHECKS_ON` (all true). All false = ALL IDENTICAL to 8976965e (cadet_test).
- Note 18: `jobCapMins(j)` (service 12, repair 22, overhaul 32, +10% a tier, 40 max) read by section 15's `jobMins` and `openJobs`' minutes; `jobCapMake(v)` (half, 20 max) read by 15's `makeMins`; 24j's TINKER_LIST 30 -> 20.
- Note 15: washer life 20 (set in the slot at load); `choreNoWasher` on the calibrate / inspection round / small fault chore lists; `fixScanMachine(d)` for FX10's scanner first use (key 1997); `jobRoomKey`, `jobRoomsRecent`, `boardSpread` (openJobs('you') and the device's Jobs list); boardTopUp skips recent rooms.
- Note 14: `CHECK_ROWS` (31 rows 'id|place|kind|name|reading', Decks 3-5), `checkTable`, `isCheck`, `checkRow`, `roundSpot`, `roundMix`, `checkTour` (key 1995), `roundMixRoute` (key 1996). 24a edits: roundRoute, roundSign + ROUND_READ, roundMark, roundJob, the rounds kind's stops + goal, roundTrainStep (tour flag). 15b: RG_TOUR tips (tip.tour.*). 24 core's trainScript picks `train.m1.torres-zeke.tour` (content/meetings) with CHECKS_ON. boardTradePost's afternoon round via roundMix.

## Tools and checks
- `tools/jobs_measure.py BUILD [DAYS] [--json OUT]`: the before/after numbers (steady player, real career). Walk estimate: 1.7x straight line at the player's pace, 2 ship min a lift ride.
- machine_check 5z: a JB2 line (washers <=10% of the quick player's Days 1-7, 12+ rooms, board minutes <=40, the caps). mech_check m1: the tour (5 stops, decks [5,5,5,4,4], one mark each) and a morning round's check points.
- Ran green: check_fast, machine_check x2, mech_check full, career, interactions (takes > 30 min: give it a long timeout), day_check 2/3/5, names, words.

## Gotchas
- A round's route may hold 'chk:<id>': use `roundSpot(id)`, never `machineById(id).kind`, and `SHIP.machines[id]` is undefined for them.
- Stage 2 picks (roundPickAsk) list machines only: a picked route has no check points (by design).
- careerText / worksText keys for the new words: round.check.<id>, round.read.<state>, round.tour.{ask,checked,goal,noted}, round.title.tour, tip.tour.<step>. All stand-ins.
- Two browsers at a time; each needs its own CADET_WORK.

## Loose ends / open questions for the user
- Stand-in words for a writer (listed in the build-table row).
- Walking still adds about 40 ship minutes to a job on another deck: the lead's separate idea (turn in from the device).
- The laundry is still the top room (8 of 109 jobs, the cart bay 7): four washers in one room and they start the game partly worn.
