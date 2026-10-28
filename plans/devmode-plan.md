# Dev mode plan v4: summary

DM1 (Dev mode engineer) for lead 43, 2026-10-28. Branch `claude/devmode-plan-2`, from `claude/staging-pad` (0.95.0 + controller work). Full page: `plans/devmode-plan.html` (published for the user, answers saved on the page as doc `devmode-plan-v4`). Plan only: no game or check change. Building waits until the controller round passes and the user says go.

Built on DP1's v3.1 (kept as `plans/devmode-plan-v3.1.html` / `.md`). The user's answers to v2.1 and v3 (artifact 2ugbTkkAFkEsgTZa3bbFdH, collection `answers`, docs `devmode-plan` and `devmode-plan-v3`) stay decided: Dev link and own Dev save; Set career always a new Dev game; wake 06:00 in bed, beat shortcuts go on to the beat's time and place; starting friendships; workdays excused, needs kept, Top up; rank by hand allowed, marked approximate; three stops with Big events last; today's tradition under the fade; Undo; Take me to and Mark. The user's comments asked for less complexity ("I want to be able to test the traditions and career progression"), so v4 adds no new machinery: jumps are Set career with a landing.

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

## Turns (about 20 hours)
- J0 (A, 3h): `DM_JUMPS` + `devmodeJump({...})`, the Jump to tab, the runner, DM_MAXDAY 40, rank buttons, Senior/Specialist by hand (approximate), Day 1 try, empty blocks J1-J3, stub check parts; measure a Day 36 jump.
- Then side by side: J1 (A, 4h) career + nights, part `beats`; J2 (B, 4h) ship events + running card (Next phase, threads -/+, its meeting, End and undo, End and keep), part `events`; J3 (C, 4h) ending + answers row + next showing, parts `ending`, `trad`; J4 (first free, 3h) the arrow, dev_arrow_check `s6`, `ev`, `end`.
- J5 (A, 2h): DEV_NOTES, design-doc, build table, full round on six runners.

## New questions (recommended first)
1. Events: jump to their calendar day (plus the agreed running tools), not 3.1's Start today/tomorrow.
2. Diplomatic visit: not until it's on.
3. Answers row (Engines/Bridge/Teach/Unsure; Stay/Go/Unsure), Engines and Go to start.
4. First-week meetings: try in J0, else keep the recipe.
5. Arrow at event meetings: yes, "Event:".
6. Slow long jumps: measure on a phone in J0; if slow, start from an earlier Mark.
7. Three builders side by side after J0.
