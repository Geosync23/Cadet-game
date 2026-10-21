# Handover: test-speed engineer (TS1)

- **Role:** make the checks faster. Every check still plays the real, drawn game: no headless or no-drawing runs (the user's decision, 03:00 UTC 2026-10-21).
- **Session:** TS1. Stopped 2026-10-21 ~03:40 UTC on lead 22's word (session_01BGQCZLK6gYTnqu6mwZ61jB): tonight is for the ship-wide events. The work moves to the optimization team, hired after the events are done.
- **Branch:** `claude/test-speed`, from `claude/integration` 675588c (0.64.6). The only change on it is this note. No game or check file was changed.
- **Brief (the user's list):** 3. run only the checks a change affects (**the main job, first deliverable**, the user via lead 22); 4. long runs that pick up where they stopped; 5. split the full round across several sessions; 2. saved-game starting points (**with caution**, see below); reuse one loaded page across checks only if results stay identical; a cadence for the full round, written into DEV_NOTES "Testing".

## What I measured (0.64.6, one browser alone, 4 cores)

| What | Time |
| --- | --- |
| Opening the page (`Game(...)`, until `__sc` is ready) | 11-13 s |
| Reload of the same page | 8 s |
| `skipTo` one ship day under `?nosave` | 0.2 s |
| `step(20)` / `step(30)` on a normal day, drawing switched off as usual | 0.02-0.1 s (the first step after a deck change: 2-5 s, the shaders being built) |
| `step(30)` **after a reload** (Monday 08:40, Deck 5) | **27-29 s** |
| The same `step(30)` with the drawing switch put back after the reload | **0.03-0.12 s** |

intro_check.py, whole run (python3 -u with a timestamp on each line; log of this run in the container only):

| Part | Took |
| --- | --- |
| 0-7 (on paper) | 8 s (most of it the page opening) |
| 8 (the evening in the real game) | ~250 s |
| 9 (a first launch arrives) | ~40 s |
| 11 (reload mid-walk) | **~930 s** (the same walk as part 8 takes ~250 s) |
| 10 (Monday) | still running after 400 s, at the briefing (stopped) |
| 13, 12 | not reached (stopped at ~1650 s) |

## Where the time goes: the biggest find

**After a page reload, every simulated frame is drawn.** `cadet_test.py`'s `Game.__init__` turns drawing off for all but the last frame of each `step()` by replacing `renderer.render` once, when the page first opens. A check that then calls `page.goto(...)` or `page.reload()` gets a new page **without** that switch, so every simulated frame is drawn in software (SwiftShader). A CPU profile of one `step(30)` after the reload: 84% `uniformMatrix4fv`, then other WebGL calls. That's about 1 s a frame on a busy deck, against ~1 ms.

- intro_check parts 9, 11, 10, 13 and **12 (the week, >1.5 h)** all run on the page reloaded in part 9. That alone very likely explains most of intro_check's 2 hours.
- Other checks that reload: join_check (2), devmode_check (2), player_check (2), career_check (1), mech_check (1). career, mech and player open their own page with `page.goto(tmp)` for the save tests: still to check whether they put the switch back.
- **Proposed fix (not made):** in `cadet_test.py`'s `Game`, put the switch back after a reload, e.g. a `Game.ready()` that waits for `__sc` and re-installs it, called by the checks after each `goto` / `reload`; or `step()` re-installs it whenever `window.__skip === undefined`. cadet_test.py is shared by every check: agree it with the lead and the check owners first.
- **Proof needed before it goes in:** the same build, the old way and the new way, with the same printed results line for line (intro_check whole, join, player, career, mech, devmode). Watch for anything that reads `renderer.info` between frames (draw-call budgets read it after the last frame of a step, which is still drawn). Expected saving: intro_check from >2 h to roughly 10-15 min (a guess from parts 8 and 11; measure it).

## The plan, in order (send it to the lead before building; the lead had not yet seen it)

1. **The reload fix above.** The biggest win for the least code. Prove identical results first.
2. **Run only the checks a change affects (step 3, the main job).**
   - `tools/affected.py [A [B]]`: from `tools/section.py --diff`'s sections (and the files changed outside the game: a check file means that check; `content/` means content_gen --check, lines, talk), prints the checks to run. check_fast always runs on top.
   - The map, section to checks, made from **real runs, not guesses:** run each check once with the browser's own coverage on (Chrome DevTools `Profiler.startPreciseCoverage` with call counts, through `page.context.new_cdp_session(page)`). Tried on 0.64.6: it works, costs ~0.1 s to start, and reports which of the game's functions ran (810 of 1206 compiled functions in a short test). Take the coverage once just after loading (that resets the counts), then at the end: the functions the check itself ran. Each function's offset gives a line, so a section (tools/section.py's rule). Keep the map in a file (e.g. `tools/check_map.json`) and regenerate it at every full round, in a separate run from the one whose results count.
   - **A change outside any function** (a table or other top-level code): use `node tools/shared.js`'s list of which sections read that table, then those sections' checks. Changes to the widely read pieces (SHIP, DECKS, shipNow, page/CSS, sections 1-5, 4b-4c, 13, the save) run the full round.
   - Add the DEV_NOTES "Run it whenever ..." rules as a hand-written list on top (the union of both, never less).
   - Check it: replay recent merges from the build table and confirm every check that actually failed on one would have been picked.
3. **Resumable long runs (step 4):** each long check writes one result line per part (`part, build hash, OK/FAIL, seconds`) to a results file as it goes; a rerun on the same build hash (the game file's sha1 plus the check file's) skips the parts already OK. intro_check's parts share one page, so "skip" means starting the next part from a known start (New game, or a reload), not resuming mid-part. Only where a part doesn't depend on the last one's leftovers (see DEV_NOTES "mech_check parts share the game").
4. **Several containers (step 5):** a manifest file on a branch lists the full round's parts (check, arguments, CADET_WORK tag); each runner session takes a slice, runs it on the named commit and pushes `results/<build>/<part>.txt` (the summary line and exit code); the build master gathers them and checks the hashes match. No chained waits: each runner works on its own, so one stuck runner never blocks the others (the old deadlock).
5. **Saved-game starting points (step 2): with caution, only where the saving is large.** After fix 1, measure again first: skipTo is cheap (0.2 s a day under ?nosave), so fixtures may no longer be worth it. If they are: made by the real game, storing the build's GAME_BUILD, the save version and a hash of the sections that plan or save (13, 14, 9 and others), compared on use; a mismatch fails loudly (never quietly falls back). **Never the only way a day is checked:** the full round still plays from Day 0. Note the game loads a save only when the page opens and never under `?nosave`, so using a fixture means a page without ?nosave, or a test-only hook in the game behind a URL flag (only with lead 22's OK).
6. **One page across several checks:** probably not worth it. Opening costs 11-13 s and most checks open one page, so it saves ~5 minutes over a full round, and the checks change a lot of the game's state (SHIP, the jobs, the flags), so results could differ. Lowest priority.
7. **Cadence (step to write into DEV_NOTES "Testing" once agreed):** check_fast on every push (as now); the affected checks on every turn; the full round at every release and at least once a day on `claude/integration`; intro_check `--week` (the long arrival-week check) whenever section 21 or the week's beats, or a planner it uses (14, 18, 20), changes.

## Gotchas

- Run each check in its own `CADET_WORK` (DEV_NOTES "Parallel runs need their own CADET_WORK"). Setup: three.js and acorn in `/tmp/cadet-work` (DEV_NOTES "Testing"), `pip install playwright numpy pillow`, `CADET_CHROME=/opt/pw-browsers/chromium`.
- Measure from a copy of the files (I used `/tmp/tw`) so edits on the branch don't change a run in progress.
- The brief mentions bigevents_check.py (EC1's): it isn't on claude/integration 0.64.6; it lives on the events branch.
- Check files have owners. The build master (BM11, session_01W7NHRM4JjqaNEJQUWNxgcE) runs the releases: coordinate any change to a check with its owner and the build master, and don't break running work.

## Open questions for the user (through the lead)

- Is the reload fix (drawing switched off again after a reload, as before it) within the "every check still runs the real drawn game" rule? Each step's last frame is still drawn, exactly as in every check before the reload.
- Which checks make up "the full round" today: the build master's list (plans/handover-build-master-s2.md) or a newer one?
