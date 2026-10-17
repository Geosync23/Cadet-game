# Re-review: claude/deck-plans-1-2-6 f7a18d2..98df62f (0.16.13: replacements and fixed leavers, mentors, couples)

Reviewer 1, 2026-10-17. **Verdict: PASS.**
- **Generator:** re-running it gives a byte-identical game file and roster page.
- **"Nothing else changed":** against 0.16.12, the only roster changes are the new `mentors` field (everyone), the leavers' `aboard`, and three people's days off (Mateo Navarro, Farah Rahman, Carmen Chen), so all four couples now share a day off. Staffing still covers every department and shift every day; everyone has two days off in a row; Torres, Calder and Halloran are as agreed.
- **Rotations:** 12 leavers over the six Sundays (days 35-245), each with `aboard: [null, day]`. Each is replaced by a reserve person with the same role (or its cadet version), who takes the leaver's bed and has `aboard: [day, null]`. No story crew and nobody with `stays` leaves, and no couple is split.
- My earlier theme-id and gift findings are settled: the designer made this branch's spellings canonical, and social A added gift items for every tag.
- **For the sim's 0.26.25 (to check then):** on a rotation day the leaver and the arrival are both "aboard" by day (`d <= aboard[1]` and `d >= aboard[0]`) and share one bed. The sim says its bed check is by time; day_check on a rotation Sunday (day 35) should show the leaver gone by the farewell and the newcomer in the bed that night. `ROSTER_ROTATIONS.out` is now a list of ids, not a count; nothing reads it yet (the sim's 0.26.25 will be first).
