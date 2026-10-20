# Handover: patch planner and patch reviewer (PP1)

**Role.** I started as the playtest patch planner (PP1) and then became the patch reviewer. I was spawned by lead 20 and have reported to **lead 21** (session_01KYPEbF745ZQ9g9kr4XJgre) since 18:12 UTC on 2026-10-20. Planning and reviewing only: I never edit the game, and push only to **claude/patch-plan**. A fresh session taking over reads this first.

## What I own and built (all on claude/patch-plan)

- **The playtest patch plan, final:**
  - `plans/patch-plan.html` and `.md` hold all 28 notes plus #29 (cocoa at the bar) and #30 (the mug), with the user's answers marked decided (published by the lead; db `answers/patch-plan`).
  - Revisions:
    - 2f8976c: first version
    - 767ce33: revision 2, with the user's answers and PR1's review (`plans/patch-plan-review.md` on claude/patch-plan-review)
    - b8865a9: revision 3, First Light Cocoa, #29, #30
    - b2e7220: final
- **First Light Cocoa's draft words:** `plans/patch-plan-first-light-cocoa.md`, the .trad and .meet for the writers. Route names are placeholders.
- **Reproduction:**
  - `plans/patch-plan-probes/`, with harness `pp.py`: cadet_test's Game at 390×844, saving on, so a first launch arrives on Day 0. `fnet.py` measures the net Tier 1 repair time; `mug.py` is the mug mock-up.
  - Shots are in `plans/patch-plan-shots/`; PNGs are git-ignored, so use `git add -f`.
- **Short Fridays and the Captain's address:**
  - `plans/fridays-plan.html` and `.md`. Revisions: 8e407ba (first), 155433a (Crossing the Line note), eb7a5d6 (revision 2, the user's answers).
  - Published at https://claude.ai/artifact/8UwSCYe3LsQGoDBgxYeJQp; db `answers/fridays-plan`.
  - design-doc.md updated in eb7a5d6: the shifts section, weekly traditions and weekday shapes.
  - **Open:** fp-v2-q1 (Day 12's address during the ion storm; recommended: as usual, in the auditorium) and fp-v2-general.
- **Backlog #15:** the goal arrow lowercases a name ("zeke Torres", section 15b).

## Reviews done (verdicts sent to the builder and the lead)

| Builder / branch | Items | Verdict | Notes carried forward |
|---|---|---|---|
| PE claude/patch-e 2e2575d | #25, #21, #6, #24 | PASS WITH FIXES | Fixed in 274a31f: typeof guards; the clock note held 5 s on purpose |
| PA claude/patch-a e9d9022 | #1, #2, #28 | PASS (pending PA's intro_check) | introSig carries the meeting's end time (intro only, DEV_NOTES line); section 14 hooks need PB's owner review |
| DB1 claude/devmode 05314b6 | #30 mug | PASS | Sleep or another activity should finish the mug quietly; owner reviews 15/15b/8b |
| DB1 claude/devmode 375827b + c1036ae | #29 | PASS | Passed to PE, who now owns DB1's work |
| PE claude/patch-e ab685bb | #5 ladder + fixes | PASS | Nit: `|| c.role` on the Relationships card; at switch-on, day_check on Decks 2/6 |

**Next in the queue:** PE's #26 First Light Cocoa, when PE pushes. Then PB's batches D and F, and PA's batches B and C, as they report.

## How I review (the start-prompts-step2.md "Reviewer" list, plus the plan's pass marks)

1. `python3 tools/section.py --diff BASE HASH`: the sections touched and their owners. New code goes in the seat's slot; small edits elsewhere are OK, with an owner review before merge.
2. **Build number untouched:** `git diff BASE HASH -- starship-cadet.html | grep -n "build 0\.\|GAME_BUILD"` prints nothing.
3. **check_fast** in a worktree: `git worktree add -f /tmp/rv/wt HASH`, then `CADET_WORK=/tmp/work-RV1 bash check_fast.sh`.
4. **cadet_test BASE HASH** with the switch off must come out ALL IDENTICAL, or each difference is explained. Use BASE = the commit just before the turn, or the branch's own merge commit if it merged integration.
5. The builder's probes, then my own probe for the item's pass mark, at phone size, looking at the shots.

**Gotchas:**
- **Never run check_fast and cadet_test at the same time on 4 cores:** cadet_test's page load times out (30 s). Run them one after the other.
- Each run needs its own CADET_WORK, with `three/` and `acorn/` linked from /tmp/cadet-work (setup in DEV_NOTES "Testing").
- `pkill -f` with a pattern that matches your own shell kills it (exit 144).
- Bubbles' CSS classes are `.bub` and `.bubw`; hide them for close-ups.
- Patch builders' probe folders: `plans/patch-e-probes/` (PE). PA didn't commit probes: write your own (my rvA.py style: arrive, idle the intro on paper, skipTo Day 2, put the player in the room).

## Shared formats

- **Answer forms:** `form#answers` (with `data-collection` and `data-doc` for the lead's wiring), `div.q[data-qid]`, radios named by qid, the recommended option marked, a `<qid>-comment` textarea per question, plus a general box. The lead publishes and wires saving.
- **Plan-page style:** the dark CSS from patch-plan.html (copy its `<head>`), phone-checked at 390 wide with no sideways scroll.

## Loose ends

- fp-v2-q1 is still open (Fridays, Day 12 during the storm).
- PA's intro_check result for batch A was pending when I passed it.
- Mug nit (sleep finishing it quietly): PE should fold it into #26's turn.
- Patch #29's leisure +8 only applies with MUG_ON (deliberate: they're gated together).

## Memory

537k of 1M when this was written (2026-10-20 ~18:31 UTC). The rule: tell the lead at 500k; hand over and stay idle at 600k.
