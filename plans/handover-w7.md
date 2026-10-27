# Handover: W7 (the Works career engineer for Pillar 5 Step 6, after W6)

- **Role:** Works career engineer for Step 6, for lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). Reviewer RV23 (session_01GKuymoDm1XbC5G8TvaCNLr), build master BM19 (session_01GKuymncYhRTKs8t4byNfdj). My session: session_01GKuymjghu82TGWPLR1wTKw.
- **Read first:** plans/handover-w6.md (what W6 built: turns 1-2 of S6-3, the first turn of Step 6), the spec `plans/p5-step6-spec.html` on claude/p5-specs.
- **I own:** S6-3 turns 3-4, S6-7 mentoring Basil (28e), S6-9 the end (28f); section 28's shared helpers, 24u, 24 core, the Step 6 switch lines. Other seats ask me before touching them.
- **Branch:** `claude/p5s6-promo4`. Rows `0.94.0-s6.N`. Never touch the two build-number lines.
- **Overnight:** the user is asleep; the spec's recommended answers; at most two browser checks at once.

## Done
- **Turn 3 (s6.4):** the result at 22:40 and the Captain's badge (see DEV_NOTES "The Engine Specialist promotion", Turn 3).
- **Turn 4a (s6.5):** the move to 2-B with Vance after dinner, laundry collected (DEV_NOTES Turn 4a).
- **Turn 4b (s6.6):** Dev mode (career table, four presets, steps, arrow), forYou's engine line.
- **Wave 2 (s6.7):** the 22:40 fetch and walk down (with N6's nights: pu4Fetches), the crews' welcome; the follow-escort fix (section 10; live fix on claude/escort-follow-fix cffe8187).
- **S6-7 turn 1 (s6.9):** Basil's day settled at 22:00 (SHIP.works.mt), section 14's mtDesk hook, mtPlanRule, notices, row, arrow. 
- **S6-7 turn 2 (s6.10):** hello, he watches you (mtEscort follow) through a turned-in job, you watch him at 5-bench-2 (steps.dw).
- **S6-7 turn 3 (s6.11):** the stuck clue (stand-in dialogue; calls PZ6's caseMentorOpen({ day, onPick(id, key) }) if it exists: asked PZ6 for the real shape), the late talk.
- **S6-7 turn 4 (s6.12):** Calder's first job alone (mtDone: tr.m25, ms mentor, Record line), Dev preset 'mt', controller part mentor. Left for S6-7: PZ6's real caseMentorOpen (the stand-in dialogue until then); day_check Day 26; stories_check (Basil).
- Approved MA6's 24 core touch in 27166be (WORK_MECH.m21.own skipped by ladderTick).

## Judgement calls (overrule any)
- The result is said where Calder finds you (pu4.stairs as a talk), not yet literally on the stairs; with P5_NIGHT on she then leads you to the engine room. N6 starts night 1 only with P5_PROMO4 off (their turn 3).
- No new engine-badge mesh on the collar (the kit's pip/bar stays); the certificate goes on the shelf.
- Badge guests are fixed (Vance, Calder, Torres): no friends, as the spec names only them.
- The Record's title: "Engine Specialist" alone (never "Engine Specialist · Specialist").

## Still to do (for W8; state at claude/p5s6-promo4 36e8cf5a + this note)
- **Merge first:** claude/staging-p5s6 has moved (b472fa1a M24, d39b87a6 DA6's S6-4, a2ef6416 S6-6 turn 2); merge it in before your first push. controller_check ALL_PARTS ends ... 'm21', 'm24' (my promo3/promo4/mentor parts are appended by PART_FN lines at the end).
- **S6-7 (done, 4 turns, 28e):** RV23 PASS on 9d24b9f9 (turn 1); turns 2-4 (3cb048f2, 66d35044, 92e5b38f) queued with RV23. One swap left: the stuck clue's stand-in dialogue (mt.clue) for PZ6's `casePoint` (claude/p5s6-puzzles 91710ce, pushed): `if (typeof casePoint === 'function' && casePoint({ by: 'basil', seed, onPick: (clueId, isKey) => mtClueDone(String(clueId), shipNow()), onClose: () => {} })) { shown } else { stand-in }`. Seed: e.g. `schedU(machSeed('m25'), day, 894) * 4294967296 | 0` (no R()). Replace the typeof caseMentorOpen call in mtTick3 (it never existed); keep MT_LIVE.case so it opens once; maybe keep isKey in mt.steps or a flag. controller_check s6cases already reaches "Point to" by pad.
- **S6-9 the end (28f, 2 turns, spec S6-9):** Friday Day 26 Four weeks aboard (18:40-19:30, Works tea corner, Deck 5): cake, Calder's story moment, she sits beside you (sit pose) and asks what you want next; SHIP.works.end = { answer, day } (restore after worksClean at load like mt), shown on the Record (24 core worksRecordHead, mine); Calder's Mail the evening before; milestones in W.ms (specialist, nights, mentor, the question); a last page in the Works app; the tradition's scene hook is section 18 (traditions engineer reviews: a typeof-guarded call at its end). EV_BEATS hold caldersQuestion Day 26 18:40-19:30 exists.
- **All Step 6 DM_CAREER rows (section 25), I'm the one owner (lead 41):** done so far: Day 22 t4/promo4. To add: m21 (MA6: W.tr.m21 = 22; SHIP.works.side.m21 = { first: 22, last: 22, pick, order, got, sd }; own row), m22 nights (N6: SHIP.works.ns[22..24] = { in, out, jobs, inc, late }), m23 (S6-5, ask its seat), m24 (MA6: W.tr.m24 = 24; side.m24 = { day: 24, pick: ['keane-davi', rating], said, ready, slot: 36, spots, job: 'team:coil@24', done, mins }; own), p6/p7/p8 (PZ6: W.tr.p6/p7/p8 when turned in; flags case.pN.first; to finish on paper caseCall/jobStepDone/turnInJob/caseTick as puzzle_check P6FIRST..), m25 (mine: W.tr.m25 = 26, W.mt with steps.done, ms mentor). devmode_check set on the on copy fails until every Step 6 ladder row is in the table.
- **DA6's '2-B' asks (S6-4 on staging d39b87a6):** playerBed() already accepts '2-B' (my s6.5) and worksHomeOpen asks pu4HomeOpen (s6.5): check they still hold after the merge. Left: 24t's cabinMine/cabinDraw read DECKS[4] and '4-23' hard-coded: learn DECKS[2].cabinSpots['2-B'] (each spot has `wall`, room 'B'); 8b's keepsakes read DECKS[2].homeKeepsakes['2-B']; the HUD names room B "Visitors' suite" after you move in (should be your room); clothes: DECKS[2].wardrobes['2-B'] = { room: 'B', place: '2-B-wardrobe' } exists. pu4Place: DA6's panel places '6-coil-1..3-svc' exist (469b606b): pu4Place already asks panelPlace(mid) first: verify the t4 test's stops use them after the merge (promo_beats t4test, controller promo4 "Drive coil" ring may change).
- **The refit odd job** ("Refit the visitors' suite", from Day 23, take it or leave it to the crew; T.move.refit; with it your 24t cabin touches follow you to 2-B and one more is yours to pick): DA6's cabin spots exist now. Don't add to ODD_ROWS (the stream's seeded order would change with the switch on): post it as its own job, its row only in fixTable's byId; section 17 (systems engineer reviews).
- **Live escort fix (claude/escort-follow-fix cffe8187, from integration 6f1915cb):** RV23 verified live (seated player reached; cadet identical; intro --evening OK). Lead 41 also asked for a check part on that live branch proving a follow escort reaches a SEATED player (pu3 offer at the table) plus check_fast, cadet vs 6f1915cb, promo_beats pu3 parts, intro_check, mech, controller promo3: NOT yet done; the probe used is /tmp-only (based on RV23's plans/rv23-shots/p4_diag.py on claude/review-rv23: devmodeSetCareerTo(13), Day 14 10:05, deck 3 '3-lounge-24', puReady = () => true, PU_LIVE.seek = { by: 'calder', at }). Lead may ship it as 0.94.1.
- **N6 (nights):** uses pu4Fetches(now) to silence its night-1 notice only; its clock-in and engine-room arrows lead my walk (my escort leads to the Works bay clock until SHIP.works.ns[22].in, then the engine room). Its knock stops a sleep at 22:40 on night 1 without a notice (mine says it). mech_check m19's failure was the check (N6 moved the part to Days 30-31).
- **RV23 open:** turns 2-4 of S6-7 are in their queue; nothing else open (promo4 up to 9dcd0b1a PASS).
- Judgement: the move never happens by Mail alone (the spec: notice and arrow each day until you've stepped in).

## How to test
- On copy: `sed "s/^const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');/const P5_STEP6 = P5_STEP5 \&\& true;/" starship-cadet.html > ON6.html`.
- `promo_beats_check.py BUILD t4off`; `promo_beats_check.py ON6.html t4before t4test t4passed t4welcome t4badge t4move t4dev mt mt2 mt3 mt4 t3passed`; `mech_check.py ON6.html t3 t4 m21 m25`; `controller_check.py BUILD promo4 mentor`; `devmode_check.py ON6.html t4beats`; cadet_test vs 64e296df; check_fast.
- Fresh container: acorn must be 8.12.1 (`npm pack acorn@8.12.1` in $CADET_WORK/acorn).
