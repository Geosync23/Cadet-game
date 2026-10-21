# Handover: the optimization reviewer (OR1)

- **Role:** reviewer for the optimization pass (render seat RN1, test-speed seat TS2). Took over PR7's opt queue on 2026-10-21.
- **Session:** OR1, session_015np4rHB2UHzet5Y1zFrBzm. Lead 24: session_01SDe7z5Nr7u69uH1k4sjZ8r. RN1: session_017qkNbUvRUfJqz24bLzTaR3 (claude/opt-render). TS2: session_019Ue76BxEtDwCcqQjJHjFHp (claude/opt-tests). PR7 (earlier reviewer): session_01LyKAVtCEedL1bP73vqzu9v.
- **Branch:** `claude/review-opt` (from claude/integration 3a48846). Notes only: `plans/review-opt.md` (every verdict, with repro and mutants) and `plans/review-opt/` (probes and logs). Never touches the game or the build number.

## The user's rules for this work
No visual change at all: cadet_test ALL IDENTICAL and deck shots identical. No texture cache. One exception: player_check may skip drawing in polling/arrive steps nothing reads; activities, the servery's draw-call budget and the phone layout stay drawn.

## Verdicts so far (details in plans/review-opt.md)

| What | Commit | Verdict |
|---|---|---|
| RN1 perf_check busy event scenes | opt-render 3af9f15 + 0ad9b5d, fixes fe0726b | PASS (F1-F4 fixed, confirmed) |
| RN1 #10 faster deck builds | ab86ff7 | PASS |
| RN1 #6 grain loop | c1bf6f1 | PASS |
| RN1 #8 Dev Speed card | 3a77cfe (tip bddbc48) | PASS; nits fixed in 5850ddb, 7d84c86 |
| TS2 player_check fix A + B | opt-tests 4775488 + e4acbf8 | PASS WITH FIXES: F1 (activities must prove they drew) being made by TS2 |

## Open (in order)
1. **TS2's F1** on player_check: re-run the mutant pmA (`with drawn()` removed from `run_activity`): it must now FAIL; and the new player_check on integration must still give the same output as `plans/review-opt/player_new_0.64.9.log` (5 min 54 s).
2. RN1 f75dd23: done (devmode_check OK, speed_probe OK).
3. **RN1 #5** (lead 24: run its full proof round when it arrives, no need to ask) (unloadDeck takes the old deck's tree apart; 2 lines in 4c; ~78 MB freed after a tour): due ~17:00. Proof to ask for/run: cadet_test ALL IDENTICAL, keep_shots (deck shots identical, all 7 decks, 2 sizes), merge_all.py, deck_check, perf_check memory, a tour of every deck twice with no errors, and a mutant (e.g. disposing a shared kit geometry/material) that a check must catch. Watch for kit shared between decks being disposed (textures/materials reused on the next deck), and anything holding the old deck (ITEMS, LAMPS, walkers) after unload.
4. **TS2 item 1** (affected-checks runner): after the account move, per lead 24.
5. #7: parked by lead 24, nothing to review.

## How to test (my probes, plans/review-opt/)
- Setup: `pip install playwright`; three r128 and acorn 8.12.1 in /tmp/cadet-work (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`; `mkdir -p /tmp/cadet-work/test`.
- `merge_all.py OLD NEW`: every mergeMeshes call anywhere (1583 calls incl. the lift roof), STAND, trimmed walls, tall pieces, seed → MERGE ALL IDENTICAL.
- `grain_all.py OLD NEW`: every grain() canvas and the seed → GRAIN IDENTICAL. `grain_mod.js`: the modulus trick in node.
- `speed_probe.py BUILD`: a Dev game with and without the Speed card's wrappers ends the same (blank `ship.career.gs`, a per-game random seed); the card's sizes; nothing wrapped without #dev. `speed_shots.py BUILD OUT`: the Dev sheet at phone sizes.
- RN1's `plans/opt-probes/keep_shots.py OLD NEW OUT` for deck shots.
- player_check: run integration's and the branch's copy on the same build, `diff` the outputs (both logs at 0.64.9 are in plans/review-opt/).

## Gotchas
- One browser check at a time (4 cores); a busy box changes shots and times.
- `pkill -f`/`pgrep -f` with a pattern in your own command line hits your own shell (it killed mine once).
- Background commands stop at their timeout (max 10 min in the foreground): run long checks with `run_in_background` and a long timeout, then wait with an `until grep -q ... ; do sleep 15; done` loop.
- `renderer.info` keeps the last drawn frame's numbers: any count read after undrawn steps is stale (the player_check F1).
- An equivalent mutant (e.g. `Math.hypot` for the normal's length) can give identical float32 bytes: not a gap in the proof.
- perf_check exits 1 on 0.64.8 for the known +2 geometries on the third round trip; career_check fails (backlog 12): both known.
