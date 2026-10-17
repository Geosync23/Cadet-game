# Re-review: claude/sim-engineer 0cf991a..6e87e6b (0.26.30-0.26.33: the food line and trays, day 0 hours, the 0.26.29 fixes, nobody in the line for ever)

Reviewer 1, 2026-10-17. Earlier notes: sim-engineer-a7673e0.md (0.26.29) and sim-engineer-bfcd864.md (0.26.30-0.26.31). This note checks f9a145c (0.26.32) and 7a11c73/6e87e6b (0.26.33) against them.

**Verdict 6e87e6b: PASS WITH FIXES.** One must-fix (finding 1, a short change in section 14). Everything else from the earlier notes is fixed, except the deferred should-fix on tray lateness (finding 2).

Merges tested (only build-line, DEV_NOTES, design-doc and test-file conflicts resolved; NAMES OK on each):
- **F**: origin/claude/arrival d24b017/b16436f + f9a145c (then 6e87e6b) + deck-plans-1-2-6 + social 6353c2d (contains 69876a7) + social-stories + player-needs + galley 6efe188.
- **F2**: F + ship-events 3463d84 (the meal traditions).

Every browser run used `CADET_WORK=/tmp/cadet-work/rv1work` and my own probe there. The shared scratchpad `probe.py` was replaced at 08:40 by one that always loads `/tmp/cadet-work/rv-dev`.

## 1. MUST FIX (sim, section 14 `introLay`): the Chief's arrival seat is still shared, now with Torres
- f9a145c holds named intro seats in `occ.res` before anyone is planned. But introLay's `free(id)` only checks `occ` (bookings), never `occ.res` (holds). A room or tile beat's `alts` can therefore pick a seat held for someone else. When nothing in `alts` is free, it also falls back to `e.placeId` even though that is taken.
- Proof: day_check part 5 (the sim's own check) FAILS on F (days 0 and 35) and on F2 (days 0, 7 and 35), with `Arrival on, days 0 and 1, places booked twice: ['3-mess-9 torres-zeke/calder@1105']`. Before the fix the pair was keane-davi/calder or volkov-maeve/calder.
- Suggested fix: in introLay, `free = id => !(occ.get(id) || []).some(overlap) && !(occ.res && (occ.res.get(id) || []).some(([x, y, ev]) => overlap && ev !== 'intro:' + p.id && !<this person's event>))`. If none of the alts is free, plan no place (stand) rather than `e.placeId`. day_check part 5 should then be OK on F and F2.

## 2. SHOULD FIX (deferred by the sim engineer, still open): breakfast trays make the day shift late
- Unchanged since bfcd864. Probe on F, day 1 06:30-09:00 with the real galley: **36** crew are still on Deck 3 with a tray, or on their way to or in the line, after their plan has moved to work or the commute. Worst: `pell 5.8 ship min past work@5 07:49`, `rina 5.3`, `salo-saad 4.5`. At dinner it's 7.

## Fixed and verified
- **The repair note's time (a7673e0 #2):** social_check on F is **SOCIAL CHECK OK**. `Two days in one jump the same as hour by hour (with bus notes): True`, and the repair cue through the real bus is `{'cue': True, 'wrong': False, 'mem': True, 'queued': 0}`.
- **Nobody in the line for ever (bfcd864 #1, 0.26.33):** probe on F with `galleyCanServe = () => false`, day 1 06:30-09:00:
  - the line peaks at 35 and is **empty at 08:59**;
  - `LINE_LOG.left` is 48;
  - nobody stays in the line more than 12 minutes past their plan (`strand-erik 12`, `oduya 12`, ...). Before the fix: 22 still in it, up to 96 minutes late.
  - The player isn't affected: the rule is in `CrewAgent.mealStep` only, and section 15 and the galley keep the player's membership (`lineLeave('player')` from actEnd and galleyLeave).
  - Crew needs come from the plans (hunger goes up at the planned meal), so someone who leaves the line still "ate" on paper. The galley's paper model counts them as 'missed' when it is empty. That mismatch is older than this change (crew needs never read the galley). Low; for later.
- **Meal-tradition seating (a7673e0 #3):** F2, Sunday day 7: 46 going, **44 sat**; day 14: 41/41; the tasting table 27/27 and 30/30. On Sunday all 44 mess seats are used by the table, so the 20 ordinary diners in the lounge aren't kept out by empty held seats. Tasting days: 3-4 off the mess (was 7-11).
- **trayLate (0.26.32):** F2, Deck 3, day 7 16:40-20:30, the real line. Only 2 people get trayLate, both later seated with a tray (18:55 and 18:56), and **none is left at the end**. Nobody is stranded. Low: `amadi-asha` stood 15.8 ship minutes with nothing in hand before a seat came free.
- **Day 0's negative hours, machinesNew on a new game:** machine_check OK, intro_check OK (parts 0-11, including Monday's briefing and the shadow shift).

## Still open (low)
- **Split meals count two portions in galleyEvents** (bfcd864 #4). Seen again on F2: vance and haddad-tamsin breakfast, achterberg-lars dinner (day 3), mori (4), vasquez-uma (12), janssen-hugo and saruth (14).
- **food_check on F2 FAILS:** `day 7: hart-ravi 18:16 waited 6 minutes` and `carts: the cold store ran short`. I'm running baselines (bfcd864 + the same galley + ship-events, and F without ship-events) to see whether the sim's Sunday table (44 served at 18:00) or galley WIP 6efe188 causes it. See the addendum.

## Tests
- F: day_check 0 and 35 FAILED (part 5 only); social_check OK; intro_check OK; machine_check OK.
- F2: day_check 0, 7 and 35 FAILED (part 5 only; servery line 77-88 served, nobody gave up, every tray returned); food_check FAILED (see above, under investigation).
- Plans the same twice: True on every day_check run.
