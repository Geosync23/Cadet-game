# Handover: social engineer A (Pillar 4, seat 3)

Written by session_012pK2XVi5UhqEd28fakYk68 (took over from session_01DzZ669spGpdSdVMYzUog2N, whose Pillar 3 note this replaces; its content is in DEV_NOTES "Social life"). Read CLAUDE.md, DEV_NOTES.md ("Social life (section 20)", all of it), plans/pillar4-plan.md (Part 6, seat 3) and plans/social-deep-plan.md on claude/social-design (the A steps, Parts 2, 4, 5, 6, 7, 8, 8b) first.

## Role, branch and builds
- Branch `claude/social`, builds 0.36.20+. Last: **0.36.42** (e7dfa90). Based on ship integration 0.41.10.
- 0.36.41 passed the full set (social, deck, day 1, player, events, interactions, food, machine; cadet_test vs 0.36.20 ALL IDENTICAL) and reviewer 1 (session_01HK4m33sUiLuVim8VWaCPMs) passed it. 0.36.42 is a one-liner, social_check OK.
- I own section `// 20. SOCIAL` (except the sub-block `// 20c. SOCIAL STORIES` at its end, social B's) and `social_check.py`.
- Report to the lead (session_01PxXKwc5mkC7tV5MPi3p7PP) after each push; the build master (session_012K7RZ3oSX2vpBb1rR66MBh) combines.

## What's built (DEV_NOTES has every detail and number)
A1 0.36.20 query API; A2 0.36.21 memories; A3 0.36.22 lines through `lineFor`; A4 0.36.23 week-1 gating, `socialInvite`; A5 0.36.24 gifts; A6 0.36.25 reputation; A7 0.36.26 invitations; A8 0.36.27 bunk visits and notes; A9 0.36.28 crew come and go; 0.36.29-0.36.42 lining up with the other seats and the reviewers' fixes.

## Shared formats and seams (others rely on these names)
- Query API (frozen vocabulary): `relTier mem memTold warmth affBand bondOf moodOf beatOf knowsNews repBand repShip knownFor cue inWeek1 leavingSoon newHere movedOff memThing socialFill`. `CALM_TYPES` / `placeCalm` are the deck architect's, `aboard` / `crewLeaving` / `crewArriving` / `crewComeTo` the sim engineer's, `introOn` / `introNote` onboarding's (mine are `socIntroOn` / `socIntroNote`). `SOC_BOND_KINDS` (20c has `STORY_BONDS`).
- Section 22 (dialogue) owns the five lines `CHAT_GREET`, `CHAT_NEAR`, `CHAT_LIFE`, `CHAT_DEPT`, `CHATTER_IDLE` (become `linesLegacy(...)`) and the first line of `chatGreet`: don't edit them or the lines next to them. `socLine` asks `lineFor` (ctx.peek on look-ahead calls).
- 20c's seams in section 20 (keep them): `storyHour(h, pairs)` in socialHour, `relGain` in relAdd, `knowBlocks` in the Crew app person view, `socBondOf` first in bondOf, `friendCap(p)` in socialHour, `affPlanWeek(i, j, d)` in affinityPlan, `momentReady` / `momentShow` / `goodbyeMoment` in chatLine and the card, `introOptions` / `introDo` ("Do you know…?"). Section 20 saves/resets `SHIP.social.bonds` and `affWeek` for 20c.
- Bus (section 13): I listen for repair, tradition, eventPhase, favour, gift, harvest, lateMeal, choice, introStep, jobAbandoned, jobUnclaimed, shiftStart, moment; I post tierUp, invite, gift.
- For others: `giftAdd`, `GIFT_MAKES`, `SOC_GIFTS` (player engineer's store and machine shop), `bunkNote()` (bunk tap), `repView()`, `repAskedFor(dept)`, `keepsakes()`, `movedOn()`, `crewContacts()`.
- schedU keys: social A 644-671 (used up to 665), social B 672-699.

## Loose ends
- Garden produce as gifts: the galley engineer calls `giftAdd('herbs' | 'tomato' | 'flower')` on harvest days (asked via the lead).
- The new store gifts (bar of chocolate, paper novel, music chip, pocket puzzle, spare tiles set) go into the store for the new player engineer (asked via the lead).
- The sim engineer builds `crewLeaving` / `crewArriving` after crew 0.16.13; nothing for me to change unless names differ.
- When social B's bonds merge, turn social_check's bond NOTE into a FAIL (friends 15-40, rivals 2-6, a mentor at day 14).
- Not built: A10 guiding a newcomer (needs onboarding's escort modes reversed, wave 4), A11 your own room (needs promotion), A12 tuning pass with the user. Bunk visits come fairly often; invitations about 1 a day: tune with the user's play.

## Gotchas
- **Run social_check before every push**, even one-liners (0.36.38 lost a helper and broke every card; reviewer 1 caught it).
- Section 20 sits before ROSTER (section 9) and section 21: everything lazy (`socInit`); `typeof` on a later const throws during load, so keep such checks inside try or out of load-time code.
- Plans' blocks (`planDay`) are in absolute ship minutes.
- Test overrides: `window.foo = ...` doesn't replace a script's own function or const; move the player instead, or push onto the real array.
- Before pushing a seam another seat depends on, a trial merge plus `node --check` on the main script catches name clashes.

## How to test
- `CADET_CHROME=/opt/pw-browsers/chromium python3 social_check.py BUILD.html` (13 parts, ~3 min). Then the full set one at a time (deck, day 1, player, events, interactions, food, machine, cadet_test vs the previous build), from a scratch copy of the build.

## Open questions for the user
- Are the numbers right once played (visits, invitations, gift points, reputation dips)? More drama or gentler?
