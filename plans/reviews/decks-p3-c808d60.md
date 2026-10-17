# Review: claude/decks-p3 c808d60 (0.38.8-0.38.10), reviewer 2

**Verdict: PASS WITH FIXES.** Base: ship-integration 0.41.10. I read the diff and probed the build in a browser
(tilesSeats, placeCalm).
Fine:
- Shared kit made at load with no R(): the TILES canvas, tilesBoardGeo, the wall kit. The garden's new pieces go
  after the R()-drawing beds and the trellis, and the keepsake shelf and mug rack are placed last, so nothing earlier
  moves.
- The new places are type 'event', so crew plans are unchanged.
- tilesNight is one InstancedMesh, and its cloned texture is disposed by dressHide.
- The seedlingYours trace is merged by mergeMeshes (3 draw calls, as claimed).
- CALM_TYPES and placeCalm are declared only here (social and dialogue read them; no second declaration on any branch).

1. MEDIUM (forward clash): `const TILES = { tex, mat, geo }` is the kit's board texture. Seat 10 is about to build
   "section 23. TILES", and a second top-level `const TILES` would be the same silent SyntaxError on merge as the
   TRADITIONS one. Rename it now (TILES_KIT or TILE_BOARD) and put the name in the hook register.
2. LOW-MEDIUM: two of Tiles night's eight boards seat only one player. Probe: `tilesSeats(k)` lengths for the eight
   boards are [4, 4, 4, 2, 2, **1, 1**, 2]. Board 5 (the coffee table, also the night's tap item, "Rina is defending her
   title") and board 6 (a tea table) have one lounge seat within 1.5 m. A two-player game there needs a second seat,
   a wider radius, or dropping those boards.
3. NOTE for the lead: 0.38.8's real washers bring a new machine_check FAIL ("two jobs at once: kovac-zainab"), which
   the helper reported to the systems engineer. Combine it with that fix, or expect the red check.
