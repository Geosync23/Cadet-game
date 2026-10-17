# Review checklist (Pillar 4)

The two adversarial reviewers use this on every branch before it's combined. When the team is scaled down (TEAM.md, "Staffing levels"), each helper runs it on their own push and writes the results in their report to the lead. Each finding needs a concrete path: what state or input, and what goes wrong. No style notes.

## 0. Set up
- `git fetch origin && git diff origin/claude/ship-integration...<commit> -- starship-cadet.html <your tools>`. Read the whole diff, not only the summary.
- Make a scratch merge with the branches you depend on (the sim bus, social A, the roster) and run your checks on that too. Most Pillar 4 bugs only show up once two seats are combined.
- Test setup: DEV_NOTES "Testing" (playwright, three r128 in `/tmp/cadet-work/three`, `CADET_CHROME=/opt/pw-browsers/chromium`). Run one browser check at a time.

## 1. In your seat?
- Every changed line is in a section your seat owns (pillar4-plan Part 6). The build line is the one exception everyone touches.
- Lines in someone else's section are one-line `typeof`-guarded hooks, each with a row in the hook register.
- New hash keys (`schedU(seed, d, k)` keys) are inside your range: social 644-699 (A 644-671, B 672-699), arrival 700-749, lines 750-799, tiles 800-829, crew coming and going 830-849, traditions 434-499. Search the diff for every `schedU(`.

## 2. Crashes and load order
- **`typeof` doesn't guard a `const` or `let` that hasn't been declared yet** (the temporal dead zone). If your code can run while the file is loading, every name it reads must be declared above it, or be a function declaration or a `var`. Watch the generated blocks (LINES, VOICE, TRADITIONS, ROSTER: where in the file do they sit?).
- Every hook into another section is `typeof X === 'function'` guarded and works when that section is missing.
- `find(...)[k]`, `arr[0].x`, `map.get(id).y`: what if nothing matches? Try an id that isn't on the roster, a guest, a crew member who has left.
- Numbers: NaN from `undefined` maths, negative values (reputation dips, Day 0), dividing by zero counts.
- **Day 0:** the arrival Sunday has negative absolute minutes (`(0 - 1) * 1440 + min`). Check `if (!t)`, `t >= 0`, `day >= 1`, `weekday(0)` and anything that floors or mods a day.
- Off-by-one: "within N days", "until" vs "for", inclusive ends, midnight (min 0 and 1440).

## 3. Determinism
- No `Math.random`, `Date.now`, `performance.now` or real-time timers in anything that decides what happens. Picks are `schedU(seed, day or hour, key)`.
- Shared kit made at load never calls `R()`.
- Iteration order: object keys and Map order follow insertion order. Is the insertion order itself fixed? Never sort with a comparator that can return the same value for different items and then depend on the order.
- Plans are pure: `planDay`, `eventPlan`, `introPlan` and lineFor's conditions never change state or send notes. Notes come from play.
- Run your check twice in the same page and in two fresh pages; compare.

## 4. Save and load
- New state is in the save (through `SAVE_EXTRA` or section 13), and read back defensively: wrong type, missing, an old save without it, a save from a different crew list.
- Round-trip through the real `saveGame()` / `loadGame()` with storage on (`?debug`, not `?nosave`), not only your own save/load functions.
- **New game** resets your state too (it's not a page reload). Today section 13's New game handler resets time, decks, habits, needs and social only.
- Nothing in the save holds an object reference: anything with a cycle (walkers, meshes, people from `schedPeople()`) makes `JSON.stringify` throw, and `saveGame` swallows that, so the game silently stops saving.
- The save stays small: rings and caps on everything that grows. `SAVE_V` stays 2 unless the lead says otherwise.

## 5. Phones
- Nothing new runs every frame unless it has to; per-frame work does no allocation (`filter`, `map`, spread, new objects, string building) in loops.
- Draw calls: under 450 at the busiest minute on each deck you touch; tradition decor at most 6 calls, only on its deck, only in its window.
- Every colour through `col()`; no two surfaces sharing a plane; listeners and timers removed when they're done; arrays capped.
- Regressions on decks you didn't change are pixel-identical (`cadet_test.py`). When they aren't, find out why (a flaky shot shows up comparing a build with itself).

## 6. Does the report match the code?
- Each claim in the DEV_NOTES row and the report ("inert", "no game change", "tested reload at every step", "same twice") is backed by a check that actually exercises it. Read the check: does it test the real path, or a stand-in?
- Contracts with other seats: field names, kind strings (`friends` or `friend`?), units (ship minutes, absolute or of the day), who sets and who clears each flag. Write them in the hook register or DEV_NOTES.
- Run every check your seat owns, plus `cadet_test.py`, `deck_check.py` and `day_check.py` if crew, places or schedules change.

## 7. The report
- Verdict: PASS / PASS WITH FIXES / BLOCK. Findings most severe first, each with the path, the evidence (the command or the check output) and a suggested fix.
- Reviewers write the note to `plans/reviews/<branch>-<commit>.md` on `claude/reviews` and send it to the lead and the helper.
