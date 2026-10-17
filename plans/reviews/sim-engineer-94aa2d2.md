# Review: claude/sim-engineer d45b03a..94aa2d2 (0.26.23: the d45b03a fixes, day 0 and the arrival start, introPlan, the escort walker, crewComeTo, appointment and shift notes)

Reviewer 1, 2026-10-17. Sections 13, 14 and 10 (plus cadet_test's `.nf` style line): in seat. name_check `--branches d45b03a 94aa2d2`: OK.

Tested on my own scratch merge of sim 94aa2d2 + arrival 330e538 + social d4538df + crew f7a18d2 + systems ae58e43 (the conflicts were build lines only): `node --check` and name_check OK.

**Verdict: PASS WITH FIXES.** Fine for 0.60.0: a first visit still starts on Monday 06:00, as before. One must-fix before wave 2 makes the arrival playable: the first-ever load never arrives (finding 1).

## My d45b03a findings: fixed (checked)
- **New game:** `newGameStart` clears `SHIP.flags` and `SHIP.notes` and sends `simNote('newGame')`. In the browser, after `flagSet('week1.done')` and New game: `week1.done` is gone, and the flags are only the new intro's (`escort.torres-zeke`, `week1`).
- Notes are copied as plain JSON, and a note that won't copy is dropped. `SIM_CUE` / `SIM_RING` are `var`.
- **Day 0 saves load:** New game, sign the manifest, play to 17:52, `saveGame()`, reload: the save loads (Day 0, 17:52, Deck 5), the intro carries on from `haulway`, and Torres is on the deck.

## 1. MUST FIX before wave 2: on a first-ever load the arrival never starts
- `const ARRIVING = !SAVED && arriving()` runs in section 13 at load, and `arriving()` reads `typeof introWanted`. `introWanted` is a `const` in section 21, much further down the file, so at that moment it's in the temporal dead zone: `typeof` throws, the try catches it, and `arriving()` returns false.
- Proven (`?debug`, storage cleared, reload): `ARRIVING` is false, the game opens on Day 1 06:00 in Bunk 1, `SHIP.intro.on` is false and no manifest shows, while `introWanted()` at run time is true. New game does reach the arrival (it runs after load); a brand-new player opening the link doesn't.
- Even with that fixed, the load path only sets the clock and the start tile: nothing calls `introBegin()`, so you'd stand on the ramp at 17:40 with no intro.
- Fix (two lines, two seats):
  - Section 13 decides without section 21: `!NOSAVE && !localStorage.getItem('starship-cadet-arrived')` (the key section 21 writes; share it as a `var` in 13, or read the literal).
  - Section 21 at load: `if (typeof ARRIVING !== 'undefined' && ARRIVING && !SHIP.intro.on) introBegin();` (ARRIVING is declared before section 21, so this is safe).
  - An intro_check case: storage cleared, `?debug`, reload: Day 0 17:40, Deck 5, the manifest showing.

## 2. Note (the player engineer's / arrival's): the manifest name doesn't survive a reload
- After signing as "Sam" and reloading, `SHIP.player.name` is null: section 15 doesn't save a name until the player engineer's `playerNameSet` lands, and section 21 falls back to setting `SHIP.player.name` directly. Make sure the name is saved when the two combine.

## Checked, fine
- **day_check on day 0 passes** on the combined build: no short sleep, meals or shifts, no double-booking or gaps, plans the same twice, nobody stuck, draw calls peak 292 (budget 450). `weekday(0)` and `guestStay` now wrap correctly.
- `introLay` lays the beats over the plan as fixed blocks, holds the places in `occ`, and adds lift rides when a beat is on another deck. The cache signature includes `introSig()`, so the plans are made again when the intro starts, ends or is skipped.
- `escortWhere` and `comeWhere` are live-only (in try, null before section 10 has run). `whereIs` gets an early return for the escort, which is cheap for everyone else (`escortPlan` returns null at once for anyone but the escort). In play, Torres stands facing you while you're more than 4 tiles behind.
- `crewComeTo`'s 22:00 cut-off is right on Day 0 too (it's -120 in absolute minutes).
- `shiftTick` sends `shiftStart` once a day (the `shiftSent` flag survives a reload). `apptKept` / `apptMissed` are sent from `apptTick`.
- Not yet: `crewLeaving` / `crewArriving` (social A asks for them; it falls back to the roster until they exist, so nothing breaks).
