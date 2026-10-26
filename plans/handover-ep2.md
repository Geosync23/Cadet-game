# Handover: EP2 (Pillar 5 spec writer)

Session: EP2 (session_01Hos4fCBxgEXxP8nR9E2iMq), hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Planning only: no game edits.
Branch: `claude/p5-specs` (from claude/events-plan-2; push only there).

## What I wrote
1. `plans/p5-step5-spec.html` (26f54636): Step 5 build spec. 7 pieces (S5-1 core, S5-2 Senior Officer promotion in new 24u,
   S5-3 M19 in 24v, S5-4 M18 shutdowns in 24w, S5-5 M20 in 24x, S5-6 P4/P5/P9 + old-mysteries board in 24k, S5-7 words).
   Switches P5_STEP5 (#p5s5) + P5_PROMO3/M19/M18/M20/CASES5. 4 builders at once. EV_BEATS moved to v3.1 hours (whole career)
   by S5-1. Questions: play the promotion early (Dev link); Power safety lesson vs Team jobs; shutdowns over meals.
2. `plans/p5-step6-spec.html`: Step 6 build spec. New section 28 (28a nights ... 28f end); 9 pieces + words.
   Switches P5_STEP6 (#p5s6, needs Step 5) + P5_NIGHT/M21/PROMO4/DECK6/M23/M24/M25/CASES6/END. 5 builders, then 6.
   Questions: Monday briefing weekly or once; Calder's question's answers.

## Facts found (both pages say them)
- 24p is tier-1 specific; later promotions go in 24u, 24p untouched except promoBeatsPtr, worksHome(Open).
- EV_BEATS held the old estimates (nights Days 19-20, Senior scene Day 16 10:00).
- No "Power safety" row in the game. calrig = the machine shop test rig (new tool id: arrayrig).
- Rotas: Navarro off Wed/Thu nights, Reyes and Kowalczyk off Tue/Wed, Jovanovic off Wed/Thu.
- Breakfast 07:00-09:00; DAY_SHIFT read in 43 places in 13 sections; no coil/reactor machines on Deck 6 (props only).
- Lines assuming a Senior moves to Deck 2: friday-d19.address l.47, friday-d26.address l.33, event-comet.lines ~l.98.

## How to check a page
`node -e` new Function on the <script>; a 390-px Playwright load has scrollWidth 390. Answers form saves to answers/user
(publish with the db capability).

## Later (same day)
- v2 of both step specs (e437f71d, db1313c1): beats tables for the user's rules (tons of arrows, pronounced moments), arrows_check parts step5/step6, all 5 questions on both pages. Published by lead 39: Step 5 claude.ai/artifact/9z1tyZ5faB6CPKt94DnN3N, Step 6 claude.ai/artifact/VZhNq1rnzRZYwtbjqJvxCo.
- `plans/veyli-vessel-spec.html` (e9f0962c): EV_VESSEL_ON (#evvessel), section 18 block after the comet's + slot "Vessel builder"; 2 builders; can start on 0.93.3. jobReserve slots agreed: t3 25, t4 26, vessel 27 (kept, unused). Switch lines: Step 5/6 after EV_COMET_ON, vessel after P926_APPT.
- `plans/ending-spec.html`: the ending (crossing back Day 35, the HQ offer Day 32, stay = endgame / go = goodbye + end page + kept copy). EV_ENDING_ON (?ending), section 29, 3 builders, ~850 lines. Canon: the Admiral is the Captain's fish, never explained.

## State at handover (2026-10-26 ~20:10 UTC)
- All four specs on claude/p5-specs carry the user's answers: Step 5/6 all five as recommended (test link yes, power safety lesson, mealtime shutdowns allowed, weekly briefing, four answers to Calder); vessel C1 yes, C2 yes, C3 Taavek and Calder wait at the ramp up to an hour (Zeke after 10:30); ending Q1 NO way back (no kept copy; "Keep this ending" marks the save ended), Q2 change your mind until the Captain's address, Q3 the post worded by Calder's answer.
- Bands agreed with B1 (S5-1): Tier 2 [0,10,22,32,42], Tier 3 [0,14,30,55,75]. jobReserve slots: t3 25, t4 26, vessel 27 kept, m19 32, m18 33, m20 34, m23 35, m24 36, m25 37. jobReserve skips engine kinds: t4 needs an o.engine option.
- Builders already working from these: B1 (S5-1, claude/p5s5-skeleton), VB1 (vessel), EN1 and SW6 (ending). Published pages: lead 39 holds the links.
- Loose ends: Kowalczyk's "end of night 2" beat vs her Tue/Wed nights off (social engineer to check); Pell "if he stayed" has no flag; cabin 4-04 shared by Taavek and the unbuilt nebula event's Lindgren.
- A fresh planner taking over: read this note, then the four spec pages; reply to builders' calls against the pages and the user's answers; update the pages in the same commit as any decision.
