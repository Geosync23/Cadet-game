# 0.99.5 full round: R4 notes

Runner R4, 2026-10-31. Share: interactions_check (whole, alone, no time limit), career, appt (OB2's appointment
changes are inside appt_check), saves, title_check, device_check (whole), day_check 6, 8, 16, 23, 24.

- Candidate: claude/staging-0995 e00bfabd8cefbfd66c5c71f2a22676c763a7eb8d,
  game sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matches BM23's GO; lead 48 confirmed
  the earlier 5733867d number was superseded).
- OLD: 0.99.4 claude/staging-0994 596712bc, sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matches).
- Two browsers at most, each its own CADET_WORK (/tmp/work-r4, /tmp/work-r4b); interactions_check ran alone after the
  other ten finished, started directly.

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 527s | DAY CHECK OK |
| day_check 8 | PASS | 489s | DAY CHECK OK |
| day_check 16 | PASS | 492s | DAY CHECK OK |
| day_check 23 | PASS | 514s | DAY CHECK OK |
| day_check 24 | PASS | 542s | DAY CHECK OK |
| career_check | PASS | 284s | CAREER CHECK OK |
| title_check | PASS | 612s | TITLE CHECK OK |
| appt_check | PASS | 1191s | APPT CHECK OK |
| saves_check | PASS | 287s | SAVES CHECK OK |
| device_check (whole) | PASS | 192s | device_check: OK |
| interactions_check (whole, alone) | PASS | 2609s | INTERACTIONS CHECK OK, no FAIL lines |

appt_check prints its usual 4 `FAIL planted ...` lines (scope x3, teach-me x1): its own planted-fault runs on a broken
copy, proving it catches them; the check ends OK.

No real FAILs, so no OLD comparison runs were needed. Result: **R4: OK**.
