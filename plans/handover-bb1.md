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

## Follow-up
- RV23-2 done (e69b2235): Day 32 stops being a workday after the career offer, so "Clock in" (asked at 08:00) never cleared; its done
  now also reads !playerOnDuty(d). arrows_check endgo track: stuck 1 -> 0. The Day 31 "air plant" arrow didn't show in two runs.

## After the fixes
- RV25 then RV26: the whole branch PASS at 564b8a50 (FX8-1 swimmer-leaving look: no glide through a wall).
- RV25-1 (the sketch shelf's Schedule row names your cabin now: Deck 2's room B after the move) fixed in 564b8a50, PASS.
- 0.98.0 full round, share R4 on staging-pad 7a2ae7d2: OK (career only backlog 12, the same on 0.97.0). Notes: plans/checks-0980-r4.md.
- Nothing open. A fresh session taking BB1's role starts from the lead's brief; my branch is merge-ready for the build master.
- Scratch: a detached worktree /home/user/r4 (the 0.98.0 candidate) can be removed with `git worktree remove /home/user/r4`.

## How I tested
Probes in Playwright reuse cadet_test.py's prelude (exec of its top, as day_check does) and `Game(pw, path)`; each fix was run on
0.97.0 (git show 610ad7f1:starship-cadet.html) and on the branch. Then cadet_test vs 610ad7f1, the area's checks, check_fast.
Gotchas: check_fast reads starship-cadet.html itself, so never edit it while check_fast runs (run other checks on a copy);
a `//` comment pasted mid-expression comments out the rest of the line (run names_check after every edit); a pgrep wait loop
whose pattern appears in its own command line waits forever.
