# Handover: social engineer A (Pillar 4, seat 3)

Written by session_012pK2XVi5UhqEd28fakYk68 (took over from session_01DzZ669spGpdSdVMYzUog2N, whose Pillar 3 note this replaces; its content is in DEV_NOTES "Social life"). Read CLAUDE.md, DEV_NOTES.md ("Social life (section 20)", all of it), plans/pillar4-plan.md (Part 6, seat 3) and plans/social-deep-plan.md on claude/social-design (the A steps, Parts 2, 4, 5, 6, 7, 8, 8b) first.

## Role, branch and builds
- Branch `claude/social`, builds 0.36.20+. Last: **0.36.81** (752d964). Ship integration 0.60.2 merged in at 0.36.64 (84e992e).
- 0.36.41 passed the full set; later builds ran social_check (17 parts), plus intro_check and cadet_test where they touched anything visible (0.36.65/0.36.66 ALL IDENTICAL). Reviewer 1b (session_018XY1NbMBxo2SLDPxooe5yx) reviews; 0.36.52-0.36.59 PASS WITH FIXES, fixed in 0.36.60-0.36.62.
- I own section `// 20. SOCIAL` (except the sub-block `// 20c. SOCIAL STORIES` at its end, social B's) and `social_check.py`.
- Report to the lead (now session_01KPJMYjXAPkNUcrQ8VRkhLE) after each push. Onboarding engineer: session_01KaHzfqSqF8B4bkNFrH1tsx.

## What's built (DEV_NOTES has every detail and number)
A1 0.36.20 query API; A2 0.36.21 memories; A3 0.36.22 lines through `lineFor`; A4 0.36.23 week-1 gating, `socialInvite`; A5 0.36.24 gifts; A6 0.36.25 reputation; A7 0.36.26 invitations; A8 0.36.27 bunk visits and notes; A9 0.36.28 crew come and go; 0.36.29-0.36.63 lining up with the other seats and the reviewers' fixes (notes applied at the end of their hour, asked-for waves `socialSeekAsk`, `seekSpot`); **A10 0.36.65 guiding a newcomer** and **A11 0.36.66 your own room** (both behind `flag('promoted')`, the user's rule; off in normal play, tested with the flag set: social_check parts 16-17); **A12 0.36.67-0.36.71**: the save packs 20c's bonds; ship standings gain less near the top; rivalries floor at -45 and ease every other night; unclaimed-job dips once a week per department (all approved by the lead; numbers in DEV_NOTES). 0.36.72: reviewer 1b's four fixes (seekSpot never your seat, no walking while you sleep, since words, cue tie-break). 0.36.73: rel arrays trimmed; the 140-day numbers (save about 29.6 KB in play at day 140: watch it; asked social B2 about affWeek growing). 0.36.68: `socHr` (Day 0 hours), `momentWantsVisit` in the visit picker (social B2), `kin`/`lost`/`hobbyNoun` fill-ins (crew designer 3).

## Shared formats and seams (others rely on these names)
- Query API (frozen vocabulary): `relTier mem memTold warmth affBand bondOf moodOf beatOf knowsNews repBand repShip knownFor cue inWeek1 leavingSoon newHere movedOff memThing socialFill`. `CALM_TYPES` / `placeCalm` are the deck architect's, `aboard` / `crewLeaving` / `crewArriving` / `crewComeTo` the sim engineer's, `introOn` / `introNote` onboarding's (mine are `socIntroOn` / `socIntroNote`). `SOC_BOND_KINDS` (20c has `STORY_BONDS`).
- Section 22 (dialogue) owns the five lines `CHAT_GREET`, `CHAT_NEAR`, `CHAT_LIFE`, `CHAT_DEPT`, `CHATTER_IDLE` (become `linesLegacy(...)`) and the first line of `chatGreet`: don't edit them or the lines next to them. `socLine` asks `lineFor` (ctx.peek on look-ahead calls).
- 20c's seams in section 20 (keep them): `storyHour(h, pairs)` in socialHour, `relGain` in relAdd, `knowBlocks` in the Crew app person view, `socBondOf` first in bondOf, `friendCap(p)` in socialHour, `affPlanWeek(i, j, d)` in affinityPlan, `momentReady` / `momentShow` / `goodbyeMoment` in chatLine and the card, `introOptions` / `introDo` ("Do you know…?"). Section 20 saves/resets `SHIP.social.bonds` and `affWeek` for 20c.
- Bus (section 13): I listen for repair, tradition, eventPhase, favour, gift, harvest, lateMeal, choice, introStep, jobAbandoned, jobUnclaimed, shiftStart, moment; I post tierUp, invite, gift.
- For others: `giftAdd`, `GIFT_MAKES`, `SOC_GIFTS` (player engineer's store and machine shop), `bunkNote()` (bunk tap), `repView()`, `repAskedFor(dept)`, `keepsakes()`, `movedOn()`, `crewContacts()`.
- schedU keys: social A 644-671 (used up to 667), social B 672-699.

## Loose ends
- Garden produce as gifts: the galley engineer calls `giftAdd('herbs' | 'tomato' | 'flower')` on harvest days (asked via the lead).
- The new store gifts (bar of chocolate, paper novel, music chip, pocket puzzle, spare tiles set) go into the store for the new player engineer (asked via the lead).
- The sim engineer builds `crewLeaving` / `crewArriving` after crew 0.16.13; nothing for me to change unless names differ.
- When social B's bonds merge, turn social_check's bond NOTE into a FAIL (friends 15-40, rivals 2-6, a mentor at day 14).
- A10's other half is onboarding's: `introGuide(id)` (you lead, the newcomer follows) and `introGuideEnd(id)`; I asked them to keep `introOn()` about your own intro while you guide (else week-1 gates close again). `simNote('guideAssigned', { id, day })` goes out at assignment.
- A12 done on paper; the rest waits for the user's play. The month runner is a scratch script (month.py: social_check's harness plus a stand-in player; easy to rebuild from social_check's RUN).
- The save (the lead's rule): at most 30 KB at day 140, under 40 KB at any length; every saved part hard-bounded, worst cases in DEV_NOTES "Social life", Save bounds. `social_check.py BUILD --long` (280 days, ~30 min) checks it; measure on a build merged with social B's latest. 0.36.74: occasions' appointments (`a.occ`) skipped. 0.36.75-0.36.78: heard/cues/pairs/known packed (known by a 4-char text hash), NEWS_MAX 20, CUE_MAX 24, pairs 300, moved 24, `--long` measures daily (worst day to 140 at most 30 KB, every day to 280 under 40 KB). 0.36.77: storyBondsPack/Unpack hooks for 20c. 0.36.79: affWeek only with the same crew list. 0.36.80: NEWS_MAX 16. 0.36.81: aff saved as deltas from affStart, rel/news/cues as rows (older saves load); --long runs from the arrival with event news; worst day to 140 was 26.6 KB on the 3-branch merge.
- The arrival-jump check in --long calls machinesNow() each step, as the game's tick does (the '4 extra notes' were the test's, not section 17's).
- Open: sim engineer 4's 'purity wrong' report on ship-events + 69876a7 never reproduced here; social_check now names the changed save part.

## Gotchas
- **Run social_check before every push**, even one-liners (0.36.38 lost a helper and broke every card; reviewer 1 caught it).
- Section 20 sits before ROSTER (section 9) and section 21: everything lazy (`socInit`); `typeof` on a later const throws during load, so keep such checks inside try or out of load-time code.
- Plans' blocks (`planDay`) are in absolute ship minutes.
- Test overrides: `window.foo = ...` doesn't replace a script's own function. social_check's `g.ev` runs inside the game's scope, so swap with a plain `foo = ...` there (save the real one first, put it back after); consts can't be swapped (move the player instead, or push onto the real array). Never set `SHIP.intro` to null (section 13/21 read it): restore the saved object. With section 10's `crewComeTo` merged, a visitor's card opens on arrival, later; tests stand in an instant arrival.
- Before pushing a seam another seat depends on, a trial merge plus `node --check` on the main script catches name clashes.
- **Never merge claude/ship-systems** (the lead's rule): section 17 comes only from claude/sim-engineer, which already contains it; an old section 17 makes bus notes carry the send time.
- **Trial-merge order:** merge claude/sim-engineer LAST (crew designer, arrival, social B first), or an older section 13 from another branch wins the conflicts; then check `grep -c 'function simNote'` (2), `function storyHour` (1), `const introOn` (1) before trusting a run.
- **Trial merges: never `git merge -X ours`.** It keeps your side of a whole conflict block, and a block can swallow another seat's new code next to it (the build-number line sits right beside section 13's bus, so `-X ours` silently dropped the bus). Merge normally, take theirs for every conflict outside section 20 (a small script on the markers), and check the other seat's key function is in the result (e.g. `grep -c 'function simNote'`).

## How to test
- `CADET_CHROME=/opt/pw-browsers/chromium python3 social_check.py BUILD.html` (18 parts, ~4 min; `--long` for the long-play save check). Then the full set one at a time (deck, day 1, player, events, interactions, food, machine, cadet_test vs the previous build), from a scratch copy of the build.

## Open questions for the user
- Are the numbers right once played (visits, invitations, gift points, reputation dips)? More drama or gentler?
