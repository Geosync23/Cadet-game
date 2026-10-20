# Handover: ways-of-working engineer (WW1)

**Role:** step 2 of `plans/roadmap-after-recdeck.md` as the user decided on 2026-10-20: **no cut of the game file**; bring in the new ways of working on the one file. Started by lead 20 (session_019UJSCUCdtC1kTpYiABWKhs). Session session_0192KVdPtywdv7sp3mXUXGHU. Branch `claude/ways-of-working`, started from `claude/rec-cand-s1` 1eeb99c (0.64.2). Report to the lead with send_message; never contact the user; never touch main or the main game link.

**Timing rule from the lead:** until the lead says the rec deck is published, change NO line of `starship-cadet.html` and don't message the build master BM10. Everything here is check files, tools and docs, built to merge cleanly on top of the final rec deck tip (they touch no line the rec deck round touches, except possibly the same check files if BM10 edits them: check with `git merge` when it lands).

## State: "Now" part done (see the commit list on the branch)

| Piece | Where | State |
|---|---|---|
| names_check.js (acorn; names, table keys incl. `T.key =` and gated blocks, registrations by id, "Deck 7"; reports section + line) | `names_check.js` | Ported from claude/split-rehearsal; pieces code dropped; the section rule now also finds `// 24a ROUNDS`-style headings (56 sections). 3807 names, 2838 keys, 50 registrations on 0.64.2, OK, 1 s. 8 planted problems all caught, each exit 1. |
| check_fast.sh (lanes waited on by pid; a step passes only on exit 0 AND its OK line) | `check_fast.sh` | Ported; pieces/build.py steps dropped. On 0.64.2: QUICK CHECK OK in 297 s (deck 224, device 249 alongside, machine 49, leave 23). |
| Exit-code fixes (exit 1 on failure, printed lines unchanged) | deck, machine, day, food, path, perf, disc, arc, social, cadet_test | Taken from the rehearsal (cadet_test: only the exit line; its pieces guard dropped). Proof: see "Proof" below. |
| clash_kinds.py | not ported | It reads the split rehearsal's sweep output (a split-only measurement); nothing to port for the one file. The build master's clash count (the evidence gate) is by hand, in the start-prompts draft. |
| Section finder | `tools/section.py` | list / print a section / `--where LINE` / `--diff [A [B]]` with owners from owners.md. |
| Shared-names lister | `tools/shared.js` | functions and UPPER_CASE tables/state used outside their own section, with exact signatures; `--md` makes owners.md's list. Uses acorn only. |
| GitHub check | `.github/workflows/quick-check.yml` | **DISABLED: `on: workflow_dispatch` only** (runs only if started by hand). Two commented `on:` blocks for the lead: A = shared branch `claude/integration` only, B = every claude/ branch. Validated as YAML. Pushing it triggers nothing. |
| Owners | `plans/owners.md` | the user's rule, sections → seats (the split plan's owners), contracts by hand, SHIP's records, the generated list (187 names used by 4+ other sections). |
| Map | `plans/map.md` | how to find things, file order vs section numbers, a topic → section table. |
| Backlog | `plans/backlog.md` | 13 rows + fixed. Item 3 (the "double clock hold") was dropped by lead 20 and the user: no record, probably the Day 0 evening's two designed holds (kept under "Dropped"). |
| Drafts (not applied) | `plans/step2-drafts/` | README (order), claude-md.md, dev-notes-rules.md, build-table-move.md, slots.md + add_slots.py (tried on a scratch copy: 17 slots, names_check OK; merge test: clean with slots, clash without), whole-file.md, start-prompts.md. |

## Proof of the exit-code fixes

Each of the 10 checks run three times on 0.64.2, each in its own CADET_WORK: the old copy (rec-cand-s1 1eeb99c), the new copy, and the new copy on a planted failure (a page error 4 s after load, `err.html`; cadet_test: the HUD room name's font size changed, `look.html`). Results (old and new print the same lines; the only differences are timings and cadet_test's 1-level renderer noise):

| Check | Old | New | Planted failure |
|---|---|---|---|
| cadet_test | ALL IDENTICAL, exit 0 | ALL IDENTICAL, exit 0 | DIFFERENCES FOUND, exit 1 |
| deck_check | OK, 0 | OK, 0 | FAILED, 1 |
| machine_check | OK, 0 | OK, 0 | FAILED, 1 |
| day_check (day 1) | OK, 0 | OK, 0 | FAILED, 1 |
| food_check | OK, 0 | OK, 0 | FAILED, 1 |
| social_check | OK, 0 | OK, 0 | FAILED, 1 |
| path_check | OK, 0 | OK, 0 | 1 problem, 1 |
| disc_check | ALL OK, 0 | ALL OK, 0 | FAILED, 1 |
| arc_check (70 days) | OK, 0 | OK, 0 | (14 days: STALLS, 1) |
| perf_check | **1 problem, exit 0** | **1 problem, exit 1** | 2 problems, 1 |

**perf_check on 0.64.2 reports a problem in both copies:** "memory grows across deck round trips: geo 548, 548, 550" (two geometries over three round trips; tex and heap flat). The old copy printed it and exited 0; the new one exits 1. Earlier rounds' perf PASS was the performance engineer's judgement on the printed numbers. Reported to lead 20: either it's a real small leak on 0.64.x (rec deck round trips?) or perf_check's rule needs a tolerance; until settled, perf_check's exit 1 there is expected. arc_check run with 14 days stalls by design (arcs need the default 70); the planted run used 14. Scripts: `plans/step2-drafts/proof/proof.sh` (one check, old/new/plant; paths are this session's scratchpad: edit SP) and `plant.py` (the 8 planted name problems).

## "Later": done 2026-10-20 (lead 20: the rec deck published, claude/rec-cand-s1 c575a8e)

1. c575a8e merged in (it added only DEV_NOTES and plans/cand-0640-results.md; the game is the same file). BM10's perf note: the 548→550 memory line is the same on 0.63.5 and accepted, so backlog 14 asks the performance seat for a tolerance (perf_check now exits 1 on it).
2. `archive/starship-cadet-0.64.2-whole.html`, sha256 e4897023…27624 = the published game. **The frozen branch is the lead's:** name `claude/whole-file-0.64.2`, at commit **c575a8e** (claude/rec-cand-s1, the published rec deck).
3. Slots: `python3 tools/add_slots.py` → 17 slots, 51 comment and blank lines. cadet_test vs c575a8e ALL IDENTICAL (0 px on all 15 shots), names_check OK, content_gen --check up to date, check_fast OK in 317 s. Build number unchanged (0.64.2); a "0.64.2 (step 2)" row at the end of plans/build-table.md.
4. Applied: CLAUDE.md (Read first 5, Files, How we work, the user's two rules, determinism line); DEV_NOTES (Builds summary, Rules "Shared work", Testing top, File map pointer, Working method); `plans/build-table.md` (1046 rows, unchanged; DEV_NOTES 1.42 → 0.47 MB); `plans/start-prompts-step2.md`. Not applied: DEV_NOTES' stale top paragraph (lines 3-8) and TEAM.md (the lead's files).
5. The GitHub check stays switched off.

## Gotchas

- acorn 8.12.1 must be unpacked at `$CADET_WORK/acorn/package` (names_check.js, tools/shared.js, add_slots.py). check_fast's GitHub job does it itself.
- The file's section order isn't numeric (13-24 sit between 5 and 6); section ids are the stable handle, line numbers drift.
- Section headings: `^// <num><letter>? optional-dot space CAPITALS`. A new heading in that form shows up in section.py, names_check and shared.js automatically; a comment line like `// 18 SHIP hours` (number then capitals) would be taken for a heading, so keep comments in sentence case.
- shared.js counts a name as used where it appears as an identifier; a local variable shadowing a top-level name counts too (rare; it overstates, never hides).
- The user gets an email for every red GitHub run: the check stays off until the lead switches it on.

## How to test

```
pip install playwright numpy pillow
mkdir -p /tmp/cadet-work/three /tmp/cadet-work/acorn
(cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz)
(cd /tmp/cadet-work/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz)
node names_check.js; bash check_fast.sh; python3 tools/section.py --diff HEAD~3 HEAD
```

## Open questions (for the lead)

- The shared branch's name: the split plan said `claude/integration`; the workflow's option A and the drafts use it.
- Who applies the slots: the drafts say the build master (it's the shared file).
