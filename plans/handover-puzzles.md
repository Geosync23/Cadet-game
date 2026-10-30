# Handover: Pillar 5 seat H, head-scratchers (case engine, scanner, P3)

Written 2026-10-18 by seat H (session_013nqpqRFX4hh3cLPhhpZirJ) at about 60% memory, for the fresh puzzles engineer who builds Step 3 (P1 "When does it happen?", P2 "Who saw what?", the T2 band). Read CLAUDE.md, plans/brief-p5.md (claude/lead-pillar1), plans/pillar5-plan.md Part 4 and the pages on `claude/p5-design` first (`plans/mechanics/case-engine.html`, `m7-scanner.html`, `p3-whats-been-tried.html`, `fault-tables.html`, and the Step 3 pages when the designer publishes them). Then this.

## Role, branch, builds

- **Seat H**, branch `claude/mech-cases` (from 0.60.7 candidate `claude/cand-0607` d3d720b). Builds **0.55.x**; last is **0.55.12 (5a4d362)**. All pieces reviewed PASS, nothing open (reviewer session_01MSLjUdmeVJetxFhh9PqzLt, notes on `claude/reviews-p5`).
- **Hash keys:** 874-875 (scanner), 880 (rate roll), 881 (which kind), 882-889 (the eight sub-seeds), 890-891 (P3: try times, who), 892 (`caseDecoys` order), 893 (the order suspects are shown in). 894 is free in 880-894. The second Pillar 5 range is 1000-1049 (ask the lead for a share).
- **People:** lead 12 session_01GjWhU9Z9V8RNoR8yyELA9V (report only finished pieces, blockers, design calls); designer session_01VXENaUt4vdyYtr3KjVZk9z; build master BM4 session_013h22isZZqmJJSEKSbrwabf; reviewer above; seats C (Works career, 24 core) session_01LgTgzjeqLNrjeCa2iRzbYx, S (systems, section 17) session_01KxfsfBWkCGcncuuH2n1hFB, P (player, section 15) session_0153WUGRakJnNzUCNNHf1E8X, writer W session_013DdpJv4AKFJcvuBBqjSXms, deck architect A (DA4) session_01P6DtVbtWZs9i82fJ4UzRuB. Hook names go seat to seat directly; send every finished hash to BM4 and the reviewer.
- **The join:** C owns `claude/p5-join` (fa418d2 with H 5a4d362 was green). Merge order: S, P, C, H, A, W. The only hand merge for H: both C's 24 core and H's blocks sit just before `// 6. CAMERA`; 24 core first, then 24g, then 24k (BM4's `plans/build-master/res24.py` does it).

## What H owns and built (all in starship-cadet.html)

- **Section 19, the chips block (0.55.0):** `{ kind: 'chips', items: [{ label, on, action }] }` (48 px toggles, struck through and dashed while `on === false`, `aria-pressed`). `DEVICE_SKIN.has(kind)`; `devChips(items)` falls back to a buttons block with "✕ " on a skin without chips. CSS `.device .chips`.
- **24g THE SCANNER (M7):** `scanRead(jobId)` (frozen `j.scan = [[part, value]]`), `scanView`, `scanOpen` (the hidden `scanner` app; P's look-over calls it, 0.28.73), `scanPick`, `scanFitted` (through `caseFitted`), `scanTrainReserve` = `WORK_MECH.m7.reserve` (C's training flow), `caseMachName` (S's `machineTitle` if present). Rules: cause part 12-35, others 70-96, 3 in 10 a worn decoy (same card, different sign); **on a case's job every suspect reads worn 40-60 and the rest good, independent of the cause** (the reviewer's find: the scanner must never settle a case); Day 5's training case is fixed at pump 55, seal 44, valve 49 (the cause not lowest).
- **24k CASES (the engine):** `CASE_KINDS` (kinds register themselves), `CASE_BANDS` T1-T4, `caseRate`/`CASE_MAX` by rank, `caseOffer(j, h)` → `caseMake` (up to 8 sub-seeds) → `caseSolve` → frozen case in `SHIP.works.cases.open`; `caseShow` (the card, `j.parts = []`, held till 17:00), `caseHeld`, `caseHidden`, `caseRelease` (the crew's long way), `caseClue`/`caseAsk`, `caseTick` (once a ship minute from C's `worksCareerTick`), `caseCall` (a re-call before fitting replaces the call; sends `simNote('caseCalled')`), `caseFitted` (wrong call: part back on its shelf at Tier 1, crossed by the evidence, stops reset, the machine's line), `caseHint`, `caseTalk`, `caseLong`, `caseDone` (flags 2 right first time, 4 clever; also `j.rightFirst`/`j.clever` for C's log; `worksUse(kind.ladder)`), `caseFlags`. Fault notes = `caseView`/`caseAct` (verbs `case:*`), a Works tab through `worksTabAdd({ id: 'faults', verbs: 'case', ... })`, else its own hidden `faultnotes` app. `CHIEF_NOTES[kind] = { title, key, lines }`.
- **24k P3 What's been tried?:** `CASE_KINDS.p3`, `p3Tries` (a Works crew member at work then, a hand not the Chief, not the same one twice; 2-12 hours on, or the next morning from 06:00), `p3Tick` (each try at its time takes the part off its shelf; the case shows inside your shift), `P3_NOTE` (the writer's `fault.tried.<kind>.<decoy>` + " — Surname"), `p3Stage` (Day 5's training case: 4-washer-2, or 3 if your own wash is in 2, leaking from Day 4 18:00, reserved slot 20, a week). Your m7 scanner job on Day 5 IS that washer (`c.m7`); reading it opens the case there; `worksEscortHold('m7')` keeps the teacher with you till the call.
- **puzzle_check.py:** chips; a sweep of ~300 stand-in cases over T1-T4 (each re-solved in Python: one left and it's the cause, no single clue solves it, fewest in band, reachable); the rate roll per rank; a case in play end to end; the save round trip; the scanner; a P3 sweep (~116 cases) and Day 5's case both ways (through m7 and through the row). It stands in for anything a seat hasn't landed (FAULT_CAUSES, SHIP.works, hasTool, section 17's lines) and prints which. On the join it runs with none. Note: the test page freezes `performance.now`/`Date.now`, so timing is measured from Python.

## Shared formats

- A frozen case: `{ id: 'c' + jobId, job, kind, k, band, cause, sus, fewest, clues: [{ id, type, src, at, kills }], got, crossed, known, calls, fits, posted, until, by?, m7?, wait, taken, talk, long, train, told, title }`, about 600 bytes. `at` is a place id (counts as a deck), `'board'` (taped to the job, not a deck) or none (`src.ask`: a person). `src.tool` needs `hasTool`.
- A kind: `{ name, ladder, fits(cause, m), suspects(j, seed, band), clues(j, cause, sus, seed, band), view(c), hint(c), text?(c, clue), sus?(c, id), wait?(j), tick?(c, j), open?() }`. A kind is open when its ladder row has opened (`worksIsOpen`), not when trained.
- Save: `ship.works.cases = { open, done: [[id, day, flags]] (last 20), n, first }`. C's `worksClean` drops it, but the save writes `SHIP.works` whole, so `caseState()` reads it back from `SAVED` itself (`CASE_SAVED`, cleaned by `caseClean`).

## Lessons and gotchas (read before Step 3)

- **The scanner and every other tool must not settle a case.** Any reading on a case's job has to be independent of the cause; puzzle_check swaps the cause and expects identical readings. Do the same for P1's log and P2's witnesses: a clue may only rule out what the solver says it rules out.
- **The solver is the contract.** "Exactly one left, no single clue solves it, fewest within the band" is checked at posting and again in Python by puzzle_check. A P3 note rules out exactly what was tried; the designer dropped "fine for an hour after a reset" from T1 because one note killed three suspects.
- **Scripted players get stuck on cases.** C's career/mech checks took the Day 5 case and fitted without calling (the washer stays broken by design). They now call an open case first. Any new check's player must do the same.
- **Section 17's `jobSetPart` refuses a job with no parts** (a case's job until called), so `caseCall`, `scanPick` and `scanFitted` fall back to setting `j.parts`.
- **Titles:** build from `caseMachName` (S's `machineTitle`) and the cause's `shows`. `jobCard(j)[0]` now carries the symptom ("Washer 2 (leaks)"), so it doubles. The writer's `case.title` ends in a full stop: dropped for the card.
- **The training case is held a week** (reserved slot 20); a roll case waiting for P3's tries is let go after three days (`CASE_WAIT_MAX`). Taking a waiting roll case's job early makes it a plain repair.
- **`caseOffer` runs inside `jobsHour`:** no `claimJob` or other machine-time readers there; use `caseNow()` (the hour) for times. Notices that need the UI go out from `caseTick` (`c.told`).
- **cadet_test stays ALL IDENTICAL on this branch** (nothing is drawn; everything is inert without 24 core). Always run puzzle_check and cadet_test; device_check when section 19 changes; machine_check when anything touches jobs; on a trial combine also career_check (C's) and mech_check.

## Loose ends

- P3's tries are on paper (who and when worked out at posting; the part comes off the shelf at that time). Once section 17's `jobKindAdd` try kind is wanted, post real try jobs (crew walk to the panel), keeping the same notes.
- No escort for later P3 cases (only Day 5's, through m7); talk-it-through is a toast and a Fault notes button, not an appointment yet.
- The writer's lines: `case.*`, `chief.p3.N`, `fault.tried/still.*` are read through `worksText` where wired (title, chief's notes, notes, wrong-fit lines); the rest of Fault notes (headings, buttons, hints 2-3) still uses stand-in words.
- `CASE_STATS.ms` reads 0 in tests (frozen clocks); the real measurement is puzzle_check's Python-timed 2000 makes (0.012 ms each on desktop).
- Step 3 per the plan: P1 (log clues from `machUseDay`/`MACH_HIST`), P2 (person clues via the chat card's "Ask about the fault": `caseAsk`), T2 band (3-5 suspects, 3-4 clues, fewest 3, 1-2 decks; wrong T2 seals and cartridges are spent: `CASE_SPENT`). The engine already handles `type` log/person, `src.ask`, `src.tool` and the T2 band; P1/P2 are new kinds registered like P3.

## How to test

```
pip install playwright; mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
export CADET_CHROME=/opt/pw-browsers/chromium
python3 puzzle_check.py BUILD.html          # ~2 min; prints the stand-ins it used
python3 cadet_test.py OLD.html NEW.html      # OLD = git show d3d720b:starship-cadet.html
```

## Open questions for the user

None from seat H.
