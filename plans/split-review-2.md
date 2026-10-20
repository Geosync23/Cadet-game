# Split plan: second review (SR2)

Reviewer: second split reviewer SR2, 2026-10-20, branch `claude/split-review-2`. I reviewed `plans/split-plan.html` as it stands at cc833f8 (after SR1's pass), against the game on `claude/rec-cand-s1` 1eeb99c (0.64.2, 49,829 lines, sha256 e4897023…27624). I wrote my findings before reading SR1's review (`plans/split-plan-review.md`), then compared the two (section 6).

## For the user, in plain words

**Short answer: the cut itself is safe, but the split fixes fewer of our real problems than it seems. My advice is to make the new ways of working first, without cutting the file, and to cut later only if the numbers show we need it.**

- **What the split promises and what it delivers.** I went through the project's history: every name clash, hand merge, long combine, lost piece of work and bug in the checks. Almost all of them are fixed by the *other* changes in the plan, and those changes don't need the cut:
  - the name scan;
  - the quick check;
  - the GitHub check;
  - merging early into one shared branch;
  - the build master setting the build number.
- **Why the cut doesn't stop name clashes.** The worst clashes came from two helpers each building the same thing in their *own* part of the file. A split puts those two parts in two different pieces. The glue then joins them straight back into one game, and the clash returns. Only the name scan catches it.
- **What the cut does help.** It helps with one kind of clash: several helpers adding new code at the *same spot*. That happened in every Pillar 5 combine, when everyone added their part just before section 6. But the plan's piece list keeps that spot: it becomes "the end of the cases piece". We can get the same benefit without cutting, by giving each helper its own empty, labelled slot in the file in advance. The social section already did this (section 20c), and it worked.
- **What the cut costs.** After the split there are two copies of the game in git: the pieces and the glued file. I tried the plan's "after a merge, cut; after an edit, glue" rule on a test copy. It broke in two ways:
  1. **An ordinary clash between two helpers stops at the build master every time.** A "merge" is when git combines two helpers' work. If two helpers change the same line, or two lines next to each other, git can't decide alone and flags a "clash". The rule then can't tell what to do and stops. That happens even when the two helpers worked in different pieces.
  2. **A fix can disappear without a word.** Say a helper fixes something in the glued file by mistake and saves it. If they edit a piece later and glue, the fix is quietly thrown away.

  Both can be fixed, but they show this two-copies set-up is harder to get right than the plan says.
- **A bigger memory problem than the game file.** DEV_NOTES.md is 1.4 MB, and its build table alone is about 1 MB. A fresh session told to "read DEV_NOTES first" can't. Moving the table into its own file saves more memory than the split would.
- **The GitHub check needs someone to look at it.** It's a good idea. But our helpers push to branches with no pull request, so nobody is told when it goes red. (A pull request is GitHub's page for asking to merge one branch into another; it is where check results normally show up.) The build master has to look at the check for that exact version before merging. The plan doesn't say so.
- **The repository is public**, as the plan says: anyone can read the game, the notes and the history. That's what makes the GitHub check free. The authors of five old commits show a personal email address. If you'd rather not have that public, we can talk about it separately (it has nothing to do with the split).

**Recommendation: option (d) below.**
1. Now: all the new ways of working, plus labelled slots in the one file, two small tools for finding your way around, and a slimmer DEV_NOTES.
2. Then: build one real step (Dev mode) that way and count the clashes.
3. Then: decide on the cut. If we do cut, fix the issues listed under "If you still want the split" first. You have decided to keep the glued file in git, so the script fixes for B1 and B2 below are required before the cut, not optional.

You lose nothing by waiting: the cut is mechanical and can be done on any later build in half a day.

GitHub terms used here, in one line each:
- **Branch:** one helper's own copy of the project.
- **Merge:** git combining two branches.
- **Clash** (git calls it a "conflict"): the same lines changed on both sides, so git stops and a person or session has to choose.
- **Commit:** one saved step.
- **GitHub check** (GitHub "Actions"): a program GitHub runs by itself after each push, which shows a green tick or a red cross.

## 1. Is splitting the right move? Problem by problem

Sources: DEV_NOTES.md, TEAM.md, the build masters' and lead's handover notes, and the trial results files. The numbers are from a full search of those files; the details are in this branch's history of the review.

| Problem (how often) | Example | Fixed by the split? | Fixed without the split? |
|---|---|---|---|
| Name clashes between sections (~17) | `BUSY` 0.30.7, `planWhere` 0.33.10, `worksTick` 0.44.2, `traceHidden` Step 3, `REC_SHOW` 0.83.3 | **No.** The pieces are glued back into one game, so two pieces still share one set of names. | **Yes:** the name scan (names_check.js) on every push, and one owner per function. |
| Build-number lines clash on every merge (35+ mentions; resolve.py, fixrate.py, setbuild.py written for it) | Every combine | No. | **Yes:** the build master sets the number on merge (plan section 5). |
| Many helpers adding code at the same spot (every Pillar 5 combine, 0.63.0–0.64.0; res24.py, union24.py, unionall.py) | 24a–d, 24e/f, 24h, 24p, 24g/24k all added just before `// 6. CAMERA` | **Only if each block gets its own piece.** The plan's list keeps one spot: new 24x blocks would all go at the end of `s24k-cases.js` (owned by seat H). | **Yes:** a labelled empty slot per seat in the one file, made in advance. Section 20c did exactly this "so social engineer A's merges never clash" (DEV_NOTES "Social stories"). |
| Two owners editing the same function or line (~12) | teach-loop line, `jobStopsBase`, `edgeBlocks`, `INTRO_SCENES`, `recTap` | No: same piece. | Partly: one owner per function, and early merging (smaller, fresher clashes). |
| Long combines (0.60.3 took ~9 h, 0.63.4 had 18 trials; a full round takes 45–90 min) | Two days of work combined at once | No. | **Yes:** early merging and the quick check. The check runs are the real time sink, and the plan leaves them unchanged. |
| Lost work in merges (~8) | `-X ours` dropped section 13's bus; scripts that skip a merge or commit conflict markers | No, and it adds a new way to lose work (finding B2). | Mostly: early merging (small merges need no scripts) and the build master's verify step. |
| Determinism (MACH_HIST, mech_check leaks, the build label's width) | 0.64.0's machine_check | No. | Partly: the rule written into DEV_NOTES; checks gate pushes. |
| Check fragility (CADET_WORK sharing, stand-ins, 9 checks exit 0 on failure, text-based slicing) | False passes in 0.63.4 | No. Slightly worse: one more way for a check to test old code (B3). | **Yes:** check exit codes, own CADET_WORK, quick check. |
| Session memory running out (9 build masters, 19 leads in 5 days) | The 4.7 MB publish read takes 8 helpers; a 1.4 MB DEV_NOTES | A little: smaller files to read and edit. Exact-string edits are easier to make unique in a 2,000-line piece than in a 49,800-line file. | **More:** move the 1 MB build table out of DEV_NOTES (S1 below); a section reader tool. The publish read is unchanged either way (the glued file still has to be read in full). |
| Code hidden after `//` (bit us 3+ times) | 0.53.15 roofTalk guard | No. | Reviewers grep for it; could join the quick check. |

**Conclusion:** of the ten problem kinds, the split on its own fixes none. It helps with one (same-spot adds), and only if pieces are cut finer than planned. Labelled slots give the same help without a cut. Everything else is fixed by the process changes, which don't need the split.

### The options

- **(a) No split, only the process changes.** This fixes most of the problems. What's left: same-spot clashes, and big-file editing.
- **(b) The split as planned.** Adds a two-copies set-up with real failure modes (section 2), and doesn't remove the same-spot clashes.
- **(c) A lighter split (words and big independent systems only).** All of (b)'s glue machinery for less benefit. The words are *already* split out: writers edit `content/` and content_gen.py fills the game, so cutting the generated block out of the file changes nothing for anyone.
- **(d) Recommended: (a) plus four small additions, then an evidence gate.**
  1. **Labelled slots:** before the next step, put one empty, marked block per seat in the file (like 20c), where that seat adds new code. That removes the same-spot clashes.
  2. **`tools/section.py`:**
     - `section.py 19` prints section 19 with game line numbers;
     - `section.py --where 23456` names the section of a line (useful for error messages from the browser);
     - `section.py --owner` lists which sections a branch's changes touch, so a reviewer can see when someone edits outside their area.

     That gives "find your way" and "who owns this" without the cut.
  3. **A slimmer DEV_NOTES:** move the build table (lines 12–1065, ~977 KB) to `plans/build-table.md`, and leave the last 20 rows in DEV_NOTES.
  4. **Evidence gate:** run Dev mode (step 3) this way. The build master counts the clashes that need a person, and what each was. If same-spot or big-file clashes are still frequent, cut then, with the fixes in section 2.

## 2. What can still go wrong with the plan as revised

Ratings: **blocker** = loses work or hides a failure; **should fix** = a concrete cost; **nit** = small. (The B numbers below are mine; SR1 also used B1 and B2 for its own two blockers, which are already fixed on the page.)

### B1 (blocker): the "scripts decide" rule stops every ordinary clash, even between different pieces
- **The rule (technical detail, "Getting back in step"):** "both changed and still out of step, stop and ask the build master".
- **Test 1, different pieces.** Scratch repo on 0.64.2, with my faithful sketch of the rule in `tools/glue.py` (scratchpad):
  - Helper A adds a function at the end of `s05-lighting.js`.
  - Helper B adds a note at the top of `s13-time-save.js`.
  - Each glues and commits. Merging both: the pieces merge cleanly, but **the glued file clashes**, because the two edits sit on neighbouring lines there.
  - The rule sees pieces changed and glued file changed, out of step, and STOPs.
  - The right answer was simply "glue".
- **Test 2, the same piece.** Two helpers change the same line of `s05-lighting.js`.
  - The clash appears **twice**: once in the piece, once in the glued file.
  - After the piece is fixed by hand, the rule STOPs again.
  - This contradicts the risks table's "fix the clash in the pieces, then glue again".
- **Failure scenario:** early merging means several merges a day. Each clash becomes a build master ticket, and the build master's load goes up, not down. A helper who wants to get on may "fix" the glued file by hand to get past the stop.
- **Fix:**
  - During a merge (`.git/MERGE_HEAD` present), if no piece has conflict markers, glue. The glued file is never the source after the split.
  - Or better: don't keep the glued file in git at all (S2).
  - A `.gitattributes` line `starship-cadet.html merge=ours` does **not** help on its own. I tried it: git still flags the clash, because "ours" only works after `git config merge.ours.driver true` in every copy of the repo, and every fresh session would have to remember that.

### B2 (blocker): a committed hand edit to the glued file is lost without a word
- **Test:**
  1. The helper edits the glued file by mistake. Old notes, grep results and browser error lines all point there.
  2. They commit without running the quick check.
  3. Later they edit a piece and glue.
  4. The rule compares with HEAD: pieces changed, glued file not changed, so it glues.
  5. The committed fix is gone (`MISTAKE_FIX` count 1 → 0). No message.
- **Why:** the rule only asks what changed since HEAD. It never asks whether HEAD itself was in step.
- **Fix:** before gluing or cutting, check that HEAD's pieces glue to HEAD's glued file. If they don't, cut HEAD's glued file first, or stop and say so. Same for HEAD^1 on a merge.

### B3 (blocker): checks can test the old game and report OK
- Every check reads `starship-cadet.html`. A helper who edits a piece and forgets to glue, then runs `day_check.py` alone (as briefs and reviews do, outside the quick check), tests the *old* code. They then report "day_check OK" for their change. Reviewers and build masters trust that line.
- Only check_fast's first step catches this, and helpers run single checks all the time.
- **Fix:** `cadet_test.py` (which every browser check loads) refuses to run when `pieces/` exists and the build file it is given is the repo's own `starship-cadet.html` and is out of step with its pieces. It should say "run build.py". That's a few lines in one file.

### S1 (should fix): the GitHub check's result reaches nobody
- Helpers push to branches without pull requests. A red cross on such a commit wakes no session; only pull-request activity reaches a session.
- "Nothing depends on a session remembering" (roadmap) is therefore not true yet.
- **Fix:** before each merge, the build master reads the check result *for the exact commit being merged*, with the GitHub tool `actions_list` → `list_workflow_runs` on the branch. A result for an older push doesn't count.
- Also, with "cancel-in-progress", a helper who pushes every few minutes never gets a finished run. The build master should wait for one, or run check_fast itself.

### S2 (should fix, but the user has decided otherwise): keep only the pieces in git, not the glued file (decision 2's other choice)
- **Update, 2026-10-20:** lead 20 passed on the user's call that the glued file stays committed. I leave the reasoning below for the record. With that call, B1 and B2 must be fixed in the scripts before the cut, and B3 (the checks refuse an out-of-step build) matters even more.
- With the glued file in git:
  - every clash appears twice (B1);
  - there are two sources of truth, which needs the cut-or-glue rule (B1, B2) and makes helpers' grep hits double (`recShow`: 18 real hits become 36);
  - an old habit (edit the big file) does damage.
- Without it, the plan's listed costs are each small and fixable once:
  - checks auto-glue: one call in cadet_test.py, which also fixes B3;
  - publishing: `python3 build.py` first;
  - "open an old version": `python3 build.py --rev <commit>` glues the pieces as they were then, about 5 lines. Builds before the split are already whole in git.
- The only real cost is moving pre-split branches across (plan section 6). That is a one-time job for the build master at the cut, with split.py.

### S3 (should fix): the duplicate-name scan still misses silent second winners
- names_check.js covers top-level names, and keys in `const TABLE = {…}` and `Object.assign(TABLE, {…})`. It misses:
  - registrations by id: 23 `deviceApp({ id: … })` calls write to a Map, where the second silently wins;
  - 58 top-level `TABLE.key = …` assignments (some, like `SHIP.tiles`, are meant to happen twice);
  - 63 top-level `.push(` registrations;
  - anything inside an `if (REC_DECK) { … }` block, and that is where gated features live.
- **Fix:** also scan id strings in `deviceApp(`, `.set('…'` and the main registers. Keep an allow-list for the intended repeats.

### S4 (should fix): the plan's piece list keeps the same-spot clash
- New mechanic blocks have always been added just before `// 6. CAMERA`. After the cut that is the end of `s24k-cases.js` (seat H).
- **Fix:** if cutting, give each new sub-block its own piece and its own line in ORDER. Two seats adding ORDER lines in the same place is a one-line clash, easy to resolve. Or make the labelled slots of option (d).

### S5 (should fix): check_fast.sh's "side by side" must wait on each lane by name
- If the two lanes are written as `lane1 & lane2 & wait`, the plain `wait` returns success even when a lane failed. The plan's GitHub check would then go green on a red check.
- **Fix:** `wait $A || fail; wait $B || fail` (as in my timing script). Also require each check's OK line, as SR1 suggests.

### S6 (should fix): DEV_NOTES is too big for a fresh session
- 1,419,347 bytes; the build table is 977,470 of them (lines 12–1065). CLAUDE.md says to read DEV_NOTES first "every session".
- The lead handover is 216 KB more.
- **Fix:** move the table to its own file and keep the last 20 rows in DEV_NOTES. Start a fresh `handover-lead.md` from its last section. This helps memory more than the split.

### S7 (should fix): fresh sessions are pointed at the big file from everywhere
- CLAUDE.md, DEV_NOTES (with "around line N" all through it), 60+ handover notes and the browser's error messages all name `starship-cadet.html` and its line numbers.
- `plans/map.md` helps, but every grep and every stack trace lands in the glued file first.
- **Fix:**
  - `build.py --where LINE` (or section.py) turns a glued-file line into piece and line;
  - the first line of the glued file says "generated: edit pieces/, run build.py";
  - CLAUDE.md "Files" says the same.

### N1 (nit): cadet_test and the other full-run checks also exit 0 on failure
Nine scripts never exit non-zero: day, deck, disc, food, machine, path, perf, cadet_test, name_check. SR1 fixed only the two in the quick check. Fix the rest too: the build master's full runs, scripted, have the same blind spot.

### N2 (nit): split.py's markers are fixed heading texts
- A new column-0 line that matches one (say, a note starting `// 15b. `) makes it stop. That is safe, but puzzling.
- Once the pieces are the source, split.py is only for recovery. It could cut at the current pieces' first lines instead of a fixed list.

### N3 (nit): the build master's load
- The build master merges every reviewed piece, runs the glue and the quick check (~5 min), sets the build number and pushes.
- At 10+ merges a day that is close to an hour of check time, plus every B1 stop.
- That's fine if B1 is fixed, but the build master should hand over earlier than other helpers.

### What each helper sees in practice (with the plan as written)
- A helper edits `pieces/js/s19-device.js`, runs `build.py`, and commits both files. Most of the time that works.
- What goes wrong:
  - **the session forgets to glue** before running a single check: B3;
  - **it merges the shared branch in and hits a clash:** B1 sends it to the build master;
  - **it greps and edits the big file:** caught by check_fast if run, otherwise B2 can bite later.
- "After a merge, cut; after an edit, glue" is the kind of rule AI sessions follow well *when a script does it for them* and badly from memory. So the scripts must be right in every case above.

## 3. Five claims checked on a scratch copy

| Claim | Result |
|---|---|
| Cut and glue give the same bytes on 0.64.2 | **True.** split_sketch.py: identical, sha256 e4897023…27624, 40 pieces, 1.3 s. |
| Every code piece is valid on its own and ends with a newline | **True.** All 37 `.js` pieces pass `node --check`; every piece ends in a newline. |
| content_gen.py works on the words piece | **True.** `content_gen.py pieces/content/s22-words.gen.js --check`: "up to date" (10,017 lines, 442 conversations, 48 traditions), the same as on the whole file. It needs `plans/trad_parse.py` present, as the path filter now lists. |
| "The scripts decide which case it is, so nobody has to remember the rule" | **False in two cases** (B1, B2), from a faithful sketch of the stated rule. |
| Deck and machine checks report failure only in words; the repository is public and has no workflows | **True.** No `sys.exit` in deck_check.py or machine_check.py. GitHub: `private: false`, 0 workflow runs. |
| The quick check takes about 4.5 minutes on 4 cores | **True, just:** 4 min 39 s here, all passing (timing note at the end). |

## 4. If you still want the split: the minimum before turn 2
1. Fix B1 and B2 in the scripts (required, since the glued file stays in git by the user's call).
2. Make the checks refuse an out-of-step build (B3).
3. Write into the build master's brief: read the GitHub check result for the exact commit before merging (S1).
4. Give new mechanic blocks their own pieces (S4).
5. `wait` on each lane by name (S5); fix every check's exit code (N1).
6. Slim DEV_NOTES (S6), and add a line-to-piece finder (S7).

## 5. What SR1 found that I didn't, and what I found that SR1 didn't

**SR1 found, and I didn't look at:**
- sessions can't push tags (the frozen branch instead);
- the workflow's pip and path filter;
- the wrongly owned "Deck 1" piece (now `s04d-places-all-decks.js`);
- piece names matching section numbers;
- the final-newline rule;
- `.gitattributes -text` for line endings;
- the automatic-semicolon hazard at piece boundaries;
- retiring resolve.py and fixrate.py after the cut;
- the owner-bottleneck question.

All good. I agree with each.

**I found, and SR1 didn't:**
- **The big question:** the split on its own fixes none of the ten problem kinds, and options (a) and (d) do almost all of the work.
- **B1, B2:** the fix for SR1's own B1 (the cut-or-glue rule) has two holes: every clash stops at the build master, and a committed hand edit is lost.
- **B3:** single checks can test stale code.
- **S1:** nobody is told when the GitHub check goes red.
- **S2:** the case for leaving the glued file out of git.
- **S3:** the name scan's blind spots (registrations, gated blocks).
- **S4:** the same-spot clash moves to the end of `s24k-cases.js`.
- **S5:** the `wait` trap.
- **S6, S7:** DEV_NOTES size, and the line finder.
- **N1:** the other seven checks that exit 0.

## Timing note
Re-timed on 0.64.2 in this 4-core container, two lanes side by side, each with its own CADET_WORK, waiting on each lane by name:
- lane A: deck 206 s, then machine 51 s, then leave 22 s;
- lane B: device 234 s alongside;
- **4 min 39 s in all**, all four passing.

SR1 measured 4 min 26 s. So the 5-minute goal holds, but with only about 20 s spare. The deck check alone is 3½ minutes of it. Any growth in the checks, or a slower GitHub machine, goes over. That's not a failure (GitHub doesn't stop a run at 5 minutes), but plan now which check moves out first.
