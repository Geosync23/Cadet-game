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
- `events_check.py`: steps a few weeks of ship days and checks the ship traditions: each happens when it's due, people go, Mail the evening before, decor on the deck.
- `food_check.py`: runs the galley over whole ship days and checks food is ready, nobody waits too long, the dish pit clears and the rota holds.
- `machine_check.py`: runs the ship's machines on paper and checks wear, faults, repairs, the jobs left for the player and ship health.
- `clothes_check.py`: checks changing at your wardrobe, yesterday's clothes, the laundry hamper, the washers and saving mid-wash.
- `interactions_check.py`: checks the places you can use, the job board and the goal pointer.
- `bubble_check.py`: speech bubbles at phone size with uneven frames: they follow their speaker without shaking, jumping or swapping sides.
- `plans/`: deck plan pages, pillar plans, and `handover-<role>.md` notes for each role.

## How we work
- **One deck at a time, then review.** Work through all of a deck's turns, then stop and hand over for review: publish the build as a playable artifact, send screenshots, and summarise what was built, the judgement calls made and the test results. Don't start the next deck until the user signs off.
- **New decks start with a plan page** in the style of `plans/deck3-plan.html`, reviewed before any building.
- **Each turn:** small exact-string edits to the build (never rewrite the whole file), bump the build number in the HUD, add a row to the build table in DEV_NOTES, run the tests, commit and push.
- **Determinism and regressions** (details in DEV_NOTES "Rules that keep it working"): shared kit made at load never calls `R()`; regressions on unchanged decks must be pixel-identical, and when they aren't, find out why before moving on.
- **Phones first:** no coplanar surfaces, every colour through `col()`, watch draw calls.
- **Full tests on every change (the user, 2026-10-22).** Every game change runs the full round of checks before it is merged or published, always split across six check runners at once (about 30 minutes; the split and the steps are in plans/testing-guide.md). The test picker in tools/ stays for quick feedback while working, but never replaces the full round.
  - **The six check runners talk to each other** (the user, 2026-10-22). Runners, the build master and the lead message each other directly (session ids in TEAM.md) when:
    1. a runner's game file doesn't match the sha256 the lead sent: tell everyone and stop;
    2. a failure could affect other runners' shares (a broken build, a crash on load, shared setup): tell them;
    3. a runner fixes a setup problem: share the fix;
    4. a runner finishes early: offer to take a check from the slowest runner, agree it between them, copy the lead, and never run a check twice by accident;
    5. any FAIL that isn't on the known-old list (today backlog 12 and 14): tell the build master and the lead at once, without waiting for the end of the share.
  Results go in plans/checks-crN.md; each runner sends its final OK/FAIL to the lead and the build master. The full steps are in plans/testing-guide.md.
- Keep `DEV_NOTES.md` current so a fresh session can pick up from it.
- **Update `design-doc.md` when a design decision is made,** in the same commit as the work that depends on it: edit the section it belongs to, and move answered questions out of its Open questions.
- The user is new to Claude Code and git: explain in plain language, no jargon. No emojis in anything for the user (the user, 2026-10-21).
- **Handover before auto-summarizing (the user's rule).** Memory limit (the user, 2026-10-22): hand over at about **65%** of the context (about 650k of 1,000,000). Before that, decide case by case from the work ahead: if the next task would carry you past 65%, hand over first. Warn early when your memory is getting full, or when the next task looks big enough to fill it: helpers tell the lead, and the lead tells the user in plain words. Don't wait for the automatic summary. Then write a handover note for a fresh session (`plans/handover-<role>.md`: role, branch and builds, what you own and built, shared formats, loose ends, gotchas, how to test, open questions for the user), push it, and stay idle. A fresh session taking over a role reads its predecessor's note first. The lead keeps `TEAM.md` current and writes its own handover brief the same way.
