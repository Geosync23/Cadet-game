# Dev mode plan v4.1: summary

DM1 (Dev mode engineer) for lead 43, 2026-10-28. Branch `claude/devmode-plan-2`, from `claude/staging-pad` (0.95.0 + controller work). Full page: `plans/devmode-plan.html` (published for the user, answers saved on the page as doc `devmode-plan-v4`). Plan only: no game or check change. Building waits until the controller round passes and the user says go.

Built on DP1's v3.1 (kept as `plans/devmode-plan-v3.1.html` / `.md`). The user's answers to v2.1 and v3 (artifact 2ugbTkkAFkEsgTZa3bbFdH, collection `answers`, docs `devmode-plan` and `devmode-plan-v3`) stay decided: Dev link and own Dev save; Set career always a new Dev game; wake 06:00 in bed, beat shortcuts go on to the beat's time and place; starting friendships; workdays excused, needs kept, Top up; rank by hand allowed, marked approximate; three stops with Big events last; today's tradition under the fade; Undo; Take me to and Mark. The user's comments asked for less complexity ("I want to be able to test the traditions and career progression"), so v4 adds no new machinery: jumps are Set career with a landing.

## v4.1: CA1's review taken in (plans/devmode-plan-review.md on claude/devmode-review-ca1)
- F1: devmodeCareerSet only up to the table's last day (Day 26), and it merges (ms, done, tr/pu keys the table doesn't name kept). Check: a Day 36 jump keeps nights, mentor, question in W.ms.
- F2: the runner takes a stops list `{ at, fn }` (cqAnswer ~Day 26 19:10; endOfferDone, endSay Day 32 from 16:00); the answers' state and defaults are J0's (`DM_UI.ans`); J1/J3 never edit devmodeCareerSteps.
- F3: plain Set career past Day 32 says Stay (endgame); only the ending's Go jumps say Go; the panel says which answers.
- F4: no Mark fallback (v2.1 q13: a long first jump is fine with a progress bar and a Stop): progress line plus a Stop button; "about a minute on a phone" (CA1: Day 36 15 s headless, 65 s at 4x CPU slowdown).
- F5: stub parts events1/events2, ending1/ending2; J0 measures a whole part; answer combinations from one Day 26 landing with Undo.
- F6: added jumps: M19 lesson (Day 17), M20 training (Day 19), old mysteries (Day 21), first rotation (Day 21), Short Friday 15:30 and the Friday address (Day 5), the slower career's ending.
- F7: the page says it's the larger option (~22 h) and offers a first cut (~12 h: Career and Nights, the ending's three landings, one jump per event, the running card) as question 6.
- J0 is now 4 h (it owns devmodeCareerSteps and devmodeCareerSet); total about 22 h.

## What changed from v3.1
- Stops 1a, 1b, 2: built and live (DB1, DB2), kept.
- Set career: Days 0-30 -> 0-40; rank buttons; ~40 jumps (were 8 beat shortcuts).
- Big events (Stop 3, never built): v3.1's Start today/tomorrow becomes jump to the event's calendar day (question 1, since events are now on fixed days other things depend on); Next phase, threads - and +, End and undo kept as agreed; End and keep now possible (eventFinish split out).
- Events now: the Line, storm, comet, Veyli vessel, crossing back (visit still a draft).
- Steps 5-6 and the ending: built; their beats become jumps.
- Traditions: plus "Go to its next showing".
- Career arrow (added 23 Oct, after v3.1): follows nights, briefing, Basil, Calder's question, ending.

## Audit (section 25 on staging-pad)
- Works: clock, Take me to, Mark/Undo/Copy real game, Speed, Step 3 beats, Engine Specialist beats, Basil.
- Partly: traditions (no cake/invitation/flag, no event-only ones, no real next showing), Set career (to Day 30), ranks by hand (Junior/Officer only), Step 5 (Next step only), the arrow (silent after Deck 2 move), Calder's question (answer not set for later jumps), first-week meetings (play-once recipe).
- Missing: ship-wide events, running-event controls, Monday briefing, nights 1-3, the ending.

## Turns (about 22 hours; see v4.1 above for J0's added work)
- J0 (A, 3h): `DM_JUMPS` + `devmodeJump({...})`, the Jump to tab, the runner, DM_MAXDAY 40, rank buttons, Senior/Specialist by hand (approximate), Day 1 try, empty blocks J1-J3, stub check parts; measure a Day 36 jump.
- Then side by side: J1 (A, 4h) career + nights, part `beats`; J2 (B, 4h) ship events + running card (Next phase, threads -/+, its meeting, End and undo, End and keep), part `events`; J3 (C, 4h) ending + answers row + next showing, parts `ending`, `trad`; J4 (first free, 3h) the arrow, dev_arrow_check `s6`, `ev`, `end`.
- J5 (A, 2h): DEV_NOTES, design-doc, build table, full round on six runners.

## New questions (recommended first)
1. Events: jump to their calendar day (plus the agreed running tools), not 3.1's Start today/tomorrow.
2. Diplomatic visit: not until it's on.
3. Answers row (Engines/Bridge/Teach/Unsure; Stay/Go/Unsure), Engines and Stay to start; the ending's Go jumps say Go.
4. First-week meetings: try in J0, else keep the recipe.
5. Arrow at event meetings: yes, "Event:".
6. A first cut (~12 h) first, the rest after the user has tried it.
7. Three builders side by side after J0.
