# Re-review: claude/player-needs 7959655..9c18045 (0.28.38-0.28.40: my lows, the till and the full locker, someone stepping aside)

Reviewer 1c, 2026-10-17. Diff: `git diff 7959655 9c18045` (section 15, player_check, DEV_NOTES). Tested on galley 40166d6 + sim bfcd864 + player 9c18045 (merged as before).

**Verdict: PASS.** The job-loop part can only be proven once sim 0.26.36 (`crewMakeWay`) is final; I'll rerun it then, with food_check on galley 0.29.34.

## Checked
- **cadet_test, 0.28.37 merge vs 0.28.40 merge: ALL IDENTICAL.**
- **player_check on the merge:** everything passes except the job loop's 5 (the cook on the range panel, galley + sim's, fixed by sim 0.26.36), which are exactly as before. The new cases pass:
  - **the real line on a combined build:** from [19,10], 15.8 tiles away, you're never in `servLine()` while walking, you're in it while queueing, and you're served ("curry and rice"). This is the case I asked for.
  - **someone in the way:** a refused first walk goes to `wait`, then `walk`, `in`, `do`. The stand-in `crewMakeWay` is released 0 times before you get up and once after. Release also happens on every other way out: `actEnd` (a wait over 8 s, a tap elsewhere, a lift), and the walk-off path.
  - **the till:** with 1 credit, no sale and nothing in the locker. **A full locker** keeps the new comfort and drops the oldest.
- **My three lows:**
  - the tray clears on a sleep or time skip, and once you're off Deck 3;
  - the toast can no longer say "null";
  - the strip's pulse now only changes the low icons' opacity, in tenths, with no rebuild.

## Note (low)
- With no dish, `dishName` turns the tray into "the hot meal", so you'd get a meal from an empty servery rather than no tray. That can't happen today: `galleyTurn` already requires `galleyCanServe` in the same tick as `foodFrom`. If it ever can, end the queue with `A.o.why` and no tray instead.
- When sim 0.26.36 lands, make sure its release function can be called twice safely. `actEnd` and the walk-off path can both reach it for one stepping-aside.
