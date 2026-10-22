# Review: "The bunk says it's too early" (DS1), claude/bunk-early 6b8bb392 (RV6)

Reviewer RV6 (session_018Jzc4LeoHvuahsS7VHAzn3), 2026-10-22, for lead 29. Builder DS1 (session_01MZBSf7MZeb9C89wpoavLko).
What: `git diff b9f053ba 6b8bb392`: section 15, two small edits, and player_check lines.
- (a) `bunkLie`: your own bunk by day still lies you down to rest; the words now start "Too early to sleep: you can turn
  in from 20:00." (bedtime() unchanged, 20:00-05:30).
- (b) `bunkTap`: another "Bunk" in the room you sleep in (same deck, same room as your bed) walks you there and shows its
  words plus " Yours is the next one."; bunks in other rooms fall through as before.

## Verdict: PASS (two small word points for the writer or the lead)

| Check | Result |
|---|---|
| cadet_test b9f053ba vs 6b8bb392, alone | ALL IDENTICAL |
| player_check | PLAYER CHECK OK (by day: "Too early to sleep..."; bedtime at 19:59/20:00/05:29/05:30; Tomas's bunk says "Yours is the next one", Pell's in Bunk 2 doesn't) |
| check_fast on 6b8bb392 | (running; DS1 reports QUICK CHECK OK) |
| Planted faults (be_*, 4) | 4 of 4 caught: the old words; any room; no "Yours is the next one"; the other-bunk branch off |

## Small points (not blocking)
1. **"Too early" in the early morning.** bedtime() ends at 05:30, so from 05:30 to the alarm a lie-down says "Too early
   to sleep: you can turn in from 20:00." That's true, but odd at 05:45; "It's daytime: you can turn in from 20:00"
   would read right at any hour. On Thursday's inspection card (05:30-08:00), "Lie down" shows the same words.
2. **"Yours is the next one" in a room of three.** Bunk 1 has Tomas's and Lukas's bunks besides yours (DS1's note);
   from the one not beside yours, "the next one" isn't quite right. "Yours is the one by the locker" or similar, or
   only the bunk beside yours saying it. For the writer.

## Checked and fine
- bunkTap returns true only for an item called "Bunk", on your bed's deck, in your bed's room, and not your own (over
  1.2 from it, as before); everything else falls through to the old path.
- Off-path: nothing else calls bunkTap differently; cadet_test identical.
