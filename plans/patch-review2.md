# Review update 2 (0.99.93-review): the user's answers, 2026-11-15 ~12:50 PM ET

Base: claude/staging-fable-review (tip cf5706ff, game commit c4999dae, game sha256 d6b9ce81...a1c0, label 0.99.92-review).
The review version is NOT adopted into main yet (the user wants to play it first). This update stays on the review
branch and is published over the two Review links only (WCna9m9E... play, 4nh7HATo... Dev). main does not move.

## The user's answers (questionnaire https://claude.ai/artifact/RtaryhDaBFcQx9Jz2biFmn)
1. Adopt the review version: not yet, play it first.
2. Food arrow ahead of another need: yes, as built. No change.
3. Theo stuck Day 14 (backlog R6-1): fix in the next update. -> piece A
4. Day 1's board: leave it as it is, "just make sure it's obvious which is the mission Calder wants done". -> piece B
5. Meals in the day's arrow: yes, breakfast before the shift arrow, dinner after clock-out, week 1 only. -> piece C
6. Work before clocking in: no paid jobs before clocking in, "with a tool tip". -> piece D
7. Pay: by the job's length and parts, and add more to buy. -> piece E (plan to the user first)
8. A day's work: no stopping point. No change.
9. Reputation's pace: leave it. No change.
10. First promotion: keep Day 9, update the design document. -> piece G
11. Apps: leave all 21. No change.
12. Week 1 work order: leave it. No change.
13. When something goes wrong: try to carry on quietly and only log it. -> piece F
14. Faster load that changes pictures (TEX_READ_ON): leave it off.
15. Lighter published file: no.
16. Reload mid-activity: a sensible moment nearby is enough. No change.
17. Safari on iPhone: not a target.
18. 60 fps cap: not now.

## Pieces (each behind its own switch; all off = cadet_test ALL IDENTICAL vs 0.99.92-review d6b9ce81)
- A (W1) R2_THEO_ON: Day 14, deck 7, teague-theo stuck 20 ship minutes at 14:49 (day_check 14 fails on 0.99.91 too). Find
  the cause, fix it, day_check 14 passes; check no other day regresses.
- F (W1) R2_QUIET_ON: LOOP_GUARD_ON's card. The user wants the game to carry on quietly and only log. Lead's reading: an
  error that comes and goes never shows a card (logged once per kind); the card stays ONLY for a true freeze (every
  frame failing for about 10 real seconds), since otherwise the player has a frozen screen and no word. The user is
  asked to confirm that last part; build it so the freeze card is one constant to turn off.
- B (W2) R2_SHADOW_ON: Day 1's board unchanged in what it offers, but Calder's job is unmistakable: listed first, a clear
  mark in Calder's words (e.g. "Chief Calder's job for today"), and the arrow/pin goes to it first.
- C (W2) R2_MEALS_ON: week 1 only (Days 1-7): the day's own arrow includes breakfast before the shift arrow and dinner
  after clock-out. Must sit with FRP_FOOD_ON and TB7-1 (never point at a closed servery).
- D (W2) R2_CLOCK_ON: board jobs cannot be taken (so are not paid) before you clock in; a plain tip says why the first
  time ("Jobs open once you've clocked in at 09:00" or similar); the board arrow before the shift goes away. Mind the
  shadow job, night shifts, off days, Dev jumps and checks that take jobs at 06:00.
- E (W3) R2_PAY_ON: pay by the job's length and parts instead of a flat 15, and more to buy. PLAN FIRST: a pay table
  (per job kind, minutes, parts), a week's expected income for an ordinary player, and a list of new things to buy with
  prices, as a short page for the user to approve. No game change before the user's OK.
- G (W2 or W3, with their commit): design-doc: first promotion on Day 9 (replace "about 2 ship weeks"); move the
  answered questions out of Open questions (1-18 above).

## After the pieces
Reviewer (fresh, from plans/handover-rv37.md on claude/review-rv37), build master (fresh, from plans/handover-bm29.md on
claude/staging-fable-review), full round of six, publish over the two Review links, label 0.99.93-review.
