# Handover: reviewer PR9

Written 2026-10-22 by PR9 (session_01B1FUTc4sJR4Q5FFnx7L6Db). Every result, find and verdict is in `plans/review-9.md`;
logs in `plans/review-9/logs/`, shots in `plans/review-9/shots/`, tools in `plans/review-9/`.

## Role, branch, people

- **Role:** reviewer. Took over from PR8 (Short Fridays), then controller support (foundation, P1, P2, P4), now the
  Pillar 5 fixes FX1-FX3.
- **Branch:** `claude/review-8` (push only there). Never changes the game.
- **Lead:** lead 28, session_01S7AdxK1ZyXiEFowP3k5gng (leads 25-27 handed over; TEAM.md on the lead branch is the
  source).
- **Builders now:** FX1 session_01WmdPR5B5QC56Hid3F5M1wv (claude/p5-fix1), FX2 session_01JRCSTi6r1qQ51mTgwgJ7es
  (claude/p5-fix2, nothing received yet), FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (claude/p5-fix3). AR1
  session_01XcfcbFvi4nMVUPZgT2BcmE owns `arrows_check.py` (claude/arrows-plan) and the arrows plan.
- Controller people (all my packages passed): CT1 session_019sqDowb6QNf3KZAYMSx1jM, CP1 session_015ZhJRKCEditHrVhwdhszYq,
  CP2 session_016zb2DTsTLqNNNeuegePDgE, CP4 session_01VTXDwLqWGJVRh95HozqhCu, RV2 session_01E1TTHbhLzy2U6pAoGh7E9a,
  RV5 session_01DdhmKNwjve4tpJ1zq6ozyv (combined controller branch), CTT2 session_011yMob9ZzgmCFENoNhjJ44z (the check).

## State (verdicts)

| Work | Verdict |
| --- | --- |
| Short Fridays: release (storm + Fridays), 208581c, c3b76f4, 5b55f84, 3bd9b2c, fridays-20 + its check | all PASS (done) |
| Controller foundation (turns 1+2), turn 3 (game) | PASS |
| Controller P1 (cff5bab7), P2 (5b4d9f0 incl. "George"), P4 (f904532) | PASS |
| FX1 1433e5f | FIXES NEEDED (sent): TRAIN_LEAD 15; meeting arrow back after a borrowed arrow clears; a new stuck "Take your first round at the job board" arrow blocks Clock in Days 3 and 8 |
| FX3 b063f86 | PASS WITH FIXES: own parts fail on base / pass on tip, cadet_test identical, the main lift green in arrows_check. Fix (clear only its own arrow, INC_GOAL) done by FX3 in its next push: re-check that delta + hauling on any day + the promotion talk |
| FX2 | moved to AR2 (lead 27) |

New red for AR1/FX1 (exposed by FX3): "Repair the light relays" arrow up over 3 ship hours from Day 2 09:49 (logs/fx3_ar_week.log).

## How to test (Pillar 5)

- Base copy: integration 2b4a05db. `arrows_check.py` from claude/arrows-plan: `python3 arrows_check.py BUILD.html shift`
  (~4 min), `week` (~12 min). Baseline FAILs: `logs/ar_base_shift.log` (2), `logs/ar_base_week.log` (18). For each fix:
  its own check part FAILs on 2b4a05db and passes on the tip; cadet_test 2b4a05db → tip ALL IDENTICAL; arrows_check lines
  that turn green, and any line that turns red that was green (FX1 did that: Days 3 and 8 clock in).
- Clashes: FX1+FX3 merge with only a build-table conflict, but both call setGoal/clearGoal: check who clears whose arrow.
- To run an older check file against the base, copy it under another name and fix its `__file__.replace(...)` line.

## Gotchas

- `pkill`/`kill` by a pattern that is in your own command line kills your shell (exit 144); find pids with awk excluding
  itself, or write the script to a file first.
- Editing a running bash script does nothing (bash keeps the old file): kill and restart.
- Container restarts kill background runs: rerun from where the logs stop (low pids show a restart).
- The test harness fixes the page clock (`performance.now` is virtual): frame time can't be measured in a check page.
- One browser at a time.

## Open questions for the user

None from me (the name question was answered: "George", no rename).

## Stopped (2026-10-22 ~14:20, memory near 60%)

Left for the next reviewer: (1) FX1's re-check when FX1 pushes (its three fix requests; arrows_check week must not turn
Days 3 and 8 clock-in red; compare with logs/ar_base_week.log and logs/fx1_ar_week.log); (2) FX3's next push: the INC_GOAL
delta (mech_check fx3's new "Food" arrow case should fail with the old unconditional clearGoal), hauling's lesson on any
day, the promotion talk readable; cadet_test and arrows_check week again.
