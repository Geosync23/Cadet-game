# CR2 results: 0.63.4 candidate 92d40d5 (claude/p5-cand-s4)

Second check runner (CR2), final round, 2026-10-19 ~08:01-08:25. Each check ran with its own CADET_WORK (/tmp/cw2/<tag>-<check>), at most two browser checks at once, CADET_CHROME=/opt/pw-browsers/chromium, from a detached worktree of 92d40d5 (smoke and newgame from plans/build-master/ with cadet_test.py copied beside them).

| check | result | time | last line |
|---|---|---|---|
| smoke | PASS | 82s | SMOKE OK |
| newgame | PASS | 36s | NEWGAME OK |
| events | PASS | 307s | EVENTS CHECK OK |
| device | PASS | 217s | device_check: OK |
| food | PASS | 106s | FOOD CHECK OK |
| clothes | PASS | 158s | ALL OK |
| arc | PASS | 21s | ARC CHECK OK |
| deck | PASS | 147s | DECK CHECK OK |
| path | PASS | 86s | PATH CHECK OK |
| tiles | PASS | 136s | ALL OK |
| disc | PASS | 139s | ALL OK |
| bubble | PASS | 287s | BUBBLE CHECK OK |
| join | PASS | 120s | JOIN CHECK OK |
| leave | PASS | 17s | LEAVE CHECK OK |

All 14 PASS. BM7 ran the other half (interactions, cadet, career, mech, machine, puzzle, social, lines, player, day 0-8, intro --week).

## Second half for BM8: claude/p5-cand-s4 c336170 (game file = 92d40d5)

Run one after another, each with its own CADET_WORK, from a detached worktree of c336170, ~08:27-08:45.

| check | result | time | last line |
|---|---|---|---|
| day_check 5 | PASS | 205s | DAY CHECK OK |
| day_check 6 | PASS | 209s | DAY CHECK OK |
| day_check 7 | PASS | 199s | DAY CHECK OK |
| day_check 8 | PASS | 209s | DAY CHECK OK |
| intro_check --week | PASS | 212s | OK |

All 5 PASS.
