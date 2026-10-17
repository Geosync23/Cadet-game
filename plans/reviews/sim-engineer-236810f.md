# Addendum: claude/sim-engineer 6e87e6b..236810f (0.26.34) and a look at 7c1feea (0.26.35)

Reviewer 1, 2026-10-17. This follows sim-engineer-6e87e6b.md.

**Verdict 236810f: PASS WITH FIXES.** The only open must-fix is 6e87e6b's finding 1 (the Chief's seat 3-mess-9 shared with Torres), and 236810f doesn't change it. Nothing new must be fixed.

Merges: **F3** = F (see the 6e87e6b note) + 236810f; **F4** = F2 (with ship-events) + 236810f. NAMES OK on both. Runs used `CADET_WORK=/tmp/cadet-work/rv1work` and my own probe.

## Still open (from 6e87e6b)
- **MUST FIX:** day_check part 5 FAILS on F4 day 0 and F3 day 1: `['3-mess-9 torres-zeke/calder@1105']`. introLay's `free()` still ignores `occ.res`. 0.26.35 (7c1feea) doesn't touch it.

## Checked in 236810f
- **Catch-up when entering a deck mid-meal (`lineCatchUp`)**, probe on F4 (each entry steps half a ship minute before reading):
  - **Deterministic:** entering at day 1 07:12 twice gives identical results (`sameTwice: true`).
  - **Matches watching live:** entering at 07:12 gives the line `['moreau-signe', 'amadi-asha']`, 20 trays, 10 seated eating. Watching live from 06:30 to 07:12 gives the same line in the same order, 21 trays, 13 seated. Close; the catch-up places people by path length, so it can't be exact.
  - **Day 7, 18:05 (the Sunday table):** entering gives line 1, 1 tray, 3 seated; live gives line 0, 1 tray, 3 seated.
  - **No doubled seats and no tray outside the mess hall** on entry at 07:00, 07:10, 07:12, 07:20 or 07:35, or on day 7 at 18:05 (`dup: []`, `trayOut: []`).
  - Low: the catch-up serves at `galleyServeMins` and never asks `galleyCanServe`. Entering mid-meal with an empty galley therefore shows people already served who would have waited live. Live play then sends them on, so it's cosmetic.
  - Low: a catch-up person with no planned seat gets one from `seatsBeside` while the fill is still placing others. In theory, a person placed later in the same fill whose own plan has that seat could land on it. I didn't see it happen (no doubled seats in any probe).
- **No tray for lift arrivals until the counter:** someone who joins a meal from outside the mess hall goes to the line first (`m.served = false`). No tray outside the mess hall in any probe or day_check (F3 day 1: 128 served, 125 trays out and 125 returned; F4 day 0: 77 served, 58 trays out and 58 returned).
- **The occasion host stays the whole time (`apptReply`):** `a.occ` gives `a.len`, else APPT_WAIT. It's a one-line change, and its device side (ee3fcdd) is in another review.
- **`Number.isFinite` in simNote and simLater:** a `null` or string `t` no longer passes. social_check stayed OK on F (6e87e6b, which has the same max(t, SIM_AT)).

## 7c1feea (0.26.35), read only
- `SHIP_START_ARRIVAL` moves to tile [5, 7] facing south (the Tern's aisle, 5-tern-aisle-1). That tile is walkable only with the deck architect's walkable Tern (decks 0.38.19). On a combine without that deck build, the player would start inside the Tern's hull.
- The build master should run intro_check parts 8, 9 and 11 (the arrival in the real game) on the combine.
- The day_check change only prints where the leavers wait.

## Tests
- F3: day_check 1 FAILED (part 5 only). Servery line OK, gave up 0.
- F4: day_check 0 FAILED (part 5 only). Catch-up probe as above.
- Earlier in the same session: the empty galley (0.26.33) clears its line (35 at most, 48 left, nobody kept more than 12 min); social_check OK; intro_check OK; machine_check OK.
