# Review: decks 0.38.18 (eb0e776): the walk-in Tern

Reviewer 2, 2026-10-17. Against the plan review (decks-p3-8e8894b-tern-plan.md). **Verdict: PASS WITH FIXES.**

Checked:
- deck_check rc 0. Deck 5 is 175 draw calls by the lift, the same as before: the roof and the ramp are each merged into one mesh.
- In the browser: the well is blocked while the ramp isn't fully open and free once it is. On other decks there's no leftover block, and coming back to Deck 5 the hinge snaps to the right pose. The start tile [5,7] is free. ternInside is true on the well.
- Plan fixes taken: start in the aisle, the rota-day note, the ramp kept out of the save (it starts open).

## Fix 1 (MEDIUM): ternClear doesn't see the crew
`ternClear()` checks only `walkers`, which holds the player and old-style walkers. The scheduled crew, including any escort or arrival crowd, are `DECK_CREW` CrewAgents, which aren't in `walkers`. In the browser, with a crew agent standing on the well [5,8], `ternClear()` → **true**. The onboarding scene, which uses it before closing the ramp, would close it on the escort. Add `DECK_CREW.some(a => tiles.has(K(cellAt(a.x, a.z))))`.

## Fix 2 (LOW-MEDIUM): ternRamp(false) doesn't refuse
With the player on the well, `ternRamp(false)` closes anyway: the well becomes blocked under the player. The plan asked to refuse or to move them first. ternClear exists but nothing enforces it. Either check it in ternRamp, or say clearly in the comment that callers must.

## Combine order (as the lead said)
On this branch alone a new game still starts at `SHIP_START_ARRIVAL.tile = [7,8]` / `INTRO_START.tile = [7,8]`. That tile is now **blocked** (free → false). The sim 4 and onboarding changes to [5,7] must land in the same combine.

Low:
- When open, the ramp is a 1.88 m plate at -1.52 rad from a hinge at y 0.1, so its far end sits at about y 0.2 and slopes slightly **up**, away from the door. A hinge at about -1.62 rad, or one lower, would let it rest on the floor.
- The cabin floor is a 2 cm box on the deck (top at y 0.02). It isn't coplanar, but it's close; watch for flicker on a phone at a distance.

## Addendum: 0.38.19 (a570274)
- Fix 2 is done: `ternRamp(false)` returns false when not clear, a close in progress waits, and the well blocks only below half open.
- **Fix 1 is still open:** `ternClear()` is unchanged and still checks only `walkers`. Now that both the refusal and the waiting go through it, a crew agent (escort, arrival crowd: `DECK_CREW`) on the ramp or in the well is still not seen, so the ramp closes on them. One line: `|| DECK_CREW.some(a => tiles.has(cellAt(a.x, a.z).join(',')))`.
- The traditions side for this pass: 0.34.45 to 0.34.47 (708c4ca, e23620a, 3377935) PASS, see ship-events-2951e5b.md.
