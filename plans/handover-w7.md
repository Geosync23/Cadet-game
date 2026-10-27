# Handover: W7 (the Works career engineer for Pillar 5 Step 6, after W6)

- **Role:** Works career engineer for Step 6, for lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). Reviewer RV23 (session_01GKuymoDm1XbC5G8TvaCNLr), build master BM19 (session_01GKuymncYhRTKs8t4byNfdj). My session: session_01GKuymjghu82TGWPLR1wTKw.
- **Read first:** plans/handover-w6.md (what W6 built: turns 1-2 of S6-3, the first turn of Step 6), the spec `plans/p5-step6-spec.html` on claude/p5-specs.
- **I own:** S6-3 turns 3-4, S6-7 mentoring Basil (28e), S6-9 the end (28f); section 28's shared helpers, 24u, 24 core, the Step 6 switch lines. Other seats ask me before touching them.
- **Branch:** `claude/p5s6-promo4`. Rows `0.94.0-s6.N`. Never touch the two build-number lines.
- **Overnight:** the user is asleep; the spec's recommended answers; at most two browser checks at once.

## Done
- **Turn 3 (s6.4):** the result at 22:40 and the Captain's badge (see DEV_NOTES "The Engine Specialist promotion", Turn 3).
- **Turn 4a (s6.5):** the move to 2-B with Vance after dinner, laundry collected (DEV_NOTES Turn 4a).
- Approved MA6's 24 core touch in 27166be (WORK_MECH.m21.own skipped by ladderTick).

## Judgement calls (overrule any)
- The result is said where Calder finds you (pu4.stairs as a talk), not yet literally on the stairs; with P5_NIGHT on she then leads you to the engine room. N6 starts night 1 only with P5_PROMO4 off (their turn 3).
- No new engine-badge mesh on the collar (the kit's pip/bar stays); the certificate goes on the shelf.
- Badge guests are fixed (Vance, Calder, Torres): no friends, as the spec names only them.
- The Record's title: "Engine Specialist" alone (never "Engine Specialist · Specialist").

## Still to do
- **Turn 4b:** the refit odd job (section 17's ODD_ROWS, one row, from Day 23, "Refit the visitors' suite"; T.move.refit; with it 24t's touches follow you: cabinMine reads 4-23 only today), forYou's engine line (17), Dev mode puDevSteps/puDevNext for Tier 4 and presets Days 21-26 (section 25).
- Judgement: the move never happens by Mail alone (the spec: notice and arrow each day until you've stepped in).
- Wave 2: the comet/welcome night parts, then S6-7 (28e), S6-9 (28f).

## How to test
- On copy: `sed "s/^const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');/const P5_STEP6 = P5_STEP5 \&\& true;/" starship-cadet.html > ON6.html`.
- `promo_beats_check.py BUILD t4off`; `promo_beats_check.py ON6.html t4before t4test t4passed t4badge t3passed`; `mech_check.py ON6.html t3 t4 m19`; cadet_test vs 64e296df; check_fast.
- Fresh container: acorn must be 8.12.1 (`npm pack acorn@8.12.1` in $CADET_WORK/acorn).
