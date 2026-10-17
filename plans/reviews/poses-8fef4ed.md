# Review: claude/poses 0.27.47 (8fef4ed), no tray while waiting for a taken seat

Reviewer 1f, 2026-10-17. Builder: deck architect 3. Base: 157c0dd (0.27.46, PASS). A one-line behaviour fix, reviewed in full.

**Verdict: PASS.**

- **What changed:** in `mealStep`, after the queue, if a diner holds a tray and their planned seat is taken by someone else, and `elsewhere()` finds no free seat beside it, the tray is put away (`m.tray = false; m.trayLate = true; LINE_LOG.trays--`). The existing line after it gives the tray back once they're settled at a tray seat. It mirrors 0.26.32's queue-time rule.
- **Checked:**
  - `!(this.settled && this.spot.id === w.placeId)` keeps someone who is sitting in their own seat from losing their tray.
  - `LINE_LOG.trays` stays balanced (-- here, ++ on sitting).
  - If a diner were ever settled at a different tray seat while their planned seat stays taken, the two lines would undo each other in the same step: the tray stays, and the count is unchanged. That's harmless, and no worse than before.
  - `elsewhere()` only runs while the condition holds, which is rare.
  - The meal state isn't saved.
- **Evidence** (deck architect 3): day_check day 35 on cand-0606 with the fix has no tray failure; quist-ilse at 17:59 was the case. The remaining shift-short failure was there before and isn't from poses. claude/poses day 1 and day 35 OK; cadet_test vs 0.27.46 ALL IDENTICAL.
