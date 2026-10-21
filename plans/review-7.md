# Review 7 (PR7): the crew-rotation patch and Dev mode Stops 1b and 2

Reviewer: PR7, session_01LyKAVtCEedL1bP73vqzu9v, for lead 23 (session_01XXiKm9iPgm565SZ4n1knmU). Branch claude/review-7 from claude/integration (3a48846).

Builders:
- PT1 (session_013KBHqs7JLoNRVFCVWdfngN, claude/patch-crew): the first crew rotation on Sunday Day 21 17:40, the "Off the Tern" tradition, ROT_TERN on; the opening camera ~10% closer.
- DB2 (session_01RAw82oHw329cHYC7wapKu8, claude/devmode-2): Dev mode Stop 1b (Traditions tab) and Stop 2 (Set career), plans/devmode-plan.html v3.1.

Method per turn: the diff read; cadet_test (what changes and why); check_fast; the area's checks; a live probe on a real save at phone size with reloads; mutants to prove the checks catch them. Probes and mutants in plans/review-7/.

## Verdicts

| Builder | What | Commit | Verdict |
|---|---|---|---|
| PT1 | T1: first rotation to Day 21; opening view closer | claude/patch-crew 1badd51 + e597de2 | PASS (doc fixes for T2) |
| DB2 | D5 Traditions tab | claude/devmode-2 d261274 | PASS |
| DB2 | D6a+D6b+D7 Set career, the Career tab | claude/devmode-2 261f7ad + d686b86 | PASS |
| RN1 (for lead 24) | opt #4 shaders kept | claude/opt-render 6fd3505 (game 8a9de48) | PASS |
| TS2 (for lead 24) | perf_check right rooms | claude/opt-tests c2a32e2 | PASS |

## Log

- 2026-10-21: started; told PT1 and DB2. Neither branch is on origin yet.

## TS2: perf_check right rooms (c2a32e2), PASS

- Test-only diff. perf_check (TS2's) on 0.64.8: every scene's three views stand in its room; the numbers equal plans/opt-measure.md's "with the fix" column, scene for scene.
- Mutant: the old `nearestOpen(tile)` call: 18 "you stand in" PROBLEMs (Machine shop, Fan hall, Bow lounge x2, Cabin 4-05, Gym), exit 1.
- Known, not TS2's: perf_check exits 1 on 0.64.8 for the +2 geometries on the third deck round trip (since 0.64.6).

## PT1 T1: first rotation to Day 21, opening camera 1.65/1.25 (1badd51, e597de2), PASS

- crew-roster-gen.py on the branch rebuilds the ROSTER block byte for byte.
- cadet_test 0.64.8 -> T1 with the camera line reverted: ALL IDENTICAL. With it: shots, mem/calls/tris, screen taps and steer walks differ (the same pixel lands elsewhere); deck data, paths, collisions, crew identical; no errors.
- day_check 20, 21, 22 OK; events_check OK; GitHub quick check on 1badd51 green.
- rot_probe.py (real save, 390 and 360, reloads at D20 21:00, D21 14:40/15:20/18:00, D22 08:00): state the same after each reload; Theo in moved once; Basil aboard; no errors. The keys a reload changes are the same on 0.64.8 (catch-up after a skip), so not the patch.
- Mutants: Basil aboard [35,null] (m1) and ROSTER_ROTATIONS day 35 (m2): events_check FAILs both; day_check 21 passes both.
- Doc fixes sent for T2: DEV_NOTES ~1182 (Days 35, 77...), plans/handover-sim.md, talk-pack-plan.md, work-pools-plan.md. Nit: ?seats labels show at zoom > 1.2 (landscape opening now 1.25), demo only.

## Log (cont.)

- D5's first devmode_check run used the integration copy of devmode_check.py (no 'trad' part), so its OK and the mutant d5_ma "OK" didn't count; rerun with d261274's devmode_check.py. Probes sign the arrival manifest first (it covered the sheet: my setup, not a game bug).
- D6a and D6b reviewed together on 39b2acd.
- RN1 (lead 24's asks): opt #4 shaders kept (6fd3505), perf_check event scenes (3af9f15). Early finding sent for the latter: switched() doesn't count `const NAME = true;` as on, so a switched-on feature's busy scene SKIPs.

## RN1 opt #4: shaders kept (6fd3505), PASS

- cadet_test 0.64.8 -> 6fd3505 ALL IDENTICAL; keep_shots.py 14/14 deck shots identical (programs 22 after lap 1; memory as old); deck_check OK; GitHub quick check green.
- keep_probe7.py (day, night, a week on, day again; 2 laps of 7 decks each): 22 programs from mid lap 1, none unkept, bounded. 0.64.8 at most 20 alive; mutant without usedTimes++ the same as 0.64.8.
- Section 12's one line reviewed for the HUD seat: fine.

## DB2 D5: the Traditions tab (d261274), PASS

- cadet_test 0.64.8 -> D5 (no #dev) ALL IDENTICAL; also with the DEVMODE guard removed from the eventsOn line (devmodeState() is null off).
- devmode_check (d261274's copy; my first run wrongly used integration's, without 'trad') OK incl. trad; events_check OK; check_fast OK 261 s.
- Mutants (trad part): tr not in SAVE_EXTRA, eventsOn hook removed, SHIP_DAYS not cleared: all FAIL.
- dm_trad_probe.py (real taps, 390 and 360, reloads): quiz in 20 minutes (17:25, 22 going), listed after a reload, Take me there to the Bow lounge, 22 at the quiz at 17:40 on the deck, Stop it restores Day 3's calendar, Undo brings it back, birthday whose by taps (38 going; quiz gives way), real keys untouched, no errors.
- The gives-way rule: agreed by lead 24.

## DB2 D6a + D6b + D7: Set career and the Career tab (261f7ad, d686b86), PASS

- Reviewed as one (D6a's runs hadn't started when D6b and D7 came).
- cadet_test 0.64.8 -> 261f7ad (no #dev) ALL IDENTICAL; check_fast OK 263 s; devmode_check (261f7ad's) OK with trad, set and career.
- Mutants, all FAIL: DM_CAREER m4 on Day 4; W.op not written; devmodeWeekMet skipped; devmodeFriends off; Officer by hand without PROMO.home; devmodeTestOpen without ladderOpen.
- dm_set_probe.py (taps; 390 Day 12, 360 Day 10): landing, rank, trainings, cabin 4-23, nothing asked, foot "approximate", worksClean's keys kept, the same after a reload, played to 19:00 with nothing re-opened, Undo, real keys untouched. Its "ship.works byte-equal" line was a timing artefact: a direct check shows the Dev save's ship.works byte-identical across a reload; a plain game's 'cases' moves on across a reload by itself.
- D7 nit (/2$/ in devmodeRank) fixed by DB2 in d686b86 (DM_PROMO_DONE), read.
- Design note to the lead: Set career to Day N = the end of day N (the plan's D6 test); the Day 9 and Day 10 beat shortcuts give the before-the-beat states.

- Lead 24 moved RN1's perf_check scenes (3af9f15 + 0ad9b5d), opt #10 (5358a60) and opt #6 (1a62fc7) to OR1 (session_015np4rHB2UHzet5Y1zFrBzm); my reading notes and planned runs sent to OR1. My node check of opt #6's reduction: 40M steps, 0 differ.
