# Handover: B3 (Step 5 builder, S5-4 shutdowns, mechanics seat B)

- **Role:** mechanics seat B for Pillar 5 Step 5, hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). My session: session_014FBmsiTsA9QymoN2qt4NyL. Planner: EP2 (session_01Hos4fCBxgEXxP8nR9E2iMq).
- **Branch:** `claude/p5s5-mech-b`, from `claude/p5s5-skeleton` 5957d244. Build-table rows `0.93.4-sd.1` to `sd.5`. The two build-number lines are untouched.
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs (db1313c1), piece S5-4. DEV_NOTES has a section "Shutdowns, M18".

## What I built (all behind `P5_M18`, under `P5_STEP5`; off = identical)
- Section 24w's slot: `SHUT_BRANCHES` / `sdBranches()`, the save `SHIP.works.sd` (`sdClean`, `sdPeek` read only, `sdData` makes it), `sdBook`, `sdCancel`, `sdSettle` (22:00), `sdMark` (jobs that need a shutdown), `sdPlanShut` (the planner hook), the planning screen (`sdView`, `sdAct`, `SD_UI` the live draft), `sdWarn`, Brennan's `sdChatButton` / `sdChatSay`, the training (`WORK_MECH.m18`, `sdStandIn`, `sdTrainReserve`, `sdBookedHook`, `sdTrainBeats`), the day (`sdDayTick`), `sdItems` (Schedule rows).
- One line each in others' sections (owners to review): section 14 `take()` (`sdPlanShut`, the sim engineer), section 15 `devDay` (`sdItems`, the device/player engineer), section 20 `chatShow` + `chatDo` (`sdChatButton`, `sd-tell`, the social engineer).
- Job slots reserved: 42 (the training's job), 43 (jobs marked for a shutdown).

## Judgement calls (overrule any)
- Branches: galley (Galley + Mess, keep Galley), gym (Gym + Laundry, keep Laundry) on 6-junction-1; junior (Junior common room + Music room, keep Music) and lounge (Bow lounge + Call booths, keep booths) on 6-junction-2; science (Survey lab, Sample lab, Observatory; keep Sample lab, Observatory) on 2-breaker-1 (and 2-junction-1); bridge (Observation room + Ready room, keep Ready room) on 1-junction-1; works (Tea corner + Machine shop, keep shop) on 5-inverter-1 (and Deck 5's batteries). Confirmed by B3 (no deck architect seat, lead 39): every room exists in its deck's map (checked in the game: DECKS[n].rooms), each junction is in its own utility room, and no branch holds a cabin, a washroom or a work station's own room except the galley (cooks keep working).
- Bookable starts 08:00-20:00 (there is no lunch; breakfast and dinner are the meal clashes). One hour long.
- A shutdown closes only places taken through `take()` (leisure, meals, traditions' crowd spots); people working there (the cooks) carry on.
- Question 3 (answered by the user, as recommended): "allowed, marked plainly, crew grumble". `SD_MEALS_OK = false` refuses clashing hours instead.
- The training is self-led (no "watch" step): Calder's talk at the junction, then the screen; she doesn't walk beside you to the device (worksEscort is 24 core's, and S5-2 owns its one line there).
- More than six affected: one "Post a ship notice" button warns all (kept as `all: true` on the booking).
- Reputation: done +2; Brennan not told in person -1; a meal/tradition hour -1; missed -3.

## Loose ends
- Not built: the junction room going dark (lead 39: skipped for Step 5, later polish).
- Words: every line is a stand-in through `worksText` keys `sd.*` and Calder's `train.m18.*` work lines; the head writer's `content/works/m18.lines` and a `train.m18` meeting replace them (the stand-in meeting is only made when neither exists).
- No Dev-mode preset yet (section 25 is the Dev mode seat's); controller_check and saves_check set the state up on paper instead.
- S5-6's P9 (a shutdown clash) can read `SHIP.works.sd` and `sdBranches()`. The section 14 hook is shared: `WORKS_PLAN_RULES` and `WORKS_SETTLE` (DEV_NOTES); proposed to B4, who may need a second hook to land a moved routine at an exact hour.
- Slots: the spec's slot table gives m18 slot 33; I use 42 and 43 (free), so 33 is released (told lead 39; EP2 archived).
- Words: the code uses SW3's keys where they exist (sd.tab, sd.job {machine}, sd.feeds.rooms, sd.who.n, sd.who.none, sd.prev, sd.next, sd.warn, sd.book, sd.cancel, sd.booked, sd.warn.ask, sd.notice, sd.ptr, sd.done, sd.missed, mail.sd.missed, mail.sd.settled, m18.ptr, m18.notice; Calder train.m18.follow.*; Brennan sd.warn.brennan, sd.grumble.brennan). My own keys (the leftovers) are written by me in `content/works/shutdowns.lines` (lead 39: no writer seat), baked; lines_check PASS. Not wired: SW3's crew bank kinds sd.off, sd.thanks, sd.grumble, sd.lapsed (the code's bubbles use sd.crew.* from shutdowns.lines).

## How to test
- Off: `cadet_test.py OLD NEW` ALL IDENTICAL; `bash check_fast.sh`.
- On (make `BUILD_ON` = a copy with `const P5_STEP5 = true;`): `mech_check.py BUILD_ON m18`; `saves_check.py BUILD shut`; `controller_check.py BUILD shut`; `DAY_SD=1080:galley day_check.py BUILD_ON 19`; `DAY_SD=1080:galley food_check.py BUILD_ON 19 2`.

## Gotchas
- `pgrep -f cadet_test.py` matches the waiting shell itself; wait on the background task instead.
- controller_check's touch half lists only what's on screen: part `shut` uses a tall page (h=2400).
- Don't run cadet_test alongside check_fast on 4 cores.

## State at the stopping point (lead 40, 2026-10-26)
- **S5-4 shutdowns:** `claude/p5s5-mech-b` 7e6bca4b (and this note on top). It holds RV20's FIXES NEEDED on 5ad090ff, all done (row 0.93.4-sd.10):
  - M2: Brennan only when the screen asked.
  - M3: the parts first; the power never stays off past the hour.
  - S1 and S2.
  - M1 (Calder at the 09:15 talk) is 24 core's teacher fix, from B5.
- **Also in that sha:**
  - B1's claude/p5s5-career 51b1a9c6 merged (the ladder order).
  - B4's p9ShutClash hook on the screen (sd.11).
- **Checks:** off: cadet_test ALL IDENTICAL, check_fast OK. On: mech m18, saves shut and controller shut all OK.
- **Waiting:** RV20's re-review of 7e6bca4b. B4 tests P9 on a merge.
- **S5-5 the sensor array:** `claude/p5s5-m20` 989b1759; see plans/handover-b3-m20.md there. RV21 PASSed it with 4 shoulds, all done; awaiting RV21's re-check.
- **Nothing else open.** The shared section 14 hook (p9PlanRule / p9Settle by name, WORKS_PLAN_RULES / WORKS_SETTLE) is in DEV_NOTES "Shutdowns, M18".
- **RV20 PASS on fa1e152c** (2026-10-27 00:45 UTC; notes claude/review-rv20 eb95b418). Its one should (the parts text's missing space) is fixed in `sdParts` (row sd.12). Note from RV20: with B1's 51b1a9c6 merged, machine_check on the switched-on copy fails until B5's fix lands (not this piece's).

## State for the move to the new account (lead 40, 2026-10-27)
Everything is pushed. Nothing is half done.
- **S5-4 shutdowns** (`claude/p5s5-mech-b` 98460d79) and **S5-5 the sensor array** (`claude/p5s5-m20` 247420aa, RV22 PASS): both merged by BM18 into `claude/staging-0.94.0`. The M20 note is `plans/handover-b3-m20.md` on claude/p5s5-m20.
- **Talk up close** (`claude/talk-close` f52e2abc, from staging-0.94.0 ac810e7e; the user via lead 40). A normal change, no switch. You can still tap anyone, but if you're more than `TALK_NEAR` (2.5) away the card only says what they're doing and where ("Pell is at work in the Works bay. Walk over to talk.") with one button, Walk over; it walks you beside them and the talk options open when you get there. Code in section 20 (`TALK_NEAR`, `DOING_WORD`, `chatDoing`, `chatWalk`, the `far` mode in chatOpen/chatShow/chatDo/chatTick) and section 10 (tapCrew and the seek chip pass `{ tap: true }`; far taps don't stop or turn the person). Design decision in design-doc.md ("You talk to people up close", 2026-10-27), DEV_NOTES "Talking up close", build-table row talk-close. Checks: interactions, player, arrows week guide, check_fast all OK. controller_check part ending has 4 FAILs, the same on the base ac810e7e (old, not from this). **Waiting:** RV22's review, then BM18's merge.
- **Training titles** (`claude/train-titles` 7ce89d56, from staging-0.94.0 64a1ba76; lead 40, RV22). 24 core's titles named the teacher with `worksFirst` (Ines) while the arrows used `guideWho` (Calder for the stand-in). Now `guideWho` in six spots: the lesson-clash warning, trainOffer's title, trainArrow's label, arrOffer's title, and worksNext's two lines ("Calder will show you..."). Checks: check_fast OK, cadet_test ALL IDENTICAL (switch off), mech m19/m20 OK. career_check FAILs only "busy: Relied on before Day 5", the same on the base (backlog rows 12 and FX28-1). **Waiting:** RV22's review, then BM18's merge.
- **24 core for Step 5** is mine since B5 was archived: read `plans/handover-b5.md` on claude/p5s5-promo 9c90616c first.
- **Next for this seat:** earmarked for Step 6; nothing started.
