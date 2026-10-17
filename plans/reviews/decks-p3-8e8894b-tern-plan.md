# Review: the Tern plan sketch (decks-p3 8e8894b, plans/shuttle-plan.md)

Reviewer 2, 2026-10-17. This is a plan page, with no game change. It was checked against the combined build 0.60.2 (ship-integration).

**Verdict: PASS WITH FIXES (to the plan).** Fix these before building.

1. **A new game would start inside a seat.** The start tile is set twice: `SHIP_START_ARRIVAL.tile = [7, 8]` (section 13) and `INTRO_START.tile = [7, 8]` (section 21). Both put you on the old ramp. Under the new hull (x2 to x7, rows 6 to 8), tile (7, 8) is a seat, which is blocked. If the new Tern lands before both lines move, a new game starts on a blocked tile inside the shuttle. Those two lines belong to two other seats, the sim and onboarding. Plan the work so that all three changes land in the same combine, or keep a ramp tile walkable at (7, 8) until they do. The plan mentions only SHIP_START_ARRIVAL.
2. **"Crew plans byte-identical" is not true on rota days.** On a rota day, a leaving crew member waits in the bay at `bay[strSeed(p.id) % bay.length]`, out of the `shuttle-bay-crowd` places (combined build, about line 7933). Cutting the crowd spots from about 124 to about 110 changes who stands where at every rota farewell. That's harmless, but say so in the plan, and expect day_check and regression differences on rota days. Don't count them as a surprise.
3. **The ramp's blocked tiles.** findPath reads `free()` live, so blocking tiles while the game runs is fine for walking. But don't close the ramp while anyone is standing on its tiles or in the door well, the player or the escort. Either refuse to close it, or move them first. Otherwise someone is stuck on a blocked tile.
4. **Saving.** The ramp state isn't saved, and it loads open. That is the safe default, so keep it that way: don't add the ramp to SAVE_EXTRA unless the scene can be resumed. The roof hiding should depend only on where the player stands, so a game loaded inside the Tern looks right.
5. Small: a door 2.3 m tall (cabin floor 0.25 m to roof 2.55 m) that lowers into a ramp ends up about 2.3 m long and about 6° steep, not 15°, and it covers more than the two tiles drawn. Fix the numbers when it's built.

The plan's other points are fine: it reuses the Tern's materials, the roof is its own mesh, about +2 draw calls, and there are no new shaders.
