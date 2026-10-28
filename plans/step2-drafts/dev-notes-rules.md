# Draft: DEV_NOTES additions for step 2 (not applied)

## 1. "Rules that keep it working": add a new group after "Determinism"

> Shared work (step 2, from the roadmap's lessons of 2026-10-19):
>
> - **The crew's planner never reads records built while the game runs.** A day's plan must come out the same whenever it's made, so it may read only what is fixed for that day (the roster, the day number, seeded rolls, records settled at a known hour, like the rec deck's at 22:00 the evening before). Never `MACH_HIST`, a machine's live state, who's on the deck now or anything else filled in as you play. (The MACH_HIST bug: a plan's fallback read the live history, so the same day planned at two moments differed; machine_check and day_check disagreed between runs. Fixed in 0.64.1 by `recPlanShut` / `recSettled`.)
> - **Checks never assume an empty deck or a free time slot.** Before a check places the player, books a seat or starts an event at a time, it looks for a free one (or clears it) and says which it used. A new tradition, a new place or a crew change must not break an unrelated check. (Two check fixes on 2026-10-19 were checks that assumed a slot nobody used; and interactions_check's floor tap that hit a crew member.)
> - **New features are gated until they're switched on.** A new feature sits behind one named switch (like `REC_DECK`), and with the switch off the game is identical: cadet_test ALL IDENTICAL against the build before it, the same days in day_check. Texts that only make sense with the feature on (like "Seven decks") are gated too. Switching it on is its own reviewed step.
> - **One owner per function and table** (`plans/owners.md`). No new top-level name that already exists anywhere in the file (names_check fails it); add to a shared table only through its owner's registry or slot.
> - **New code goes in your seat's labelled slot** (between `// ---- slot: <seat> (section N) ... ----` and `// ---- end of slot: <seat> ----`; new lines go just above the end line; the list is in `plans/map.md`), not at the end of a neighbour's section, so two seats never add lines at the same spot.

## 2. "Testing": add at the top

> **The quick check before every push** (step 2): `bash check_fast.sh` (about 5 minutes on 4 cores; `CADET_WORK` must hold `three/` and `acorn/`: `cd $CADET_WORK && mkdir -p acorn && cd acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz`). It runs, in order, stopping early if a fast step fails: `content_gen.py --check` (the words are baked), `node names_check.js` (the script parses as the browser reads it; no name, shared-table key or registration made twice, gated blocks included; no "Deck 7" in text), then two lanes side by side, each in its own CADET_WORK: deck_check, machine_check, leave_check | device_check. A step passes only if it exits 0 **and** prints its OK line. Prints `QUICK CHECK OK in N s` or `QUICK CHECK FAILED` with the failing lines and the log path. The full checks below are unchanged and still run before every release.
>
> **Every check exits 1 when it fails** (step 2): deck, machine, day, food, path, perf, disc, arc, social and cadet_test used to print FAILED and exit 0, so a script or GitHub saw a pass. Their printed lines are unchanged.
>
> **names_check.js** (step 2, from the split rehearsal): `node names_check.js [GAME.html]`, 1 second. On a FAIL it names the section and game line of both copies. Repeats that are meant are listed in its `MEANT` set with the reason (section 19's 'crew' app shell, replaced by section 20's; `SHIP.tiles` reloaded from the save); a table key declared `null` and filled once later by its owner is allowed.
>
> **Finding your way:** `python3 tools/section.py` (list), `tools/section.py 19` (print a section), `--where LINE`, `--diff A B` (sections and owners a change touches); `node tools/shared.js` (functions and tables used outside their section; `--md` makes the list in `plans/owners.md`).

## 3. "File map": replace with a pointer

> The sections, where each thing lives and who owns it: `plans/map.md` and `plans/owners.md`; `python3 tools/section.py` lists the sections with today's lines.

(The current "File map" lists only 1-12, 17, 18, 22, 20 and the 13-15 group; map.md covers all 56.)
