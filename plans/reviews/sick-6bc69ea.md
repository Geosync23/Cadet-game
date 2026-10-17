# Skim: the sickness words (claude/leave 4dd0409, 0.61.7) and the leave_check fix (6bc69ea)

Reviewer 1d, 2026-10-17. 4dd0409 bakes head writer 4's words. 6bc69ea changes only leave_check.

## Verdict: PASS (content only, light look)

- **Game code:** the only changes are the build number and the re-baked blocks.
- **The bake:**
  - `content_gen.py --check`: up to date (6864 lines, 16 meetings).
  - lines_check: PASS (0 errors, 4 warnings, none in the new sick lines).
- **leave_check at 6bc69ea:** OK.
  - The get-well and glad-you're-better lines now come.
  - The 6bc69ea fix is sound: the lines are for acquaintances and up, so the check now uses someone who knows you.
- **My probe (sick-6bc69ea-probe.py):** unwell on day 51 in the infirmary (3-visit-1). The exam `moment:sick:51` plays, with 7 lines. All of sickExam1-3 and sickExamCover are baked.

The lows from sick-b0c0f37.md still stand (the refund overshoot, the same sick days in every game, walking at 26% at the worst).
