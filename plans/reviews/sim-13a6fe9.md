# Review: claude/sim-engineer e4d6ace..13a6fe9 (+ 0d3def9 docs) (0.26.38: farewell friends, leavers' spots held, couples together in a crowd)

Reviewer 1c, 2026-10-17. Diff: `git diff e4d6ace 13a6fe9` (sections 14 and 10, DEV_NOTES, the sim handover). Tested on **sim 13a6fe9 + social-stories 26ed2a0 (20c's `farewellCrew`) + roster 1348dfd**, which has the real rotations. Only build-line conflicts, plus player_check's washer case.

**Verdict: PASS.**

## Checked
- **day_check day 161** (the busiest rotation: zamora-quinn, keane-davi and ueda-vera all leave) **and day 35** (teague-theo): DAY CHECK OK, both.
- **The plan itself, from `shipDay(d)`:**
  - a fresh game has no friendships, so `farewellCrew` returns [] and nobody gathers; that's correct;
  - so I gave each leaver a stand-in list of four friends from their own department.

  | Day | Leavers (14:30-15:00, 'leave') | Friends who came (14:32-15:02, 'farewell') | Spots booked twice |
  | --- | --- | --- | --- |
  | 161 | crowd-1, crowd-2, crowd-3 (the front spots) | 8 of 12, at crowd-4 to crowd-11; the rest were busy | none |
  | 35 | crowd-1 | 3 of 4, at crowd-2 to crowd-4 | none |

- **The `leave:<id>` hold** in `occ.res` comes before anyone is planned and matches no tag, so friends fill the spots round the leaver, never theirs. Generated crowd spots are plentiful, so the `|| bayL[0]` fallback for more leavers than spots can't happen with today's roster (at most 3 a day).
- **Couples in a crowd:** `take()` sorts the gather pool by distance from the partner's spot only when the partner already holds one then. The empty pool is still guarded (`if (!pool.length) continue`) before `pool[0].gather` is read.
- **Without 20c** there's no gathering, but the hold is still made. That only moves a leaver from a remembered or seeded bay spot to the front one, which is deterministic and harmless.

## Note (low)
- Friends stay until 15:01-15:02, a minute or two after the leaver boards at 15:00: they wave the shuttle off. That's fine; just mention it to social B2 in case a "goodbye" line is timed to 15:00.
