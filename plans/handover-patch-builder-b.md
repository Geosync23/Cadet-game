# Handover: patch builder B (PB), 2026-10-20

**Role.** Sim engineer for the playtest patch (`plans/patch-plan.html`, final): I own sections 13, 14 and 10 (ship time and saving, the crew's schedules, the crew walking). My new code is in the slot `// ---- slot: Sim engineer (section 14)`. I report to lead 22 (session_01BGQCZLK6gYTnqu6mwZ61jB; lead 21 handed over 2026-10-21). PR2 (session_013ttt3gV3DaF9y4caBtFnh9) reviews the patch, and OR1 (session_01W7AHxrcgBM3rJNtCFKwp9W) stands in for the section owners.

**Branch.** `claude/patch-b`, from `claude/integration` 0.64.4 (merged in). I haven't changed the build number. check_fast was OK on every push.

## Done
- **Batch D**, reviewed and passed by PR2 and OR1:
  - #7: the Captain's music habit dropped through `plans/crew-roster-gen.py`; her other-evening chance is now .15. The generator first had to be brought in line with hand edits made to section 9.
  - #9: a toilet trip's walk (`walkLead`, 1.6 times the straight line) is taken out of the end of the activity before it, at most half of it; nearest stall first.
  - #10: crew step out of the lift one at a time; a walker closing on someone ahead going the same way takes their pace; each walker has a drawn-only lane (`walkGap`, `walkLaneStep`, `liftOutOk`).
  - #8: the stall's red cap (`stallCapAdd` and `stallCapsTick`; hook 1d8d606 in 4b).
  - Details: DEV_NOTES "The playtest patch, batch D".
- **Batch F**, passed by PR2 and OR1:
  - #16: `JOB_PACE` .72 on your machine jobs.
  - #20: `WORK_HUNGER` 3 an hour extra at work.
  - #22: social drains [3, .25].
  - #27: `SLEEP_TAPER` [90, 1/3].
  - Hook: 22c4442 (17, the job board). 9e34423 (24, Tier 1 "Relied on" 40 -> 48) was REVERTED: its reason was wrong (see below).
  - machine_check now allows 3-7 jobs a shift (6.0 before batch F, 6.2 after). player_check's paper week has company at meals and chats.
  - Details: DEV_NOTES "The playtest patch, batch F".
- **#10 follow-up** 6c7be04: the escort and walk-up steps ease the drawn lane to the middle.
- **#31** 95c22e7 and the reason commit: "Ask Zeke" parked behind `INTRO_ASK_ON = false` (section 21, PA's); intro_check part 8 flipped; design-doc's arrival paragraph marks it cut, with the user's reason. Waiting on PR2's review.

## Owner reviews I gave (PA's claude/patch-a)
- 47b3dba: OK.
- 155f0d4: OK.
- 6e9e86d: OK with one fix, `if (mine == null || mine === pl.id) continue;` in the schedDesks trade.

## Gotchas
- **Toilet walks:** don't push a toilet visit later. That made days end past midnight, a tradition overrun, and day_check's rec-deck comparison (Deck 3 must never hold fewer people with the rec deck than without, minute by minute) fail by one person. The basin step after the toilet has no walk of its own: giving it one ate the toilet visit.
- **Probes:** `plans/patch-plan-probes/c9c.py`, `c10c.py` and `c8d.py`. They skip drawing (`window.__skip = true`); with rendering on they take more than 20 minutes each.
- **Running checks:** at most 2-3 checks at once on this 4-core box, or pages time out loading (a `Page.goto` timeout is load, not a real failure). Give each check its own `CADET_WORK`.
- **Killing probes:** never `pkill -f <pattern>` when the pattern appears in your own command line; it kills the shell.
- **Timing the game:** the test harness clock is virtual, so `performance.now()` timings read 0. Count the operations instead.

## Loose ends
- **Optional (#9):** more crew go to the toilet after waking (.5 -> .7). Not done.
- **Reputation pace (backlog rows 12 and 17):** the busy player's early "Trusted" (Day 3) and "Relied on" (Day 4) predate batch F; the user will balance them later. career_check FAILs on row 12 by the user's decision: don't "fix" it. JOB_PACE doesn't speed reputation up much: career_check's paper players don't time jobs (identical points a day before and after F), and in timed play a steady player does 6.0 jobs a shift day before F, 6.2 after, because the board's work is the limit.
- **Dev mode:** the "Set career" table should be re-measured after batch F.

## Heads-up from the events engineer (EV1, claude/events-base, 2026-10-20)
Nothing to do yet. Once `EVENTS_ON` is switched on (with the storm update, after the user's review):
- The ion storm starts on Day 11, not Day 10 (a fixed calendar, `EV_CALENDAR` in section 18). Its phases, meetings and news can wait out a held hour: every Friday 15:30-17:00 from Day 5 (the Captain's address).
- New gatherings (the lantern supper, the Line ceremony and supper, the comet) reach section 14's planner the same way the all-clear party does: `EV_SHIPWIDE` → `evTable`/`eventsOn`, each with its own hash key.
- Switched off, it is all byte-identical to 0.64.5.
- `eventFree` (section 14) is shared between the Fridays plan's part A (the 15:30 Friday end) and the storm update: neither should change it without the other.

## Owner reviews since (2026-10-21)
- FR1's Short Fridays hooks ffb3b98 (claude/fridays): OK. Suggested, not required: pick the Friday skeleton per day from crew aboard on that day, so it survives crew rotations.
- EV1's event-meetings hook (F0b, after 0.64.7): shape agreed, and EV1 writes it.
  - gatherings() adds event meetings inside EVENTS_ON.
  - A meeting during the shift is a 'meet' break in shiftWithBreaks, counted as work in dayReport by its exact tag.
  - Who goes comes from the calendar only, plus a skip list that is set once and never changes; shipDay's cache must change if the list is (re)set.
  - To review when it arrives.
- Backlog #18 (day_check Day 12, the rec deck guard) fails the same way on 0.64.4, so it isn't from this patch.
