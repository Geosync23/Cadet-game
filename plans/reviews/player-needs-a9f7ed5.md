# Review: claude/player-needs 0.28.52 (a9f7ed5; merged as 18eedb8), a tap at your job's stop, and the Repair button

Reviewer 1f, 2026-10-17. Builder: player engineer 7 (session_01CrRKCZzVtM68JrPqJByCMk). Behaviour, reviewed in depth.

**Verdict: BLOCK.** One softlock (HIGH) and one MEDIUM. The rest is sound.

## What changed
- `jobHere(p, viaRay)` / `jobSpotTap`: a tap within 1.5 m of your chore's next stop or your repair's panel (or whose line of sight passes within .6 m of it) starts that work. It's hooked into `playerTap` (any thing but the job board or ship health), `playerFloorTap` and the tap on `see` (glass-backed) items.
- `jobDoorOpen(deck, room)` in `doorOpenFor`: a locked room opens while your chore's next stop is in it (section 18's veyliLamp in the Captain's quarters).
- `#repairBtn` (`handTick`/`handRepair`) appears at the stop with the parts in hand.
- `ixChoreTap` measures a thingless tap from its point.

## Checked
- The `ixChoreTap` condition rewrite is logically the same as before for things.
- The Repair button: hidden while paused, on the lift ride, mid-activity and in dialogue. Its `pointerdown` stops propagation, and `handTick` runs in `playerUpdate`, so it's frozen when paused.
- `jobDoorOpen` only opens a door for the player, and only for the next stop of a chore (`k` skips the fetch step).
- The floor and glass cases the user reported work: player engineer 7's interactions_check clicks all 7 lamp stops plus stormBallasts, veyliLamp and an oven repair.

## Findings
**HIGH (softlock): you're locked in the Captain's quarters after fitting veyliLamp's lamp.** `jobDoorOpen` is true only while the lamp stop is still to do. Fit the lamp and it's false, and `edgeBlocks`/`doorOpenFor` keep the closed door shut both ways. **Probe** (`player-needs-18eedb8-locked-probe.py`): at the stop, a path to the lift exists; after the stops are done, `findPath` to the lift is **false**, with the player in room C. **Fix:** let the player out of the room they're in (in `doorOpenFor` or `jobDoorOpen`, true when the player stands in that room), or keep it true until the job's turned in or you've left. Add a check: stops done → a path to the lift.

**MEDIUM: while you hold a repair, taps on everyday things near that machine are taken over.** `playerTap` runs `jobSpotTap(point)` before the thing's own action, for anything within 1.5 m of the panel (or along the tap's line of sight). **Probes:**
- `player-needs-18eedb8-near-probe.py`: about 60 tappable things on Decks 1-6 sit within 1.5 m of some panel. Examples: other washers, battery banks, pumps, ovens, the chest freezer, a Calendar 0.05 m from a panel, a Deck 4 bunk 1.34 m from washer-4's, the mug rail, the Welding bench.
- `player-needs-18eedb8-hijack-probe.py`, real clicks:
  - with washer-1's repair held, tapping **Washer 2** gives "Inspecting: The washer needs a seal" instead of "You start a load";
  - with battery-1's, the **Welding bench** gives the battery repair instead of crafting;
  - on Deck 1, the Works station tap goes to the databus repair.

**Fix:** use the job route only when the tapped thing has nothing of its own to do. Either move the `playerTap` hook to the end (a fallback), or limit it to floor taps, `see` items and things with no action. That keeps the user's lamp cases.

## player_check on 18eedb8
PLAYER CHECK OK on 18eedb8 (reviewer 1f), no page errors. It doesn't cover the softlock or the tap takeover; see the probes.
