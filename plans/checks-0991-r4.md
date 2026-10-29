# 0.99.1 full round: R4 notes

Runner R4, 2026-10-29. Same share as 0.99.0 (plans/round-0990.md R4): interactions_check (whole, alone, no time
limit), career, appt, saves, title_check, day_check 6, 8. Change in this build: the title screen starts asleep.

- Candidate: claude/staging-0991 f77c26d9525395a290e2b902fedcbf09f4849364,
  game sha256 8e4ac5459ca78df284390d9438c09b7118ce5448d4c0093dbf9b894bf19e2d9d (matches BM21's).
- OLD: 0.99.0 claude/integration 6d5684ba, sha256 041a699c00cb28607d97ef4f8add5594b47b6e204294f9b93aab7e82adad4ee2 (matches).
- Two browsers at most, each its own CADET_WORK; interactions_check ran alone after the rest finished.

| Check | Result | Time | Key lines |
|---|---|---|---|
| career_check | PASS | 251 s | CAREER CHECK OK |
| appt_check | PASS | 1017 s | APPT CHECK OK (its usual 4 `FAIL planted` lines are its own planted-fault runs) |
| saves_check | PASS | 280 s | SAVES CHECK OK |
| title_check | PASS | 263 s | TITLE CHECK OK; `the gate: asleep, only the wake line shows`; `a key wakes it ..., nothing chosen`; `pad: a press wakes the gate, nothing chosen` |
| day_check 6 | PASS | 467 s | DAY CHECK OK |
| day_check 8 | PASS | 464 s | DAY CHECK OK |
| interactions_check (whole, alone) | PASS | 2464 s | INTERACTIONS CHECK OK |

No real FAILs, so no OLD runs needed. Result: **R4: OK**.
