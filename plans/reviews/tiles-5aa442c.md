# Sanity read: plans/tiles-plan.html (claude/tiles 5aa442c), reviewer 2

**Verdict: sound, with a few fixes before it's built.** The balance claims hold up under an independent
simulator (plans/reviews/tiles-5aa442c-sim.py, written from the page's rules alone, 2,000 games per row, seed 1):

| Reading of DOCK | Players | First player wins | Draws | Turns (both) | Games that never reach 7 |
| --- | --- | --- | --- | --- | --- |
| any moved, jumped or launched tile can dock | Easy vs Easy | 48.0% | 0.0% | 22.9 | 51% |
| same | Medium vs Medium | 51.2% | 0.0% | 18.9 | 26% |
| only a launched tile can dock | Easy vs Easy | 47.5% | 0.6% | 25.7 | 68% |
| same | Medium vs Medium | 48.9% | 0.1% | 22.6 | 38% |

The page says 49.2% / 22.4 turns (Easy) and 49.6% / 18.6 (Medium). Only the first reading matches them.

1. **MEDIUM, the rule text:** DOCK says "If the tile you just *placed*...", which reads as launch only. The numbers
   (and "3-4 docks but only 1-3 launches a game") need any moved tile to dock. Reword it: "the tile you just moved,
   jumped with or launched". Read the other way, games run longer and most Easy games hit the cap.
2. **MEDIUM, Rina's champion level isn't tested.** It's "one notch above Hard", but it's not in the simulator. The
   user's streak question depends on how often *you* can beat her. Simulate it, and give a target (e.g. a
   Medium-strength player beats her at least 15-20% of the time), or her arc may never pay off.
3. **LOW, a rule gap:** "If you can't move, the game ends there" doesn't say who wins. Say "scores compared as at the cap".
4. **LOW, the worked turn:** step 4 says "their Planet on e4 is eyeing your Ship on e2". Those squares are in the same
   column, two apart, and jumps are diagonal, so no jump is possible. Use a diagonal example.
5. **LOW, the tie rule:** at the 14-turn cap the second player moves last, so has the last chance to "dock last".
   That's probably small, but tiles_check should report tie-break wins by seat, not assume them.
6. **Build notes (determinism):** the crew's random choices (Easy's coin flip, picking among equal moves) and Tiles
   night's pairings and results must use seeded hashes in 800-829 (schedU), never Math.random or R(), so tiles_check
   and a reloaded save replay the same. Please commit the throwaway simulator next to the plan, so the numbers can be
   reproduced.
7. **LOW, phone width:** 6 × 56 pt = 336 pt, plus the a-f / 1-6 labels and the bezel, is wider than a 320 pt phone
   (iPhone SE). Let squares shrink to 44 pt minimum there.
8. **Name clash (for the code, not the page):** claude/decks-p3 already declares `const TILES` and `tilesSeats`.
   Don't declare those names in section 23 until the rename is confirmed.
