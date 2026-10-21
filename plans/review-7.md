# Review 7 (PR7): the crew-rotation patch and Dev mode Stops 1b and 2

Reviewer: PR7, session_01LyKAVtCEedL1bP73vqzu9v, for lead 23 (session_01XXiKm9iPgm565SZ4n1knmU). Branch claude/review-7 from claude/integration (3a48846).

Builders:
- PT1 (session_013KBHqs7JLoNRVFCVWdfngN, claude/patch-crew): the first crew rotation on Sunday Day 21 17:40, the "Off the Tern" tradition, ROT_TERN on; the opening camera ~10% closer.
- DB2 (session_01RAw82oHw329cHYC7wapKu8, claude/devmode-2): Dev mode Stop 1b (Traditions tab) and Stop 2 (Set career), plans/devmode-plan.html v3.1.

Method per turn: the diff read; cadet_test (what changes and why); check_fast; the area's checks; a live probe on a real save at phone size with reloads; mutants to prove the checks catch them. Probes and mutants in plans/review-7/.

## Verdicts

| Builder | What | Commit | Verdict |
|---|---|---|---|
| TS2 (for lead 24) | perf_check right rooms | claude/opt-tests c2a32e2 | PASS |

## Log

- 2026-10-21: started; told PT1 and DB2. Neither branch is on origin yet.

## TS2: perf_check right rooms (c2a32e2), PASS

- Test-only diff. perf_check (TS2's) on 0.64.8: every scene's three views stand in its room; the numbers equal plans/opt-measure.md's "with the fix" column, scene for scene.
- Mutant: the old `nearestOpen(tile)` call: 18 "you stand in" PROBLEMs (Machine shop, Fan hall, Bow lounge x2, Cabin 4-05, Gym), exit 1.
- Known, not TS2's: perf_check exits 1 on 0.64.8 for the +2 geometries on the third deck round trip (since 0.64.6).
