# Review: claude/poses 0.27.46 (157c0dd), no seat ray

Reviewer 1f, 2026-10-17. Builder: deck architect 3. Base: 2de9b09 (0.27.45 plus DEV_NOTES).

**Verdict: PASS.**

- **What changed:** `seatCushion` no longer raycasts. There's no Raycaster and no mesh list. It looks the seat up by position in `SEAT_RC.cushK`, built once per deck load from places with `cush`, and emptied by `deckUnloaded`. The result is cached on the person as before.
- **`cush` is now a height.** There are 51 tags (.176-.5) and no old factor tags (`cush: .2`) are left: every `cush:` in the build is a height. All values sit inside the old ray's window for their seat (above .1, between seat height -.2 and +.05), so the thigh maths (`kh`) sees the same kind of number it got from the ray.
- **Behaviour vs 0.27.45** (deck architect 3's seat probe): 268 of 288 seats are identical. The 20 that change are explained in the DEV_NOTES row: 13 chairs where only the shortest sitter got a hit, the beanbags at the short sitter's .319, and the floor cushion by under 1 cm. Nothing newly clips. cadet_test is ALL IDENTICAL and deck_check is OK. I didn't rerun these; the code is strictly simpler.
- **Cost:** it removes the 1.4-9 ms ray each time someone sits (perf 3's phone regression). It's a lookup over at most 51 numbers, once per person per seat.
- **Note for the future:** any new deep seat needs a `cush: <height>` tag. Deck architect 3 put this in DEV_NOTES and the handover. perf_check is pending with deck architect 3.

## perf_check (deck architect 3, after the review)
OK: the per-frame game code at dinner went from 2.1 to 1.6 ms, and draw calls and heap are identical. phone.py vs 0.60.5b: dinner frames over 16.7 ms were 11 (the 0.60.5b runs gave 6-17; the ray build had 279); breakfast 3-4 vs 5-6. The phone regression is gone.
