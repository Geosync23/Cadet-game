# CR2 results: 0.63.5 candidate 1e70683 (claude/p5-cand-s5)

1e70683 = 0.63.4 aa4f42c + BM8's mech_check fix 4e0c385 + X2/X3 claude/crew-pt1 79959ff (crew pieces 0.71.3-0.71.6, X3's interactions_check fix). Run 2026-10-19 ~09:13-09:55 by CR2 for BM8: checks from a detached worktree of 1e70683, each with its own CADET_WORK, at most two browser checks at once.

| check | result | time | last line |
|---|---|---|---|
| smoke | PASS | 77s | SMOKE OK |
| newgame | PASS | 38s | NEWGAME OK |
| day_check 4 | PASS | 330s | DAY CHECK OK |
| intro_check --week | PASS | 427s | OK |
| day_check 5 | PASS | 396s | DAY CHECK OK |
| device | PASS | 229s | device_check: OK |
| food | PASS | 101s | FOOD CHECK OK |
| clothes | PASS | 156s | ALL OK |
| day_check 6 | PASS | 392s | DAY CHECK OK |
| deck | PASS | 148s | DECK CHECK OK |
| tiles | PASS | 131s | ALL OK |
| day_check 7 | PASS | 379s | DAY CHECK OK |
| join | PASS | 196s | JOIN CHECK OK |
| leave | FAIL | 23s | LEAVE CHECK FAILED |
| arc | PASS | 20s | ARC CHECK OK |
| path | PASS | 85s | PATH CHECK OK |
| disc | PASS | 138s | ALL OK |
| day_check 8 | PASS | 324s | DAY CHECK OK |
| events | PASS | 207s | EVENTS CHECK OK |
| bubble | PASS | 254s | BUBBLE CHECK OK |

19 PASS, 1 FAIL.

**leave FAIL**, the only FAIL line: `FAIL the Works crew don't use the clock: [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1]` (clock stops in planDay(p, 10) per Works crew member; the rule wants every one at least 1 and three quarters (8 of 11) at 2; here 7). Passed on 0.63.4 (92d40d5). BM8 placed it: 2bc08d5 + X2 6c26c72 alone fails with the same numbers (X2's varied mornings vs the time clock's 6-minute wait); sent to X3.

## Re-run on ee9f9ed (= 1e70683 + X3's 0.71.7 6a4e153: Works clock-out waits 20 min)

For BM8, ~10:27-10:50, from a detached worktree of ee9f9ed, own CADET_WORK each, two at a time. (BM8 re-ran leave, day 0-3, cadet, interactions.)

| check | result | time | last line |
|---|---|---|---|
| day_check 4 | PASS | 357s | DAY CHECK OK |
| day_check 8 | PASS | 375s | DAY CHECK OK |
| events | PASS | 317s | EVENTS CHECK OK |
| day_check 5 | PASS | 353s | DAY CHECK OK |
| food | PASS | 97s | FOOD CHECK OK |
| deck | PASS | 144s | DECK CHECK OK |
| day_check 6 | PASS | 304s | DAY CHECK OK |
| day_check 7 | PASS | 201s | DAY CHECK OK |

All 8 PASS.
