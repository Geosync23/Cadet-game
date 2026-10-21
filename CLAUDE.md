# Starship Cadet

A cozy starship-life sim: a single-file three.js game (`starship-cadet.html`) set aboard the CSV Wren.

## Read first, every session
1. `DEV_NOTES.md`: how the build works, the rules, testing, and what's next. Its "Next" section names the current job.
2. `design-doc.md`: what the game is. It's the single source of truth for the design (it replaces the old v4 PDF, now in `archive/`, and the Living Ship addendum), with all open questions in its last section.
3. `plans/deckN-plan.html`: the agreed layout of each deck. A deck is only built from an agreed plan.
4. `TEAM.md`: who's working on what. Several sessions work in parallel under a lead session; stay inside the files your brief names.
5. `plans/map.md` (where things live, by section) and `plans/owners.md` (who owns which section, and the shared functions and tables). `python3 tools/section.py --where LINE` turns any line number into its section.

## Files
- `starship-cadet.html`: the game (one file; three.js r128 from cdnjs).
- `cadet_test.py`: the regression test (compares two builds; see DEV_NOTES "Testing").
- `deck_check.py`: visits every built deck and checks reachability, crew, draw calls and memory.
- `day_check.py`: fast-forwards one ship day and checks the crew's schedules (sleep, meals, shifts, places, nobody stuck, draw calls).
- `player_check.py`: checks the player's needs, activities, walking speed and saving.
- `events_check.py`: steps a few weeks of ship days and checks the ship traditions: each happens when it's due, people go, Mail the evening before, decor on the deck.
- `bigevents_check.py`: the ship-wide events on paper with the events base switched on (in a copy): each event on its calendar day, phases at their minutes, the Friday hold, the career-beat guard, casts, gatherings' places, room clashes, a self-test with planted clashes, and late saves; and nothing with it off. Not in check_fast (EC1 owns it).
- `food_check.py`: runs the galley over whole ship days and checks food is ready, nobody waits too long, the dish pit clears and the rota holds.
- `machine_check.py`: runs the ship's machines on paper and checks wear, faults, repairs, the jobs left for the player and ship health.
- `clothes_check.py`: checks changing at your wardrobe, yesterday's clothes, the laundry hamper, the washers and saving mid-wash.
- `interactions_check.py`: checks the places you can use, the job board and the goal pointer.
- `bubble_check.py`: speech bubbles at phone size with uneven frames: they follow their speaker without shaking, jumping or swapping sides.
- `devmode_check.py`: checks Dev mode (section 25, `#dev`): nothing without the Dev link, the real save untouched, Undo, Mark, the Dev clock, Take me to.
- `names_check.js`: reads the game's script the way the browser does: it must parse; no top-level name, shared-table key or registration (`deviceApp({ id })` and the like) made twice; no "Deck 7" on screen. Names the section and line of each problem.
- `check_fast.sh`: the quick check (about 5 minutes): words baked, names_check, then the deck, machine and leave checks side by side with the device check. Run it before every push. GitHub runs the same by itself on every push that touches the game, the checks or the words (`.github/workflows/quick-check.yml`): a tick or a cross on the commit, in about 5 minutes.
- `tools/section.py`: print a section, name the section of a line, list the sections (and owners) a change touches. `tools/shared.js`: which functions and tables are used outside their own section.
- `archive/starship-cadet-0.64.2-whole.html`: the whole game as published with the rec deck (0.64.2), kept unchanged.
- `plans/`: deck plan pages, pillar plans, `handover-<role>.md` notes for each role, `owners.md`, `map.md`, `backlog.md` (small known bugs) and `build-table.md` (every build's row).

## How we work
- **One deck at a time, then review.** Work through all of a deck's turns, then stop and hand over for review: publish the build as a playable artifact, send screenshots, and summarise what was built, the judgement calls made and the test results. Don't start the next deck until the user signs off.
- **New decks start with a plan page** in the style of `plans/deck3-plan.html`, reviewed before any building.
- **Each turn:** small exact-string edits to the build (never rewrite the whole file), add new code in your seat's labelled slot (`// ---- slot: <seat> ...`), add a row to the build table (`plans/build-table.md`) under your work's name, run your area's checks and then `bash check_fast.sh`, commit and push. **Never push when check_fast says FAILED.**
- **The build number is the build master's.** Helpers don't change the two build-number lines (the header's `build` line and `GAME_BUILD`); the build master sets them when merging into the shared branch. (Nearly 8 in 10 past merge clashes were only those two lines.)
- **Merge early, into one shared branch.** Each reviewed piece of work is merged by the build master into `claude/integration` straight away, with check_fast. Helpers start from it and bring it into their own branch often (at least at the start of each turn), so nobody drifts days apart and a clash shows up while it's small.
- **Owners** (`plans/owners.md`, the user's rule): small edits in another seat's section are fine, and the owner reviews them before they're merged. A change to a shared function's inputs or result, or to a shared table's shape, goes to its owner first. `python3 tools/section.py --diff` shows which sections (and owners) your branch touches.
- **Found a small bug outside your brief?** Add a row to `plans/backlog.md`; don't fix it on the side.
- **Every page published for the user leaves room for the user's answer** (the user's rule). A plan page, survey or results page has a place to comment and to answer its questions on the page itself (load the `artifact-capabilities` skill for a page that keeps what the user writes), so nothing the user says there is lost.
- **Cut things are parked, never deleted** (the user's rule). When something is cut from scope, mark it cut and keep it on record: in design-doc.md (its section, marked cut, with the date and the user's reason) and in the plan that held it (`plans/`). Its keys, ids and names stay retired, not reused. Code already built for it stays switched off; taking it out of the file is its own reviewed step, with the record kept.
- **Determinism and regressions** (details in DEV_NOTES "Rules that keep it working"): shared kit made at load never calls `R()`; the crew's planner never reads records built while the game runs; new features stay switched off (identical game) until they're switched on; regressions on unchanged decks must be pixel-identical, and when they aren't, find out why before moving on.
- **Phones first:** no coplanar surfaces, every colour through `col()`, watch draw calls.
- Keep `DEV_NOTES.md` current so a fresh session can pick up from it.
- **Update `design-doc.md` when a design decision is made,** in the same commit as the work that depends on it: edit the section it belongs to, and move answered questions out of its Open questions.
- The user is new to Claude Code and git: explain in plain language, no jargon.
- **Handover before auto-summarizing (the user's rule).** Warn early when your memory is getting full, or when the next task looks big enough to fill it: helpers tell the lead, and the lead tells the user in plain words. Don't wait for the automatic summary. Then write a handover note for a fresh session (`plans/handover-<role>.md`: role, branch and builds, what you own and built, shared formats, loose ends, gotchas, how to test, open questions for the user), push it, and stay idle. A fresh session taking over a role reads its predecessor's note first. The lead keeps `TEAM.md` current and writes its own handover brief the same way.
