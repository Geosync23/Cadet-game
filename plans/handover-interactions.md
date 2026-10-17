# Handover: the interactions engineer (section 15b)

Written 2026-10-17 at build 0.37.8 (`claude/player-interactions` 6492ead). Read it with `DEV_NOTES.md` ("Player interactions (section 15b)"), `plans/handover-player.md` (section 15, which 15b plugs into), `plans/handover-systems.md` (section 17's jobs) and `plans/pillar3-plan.md` ("Jobs: take and turn in at the board", C13 tips).

## Role
- **Job:** everything the player can use beyond section 15's basics, the job board and turning jobs in, the on-screen goal pointer, the ship health panel, the job-loop tip triggers.
- **Branch:** `claude/player-interactions`. **Builds:** 0.37.0 to 0.37.8 (all merged or merging into the combined 0.41.x builds).
- **Section:** `// 15b. PLAYER INTERACTIONS`, right after section 15. Names are prefixed `ix` / `IX_`, plus `setGoal`, `clearGoal`.
- **Test script (mine):** `interactions_check.py`. Run with the others every turn (one at a time).

## What's built
- **Use what the crew use (0.37.0-0.37.2).** `ixTap` (via section 15's `PLAYER_TAPS`) maps the place nearest the tapped thing (`ixKind`) to an activity in `IX_ACTS`, registered into `PLAYER_ACTS` and run by section 15's `actStart` loop: bar, tea, reading seats, lounges/common rooms, observatories and telescope, garden beds, music, laundry folding, public basins, the gym's water. Side gains (`also`, plus `with` for company) come from `ixSide` in 15b's frame loop and follow `A.done` (so `needEffects().task` applies). Leaves alone: section 15's own taps (`ixTheirs`), real machines within `MACHINE_NEAR` (`ixMachine`), washers, places in another room, private cabins (`privatePlace`), beds/notices/boards (`IX_SKIP`), plain seats (section 15's sit-anywhere).
- **Job board (0.37.0, 0.37.2, 0.37.6).** Tap "Job board" → `ixBoard` panel: your job (Turn it in / Drop it), `openJobs('you')` with Take it (only for jobs section 15 or 15b can walk you through), other open jobs with why not, the crew's jobs greyed. `.ixpanel` box: centred, clamped to the screen and safe areas, scrolls inside. Tap outside closes (capture `pointerdown`, no walk).
- **Chores and turn-in (0.37.3).** `ixChoreTap`: non-machine chores (lamp, vent, delivery, round) walked stop by stop (`ixStop`), `jobStepDone` per stop; `TURN_IN` is on (section 17), so finished jobs wait for Turn it in (`turnInJob`); chores are paid there (`JOB_PAY`), section 15 pays repairs and cart runs when it finishes them.
- **Goal pointer (0.37.0 on).** `setGoal({ deck, at | place | room | item, label })` / `clearGoal()`; otherwise your job's next step (`ixJobStep`: storage, machine shop, machine, cart run stages, chore stops, then "Turn it in at the job board"). DOM `#ixGoal`, own `requestAnimationFrame`, hidden with no goal, while `SHIP.player.track === null`, or while section 15's progress bar shows (`actProgress()`, 0.37.8).
- **Tracking (0.37.4).** `SHIP.player.track` (the device's Track switch): set to the job id on taking; saved via `SAVE_EXTRA`.
- **Tips (0.37.4).** `ixTip(id, text)` → the device's `tipShow`: `board`, `taken`, `machine`, `turnin` (the device fires `device`).
- **Held props (0.37.5).** `ixHold()` → section 15's held-prop line: `'carry'` for a delivery between pickup and drop, `'toolbox'` for any other unfinished job.
- **Ship health panel (0.37.6).** Tap "Ship health" (Deck 1, Deck 5) → `ixHealth`: `shipHealthRows()` as bars + condition words, worst fault per system, jobs on the board.

## Hooks outside 15b (all agreed, identical text on the owners' branches)
- Section 15: `const PLAYER_TAPS = [];` above `playerTap`, and `if (PLAYER_TAPS.some(f => f(it, at, point))) return true;` after `jobTap`.
- Section 15: the held-prop line ends `... 'tray' : typeof ixHold === 'function' && ixHold() || false;`.
- Section 17: `let TURN_IN = true;` (the lead's decision, 0.37.3).
- `player_check.py`: two `turnInJob` lines (before the job loop's `done = …` and the cart run's `fin = …`), and "the crate goes" checks `is not True`.
- `machine_check.py`: `TURN_IN = false` at setup (its 5g turns it on itself).

## Loose ends
- Chore stops have no tap-target for a few lone places (DEV_NOTES lists them); neighbours reach them.
- The chore pointer can't know progress inside a stop; it points at the next undone stop.
- Gains in `IX_ACTS` are my judgement; tune there.

## Gotchas
- Name clashes kill the merged build: grep every new top-level name across branches first.
- Section 15 runs `jobTap` and `cartTap` before `PLAYER_TAPS`; ixTap runs before ACT_TAP, sitTap and machineTap, so it must defer (`ixTheirs`, `ixMachine`, plain seats → null).
- `.device` is the device's sheet (section 19): never borrow it for a panel.
- Run checks one at a time; `pkill -f <check>` can kill your own shell.
- The arrow's `ixFrame` runs before the main loop each frame (it registered its rAF first).

## How to test
`CADET_CHROME=/opt/pw-browsers/chromium python3 interactions_check.py BUILD.html` (about 8-10 minutes): parity taps on Decks 1/3/4/5, held/private/notice/machine cases, walk-away, the board (take, drop, turn in), tracking and tips, the pointer (steps, other deck, setGoal, arrow vs marker, hidden under the progress bar), chores end to end with TURN_IN, the ship health panel, and a fresh game's Day 1 having a job for you every hour 06:00-16:00. Then cadet_test (ALL IDENTICAL), deck, day 1, food, machine, player, events checks.

## Questions for the user
- Are the activity gains right (a drink: food +10, a little company; lounging: social +4, more with people around)?
- Should the ship health panel show more (each machine's state, a history)?
- Should chores carry other props (a ladder for lamps, a brush for vents)?
