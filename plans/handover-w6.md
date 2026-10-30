# Handover: W6 (the Works career engineer for Pillar 5 Step 6)

- **Role:** Works career engineer for Step 6, hired by lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). My session: session_01GKuymmTEpqHLycbYTJwRQn.
- **Branch:** `claude/p5s6-core`, from `claude/staging-0.94.0` 07e033c9. Build-table rows `0.94.0-s6.N`. The two build-number lines are never touched.
- **Spec:** `plans/p5-step6-spec.html` on claude/p5-specs (version 2; the user's answers all "recommended"). Read with the Step 5 spec, `plans/handover-b5.md` (claude/p5s5-promo) and `plans/handover-b3.md` (claude/p5s5-mech-b): 24 core and 24u are mine now.
- **Overnight rules (lead 41, plans/overnight-decisions-lead41.md on claude/lead-41-e86n0x):** the user is asleep; at most 5 seats working at once; at most two browser checks at a time (check_fast is already two).

## Done: the first turn (spec section 6, row First), all off
- Section 13: `P5_STEP6` and its nine sub-switches (P5_NIGHT, P5_M21, P5_PROMO4, P5_DECK6, P5_M23, P5_M24, P5_M25, P5_CASES6, P5_END).
- Section 24 core: `if (P5_STEP6)` block with the ladder rows m22, m21, t4, m23, p6, p7, m24, p8, m25 and a stand-in `WORK_BANDS[4]`.
- Section 18: Step 6's held hours (p5Briefing, tier4Test, deck2Move, mentoring) inside Step 5's block.
- Section 28 (new, after 24x): `P5_NIGHTS`, `P5_LEAVE`, `p5NightOf`, `p5NightAt`, and the slots 28, 28a-28f.
- tools/affected.py (days 23-26; RULES 28-28f), cov_run.sh, testing-guide's event days, owners.md, map.md, DEV_NOTES.

## Judgement calls (overrule any)
- m22 (the night shift) is tier 1 with `rank: null`, since it's "any rank".
- p6, p7, p8 are tier 4 (they ride on the Engine Specialist's nights and Day 25); S6-8 may change it.
- p8's teacher is a stand-in (Halloran, Torres): the roster has no machine shop tech.
- WORK_BANDS[4] = [0, 16, 34, 60, 85]: a stand-in, only shown.

## Next for this seat (after 0.94.0 is published)
- Wave 1: S6-3's day parts in 24u (the offer, the test t4 slot 26, the badge, the move).
- Wave 2: S6-3's night parts (the comet 22:40, the welcome), then S6-7 mentoring (28e). End: S6-9 (28f).

## Gotchas
- `P5_NIGHTS` and `P5_LEAVE` are consts in section 28, after sections 13-24 in the file: read them only once the game runs (a const read before its line throws, even inside `typeof`).
- day_check on the on copy: make it with `const P5_STEP5 = true;` and `const P5_STEP6 = P5_STEP5 && true;`.

## Done for lead 41 between Step 6 turns (2026-10-27, all merged or with BM19)
- `claude/talk-close-fix` 6dfc4ec1: a far talk card closes when you move off or after 10 s; no full card unasked (RV23 PASS, in staging 9faaee80).
- `claude/career-check-pick` 4cb6d37b: career_check's paper player makes the pick on M19's jobs (backlog W6-1); mech_check skips t3 like t2 (W6-2). Merged.
- `claude/vessel-words` 0f8a2406: four Veyli vessel lines cut to 90 characters or less.
- `claude/check-offcopies` 00161062: arrows_check's follower closes a device a nearby tap opened (the week stall at the wobbly stool, by the Old mysteries board); mech_check ps's stand-in Calder first in DECK_CREW; events_check's vessel-off and promo_beats t3off on off copies.

## Notes for S6-3 and later
- **mech_check row_check:** add t4 beside t2 and t3 (24u's test job is no training) when S6-3 registers WORK_MECH.t4.
- **Dev mode:** devmodeNextTraining (section 25) doesn't check WORK_MECH, so with Step 6 on before its pieces land it could offer m22 (RV23's note).
- **career_check's paper player** now answers pick stops; a new pick-style job needs `j.bad` (or options that accept one in turn).
- Checks run on a switched-on build since 0.94.0: make off parts run on an off copy (`= true;` line swapped), as BM19's sweep did.

## S6-3 state (W6, 2026-10-27, handing over at about 60% memory)
- **Branch:** `claude/p5s6-promo4` from `claude/staging-p5s6` 64e296df (0.94.0 + the first turn). Rows `0.94.0-s6.2` (turn 1, d40a95ee) and `0.94.0-s6.3` (turn 2, bfcebb6d). Sent to lead 41 and RV23 (session_01GKuymoDm1XbC5G8TvaCNLr); no verdict yet.
- **Turn 1 (done): the offer.** 24u after S5-2's code: `PU4`, `PU4_LIVE`, `puT4`, `pu4Clean` (puClean keeps `pu.t4`), `pu4Set`, `pu4Ready`, `pu4TestDay`, `pu4Script` (stand-in pu4.offer / .dinner), `pu4Offered`, `pu4OfferTick` (workday from 08:00 after any held hour; Saturday nothing; Sunday from 18:00 = dinner; 22:00 by Mail), `pu4Escort` (in p5Escort), `pu4NearTick` (Torres at Trusted), `pu4BeatsTick` (friends' Mail 20:00 the evening before), `pu4Check` / `pu4RepUp` / `pu4Next` / `pu4Items` (called from puCheck, puRepUp, puNext, puItems). Dev mode's devmodeNextTraining skips rows with no WORK_MECH; mech_check skips t4.
- **Turn 2 (done): the test.** `PU4_T`, `pu4Coil` (worst of 6-coil-1..3), `pu4Place` (panelPlace when S6-4 adds panels, else `6-engine-N`), `pu4Stops` (fetch, isolate, read, wind, cycle), `pu4StepDone`, `pu4JobDone`, `pu4MakeJob` (slot 26), `pu4Passed` (W.tr.t4; 24 core worksDone asks), `pu4Delay` (again in 2 workdays), `pu4TestGuide`, `pu4TestBeats` (Torres waits by crewScene), `WORK_MECH.t4`, jobKindAdd('tier4'). Outside 24u: worksDone, trainTick `/^t[234]$/`, 15b BOARD_KINDS and boardLessonName.
- **Checks:** `promo_beats_check.py BUILD t4off`; on ON6 (a copy with `const P5_STEP6 = P5_STEP5 && true;`): `t4before t4test t3passed`; `mech_check.py ON6 t3 t4 m19`; cadet_test vs 64e296df ALL IDENTICAL; check_fast OK.

## S6-3 still to do (turns 3 and 4, spec piece S6-3)
- **Turn 3, the result and the badge.** The result is said on the walk down at 22:40 on Day 22 (night part, wave 2, with S6-1's nights). For wave 1 a fallback is enough: with the night parts not built, at 22:40 a notice plus `pu4Promote(now)` (tier 4, rank 'specialist', W.xp 0, W.ms ['specialist', d], newsAdd, simNote('promoted', { tier: 4 })), mirroring `puPromote`. The badge: Tuesday Day 23 16:30, the observation room (an `OCCASIONS.pu4Badge` like `pu3Bar`, promoCerTimes, promoGuests; Calder, Torres, Vance; script pu4.badge, the pin pose), the invite notice as you wake, 16:00 "Go now", a level 1 arrow from 16:15; if you sleep through it the Captain waits until your next waking afternoon; Calder says there that your Deck 2 quarters are ready for Thursday, then her Mail. "Senior Officer, Engine Specialist" on the Record (worksRecordHead). The EV_BEATS hold engineSpecialist is Day 23 16:15-17:10.
- **Turn 4, the move and Dev mode.** Thursday Day 25: Calder's Mail at 17:00; after dinner (once you leave the mess, or 20:00) Vance walks you up to room B on Deck 2 (24p's promoBeatsWalkWait / promoMoveEscort pattern; hold deck2Move 19:00-22:00); open till 22:00, then the next day at the shift's end. `SHIP.works.home = '2-B'` (worksHome, worksHomeOpen in 24p, cabinMine in 24t learn it), 4-23 back to "Spare 4-23", laundry collected (21b, onboarding engineer reviews). The refit odd job from Day 23 (one row in section 17's odd-jobs table, systems engineer reviews). Dev mode: puDevSteps / puDevNext for Tier 4 and presets Days 21-26 (section 25). promo_beats_check parts t4passed, t4comet, t4welcome, t4badge, t4move.
- Words are stand-ins (`pu4.*`, `train.t4.*`); the head writer's promo-t4.lines replace them.
