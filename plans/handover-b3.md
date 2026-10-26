# Handover: B3 (Step 5 builder, S5-4 shutdowns, mechanics seat B)

- **Role:** mechanics seat B for Pillar 5 Step 5, hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). My session: session_014FBmsiTsA9QymoN2qt4NyL. Planner: EP2 (session_01Hos4fCBxgEXxP8nR9E2iMq).
- **Branch:** `claude/p5s5-mech-b`, from `claude/p5s5-skeleton` 5957d244. Build-table rows `0.93.4-sd.1` to `sd.5`. The two build-number lines are untouched.
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs (db1313c1), piece S5-4. DEV_NOTES has a section "Shutdowns, M18".

## What I built (all behind `P5_M18`, under `P5_STEP5`; off = identical)
- Section 24w's slot: `SHUT_BRANCHES` / `sdBranches()`, the save `SHIP.works.sd` (`sdClean`, `sdPeek` read only, `sdData` makes it), `sdBook`, `sdCancel`, `sdSettle` (22:00), `sdMark` (jobs that need a shutdown), `sdPlanShut` (the planner hook), the planning screen (`sdView`, `sdAct`, `SD_UI` the live draft), `sdWarn`, Brennan's `sdChatButton` / `sdChatSay`, the training (`WORK_MECH.m18`, `sdStandIn`, `sdTrainReserve`, `sdBookedHook`, `sdTrainBeats`), the day (`sdDayTick`), `sdItems` (Schedule rows).
- One line each in others' sections (owners to review): section 14 `take()` (`sdPlanShut`, the sim engineer), section 15 `devDay` (`sdItems`, the device/player engineer), section 20 `chatShow` + `chatDo` (`sdChatButton`, `sd-tell`, the social engineer).
- Job slots reserved: 42 (the training's job), 43 (jobs marked for a shutdown).

## Judgement calls (overrule any)
- Branches: galley (Galley + Mess, keep Galley), gym (Gym + Laundry, keep Laundry) on 6-junction-1; junior (Junior common room + Music room, keep Music) and lounge (Bow lounge + Call booths, keep booths) on 6-junction-2; science (Survey lab, Sample lab, Observatory; keep Sample lab, Observatory) on 2-breaker-1 (and 2-junction-1); bridge (Observation room + Ready room, keep Ready room) on 1-junction-1; works (Tea corner + Machine shop, keep shop) on 5-inverter-1 (and Deck 5's batteries). Not yet agreed with the deck architect.
- Bookable starts 08:00-20:00 (there is no lunch; breakfast and dinner are the meal clashes). One hour long.
- A shutdown closes only places taken through `take()` (leisure, meals, traditions' crowd spots); people working there (the cooks) carry on.
- Question 3 (unanswered): "allowed, marked plainly, crew grumble". `SD_MEALS_OK = false` refuses clashing hours instead.
- The training is self-led (no "watch" step): Calder's talk at the junction, then the screen; she doesn't walk beside you to the device (worksEscort is 24 core's, and S5-2 owns its one line there).
- More than six affected: one "Post a ship notice" button warns all (kept as `all: true` on the booking).
- Reputation: done +2; Brennan not told in person -1; a meal/tradition hour -1; missed -3.

## Loose ends
- Not built: the junction room going dark (needs per-room lighting; draw-call and pixel risk; the performance engineer's call).
- Words: every line is a stand-in through `worksText` keys `sd.*` and Calder's `train.m18.*` work lines; the head writer's `content/works/m18.lines` and a `train.m18` meeting replace them (the stand-in meeting is only made when neither exists).
- No Dev-mode preset yet (section 25 is the Dev mode seat's); controller_check and saves_check set the state up on paper instead.
- S5-6's P9 (a shutdown clash) can read `SHIP.works.sd` and `sdBranches()`.

## How to test
- Off: `cadet_test.py OLD NEW` ALL IDENTICAL; `bash check_fast.sh`.
- On (make `BUILD_ON` = a copy with `const P5_STEP5 = true;`): `mech_check.py BUILD_ON m18`; `saves_check.py BUILD shut`; `controller_check.py BUILD shut`; `DAY_SD=1080:galley day_check.py BUILD_ON 19`; `DAY_SD=1080:galley food_check.py BUILD_ON 19 2`.

## Gotchas
- `pgrep -f cadet_test.py` matches the waiting shell itself; wait on the background task instead.
- controller_check's touch half lists only what's on screen: part `shut` uses a tall page (h=2400).
- Don't run cadet_test alongside check_fast on 4 cores.
