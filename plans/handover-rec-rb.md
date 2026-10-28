# Handover: rec engineer B (RB), the rec deck's works

**Role:** RB in `plans/brief-recdeck.md` (on `claude/lead-pillar1`): the rec deck's machines and jobs (R10), the "Deck 7" sweep, crew poses and the auditorium, phone perf, the checks, and the switch (`REC_DECK = true`, last). Reports to lead 18 (session_01CBur9nrJ411pFkHopF96RL). Successor: RB2 (session_018cunWUG3yeKN8NzCPdRbTy).
**Branch:** `claude/rec-works` from the 0.63.4 final aa4f42c. Series 0.84.x.
**Others:** reviewer R6 session_01CPyuA1o5jgxwQtv7huZTNg; build master BM8 session_01YGy9FDmcbkySMJpVPYJaAo (combines 0.64.0 after 0.63.5 is final and the lead says go; send R6 and BM8 each hash); RA (crew use, traditions) session_012mZrFQrGpbNeNWuRg4Bxyp; W3 (writer) session_01LbftuR6cNubo3CvAScTuv5.

## Builds (all in DEV_NOTES' build table, rows after 0.82.8)

| Build | Hash | What |
| --- | --- | --- |
| 0.84.0 | 2e46584 | `REC_MACHINES` (16, section 4e before `DECKS[7]`), `-svc` work:works places, 13 kinds in a 'rec' system (only while `REC_DECK`), `machineList` skips Deck 7 while dormant; the 47-site `deckWord` sweep; the directory sign's R row. |
| 0.84.1 | f7a30ca | `FAULT_CAUSES` for the 13 rec kinds, `LOOK_WET`/`LOOK_LIT`, lives tuned; machine_check's delivery case unloads till empty. |
| 0.84.2 | 00cfd80, 58fea44 | `deckIn(n)` ("on the rec deck" mid-sentence, lead 18's call); the directory footer on R "You are on the Recreation Deck". R6: PASS (58fea44). |
| 0.84.3 | e4c5da2 | R6's fix on 0.84.0: 19 more ", "/"(" sites + evPlaceName through `deckIn`; `deckWord` only at a label's start. |
| 0.84.4 | 3a1cc57 | `recShutAt(t)` (pure, for RA's schedules) / `recShut()`; `recSigns()` from worksTick (milky/green pool on `RK.poolOwn`, red tags and tape on the wall, FLOAT ROOM CLOSED sign, net off); refusal guard lines in 15r. |
| 0.84.5 | d9aea96 | The pool leak trace: `line: 'pool'` on the poolfilter seal, `MACHINE_LINKS.pool` (REC-on only), `LINE_SHOWS`, `poolDripGoal`, the Deck 5 puddle; machine_check case "Pool leak". |
| 0.84.6 | 4cfe651 | Crew rec moves via a place's `move` (swim, tread, kayak, climb + rope, float, fan) and the `sit:slump` pose (section 8c `REC_CREW`, `recCrewRopes`). |
| 0.84.7 | b899519 | The rec causes' `still` lines in the house meaning (W3). |

Naming (lead 18): signs and formal labels "Recreation Deck"; mid-sentence "the rec deck" (`deckIn`); a label's start "Rec deck" (`deckWord`); crew speech "rec dec" (W3).

## Calls made (lead 18 accepted)
- Rec machines are their own system `'rec'` (weight 1, deck scope), using existing STOCK parts (no new parts, shelves unchanged). `SYSTEMS.push('rec')` only while `REC_DECK` is on; the Ship health board shows 10 rows, lowest first, so one healthy row drops off.
- Wall holds and seat hinges are tier-1 machines whose only cause is the chore.
- Deck 7 machines do NOT join Step 4's rounds/logbook (lead 17's call 5).
- Rec causes use only 'always'/'warm'/'touched'/'at-time' (Deck 7 has no crew hours yet, so 'peak'/'after-use' would never show).

## Testing
- Every check on the dormant build (must be identical to the base: cadet_test ALL IDENTICAL, machine_check OK) AND on a test copy with the switch on: `sed 's/^const REC_DECK = false;/const REC_DECK = true; /' starship-cadet.html > on.html`.
- Own CADET_WORK per run (`/tmp/wN`, with `test/` and a `three` link to /tmp/cadet-work/three).
- machine_check REC-on: steady player 5.8 jobs/day, repairs 49% (dormant 5.6, 45%).

## Gotchas
- `machineList` had no `playerOnly` filter: anything in `DECKS[7].machines` would go live at once. The REC_DECK skip is the gate; keep it until the switch.
- machine_check execs `cadet_test.py` from its own folder: run it from the repo, or copy cadet_test.py beside it.
- The GAME_BUILD line is ~8777, not near the header; bump both (header line 288).

## Round 2: done (0.84.4-0.84.6); interfaces given to RA
- `recShutAt(t)` -> `{ pool, river, belays, route, court, board, float, lights, mic }`; board/lights words come from how bad the condition is (the hour record keeps no causes).
- Crew moves: place fields as in DEV_NOTES' 0.84.6 row. RA owns the places.
- The two edits to existing trace functions (`traceSymptom` reads `LINE_SHOWS`; `traceGoal` asks `poolDripGoal` first) were lead 18's allowance ("additive, no copy"); tell R6 if asked.

## Loose ends (for RB2)
- Round 3 is RB2's: the auditorium (screen down over the windows, house lights, stage pools, `perform`/`address` poses, `recShow(state)` that RA calls: signature not yet promised), phone perf (plan section 10 targets; machineFx ≤ 4; water off-screen skips its update), then round 4: device_check/machine_check loop over `DECK_ORDER`, `REC_DECK = true`, a save on the rec deck loads there.
- The traced pool leak is tier 1 work (pool filters are tier 1): it posts only for a trained Officer, but any crew can take it.
- Climbing a roped-off or tagged route is still allowed for you (only "both belays out" refuses); RA or RB2 can steer to an open route.
- Walking into the shut float room toasts on every walk-in (`recRoomIn` starts floating on entry).
- Crew climb to the player's `top` (~1.4 m); a third climber at once gets no rope; someone leaving mid-move jumps to the walk tile.
- Fault words: W3's are in `content/works/faults-rec.lines` (claude/writer-rec 019dcd1). The three refusal toasts in 15r and the leak's 'trace.pool.*' toasts are plain strings: W3 will send RB2 keys to wire.
- Reviewer is now R7 (session_01HCwvy5w432bhz41UYxHYwq); R6 passed up to e4c5da2.
- Not yet run on the REC-on copy: day_check/events_check with real rec crew (RA's places don't exist yet), interactions_check (taps, job board, goal arrow on Deck 7), disc_check.

## Helpers
I built round 2 with subagents writing exact-string edit scripts on copies (scratchpad `edits/r2*.py`), then applied and re-tested each on the branch. Works well for memory; review their diffs for `R()` and version labels.
