# 0.98.0 full round: R4 (BB1)

- NEW: claude/staging-pad 7a2ae7d2, game sha256 22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f (matched BM20's).
- OLD: 0.97.0 claude/integration 610ad7f1, game sha256 0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f.
- Run 2026-10-29 from a detached worktree at 7a2ae7d2, CADET_WORK /tmp/work-r4, one check at a time, in the share's order.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole, alone, no time limit) | OK | INTERACTIONS CHECK OK |
| career_check | FAIL, known old (backlog 12) | `FAIL busy: "Relied on" before Day 5`, the only FAIL |
| appt_check | OK | APPT CHECK OK (its "planted" FAIL lines are its own self-test of planted faults, as expected) |
| saves_check | OK | SAVES CHECK OK |
| day_check 6 | OK | DAY CHECK OK |
| day_check 8 | OK | DAY CHECK OK |

## The one FAIL
career_check `busy: "Relied on" before Day 5`: **known old (backlog 12)**. Proof: career_check on OLD (0.97.0, sha256
0bd1b5b6...) fails with the same single line (`FAIL busy: "Relied on" before Day 5`, then CAREER CHECK FAILED).

R4: OK (known old only).
