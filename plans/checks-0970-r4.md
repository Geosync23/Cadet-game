# 0.97.0 full round: share R4 (2026-10-28/29)

- Candidate (NEW): claude/staging-pad b9b7e3d7bdee47016477770349c5bfa7e8fc84e1, game sha256
  0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f (matches BM20's).
- OLD: 0.96.0, claude/integration fe11cd66, game sha256 332925003934b49686c080515e154131a07f7fe7a3c14fbe0f6f7684933a129e.
- Two lanes, each with its own CADET_WORK (/tmp/work-r4, /tmp/work-r4b): lane A interactions_check alone, detached,
  no time limit; lane B the rest one at a time. CADET_CHROME=/opt/pw-browsers/chromium.

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| interactions_check (whole) | OK (exit 0) | 64 | `INTERACTIONS CHECK OK`; no FAIL lines |
| career_check | FAIL, known old (exit 1) | 4 | `FAIL busy: "Relied on" before Day 5` (the only FAIL); `CAREER CHECK FAILED` |
| appt_check | OK (exit 0) | 20 | `APPT CHECK OK` |
| saves_check | OK (exit 0) | 5 | `SAVES CHECK OK` |
| day_check 6 | OK (exit 0) | 8 | `DAY CHECK OK` |
| day_check 8 | OK (exit 0) | 8 | `DAY CHECK OK` |

## The one FAIL

career_check `busy: "Relied on" before Day 5`: **known old (backlog 12)**. Proof: the same check on OLD (fe11cd66,
sha256 3329...129e, run during setup) fails the same way, with that line as its only FAIL.

Result: **R4: OK** (one known old FAIL, backlog 12).
