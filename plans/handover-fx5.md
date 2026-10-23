# Handover: FX5 (fixer), 2026-10-23

Session session_01LGRr55ZQCd11PuqhJEn9Jj. Reported to lead 30, then lead 31 (session_0118SXBCdg87nDiXdtrGNVSR).
Memory about 60% at writing: stopping here; a fresh fixer takes any new job.

## What I built (all reviewed, all PASS)
| Branch / commit | What | Reviewer | Where it went |
|---|---|---|---|
| claude/p5-fix5 c5eb7119 | p3 "What's been tried?" learned on Day 5: WORK_MECH.p3.open trains you when the solve was already counted (the case is Day 5's scanner job, solved before the p3 row opens) | RV9 | arrows-c (c68731c3) |
| claude/tip-clear feb2e54a | a device tip card never sits over the goal arrow's target (section 19 slot, tipClear: moves below the pin, else lets taps through) | RV8 | breakfast-back line |
| claude/booth-arrow 3ec51eba, 6caeb176, 771c9ff2 | Day 0 call-home arrow and the Tracked "The call booths" row point at a free booth until the call begins; a tap at the booth's pin over someone is the booth (ixPinBooth) | RV10 | arrows-c / 0.92.0 |
| claude/day0-table 153084a1 | Day 0's kept seat past 19:00 not cut by the next walk's lead (kept flag); intro_check booth line frees a booth | RV10 | 0.92.0 |
| claude/day0-stay (from integration-next 51a1bb34) | after the Day 0 dinner, diners with an hour or more till their evening stay on Deck 3 (a free lounge seat or bench, else about the deck) instead of the bunk trip (the user's yes, 17:00 UTC) | RV10 | to BM15 for 0.92.2 |
| claude/day0-trickle 0e392cf3 + de475883 | Day 0's table trickles out from Zeke's LIVE goodnight (the user, 2026-10-23): section 14 day0Free/day0Trickle patch only the diners after Day 0 is planned (2-50 min after the goodnight, then bunk till their planned evening); plans never read the live minute | RV10 | to BM15 for 0.92.1 |

## Loose ends / for the next session
- Done (day0-stay): after the Day 0 dinner no diner takes the lift to their bunk; all stay on Deck 3 (the user's yes, then lead 31: whatever the wait).
- tip-clear (feb2e54a) was not in arrows-c when booth-arrow was reviewed: a tip card over a pin still took taps there; check it's in the merged line.
- Backlog idea (not filed): day0Trickle leaves the table seats "held" in occ until the old end (harmless today: nobody else's plan is made after it).

## Gotchas
- Two interactions_check runs at once in one CADET_WORK can stall (RV10 saw it at "near your job, but not it"); give each run its own CADET_WORK.
- cadet_test's a_start shot once differed under heavy load; alone it was identical. Rerun alone before calling a regression.
- intro_check's call-home lines depend on who holds the booths that evening; the check frees one booth itself now.
- Day 0 checks need the arrival ON (newGameStart(true) + the manifest form); cadet_test's Game page has it off.

## Handy scripts (scratchpad, not in the repo)
/tmp/claude-0/-home-user-Cadet-game/d1e0d562-ea3d-58ae-a098-a0b09d2eac81/scratchpad/: ev/intro_check.py (intro_check --evening with a live monitor: the long table's seated count and crew place changes around the goodnight), tr2.py (Day 0 plans with/without a live goodnight: who changes, the table curve), pin_probe.py (booth pin real taps at 320x640), booth_probe*.py.

## Open job handed over (lead 31, 2026-10-23 19:05 UTC): Day 0 diners carry on with their own evening
The user: "It should return to full simulation once the dinner is over. Let them do what they will do. Their departure
from the mess hall must be staggered and slow though." day0-stay (583af9ed) is DROPPED. Branch from integration-next
54efee21 (has day0-trickle 0e392cf3 + de475883); reviewer RV10 (session_01XeJ6bvySekD1V8Sfh1tzgb).

What 0.92.1 does now (section 14, `day0Trickle(day, S)` just below `planDay`, called in `shipDay` after Day 0's plans;
`day0Free()` = SHIP.intro.done.free while the intro is on; shipDay's cache rebuilds Day 0 when it changes):
the day's plans hold the table to 19:45 + 2-50 min (tradGood/tradLeave, U(532)); once the live goodnight is known, each
tradition diner's table run is cut at goodnight + 2 + round(48 * schedU(p.seed, 0, 534)), and the gap up to their OLD
leave time is a made-up filler (bunk trip, or 'off' with no place). Their real evening starts only at the old time.
That filler is what the user doesn't want.

Suggested approach (mine, not built): per diner, plan their evening again from the minute they stand, others fixed.
- Leave time: keep L = goodnight + 2 + round(48 * schedU(p.seed, 0, 534)) (the staggered, slow departure RV10 passed).
- Take the diner's own bookings after L out of the shared bookings: `day.occ.who.get(p.id)` lists [from, to, placeId];
  remove the matching [from, to, ...] entries from `day.occ.res.get(placeId)` (check how `hold()` writes them, section 14
  around `const take = (act, opts, dur, o = {})` ~line 10131, and `isFree`).
- Re-run `schedBuild(p, 0, day.occ, S)` with tradLeave forced to L for that person (e.g. a module-level Map read at the
  top of `tradLeave`: `if (DAY0_LEAVE.has(p.id)) return DAY0_LEAVE.get(p.id) - B`), then pass it through `introLay` and
  `guestTrim` as shipDay does (see shipDay's loop ~line 10795). The re-run books its places in day.occ, so diners done
  one after another never share.
- Splice: keep the OLD plan up to L (cut the table run at L), then the NEW plan's segments from where it leaves the
  table on (first one starting at L). Earlier new segments are discarded (past, and may differ).
- Determinism: inputs are the saved goodnight minute only; a reload must give the same plans (plan twice and compare).

Proofs RV10 will want (all on paper with the arrival on, plus one live):
- nobody but the diners changes plan (compare Day 0 plans with and without SHIP.intro.done.free; events_check 1a
  already has this line, "changed the plans of people not at the table");
- no place double-booked (all plans), no gaps between segments;
- the table curve unchanged (as on 54efee21: 18:20 goodnight, 42 -> 32 after 10 min -> about 2 after an hour; at most
  4 up in a minute);
- each diner's first step after the table is their own simulated evening (no 'off'/bunk filler); new events_check line;
- live: intro_check --evening with the monitor (scratchpad ev/intro_check.py): crew off the table move as on the base.
Checks: check_fast, events_check, intro_check, day_check 0/1/7, cadet_test vs 54efee21.
Probes in my scratchpad: tr2.py (paper: changed others, double bookings, curve, fills by kind), ev/intro_check.py.
