# Handover: FX29 (builder, lead 39), 2026-10-26

Hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi) to continue FX24's Doors setting on claude/doors-3way (FX24's
note: plans/handover-fx24.md, section 5). Reviewer RV18 (session_01PMfvrCN6StPzwVSPGX7ijH); build master BM18
(session_01A3S2VBMYmTt2wCZa8ej7XR); check runners CR1 (arrows, session_01CsWNjCsy8u5mrHJgTVgCst), CR5 (controller,
session_01CHoEsvv7zMPZDr1ir7uAiz), CR6 (interactions, player). Build-number lines not touched (the build master's).

## 1. claude/doors-3way (from FX24's 3051de4e), tip at this note's commit
All in section 15b's Auto doors slot unless named.
- **An arrow's way opens its doors** (lead 39's option a): `adoorWay(g)`, called by `ixFrame` with `goalNow()` every
  frame. It finds the path (findPath, the player as `who`) from your tile to the arrow's goal: `ixGoalWorld`, or the
  lift panel for another deck; the nearest free tile when the goal's tile isn't free. It keeps the doors on that path
  that `adoorKind` counts as shut to you, in `ADOOR.way = { key, cells, doors }`. `adoorShut` returns false for them,
  in every setting, so keys, touch steering and the controller all pass. Found again when the goal's tile or deck
  changes or you step off the way's tiles; a door from the old way you're within 1.6 m of stays in. No arrow, or
  'all': `ADOOR.way` null.
- **A tap on yourself** (RV18's should): `pick()` never returns the player, so 0.93.3's adoorTapSelf line in `tap()`
  never ran. Now `adoorOnMe(cx, cy)` (your body on screen, feet to head, about a body's width) is asked only where
  the tap would otherwise walk you over the floor (`meDoor` in `tap`: when nothing is under the tap, and just before
  the floor walk at the end). Your job's stop under it (`jobSpotTap(h.point)`) and the arrow's pin (`atPin`) come
  first; crew, items, doors and floor places are handled earlier in `tap` as before.
- **The hint**: `adoorHint()` (from `ixFrame`): your steering (`player.steer`, no path) pushing at a door shut to you
  (within .6 m, ahead of you) toasts "A private room / Tap the door to open it." ("Press A, or tap the door, to open
  it." when `PAD.used`). 3 a session at most, 20 s apart (`ADOOR.hints`, `ADOOR.hintAt`; not saved).
- **controller_check** `walk_to`: when the stick stalls (no movement 2 polls) with a door shut to you within 1.2 m
  (`SHUT_NEAR`), `open_door` cycles the ring to the `door:` key and presses A, then walks on (CR5's 'day' FAIL on
  3051de4e; lead 39: the check opens the door as a player would, steering stays stopped).
- **interactions_check** doors part, new lines: the arrow's way (setGoal past a bunk door, steer through; clearGoal,
  shut again), the hint (once, the words), a real tap on yourself (clears `ADOOR.here` first: adoorSet in the doorway
  the last part left you in holds that door open).
- design-doc Doors line ("An arrow's way opens its doors", the hint, the tap on yourself); DEV_NOTES Auto doors entry;
  build-table row "doors-3way-b (FX29)".

Checks on bdb6f00a (game file the same as 1dc4825e, sha256 b0dd6aaa...): check_fast QUICK CHECK OK; controller_check
door + day OK (CR5 too, on 329ad201); interactions_check OK (alone). cadet_test vs 3051de4e: state, paths, collisions,
taps identical; shots e_night .. i_tap0 differ (~2000 px) only by Bunk 1's door open: the start's "Very hungry" arrow's
way runs through it and you stand beside it (rule a, intended). Not run by me: player_check (CR6); arrows_check
(CR1 on 329ad201: week OK; week guide still stalls Day 6 20:10 / Day 7 18:20, the same on d9c7e5f0: older than the
doors, FX30's job on claude/week-guide-fix, session_01HSG9H3UnSNhTDxZtKoACnB).

## 2. claude/events-check-swapfix (lead 39, for BM18's 0.93.3 gate), 8a91f1dc, test only
- events_check: "diplomatic phases" reads the visit's own steps up to its first 'end' (with the swap on, the comet
  starts inside its window). Lead 39's lines.
- bigevents_check late saves follow EV_SWAP_ON: a Day 20 save has the comet due Day 22 with the swap on or off (FX25
  moved the comet to Day 22; FX22b's "not SWAP" assumed Day 26); a Day 23 save passes over 'diplomatic' too with the
  swap on. BIGEVENTS CHECK OK on staging-0.93.3 acbb52e0 + this.

## Loose ends / gotchas
- interactions_check takes about 64 min here (both d9c7e5f0 and 329ad201, section by section within seconds: not the
  doors); plans/testing-guide.md says ~8. Worth a backlog row (told lead 39).
- One run of interactions_check on 1dc4825e (heavy load) printed "a tap on someone in front of the glow ... ([])": no
  crew placed at any angle. It passed alone on bdb6f00a; not reproduced.
- Near the camera, doors and walls are cut down (FX24's gotcha): a door's tap box is a floor strip your body covers.
  That's why the tap on yourself exists.
- `adoorWay` calls `ixGoalWorld` every frame in 'private'/'none' mode (a second call beside ixFrame's own); cheap, but
  if a perf check flags 15b, that is the place.

## How to test
plans/testing-guide.md section 2 setup (playwright, three r128 and acorn in CADET_WORK, CADET_CHROME). Separate
CADET_WORK folders and log files for runs side by side. `python3 controller_check.py BUILD door day`;
`python3 interactions_check.py BUILD` (look for "Auto doors:" and the FX29 lines); cadet_test from a scratch folder
against `git show 3051de4e:starship-cadet.html`.

## Open questions for the user
None of mine. The hint's words ("A private room" / "Tap the door to open it.") were my wording; CS1 may want to bake
them into the words if that's the rule for toasts.
