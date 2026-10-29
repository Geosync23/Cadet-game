# 0.99.0 full round: R4 notes

Runner R4 (fresh seat), 2026-10-29. Share: interactions_check (whole, alone, no time limit), career, appt, saves,
title_check, day_check 6, 8.

- Candidate: claude/staging-099 a4c9febe2264f02adf812602de5614a5f3130889,
  game sha256 041a699c00cb28607d97ef4f8add5594b47b6e204294f9b93aab7e82adad4ee2 (matches BM21's).
- OLD: 0.98.0 37b858b4, sha256 81c07a059437fd391370af0133b9fff8c35ae56ad4d31718151b7274acce59b1 (matches);
  setup smoke run: appt_check on OLD, APPT CHECK OK.
- Two browsers at most, each its own CADET_WORK; interactions_check ran alone after the rest finished.

| Check | Result | Time | Key lines |
|---|---|---|---|
| career_check | PASS | 240 s | CAREER CHECK OK; `busy: "Relied on" from Day 4 (expected: the calendar sets the pace)`; backlog 12 does not show |
| appt_check | PASS | 1043 s | APPT CHECK OK |
| saves_check | PASS | 268 s | SAVES CHECK OK |
| title_check | PASS | 269 s | TITLE CHECK OK |
| day_check 6 | PASS | 482 s | DAY CHECK OK |
| day_check 8 | PASS | 466 s | DAY CHECK OK |
| interactions_check (whole, alone) | PASS | 2516 s | INTERACTIONS CHECK OK |

No FAILs, so no OLD comparison runs were needed. Result: **R4: OK**.
