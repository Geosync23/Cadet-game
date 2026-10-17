# Re-check: leave fixes (claude/leave 8f1f88a, 0.61.3)

Reviewer 1d, 2026-10-17. This re-checks the fixes for leave-492364d.md.

## Verdict: PASS

Every finding is fixed as proposed:

| # | Finding | Fix | Shown by |
| --- | --- | --- | --- |
| 1 | Older save: a false missed shift | `careerInit` takes `on` from today's `shiftStart` notes, else from `flag('shiftSent')` | My probe: work stays 50, `on` 10, no missed tip |
| 2 | A summons on a leave day | `careerDue` requires `playerShiftOn(d)` | My probe: no occasion on the leave day |
| 3 | Pell absent from the send-off | `careerSendoff.with = ['pell', 'calder']`; `occasionAdd` passes them to `apptAdd` | The code. No other occasion has `with`, so the others are unchanged. |
| 5 | leave_check's late days never scored | The check calls `repNote` | With real late scoring: the Chief on day 9, the Captain day 12, the last day 20 |
| 6 | The Chief's step overwritten | The ladder steps up only when `!c.q` | My probe: the Chief on day 16, then the Captain day 17 (was stuck) |
| 7 | A day lost at the cap | Cancelling always gives the day back | You can briefly hold 6, which is fine |
| 8 | DEV_NOTES save line | Now lists `q` and `qd` | — |

Finding 4 was kept as it is (the lead's call).

## What I ran on 8f1f88a
- **leave_check:** LEAVE CHECK OK, including my two cases.
- **My probe** (leave-492364d-probe.py):
  - Diligent and casual players: still no summons.
  - New game from the closing card: works.
- The diff is 17 lines of game code, all in the career block, plus one argument in `occasionAdd`. No other check is needed.
