# Handover: dinner-wait investigator (FD1)

**Role:** found why `food_check.py BUILD 11 4` failed dinner waits after the Fridays merge into claude/storm-update, and fixed it. Lead 24. Done; idle.

**Branch:** `claude/food-waits`, from `claude/integration` f782c5d. Commits 0f808c3 (food_check, backlog row 20, renumbered 22 by BM12) and 2ad7db8 (build-table row), plus this note. Check-only: the game file is unchanged. PB reviewed it (OK). BM12 merged it (2ad7db8) into the 0.64.10 candidate; food_check 11 4 OK there.

## The cause
- The first bad commit is 4ee3fdc (integration 0.64.7 merged into claude/fridays), which reached storm-update through 4311ffe. PR6's bisect found it too. The trigger is `FLC_ON = true` (First Light Cocoa): the tip with only FLC_ON false gives adb71aa's result. LADDER_ON and MUG_ON play no part.
- First Light Cocoa moves about 40 people's Day 1 evenings. Machine wear differs by hundredths and snowballs. By Day 11 at about 08:00, `3-range-1` faults as well as `3-oven-2`. `shipEffectsAt(3, m).cook` is then 1.24, so 30 portions are ready at 17:00 instead of 40, and queues form.
- food_check's live visits (Deck 3 at Day 11 18:00 in part 4, and the menu board in 4d) run `machinesNow` up to then. `histHour` clamps every later hour to the last recorded one, so the forecasts in 4b (carts), 4c (chiller) and 4e (28 days) ran with both cookers faulty for weeks. Part 1 runs before the visits, so it read Day 1's machines and passed.

## The fix
- `fresh()` in food_check: `setShipNow(T0); machinesNow()`, where T0 is the load time. A clock earlier than the machines' record starts them afresh (`machinesReset`: jobs, MACH_HIST, and plans that read `recAt`). It's called before 4b, 4c and 4e. 4c also runs the machines to 09:30 before catching Mail, otherwise the stores' "Out of filters" Mail is mail[0].
- Follow-up (lead 24, EV7's garden carry FAIL with the Line on): `fresh()` also before 4k (the garden reads the machines' record: irrigation, grow lights). FD1 couldn't reproduce EV7's FAIL (line-update c9fa161 with EVENTS_ON and EV_LINE_ON true passes 1 7 with the old check too), so it's a precaution: with it, off 1 7 output is identical to before, off 11 4 OK, Line-on 1 7 and 11 4 OK, check_fast OK. If EV7's FAIL still shows, ask EV7 for the exact copy recipe.
- Gotcha (PB): the rewind clears jobs from earlier parts. Any new forecast part added after 4e must call `fresh()` itself.

## Proof
- integration f782c5d, 11 4: 17 FAILs before the fix, OK after.
- Storm tip 88bd57c with events on: food_check 11 4 and 1 7 OK; day_check Days 12 and 14 OK; events_check (storm's own copy) OK.
- Events off, 1 7: output identical to before the fix.
- check_fast: OK.

## Loose ends
- Backlog row 22 (was 20 on this branch): the cookers fault every 2-4 days, and with the machines run for real, Days 11-24 on the storm tip have 7 dinners with 10-36 minute queues (adb71aa: 1). It's a design call for the galley and systems seats (fault frequency vs "meals run late"). The user hasn't been asked yet.
- A fresh container needs `/tmp/cadet-work/three` (DEV_NOTES) and `/tmp/cadet-work/acorn` (`npm pack acorn`, then untar) for check_fast.
- Gotcha: don't switch branches while a check runs from the repo folder. It picks up the other branch's check files (events_check failed on DIALOGUE_EL that way).

Probe scripts (galleyReport after a Deck 3 fill, machine history hour by hour, a planDay diff between builds) were in FD1's scratchpad and are not kept.
