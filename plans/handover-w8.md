# Handover: W8 (the Works career engineer for Pillar 5 Step 6, after W7)

- **Role:** Works career engineer for Step 6, for lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message). Reviewer RV23 (session_01GKuymoDm1XbC5G8TvaCNLr), build master BM19 (session_01GKuymncYhRTKs8t4byNfdj). My session: session_01GKuymk95u5t4uDsahatkPN.
- **Read first:** plans/handover-w7.md and plans/handover-w6.md (what came before), the spec `plans/p5-step6-spec.html` on claude/p5-specs, DEV_NOTES "Mentoring Basil" and "Calder's question".
- **I own:** 24 core, 24u, section 28's shared helpers, 28e, 28f, the Step 6 switch lines, all Step 6 DM_CAREER rows (section 25). Other seats ask me before touching them.
- **Branch:** `claude/p5s6-promo4`. Rows `0.94.0-s6.N`. Never touch the two build-number lines.

## Done
- **s6.13:** merged claude/staging-p5s6 (a78f596: M24, DA6's S6-4, S6-6 turn 2; conflicts only in mech_check, controller_check, build-table: kept both sides). S6-7's clue now opens PZ6's casePoint (when the build has it). S6-9 turn 1: Calder's question (28f). 24 core: worksEscort skips p5nEscort while the asker is with you on a training/test job.

- **s6.14:** S6-9 turn 2: Calder at her tea (her plan doesn't take her there: backlog W8-1), the seats cleared live, the Works app's last page; screenshots plans/w8-shots/.

## Still to do
1. **career_check Days 0-26** (a --s6 part: steady and slow, twice identical, nights, door plates, 4-23 back to spare); stories_check / fridays_check / events_check / bigevents_check on Day 26 with Step 6 on.
2. **The refit odd job** and **DA6's '2-B' asks** (see handover-w7 "Still to do": 24t cabinMine/cabinDraw from DECKS[2].cabinSpots['2-B'], 8b keepsakes from DECKS[2].homeKeepsakes['2-B'], the HUD's room B name after you move in).
3. **All Step 6 DM_CAREER rows** (m21, m22 nights, m23, m24, p6-p8, m25) so devmode_check set passes on a Step 6 copy (handover-w7 lists each row's shape).
4. Live escort check on claude/escort-follow-fix (handover-w7) if lead 41 still wants it.

## Judgement calls (overrule any)
- The question needs an Engine Specialist (tier 4); not one yet on Day 26, it waits for the first Friday tea after you are one (same place and time, the words say "Friday tea").
- "She sits beside you": the tea corner has two seats ('5-tea-1', '5-tea-2', across the little table); she takes the one you're not on and the arrow shows you the other. Not sat after three minutes, she asks anyway.
- Missed at the tea: she comes to find you (follow) that evening till 22:00 and each later day 10:00-21:00 until asked.
- Names: cq* (section 29, the ending, already has endAnswer etc.); words and scenes keep the spec's end.* keys.
- The p5nEscort skip (24 core): N6's word on Day 22 is then said beside you during the Tier 4 test. Told N6 and the lead.

## How to test
- On copy: `sed "s/^const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');/const P5_STEP6 = P5_STEP5 \&\& true;/" starship-cadet.html > ON6.html`.
- `CADET_CHROME=/opt/pw-browsers/chromium` on every browser check (pip's Playwright wants another Chromium otherwise).
- `promo_beats_check.py ON6.html t4before t4test t4passed t4welcome t4badge t4move t4dev mt mt2 mt3 mt4 cq cq2 t3passed`; `mech_check.py ON6.html t3 t4 m21 m24 m25`; `controller_check.py BUILD promo4 mentor`; cadet_test vs 64e296df; check_fast.
- mt3's casePoint path: merge claude/p5s6-puzzles into a scratch worktree, apply the game diff, make its ON6 copy.
