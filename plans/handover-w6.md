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
