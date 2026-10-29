# Handover: BB1 (0.99 backlog builder; was BT1, the backlog triage helper)

Session: session_01GKuymne2zVMSTZjvCCmXKH. Lead: lead 45 (session_01GKuymnu4NeXJhwPe21FWk7), reviewer RV25 (session_01GKuymnnpKvNH4Ki69KEzwG).

## Branch
`claude/backlog-triage` (this session may push only here). Restarted from `claude/staging-pad` 610ad7f1 (0.97.0, live), with the
old triage commits merged back in (a merge commit, no history rewrite). Build lines untouched (the build master's).

## What's here
- `plans/backlog-triage.html`: the "Backlog before 1.0" page (https://claude.ai/artifact/FVcaELmHkiq2hHCQp6defE). The user's answers are in
  its db collection "answers" (44 docs). Version 1 lost the user's first answers (a redraw on every db change); version 2 saves each answer
  by itself and never redraws over unsaved ones.
- `plans/backlog-1.0-final.md`: the user's final list (the lead later moved the 1.0-patch items into 0.99).
- The fixes, one commit each ("Backlog <id>: ..."), build-table row 0.97.0-bb.1. Done: FX17-1, N6-1, PB1-1, TM-1, DV1-3, DV1-2, FX21-1,
  30, FX3-2, FX10-1, RV18-D1, RV18-C2, RV18-C1 (guard, not reproduced), FX3-1 (lead 45's OK), CP5-1 (controller_check a11y follows),
  RV23-3, 15 (Saruth, lead 45's smallest version), FX8-1 (drawn glide, horizontal only). Sent to RV25 at tip 167a07c4.
- No change: 31, JB1-1 (already fixed on 0.97.0); EV1-1 (lead 45: no change). Not reproduced: DV1-1.
- Left for others (lead's call): V-1 seated formal dinner and V-2 vessel nod (events side), SD3-1 (SD3).

## In progress
- RV23-2: the follower's stale "Clock in: shift at 09:00" from 16:03 the day before (Day 32) and "air plant, Deck 5" on Day 31, from
  RV23's arrows endgo track run. Reproducing with `arrows_check.py BUILD endgo track` (about 25 min).

## How I tested
Probes in Playwright reuse cadet_test.py's prelude (exec of its top, as day_check does) and `Game(pw, path)`; each fix was run on
0.97.0 (git show 610ad7f1:starship-cadet.html) and on the branch. Then cadet_test vs 610ad7f1, the area's checks, check_fast.
Gotchas: check_fast reads starship-cadet.html itself, so never edit it while check_fast runs (run other checks on a copy);
a `//` comment pasted mid-expression comments out the rest of the line (run names_check after every edit); a pgrep wait loop
whose pattern appears in its own command line waits forever.
