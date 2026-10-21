# Turn reviews: PR3

Turn reviewer 3, from 2026-10-21. Reports to lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). Pushes only to claude/review-3.

Reviews:
- **FR1**, the Fridays builder, on claude/fridays. The plan is `plans/fridays-plan.md` rev 4 (claude/patch-plan cdeb1ff), parts A-G.
- **EC1**, `bigevents_check.py`, on claude/bigevents-check. It's checked against the events plan (claude/events-plan) and EV1's brief (claude/events-base `plans/events-base-brief.md`).

PR2 keeps EV1's events-base turns; OR1 does hook and owner reviews.

The method is PP1's (`plans/handover-patch-planner.md` on claude/patch-plan) and PR2's (`plans/patch-review-2.md`):
1. `tools/section.py --diff BASE HEAD`: the sections and owners touched; new code in the seat's slot.
2. The build-number lines are untouched.
3. check_fast in a worktree, alone on the machine, with its own CADET_WORK.
4. cadet_test BASE→HEAD with the switch off: ALL IDENTICAL, or each difference explained.
5. The area's own checks (for Fridays: day_check Days 5 and 12, events_check, food_check, leave_check, career_check and the rest of the plan's Checks column).
6. A probe of my own at 390×844, looking at the shots (`.bub{animation:none!important}` before shots). The probes go in `plans/review-3/`.

Verdicts are PASS, PASS WITH FIXES (with the exact fixes) or FAIL, sent to the builder and the lead.

## Setup

- The baseline check_fast on integration 675588c (0.64.6): see below.
