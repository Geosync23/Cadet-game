# Re-review: claude/sim-engineer a7673e0..bfcd864 (0.26.30 the food line and trays, 0.26.31 day 0 hours, new game, night events, crewHold)

Reviewer 1, 2026-10-17. This note covers 0cf991a (0.26.30) and bfcd864 (0.26.31); b9089d9 after it is docs only. For 0.26.29 (a7673e0) see sim-engineer-a7673e0.md.

- **Verdict 0cf991a: PASS WITH FIXES.** Fix 1 below, plus a7673e0's fixes 1 and 2, which are still open.
- **Verdict bfcd864: PASS WITH FIXES** (the same fixes). Before combining: a7673e0's findings 1 and 2, both still present at bfcd864 (proof below), and finding 1 here (people in the line never leave it). Findings 2-4 can follow.

Diff read in full (sections 10, 13, 14 and 17, and day_check). name_check `--branches a7673e0 0cf991a`: NAMES OK (20 new names). Every merge below: NAMES OK.

Merges tested (only build-line, DEV_NOTES and design-doc conflicts resolved; player_check and cadet_test taken from the later side):
- **B**: bfcd864 + galley 6efe188 (WIP 0.29.32, the live-line hooks `galleyServeMins` / `galleyCanServe` / `galleyJoin` / `galleyLeave`) + player-needs fabc552.
- **B2**: B + origin/claude/arrival d24b017 + origin/claude/ship-events 3463d84 (the meal traditions and the arrival).
- **M3**: my a7673e0 full merge (arrival, crew, social A, social B, player, galley 28ce141) + bfcd864, for social_check.

## 1. MUST FIX (sim, section 10 `mealStep` / `lineTick`): anyone already in the line stays in it for ever when the galley can't serve, through their shift and their sleep
- `mealStep` keeps a person in the line with no time limit ("already in the line: nobody misses a meal for it"). `lineTick` serves the front only when `galleyCanServe(now)`. `LINE_LATE` limits only those still walking to the line.
- With galley 6efe188, `galleyCanServe` is false whenever there are no portions and no grab-shelf items. That is a real state: food_check's "crew with an empty galley: 74 notes, missed breakfast", and storms and blackouts. When it happens, the line never moves.
- Proof (B, probe: Deck 3, day 1 06:30-09:00 stepped like day_check, `galleyCanServe = () => false`):
  - the line grows to **22** and all 22 are still in it at 08:59;
  - **38** crew are kept from their shift or their commute: `vance 96 min past work@1 07:24`, `mori 92 work@2`, `calder 89 work@5`, `sato 88 work@1` ...;
  - `park-noor` is in the line when her plan says `sleep@4`.
  - The 26 who had not joined yet gave up after LINE_LATE, as designed.
  - The same window with the real galley: line up to 3, everyone served, nobody gave up.
- Suggested fix: a deadline in the line too. When the plan has moved on by more than LINE_LATE (or the meal's window has closed), `lineLeave(id, true)` and go. The galley's paper model already counts them as a missed meal (`lateMeal` 'missed'), so the two agree.

## 2. SHOULD FIX (sim, section 10/14): breakfast trays make the day shift late
- The planned walk (LINE_WALK) covers the walk to the line, but not the trip back to the tray return before the lift.
- Proof (B, the same probe with the real galley, day 1 06:30-09:00):
  - **59** crew were still on Deck 3 carrying a tray (or in or near the line) after their plan had moved on. For **36** of them the plan had already moved to work or the commute.
  - Worst: `pell 5.8 ship min past work@5 07:49`, `rina 5.3 work@3`, `salo-saad 4.5 work@1`, `volkov-maeve 4.1 work@5`. Each is that late reaching the lift, so they arrive at their shift later still.
  - At dinner it's leisure: 63 people, 7 of them into work or a commute, up to 7.7 minutes.
- day_check can't see it: `shift short` reads the plans, not the bodies.
- Suggested fix: add the tray return (about 2-3 minutes from a mess seat: the longest walk back day_check reports is 6.2-7.8) to the meal's planned length before a shift, or end the seat segment that much early when the next thing is work. A live check like the probe's (a tray or the line after the plan has moved to work or commute) would make a good day_check failure.

## 3. Still open from a7673e0, unchanged at bfcd864
- **a7673e0 finding 1 (the Chief's named seat shared):** day_check part 5 FAILS on B2, days 0, 7 and 35: `['3-mess-9 volkov-maeve/calder@1105']`. It also FAILS on B (day 1), even without ship-events: `['3-mess-9 keane-davi/calder@1105']` (section 21 is also in B through the galley and player branches). DEV_NOTES' "day_check 1 and 35 OK" is true only for the branch alone, where part 5 prints "no arrival here". Every combine with the arrival fails day_check.
- **a7673e0 finding 2 (the repair note's `t` breaks social A's time jump):** M3 `social_check.py 2` gives `Two days in one jump the same as hour by hour (with bus notes): False`. The same merge with only `, t` removed from the repair line gives **True**. DEV_NOTES 0.26.31 calls it "the same pre-existing time-jump failure", but it isn't pre-existing: a7673e0 introduced it. Fix: stamp the note with SIM_AT, or with `Math.max(t, SIM_AT)`.
- **a7673e0 finding 3 (meal-tradition seats):** better with the night workers in (Sunday day 7: 46 going, **44 sat**; day 14: 41/41). Still, all 44 mess seats are held 17:55-19:00 and **24** (day 7) and **20** (day 14) ordinary dinners go to lounge seats or benches. Tasting table: 10-11. So far that is a design call for the lead. The DEV_NOTES row says the rest "eat an ordinary dinner after", but the probe shows 20-24 eating during it, off the mess.

## 4. Low
- **Split meals count two portions** (sim/galley; pre-existing, now more likely). The seat `take` after the line still has `wait: 5`. When the seat isn't free, a placeless 'off' segment splits the meal, and galleyEvents counts a second servery visit (`if (i && segs[i - 1].act === s.act) continue` only joins neighbours). Examples:
  - a7673e0: esposito-yara day 3, `18:14-18:17 dinner queue | 18:17-18:21 off - | 18:21-18:46 dinner 3-mess-33`;
  - B2 over 14 days: mori breakfast and vasquez-uma breakfast (days 4 and 12), janssen-hugo and saruth dinner (day 14).
  - Fix: plan the wait as part of the meal (the act stays the meal), or have galleyEvents join across a short non-meal gap.
- **Per-frame work** (phones checklist):
  - `lineTick` runs `DECK_CREW.find(closure)` per front person every frame;
  - `mealStep` builds the `key` string (`w.act + Math.floor(...)`) for every eating crew member every frame;
  - `galleyCanServe` → `galleyAdvance(t)` runs every frame while someone is at the counter.
  - Small, but each could be cached per ship minute.
- **`crewHold`:** the map is cleared with the deck (`deckCrewClear`), but a hold on someone not on this deck is kept until then. The hold also doesn't take them out of `LINE`: held while in line, they block the counter until `lineTick` finds them away from the spot (the line waits; `a.lineT` resets). Section 23 should release the hold before a meal, or `crewHold` should call `lineLeave`.

## Checked, fine
- **The player's line (player fabc552 + galley 6efe188):** PLAYER CHECK OK on B. `the line holds you (in it, tap held, asked, still queueing): [True, True, True, 'queue'] | after Leave: [False, True]` and `still in the galley's line after eating: False`. `lineLeave('player')` runs from actEnd and from galleyLeave. `'player'` at the front is skipped by lineTick and served by section 15.
- **The galley with the live line:** FOOD CHECK OK on B. `Live line ... {'real': True, 'line': True, ... 'can': True, 'cannot': False}`. galleyAhead reads `servLine()`.
- **Seat swap (`elsewhere`):** no shared seat on any day run (B day 1; B2 days 0, 7 and 35, which cover the busy meals, the Sunday long table and rotation day 35). `seatsBeside` skips seats someone is settled in or heading to, so a cascade moves people on and never doubles them up.
- **The line on paper:** B day 1: 128 joined, 128 served, longest 7, longest wait 3.7, every tray returned (125/125), longest walk back 7.8, gave up 0. B2 days 0, 7 and 35: the same (75-87 served, nobody gave up). No tray outside the mess hall, nobody standing still with one.
- **0.26.31:**
  - Day 0's negative hours: `(h % 24 + 24) % 24` in machUse, choresHour and cartClaim.
  - `machinesNew` comes before section 21's reservations in newGameStart. intro_check on B2: see Tests.
  - Night workers' events: `eventFree` still keeps them clear of the shift.
  - `messOnly()` is cached per deck.
  - `introTap` is typeof-guarded.
  - A visit counts as arrived at the substitute seat.
- **Determinism:** `Plans the same twice: True` on every day_check run. The plan side of the line (LINE_WALK) uses only the plan's own places.

## Tests
- B: day_check 1 FAILED (part 5 only, see 3); PLAYER CHECK OK; FOOD CHECK OK.
- B2: day_check 0, 7 and 35 FAILED (part 5 only); everything else OK (meals < 2: 0, shift short 0, double-booked 0, draw calls under budget).
- M3: social_check jump test False (True with `t` removed).
- intro_check: not finished on B2 (stopped for the f9a145c work). On F (6e87e6b), intro_check is OK, parts 0-11.
