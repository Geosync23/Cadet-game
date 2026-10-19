# Reviews: Pillar 5 Step 3 last piece and Step 4 (reviewer R4)

R4 succeeds R3 (whose verdicts are in `plans/reviews-p5-step2.md`). Newest first.

## Step 4

### E3 claude/mech-diagnose 9d179e9 (0.53.4, the places turn): PASS WITH FIXES (five leak joints move)
Base 0.63.3 7a6e137. Diff: one places block after Step 3's, two Deck 5 props (your bench, the order board), build lines, DEV_NOTES.
- One owner: E3 alone defines `DECKS[n].leakJoints`, `growRacks`, `cabinSpots` and the new place ids; E2 (cfc4961a) only reads `leakJoints` through `placeById`. E1 (89369630) touches none of them. Good.
- Places are `type: 'event'` with `event: 'side' | 'leak' | 'leakp'`: inert for crew plans. Ids unique (deck_check OK, my run too). Nothing saved, no R().
- Props: the bench under the Works bay window (room w i0 10: the bench blocks tile 10,4; the place is 11,4, clear) and the order board on the machine shop's north wall (edges h,21-23,9 are 'wall'). Both look right in screenshots.
- **Fix: five leak joints are on the wrong spot.** I checked each joint's wall edge (EDGES at the place tile's `wall` side) and the place tile:
  - `3-leak-2` (galley 36,6 'w'): no edge at v,36,6, open floor: the joint and damp would hang in the air.
  - `3-leak-4` (promenade 13,9 'n'): the tile is BLOCKED by the call booths (12-14,9); standing there puts you inside the booth and the joint behind it. deck_check lets it through because a standing place on a blocked tile passes when a neighbour is reachable.
  - `4-leak-3` (laundry 12,16 'n') and `4-leak-4` (junior corridor 8,4 'n'): edge h,12,16 / h,8,4 is a `door`: the joint and damp would sit on a doorway.
  - `4-leak-2` (starboard washroom 2,18 's'): no edge at h,2,19: it's the curved hull, so the flat `wallAt` spot isn't on the wall.
  The other seven: wall or hull edges, tiles free, puddle tiles free and in the same room. Keep the ids and order (E2 reads them); move each to a free tile whose `wall` edge is 'wall' (or a straight 'hull'). Worth a line in deck_check: a leak place's tile free and its wall edge 'wall'/'hull'.
- Minor, no fix needed: `4-23-shelf` sits on exactly `4-23-keepsake`'s at/xy/face (fine while both are player-only).

## Step 3: U's Tracked device app

### C2 claude/works-career f553607 (0.44.27): PASS (for BM6, over f3b744c)
One game line: careerJobIn pushes a department's rep entry into j.gains.rep only if none is there yet; plus build lines, career_check (calls it twice, expects one entry), C2's handover. No lines shared with U 1d602ff7.

### U claude/hud-pt1 1d602ff7 (0.72.4, button kept beside the app): PASS
Scope changed by the user ~04:00 (via lead 16): the device app stays AND the main-screen button stays. 94a1b127 below (button removed) is superseded, not to be merged.
- Merged on every Step 3 tip (as below), `node --check` clean. The button, panel, placement and frame loop are back as in 0.72.3 (the frame loop moved after recFrame, harmless); the panel and the app share `trkTap(key)` (true when it starts something: the panel or the device closes; a stop keeps it open and redraws). App first in the list, as below.
- turnInGains now shows one chip per department and one per system (the larger if a system shows twice). The doubled rep chip came from interactions_check seeding `j.gains.rep` before C2's careerJobIn pushed its own; in play C2 is the only writer of `g.rep`. C2's f553607 (0.44.27) also writes it once per department; the two guards agree (writer and reader), no shared names. Fine together; noted for one-owner hygiene only.
- Checks on the merge: interactions_check OK (5f6761e's job-by-title tap included), device_check OK, cadet_test vs the same merge without U's 0.72.4: ALL IDENTICAL, no state differences.

### U claude/hud-pt1 94a1b127 (0.72.4): PASS WITH FIXES (one check line, no game change)
Reviewed merged on every Step 3 tip (S2 0d0aa59, C2 f3b744c, M2 b3e5cf9, M3 42c76cc, H2 935b1d9, DA5 25dbfce, X 3a494c8, W2 a21487e; the jobStopsBase S2/H2 hunk resolved the known way, S2 first), `node --check` clean.
- Behaviour as asked: the HUD button, its panel, CSS, placement and frame loop all go; `deviceApp({ id: 'tracked', order: 1 })` is first in `deviceApps()` (boot -1 is hidden, home 0 is excluded, Settling in 5). The same `trkItems`/`trkOn` as before; a tap tracks (the device closes so the arrow shows), a second tap stops it (the device stays open); rows with no goal show "no arrow for this one" and aren't buttons. The heads-up's overlap list drops 'trkBtn'. Nothing saved.
- No other tip names trkBtn/trkPanel/trk* except interactions_check's old block, which is guarded by the button existing; no duplicate top-level names.
- cadet_test vs the same merge without 0.72.4: the only differing pixels are the old button's spot (x 132-254, y 86-115) in every shot; no state differences. device_check OK.
- interactions_check: **FAIL "a tap on your job tracks it again"** is the check, not the game: `tap('Job')` looked for the old panel's "Job" tag, which the app no longer shows on the job row (tags only on the "on" rows). With `tap(myJob().title)` the tap is found and the check passes. **Fix: in interactions_check.py, tap the job by its title** (e.g. `tap(g.ev('myJob().title'))`).
- The other FAIL (turn-in rep chip shown twice) is the known C2 f3b744c × U 0.72.3 clash BM6 is already placing; 0.72.4 doesn't touch the turn-in.
