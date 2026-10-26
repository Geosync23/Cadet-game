# Handover: B1 (the Works career engineer for Pillar 5 Step 5)

- **Role:** Works career engineer for Step 5, hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). My session: session_01GeUbys3v6keTivBrcgHznP. Planner: EP2 (session_01Hos4fCBxgEXxP8nR9E2iMq).
- **Branches:** `claude/p5s5-skeleton` 5957d244 (S5-1 turn 1, the skeleton the other seats start from); `claude/p5s5-career` (S5-1 turns 2-3, then S5-2). Build-table rows `0.93.4-s.1` to `0.93.4-s.3`. The two build-number lines are never touched (the build master's).
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs (v2 has the beats table near the top: what you see, when it clears, who speaks, line counts; and the arrow-follower check part step5). Plan v3.1: `plans/pillar5-steps56-plan.html` on claude/events-plan-2, sections 4 (the promotion pattern) and 5 (day by day).
- **User rules for all Step 5 work:** every piece works with a game controller; tons of arrows and super obvious progression (level 1 arrows on the day, a ring line on what you tap, notices, Tracked and Schedule rows, said in person first, Mail only as the record); key moments are staged scenes with dialogue.

## What's built (all behind `P5_STEP5`, off; `?p5s5` previews)
- **Turn 1 (skeleton):** section 13's six switches (`P5_STEP5`, `P5_PROMO3`, `P5_M19`, `P5_M18`, `P5_M20`, `P5_CASES5`); 24 core's `if (P5_STEP5)` block before BAND_WORD: ladder rows (ps right after t2; then t3, m19, p4, m18, p5, m20, p9, mys pushed), `WORK_TOOLS.arrayrig`, the bands; section 18's `if (P5_STEP5)` block after the event swap: EV_BEATS at v3.1's hours plus seniorResult and nightShift3; empty sections 24u-24x with slots `Later promotions`, `Power and relays`, `Shutdowns`, `Sensor array`.
- **Turn 2:** `WORK_BANDS[2] = [0, 10, 22, 32, 42]`, `WORK_BANDS[3] = [0, 14, 30, 55, 75]` (career_check part s5). Power safety in 24u: `psTick`/`psAsk` (a small row has no lesson in 24 core, so ps makes its own appointment: occasion `works.ps`, Deck 6 port junction 6/j, 09:00 or 09:15, 20 minutes, Mail + toast, level 1 arrow, talk `train.ps.calder` (stand-in in code until the head writer's words), trained when met, asked again the next workday if missed). mech_check part `ps`.
- **Turn 3:** 24u `puCheck()` (Training tab "Your promotion: the Tier 3 test"; 24 core's tab asks it in one typeof line); 24u `psDevNext()` (Dev arrow for ps; section 25's dvCareerNext asks it and leaves ps out of its small rows); section 25's DM_CAREER Step 5 rows (`test3` on Day 15, `promo3` on Day 16 = Tier 3, rank senior, `pu.t3` passed, milestone `senior`) and devmodeCareerFor reading them; event days 15 and 16 in tools/affected.py (+ cov_run.sh, the testing guide's table); dev_arrow_check part `s5`; bigevents_check's guard samples follow the new hours with the switch on.

## Open (asked, not answered when written)
- **Tier 2 bands:** the spec's "steady Relied on by Day 13/14" and "very busy not before Day 12" can't both hold on paper (steady 45 by the end of the storm Saturday, very busy 52 by the end of Day 11). I kept the steady target (42); the other choice is 54 (busy Day 12, steady Monday Day 15). Asked EP2 and lead 39. Backlog 12 already says the user parked the very busy pace for a later balance pass.
- The user's question 2 (Power safety) is still open; ps is the recommended answer.

## Judgement calls
- Stages: m19 [0, 3, 6] uses, m20 [0, 2, 4]; ps `needs: null`; m20 `by: ['mori', 'calder']`; mys `by: ['calder']`; engineSpecialist's hold kind `'captain'`.
- Ladder job slots: `10 + (index among big rows) % 10`, so t3, m19, m18, m20 share 10-13 with m1, m4, m5, m7. Each sub-block should reserve its own slot (the Tier 2 test uses 20, the fix-scan 24).

## S5-2 (the Senior Officer promotion), not started
- Section 24u, behind `P5_PROMO3`. Mirror 24p (720 lines; the functions list is worth reading first: `promoAnnounce`, `promoPassed`, `promoDelay`, `promoSummonsTick`, `promoSeekTick`, `promoEscort`, `promoCerTick`, `promoCakeTick`, `promoGuide`, `promoBeatsTick`, `promoTalkTick`, `promoBeatsItems`, `promoNotice`, `promoMail`, `promoCerTimes`, `promoGuests`, `promoBusy`, `promoWorkday`, `promoPartsAside`). Call 24p's helpers, never change 24p except the one line in `promoBeatsPtr` (key 't3' asks 24u).
- Save: `SHIP.works.pu = { t3: { day, tries, passed, res, bar, toast } }`, read back by 24u itself (worksClean keeps only 24 core's fields; `side` is kept whole, or read it from the save as 24k/24f do).
- The Tier 3 test job: a junction on Deck 6 in the worse state (jobReserve with a free slot), 09:00-15:00, warn two people from SHUT_BRANCHES' rooms (S5-4's table; schedU key 853), Calder escorts (worksEscort's 24u part: one line in 24 core).
- Checks to extend: promo_beats_check (t3off ... t3toast), career_check (Senior Officer on Day 16 for a steady player), arrows_check new part step5 (the arrow-follower, three ways), saves_check, day_check 15/16, controller_check.

## How to test
- Fresh container: `pip install playwright numpy pillow`; three r128 and acorn 8.12.1 into /tmp/cadet-work (plans/testing-guide.md section 2); `export CADET_CHROME=/opt/pw-browsers/chromium`.
- Switch on in a copy: `sed "s|^const P5_STEP5 = URL_FLAGS.has('p5s5');|const P5_STEP5 = true;|" starship-cadet.html > on.html`.
- Quick parts: `python3 career_check.py on.html --s5` (25 s), `python3 mech_check.py on.html ps`, `python3 dev_arrow_check.py on.html s5`.
- **Run browser checks one at a time on 4 cores:** mech_check's GPU process takes about 3 cores, and parallel runs time out loading the page.
- Known-old: career_check "busy: Relied on before Day 5" (backlog 12) on and off; events_check FX24-2 (Farouk Day 7).
