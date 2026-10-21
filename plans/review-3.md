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

- check_fast on integration 675588c (0.64.6) passed in 213 s (CADET_WORK=/tmp/work-RV3).

## A clash found: Friday traditions in 15:30-17:00 (sent to FR1 and the lead)

The Fridays plan says "Nothing runs between 15:30 and 17:00" on a Friday. At 675588c two live TRADITIONS do:
- cook-along: Fri 15:30-16:30, the mess (line 33728).
- tiles-ladder: Fri 15:00-16:30 with jitter 15, the bow lounge (line 33772).

With SHORT_FRIDAY on, both clash with the 16:00-16:50 address. Where they move is the user's call. On review: with the switch on, no tradition overlaps a Friday 15:30-17:00; with it off, both are unchanged.

## EW1 friday-weekly.address: claude/events-lines d15803c (content, sent by EW1). PASS WITH FIXES

**Clean:**
- Marrow's voice is right (calm, "we", quiet jokes, nothing on her NEVER list), and there are no spoilers.
- Names and facts match the game and facts.md.
- The pools last 6-8 weeks without obvious repeats.
- Every line fits 90 characters with a 24-character {me} (NAME_MAX) and the longest tradition name, apart from fix 4.

**Fixes:**
1. `cue:tradition.tasting-table` (Tuesday) and `cue:tradition.department-cup` (Sunday) never fire: the tradition cue lasts 1 day (SOC_CUE_OF). Add a "this week" condition with FR1, or drop the two lines. {winner} must read as a team name.
2. `cue:tradition.tiles-ladder.you`: the ladder sits on the address (the clash above). Hold it until that's decided.
3. The people pool's `pick: 2` can repeat a welcome or a goodbye. Split it into an arrivals pool and a leavers pool.
4. Line 73 is 94 characters with three leavers (Day 161). "This week" for rotations means since last Friday's address, because they land on Sundays.

**Carried:**
- myrank: still needs agreeing.
- The new slots and conditions are FR1's to build; health: is section 17's.

**For the lead:** the nod rotation has no Bridge/helm week.
