# CR2 results: 0.64.0 rec deck combine 3add6bf (claude/rec-cand-s1)

3add6bf = 0.63.5 final be3d7ee + RB2 f319ab3 + RA 9dfe971 + W3 a095799 + RB2 87e3c5f; REC_DECK = true. Run 2026-10-19 ~12:50-13:23 by CR2 for BM8, then BM9: checks from a detached worktree of 3add6bf, each with its own CADET_WORK, two at a time. **Stopped part-way at ~13:23: the user asked to pause all work (lead 19).**

Note: day_check.py exits 0 even when it prints DAY CHECK FAILED, so read the last line, not the exit code.

| check | result | time | last line |
|---|---|---|---|
| day_check 0 | PASS | 535s | DAY CHECK OK |
| day_check 1 | FAIL | 543s | DAY CHECK FAILED |
| day_check 2 | FAIL | 535s | DAY CHECK FAILED |
| day_check 6 | PASS | 523s | DAY CHECK OK |
| day_check 7 | PASS | 550s | DAY CHECK OK |
| day_check 8 | FAIL | 551s | DAY CHECK FAILED |

Each FAIL has a single FAIL line: `FAIL work: ['volkov-maeve 476/480']` (shift short by 4 min); no stuck crew, draw calls peak 253 or less, errors []. Weekdays fail, weekend days (0, 6, 7) pass. BM9 placed it: the two lift rides on Maeve's rec round (REC_ROUND, from 9abd51f) are planned as commute in the middle of her shift. RC is fixing it in the planner, and the day set will be re-run on RC's hash.

- **Stopped part-way (killed at the pause):** day_check 3, day_check 21.
- **Never run:** day_check 4, 5, 14 and 28 (BM9 dropped them until RC's hash lands); events, intro_check --week, join, food, clothes, smoke, newgame, leave, bubble, tiles, path, arc.
