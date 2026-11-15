# Round fable (candidate 1): share R2 (2026-11-15)

- Candidate 1: claude/staging-fable-review c4999dae, label 0.99.92-review, game sha256
  d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0 (matched before and after the runs). Check files from c4999dae.
- OLD: 0.99.91, main cdd9efd, game sha256 b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (matched).
- Build master BM29, lead 52. Each check run once, on the candidate; OLD only for the one that failed.
- Not run here by the round's plan: cadet_test and plain lines_check (BM29's runs on this exact file are the round's runs).
- All-off copy for the pf_f1 proof: 60 switches false, each found exactly once: the 39 up to 0.99.91 (my predecessor's
  list), FR1's 9 (LIB_SAY_ON's indented line included) and the 12 FRP switches. TEX_READ_ON was already off.

## Results

| Check | Result | Key lines | "skipped" lines | Minutes |
|---|---|---|---|---|
| intro_check (whole) | OK | exit 0, last line `OK` | 0 | 42 |
| intro_check --dinner | OK | exit 0, `OK` | 0 | 2 |
| intro_check --firsts | OK | exit 0, `OK` | 0 | 1 |
| path_check | OK | `A played day: 2865/2865 real calls the same`; `PATH CHECK OK` | 0 | 1 |
| arc_check | OK | `errors []`; `ARC CHECK OK` | 0 | 0 |
| lines_check --day | **FAIL, the same on OLD** | `ERROR other talk on screen during a conversation (1 seconds)`; `lines_check --day: FAIL (1 errors)`; exit 1 | 0 | 4 |
| day_check 0, 1, 5, 7, 21, 22 | OK, all six | each `errors []`, `DAY CHECK OK` | 0 each | 5 each |
| arrows_check endgo | OK | `missed 0, stuck 0`; `ARROWS CHECK OK` | 0 | 10 |
| pf_f1_same 0.99.91 vs candidate, 10 days | OK by the agreed rule | `F1 checks 23674 mismatches 0`; `page errors [] []`; fingerprints 30, differ 25 (OLD lacks the new switches, so by design; prints FAILED for that reason only) | 0 | 1 |
| pf_f1_same 0.99.6 (d7ad4c58) vs the all-off copy, 10 days | OK | `fingerprints 30 differ 0`; `F1 checks 23674 mismatches 0`; `page errors [] []`; `PF F1 SAME OK` | 0 | 1 |

No check had a "skipped" line.

## The one FAIL: lines_check --day

- Candidate: `ERROR other talk on screen during a conversation (1 seconds)`, exit 1.
- OLD (0.99.91, in its own worktree at cdd9efd, so it read its own words files): the same error,
  `other talk on screen during a conversation (3 seconds)`, `lines_check --day: FAIL (1 errors)`, exit 1.
- The day's spoken lines are the same list on both builds, line for line, but for one line a ship minute later on the
  candidate (Calder's "Card in the clock, cadet..." at 10:29, was 10:28). The six visits are the same.
- So it fails the same way on OLD with the same message: old, not caused by the candidate. But it is **not on the
  known-old list** (backlog 14 and 23 only), and it has no backlog row that I know of.
- Round 09991b's R2 recorded lines_check --day as PASS on this very OLD file (b321a4ec...), so the check's result
  depends on the run (it counts real seconds in which a passing remark and a conversation are both on screen). It looks
  like a check that flickers, to be reported either way rather than waved through. I did not rerun it (the rule: once).

## Result

R2: every check OK except lines_check --day, which FAILs the same way on OLD (0.99.91). No failure new to the candidate.
