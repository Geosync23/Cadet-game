# Re-review: claude/social c9ffe12..f05d7db (0.36.38-0.36.39: leavers from the sim, aboard always asked, gifts for every tag)

Reviewer 1, 2026-10-17. Section 20 only. name_check OK; `node --check` passes, because the bug below happens at run time, not when the file is read.

**Verdict: BLOCK** (a one-line fix).

## 1. BLOCK: `socP` was deleted but `leavingSoon` and `newHere` still call it
- 0.36.38 rewrote `socAboard`, `leavingSoon` and `newHere` and dropped the line `const socP = x => ...`. Both functions still use `p = socP(x)` as their default argument, so every call without a person throws `ReferenceError: socP is not defined`.
- Proven in the browser (`?nosave&debug`, f05d7db): `chatLine(tomas)` throws "socP is not defined", and so do `leavingSoon('tomas')` and `newHere('tomas')`.
- Effect in play: `chatLine` computes `ctx.newHere` and `ctx.leaving` first, so the chat card's line can't be made for anyone. `socialSeek` calls `leavingSoon(p)` once a ship minute for every crew member you know who's nearby, inside `socialTick` in the main loop, so the error is thrown from the frame loop as soon as you stand near someone you've met.
- Fix: put back `const socP = x => x && x.id ? x : (socInit(), SOC.idx.has(x) ? SOC.crew[SOC.idx.get(x)] : null);` and run social_check before pushing (it would have caught this: its "Coming and going" part calls `leavingSoon`).

## Otherwise (checked, fine once 1 is fixed)
- `socAboard` now always asks section 14's `aboard(p, d)`. For crew that is `guestStay(p, d) !== 'away'`, which returns 'in' for anyone who isn't a guest, so nobody disappears. Leave and arrival days come from `crewLeaving` / `crewArriving` when the sim has them (each call in try), else the roster's window. That fixes the "leavers never leave" finding once the sim's names are confirmed.
- Every gift tag now has items (music and game included); the new machine-shop items are in `GIFT_MAKES`.
- The farewell on a weekday at 19:45-20:30 still sits before quiet hours.
