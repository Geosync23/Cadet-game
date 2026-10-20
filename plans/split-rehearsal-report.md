# Split rehearsal: report

Split rehearsal engineer SX1 (session_01Ppc31k1KyVmB5tBQKkJTAh), for lead 20, 2026-10-20. Branch `claude/split-rehearsal`, a throwaway branch that is never merged. It holds a real cut of 0.64.2 (rec-cand-s1 1eeb99c, sha256 e4897023…27624), the real tools, and the test tools in `plans/split-rehearsal/`.

## For the user, in plain words

**What I did.** The plan was tested for real on a copy of the game, not just read through:
- I built the real scripts and cut the game into its 40 pieces.
- I replayed real past combines from the project's history the new way, and compared the results letter by letter with what was actually combined then.
- I tried 20 ways of getting it wrong, each for real.
- I ran the GitHub check on GitHub itself: green, then broken on purpose, then green again.
- I ran the usual game checks on the glued game.

**Is the split safe?** With the scripts as I rebuilt them, yes:
- **No work was lost anywhere.** That covers every replayed merge (13 real merges, 10 of them done two ways), 390 more real merges checked automatically, and every planned mistake.
- **The glued game is the same game.** It is the 0.64.2 file letter for letter, and every check passes on it.
- **The GitHub check works.** It went green in about 5 minutes. On a broken piece it went red in about 30 seconds and named the piece and line.

**Did the scripts need fixing?** Yes, more than once:
- The first version of the "glue or cut" script would have quietly thrown away 762 lines of a writer's real work in one replayed combine.
- The second reviewer (SR2) found two more holes in the plan's rule.
- The version on this branch handles every one of those cases, and I tested each of them.

So the split *can* be made safe. But the safety lives in about 200 lines of careful script that everyone depends on, and that script is the newest and least proven part of the set-up.

**Does the split make combining easier?** No. This is the main finding:
- Across 689 real merges, git clashed in the same places whether the game was in pieces or in one file.
- **77% of the merges that clashed did so only because of the build number.** Every helper changes the same two build-number lines every turn. The rule you've already chosen (the build master sets the build number when merging) removes those clashes, with or without the split.
- Of the clashes left after that, about half were two helpers changing the same code. Nothing mechanical prevents those.
- The other half were two helpers adding new code at the same spot. Labelled "slots" in the one file (SR2's option d) prevent those. The split only prevents them if the pieces are cut much finer than planned.

**Does the split stop name clashes?** No. Yesterday's clash (`REC_SHOW`) can't be seen on either helper's branch alone, split or not. It shows up the moment the two are combined, and the new name check catches it then, including the silent kind that today's checks miss. What makes it show up *early* is combining early and the name check, not the split.

**My honest view: don't split now.** Do the other changes first:
- the build master sets the build number;
- the quick check before every push, and the GitHub check;
- the improved name check;
- the fixed check exit codes;
- early combining;
- labelled per-seat slots.

All of these tools are built and tested on this branch, and they work on the one-file game as it is today. Keep the split's scripts on the shelf. They're proven, and the cut takes minutes if Dev mode shows it's needed. The split's real benefit is smaller files for sessions to read and edit, and that's worth something. But it isn't what has caused our lost work or our long combines, and it adds a second copy of the game that has to be kept in step forever.

**One thing to know about the GitHub check:** every red run emails you, as the owner of the repository. That's 3 so far from these tests, and I kept them to the minimum. With many helpers pushing, that could be a lot of mail. Before it's switched on for real, decide where those emails go. You can turn them off in GitHub's notification settings, or the check can run only on the shared branch.

## 1. What was tested

| # | Test | How |
|---|---|---|
| 1 | Cut and glue, byte for byte | The real `split.py` / `build.py` on 0.64.2 |
| 2 | Replaying real history | `plans/split-rehearsal/replay.py` rewrites the real commits as if the split had happened earlier (each commit gets its pieces). It redoes the real merges the new way, then compares with the real combined file. |
| 3 | Every real merge since 09-01 | `plans/split-rehearsal/sweep.py`: 689 merges. For each, does git merge the pieces the way it merges the whole file? |
| 4 | What the remaining clashes were | `plans/split-rehearsal/clash_kinds.py` (SR2's option d question) |
| 5 | 20 ways to get it wrong | `plans/split-rehearsal/scenarios.py`: each in its own scratch git repository, for real |
| 6 | The GitHub check | `.github/workflows/split-rehearsal.yml`, this branch only (removed at the end) |
| 7 | The game is the same game | cadet_test against the one-file 0.64.2, then deck, machine, events, day 0-2 and interactions on the glued file |

## 2. The tools as built (and what changed from the sketches)

All are on this branch, at the top level.

### `split.py`
- Cuts by section heading, like SR1's sketch.
- The list of pieces, their order and their headings now live in one file, `pieces/ORDER`. Adding, renaming or moving a piece means editing that one file; the script itself never changes.
- **Found while building it:** markers that end in a space (`// 4c. `) were stripped by the editor on save. They are written as `\s` now, because that is exactly the kind of invisible change that would break a cut months later.

### `build.py`, rebuilt three times
The plan's rule ("after an edit glue; after a merge cut; both changed: stop") failed in three ways in testing (SR1's B1, SR2's B1 and B2). The version here does one thing every time: it finds the last commit where the game file and the pieces agreed (looking back past any out-of-step commits, not just at HEAD). Then it compares both sides with that point:
- **only the pieces changed:** glue;
- **only the game file changed:** cut (a branch from before the split, a hand edit, an old tool);
- **both changed:** combine the two with git's own three-way merge, then cut. If they clash, it stops and changes nothing.
- **the game file has git's clash markers** (`<<<<<<<`):
  - if the other side of the merge is from after the split and in step, glue: the clash is the pieces' clash, already fixed there;
  - if the other side is from before the split, stop and say "fix the clash in the game file (the one time to edit it), then run build.py again", which then cuts.
- **a piece lost its final new line:** it is put back.
- **the order of the pieces changed:** a loud warning, because order is part of the game.

`build.py --check` fails, naming the pieces, when:
- the game file and the pieces differ;
- a piece has no final new line;
- a piece has clash markers;
- a file in `pieces/` isn't listed in ORDER;
- **the game file would not cut back into the same pieces** (new: this catches a renamed or copied section heading at once, not at the next merge).

### `names_check.js` (acorn), extended past SR1's sketch with SR2's S3

What it reads:
- It parses the game as a browser does, and also each piece on its own.
- It reports every problem by **piece and line**, or, on the one-file game, by **section and line** (from the file's own `// 19. DEVICE` headings).

What it flags (each tested by planting it; all caught, section 4):
- names made twice;
- keys added twice to a shared table (`const T = {…}`, `Object.assign(T, {…})`, `T.key = …`, also inside `if (REC_DECK) {…}`);
- registrations made twice by id (`deviceApp({ id })`, `X.push({ id })`, `worksTabAdd`…);
- "Deck 7" in a string.

What it allows:
- two repeats that are meant, each listed with its reason (section 19's 'crew' app shell replaced by section 20's; `SHIP.tiles` reloaded from the save);
- a table entry declared `null` and filled once by its owner (`PAUSE.tiles`).

On 0.64.2: 3,807 names, 2,838 table keys, 50 registrations, no problems, 1.3 s.

### `check_fast.sh`
- Waits on each lane by name (SR2 S5).
- A step passes only if it exits 0 **and** prints its OK line.
- Each lane has its own CADET_WORK.
- It stops after the fast steps if they fail, so a broken piece goes red in seconds.
- It runs on the one-file game too (it skips the pieces step).

### The checks
- Every check that exited 0 on failure now exits 1 (SR1's B2, SR2's N1): deck, machine, day, food, path, perf, cadet_test, disc, arc, social.
- `cadet_test.py` (which every browser check loads) now refuses to test the repository's game file when it is behind its pieces (SR2 B3).

### The two generators
- `content_gen.py` now writes the words piece, and refuses to write the game file.
- `plans/crew-roster-gen.py` writes the crew data piece.

## 3. Results

### 3.1 The cut
`split.py` on 0.64.2 gives 40 pieces. Gluing them back gives sha256 e4897023…27624, **identical**. The pieces match SR1's sketch file for file. `build.py --check` takes 0.1 s, the cut 0.35 s.

### 3.2 Replaying real history

The new way, compared letter for letter with the real combined file:

| Replay | Split made at | Merges | Clashes, whole file / pieces | build.py said | Identical to the real result |
|---|---|---|---|---|---|
| **0.64.0** (BM8: be3d7ee + f319ab3, 9dfe971, a095799, 87e3c5f) | 0.63.4 (aa4f42c); 52 commits rewritten | 4 | 2/2, 5/5, 0/0, 3/3 | GLUED ×3, in step ×1 | **4 of 4** |
| 0.64.0, **every seat's branch from before the split** | 0.63.5 (be3d7ee), the moment before the combine | 4 | 2, 5, 0, 3 (game file only) | STOPPED → fix in the game file → CUT ×3; **CUT** ×1 (see below) | **4 of 4** |
| **0.63.3** (6 seats: 8a72e61 … 8944a43) | 0.63.2r (898d58d) | 6 | 2/2, 2/2, 2/2, 3/3, 2/2, 2/2 | GLUED ×6 | **6 of 6** |
| 0.63.3, every seat pre-split | 29b661a | 6 | the same, in the game file only | STOPPED → fix → CUT ×6 | **6 of 6** |
| **0.63.5** (crew-pt1, a real branch from before 0.63.4, merged after it) | 0.63.4 | 3 | 2, 2, 0 | STOPPED → fix → CUT ×2, in step ×1 | **3 of 3** |

The pre-split rows use the real clash fixes from history, made in the game file as build.py asks.

- **The silent case, in real data.** In the pre-split 0.64.0 replay, W3's writer branch a095799 merged with no clash and no message, and git saved the merge by itself. That is exactly the review's blocker. build.py saw that only the game file had changed since the last agreed point and cut it into 10 pieces. **A plain "glue again" (the plan's first rule) would have silently thrown away 762 added and 30 changed lines of W3's work.**
- **Where the clashes were.** 18 of the 23 clashes across these combines were the two build-number lines (`s01` header and `s13` GAME_BUILD).
  - 0.64.0's real clashes: 2 blocks added at the same spot (REC_MACHINES / REC_CREW_PLACES; the -svc push / the gathers), plus 2 changes to the same function (recTap's court lines; the climbing wall).
  - 0.63.3's real clashes: 1 in section 17, plus 2 lines added next to the build line.
- **Pieces vs whole file.** The pieces clashed in exactly the same places as the whole file, every time. The split didn't remove a single clash; it only said which piece each was in.

### 3.3 Every real merge since 09-01 (`sweep.py`)

- **Scope:** 689 merges in the whole repository. 518 changed the game on both sides.
- **As they were:**
  - 508 clashed, whether in pieces or as one file;
  - **393 of those 508 (77%) clashed only in the two build-number pieces;**
  - only 10 were clean, and in all 10 the glued pieces were byte-identical to git's whole-file merge.
- **With the build number taken out** (both sides given the base's build lines, as the "build master sets it" rule would):
  - **390 merges were clean, and in all 390 the glued pieces were byte-identical to git's whole-file merge.** This is the strongest evidence that the split doesn't change what git does.
  - 116 still clashed both ways.
  - 6 clashed one way only. Three of them clashed only in the generated words block, where the fix is "re-run content_gen" either way. The other three were older merges where a section didn't exist yet, so its code sat inside its neighbour's piece.
  - 10 had different clash counts. All of them are from before every section existed, again a neighbour's piece holding a new section.
  - Lesson: **a new section must come with its own piece** (SR2's S4 says the same).

### 3.4 What the remaining clashes were (SR2's option d, `clash_kinds.py`)

With the build number out of the way: 119 merges still clashed, with 606 clashes between them.

| Kind | Clashes | What prevents it |
|---|---|---|
| Both sides changed the same existing code | 316 (52%) | Nothing mechanical: an owner, talking, early combining |
| Both sides only added new lines at the same spot | 260 (43%) | Labelled per-seat slots (option d); the split only if the two additions land in different pieces |
| In the generated words block | 30 (5%) | Re-run content_gen |

- 18 of the 119 merges had nothing but same-spot additions: slots would have made them clean.
- I couldn't literally replay history "with slots", because the helpers would have written their code in different places. This count is the honest upper bound of what slots (or a finer split) can save.
- Many of the 260 are the same work arriving twice by different routes, because branches merged each other a lot.

### 3.5 The real name clash of 10-19 (REC_SHOW)

**Timeline:**
- rec-works added `const REC_SHOW` and `function recShowTick` at 10:13 (0ab43cd).
- rec-crew added `let REC_SHOW` and `function recShowTick` at 10:15 (4c97122).
- Reviewer R7 found the clash; it was renamed at 12:14 (9dfe971).

**What names_check says:**
- **On each branch alone: OK.** No scan of one branch can see it, split or not.
- **On the two combined:** "FAIL … Identifier 'REC_SHOW' has already been declared".
- With only `REC_SHOW` renamed, the silent half remains, and names_check says "FAIL name recShowTick made twice: section 18 (SHIP EVENTS), game line 34231 and section 8c (REC DECK MOVES …)". `node --check` accepts that file.

**So would it have been caught early?** Yes, if the two had been combined early: when the second was merged into the shared branch, or when either helper brought the shared branch in and ran the quick check. The scan catches it the moment it's combined; early combining decides when that moment is. The split plays no part.

### 3.6 Twenty ways to get it wrong (`scenarios.py`; each a real git repository)

| Scenario | What the tools said | Work lost? | Would a check go red? |
|---|---|---|---|
| A branch from before the split, merged after it (clean, silent) | `--check` red; build.py: CUT | No (a plain glue would have lost it) | Yes |
| The same, with a clash | build.py STOPPED: fix the game file, run again; then CUT | No | Yes |
| Two seats, same piece, different lines | Clean; in step | No | No need |
| Two seats, same line | The piece **and** the game file clash; fix the piece; build.py: GLUED | No | Until fixed |
| Two seats at a piece boundary (SR2 B1) | Pieces clean, the game file clashes; build.py: GLUED | No | Until fixed |
| A hand edit to the game file, committed | `--check` red; build.py: CUT into the right piece | No | Yes |
| A hand edit **and** a piece edit, committed out of step, then merged into the shared branch as is | build.py: COMBINED (both kept) | No | Yes |
| A hand edit and a piece edit of the same line, differently | build.py STOPPED, nothing written | No | Yes |
| A committed hand edit, then a later piece edit and glue (SR2 B2) | build.py looks back past the out-of-step commit: COMBINED | No | Yes |
| A forgotten glue, then merged as is | `--check` red (names the piece); build.py on the shared branch: GLUED | No | Yes |
| A single check run on a game file behind its pieces (SR2 B3) | "STOPPED: … this would test old code. Run python3 build.py first." | No | Yes |
| A piece without its final new line | `--check` red; build.py puts it back | No | Yes |
| A renamed section heading | `--check` red at once ("would not cut back into this piece") | No | Yes |
| Two pieces swapped in ORDER | build.py warns; the fast steps stay green; the game fails to start ("Cannot access 'DEVICE_APPS' before initialization"), so deck_check in the quick check goes red | No | Yes (browser lane) |
| A writer changes the words | content_gen writes the piece and refuses the game file; build.py glues | No | If content_gen is forgotten: yes |
| An old content_gen writes the game file | `--check` red; build.py: CUT into the words piece | No | Yes |
| A clash fixed by hand in the game file, differently from the piece | build.py: CUT (the game file's fix wins; both kept here) | No | Until run |
| Reverts (a commit after the split; a merge; a commit from before the split) | In step / in step / `--check` red then CUT | No | Yes |
| Two seats each add a new piece at the same place in ORDER | ORDER and the game file clash; keep both lines; GLUED | No | Until fixed |
| **Going back to the one-file way** while a branch has an unglued piece edit | **That edit is lost** (only the glued file survives) | **Yes** | No |
| Planted name problems (SR2 S3): a second function, deviceApp id, `T.key =`, key inside `if (REC_DECK)`, `.push` id, repeated `let`, "Deck 7" | All 7 caught, each with its piece and line | n/a | Yes |
| A failing lane / a check that prints FAILED but exits 0 (SR2 S5) | QUICK CHECK FAILED / step FAILED | n/a | Yes |

**The one way to lose work.** Going back to the one-file way while some branch still has a piece edit that was never glued. **Rule if it ever comes to that:** before going back, every open branch must pass `build.py --check`.

### 3.7 The GitHub check, for real (this branch only)

| Run | Push | Result | Time |
|---|---|---|---|
| 1 | Workflow added | **Failed with no job and no log.** `${{ }}` inside a `{ }` YAML mapping is not valid. Lesson: a broken workflow file shows only a red cross. Validate it before pushing (`python3 -c "import yaml…"`). | 0 s |
| 2 | Fixed | **Green** | 5 min 15 s (setup 40 s; check 263 s: deck 176, machine 65, device 249 alongside, leave 20) |
| 3 | SR2 fixes | **Green** | 5 min 4 s (cached setup 24 s; check 4 min 34 s) |
| 4 | A missing bracket in `s19-device.js` | **Red**: "the game's script does not parse: Unexpected token at js/s19-device.js line 140 (game line 10914)" | 34 s from push to red |
| 5 | A duplicate `function recShowTick` in the events piece | **Red**: "FAIL name recShowTick made twice: js/s18-events.js line 2198 (game line 35903) and js/s08c-rec-moves.js line 455 (game line 49230)" | 32 s |
| 6 | Fixed and glued (the game is 0.64.2's again, byte for byte) | **Green** | 5 min 5 s (check 4 min 30 s) |

**Each red run emailed the user**, who noticed runs 1, 4 and 5. In real use, every red push by any helper would email the repository's owner. **Decide before switching it on:**
- the user turns off "Actions" emails in their GitHub notification settings; or
- the check runs only on the shared branch, as SR2 suggests the build master reads the result there anyway.

The workflow file was removed from this branch at the end (lead 20's ask).

### 3.8 The same game

On the glued file (byte-identical to 0.64.2), each in its own CADET_WORK, at most 3 at once:

| Check | Result |
|---|---|
| cadet_test vs the one-file 0.64.2 | **ALL IDENTICAL** |
| deck_check | **OK** (183 s) |
| machine_check | **OK** (50 s) |
| events_check | **OK** (375 s) |
| day_check, day 0 | **OK** (386 s) |
| day_check, day 1 | **OK** (369 s) |
| day_check, day 2 | **OK** (368 s) |
| interactions_check | **OK** (357 s) |

All passed. Local check_fast with the whole test set running alongside: **OK in 308 s**. On GitHub the quick check took 263 s, 274 s and 270 s: inside 5 minutes, with about half a minute to spare.

## 4. Honest view: split, or the same safety without it?

**The evidence against splitting now:**
1. **It doesn't change what git does.**
   - 390 of 390 clean real merges glue to exactly git's whole-file result.
   - In every replayed combine, the pieces clashed in exactly the same places as the whole file.
   - Combining effort is unchanged.
2. **The biggest source of clashes is the build number (77% of clashed merges).** Your decision already fixes it, without the split.
3. **Name clashes are found by the name check plus early combining.** 10-19's clash is invisible on either branch alone, in pieces or not.
4. **The split brings its own risks, and keeping them safe took real work:**
   - the plan's first glue rule lost real work (762 lines in replay);
   - its second version had two more holes (SR2);
   - order changes break the game;
   - going back can lose unglued edits;
   - every helper and every brief must learn "edit pieces, run build.py", against 60+ notes that say "edit starship-cadet.html".

   The tools here handle all of that, and I tested them, but they're about 200 lines of the most delicate code in the set-up, written today.

**The evidence for splitting:**
- Smaller files for sessions to read and to edit uniquely (s19-device is 1,000 lines against 49,800).
- A clash or error is reported by piece.
- Ownership is visible in the file list.

Most of that can be had without the cut: names_check already names the section on the one-file game, and SR2's section.py does the rest.

**The same safety without splitting: yes, almost all of it.** Every check-side tool here runs on the one-file game today:
- names_check, by section and line;
- check_fast, which skips the pieces step;
- the fixed exit codes;
- the GitHub check.

Together with the build master setting the build number, early combining and labelled per-seat slots for new code (option d), they cover:
- the build-number clashes (77% of the clashed merges);
- up to 43% of the clashes that are left (same-spot additions);
- every name clash we've had.

**Recommendation: option (d) now, the split on the shelf.**
- Move this branch's tools over without `pieces/`, `split.py` and `build.py`:
  - names_check.js;
  - check_fast.sh;
  - the exit-code fixes;
  - the GitHub check, after the email question.
- Count clashes during Dev mode.
- If big-file editing or same-spot clashes still hurt, cut. It takes minutes with these tools, which are proven, including the conditions under 4.1 below.

### 4.1 If the split goes ahead anyway: what must come with it
1. This branch's `build.py` (not the plan's rule), `--check` with the cut-back test, and the cadet_test guard.
2. A new section gets its own piece and ORDER line.
3. Before any going-back: every open branch passes `build.py --check`.
4. `resolve.py` and `fixrate.py` are retired, or pointed at the pieces (SR1 N4).
5. The GitHub check's email question settled; the build master reads the result for the exact commit before merging (SR2 S1).
6. A pre-split branch is merged as usual. If build.py stops, fix the clash in the game file once, then run build.py.

## 5. How to re-run

**Setup:**
- `pip install playwright numpy pillow`
- three r128 and acorn 8.12.1 unpacked under `$CADET_WORK/three` and `$CADET_WORK/acorn` (`npm pack`).

**Commands** (`PS=plans/split-rehearsal`):
- `python3 build.py --check`
- `node names_check.js [GAME.html]`
- `bash check_fast.sh`
- `python3 $PS/replay.py WORKDIR aa4f42c ae44907 c8e3735 bf1c2f9 3add6bf` (0.64.0); add nothing for post-split, or use split commit `be3d7ee` for the all-pre-split version.
- `python3 $PS/replay.py WORKDIR 898d58d 8a72e61e 9f6b1105 7b29c3fc 0e4d8f82 46e22701 8944a430` (0.63.3).
- `python3 $PS/sweep.py OUT.json --since=2026-09-01 [--norm-build]` (about 10 minutes), then `python3 $PS/clash_kinds.py OUT.json`.
- `python3 $PS/scenarios.py WORKDIR [NAME ...]` (about 4 minutes; the transcript is in `WORKDIR/scenarios.md`).
