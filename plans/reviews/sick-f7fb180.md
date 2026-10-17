# Re-check: f7fb180 (0.61.10), the missed-shift warning back

Reviewer 1d, 2026-10-17. This covers the open items from sick-9268f00.md and its 1612d2b addendum.

## Verdict: PASS WITH FIXES (one MEDIUM left: the checks flicker)

- **Fixed.** `if (!(c.k & 2)) { c.k |= 2; careerTip('missed'); }` is on its own line again (`careerMissed`), and leave_check asserts `k & 2` after the first miss.
- **Still open, now MEDIUM: leave_check flickers.** I ran leave_check on f7fb180 three times: FAILED once, OK twice. The failure:
  `FAIL a sick note gave back 0 for a miss that took 0`

  - The case's miss never happened.
  - The likely cause: `gs` is random per game (`Date.now() ^ Math.random()`) even on the checks' URL (`?nosave&debug`), so on some runs the test day rolls as a sick day. A sick day is excused, so there's no miss.
  - Any check that steps the player past day 7 (events_check runs to day 100 and beyond) can flicker the same way.

  **Fix (one condition in `careerInit`):** `gs: NOSAVE ? 0 : (Date.now() ^ Math.floor(Math.random() * 2147483647)) | 0`. Checks are then deterministic, and real games still vary. leave_check's "two seeds differ" case can set `gs` by hand.
- My earlier LOW (players who skip the arrival share sick days) is gone since 0.61.9's `gs`.
