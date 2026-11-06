# 0.99.7 full round: R4 notes

Runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-06. Share: R4 in plans/round-0997.md plus cr1_check. Notes on
this session's own branch claude/checks-0996-r4 (lead 49 agreed). Build master BM26 (took over from BM25), lead 49.

- Candidate: claude/staging-0997 7fd8f6b (build turn 363107d, later commits docs only), game sha256
  b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d (matches the GO).
- OLD: 0.99.6 claude/integration d7ad4c58, sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches).
- Two lanes, own CADET_WORK each (/tmp/work-r4 day checks, then the OLD appt run; /tmp/work-r4b the rest).
- fixtap off copy: `sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/'` (one line).

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 307s | DAY CHECK OK |
| day_check 8 | PASS | 305s | DAY CHECK OK |
| day_check 23 | PASS | 302s | DAY CHECK OK |
| day_check 24 | PASS | 287s | DAY CHECK OK |
| day_check 16 | PASS | 309s | DAY CHECK OK |
| career_check | PASS | 205s | CAREER CHECK OK |
| cr1_check | PASS | 14s | CR1 CHECK OK |
| appt_check | **FAIL, NEW** | 774s | APPT CHECK FAILED: 6 real FAILs (below) besides its usual 4 planted ones |
| saves_check | PASS | 225s | SAVES CHECK OK |
| title_check | PASS | 363s | TITLE CHECK OK |
| device_check (whole) | PASS | 194s | device_check: OK |
| fixtap_probe (off copy) | PASS | 42s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 31s | 311 rows; only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 73s | every case the same off and on; errors [] |

## appt_check: NEW FAIL

On the candidate:
```
FAIL brennan-book (brennan): the join offered, None leading it
FAIL brennan-book (brennan): a tap on None joins you and opens the scene
FAIL brennan-book (brennan): kept
FAIL brennan-book (brennan): in the Record
FAIL rules: the scope's after line said once the next day ([])
FAIL fixes: a tap on Brennan opens her scene
```
(booked, Day 4 14:30, the Schedule, the host at work, heads-up and Mail all ok.)

On OLD (d7ad4c58) the same lines pass: "the join offered, brennan leading it", "a tap on brennan joins you and opens
the scene", "kept", "in the Record", "rules: the scope's after line said once the next day (["Sato says you didn't
touch the focus. She's very impressed."])". The whole OLD run ends APPT CHECK OK (only its usual 4 planted lines). So it is NEW.

TB6 bisected it (its message to R4): EV997_LIGHT_ON (the Last Light, Day 4 14:00-14:40, over the 14:30 booking); off
on a copy, the invite part passes; TRAD997_ON and CAL997_ON off do not help. EV1's to fix. Reported to BM26 and lead 49.

Result: **R4: FAIL: appt_check (Brennan's book has no leader on Day 4; Sato's after line missing), NEW.** Everything
else OK.
