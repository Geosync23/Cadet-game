# Handover: SC1 (breakfast at 07:00, then dinner spread)

Written by SC1 (session_01BBC5dx3LtPPiWkTdurPTmJ), 2026-10-23, at about 63% memory; brought up to date at about 66%, when SC1 stood by. Report to the current lead (lead 31, session_0118SXBCdg87nDiXdtrGNVSR, at the time of writing). Reviewer: RV8 (session_01Q6uHYWus4ncyEgqWEYhJh5).

## Branches and builds

- **claude/patch-play1-f**: playtest patch 1 note 18 (breakfast at 07:00), merged as 0.64.17, then rolled back (2cabe96b) at the user's request. Kept for history; don't build on it.
- **claude/breakfast-back** (from claude/integration 989fd566, 0.91.0): 2b81d8a0 reverts the rollback (brings back exactly 0.64.17: breakfast, the m12 fixture, the Line supper tradMeal fix, CP4's bubble-slide cap); 0cd37b1b makes interactions_check close device tips before its lift-panel tap. RV8 PASS (02:51). All my checks green (see the build table rows "breakfast-back").
- **claude/dinner-spread** (from breakfast-back): 0672133b spreads the leaving at meal traditions (section 14: `tradLeave`, `tradStay`, `evening()`'s `mt` line); a879ab27 merges breakfast-back's tip fix; 022724a4 reads Day 0's goodnight through `introStepById('free')`; ed6bcbf3 (the tip sent to RV8): never past the tradition's end (who'd overrun leaves in its last 12 minutes), `by` at least the end, and Day 0's seat past 19:00 split off as an ordinary dinner. All green; with RV8.

## What I built (plain words)

- **Breakfast 07:00-09:00** (section 14 `MEALS`, `morning()`, the night shift's block; section 16 `GALLEY_SHIFTS`, `FOOD.open`, `galleyPlan`). The crew's wake stays 05:30-07:15. The night shift comes off at 06:00, unwinds in the Deck 3 lounge, eats from 07:00, then showers and sleeps. The galley's early hands still start at 05:30: prep, cook with the chef 06:00-06:30, bake, then the line from 07:00.
- **tradMeal's walk** (section 14): a long walk to the servery line sets off earlier so the least time seated fits (the Line supper standing fix).
- **Dinner spread** (section 14): each diner at a meal tradition keeps their seat for their own meal plus a linger, 35-75 minutes from sitting (by seed, `U(531)`), never past the tradition's end (who'd overrun leaves in its last 12 minutes, `U(533)`; a first try allowed 20 minutes past it and broke events_check and the Line supper's seated sittings); `evening()` ends their dinner block at that same minute so `linger()` doesn't stretch the seat to a shared end. Day 0's Sunday table: seats kept until Zeke's goodnight (`introStepById('free').at`, a fixed minute: plans never read live records), then everyone leaves over the next 25 minutes (`U(532)`).

## Numbers (on paper, the crew's plans)

- Worst minute of departures, 0.91.0 -> dinner-spread: spice-shelf supper 22 -> 5; tasting table 22 -> 3; ordinary Sunday table 7 -> 6 (24 -> 17 in 5 min). Ordinary dinners and breakfasts were already spread (2-4 a minute); the worst breakfast minute (8 at 09:00 on Day 1) is the day shift leaving for work.
- Day 0 with DS1's 17:15 arrival (`free` at 1185, 19:45): the table is full (48) from 18:20 to 19:30, then thins 19:35-20:05. With today's 19:00 goodnight: full 18:20-18:50, thins 18:55-19:20.

## Loose ends

- RV8's review of dinner-spread ed6bcbf3 (cut-off 07:00 UTC for the combined morning build); breakfast-back already PASSED.
- DS1's claude/zeke-tour (17:15 arrival) merges onto breakfast-back/dinner-spread; DS1 will merge, not rebase.
- FX5 has the player-facing fix for tip cards covering the lift panel the arrow points at.
- Day 0: in play (DS1's zeke-tour 99687fc8, 17:15 arrival) you sit at 18:17 and the goodnight comes at 18:20, the Chief about 18:26, Tomas 18:41; but the plans use the latest minute (19:45), so the table stays full about an hour after you're free. That guarantees "full while you're there"; if the user wants them gone sooner after the goodnight, the plans need an earlier fixed minute.

## How to test

Setup: plans/testing-guide.md section 2. My round script and probes are in my scratchpad (not in the repo). Checks used: check_fast, food_check 11 4 and 1 7, day_check 0 1 5 7 (and the event days), intro_check --week, interactions_check, bubble_check, events_check, bigevents_check, mech_check, perf_check with PERF_SCENES='Line ceremony', cadet_test alone (old vs new; to prove a difference is only the schedule, put sections 14 and 16 back to the old build's in a copy: ALL IDENTICAL).
