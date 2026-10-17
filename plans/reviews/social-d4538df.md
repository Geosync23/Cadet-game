# Re-review: claude/social f05d7db..d4538df (0.36.40-0.36.41)

Reviewer 1, 2026-10-17. **Verdict: PASS.** The BLOCK is lifted.
- `socP` is restored. In the browser, `chatLine(tomas)` gives a line, and `leavingSoon` / `newHere` answer (`null`, `false`).
- `typeof introOn` is inside the try.
- The reserve test uses the game's own `ROSTER_RESERVE`. On a scratch merge with the crew designer's f7a18d2 (86 crew), social_check is **OK**: the reserve case passes, there are no errors, and name_check is OK. `name_check --branches f05d7db d4538df`: OK.
- The leavers finding is fixed from 0.36.38 (`leaveDay` / `arriveDay`), once the sim engineer confirms `crewLeaving` / `crewArriving`.
