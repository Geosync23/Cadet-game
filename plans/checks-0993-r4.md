# 0.99.3 full round: R4 notes

Runner R4, 2026-10-30. Same share as 0.99.0 (plans/round-0990.md R4): interactions_check (whole, alone, no time
limit), career, appt, saves, title_check, day_check 6, 8. Changes in this build: mess hall sound; the Day 0 dinner's
Chief on the cards; the call-home card after you eat; the original title song back.

- Candidate: claude/staging-0993 df74ce0fbf33f40bb2cee71369ef589871a1eb94,
  game sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matches BM21's).
- OLD: 0.99.2 claude/integration d180a704, sha256 27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matches).
- Two browsers at most, each its own CADET_WORK; interactions_check ran alone after the rest finished.

| Check | Result | Time | Key lines |
|---|---|---|---|
| career_check | PASS | 219 s | CAREER CHECK OK |
| appt_check | PASS | 862 s | APPT CHECK OK (its usual 4 `FAIL planted` lines are its own planted-fault runs) |
| saves_check | PASS | 269 s | SAVES CHECK OK |
| title_check | PASS | 305 s | TITLE CHECK OK |
| day_check 6 | PASS | 352 s | DAY CHECK OK |
| day_check 8 | PASS | 369 s | DAY CHECK OK |
| interactions_check (whole, alone) | PASS | 2052 s | INTERACTIONS CHECK OK |

No real FAILs, so no OLD runs needed. Result: **R4: OK**.
