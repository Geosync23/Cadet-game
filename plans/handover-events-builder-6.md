# Handover: events builder 6 (EV6), the ion storm's last steps

Written 2026-10-21 ~15:40 UTC by EV6 (session_012u45Yq4bSmo6bgqe5phZ9b), at about 285k tokens, for the account move
(lead 24's ask). Read EV4's note first (`plans/handover-storm-builder-2.md`), then EV3's (`plans/handover-storm-builder.md`).

## Role, branch, people

- **Role:** the ion storm update's last steps: the user's lantern supper change, the S9 clean-up, S10 (switch-on).
  Crossing the Line moved to EV7 (session_01WeSNWT2a7Fs8HS3j9HWamK), not this role.
- **Branch:** `claude/storm-update`, head **ab3e2fb7** (S10). Never set the build lines (BM12 does); name each turn in
  the "Ion storm update" table of plans/build-table.md.
- **Lead:** lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r (lead 23 handed over ~12:50).
- **Reviews:** PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i). PB (session_01FWW2piuXkFYaRRzLXZiqYb) owns sections 10/13/14.
  EC1 (session_01QgShGXD6P24DDxTp8npN41) owns bigevents_check.py (take it as is from claude/bigevents-check).
  FR3 (session_01935gmiyLoy5fgvs3xQd7QC) owns Short Fridays and fridays_check. FD1 (session_01YJhagf6oyF6SeT5XGvrL5H)
  owns the food_check dinner waits.

## What I built (all pushed)

| Commit | What | Review |
| --- | --- | --- |
| 829f242c | **Lantern supper in seated sittings** (the user's change, 11:45): EV4's standing diners out (section 10's `trayTo` back to one argument, `evStandTray` gone, day_check's `standMeal` gone, the `@gather-mess` places gone); the supper `seated: true` (new: eventPools leaves a seated event's venue crowd spots out; every venue gathering gets them otherwise), `stay: [45, 60]`, 18:00-19:45 (len 105). 51 sat, at most 42 at once of 48 seats. design-doc's storm section. | PB OK, PR6 PASS |
| fd11d82c | design-doc: the no-standing rule is the lantern supper's, not general; the Line supper is an open question (lead 24 is asking the user; EV7's) | doc only |
| 4a48faca | **S9 clean-up:** the three old stand-ins (the events plan's first audit f9431a62 item 14: the plain address banner ADDRESS_EL, the plain dialogue strip DIALOGUE_EL, the old camera shake eventFeelFrame + FEEL.flicker), all shadowed by section 19 / 8b; events_check's 4 lines. Off: ALL IDENTICAL. | PR6: read, fine; runs queued |
| db60020a | merged claude/fridays 11b2220 (notes conflicts only) | — |
| b991877a, 88bd57c2 | EC1's bigevents_check ef9d7fc, then 2de5554 (handles EVENTS_ON on already) | EC1's |
| ab3e2fb7 | **S10:** `const EVENTS_ON = true;` (one line), design-doc + DEV_NOTES ("on"; how to switch off), build-table row with the round | to PR6 |

Results of the S10 round: `plans/storm-s10-round/` (summaries, each FAIL's lines, round.sh the runner).

## In flight / exact next step

1. **Done (see the build table's 'storm S10 findings' row):** devmode_check's failure is chance (a random game seed can make Day 8 a sick
   day; re-run OK); career_check fails the same way switched off (not new); mech m17 is a check problem (storm wear leaves crew
   repair jobs in its Day 18 window, so its two passes differ). The devmode fix is DB2's; the mech m17 check fix is done (the build table's "storm S10 mech_check fix" row).
2. Nothing in the game needs changing for S10.
3. Take FR3's fridays_check fix (storm lines filled with the storm on) and FD1's food_check fix (claude/food-waits
   0f808c3) when they land; re-run those two.
4. Report to PR6 and lead 24. BM12 merges S10 with FR3's turn 10 (SHORT_FRIDAY on) together, only on lead 24's go.

## Gotchas

- The planner gives any gathering with a `venue` its venue's crowd spots (eventPools): `seated: true` to keep them out.
- A meal gathering's sitting must leave `min` (25) minutes after the walk to the line (long from the garden), or the
  diner eats with no place. A short `stay` makes that worse, not better.
- Test copies now flip the other way: on is the default; off = `sed 's/^const EVENTS_ON = true; /const EVENTS_ON = false;/'`.
- cadet_test can't see the storm (Day 1, Deck 4): the full round is the proof.
- Background jobs are killed at 2 h, including time spent waiting: chain checks in ONE job, not waiters.
- perf_check writes perf_check.json in the repo root: don't commit it.

## How to test a turn

names_check, then the area's checks on and off (events_check, day_check 11-15, bigevents_check, food_check 11 4), then
cadet_test (off copy against the last tip: ALL IDENTICAL), then check_fast, then the build-table row, commit, push, PR6 and lead 24.
