# Handover: mechanic engineer 1 (E1), Pillar 5 Step 4

Written 2026-10-19 ~06:30 UTC, updated ~06:40 (handed over at ~70% memory after 0.45.13) by E1 (session_01AHeKjieg3qWjnEVuHecsHd) for a fresh session taking the seat. Read first: CLAUDE.md, the brief (`git show origin/claude/lead-pillar1:plans/brief-p5s4.md`), the Step 4 pages on claude/p5-design `plans/mechanics/` (step4-stages, m11-tool-upkeep, m12-logbook; step4-stages' "Builders' questions" has D3's answers), DEV_NOTES rows 0.45.7-0.45.12 and the hook register's E1 rows, then the older M1 notes (DEV_NOTES "Pillar 5 mechanics: rounds, ...").

## Seat, branch, builds, people
- **Seat E1**, branch `claude/mech-rounds`, series 0.45.x (0.45.7-0.45.13 used; next **0.45.14**). Base: 0.63.3 final (claude/p5-cand-pt1 7a6e137).
- Lead 17 session_016bN7x175WBwBL7S9xc2Lpb (lead 16 handed over). Build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z. Reviewer R5 session_01XJyHzg4QvX2nsdtf9zT1TH (R4 passed up to 0.45.10). E2 retired: E5 session_01QsZymCraDjLzVDooLvigNk builds team parts on manifestRun (E2's notes: plans/handover-mech-e2.md on claude/mech-incidents); playerRigRebuild is declared in E2's 24l: never declare one in 24 core. E3 session_01WkkCvj4yxnMALMQYG2DsWM (claude/mech-diagnose, places in 0.53.4 9d179e9). W2 writer session_01866TWKzGRgZmFcxiYRi4db. D3 designer session_0115ZiGhf9s3oYtFdjs7TgYS. U2 (HUD, arrow/tips) session_012TFwzt5eZoNZKrXrXTzN2w.
- Report: one line per finished piece to the lead; hashes to BM7 and R5.

## What E1 built (all in section 24 unless said)
- **0.45.7 24 core on C's behalf:** `toolWear(id, n)` (n of 100; wear saved 0-1 as before), `toolCharge`, `toolState` (charged / low <60 / due <30), `toolStateWord`, `toolSlow` (1.25 when due, toast once a day, `side.slow`), `toolUpkeepOn()` (no wear before the m11 row opens: R4's fix, 0.45.10). Scanner 4/scan (24g's scanRead), pipe kit 5/trace (24i at traceFound; the reading's `opts.tool`). `worksSide()`, `worksSideXp(n, why)` (+2 a ship day across all side jobs, `side.xp`), `WORKS_SIDE_KINDS` (turn-in of a listed kind pays a flat `WORK_XP[kind] ?? 1` through the cap; `j.xp === 0` pays nothing). `side` lives right after `cur` (worksInit + worksClean; BM7's key-order FAIL). Section 15: `myBedRoom()` / `bedText(s)` make the Bunk 1 texts say "Cabin 4-23" after the move.
- **0.45.8** every Step 4 ladder row in CAREER_LADDER (m10, m11, m12, m13, m14, m15 (0.45.11), m17), as the owning seats sent them. The fault-finder ticket's row will come from E2.
- **0.45.9 playtest 2 item 1:** `WORK_MECH[id].self` (24 core: after the meeting straight to trainDo, no teacher job, nobody following); m1 is self: the whole training route is yours on the board. `roundTrainStep()` for U2's arrow/tips (take/go/look/mark/next/done).
- **0.45.11 round 2:** 24m tool upkeep (bench taps, `benchStart`, scanner charge via WORK_TICK, `benchHold` acts with `def.onDone`, the rack after 4) and 24n the logbook (`logChoices`, `logbookWrite`, `logLast`, the 22:00 flag, Calder at progress talks). Live only with E3's places. Record lines: E2's fault-finder grade (`ms` ff1-3), E3's star logger (`ms` stars).
- **0.45.12:** `manifestRun(list, to, o)` in 24d (parts from their shelves to a place or machine panel; 'haul' job with `j.src = 'stores'`, reserved slot 30, held to `o.until`, then withdrawn; `j.delivered` + `simNote('manifestRun', { job, for, to, parts })`; `manifestRunDelivered(id)`, `manifestRunEnd(id)`). Shape agreed with E2 (24h teamParts). TELL E2 THE HASH when it's final.

## Still to do (round 3 / 4)
- DONE in 0.45.13 (9ad6eaa line, final below): hauling stage 2: `haulFree(d)`, `haulOrderAsk(j)` (a WORK_TICK once per run; `j.order`), `haulStops` follows it, `haulTidy(j)` at your turn-in; row m4 stage 1 at 2 uses; an officer's run held at stage 2. mech_check part `haul2`.
1. (done) **Hauling stage 2** (D3's answers on step4-stages): after 2 runs, "choose the order": when you take a run, pick the delivery order (deviceChoose, one stop at a time; store `j.order`; haulStops builds deliver stops in that order; only before any delivery is done); "A tidy run" (W2's `haul.tidy`) when deck changes equal the fewest; `worksSideXp(1, 'haul')` as an officer, nothing extra as a junior. After promotion the run stays the crew's by default but is held for you to 16:00 once you've reached stage 2 (24d's post: `crew: ... || playerRank() !== 'junior'`).
2. **Hauling stage 3, the stocktake:** Thursdays 13:30 from Day 18 (officer, m4 trained): a job with a hold at each of E3's `5-stock-1..4` (W2's `stock.count`); the short shelf by `schedU(week, 0, 1026)`; finding it: `stock.short` / `stock.job`, puts a part in `SHIP.hold` so section 17 posts its restock; `side.stock = { week, found }`; +1 via worksSideXp. Withdrawn at 16:00 if not taken.
3. **Rounds stages 2-3** (24a): stage 2 (after 5 rounds): pick 4-6 of the deck's machines with "last looked" days (`side.round.last`; W2's `round.last` / `round.last.never`); finding two or more worn: Torres's `round.two` + worksSideXp(1, 'round'). Stage 3 (scanner, after stage 2: worksStage('m1') >= 2 and use >= 5): one look per room from its first machine's panel reads them all (`round.doorway`), finds the unhealthy ones, `toolWear('scanner', 4)`.
4. playerRigRebuild is E2's (lead 17: E2 owns the pin); E1 does not declare one.
5. W2 has all my keys (incl. round.title.first, bench.charging(.now), bench.rack(.done)).

## Gotchas
- **Two browser checks at a time at most**; a third (or overlap) gives "game failed to start": just re-run that one alone.
- `placeById` builds its index once on first call: never call it at load (use `DECKS[n].places.some(...)`). `PLACE_OF` holds only the current deck's places.
- `machinesNow()` re-posts jobs and stock runs down by Day 17+: plant stock (`SHIP.stores.x = 3`) in tests.
- A training job reserved at the meeting is posted for the next minute (`found` = now + 1): advance the clock before claimJob in tests.
- Never `pkill -f` a pattern in your own command line.
- Scratch merges for E3's places: `git worktree add /tmp/.../wt HEAD && git merge 9d179e9` (only the build-number lines conflict).

## How to test
Setup: `pip install playwright`; three r128 into /tmp/cadet-work/three (`npm pack three@0.128.0`, untar); `CADET_CHROME=/opt/pw-browsers/chromium`. Per push: `mech_check.py BUILD [side m1 m4 m11 m12 ...]` (parts `side` and manifestRun are E1's core), `career_check.py`, `machine_check.py` (haul/jobs), `interactions_check.py` and `player_check.py` (taps, texts), `cadet_test.py OLD NEW` (ALL IDENTICAL expected). Run them from a script that logs each result (TEAM.md "Long check runs").

## Open questions for the user
- None from this seat. (D3 answered the hauling-after-promotion question; the lead decided the Tier 2 bands stay as C2's.)
