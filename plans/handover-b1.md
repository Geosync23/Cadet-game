# Handover: B1 (Step 5 builder, S5-1 turn 1)

- **Role:** builder for Pillar 5 Step 5, hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). My session: session_01GeUbys3v6keTivBrcgHznP. Planner: EP2 (session_01Hos4fCBxgEXxP8nR9E2iMq).
- **Branch:** `claude/p5s5-skeleton`, from `claude/staging-0.93.3` (= claude/integration d9c7e5f0, 0.93.2). Build-table row `0.93.4-s.1`. The two build-number lines are untouched (the build master's).
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs; plan v3.1 `plans/pillar5-steps56-plan.html` on claude/events-plan-2.

## What I built (S5-1 turn 1, the skeleton)
- Section 13, beside EV_COMET_ON: `P5_STEP5 = URL_FLAGS.has('p5s5')` (the spec says `#p5s5`, but URL_FLAGS reads the query string, so it's `?p5s5`, as `?evswap`), and `P5_PROMO3`, `P5_M19`, `P5_M18`, `P5_M20`, `P5_CASES5` (`P5_STEP5 && true`).
- Section 24 core, an `if (P5_STEP5)` block just before BAND_WORD: ladder rows ps, t3, m19, p4, m18, p5, m20, p9, mys; `WORK_TOOLS.arrayrig`; `WORK_BANDS[3]` = a copy of tier 2's (stand-in).
- Section 18, an `if (P5_STEP5)` block after the event swap's block (before the comet's): EV_BEATS at v3.1's hours, plus new rows seniorResult and nightShift3.
- Sections 24u, 24v, 24w, 24x (empty) after 24p's slot, before section 6, with slots `Later promotions`, `Power and relays`, `Shutdowns`, `Sensor array` (written by hand in add_slots.py's format: the tool refuses a file that already has slots).
- plans/owners.md, plans/map.md, tools/affected.py (RULES for 24u-24x), DEV_NOTES section "Pillar 5 Step 5".

## Judgement calls (tell EP2 / lead if they disagree)
- Stages I picked (the spec gives none): m19 `[0, 3, 6]` uses, m20 `[0, 2, 4]`; all others one stage. ps `needs: null` (rank officer and Day 12 gate it). m20 `by: ['mori', 'calder']`. mys `by: ['calder']` (a row needs a by).
- engineSpecialist's kind set to `'captain'` (the spec's table says captain; today it's 'beat'). seniorOfficer kind kept 'captain'.
- Night holds: Day 22 [1360, 1800], Days 23 and 24 [1245, 1800] (06:00 next day = 1800).
- The ladder's job slot is `10 + (index among big rows) % 10`: the new big rows (t3, m19, m18, m20) land on 10-13, the same as m1, m4, m5, m7. Builders should reserve their own free slot.

## Not done (left for S5-1 turns 2-3, per the spec)
- WORK_BANDS[2] re-tune and real WORK_BANDS[3]; the ps lesson (WORK_MECH.ps); Training tab Tier 3 rows; Dev presets; day_check EVENT_DAYS 15 and 16; career_check / mech_check parts.

## Tests (turn 1)
- Switch off: cadet_test ALL IDENTICAL vs staging-0.93.3; check_fast OK (425 s).
- Switch on (a copy with `const P5_STEP5 = true;`): day_check 1 OK; events_check only the known-old FX24-2 (Farouk, reading corner Day 7), no new FAIL.

## Setup gotcha
- Fresh container: `pip install playwright numpy pillow`, three r128 and acorn into /tmp/cadet-work (plans/testing-guide.md section 2). Don't run cadet_test at the same time as check_fast on 4 cores: the page load timed out.
