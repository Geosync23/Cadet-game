# Dev mode plan v4.4: summary

**v4.4 (lead 43, 2026-10-28):** the user's q2 comment "Switch it on now" = include the Diplomatic visit. Its jumps are added to Ship events (J2 +1.5 h; total about 24 h, about 50 jumps): Vance's memo Day 16 08:25, the Veyli aboard Day 17 09:55 (shuttle bay), the guests' day Day 18, the formal dinner Day 18 evening, the gift exchange Day 19 08:15, the farewell Day 19 08:55. Found: `SHIP_EVENTS.diplomatic` still has `draft: true` (staging-pad line ~46550; the swap block reshapes it but never clears it; evCalPlan passes drafts over), so the visit doesn't run in a real game (CA1's Day 36 runs: no visit; events_check sets draft false only while it tests). Reported to lead 43 for the events side; the jumps work once the mark is removed.

**The user's answers (2026-10-28, doc devmode-plan-v4): decided.** 1 calendar day; 2 "later", with the comment "Switch it on now" (lead 43 asking what they mean; not acted on); 3 answers row; 4 try in J0; 5 arrow at event meetings yes; 6 ALL (full ~45 jumps / ~22 h, not the first cut); 7 three builders; 8 drop End and undo (cut, recorded in design-doc). Design-doc "Dev mode" updated. J0 waits for the controller round (lead 43's go).

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
- F8 (second pass, d5fb07c): End and undo put to the user as question 8: (c) drop it, recommended; (a) keep the event's first-morning Dev save (~116 KB) to go back to, about 2 h more; no section 18 change either way (no restore point inside a jump's run; ending without logging restarts the event; its purpose is now guaranteed by the fixed calendar). Undo my last Dev action covers going back.
- F9: threads - and + greyed once e.mine.settled; after End and keep the day's crew plans are made again (as devmodeTradsAgain).
- F1 is also a live bug in today's Set career (Days 27-30): backlog DM1-1, fixed by J0.
- CA1's PASS note: J0's devmodeCareerFor takes a "week slow" day offset for the slower career's ending, so J3 never edits J0's lines.
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
8. End and undo: drop it (recommended), or keep a copy of the event's first morning.
