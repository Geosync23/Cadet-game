# Round "fable", check runner R6 (session_01GKuymjzQWrtt6PCGyfmQUB), 2026-11-15

- Candidate 1: claude/staging-fable-review at c4999dae, label 0.99.92-review.
  Game sha256 d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0 (matched before the first run).
- OLD: 0.99.91, main cdd9efd, game sha256 b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (matched).
- Each check run once on the candidate. OLD run only for the one that failed (Day 14).

**Result: R6 OK. One FAIL, day_check Day 14, the same on OLD word for word: old, not the candidate's. It needs a backlog row.**

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole, alone) | PASS | exit 0, `INTERACTIONS CHECK OK`, 2205 s, "skipped" lines 0 |
| day_check Day 10 | PASS | exit 0, `DAY CHECK OK`, 442 s, skipped 0 |
| day_check Day 14 | **FAIL, old** | exit 1, `DAY CHECK FAILED`, 458 s, skipped 0, errors []. The one line: `FAIL deck 7: teague-theo 14:49 stuck 20.0 ship minutes`. Proof below |
| day_check Day 15 | PASS | exit 0, `DAY CHECK OK`, 456 s, skipped 0 |
| day_check Day 20 | PASS | exit 0, `DAY CHECK OK`, 454 s, skipped 0 |
| perf_check BUILD OLD (alone, last) | PASS | exit 0, `PERF CHECK OK (2 skipped: switch not in this build; 0 waiting: not built yet)`, 4281 s. No PROBLEM line, no spike to re-measure. File 8.91 MB, load 7.1, 7.7, 7.7 s. A week of play: 470/41/93 -> 472/41/93 (geometries, textures, heap MB). Deck round trips 470 -> 470 -> 470 (backlog 14 did not show) |

## The Day 14 FAIL and its proof
- Candidate: `Deck 7: up to 19 crew, worst stuck 20.0 ship min (teague-theo 14:49)` and
  `FAIL deck 7: teague-theo 14:49 stuck 20.0 ship minutes`. Everything else in the day's log is fine (no other FAIL,
  no page errors, "Deck 4 the same twice: True", draw calls peak 176 of 450 on deck 7).
- OLD (0.99.91), same command, Day 14: exit 1, `DAY CHECK FAILED`, the same two lines word for word
  (teague-theo, 14:49, 20.0 ship minutes, deck 7), errors [].
- By the round page ("The list", point 4): a day that fails the same way on OLD is recorded as old and new to the
  backlog, not held against the candidate. Day 14 was never run in a round before. Told to BM29 and lead 52 at once,
  and again with the OLD result. The backlog row is for BM29 or the lead to add (R6 did not touch plans/backlog.md).

## "Skipped" count
- 0 lines in every log but perf_check's.
- perf_check: 1 line containing "skipped" (its OK line), and 4 `SKIP` lines = 2 scenes, each listed for NEW and OLD:
  "Step 6: the engine room, Tue 21:00" and "Step 6: engine control, Tue 21:00", "SKIP: not all of P5_STEP6 in this
  build". The same 2 were skipped in round 09991b (R6's notes there), so nothing new; named here for BM29 to compare.

## What happened along the way
- perf_check had started (21 seconds in) when the Day 14 FAIL was read. It was stopped so that Day 14 on OLD would not
  run beside it, then started again from scratch, alone, after the OLD run ended. So perf_check has one full run.
- Days 10 and 14 ran in one lane, Days 15 and 20 in a second (two browsers at most, each lane with its own kit folder).
- No container restart. No setup trouble.
