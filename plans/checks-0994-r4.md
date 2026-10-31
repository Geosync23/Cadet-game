# 0.99.4 full round: R4 notes

Runner R4 (fresh seat), 2026-10-31. Share: interactions_check (whole, alone, no time limit), career, appt, saves,
title_check, day_check 6, 8, 23, 24.

- Candidate: claude/staging-0994 8976965effdbff3473a85f31b4deb7c7f3a4a669,
  game sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matches BM22's GO; STORIES2_ON = true).
- OLD: 0.99.3 claude/integration 57eceec4, sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9
  (matches); setup smoke run: career_check on OLD, CAREER CHECK OK.
- Two browsers at most, each its own CADET_WORK (/tmp/work-r4, /tmp/work-r4b); interactions_check ran alone after the
  other eight finished.

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 346 s | DAY CHECK OK |
| day_check 8 | PASS | 330 s | DAY CHECK OK |
| career_check | PASS | 192 s | CAREER CHECK OK; `busy: "Relied on" from Day 4 (expected: the calendar sets the pace)`; backlog 12 does not show |
| title_check | PASS | 438 s | TITLE CHECK OK |
| appt_check | PASS | 844 s | APPT CHECK OK |
| day_check 23 (story day) | PASS | 340 s | DAY CHECK OK |
| day_check 24 (story day) | PASS | 242 s | DAY CHECK OK |
| saves_check | PASS | 176 s | SAVES CHECK OK |
| interactions_check (whole, alone) | PASS | 2000 s | INTERACTIONS CHECK OK |

appt_check prints 4 `FAIL planted ...` lines (scope x3, teach-me x1): its own planted-fault runs on a broken copy,
proving it catches them (same 4 as in the 0.99.0 round); the check ends OK.

No real FAILs, so no OLD comparison runs were needed. Result: **R4: OK**.
