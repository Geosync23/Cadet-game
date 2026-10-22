# Review: the optimization pass (OR1)

Reviewer: OR1, session_015np4rHB2UHzet5Y1zFrBzm, for lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r). Took over PR7's opt queue (PR7: session_01LyKAVtCEedL1bP73vqzu9v, who reviewed #4 and TS2's room fix). Branch claude/review-opt from claude/integration (3a48846). Probes in `plans/review-opt/`.

The user's rules for this work: no visual change at all (cadet_test ALL IDENTICAL, deck shots identical); no texture cache; the one exception, player_check may skip drawing in polling/arrive steps nothing reads.

Method per item: the diff read against the code it replaces; cadet_test old -> new; the item's own proof re-run, and my own probe where the author's didn't cover every caller; check_fast; 1-4 mutants planted to show the proof catches them. One browser check at a time.

## Verdicts

| Builder | What | Commit | Verdict |
|---|---|---|---|
| RN1 | perf_check busy event scenes | claude/opt-render 3af9f15 + 0ad9b5d, fixes fe0726b | **PASS** (F1-F4 fixed in fe0726b, confirmed) |
| RN1 | #10 faster deck builds (4a-4c) | ab86ff7 (+ 960f2ce, 5358a60 docs) | PASS |
| RN1 | #6 grain loop | c1bf6f1 (+ 9604b97, 1a62fc7 docs) | PASS |
| TS2 | player_check fix A + fix B | claude/opt-tests 4775488 + e4acbf8 | PASS WITH FIXES (F1 needed, small) |
| TS2 | player_check F1 (activities prove they drew) | claude/opt-tests 26e6902 | **PASS** (OR2: OK on 0.64.11, mutant pmA fails) |
| TS2 | item 1 affected-checks runner | claude/opt-tests dffcfa1 is a draft ("rules half working") | waiting for TS2 to say it's ready |
| RN1 | #8 Dev Speed card | 3a77cfe + 08e380d (checked on the branch tip bddbc48) | PASS (N1 fixed 7d84c86, N2 fixed 5850ddb; f75dd23 moves the start-up line below the Speed block (DB2's nit): devmode_check OK and speed_probe OK on it, confirmed) |
| RN1 | #5 stale decks let go (unloadDeck) | claude/opt-render cd9d030 (row dfd662d), tip 862722f | **PASS** (OR2, below) |
| RN1 | #8 Dev Speed card, final | tip 862722f | **PASS**, no nits left (OR2: devmode_check OK on integration 0.64.11 + opt-render) |
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

## RN1 perf_check fixes (fe0726b), confirmed

- F1: `PERF_SCENES='lantern|all-clear|Tern'` on integration 0.64.8: all three WAITING; last line "PERF CHECK OK (0 skipped: switch not in this build; 3 waiting: not built yet)" (F4). On claude/storm-update `PERF_SCENES=lantern`: measured (62 people, 260 / 417 / 293 ...), equal to opt-measure's row.
- F2: DEV_NOTES says about 11 minutes alone. F3: the search is case-sensitive now ('Tern' ran only the Tern row).

## RN1 f75dd23 (Dev start-up line moved below the Speed block), confirmed

- The only change: `if (DEVMODE) { devmodeCss(); devmodeBuild(); devmodeState(); }` now runs after the Speed card's wrappers are in place. devmode_check: DEVMODE CHECK OK. speed_probe.py: SPEED PROBE OK (a Dev game with and without the wrappers ends the same: save, clock, deck, place, walkers; nothing wrapped without #dev; sizes listed).

## Where this stopped (17:55, account handoff)

- TS2's F1 (26e6902) arrived, not yet re-run here. RN1 #5: code read, cadet_test ALL IDENTICAL; the rest of its proofs are listed in plans/handover-review-opt.md.

## Log

- 2026-10-21: took over PR7's opt queue; told PR7. RN1 has since written plans/handover-opt-render.md (RN1 idle); #7 measured and proposed parked (nothing built), #8 built.
- #8 reviewed on the branch tip (bddbc48, which has integration 0.64.9 merged in): PASS.
- perf_check items: F1-F4 sent to RN1 and lead 24. RN1 is handed over, so lead 24 says who makes F1 (a two-line change in perf_check.py's SCENES).

## OR2 (session_01AnRKXUUGi8mwREwvt4WbaV, lead 25 session_01J2aTyEohBf8KFHCsTqt3LW), from 2026-10-21 after the account move

### TS2 player_check F1 (26e6902): PASS
- opt-tests' player_check on integration 0.64.11 (70aa91f): PLAYER CHECK OK, exit 0, 5 m 44 s. Against `player_new_0.64.9.log`: the same lines except the `calls<=` counts, all lower on 0.64.11 (its closer camera); needs, times and poses identical.
- Mutant pmA (`with drawn()` taken out of run_activity): FAIL on every activity ("Shower: drawn ... frame 1 -> 1"), exit 1. Caught.
- Merge note: opt-tests clashes with integration in perf_check.py (f5d6815 vs the Fridays scenes de18921) and the build table; opt-render carries f5d6815 and RN1's later perf_check, so merge opt-render first and take its perf_check.

### RN1 #5 (cd9d030, tip 862722f): PASS
Builds (in /tmp/or2, made by merging, nothing pushed): **r5** = integration 0.64.11 (70aa91f) + claude/opt-render 862722f (the game merges cleanly; perf_check.py and the build table clash, see below); **sf5** = integration + claude/storm-update 0b77dfc + claude/fridays 6e8e0af + opt-render (EVENTS_ON and SHORT_FRIDAY on, as the release will have them). The "old" of each is the same file with #5's one line taken out (r5_no5, sf_no5).
- detach_play.py (OR1's probe; now takes `DP_TIMES`): r5, events off and on: DETACH PLAY OK, 43 decks unloaded each, no errors. sf5: OK on Days 0-7, and again with `DP_TIMES` = Day 11 19:00, Day 12 14:30 / 16:15 / 17:25 (the storm front, the address, the Friday dinner), Day 13 20:00, Day 14 10:30, Day 19 16:15, Day 21 11:00: 64 decks unloaded, no errors.
- Mutant m5a (one Group shared between decks, added to each new deckRoot): BACK on every deck change. Caught.
- cadet_test r5_no5 -> r5: ALL IDENTICAL. sf_no5 -> sf5: ALL IDENTICAL (one earlier run had 1-level noise on j_steer1/2; the rerun and old vs old were exact). int -> r5 (all of opt-render on 0.64.11): ALL IDENTICAL.
- keep_shots r5_no5 -> r5: DECK SHOTS IDENTICAL. **sf_no5 -> sf5: 2 pixels 1 level off on Deck 7 at 390x844, both runs; old vs old identical.** Found why: they are on the glow of the REC DEC sign (KIT.recBigSign, a 1024x300 canvas drawn with `shadowBlur`, no R()). With the test browser's graphics-chip canvases on, that canvas's pixels change from lap to lap **in the old build too** (scene_dump2.py: three laps, three different hashes in each build), because Chromium draws a canvas on the chip or not depending on what else it holds, and #5 changes what it holds. Every object, matrix, material and light in the Deck 7 scene is the same old vs new (scene_dump.py). With `--disable-accelerated-2d-canvas` the sign is the same on every lap and in both builds, and keep_shots_cpu.py gives DECK SHOTS IDENTICAL on sf. So it's the browser, not the game: the game draws the same thing. (The same could show on any later change that moves memory around; the deck-shot proof with that switch is the steady one.)
- merge_all r5_no5 -> r5: MERGE ALL IDENTICAL.
- day_check Day 12 on sf_no5 and sf5: output identical line for line; both DAY CHECK FAILED with "the rec deck is on but nobody came to it in the evening" (the storm; RN1 saw it on Day 13; **Day 12 too on the combined release build**: not #5's, for the release).
- check_fast on r5: QUICK CHECK OK in 256 s. devmode_check on r5: DEVMODE CHECK OK (also closes #8).
- Merge: claude/opt-render into integration: the game merges cleanly; perf_check.py clashes in two places (SCENES and SCENE_JS): take opt-render's side in both, since it already holds de18921's three Friday scenes (with 'on'/'busy') and FR3's 'cells' on top of the room fix. The build table: keep both sides' rows.

### PB2's section 14 double-meal fix (claude/patch-b2 be8871d + 21dc0e1, on line-update 8bfff3b): PASS (lead 25's ask)
Run on claude/integration a4a5735 (old) and a4a5735 + be8871d's 3 lines (new; the patch applies unchanged).
- Code read: `meet` is `gatherings(p, d, F)`, new objects on every call (the eventPlan entries are copied into fresh literals; eventMeetPlan's have no `meal`), so `e.ate` lives only inside one person's plan for one day: no leak across people, days, replans or saves (nothing saves `meet` or a plan; shipDay rebuilds on load). `tradMeal` always ends in a meal (a seat, or `seg(e.meal, ...)` standing), so `ate` is never set without eating. `morning()` and `evening()` run once per plan (the GB / day / night branches don't overlap). The planner reads nothing built during play.
- double_meals.py (every crew member's plan, a meal = a run of that meal's segments, a gap under 10 min the same meal), Days 1-28: old 4 (Day 21 bramwell-basil, amadi-asha, santos-zofia; Day 28 mbeki-bo), new 0. no_meals.py: the list of plans with no breakfast or no dinner identical old/new over Days 1-28 (nobody loses a meal).
- cadet_test old -> new: ALL IDENTICAL.
- day_check 21 and 28: DAY CHECK OK both, old and new. Servery line Day 21 135 -> 132 joined, Day 28 133 -> 132 (exactly the second dinners gone); small evening count shifts.
- food_check 21 8: FAILED old and new with the same one line (garden good, backlog 23); new: Day 21 came to eat 155 -> 152, wasted 3 -> 6; Day 28 153 -> 152, wasted 5 -> 6 (the galley cooks the same 150; the doubles had been eating the spare). Not a fault; FYI to the food seat.
- Note, not a blocker: the GB branch (gap-based days) keeps its own `ate[m]` table, which a tradition eaten inside `leisureUntil` doesn't update; nothing doubles there in Days 1-28, so no change asked.

### TS3: opt item 1, the affected-checks runner, option (a) "Careful" (claude/opt-tests 7009b108): PASS (two optional nits)
Test-only: tools/affected.py, tools/affected_replay.py, tools/check_map.json (all 28 checks under check_cover on a4a5735), plans/opt-cover/, DEV_NOTES "Testing". No game change.
- Code read: `translate` (moving a line from an old commit into the map's game) is right for changes, pure insertions and deletions; the table/state step looks the old game's declaration up in the map's game's uses; a section not in RULES runs every check (`RULES.get(s, ['*'])`); a check file picks itself, cadet_test.py picks all.
- `python3 tools/affected_replay.py`: output identical to plans/opt-cover/replay-0.64.12.txt, 23 of 23, exit 0, about 70 s. (It needs the whole history: on a shallow clone 6 commits say "not in this clone" and it exits 1; `git fetch --unshallow` first, as it says.)
- Mutants: intro taken out of the map: exit 1, "155f0d4 intro" missed (both rows). mech taken out: exit 1, "1c4bc67 mech". translate made to return the lines unmoved: exit 1, 155f0d4 intro missed (so the line-moving is really tested).
- Item 5 (ee48072 counted against 155f0d4): accepted. ee48072's parent already had 155f0d4's escort, ee48072 with 155f0d4 reverted passes intro --evening, and intro_check never taps the floor, so ee48072 broke nothing; 155f0d4, where the failure came in, is picked (by the map). Adding intro to section 11's rule would cost 11 min on every section-11 turn for nothing.
- Plain `intro_check.py` (the tool's command) runs part 8, the evening, too, so picking "intro" does run the part that failed.
- Weak spot, not a fault: of the 23, only 155f0d4 (7 checks) and 1c4bc67 / 1f91e90 (20-21) are commits where the tool doesn't pick everything; the rest prove only that the full round catches them.
- Nit N1 (optional): LOAD_CHECKS (cadet, deck) are added only when no changed line was hit by any check; a change that touches both a load-only line and a played line doesn't add cadet. Today only section 18f has load-only lines outside a rule with cadet (the Friday address's registration and its save loading, 11 lines, which the 18f rule's events/fridays cover), so harmless; dropping `not hit and` costs at most 2 min.
- Nit N2 (optional): `--map` pointing to a file that isn't JSON (e.g. /dev/null) ends in a traceback.
- Note for the lead (not this item): the tool's day_check is Day 1 only; RN1's and my storm-day findings (day_check 12/13) show later days fail on their own. The release round should name the event days it runs.
- Merge: the same perf_check clash as before; after opt-render, take opt-render's side of both hunks (it holds everything opt-tests has plus PR7's noSpot guard). Build table: keep both.

### TS3: option (b) "Middle" on trial (claude/opt-tests 975ca4cc): PASS WITH FIXES (one DEV_NOTES clause); (b) rightly not adopted
- `affected_replay.py --middle`: output identical to plans/opt-cover/replay-0.64.12.txt; (a) 23/23 and (b) 23/23, exit 0. `--middle` is off unless asked, so (a) is unchanged (the 7009b108 replay still holds).
- **F1, a hole in (b)'s safeguard:** it fires only on changed *lines* that are shared. A changed *table or state* is read by lines, and under --middle those reads drop the shared lines (`uses - shared`), so a table read during play only by shared lines picks nothing from the map and doesn't fire the safeguard: only its section's rule is left. 222 tables/state are like that on the 0.64.12 map (e.g. MEALS-like: TRAD_LINE read by 27 checks, MACH_WORKS 27, JOB_MAKE 26, DAY/NIGHT 24). Shown: `DAY`'s hemi .85 -> .86 in the working tree: (a) 21 checks, 97 min; (b) 3 checks (cadet, perf by the rules; devmode by the map), 22 min, no safeguard. MACH_WORKS would run only section 17's four. If (b) is looked at again, the safeguard must also fire when a changed table/state has a use among the shared lines; that would make (b) cost more still, so the decision not to adopt it stands even firmer. **Fix asked:** one clause in DEV_NOTES' "Option (b)" paragraph saying this, so a later look starts from it.
- Suggestions for that later look (not needed now): a pure insertion fires the safeguard only when *both* neighbours are shared; one shared neighbour is enough to be careful (an insertion at the edge of shared code). SHARED as a share of the map's checks (e.g. 80%, rounded up) rather than a fixed 23, so adding checks doesn't change its meaning.

### Corrections to my own notes (OR2, 22:10)
- **detach_play's day labels were one day late.** `setShipNow(abs)` makes minute 0 Day 1, but the probe (and my `DP_TIMES`) used `d * 1440` as if minute 0 were Day 0. So the "Days 0-7" pass was Days 1-8, and my "Day 11 ... Day 21" pass was Days 12-22 (it missed the Day 12 address and the Day 21 arrival). Rerun on sf5 at the right minutes, Day 12 14:30 / 16:15 / 17:25, Day 13 18:30 / 20:00, Day 14 19:30, Day 19 16:15, Day 21 17:40 (`DP_TIMES="((11,870),(11,975),(11,1045),(12,1110),(12,1200),(13,1170),(18,975),(20,1060))"`): DETACH PLAY OK, 64 decks unloaded, no errors (`review-opt/detach_sf5_eventdays.log`). #5's PASS stands.
- **day_check Day 12's "rec deck is on but nobody came" is backlog 18,** which fails on plain integration with the storm off too (0.64.6, and fridays with SHORT_FRIDAY off). It isn't the storm's; the storm's Saturday (Day 13) is the other case (EV4's 4fa198f). Still not #5's (old and new identical).

### TS3: item 1 additions (02f9efdb) and the testing guide (9bdad796)
- 02f9efdb: N1 fixed (load-only lines always add LOAD_CHECKS), N2 fixed (a bad --map exits 2 with a message). The event days as entries (day0/5/7/12/13/16/19/21/27, 8 min each): the full round is now 33 checks, 176 min. day_check.py changed picks day1 + every event day. Fine. Nit N3: affected_replay.py still maps any `day...` failure to `day1` (`'day1' if w.startswith('day')`); now that the days are their own entries, a known failure on, say, day13 should be scored against `day13`. Not yet reachable (failures.md has only day1).
- affected_planted.py on paper: read; the six faults are each outside their section's rules. Waiting for `--run` (each fault must really fail its check) before a verdict on it.
- testing-guide.md, fact-checked line by line against the checks, tools and notes: most of it is right (every OK line, every flag, minutes, the rules table, the event-days table, the release steps). To fix:
  1. L121: the Day 12/13 row says backlog 18 is the storm. Backlog 18 is Day 12 failing with the storm off too (0.64.6; fridays with SHORT_FRIDAY off); the storm's Saturday (Day 13) is the separate 4fa198f case. Split it into two rows.
  2. L370: "Results: plans/opt-cover/planted.md" doesn't exist yet (make it with --run, or drop the line).
  3. L171: "35 (the next rotation)": ROSTER_ROTATIONS is Days 21 and 77 now.
  4. L118: "520 -> 520 -> 522": backlog 14 and the build-master note give 548 -> 548 -> 550.
  5. L265: "Dev mode turn picks 1 check; crew, events or Fridays 20-24": the replay has a Dev mode turn at 23, a crew turn at 6, an events turn at 10. Say it varies (DEV_NOTES L1546 has the same).
  6. L172-173, L296: adding an event day needs its tuple in `CHECKS` too (not only EVENT_DAYS), and cov_run.sh has no day list (its `day[0-9]*` case runs the days named). The map has no event-day covers yet, so they pick by the rules only; DEV_NOTES L1544's "and by the map" is ahead of itself.
  7. L221: load-only lines pick cadet (deck is check_fast's, never listed); L225 already says so.
  8. L321: the (b) column shows only with --middle.
  9. L358: planted "on paper (40 s)": no source; --run is "about 40 min".
  10. L352 "only 3 of the 14": two more commits pick 23 of 24; say "well under all" for 3.
  11. DEV_NOTES' setup says only `pip install playwright`; the guide's `playwright numpy pillow` is right (cadet_test imports both). Fix DEV_NOTES.

### PB2: backlog 18's fix (claude/patch-b2 38424f0, row 8bffab5): FAIL for now (a new day_check 13 failure); the code change itself is right
Run on integration a4a5735 old vs a4a5735 + 38424f0's lines (applies unchanged).
- Code read: `schedU` is a pure hash, so rolling it once earlier changes no other number; `si` is read nowhere else; with `stay` true the old branch is taken exactly as before; the only change is the intended one (a stayIn block that loses the roll can go to the rec deck again).
- plan_days.py (every plan, Days 1-35, events off): only Days 11, 12, 13 change (30, 29, 21 people). Rec deck segments ending after 17:00: Day 11 65 -> 217, Day 12 0 -> 158, Day 13 200 -> 227 (ordinary days 254-313).
- cadet_test: ALL IDENTICAL. check_fast on the new build: QUICK CHECK OK in 227 s.
- day_check 12: old FAILED (backlog 18), new **OK** (rec deck mean 4.1, peak 11). day_check 11: new OK.
- **day_check 13: old OK, new FAILED, "deck 3: kovac-zainab 09:31 stuck 15.7 ship minutes"; the same on a second run** (logs b18_day13_old.log / _new.log). Her plan is the same old and new (09:15 lift to Deck 3, the grab shelf 3-grab-1, 09:17 lift to Deck 5 for her 09:20 shift), and nobody's Deck 3 plan before 15:00 differs. What does differ is the crew's needs going into Day 13 (06:30 lowest social 38 -> 17; Day 12's evenings changed), so the live crowd on Deck 3 that morning behaves differently and she is held 15.7 min between the grab shelf and the lift. Probably a crowd/lift weakness this only exposes, but a check that passed now fails: find out why before merging (CLAUDE.md).
- **Update (23:40), PB2's trace:** what holds kovac-zainab is two different jobs booked at 3-lights-1-panel for the same 09:12-09:32 walk (her storm chore `event:ionStorm:stormBallasts@9`; moreau-signe's service `3-lights-1@276`). Moreau sits first and kovac waits on the walk-to tile until 09:32. Section 17's job routing doesn't check other jobs' bookings of a place. PB2's on-paper scan of the build WITHOUT the fix finds the same kind of clash on Day 13 (3-oven-1-panel) and Day 30 (1-relay-1-panel). day_check 14 and 15 with the fix: OK. Consistent with what I see: both plans are Works shifts on Deck 5 and the same old and new (the jobs are laid over them while the game runs). I haven't rerun the trace. **Verdict: PASS once lead 25 OKs the section 17 backlog row;** please commit the scan script so the row can be reproduced.

### PB2: section 17 double booking (claude/patch-b2 5b4eb4f, scan 5843d29, rows 135caaf) + backlog 18 (38424f0): PASS, both
Run on integration a4a5735 + 38424f0 + 5b4eb4f's lines (b2_new), against a4a5735 + 38424f0 (b_new) and a4a5735 (b_old).
- Code read: at the end of jobRun, a stop at a machine's panel that another not-done job (its segs, or a team job's segsBy) holds at an overlapping time makes the run null: the hour's next crew member, or the next hour (the path a job that doesn't fit already takes). Stale bookings can't block: segs are set only when crew claim a job, and deleted when you take it (18334); a team job's members have their own spots and `o !== j` skips the job itself. jobRun already ran inside the hourly job loop that reads SHIP.jobs, so no new kind of read.
- jobclash.py (Days 1-60, any place): b_old 2 clashes (Day 13 oven panel, Day 30 relay panel), b_new 3 (Day 13 oven, Day 40 cart dock, Day 57 2-works-5), b2_new **[]**. Note: the scan is on paper and doesn't show the 3-lights-1 clash day_check's live run hit on Day 13 morning; day_check 13 is the proof for that one.
- day_check 13 on b2_new: **OK** (Deck 3 worst stuck 4.1, teague-theo, as before backlog 18's fix). day_check 30: OK (old OK too). mech_check: MECH CHECK OK. cadet_test b_new -> b2_new: ALL IDENTICAL. check_fast on b2_new: QUICK CHECK OK in 219 s. From before: day_check 11, 12 OK with backlog 18's fix; PB2: 14, 15 OK.

### TS3: item 1 final (claude/opt-tests da8e97ca): PASS
- My 11 guide fixes (492eafbf) are in; N3 fixed (the replay scores a dayN failure against dayN). DEV_NOTES' setup installs numpy pillow.
- The map: 37 entries (28 checks + 9 event days), all on a4a5735's game. `--middle`'s SHARED is now 80% of the map's checks, rounded up.
- `affected_replay.py --middle`: part 2 identical to plans/opt-cover/replay-0.64.12.txt; (a) 23/23, (b) 23/23, exit 0. Cost now (event days in): (a) 24.2 of 33 checks, 132 min on average; full round 176; rules alone 12.4, 73.
- `affected_planted.py` on paper: 6 of 6 picked by (a) and (b), the rules missing each (each fault's check is outside its section's rules), exit 0.
- `--run`, rerun by me on two behaviour faults: "your tasting vote is not kept" (18 -> food): exit 1 against 0 on the game as it is, 2 new FAILs (the tally, your tastes). "a due tool no longer slows a look step" (15 -> mech): exit 1 against 0, 1 new FAIL ("a look step with a due tool takes a quarter longer"). Both as TS3 reported. The throwaway worktrees were cleaned up (no stray branch or worktree).
- The counting rule (`fails()`): a FAIL or error line that the game as it is doesn't print, numbers set to '#' first, or exit 1 where the base exits 0. Numbers to '#' means a known FAIL whose numbers move doesn't count as new: it under-claims, the safe side.
- Crash typos as faults (3 of 6): fair. They are the commonest real break, and a check catches one only if it runs that line, which is what the map claims. But they prove coverage, not that a check notices wrong behaviour. The 3 behaviour faults (escort, tool slow-down, tasting vote) are the stronger evidence, and the six that left their checks green (listed in planted.md) are real check gaps for their owners.
