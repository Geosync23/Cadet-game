# Draft: moving DEV_NOTES' build table into its own file (not applied)

**Why** (SR2's S6, the roadmap): DEV_NOTES.md is 1.42 MB, and the build table is 0.98 MB of it (lines 12-1066 at 0.64.2: the "Current build" heading, a stale paragraph, the table and a note). CLAUDE.md tells every session to read DEV_NOTES first; most of what it reads is old table rows. Moving the table out roughly triples how much of the notes a fresh session can read for the same memory.

## The move (one commit, by the lead or the build master, after the rec deck is published)

1. **New file `plans/build-table.md`:** a short header ("Every build, one row each. Newest rows at the bottom of their range; the build master adds the merge rows, each seat adds its own rows under its work's name."), then the table exactly as it is today, lines 16-1064 cut and pasted with no row changed. A plain cut and paste: `sed -n 16,1064p DEV_NOTES.md >> plans/build-table.md`, then check `grep -c '^| ' ` is the same before and after (rows lost: none).
2. **Two blank lines inside the table** (today lines 990 and 1012) split it into three tables on GitHub, so rows after them show as plain text. In the new file, delete those two blank lines (nothing else).
3. **DEV_NOTES lines 12-1066 become:**
   > ## Builds
   >
   > Every build's row is in `plans/build-table.md` (moved out in step 2, 2026-10-2x, to keep these notes small). The last 20 rows:
   >
   > (the header row, then the 20 newest rows by build number, copied)
   >
   > The game is at build 0.64.x; the build master sets the build number when merging (CLAUDE.md "How we work").

   The stale "Current build: 0.60.7 (about 37,400 lines) / Two decks, joined by a working lift..." paragraph and the 0.5.x screenshot note go to the top of build-table.md (history, not current state).
4. **Also stale at the top of DEV_NOTES** (lines 3-8: "build 0.14.0", "Deck 3 is complete (0.7.0)...", "Decks 6, 1 and 2 are built ... waiting for the user's review"): replace with one line pointing to TEAM.md and the roadmap for the current state. Ask the lead first; it's the lead's file.
5. **Pointers to fix in the same commit:** CLAUDE.md "Each turn" (see `claude-md.md`); `grep -rn "build table" CLAUDE.md DEV_NOTES.md plans/*.md` (25 mentions today) — change only the ones that tell someone where to add a row (CLAUDE.md, DEV_NOTES "Working method", the build masters' and lead's latest handover notes); old handover notes stay as they are (history).
6. **Proof:** `git diff --stat` shows DEV_NOTES.md down by ~0.95 MB and build-table.md up by the same; `diff <(git show HEAD~1:DEV_NOTES.md | sed -n 16,1064p | grep -v '^$') <(grep '^| ' plans/build-table.md | ...)` lists no lost row. No game file change, so no checks needed beyond check_fast for form.

## Afterwards

- **Where rows go:** a helper adds its rows to `plans/build-table.md` under its own work's name with its own sub-number (e.g. "0.64.x-dev3"), since the build master now sets the real build number at merge; the build master adds one merge row with the real number listing what went in. (This removes the second clash spot: today every helper also appends a row at the same place in DEV_NOTES.)
- **Same-spot clashes in build-table.md:** two helpers adding a row at its end still clash (one line each, easy to resolve). If that bites, give each seat its own heading at the end of the file and append under it, like the slots in the game file.
