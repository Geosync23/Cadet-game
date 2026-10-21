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

## Open (in order), as of 17:55 on 2026-10-21 (stopped by lead 24 for the account handoff)
1. **TS2's player_check F1**: claude/opt-tests 26e6902 (handover c2c7955). run_activity and servery_seat read `renderer.info.render.frame` before and after and FAIL if it didn't move. TS2 reports: PLAYER CHECK OK in 310 s on 0.64.8, output identical to A+B; mutant pmA exits 1 ("FAIL Shower: drawn ... frame 1 -> 1"). To do: re-run pmA and the new player_check on integration yourself; diff against `plans/review-opt/player_new_0.64.9.log`; check_fast (TS2 didn't re-run it).
2. **RN1 #5** (unloadDeck takes the old deck's tree apart; claude/opt-render cd9d030, row in dfd662d; lead 24: run its full proof round when you resume). Done so far: code read (walkers and the player are added to `scene`, not deckRoot; the `.parent` reads either rebuild per deck, allow null, or only touch stale invisible pieces: REC_SHOW's `!m.parent` early returns, GV checks `GV.root !== deckRoot`, `rigProps` runs on rigs in `scene`); **cadet_test cd9d030^ -> dfd662d ALL IDENTICAL**. Not done: `plans/review-opt/detach_play.py BUILD` (my probe: arrival evening, every deck at five times over Days 0-7, a 2-day skip, events off and on; no unloaded-deck object back in the scene, no errors; it was killed mid-run), its mutant (the scratch file m5a: a Group shared between decks added to each new deckRoot right after `deckRoot = new THREE.Group(); scene.add(deckRoot);`: the probe must report BACK), keep_shots (deck shots, 2 sizes), merge_all.py, check_fast. RN1's own proofs are in the dfd662d build-table row.
3. **TS2 item 1** (affected-checks runner): not ready (plans/handover-test-speed-2.md); after the account move.
4. #7: parked by lead 24.

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
