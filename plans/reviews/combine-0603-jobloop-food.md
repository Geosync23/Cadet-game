# Check: the job loop and food_check on galley 0.29.34 + sim 0.26.34 + 0.26.36 + player 0.28.40 (for 0.60.3)

Reviewer 1c, 2026-10-17, at the lead's ask. Merge: galley 7282327, then sim 236810f (0.26.34), then **f16a110 cherry-picked** (0.26.36; only its build lines conflicted, every other added line checked present), then player 9c18045.

## Fixed
- **player_check's job loop passes:** "Inspecting: The range needs an element…", repaired, the save holds the work. The cook steps aside (`crewMakeWay`) and the player's wait-then-walk works. player_check's own someone-in-the-way case: wait > walk > in > do.
- **food_check's four old FAILs are gone** (the day-7 wait, the cold store, spoilage, busy): galley 0.29.34's Sunday-table fix.

## NEW, SHOULD FIX (sim 0.26.36): you walk straight through the chef
- **player_check now FAILs "squeeze past: slowed to half, with a polite word"** (it passed on every earlier merge). The check walks you past the settled chef at the galley: "path found, through the chef's tile: True", but "slowest 1": no slow-down and no word.
- **Why:** 0.26.36 drops every shared tile (two places' walk-to tile, like the cook's station 3-galley-2 on 3-range-1's panel [39,4]) from the player's blocked tiles, always (`!(except && except.isPlayer && sharedTile(a.spot.walk))`). The cook only steps aside (`crewWayOn`) when that tile is your goal or your place. Passing *through* it on the way elsewhere, the tile isn't blocked, so the squeeze rule never runs, and the cook doesn't move either: you walk through her at full speed.
- **Fix:** leave shared tiles out of the blocked set only while they're being kept clear for you (`crewWayOn(now)` has the tile, i.e. it's your goal, your place or a `crewMakeWay` tile); otherwise block them as before, so passing through still squeezes.

## NEW, test only (food_check, the galley's): "galleyJoin / galleyTurn: [1, False, False, True, False, True]"
- The paper check joins at 18:00 and expects your turn at `j.turnAt`. With the live line, `galleyTurn` needs you at the front (`lineFront`). Since sim 0.26.34 plays the line forward when a deck loads mid-meal, someone (`ahead: 1`) is already in it, so your turn hasn't come yet. Not a game bug: `takePortion` and the rest of the line work in the same run, and on the real line the player is served (player_check).
- **Fix (galley engineer 3):** in that check, clear `LINE` before joining, or step until `lineFront('player')` and then expect the turn `GALLEY_SERVE.you` later.
