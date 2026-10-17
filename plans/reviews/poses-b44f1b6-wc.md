# Light review: claude/poses b44f1b6 (0.27.42, deck architect 3): toilets on Deck 4, WC signs on every toilet stall

Reviewer 1e, 2026-10-17. A light review. The code is small. It changes the place list, so the crew's plans change too, but the architect has already run deck_check, day_check day 1 and player_check.

## Verdict: PASS

- **The WC sign:**
  - A canvas texture made at load, with no `R()`. It is shared kit, so the stall doors on Decks 2-5 all get it.
  - The door's front face is at z .55. The sign spans z .545-.565, so it is 1.5 cm proud, with no shared plane: the same pattern as the green "vacant" light beside it.
  - x 0 ± .18 clears the handle at x .38.
  - +1 texture and +1 draw call, as the architect reported.
- **`washroom()` and `o.wc`:**
  - The default stays at 1, so other washrooms don't change.
  - Deck 3's `o.toilets` path is untouched.
  - Deck 4's p and q get `wc: 2`.
- **The new places:**
  - p: 4-toilet-p2 at [4,0], xy 4.08.
  - q: 4-toilet-q2 at [3,19], xy 3.92.
  - The two rooms mirror each other, and no tile is used by two places.
  - Nothing else in the code, the tests, the plans or `content/` names the old ids 4-shower-p2 or 4-shower-q1.
  - The save keeps no place ids (`habitLog` is per crew member), so old saves are fine.
- **interactions_check on b44f1b6:** INTERACTIONS CHECK OK.
- **The morning rush:** 6 juniors a day now wash at a basin (showers 26 → 24 in the morning, 20 → 16 in the evening), and nobody goes without. That's acceptable, and it was the lead's choice. Worth keeping in mind if hygiene ever matters for crew.
- **Nit:** the sign's font is `system-ui`, so "WC" will look slightly different on each phone. That's harmless and deterministic on any one device.
