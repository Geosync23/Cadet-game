# Reviews: Pillar 5 Step 3 last piece and Step 4 (reviewer R4)

R4 succeeds R3 (whose verdicts are in `plans/reviews-p5-step2.md`). Newest first.

## Step 3: U's Tracked device app

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
