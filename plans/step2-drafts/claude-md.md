# Draft: CLAUDE.md changes for step 2 (not applied)

Apply with exact-string edits once the rec deck is published. Everything not listed stays as it is.

## 1. "Read first, every session": add a 5th item

> 5. `plans/map.md` (where things live, by section) and `plans/owners.md` (who owns which section, and the shared functions and tables). `python3 tools/section.py --where LINE` turns any line number into its section.

## 2. "Files": add after the `bubble_check.py` line

> - `names_check.js`: reads the game's script the way the browser does: it must parse; no top-level name, shared-table key or registration (`deviceApp({ id })` and the like) made twice; no "Deck 7" on screen. Names the section and line of each problem.
> - `check_fast.sh`: the quick check (about 5 minutes): words baked, names_check, then deck, machine and leave checks side by side with the device check. Run it before every push. GitHub runs the same (`.github/workflows/quick-check.yml`) once the lead switches it on.
> - `tools/section.py`: print a section, name the section of a line, list the sections (and owners) a change touches. `tools/shared.js`: which functions and tables are used outside their own section.

## 3. "How we work": replace the "Each turn" line

Before:

> - **Each turn:** small exact-string edits to the build (never rewrite the whole file), bump the build number in the HUD, add a row to the build table in DEV_NOTES, run the tests, commit and push.

After:

> - **Each turn:** small exact-string edits to the build (never rewrite the whole file), add new code in your seat's labelled slot, add a row to the build table (`plans/build-table.md`) under your work's name, run your area's checks and then `bash check_fast.sh`, commit and push. **Never push when check_fast says FAILED.**
> - **The build number is the build master's.** Helpers don't change the two build-number lines (the header's `build` line and `GAME_BUILD`); the build master sets them when merging into the shared branch. (Nearly 8 in 10 past merge clashes were only those two lines.)
> - **Merge early, into one shared branch.** Each reviewed piece of work is merged by the build master into `claude/integration` straight away, with check_fast. Helpers start from it and bring it into their own branch often (at least at the start of each turn), so nobody drifts days apart and a clash shows up while it's small.
> - **Owners** (`plans/owners.md`, the user's rule): small edits in another seat's section are fine, and the owner reviews them before they're merged. A change to a shared function's inputs or result, or to a shared table's shape, goes to its owner first. `python3 tools/section.py --diff` shows which sections (and owners) your branch touches.
> - **Found a small bug outside your brief?** Add a row to `plans/backlog.md`; don't fix it on the side.

## 3b. "How we work": add two of the user's rules (lead 20, 2026-10-20)

> - **Every page published for the user leaves room for the user's answer.** A plan page, survey or results page has a place to comment and to answer its questions on the page itself (load the `artifact-capabilities` skill for a page that keeps what the user writes), so nothing the user says there is lost.
> - **Cut things are parked, never deleted.** When something is cut from scope, mark it cut and keep it on record: in design-doc.md (its section, marked cut, with the date and the user's reason) and in the plan that held it (`plans/`). Its keys, ids and names stay retired, not reused. Code already built for it stays switched off; taking it out of the file is its own reviewed step, with the record kept.

## 4. "Determinism and regressions": extend

Before:

> - **Determinism and regressions** (details in DEV_NOTES "Rules that keep it working"): shared kit made at load never calls `R()`; regressions on unchanged decks must be pixel-identical, and when they aren't, find out why before moving on.

After:

> - **Determinism and regressions** (details in DEV_NOTES "Rules that keep it working"): shared kit made at load never calls `R()`; the crew's planner never reads records built while the game runs; new features stay switched off (identical game) until they're switched on; regressions on unchanged decks must be pixel-identical, and when they aren't, find out why before moving on.

## Notes for whoever applies it

- "One deck at a time, then review" and the plan-page rule stay: the user's review rhythm is unchanged (roadmap: "Keep the user's review rhythm").
- If the lead keeps the GitHub check on the shared branch only (option A in the workflow file), add to the "Merge early" line: "the build master reads the GitHub check's result for the exact commit before merging on".
