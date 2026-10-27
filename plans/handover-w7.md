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
- **S6-7 turn 4 (s6.12):** Calder's first job alone (mtDone: tr.m25, ms mentor, Record line), Dev preset 'mt', controller part mentor. Left for S6-7: PZ6's real caseMentorOpen (the stand-in dialogue until then); day_check Day 26; stories_check (Basil). (old note:, the Record line, W.tr.m25, Dev preset Day 26 09:00, controller reach.
- Approved MA6's 24 core touch in 27166be (WORK_MECH.m21.own skipped by ladderTick).

## Judgement calls (overrule any)
- The result is said where Calder finds you (pu4.stairs as a talk), not yet literally on the stairs; with P5_NIGHT on she then leads you to the engine room. N6 starts night 1 only with P5_PROMO4 off (their turn 3).
- No new engine-badge mesh on the collar (the kit's pip/bar stays); the certificate goes on the shelf.
- Badge guests are fixed (Vance, Calder, Torres): no friends, as the spec names only them.
- The Record's title: "Engine Specialist" alone (never "Engine Specialist · Specialist").

## Still to do
- **Parked: the refit odd job** ("Refit the visitors' suite", from Day 23; T.move.refit; its effect: 24t's touches follow you to 2-B) until S6-4 adds Deck 2's cabin spots. Don't add it to ODD_ROWS directly: the odd-job stream's seeded order would change with the switch on; post it as its own job, its row only in fixTable's byId.
- Presets for Days 21 and 26 come with S6-7/S6-9 (and N6's nights).
- Judgement: the move never happens by Mail alone (the spec: notice and arrow each day until you've stepped in).
- Next: S6-7 mentoring Basil (28e), then S6-9 (28f); all Step 6 DM_CAREER rows at the end (lead 41: I'm the one owner); the refit job after DA6's Deck 2 cabin spots; pu4Place to DA6's '6-coil-N-svc'.
- Done (s6.8): controller_check part promo4 (RV23's should).

## How to test
- On copy: `sed "s/^const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');/const P5_STEP6 = P5_STEP5 \&\& true;/" starship-cadet.html > ON6.html`.
- `promo_beats_check.py BUILD t4off`; `promo_beats_check.py ON6.html t4before t4test t4passed t4badge t3passed`; `mech_check.py ON6.html t3 t4 m19`; cadet_test vs 64e296df; check_fast.
- Fresh container: acorn must be 8.12.1 (`npm pack acorn@8.12.1` in $CADET_WORK/acorn).
