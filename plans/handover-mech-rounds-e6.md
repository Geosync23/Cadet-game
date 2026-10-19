# Handover: mechanic engineer E6 (took E1's seat), Pillar 5 Step 4

Written 2026-10-19 ~07:20 UTC by E6 (session_018cZuXpb4XdFs47zXoPcF8B) at ~50% memory, after 0.45.18, on the lead's ask. Read first: CLAUDE.md, E1's note `plans/handover-mech-rounds-e1.md` (everything there still holds unless changed below), the brief (`git show origin/claude/lead-pillar1:plans/brief-p5s4.md`), DEV_NOTES rows 0.45.7-0.45.18.

## Seat, branch, builds, people
- Seat E1/E6, branch `claude/mech-rounds`, series 0.45.x; used up to **0.45.18**, next **0.45.19**.
- Lead 17 session_016bN7x175WBwBL7S9xc2Lpb. Build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z. Reviewer **R6 session_01CPyuA1o5jgxwQtv7huZTNg** (R5 has handed over and is inactive). E4 session_01PtXCwVBprdkJ6AcQisEyJq, E5 session_01QsZymCraDjLzVDooLvigNk (team parts on manifestRun; playerRigRebuild is E5's, never declare one), X2 session_016jw3fP3pGztfciWgr6hg9A, U2 session_012TFwzt5eZoNZKrXrXTzN2w (roundTrainStep for its guide: unchanged).
- Report: one line per finished piece to the lead; hashes to BM7 and R6.

## What E6 built
- **0.45.14** (2edb69c, R5 PASS): 24n `logbookTick` night crew only on a WORN flagged machine, never a `heldForYou` job; 24 core turn-in: side kinds pay `(WORK_XP ?? 1) + right` (rewiring's right-first-time), capped.
- **0.45.15** (910131e, R5 PASS): 24d hauling stage 3, the Thursday stocktake: job kind `stocktake` (side, never the crew's), Thu 13:30-16:00 from Day 18 for an officer trained in m4, slot 31; stops at E3's `5-stock-1..4`; `stockShortFor(d)` (key 1026), `stockFound` (2 parts stores -> hold, so section 17 posts the restock; +1 capped), `SHIP.misplaced` put back, `stockWithdraw` at 16:00; `side.stock = { week, found }`.
- **0.45.16** (f36d81e, R6 PASS): 24a rounds stage 2 (`roundPicks`, `roundPickAsk`/`roundPicked`, `roundWalk` shared with roundRoute, `roundLast` = `side.round.last`, two worn -> Torres's round.two +1) and stage 3 (`roundDoorway`, `roundDoor` from the kind's stepDone).
- **0.45.17** (64a2b19, not reviewed yet): hauling order set only when complete and before any delivery (`haulOrderAsk(j, got)`); `round.pick.some`; manifestRun leaves out / flags empty shelves (`j.empty`, the note lists what came); tester on the bench (`TOOL_UPKEEP.tester`).
- **0.45.18** (see git log): the doorway reads every machine in the room, route or not.

## Loose ends
- R6 to review 0.45.17 and 0.45.18.
- New lines with no writer (listed in rows 0.45.16-0.45.17): "looked at today", "That's my round", `round.pick.some`, "No {part} on the shelf.", `bench.tester`. The next writer checks them; W2's old `round.pick` ("Pick five") is no longer read by stage 2.
- `logLast(n)` is still unused (for whoever builds Calder's progress-talk read-out).
- R5's other notes not acted on: benchStart counts the use before the hold ends; the three log choices read the same on a quiet day; the flag question is a second deviceChoose (lost if refused); the works.ms.stars / grade names vs W2's.

## Gotchas (beyond E1's)
- `jobStops(j)` gives `{ step, places: [id] }`; a kind's own `placeId`/`crate` are on `kindStops(j)[k]`.
- `j.found` is the job's found TIME: never use it as a flag.
- In mech_check tests, call `machinesNow()` after `setShipNow` BEFORE planting machine states or SHIP.misplaced (jobStepDone runs the hours and the crew fix/fetch things).
- Stubbing `deviceChoose` / `simTimeout` inside a test: assign and restore them (they're function declarations in the game scope).
- My check runner: a script runs career+machine, then interactions+cadet_test, then mech_check, two browsers at a time, logging each (copy the build to a scratch file first so you can keep editing).

## How to test
As E1's note. Rounds: `mech_check.py BUILD m1` (part round23); hauling/stocktake/manifestRun: `m4`; logbook/upkeep need E3's places (scratch merge with 9d179e9, take HEAD's side of the build-number conflicts): `m11 m12`.

## Open questions for the user
- None from this seat.
