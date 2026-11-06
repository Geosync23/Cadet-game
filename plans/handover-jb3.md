# Handover: JB3 (patch 0.99.7, the user's notes 3, 21, 22: jobs and places)

- **Role:** jobs builder for lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Reviewer **RV32** (session_01GKuymkDX3gviqiGJcKLWuS).
  My session: session_01GKuymmiCEm3CMMrMTdWMEo (JB3).
- **Branch:** `claude/p997-jobs` from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8). Build number lines untouched.
- **Switches:** `var JB3_SHELF_ON, JB3_SCI_ON, JB3_REC_ON, JB3_TEA_ON, JB3_FOOD_ON` in section 17's Systems slot (the JB3 block after JB2's), all
  **false** on the branch (cadet_test vs 0.99.6: ALL IDENTICAL). The build master switches them on. Every test of the
  features ran on a copy with all three true.

## What each note does (with the switches on)
- **Note 3, "the player doesn't get lights from the light shelf".** Two causes found, both fixed under `JB3_SHELF_ON`:
  1. The shelf ran out. The crew's repairs (section 17 jobsHour, the crew claim) took the last parts, so between
     Wednesday deliveries relays were at none most of Days 5-10 and lamps ran out on Day 13. A chore that needs a lamp has
     no lathe path, so it was stuck till Wednesday while the arrow still said "Fetch a lamp: the Lights shelf". Now the
     crew leave `SHELF_KEEP` (relay 2, lamp 2, breaker 1, cable 1; never a NO_MAKE part) and make theirs at the lathe
     instead (`jb3Keep(p)`, two edits in jobsHour). Probe: relays and lamps never under 2 over 14 days.
  2. The shelf marker. The arrow's pin is the place in front of an aisle (5-parts-1..4), as near the shelf before it as
     its own; a real tap at the pin met the neighbouring shelf at two of four camera turns for Filters, Plumbing and
     Galley parts (48 of 72 taps: "No filters on the Lights shelf", every time). `jb3PinTap(id)`, asked by `shelfWrong`:
     a tap whose line passes within JOB_RAY of the wanted shelf's spot is that shelf. After: 96 taps, 0 fail.
  Also section 15's fetch toast (Player engineer's line) says the lathe's real minutes (makeMins) instead of "about an hour".
- **Note 21, more science-area jobs, especially early.** `jb3Post` (one hook line in boardTopUp, before the board count):
  while no science-room job is up for you, one is posted from FX10's science stream in `SCI_ROOMS` (survey lab L, sample
  lab M, observatory J, chart room K, science corridor '='): two a shift in Days 1-7 (from 09:00 and 13:00), one a
  shift after (from 10:00); a room you had a job in over two days passed over; counts toward the board's minimum. Not
  while the ship's upkeep is under `SCI_UPKEEP` 10 in all (without that machine_check 5v "the ship meters: your jobs"
  failed: a steady player had the upkeep done in week 2 and small jobs showed no meter). Week 1 on paper: 7 offered (was 2).
- **Note 22, a few rec deck jobs in the first week.** `REC_N` 2 small jobs on the rec deck in Days 2-7, one a shift day
  from 10:00, `REC_GAP` 2 days apart, two different rooms; flags `jb3.rec` (days posted) and `jb3.recRoom`, so a day the
  board is held for a training job just moves it on. On paper: Days 2 and 4. Nothing after week 1.
- **Backlog CR1-2 (lead 49's extra item), `JB3_TEA_ON`:** a round's check point c5-water ("the tea corner's water tap",
  5-tea-3) is the Hot water, but tapping it or the Mug rack made tea (ixTea) and the check was never done. Section 15's
  `choreThingTap` asks `jb3CheckThing(j, nx, it, s)`: while a round's next stop is a check point, a tap on the thing
  `CHECK_THING` names for it (c5-water: Hot water, Mug rack), within `CHECK_REACH` 3 m, is the stop. The follower's side
  (it tapped the washroom Toilet through the wall; its "water" rule kept the visit going) is backlog JB3-2 (check side).
  JB3-1: a chore whose part is out still has no lathe path (rare now with the reserve).
- Jobs posted carry `j.jb3` ('s' or 'r'), FX10's shape (chore 'fix', fixS of their stream).

## Tests (switches on, copy)
machine_check OK (and each switch alone), interactions_check, arrows_check shift week OK, day_check Day 1 and Day 2 OK,
deck_check OK, puzzle_check OK; check_fast on the branch OK; cadet_test vs 0.99.6 ALL IDENTICAL (switches off). Probes in the scratchpad were one-offs (lamp chore,
grow-light repair, the shelf from every turn, shelf pins at 4 turns x 6 spots, a science and a rec job by real taps,
stock over 14 days); `tools/jobs_measure.py BUILD 14 --json OUT` gives the mix (count science rooms and rec deck by week).

## Gotchas
- `jb3Keep` is asked by jobsHour, which can run before the slot's line at load: the switch is a `var`, so it reads
  undefined (false) and short-circuits before `SHELF_KEEP` (a const) is touched.
- `jb3PinTap` reads section 11's `ray` (set at each tap). A check calling playerTap directly carries the last real tap's ray.
- CR1 (claude/p997-career, the board mix for newly learned types) may also edit boardTopUp / boardTradePost: my only line
  there is `if (JB3_SCI_ON || JB3_REC_ON) jb3Post(h, jobs, t, m, end);` just before `let n = jobs.filter(...)`.

## Open questions for the user (defaults built)
- The Works keeps two relays and two lamps (one breaker, one cable) on the Lights shelf for your jobs: yes.
- Science-room jobs: two a shift in the first week, one after: yes. Rec deck: two in the first week, none extra after: yes.

## Review
- **RV32: PASS on e96ec5a** (game bae8e769...456d, includes 43a96ae), 2026-11-06 ~09:35 UTC. Off: cadet_test ALL IDENTICAL;
  all four on: check_fast OK; a fresh save with the intro at 390x844, Days 0-6, showed science jobs Days 1-4 and rec deck
  jobs Days 2 and 4. Owners to review: section 15's two lines (Player engineer). Next: BM24 merges and switches on.

## Round items (lead 49, from RV33, after the PASS)
- **machine_check "food runs in live play"** (fails with CL1, EV1 or TB6 on): `JB3_FOOD_ON`. `leaveEnd` (meals) and `cartPost`
  ask `jb3MealsHeld(j)`: a food run is held for you only on your shift day and when its hour ends by your shift's end.
  Cause: Sunday's 16:00 run held to 17:00, the Works crew's shift ended then, nobody on 'work' till it lapsed at 20:00.
  Tested on staging-0997 8ed0635 + CL1 ba61507 + EV1 286ed5e, all 27 0.99.7 switches on: the food part passes.
- **"the ship meters: your jobs"** with the calendar on: not a missing mapping (the lead's guess). The job (in my run
  fix-oj-d3lounge-sofa@230, FX20's) maps fine; the ship's upkeep was 0 everywhere and the board 96 (machines 95.7), so a
  small job had nothing to show. Lead 49 chose the check: machine_check 5v now also leaves out a job finished when the
  ship's upkeep was already all done (sum < 1), its own "nothing left to show" rule. A check change, not a game change.
- **food_check "cake"** fails on that staging copy with and without JB3_FOOD_ON (Day 4 birthday cake): not mine, told the lead.
- **RV33: PASS on 1bbed58 (with 35ab083)**, 2026-11-06 ~12:06 UTC: off ALL IDENTICAL; on BM25's staging aef7c14 + this +
  CL1 + EV1 (31 switches) machine_check fails food runs without JB3_FOOD_ON and passes with it; a planted missing mapping
  still fails 5v, so the new exemption hides nothing real; food_check's cake is CL1's (fixed in CL1 bb26552). All five
  JB3 switches reviewed; BM25 switches them on.
