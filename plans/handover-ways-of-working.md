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

Each of the 10 checks run three times on 0.64.2, each in its own CADET_WORK: the old copy (rec-cand-s1 1eeb99c), the new copy, and the new copy on a planted failure (a page error 4 s after load, `err.html`; cadet_test: the HUD room name's font size changed, `look.html`). Results table: filled in at the end of "Now" (see the commit message and the report to the lead). Scripts: `plans/step2-drafts/proof/proof.sh` (one check, old/new/plant; paths are this session's scratchpad: edit SP) and `plant.py` (the 8 planted name problems).

## "Later" (only when the lead says the rec deck is published)

1. Merge the published tip into this branch; rerun check_fast and names_check.
2. The slots: `python3 plans/step2-drafts/add_slots.py`, then cadet_test (old tip vs slots) ALL IDENTICAL + screenshots (phone and desktop) for the lead; no build number change.
3. The whole-file archive copy + frozen branch (`plans/step2-drafts/whole-file.md`).
4. Apply the drafts: CLAUDE.md, DEV_NOTES rules/testing, the build table move (ask the lead about DEV_NOTES' stale top paragraph first), the start messages (the lead's file).
5. TEAM.md is the lead's: tell the lead what to add.

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
