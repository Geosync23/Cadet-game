# 0.96.0 full round: share R4 (2026-10-28)

- Candidate (NEW): claude/staging-pad 6db1cdd2f7f47e76d4f46ba3f05843ec10900dd6
- Game sha256: c62d63999e6b596d21806d1cb14fa9ab3168a50c5038dfcc1c04f3163d37a74e (matches BM20's)
- OLD: 0.95.0, claude/integration b5199dc3, game sha256 b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a
- Setup: CADET_CHROME=/opt/pw-browsers/chromium, three.js r128 + acorn 8.12.1 in own CADET_WORK (/tmp/work-r4 for
  interactions, /tmp/work-r4b for the rest). Two browsers at most: interactions_check alone in one lane (detached,
  no time limit), the rest one at a time in the other.

## Results

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | OK (exit 0, 4410 s) | `INTERACTIONS CHECK OK` |
| career_check | FAIL, known old (backlog 12) | `FAIL busy: "Relied on" before Day 5` (the only FAIL), `CAREER CHECK FAILED` |
| appt_check | OK (exit 0, 1303 s) | `APPT CHECK OK` (its FAIL lines are the planted-fault self-test, each followed by "its part fails" ok) |
| saves_check | OK (exit 0, 355 s) | `SAVES CHECK OK` |
| day_check 6 | OK (exit 0, 540 s) | `DAY CHECK OK` |
| day_check 8 | OK (exit 0, 523 s) | `DAY CHECK OK` |

## FAILs

- career_check `busy: "Relied on" before Day 5`: **known old (backlog 12)**. Proof: career_check on OLD (b5199dc3,
  sha256 above) fails the same way, the same single line (`FAIL busy: "Relied on" before Day 5`, line 24), exit 1.

No NEW FAILs.

## Notes

- career_check ran twice on NEW: the first run's log was deleted by my own cleanup at the start (a setup slip, not
  the game); the second run is the one recorded above.
- At the start two copies of interactions_check were launched by mistake; both were stopped within a minute, their
  browsers cleaned up, and one copy restarted alone at 15:25:50. The recorded run is that single copy.
