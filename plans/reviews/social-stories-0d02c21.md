# Re-review: claude/social-stories 8829736..0d02c21 (0.39.20)

Reviewer 1, 2026-10-17. **Verdict: PASS.**

- The only game change is `AFF_SNAP_MAX` 300 -> 600 (plus the build line), the lead's ruling: |aff| >= 30 stays the rule, the 600 is a safety ceiling. Read in the diff; nothing else in the game file changed.
- Social B2 reports a peak of 585 qualifying pairs over 140 days, so the ceiling never binds before day 140, and the snapshot is byte-identical to 47b02d6 on days 56-70, 135 and 140 (so seating is back to the plain ±30 rule).
- Headroom, for the lead: with the ceiling at 600 the affWeek part grows to about 4.8 KB, which puts the social save near 27.9 KB at day 140 (my 8829736 review's estimate from 25.5 KB measured with `social_check --long`). That is about 2 KB under the 30 KB budget, and 585 pairs is close to the 600 ceiling, so past day 140 the ceiling will start to bind. Social A's `--long` check (day 140, 30,000 B) is the guard; it should also run on the combined build.
- DEV_NOTES now says 25.5 KB with a player (0cc815f), as asked.
