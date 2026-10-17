# Review: claude/leave 0.61.18 (ea89382), leaving early is a short shift

Reviewer 1f, 2026-10-17. Builder: career engineer (session_01862tURG1qXAVGj2sdUrVCw). Base: da6abc6 (0.61.17, PASS).

**Verdict: PASS** (one LOW, a design call for the lead; nothing to fix before combining).

## What changed
- `careerClock`: clocking out before 15:00 (`CAREER.earlyOut` 900) gives `repAdd(null, 0, { work: -2 }, 'early')`, an extra toast sentence and a `clock.early` remark (falls back to `clock.out`; the key is on claude/content in `banks/clock.lines` and two voices).
- `careerFullDay(d)`: true in the first week, with no clock record, if never clocked out, or out from 15:00.
- The run of missed shifts (`c.ms`) and the Chief's re-arm (`c.ca`) now reset in `careerDayEnd` for a full worked day, not at 12:30 in `careerTick`'s loop.

## Checked
- **Never a miss:** clocking in sets `c.on = d` (via `careerAtWork` / `careerStarted`), and the miss test in the loop only looks at `c.on !== k`. An early clock-out doesn't touch `c.on`, so a short shift can't count as a miss, even when you clock out before 12:30.
- **One dip a day:** `careerClockedOut(d)` refuses a second clock-out, and you can't clock back in after clocking out. With shiftStart's on-time +1, a short shift nets about -1.
- **Order:** `careerDayEnd(k)` runs on the first tick of day k+1, after `careerLadder` in the same loop step. `c.ci`/`c.co` are still day k's then, because you can't clock in before 07:00. When several days are caught up at once (a time jump), only the last worked day can have `c.on === k`, and its clock record is still the latest one. So `careerFullDay` reads the right day.
- **Moving the reset from 12:30 to the day's end:** on a worked day, `c.ms` stays as it was until midnight. It can only reach `chiefRun` (3) on a missed day, and by then the Chief has fired (`c.ca = 1`), so the later reset never books a second Chief. The Captain's step reads work, not `ms`.
- **Forgot to clock out:** `careerTick` signs you out at 17:00 (`co` = 17:00) before the loop runs, so that day is full.
- **Saving:** no new saved field. `R.cnt.early` is a new counter in `SHIP.rep.cnt`, which saves as an open map; no `REP_TAGS` entry reads it, so nobody is "known for" early finishes.
- **leave_check on ea89382:** see the result below.

## Findings
**LOW (design, for the lead): honesty costs more than walking off.** If you clock in and walk away without clocking out, the clock signs you out at 17:00 with "no harm done": a full day with no dip, and it ends the run. Clock out yourself at 14:00 and you get -2 and the run stays. So a player learns that the time clock is better left alone. Possible fixes, if the lead wants one:
- (a) Treat the 17:00 auto sign-out as full only if you were on Deck 5 (or in a Works room) at some point after 15:00.
- (b) Accept it as cozy and forgiving, and leave it as it is.

My lean is (b) for now, because the dip is small and the forgiving sign-out was the user's earlier choice. I'm raising it so the lead knows.

## leave_check
LEAVE CHECK OK on ea89382 (run by 1f, about 25 minutes), including the two new lines: out at 10:00 gives a dip and keeps the run with no miss; out at 16:00 ends the run.

## Follow-up: 0.61.19 (7c07465) and 0784b54
**PASS (skim).** 0.61.19 re-bakes head writer 5's `clock.early` lines from content 0.48.80 (d494709, PASS). The `content/clock` and `banks/clock.lines` files are identical to d494709's, and the html diff is the baked lines plus the build number. 0784b54 changes only `plans/handover-career.md`. So the range da6abc6..0784b54 passes.
