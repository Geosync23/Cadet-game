# Handover: rec engineer B (RB), the rec deck's works

**Role:** RB in `plans/brief-recdeck.md` (on `claude/lead-pillar1`): the rec deck's machines and jobs (R10), the "Deck 7" sweep, crew poses and the auditorium, phone perf, the checks, and the switch (`REC_DECK = true`, last). Reports to lead 18 (session_01CBur9nrJ411pFkHopF96RL). Successor: RB2 (session_018cunWUG3yeKN8NzCPdRbTy).
**Branch:** `claude/rec-works` from the 0.63.4 final aa4f42c. Series 0.84.x.
**Others:** reviewer R6 session_01CPyuA1o5jgxwQtv7huZTNg; build master BM8 session_01YGy9FDmcbkySMJpVPYJaAo (combines 0.64.0 after 0.63.5 is final and the lead says go; send R6 and BM8 each hash); RA (crew use, traditions) session_012mZrFQrGpbNeNWuRg4Bxyp; W3 (writer) session_01LbftuR6cNubo3CvAScTuv5.

## Builds (all in DEV_NOTES' build table, rows after 0.82.8)

| Build | Hash | What |
| --- | --- | --- |
| 0.84.0 | 2e46584 | `REC_MACHINES` (16, section 4e before `DECKS[7]`), `-svc` work:works places, 13 kinds in a 'rec' system (only while `REC_DECK`), `machineList` skips Deck 7 while dormant; the 47-site `deckWord` sweep; the directory sign's R row. |
| 0.84.1 | f7a30ca | `FAULT_CAUSES` for the 13 rec kinds, `LOOK_WET`/`LOOK_LIT`, lives tuned; machine_check's delivery case unloads till empty. |
| 0.84.2 | 00cfd80 | `deckIn(n)` ("on the rec deck" mid-sentence, lead 18's call). |

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

## Round 2 status / loose ends
(filled in at handover)
