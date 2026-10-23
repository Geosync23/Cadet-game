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
| claude/day0-trickle 0e392cf3 + de475883 | Day 0's table trickles out from Zeke's LIVE goodnight (the user, 2026-10-23): section 14 day0Free/day0Trickle patch only the diners after Day 0 is planned (2-50 min after the goodnight, then bunk till their planned evening); plans never read the live minute | RV10 | to BM15 for 0.92.1 |

## Loose ends / for the next session
- RV10's note on day0-trickle: diners with an hour or more until their planned evening go back to their bunk (lift both ways). If the user wants them to stay around Deck 3 instead, change day0Trickle's fill (section 14, below planDay).
- tip-clear (feb2e54a) was not in arrows-c when booth-arrow was reviewed: a tip card over a pin still took taps there; check it's in the merged line.
- Backlog idea (not filed): day0Trickle leaves the table seats "held" in occ until the old end (harmless today: nobody else's plan is made after it).

## Gotchas
- Two interactions_check runs at once in one CADET_WORK can stall (RV10 saw it at "near your job, but not it"); give each run its own CADET_WORK.
- cadet_test's a_start shot once differed under heavy load; alone it was identical. Rerun alone before calling a regression.
- intro_check's call-home lines depend on who holds the booths that evening; the check frees one booth itself now.
- Day 0 checks need the arrival ON (newGameStart(true) + the manifest form); cadet_test's Game page has it off.

## Handy scripts (scratchpad, not in the repo)
/tmp/claude-0/-home-user-Cadet-game/d1e0d562-ea3d-58ae-a098-a0b09d2eac81/scratchpad/: ev/intro_check.py (intro_check --evening with a live monitor: the long table's seated count and crew place changes around the goodnight), tr2.py (Day 0 plans with/without a live goodnight: who changes, the table curve), pin_probe.py (booth pin real taps at 320x640), booth_probe*.py.
