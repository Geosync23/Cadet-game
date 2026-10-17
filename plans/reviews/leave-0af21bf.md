# Skim: claude/leave 0af21bf (0.61.12): a New game no longer starts sick

Reviewer 1e, 2026-10-17. A skim of the code and the test. I didn't run it.

## Verdict: PASS

- `sickToday` now needs `sd > 0`, so a fresh `sd = 0` means "never", not "sick on day 0, the arrival day".
- The sick-note refund (`c.md > 0 && c.md === d`) is guarded the same way.
- I looked at every other `sd`/`md` comparison:
  - `sickDue` already treats `!c.sd` as "never ill".
  - `careerTick`'s `c.sd !== d` can't start a sickness on day 0, because `d > CAREER.grace` is needed first.
  - The get-well lines return early on `!c.sd`.
- **The new leave_check case:** day 0 at 17:40, after `careerTick`. It checks that you're not sick today, not sick now, at stage -1, that the card is hidden and that day 0 isn't excused. That matches the bug. It hides a sick card left open by the case before it, which is fine.
- **Consistency:** player 0.28.47 (48f66e8) carries the same `sd > 0` line, as 0.60.5a did, but with a different comment. When both are merged, expect a small conflict on that one line. Either side is fine.
