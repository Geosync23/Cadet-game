# Starship Cadet

A cozy starship-life sim: a single-file three.js game (`starship-cadet.html`) set aboard the CSV Wren.

## Read first, every session
1. `DEV_NOTES.md`: how the build works, the rules, testing, and what's next. Its "Next" section names the current job.
2. `design-doc.md`: what the game is. It's the single source of truth for the design (it replaces the old v4 PDF, now in `archive/`, and the Living Ship addendum), with all open questions in its last section.
3. `plans/deckN-plan.html`: the agreed layout of each deck. A deck is only built from an agreed plan.
4. `TEAM.md`: who's working on what. Several sessions work in parallel under a lead session; stay inside the files your brief names.

## Files
- `starship-cadet.html`: the game (one file; three.js r128 from cdnjs).
- `cadet_test.py`: the regression test (compares two builds; see DEV_NOTES "Testing").
- `deck_check.py`: visits every built deck and checks reachability, crew, draw calls and memory.
- `day_check.py`: fast-forwards one ship day and checks the crew's schedules (sleep, meals, shifts, places, nobody stuck, draw calls).
- `player_check.py`: checks the player's needs, activities, walking speed and saving.
- `plans/`: deck plan pages.

## How we work
- **One deck at a time, then review.** Work through all of a deck's turns, then stop and hand over for review: publish the build as a playable artifact, send screenshots, and summarise what was built, the judgement calls made and the test results. Don't start the next deck until the user signs off.
- **New decks start with a plan page** in the style of `plans/deck3-plan.html`, reviewed before any building.
- **Each turn:** small exact-string edits to the build (never rewrite the whole file), bump the build number in the HUD, add a row to the build table in DEV_NOTES, run the tests, commit and push.
- **Determinism and regressions** (details in DEV_NOTES "Rules that keep it working"): shared kit made at load never calls `R()`; regressions on unchanged decks must be pixel-identical, and when they aren't, find out why before moving on.
- **Phones first:** no coplanar surfaces, every colour through `col()`, watch draw calls.
- Keep `DEV_NOTES.md` current so a fresh session can pick up from it.
- **Update `design-doc.md` when a design decision is made,** in the same commit as the work that depends on it: edit the section it belongs to, and move answered questions out of its Open questions.
- The user is new to Claude Code and git: explain in plain language, no jargon.
