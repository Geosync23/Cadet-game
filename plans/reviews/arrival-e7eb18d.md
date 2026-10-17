# Re-review: claude/arrival e16bd6a + e7eb18d (0.42.3-0.42.4, fixes for reviewer 1, introWanted / introNewGame / introSig)

Reviewer 1, 2026-10-17. Diff: `git diff 9881cbf origin/claude/arrival`. Section 21 only (plus the build line). intro_check OK on the branch and on a scratch merge with sim d45b03a (rerun here; the only conflict is the build line). name_check: no clash with sim. Section 21's `introOn` / `introNote` still clash with social A's 3d266bf. That rename is on social A's side; see social-3d266bf.md.

**Verdict: PASS WITH FIXES** (one new should-fix, from the fix for finding 4).

## Fixed (checked)
1. Flags: `introBegin` clears `INTRO_FLAGS`; the check has a second-arrival case and passes merged with the sim bus.
2. `introEnd` sets the end state: the device, Calder, every week gate (not the mug or the seedling).
3. Checkpoints need the room and `INTRO_REACH = 2`; the lift checkpoint moved; there's a data check for neighbours. The wanderer now misses 5 steps.
4. Waits count from `SHIP.intro.since` (saved, read defensively). The 10-minutes-behind player misses nothing.
5. `introBeats` uses the fallback's `until` (Calder until 20:00).
6. Days off: a WAITING line until the crew designer's change is in. Make it a FAIL in the combined build (0.60.0); informational on the branch alone is fine.

## NEW, SHOULD FIX: after one missed step, a normal walking pace loses the rest of the evening
- The catch-up rule (once the previous step was missed, wait only `min(5, wait)`) is shorter than the time it takes to walk between checkpoints. Walking a step at the pace your own "slow" case allows takes 6-7 ship minutes, about 10-12 real seconds.
- Proven on paper (the same loop as intro_check's, one slow step and then a steady pace):

  | Slow step | Then each step after | Missed |
  | --- | --- | --- |
  | haulway, 25 min | 7 min | haulway, works, lift, wing, bunk, toMess, servery (7) |
  | lift, 25 min | 6 min | lift, wing, bunk, toMess, servery (5) |
  | bunk, 35 min | 7 min | bunk, toMess, servery |
  | lift, 25 min | 4 min | lift only |

  One slow moment (looking round the shuttle bay, a missed lift) costs the bunk and the device handover, and the walk to dinner, even though the player is following him all the way.
- Fix ideas (pick one):
  - Keep the short wait only while you're not coming: use it when `here` is off the step's deck, or further away than at the last tick, and the full wait while you're closing in.
  - Or replace the 5 minutes with a budget: each step's wait is the full wait, capped so the remaining steps still fit before 20:00.
- Add the table above as an intro_check case ("one slow step, then a steady 7 minutes: misses only that step").

## Note (low)
- `introBeats` gives section 14 each step's nominal window (`at` to `at + wait`), but a step can now wait longer (from `since`). That's fine as long as section 10 gives `escortPlan` precedence over the plan while the intro runs, so Torres isn't walked off by his plan while the step still waits for you. Worth a line in the hook register for the sim engineer.
