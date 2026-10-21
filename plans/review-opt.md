# Review: the optimization pass (OR1)

Reviewer: OR1, session_015np4rHB2UHzet5Y1zFrBzm, for lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r). Took over PR7's opt queue (PR7: session_01LyKAVtCEedL1bP73vqzu9v, who reviewed #4 and TS2's room fix). Branch claude/review-opt from claude/integration (3a48846). Probes in `plans/review-opt/`.

The user's rules for this work: no visual change at all (cadet_test ALL IDENTICAL, deck shots identical); no texture cache; the one exception, player_check may skip drawing in polling/arrive steps nothing reads.

Method per item: the diff read against the code it replaces; cadet_test old -> new; the item's own proof re-run, and my own probe where the author's didn't cover every caller; check_fast; 1-4 mutants planted to show the proof catches them. One browser check at a time.

## Verdicts

| Builder | What | Commit | Verdict |
|---|---|---|---|
| RN1 | perf_check busy event scenes | claude/opt-render 3af9f15 + 0ad9b5d | PASS WITH FIXES (F1 needed; F2-F4 small) |
| RN1 | #10 faster deck builds (4a-4c) | ab86ff7 (+ 960f2ce, 5358a60 docs) | PASS |
| RN1 | #6 grain loop | c1bf6f1 (+ 9604b97, 1a62fc7 docs) | PASS |
| TS2 | player_check fix A + fix B | claude/opt-tests 4775488 + e4acbf8 | PASS WITH FIXES (F1 needed, small) |
| TS2 | item 1 affected-checks runner | claude/opt-tests dffcfa1 is a draft ("rules half working") | waiting for TS2 to say it's ready |
| RN1 | #8 Dev Speed card | 3a77cfe + 08e380d (checked on the branch tip bddbc48) | PASS (nits N1, N2; section 25's owner to look) |
| RN1 | #7 lighter busy frames | ff6a712 measured, proposed parked | nothing built to review |

## RN1: perf_check busy event scenes (3af9f15 + 0ad9b5d), PASS WITH FIXES

Test-only diff (perf_check.py, DEV_NOTES, build table, opt-measure).

What I ran:
- `switched()` on its own against every branch's game (integration, fridays, line-update, patch-crew, storm-update): it changes exactly the switch lines and nothing else; fridays' `SHORT_FRIDAY = true` is left alone and counts as on; a switch that isn't in the file gives SKIP. Right on all 15 cases.
- Full perf_check (0ad9b5d's) on integration 0.64.8, alone: 11 min 12 s. The 8 old scenes stand in their rooms with the numbers of opt-measure's "with the fix" column; Friday x3 and Line x2 SKIP; the Tern row WAITING; exit 1 only for the known +2 geometries on the third round trip.
- `PERF_SCENES='Captain|after the address'` on claude/fridays: both measured switched on at all 7 views (174 / 209 / 171 ... and 204 / 274 / 232 ...), equal to opt-measure's table; PERF CHECK OK.
- `PERF_SCENES=Tern` on claude/patch-crew (Day 21 rotation now in): the Tern row measures (9 people now, T2 in) at all 7 views, PERF CHECK OK.

Mutants (pm1-pm3, the probe copies in my scratch):
- pm2, the `cells` block off: the rec lift lobby scene stands in the Main lift: 7 "you stand in Main lift" PROBLEMs, exit 1. Caught.
- pm3, no tile counted free: "FAIL: no free tile to stand on in Lift lobby", exit 1. Caught.
- pm1, the "already on" line removed: the Friday scenes SKIP on claude/fridays and the check still says OK. That's the design (a SKIP isn't a failure), so a lost scene is only visible on its line; see F4.

Fixes:
- **F1 (needed): the two storm scenes measure on builds without the storm.** `EVENTS_ON` is in every build since 0.64.8 (the events base), so on integration, fridays and patch-crew the "lantern supper" and "storm all-clear party" rows switch the base on and measure an ordinary Saturday supper (49 people, not the lantern supper) and a Sunday bow lounge (34). They print numbers like real measurements, and a later run with the storm merged would compare against them by name. Repro: `PERF_SCENES='lantern|all-clear' python3 perf_check.py` on integration 3a48846: both rows measured, "(switched on: EVENTS_ON)". Fix: give both a `needs`, e.g. `'needs': "typeof EV_STORM_ON !== 'undefined' && EV_STORM_ON"` (EV_STORM_ON = EVENTS_ON only on claude/storm-update), so they print WAITING until the storm is in.
- F2 (small): DEV_NOTES still says perf_check takes "about 5 minutes per build". It's 11 min alone on 0.64.8 with only the two storm scenes' 14 views running; with every switch merged the busy scenes add 8 x 7 views (about 8 more minutes).
- F3 (nit): `PERF_SCENES` is a case-insensitive search, so `PERF_SCENES=Tern` also runs "lan**tern** supper" (seen). The handover's example list is fine; say `\bTern` in the notes, or match from the start of a word.
- F4 (optional): print how many scenes were SKIPped or WAITING on the last line ("PERF CHECK OK (3 skipped, 1 waiting)"), so a switch renamed on a branch doesn't quietly drop its scene.

## RN1 #10: faster deck builds (ab86ff7), PASS

Read: `hullBeyond(x, z, d)` gives `hullDist(x, z) > d` for d >= 0: outside the hull both say no; a skipped segment's box, widened by d + .01, doesn't hold the point, so that segment is farther than d; the boxes are rebuilt whenever `HULL_SEGS` is a new array (every buildDeck). `mergeMeshes` reads each piece from its own arrays with three r128's own sums in the same order (Vector3.applyMatrix4 with the w divide; getNormalMatrix, applyMatrix3, normalize as divideScalar(length || 1)), groups in index space for indexed pieces as toNonIndexed's were, one float32 rounding either way, uv zeros for pieces without uv; anything interleaved or odd-sized takes the old copy-and-transform path. `tallCombine` copies whole arrays into one, the same numbers in the same order.

What I ran:
- cadet_test 3af9f15 -> ab86ff7: ALL IDENTICAL.
- **merge_all.py** (mine): every `mergeMeshes` call anywhere, not just the deck's (there are 20 callers: kit, cabin touches, the lift roof's shaft, the rec deck's mic, ...), fingerprinted right after it merges (FNV-1a over every resulting mesh's attribute and index bytes, groups, materials), plus STAND, the trimmed walls, tallCombine's meshes and ranges and the seed after each deck. Load, Decks 1 2 3 5 6 7 4 3, then the lift roof's `roofShaft()`: 1583 calls, MERGE ALL IDENTICAL.
- keep_shots.py (RN1's), 3af9f15 -> the branch's game (#10 + #6), three laps of all 7 decks at 390x844 and 844x390: all 14 third-lap shots 0 px different; programs stop at 22.
- check_fast on claude/opt-render 667725c (game = c1bf6f1): QUICK CHECK OK in 254 s (deck_check OK).

Mutants on merge_all:
- m10b, hullBeyond's margin d - .3 (skips segments it shouldn't): STAND differs on Deck 1 on. Caught.
- m10c, normals not normalized: differs at the first merge at load. Caught.
- m10d, uv halved for indexed pieces: differs at the first merge at load. Caught.
- m10a, `Math.hypot(nx, ny, nz)` for the normal's length: identical. An equivalent mutant (the double's last bit doesn't survive the float32 rounding), not a gap.

## RN1 #6: the grain loop (c1bf6f1), PASS

Read: for m = 2^31 - 1 and an integer 0 < s < m, x = 16807 s < 2^46 is exact in a double, x = hi 2^31 + lo with hi = floor(x / 2^31) exact (a power of two), and x mod m = hi + lo less m if that reaches m (hi + lo < 2m, so once is enough). Every seed the game sets is in range: the seven decks' `seed`s, Deck 4's 20 `floorSeeds` rows (84,604,698 to 2,116,181,630), 11 at load. The seed is written back once after the loop; `R` is a `const`, so nothing can have swapped it.

What I ran:
- gr.js in node: 30 M random seeds, the edge seeds (1, 2, m-1, m-2, 2^30, ...), and 20 M-step chains from 11, 48211 and 0: no difference from `(s * 16807) % 2147483647`.
- **grain_all.py** (mine): every `grain()` call's canvas pixels after (FNV-1a) and the seed after, at load and after each of two laps of all 7 decks (all 17 calls are at load; no deck build paints grain): GRAIN IDENTICAL, the seed after every deck the same.
- cadet_test ab86ff7 -> c1bf6f1: ALL IDENTICAL. Deck shots and check_fast as under #10 (they ran on the branch's game, which has both).
- Mutant m6a, the "less m" line removed: GRAIN DIFFERS at load. Caught.

## RN1 #8: the Dev Speed card (3a77cfe), PASS

Read: a seventh tab in `DM_TABS` and one line in `devmodeDraw` (section 25, the Dev mode engineer's), the rest in its own labelled block in the Dev mode slot. Three wrappers (renderer.render, requestAnimationFrame for `loop` only, goToDeck) installed only `if (DEVMODE)`, which needs #dev and real saving; each calls the wrapped function with the same arguments and returns its result. There's one `renderer.render` call in the game and nothing holds an old `goToDeck` reference, so every deck change is timed. Nothing calls R(); nothing goes into a save.

What I ran:
- cadet_test f13dc48 -> 3a77cfe (no #dev): ALL IDENTICAL.
- devmode_check (the branch tip's) on bddbc48: DEVMODE CHECK OK, 4 min 10 s, incl. "seven tabs ... the Speed card" and "off: the Speed card measured without #dev". check_fast on bddbc48: QUICK CHECK OK in 247 s.
- **speed_probe.py** (mine): a Dev game (#dev, real saving, 390x844) played 600 frames, Deck 3 and back, 600 more, with the card's wrappers and with them taken out: the clock, the deck, where you stand, every walker and the Dev save the same. (The save's only difference was `ship.career.gs`, a new game's own seed from Date.now and Math.random; it differs between two runs of the same build too, so the probe now blanks it.) Without #dev, render, rAF and goToDeck are the game's own and no size is recorded. The card at 390x844, turned 844x390 and the TriFold's 412x960: each size added to "Seen since opening"; the deck change, draw calls, shaders and memory lines filled; Copy's lines; Start again empties the frames. No errors.
- speed_shots.py (mine): the sheet at 390x844, 360x740, 412x960 and 960x412: seven 44px tabs (Speed alone on a third row), nothing wider than the screen, the card's text readable; the sheet scrolls to Copy and Start again.

Mutants (devmode_check off card):
- m8a, the wrappers installed without #dev (`if (true)`): "FAIL off: the Speed card measured without #dev". Caught.
- m8b, the Speed line taken out of devmodeDraw: "FAIL card: the Speed card says ''". Caught.

Nits:
- N1: section 25's header comment (game line ~51308) still says "six tabs, two rows of three".
- N2: DEV_NOTES has nothing on the Speed card yet: what it shows, that its times read 0 under the checks' virtual clock, and that its screen sizes are what perf_check's `TRIFOLD` table waits for.
- Owner: the `DM_TABS` line and the `devmodeDraw` line are in DB2's section 25 (the build-table row says the Dev mode engineer reviews); the lead routes that.

## TS2: player_check fix A (4775488) + fix B (e4acbf8), PASS WITH FIXES

Test-only (player_check.py, DEV_NOTES "Testing", build table). Fix A: the three places that stepped `window.__step` by hand now draw only each batch's last frame, as `Game.step` does. Fix B (the user's exception): `Game.step` is replaced in player_check by one that draws nothing unless inside `drawn()`; `run_activity`, `servery_seat` and the phone-layout block are inside it. The phone-layout block now sets the toast itself (it read a real-time 5.6 s `setTimeout` before).

What I ran, on integration 0.64.9 (f782c5d), alone:
- integration's player_check: PLAYER CHECK OK, 21 min 45 s.
- opt-tests' (fix A + B): PLAYER CHECK OK, **5 min 54 s**. Output identical line for line except "phone, at rest", where the toast is now cleared by the check (TS2's reported difference, explained).

Mutant:
- pmA, `with drawn()` taken out of `run_activity` (activities no longer drawn, against the user's rule): **PLAYER CHECK OK**, exit 0. Every activity reports `calls<=196`: `renderer.info` keeps the last drawn frame's numbers, so the 450-budget check (`peak < BUDGET`) read a stale count from somewhere else. Not caught.

Fix:
- **F1 (needed): make the drawn parts prove they drew.** In `_run_activity` and `_servery_seat`, read `renderer.info.render.frame` before and after (three r128 adds one per drawn picture) and fail if it didn't move ("the activity wasn't drawn"); or have STATE return `calls` only when the frame moved since the last read. pmA should then FAIL. The rule is the user's exception's own condition ("activities and the servery's draw-call budget still drawn"), so the check should guard it, not just follow it.
- The rest reads right: everything outside `drawn()` still simulates every frame; the screen-click parts (treadmills, Repair) project and ray-cast with the same camera matrices, and the output diff shows they land the same.

## Log

- 2026-10-21: took over PR7's opt queue; told PR7. RN1 has since written plans/handover-opt-render.md (RN1 idle); #7 measured and proposed parked (nothing built), #8 built.
- #8 reviewed on the branch tip (bddbc48, which has integration 0.64.9 merged in): PASS.
- perf_check items: F1-F4 sent to RN1 and lead 24. RN1 is handed over, so lead 24 says who makes F1 (a two-line change in perf_check.py's SCENES).
