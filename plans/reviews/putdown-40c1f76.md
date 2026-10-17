# Review: claude/player-needs-putdown 40c1f76 (0.28.60, player engineer 8): the Put down button

Reviewer 1g, 2026-10-17. In-depth review, because it changes behaviour and the save (`SHIP.player.crate`). The probes are `putdown-40c1f76-probe.py` (a real save and reload, a lift ride, New game) and `putdown-40c1f76-ride-probe.py` (what a tap mid-ride does). Run them next to a `cadet_test.py`.

## Verdict: PASS WITH FIXES

The button, parts, tray, crate, pointer, drop guard, tap to pick up, overnight return and save all work. One LOW: the button stays up during a lift ride, and a tap there leaves the crate in the lift car on the deck you left. The fix is one line and doesn't block the merge.

## Checks (on 40c1f76)
| Check | Result |
| --- | --- |
| PE8's `putdown_probe.py` (390×844) | PUT DOWN PROBE OK (every line ok; button 124×48 px, 12 px from the right, 18 px from the bottom, clear of the strip, Device and Pause) |
| Real save (saves on, `saveGame()`), then reload the page | the save holds `player.crate` (about 60 bytes); after reload the crate is still down on Deck 5, the job is still yours with pickup done, hands empty, no button, crate drawn on its deck: ok |
| New game with a crate down | no crate afterwards: ok (the jobs reset, so `putFrame` clears it) |
| Mid lift ride with a crate or a part in hand | **button shown** (LOW 1) |
| cadet_test vs 0.28.48 (2e69a13) | ALL IDENTICAL (0 differing px in every shot; no errors) |
| The lead's judgement calls (`putdown-40c1f76-made-probe.py`, a reserved 'lights' job: a relay off the shelf, a bracket you make) | **The job toolbox only:** no button. **Relay + bracket in hand, Put down:** the relay goes back on the shelf (+1), the bracket isn't stocked (stores unchanged) and waits at the lathe (`P.work.make` with its minutes done, 30/30), and the job stays yours. A tap at the lathe hands the bracket back at once ("You make a bracket. Now a relay from main storage next door."), and the relay can be fetched again: ok. **Gifts and the kit bag:** no button (kit bag in PE8's probe; gifts are filtered by `giftOf` in `putParts`): ok |
| Console errors | none |

## LOW 1: Put down works in the middle of a lift ride
`putFrame`'s `busy` covers an activity, the hover cart, Pause, the device, a dialogue and the lift *panel*, but not the ride itself (`ride`, section 12). Probe: a crate in hand, `startRide(4)` from Deck 5, a tap on Put down 0.4 s into the ride. The crate is set down in the lift car at Deck 5 (`deck 5, x -3.5, z -1.95`), and the player then arrives on Deck 4. You can get it back, because the pointer leads back to Deck 5 and the spot is reachable, but it reads oddly ("You set the crate down here" while the lift is moving), and parts go back on the shelf from inside a moving lift.
**Fix:** add `|| (typeof ride !== 'undefined' && ride)` to `busy` in `putFrame`, and `if (typeof ride !== 'undefined' && ride) return false;` at the top of `putDown()`, for a keyboard or assistive-tech click.

## Notes (no change asked)
- **A machine job's stops stay marked done:** after Put down, the reserved job's `stepsDone` is still `[0, 1]` (fetch, make) with empty hands. The pointer and the taps go by what you carry and `P.work.make`, so play isn't affected. Only a job card that counts stops would over-count until you fetch again (`jobStopMark` re-marks idempotently). For chores, `stepUndo(…'fetch')` already handles it. If wanted, the same `stepUndo` for a machine job's 'fetch' and 'make' would fix it.
- **Midnight, not overnight:** `night` compares calendar days, so a crate set down at 23:55 goes back to the pickup at 00:00. That matches DEV_NOTES ("left past midnight"). If the user expects "overnight" to mean while you sleep, a 06:00 cut-off would read better. That's the lead's call.
- `playerNew()` doesn't clear `SHIP.player.crate`. It's harmless today, because the New game's jobs reset and the first frame clears it, but a `SHIP.player.crate = null` there would be tidier.
- `putFrame` runs on its own `requestAnimationFrame`, not the main loop. It only changes the ship (`crate = null`, `stepUndo`, a toast) while a crate is down, so it doesn't touch the cadet_test run. While paused it still runs, but `shipNow()` stands still, so nothing happens.
- A tray put down doesn't add a dirty plate to the dish pit. That matches the old off-Deck-3 tray rule (0.28.38), so it's consistent.
- While I was driving it, I saw the arrival manifest card (z-index 40) cover the button on a fresh save. That's the manifest's modal waiting for its tap, not a Put down issue.
