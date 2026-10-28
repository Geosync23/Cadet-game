# Handover: the optimization pass, render seat (RN1)

From RN1 (the render seat), 2026-10-21, for whoever picks up the render items or review fixes next. Lead: lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r; lead 23 handed over at ~12:40). Reviewer: OR1 (session_015np4rHB2UHzet5Y1zFrBzm), the optimization reviewer; PR7 (session_01LyKAVtCEedL1bP73vqzu9v) reviewed #4. Test-speed seat: TS2 (session_019Ue76BxEtDwCcqQjJHjFHp).

## Role, branch, builds
- **Branch:** `claude/opt-render`, made from `claude/integration` 3a48846 (0.64.8). It has TS2's perf_check room fix (claude/opt-tests c2a32e2) and DB2's claude/devmode-2 merged in, and integration 0.64.9 (f782c5d) merged in at the end.
- **Build number:** never touched (the build master's).
- **Every row** is in `plans/build-table.md`: "opt #4 shaders kept (RN1)", "perf_check event scenes (RN1)", "opt #10 faster deck builds (RN1)", "opt #6 grain loop (RN1)", "opt #8 Dev Speed card (RN1)". The numbers and how they were measured are in `plans/opt-measure.md` section 5. The plan page (`plans/opt-plan.html`) is marked item by item.
- **The user's answers that shaped this:** q2 no texture cache; q4 a Dev Speed card, and the user's phone is a Samsung Galaxy Z TriFold; q6 and again today, "don't change the look of the game"; q7 watch the mess and act only when something new goes in. The added ask: the busy event scenes in perf_check at phone and TriFold sizes.

## Every opt-plan item and its state

| # | Item | State | Who |
| --- | --- | --- | --- |
| 0 | perf_check measures the right rooms | done | TS2 (claude/opt-tests c2a32e2) |
| 1 | run only the checks a change affects | test-speed seat's: see its handover | TS2 |
| 2 | where player_check's 37 minutes go | test-speed seat's | TS2 |
| 3 | the crowd sends less to the graphics chip | **parked: measured, not worth it** (the plan's bytes were a miscount, and day_check's "upload" time was drawing) | RN1 |
| 4 | keep compiled shaders across deck changes | **done, PASSED** (PR7); ready for the build master (6fd3505) | RN1 |
| 5 | find what fills the extra 134 MB | **built** (lead 24's OK): `unloadDeck` takes the old deck's tree apart, so ~78 MB of stale decks is let go; proofs running at the push (see the row), then OR1 | RN1 |
| 6 | paint texture grain faster, same pixels | **loop built, in review** (OR1); the rest **parked: the only real gain changes pixels, the user said no** | RN1 |
| 7 | lighter busy frames | **parked: measured, small** (at most ~0.15-0.2 ms of 2.4 across 4-5 owners) | RN1 |
| 8 | Dev mode Speed card | **built, in review** (OR1) | RN1 |
| 9 | texture cache | **cut by the user** (q2: no cache) | |
| 10 | faster deck builds | **built, in review** (OR1) | RN1 |
| 11 | resumable long checks, the round shared out | test-speed seat's | TS2 |
| 12 | saved starting points | **not in this pass** (the user's q5) | |
| 13 | draw-call headroom in the mess hall | **watch only** (q7); the new event scenes show it: the Line supper 419 and the lantern supper 417 of 450, zoomed out | RN1 / whoever adds to the mess |
| — | perf_check busy event scenes (the user's ask) | **built, in review** (OR1) | RN1 |
| — | the kit's shape cache (proposal) | **parked by lead 24** (modest gain, medium risk in the kit; revisit after the events land) | |

## Before and after

| What | Before | After | How measured |
| --- | --- | --- | --- |
| First frames after 7 deck changes, laps 2-3 (with a real wait after each frame) | 12.4 / 11.1 s | 10.9 / 10.6 s | `opt-probes/keep_true.py`, 390×844 |
| Shader programs rebuilt per deck change | 2-5 every change (16-18 alive) | none after the first lap (22 kept) | `opt-probes/keep_shots.py`, both phone sizes |
| Building all seven decks | 2.27 s | 1.33 s (Deck 3 599 → 346 ms, Deck 2 486 → 264, Deck 4 451 → 270) | `opt-probes/merge_bytes.py`, best of 5 |
| The grain at load (17 calls, 3 runs each) | 685-744 ms | 621-667 ms (the loop itself is 26 ms of it now; the rest is `getImageData`'s readback) | `opt-probes/grain_load.py`, `grain_split.py` |
| Busiest event scene (draw calls) | not measured | the Line supper 419, the lantern supper 417 of 450 (zoomed out, the mess) | perf_check event scenes |
| Array storage after visiting every deck (Deck 4) | 134.6 MB | 61.3 MB (perf_check's JS heap after round trips 228 → 87 MB) | `opt-probes/heap_tour.py`, perf_check |
| Crowd uploads in play (Sunday dinner) | (plan: 4.4 MB spikes) | measured right: 31 KB typical, 1.69 MB at most; left as is | `opt-probes/buf_play_true.py` |

Every built change was proven with the same pictures: cadet_test ALL IDENTICAL, plus each item's own proof (shots of every deck, merged bytes, grain fingerprints and the seed), and check_fast OK.

## What I built, where
- **Section 1** (`keepShaders`, `KEPT_PROGRAMS`), with one call in section 12's `loop()` right after `renderer.render`.
- **Section 2** `grain()`.
- **Section 4a** `hullBeyond`, `HULL_BOX`.
- **Section 4b** `mergeMeshes` (two passes, `MERGE_N3`) and `tallCombine`.
- **Section 4c** the three `hullBeyond` calls in `buildDeck`.
- **Section 25** (in the Dev mode slot, its own labelled block): `DM_SPEED`, `devmodeSpeed*`, the `speed` entry in `DM_TABS` and the line in `devmodeDraw`.
- **Checks:**
  - `perf_check.py`: `on`, `busy`, `TRIFOLD`, `cells`, `needs`, `PERF_SCENES`, `switched()`, scenes compared by name.
  - `devmode_check.py`: 7 tabs, the Speed card's text, nothing measured off.
- **Probes** in `plans/opt-probes/`:
  - `buf_true`, `buf_play_true`
  - `keep_true`, `keep_shots`
  - `merge_bytes`, `build_prof`, `shapes`
  - `grain_bench`, `grain_load`, `grain_split`, `wrf`
  - `prof_mess2`, `rigcount`, `layout_reads`, `speed_shots`

## Gotchas
- **Time a frame only with a real wait.** In this Chromium with SwiftShader, `gl.finish()` returns at once. A frame's drawing is billed to whichever later call syncs (a buffer upload, a shader compile, `getImageData`). Wait with `gl.readPixels` of one pixel. The plan's day_check "74% uploads" and the 9.2 → 6.3 s shader figure both came from this.
- **The byte counts:** WebGL2's `bufferSubData(target, offset, array, srcOffset, length)` sends `length`, not `array.byteLength`.
- **Don't name a probe's variable `HOOK`, `INIT`, `THREE` or `WORK`** when you `exec` cadet_test's top half: `instrument()` reads the global `HOOK`, and the game then fails to start with no error.
- **`pkill -f` with a pattern that's also in your own shell's command line kills that shell.** Use `pgrep` and skip `$$`.
- **The test browser's clock is virtual** (cadet_test's INIT), so the Speed card's times read 0 in shots. On the phone they're real.
- **The Line branch (claude/line-update) clashes with the current storm update in 5 places** in the game code: it was built on the older storm with standing diners. Measure its scenes on that branch alone until the Line builder merges it.
- **`switched()`** flips `const NAME = false;` or `= SOMETHING_ON;` by text and leaves `= true` alone. A switch missing from the build gives SKIP, not a failure.

## How to test
- `python3 cadet_test.py OLD NEW` (ALL IDENTICAL), then `bash check_fast.sh`.
- #10: `python3 plans/opt-probes/merge_bytes.py OLD NEW` → MERGED SHAPES IDENTICAL.
- #4: `python3 plans/opt-probes/keep_shots.py OLD NEW OUTDIR` → DECK SHOTS IDENTICAL, programs stop at 22.
- #6: `python3 plans/opt-probes/grain_load.py BUILD TMP.html` on both builds and compare the FP lines.
- #8: `python3 devmode_check.py BUILD` (or `... off card`).
- Event scenes: `PERF_SCENES='address|dinner|lantern|all-clear|Line|Tern' (case matters) python3 perf_check.py BUILD` on a build with those branches merged. The full `perf_check.py` is the check itself.
- Every command needs `CADET_CHROME=/opt/pw-browsers/chromium`, plus three and acorn in `$CADET_WORK` (DEV_NOTES "Testing").

## Loose ends
- OR1's verdicts on the four items in review. Fix and push on this branch, and tell lead 24.
- The TriFold's CSS sizes in `perf_check.py`'s `TRIFOLD` are derived (412×960 folded, 792×1080 open). Once the user's Speed card screenshots come back, put the real ones in that one table and in opt-measure "The trifold's sizes".
- Re-measure the Line supper when it becomes seated sittings (EV7).
- The known +2 geometries on deck round trips (since 0.64.6) still shows in perf_check. It isn't mine and it isn't new.
- #5's proof rounds all finished green (see its build-table row); the Day 13 day_check failure on the storm build is the storm branch's (identical without #5). The old note follows, for reruns: #5's proof rounds were still running at the push (account move): player_check, check_fast, then `scratchpad/proof5b.sh`'s event-build runs (day_check Days 13, 14, 21 on storm + Fridays + Tern switched on, and the Line's Day 7, each old vs new line by line). If the container is gone, rerun them: the builds are a local merge of claude/opt-render + storm-update + fridays + patch-crew with EVENTS_ON flipped, and claude/line-update with the two-line patch and EVENTS_ON + EV_LINE_ON flipped. Then send #5 to OR1.
- OR1's F1-F4 on perf_check are done (fe0726b); OR1 was reviewing #8 next.

## Open questions for the user
None. The two the user answered today: no visual change from the CPU-drawn textures, and the phone is the Galaxy Z TriFold.
