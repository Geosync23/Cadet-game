# Review: decks 0.38.21 to 0.38.23 (c5f94be, 2c01c8f, 3e1f4f9)

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS** (four LOW notes, none blocking). Closes reviewer 2's open item 1
(ternClear) and the trestle half of item 2.

## Tests
- cadet_test a71ac47 (0.38.20) vs 3e1f4f9 (0.38.23): **ALL IDENTICAL**. deck_check 3e1f4f9: **OK**.
- Trial merge with ship-events 3d06bcb (0.34.49; only the build-label conflict): `node --check` OK, events_check (28
  days + the year): **EVENTS CHECK OK**; harvest supper day 231 walked on Deck 3: 46/46 reached their places, stuck 0.
- **ternClear (0.38.21), in the browser:** with nobody on the ramp `ternClear()` is true; with `DECK_CREW[0]` moved onto
  each of [5,8], [5,9], [5,10] it is false and `ternRamp(false)` refuses (returns false, target stays 1). Fixed.
- **The ramp at -1.62:** open, the ramp's lowest point is 3.7 cm below the floor (a solid overlap, not a shared plane);
  the shot shows it resting on the pad with no flicker.
- **The trestle's tiles (0.38.23):** [25,10] [26,10] [27,10] are blocked while longTables or harvestTables is shown and
  free again after; they match the trestle top (deck x 25 to 28). Walking the harvest supper on Deck 3 (17:00 to 20:00,
  the decor shown by eventsDress): **nobody walked through the trestle**. The tiles are blocked from 17:30 to 19:30.

## Findings (all LOW)
1. **The end chairs are still walked through.** At the harvest supper 9 crew who weren't heading for an end chair passed
   within 0.25 of one (sato 18:11 at 23.42,4; larsen-hamid 18:13 and calder 18:20 at 32.58,4; varga-tariq 18:16 at
   32.58,1; and five more 19:04 to 19:24). It's only for the two hours a week the chairs are out, so not blocking. A fix
   if you want one: block the chair tiles while they're out and give those four places a `walk` tile beside them, like
   the mess seats.
2. **Two decor ids sharing a block.** `dressShow` only records the tiles it blocked itself (`filter(k => !BLOCKED.has(k))`).
   With longTables and harvestTables both on, the second records nothing; hide the first and the trestle (still drawn by
   the second) is no longer blocked. Seen in the browser: both on, then only harvestTables: tiles free. It can't happen
   today: over 400 days the Sunday table, harvest supper and farewell supper are never on the same day (the harvest
   supper takes that Sunday). A counted block (a count per tile) would make it safe if they ever overlap.
3. **You can be inside the trestle when it comes out** (stand on [26,10] at 17:30). You can still walk off (playerGo to
   [26,12] worked), so it's only a moment's clipping. The crew already step off a blocked tile.
4. **The benches reach 0.2 into rows 9 and 11** (z 9.8 to 10.1 and 10.9 to 11.2), the seat rows, so someone walking along
   rows 9 or 11 brushes them. Cosmetic.
