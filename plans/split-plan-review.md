# Split plan review (step 2)

Reviewer: split reviewer SR1 (session_011v45ss6jgs29Y68mkhZz35), 2026-10-20. I reviewed `plans/split-plan.html` as SA1 drafted it (25c52a5) and checked each claim against the real game files and checks. Then I made my own pass on the page, in the same commit as this file.

Bases used: 0.64.0 = `claude/rec-cand-s1` e71388f (sha256 534ceeda…918aa, 49,807 lines); 0.64.2 = 1eeb99c (BM10's merge of RE20's fixes, sha256 e4897023…27624, 49,829 lines). Tools: python 3.13, node 22, Chromium at /opt/pw-browsers, three r128 from `npm pack`, on a 4-core container.

**Verdict.** The core idea is sound: the cut is a plain text concatenation at section markers, and gluing the pieces back gives the same bytes. I reproduced that myself with a separate script, on both bases. Two blockers and several should-fix items were in the process around it, not in the cut itself. All of them are fixed on the page now, apart from four calls for the lead or the user (end of this file).

Ratings: **blocker** = would lose work or hide failures; **should fix** = wrong or missing, with a concrete cost; **nit** = small.

## Findings

### B1 (blocker): "rerun build.py" after a merge silently throws work away
- **Claim (risks table):** "The glued file gets out of step, or two helpers' glued files clash in a merge: never fixed by hand: rerun `build.py`." The risks table also said pre-split branches are carried over by "running `split.py` on its file and merging the pieces".
- **Evidence:** I tried it in a scratch repo built on 0.64.2:
  1. Branch X, from before the split, edits `starship-cadet.html` (GAME_BUILD and a comment on `ternClear`).
  2. Main splits the file, edits a piece and glues again.
  3. Merging X: git auto-merges `starship-cadet.html` with no conflict and no message (rc 0). The pieces don't change.
  4. `build.py --check` fails, which is correct. But following the plan (`build.py`) wipes X's edit: the count of its marker went from 1 to 0.
  5. Running `split.py` on the merged glued file instead kept both X's edit and main's piece edit, and the glued file and pieces were back in step.
  6. Merging pieces on their own ("split X's file, then merge the pieces") would instead give add/add conflicts on every piece.
- The same silent path opens whenever anyone edits the glued file by habit. CLAUDE.md, DEV_NOTES and dozens of briefs all say to edit `starship-cadet.html`.
- **Changed:** the risks table and a new technical subsection "Getting back in step":
  - after your own piece edit: glue again;
  - after a merge: cut again;
  - the scripts compare with `HEAD^1` (for a merge) or `HEAD` (for unsaved edits), say which case it is, and stop if both sides changed;
  - old branches: merge as usual, then cut again.

### B2 (blocker): two of the four fast checks exit "success" when they fail
- **Evidence:**
  - `deck_check.py` and `machine_check.py` have no `sys.exit`. They print `DECK CHECK FAILED` / `MACHINE CHECK FAILED` and exit 0.
  - Measured: `machine_check.py` on 0.64.0 printed `MACHINE CHECK FAILED` (FAIL "wear differs (caches cleared)", "traced faults") with rc=0.
  - So `check_fast.sh` and the GitHub check would show a green tick on a red check.
  - leave_check and device_check do exit 1 on failure.
- **Changed:** the page now says turn 3 adds `sys.exit(0 if ok else 1)` to both (a check-only edit). Belt and braces: `check_fast.sh` should also require each check's OK line.

### S1 (should fix): the base is 0.64.2, not 0.64.0, and machine_check fails on 0.64.0
- Byte identity holds on both (my marker-based cut: identical, 40 pieces, each time).
- Line counts differ on 0.64.2 in schedules (+1), player needs (+2), interactions (+1), rec activities (+4) and machines (+14).
- machine_check fails on 0.64.0 (RC's determinism bug) and passes on 0.64.2. The fast check can only gate pushes from a base where it's green.
- **Changed:**
  - the header says the cut is made on the final rec deck build (0.64.2 today);
  - the piece table uses 0.64.2's counts;
  - the fingerprints for both trials are shown;
  - the archive name and branch name follow the build.

### S2 (should fix): sessions can't push git tags
- **Evidence:** `git push origin sr1-probe-tag`: "send-pack: unexpected disconnect … the remote end hung up". `git ls-remote --tags` shows no tag, so nothing was left behind. A second attempt was blocked by this session's permission guard, so I didn't push further.
- Turn 1's "tag `whole-file-0.64.0`" therefore can't be done by a session.
- **Changed:** turn 1 keeps the archive copy plus an unchanging branch `claude/whole-file-<build>`. A tag stays optional, as one click on GitHub's Releases page for the user.
- The archive copy costs nothing in git: it is the same file contents as the glued file, so git stores it once.

### S3 (should fix): the GitHub workflow sketch would fail on every run, and its path filter misses files
- **pip:** every check `exec`s the top of `cadet_test.py`, which imports `numpy` and `PIL`. The sketch installed only playwright. **Changed:** `pip install playwright numpy pillow`.
- **Path filter:** it missed `cadet_test.py` (the base of every check; `*_check.py` doesn't match it), `content_gen.py`, `plans/trad_parse.py` (content_gen imports it), `plans/crew-roster-gen.py`, and the name scan's script. **Changed:** all of them added.

### S4 (should fix, good news): sessions can push workflow files
- **Evidence:**
  - 618087d added `.github/workflows/sr1-probe.yml`: `on: workflow_dispatch` only, and a manual-only workflow can't even be started from a non-default branch.
  - The push was accepted. 2122b1c removed the file.
  - `actions list_workflow_runs`: 0 runs.
- **Changed:**
  - the risk row now says "tried: it doesn't" refuse the file;
  - the user's "one paste" fallback is gone from turn 3;
  - the user may still need to switch Actions on.

### S5 (should fix): the duplicate-name scan misses names and silent table clashes
- **Evidence:**
  - The column-0 grep finds 3,359 names. A real parse (acorn 8.12.1) finds 3,807 top-level names. The grep only sees the first name in lines like `let W = 0, D = 0, OX = 0, OZ = 0;`.
  - The plan left `Object.assign(TABLE, {…})` key clashes for later. Those are exactly the silent kind: a second key quietly wins.
  - There are 2,740 such keys over the shared tables, many in one-line `Object.assign(PLAYER_ACTS, { … })` calls. The existing `tools/kitdup.py` covers only KIT, and a line-based generalisation I wrote misses the one-liners.
- **Also:**
  - `node --check` parses as a CommonJS module, so it accepts a top-level `return` that the browser rejects. Parsing with `sourceType: 'script'` is the browser's view.
  - Repeated `const`/`let` are already caught by any parse. Repeated `function`s are not, and I confirmed node accepts two `function f(){}`.
- **Changed:**
  - the scan reads the glued script with acorn (fetched with `npm pack`, like three);
  - sketch `plans/split-tools/names_check.js`;
  - 1.1 s on 0.64.2: 3,807 names, 2,740 keys, no repeats;
  - it caught all three planted cases: a second `function ternClear`, a second `PLAYER_ACTS.tidy`, and a repeated `let` (reported as a parse error with the game line).

### S6 (should fix): the build number would clash on every early merge
- The build number sits on two lines that every helper bumps every turn:
  - `const GAME_BUILD = '0.64.2';` in the time-and-save piece;
  - `build 0.64.2` in the header, in the setup piece.
- With "merge into the shared branch after every reviewed piece", every merge clashes on both. `tools/fixrate.py` exists only to resolve this.
- The DEV_NOTES build table (rows added at the same spot) has the same problem.
- **Changed:** section 5 now says the build master sets the build number when merging, and helpers note their work in their branch's notes.
- **Open for the lead:** this changes CLAUDE.md's "bump the build number each turn" rule.

### S7 (should fix): "Deck 1: Bridge" held about 880 lines of everyone's places
- From `// ---- Big gatherings` (0.64.2 piece line 226) to the end of 4d, the piece was the shared places and kit for every deck, with code from many seats:
  - big gatherings (`gatherSpots`, read by sections 14 and 18);
  - the Tern ramp;
  - keepsakes;
  - `WALL_KIT` additions;
  - delivery crates, haul drops, valve panels, shelves, dressing.
- Owning all of that as "Deck 1" is wrong. SA1's note "moved to their decks in the clean-up" would change load order and with it the game's bytes, so the clean-up's checks would have to carry it.
- **Changed:** a 40th piece, `js/s04d-places-all-decks.js` (876 lines), cut at that marker. Still byte-identical on both bases. The Deck 1 piece is 225 lines.

### S8 (should fix): piece numbers clashed with section numbers
- The draft numbered pieces by glue order, so the piece number and the section number disagreed for most pieces. For example:
  - `js/15-device.js` was section 19;
  - `js/16-player-needs.js` was section 15;
  - `23-events` was section 18;
  - `24-social` was section 20;
  - `29-camera-grid` was sections 6 and 7.
- The code's own comments and every note say "section 15's playerTap", "section 18's loader" and so on, so "piece 15" next to "section 15" invites edits in the wrong file.
- **Changed:** pieces are named by section (`s19-device.js`, `s15-player-needs.js`, `s04d-deck4-quarters.js`, `s22-words.gen.js`, …). The order lives only in `pieces/ORDER`, which the page already said.

### S9 (should fix): no way back was described
- **Changed:** a new risk row and a line in "In one breath". Because the glued file is committed and always in step, undoing the split means deleting `pieces/` and the two scripts. Nothing is lost and the game doesn't change.

### S10 (should fix): the final-newline rule was wrong, and nothing enforced it
- The page said every piece ends with a newline "except `tail.html`". In fact the file ends `</html>\n`, so tail.html ends with one too.
- Nothing enforced the rule. If any piece loses its final newline (some editors strip it), its last line joins the next piece's first line. A `//` note at the end of one piece would then comment out the next piece's first code line.
  - Example: `s22-words.gen.js` ends `// ---- END TRADITIONS ----`, and `s22-lines-engine-2.js` starts `const LINE_TIER = …`.
  - Whether the parse step notices depends on what follows, so the break can reach run time.
- **Changed:** the sentence is corrected, and `build.py` refuses a piece without its final newline.

### S11 (should fix): the fast check's timings were partly off; the total holds, just
- Measured on 0.64.2, two lanes side by side, each with its own CADET_WORK:
  - deck 200 s, then machine 46 s, then leave 20 s (lane A, 266 s);
  - device 224 s alongside it (lane B);
  - **4 min 26 s in all, all OK.**
- deck_check alone took 122 s (on 0.64.0). The plan said machines ~15 s (it's 46 s) and device ~4 min (it's 3 min 44 s).
- **Changed:** the page shows the measured times and says the margin is only about half a minute.
- Static steps measured: content_gen `--check` 0.8 s, `lines_check` 3.5 s (not in the fast check), names scan 1.1 s, `node --check` 0.2 s.

### S12 (should fix): private-repo numbers
- Verified: the repository is **public** (`private: false`), and there are no workflows and no runs today.
- From GitHub's docs: public repositories on standard runners are free. GitHub Free includes 2,000 minutes a month for private repositories (Pro 3,000). The default spending limit is $0, so runs stop rather than bill.
- At about 7 minutes a run, 2,000 minutes is about 285 runs a month, or about 9 a day.
- **Changed:** decision 3 and the technical section say this. If the repository goes private, the workflow narrows to `branches: [claude/integration, main]` and helpers keep running the quick check themselves. (Whether to make it private is SA1's and the lead's question for the user.)

### S13 (should fix, flagged, not changed): "a change in someone else's piece goes through its owner"
- Most features cut across pieces: the rec deck touched 47 deck-word sites and seven or more sections. Routing every small edit through a busy owner seat makes the owner a bottleneck.
- Suggestion: anyone may make a small edit in another seat's piece, and the owner reviews it before it merges into the shared branch. It's a ways-of-working call, so I left the page as it was. **For the lead or the user.**

### Nits
- **N1. Commit count unverified.** I count 405 commits on 10-19 over the branches I fetched, against the "786" on the page. It doesn't change the conclusion. Left as it was.
- **N2. Line endings.** Add a `.gitattributes` with `pieces/** -text` and `starship-cadet.html -text`, so no git setting can ever convert line endings in the glued file or its pieces. Today the file has no CR, no tab, no BOM and no trailing spaces. Not on the page; a one-liner for turn 2.
- **N3. Checks find their part of the game by its section heading.** `disc_check` slices `// 23b. LIGHTDISC` to `// 24. WORK`, and `tiles_check` slices `// 23. TILES` to `// 6. CAMERA`. `day_check` and `disc_check` patch `const REC_DECK = false;` and `const REC_TRAD_ON = REC_DECK;`. `cadet_test.instrument` uses the last `})();`. All of these work on the glued file. Section headings are load-bearing, so the risk row now says so and map.md should list them.
- **N4. Single-file merge-conflict helpers.** `tools/resolve.py` and `tools/fixrate.py` resolve clashes in `starship-cadet.html` itself. After the split, either retire them or point them at the pieces, or they "fix" the glued file.
- **N5. Readers of the glued file stay correct while it's committed and in step.** These are `lines_check.py` (the roster), `plans/traditions-calendar-gen.py` and `tools/kitdup.py`.
- **N6. A boundary hazard nothing catches yet.** A piece whose last statement has no `;` and a next piece starting with `(`, `[` or a template string could join differently. Pieces start with comment banners today, but comments don't stop automatic semicolon insertion. It's unlikely; a later step could have acorn check each piece's last token.
- **N7. `claude/integration` can sit beside `claude/integration-test`.** Neither name is a folder of the other.
- **N8. Phone width.** The draft page scrolled sideways (532 px wide at 390) because of the long sha256 in the technical section. **Changed:** `code{overflow-wrap:anywhere}`. Now 390 px, with no page errors at 390 or 1100.

## Claims I verified as true
- **The cut and byte identity.** Cutting at section markers and gluing back gives identical bytes: SA1's 39 pieces on 0.64.0 (sha 534ceeda…918aa, as stated), and my marker-based 40 pieces on 0.64.0 and on 0.64.2.
- **Every piece parses alone.** All 36 code pieces pass `node --check` on 0.64.2, and on 0.64.0 for SA1's 35.
- **`content_gen.py` works on the piece.** `content_gen.py PIECE --check` says "up to date", and a real run on a copy of the piece rewrites it byte-identically. `crew-roster-gen.py` splices by its markers, so pointing it at the crew data piece works the same way.
- **The checks are unaffected.** Every check takes the game file as an argument, or defaults to `starship-cadet.html`, which stays.
- **The build is deterministic.** Identical bytes mean identical `R()` sequences, and the regressions carry over.
- **The repository is public, and Actions is free there.**

## Evidence to re-run
- `python3 plans/split-tools/split_sketch.py GAME.html OUT -v`: cuts by markers and says whether the glued result is identical.
- `node plans/split-tools/names_check.js GAME.html`: needs `npm pack acorn@8.12.1` unpacked under `$CADET_WORK/acorn/`.
- Merge experiment (B1): a scratch git repo with steps 1 to 5 above; about 20 lines of shell, described in B1.
- Timings: the two-lane command in S11, with `CADET_WORK=/tmp/sr1-a` and `/tmp/sr1-b`.

## Open calls for the lead or the user
1. **Build number (S6):** the build master sets it on merge, and helpers stop bumping it. This changes a CLAUDE.md rule.
2. **Owners (S13):** "through the owner" or "anyone edits, the owner reviews"?
3. **Tags (S2):** fine with a frozen branch plus the archive copy, or should the user add a Releases tag?
4. **Private repository (S12):** SA1 is raising visibility with the user. The page covers both answers.
