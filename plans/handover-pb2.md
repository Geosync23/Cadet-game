# Handover: PB2 (sim engineer, patch builder B2), 2026-10-22

Written by PB2 (session_01NWyw8ebj9kTTRiEnAj2bGo) at about 60% memory, on lead 26's go. A fresh session taking the
role reads this, then PB's note (`plans/handover-patch-builder-b.md` on origin/claude/patch-b).

## Role, people
- **Owner of sections 10 (walkers), 13 (ship time and saving) and 14 (crew schedules)**, and the reviewer for any edit
  in them. Reports to the lead: **lead 26, session_015mHBLCf5jpnzBkFY1iBTqv** (branch claude/lead-26). Reviewer
  usually OR2 (session_01AnRKXUUGi8mwREwvt4WbaV). Build master BM13 (session_01ExFoVfhiFG3wYTFv2QrojC).
- Never set the build lines. Small exact edits, a build-table row per piece of work, check_fast before every push.
- **Fixes meant for integration start from `claude/integration`** (lead 25's rule, after patch-b2 sat on line-update).

## Branches and what's on them
| Branch | Base | State |
| --- | --- | --- |
| `claude/patch-b2` | claude/line-update 8bfff3b | All reviewed (OR2 PASS). Game commits **cherry-picked into integration 0.64.14** by BM13: be8871d, d7159a6, 38424f0, 5b4eb4f. Its rows: 1a8e4b7, de5ca2c, cb04cff, 8bffab5, 135caaf, 388751c; the scan 5843d29. This note too. |
| `claude/patch-play1-c` | claude/integration 32b699a6 | Playtest 1 note 17 only. Tip **0ecf99fa**, OR2 PASS, waiting for BM13 (C merges first in 0.64.15). |

## What I built (all reviewed)
1. **Double dinner** (be8871d, section 14): a meal tradition eaten standing (no seat left) sets `e.ate` in `tradMeal`;
   `evening()` / `morning()` count it, so no second meal. Base Days 21/28, Line Day 7 (12 people) cleared.
2. **Harvest salad on a farewell day** (d7159a6, section 16, lead's OK): `galleyMenu` re-adds "with fresh garden salad"
   when a farewell note replaced it (backlog PB2-2).
3. **Backlog 18** (38424f0, section 14): the storm's `stayIn` gated rec visits on the rule, not the block's roll:
   `stay = si && schedU(...) < si.share`. Events-off path only (EVENTS_ON's storm closes deck 7).
4. **PB2-3** (5b4eb4f, section 17, lead's OK): `jobRun` returns null when a stop's machine panel is held by another
   unfinished job then. Scan: `plans/pb2-probes/jobclash.py` (on paper; misses live-only clashes, day_check 13 covers one).
5. **Playtest 1 #17, crew drawn through walls** (6007b653, section 10): the walking lane used `>> 3` on an unsigned
   hash, so half the crew's lanes reached -0.54 tiles. Now `>>> 3` (±0.18 as designed). From #10 (a67ea08e, since 0.64.6).
   **day_check now checks it** (72727293): each lane within `WALK_LANE`; walking frames the lane alone draws within .1
   tile of a wall at most `LANE_WALL` = 0.1% a deck (Day 1 fixed: 0-0.05%; old build 2.6-5%).

## Reviews I gave (all as owner)
- L5j (line-update ee21dd7): PASS. FR4's #20 hold 2078010: FAIL (Day 0 dinner), reverted; fridays-20 db001aa (with my
  backlog 25 stand-in edit): PASS. TQ1's toilet queue (claude/patch-play1-i 0c05e856): PASS for 10/14.
- **Open:** SC1's breakfast at 07:00 (claude/patch-play1-f, lead's decision A: shifts unchanged, early starters grab)
  if it arrived after this note: its section 14 lines are MEALS.breakfast, schedFrame's wake line, the night-shift
  breakfast order. Watch the 05:45 watch handover, the galley's early stints, ON1's Day 1 06:00 d1-wash beat.

## Backlog rows I own or added
PB2-1 (rota days' own meal count; tradition-Sunday waste: left as is), PB2-2 (fixed), PB2-3 (fixed), 18 (fixed),
25 (fixed with FR4). Section 17 job-routing changes: rerun jobclash.py.

## Gotchas
- Run checks at most two at a time on 4 cores, each with its own CADET_WORK. Never `pgrep -f` / wait loops on a
  pattern that appears in your own command line (they match themselves).
- **A check copied from another branch may be older**: line-update's food_check lacks FD1's fixes and gave 17 false
  FAILs once. Use the check from the branch you test against.
- day_check runs decks in order and the crew's `R()` draws carry over: to trace a live case, patch a copy of
  day_check itself (I did, `day_check_tr.py` style), don't write a separate probe.
- Paper plans vs live: jobs and storm chores are made in play; machinesNow on paper doesn't see them all.
- Copy commit hashes from git output (I mistyped two in messages).

## How to test my areas
day_check (several days: 1, 5, 12, 13, 21; event days with switches on), food_check (integration's copy), path_check,
machine_check + mech_check (section 17), jobclash.py, cadet_test (crew-only differences explained), check_fast.

## Open questions for the user
None from me.
