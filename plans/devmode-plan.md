# Dev mode jumps plan: summary

DM1 (Dev mode engineer) for lead 43, 2026-10-28. Branch `claude/devmode-plan`, from `claude/staging-pad` (0.95.0 + controller work). Full page: `plans/devmode-plan.html` (published for the user, with answer boxes). Plan only: no game or check change. Building waits until the controller round passes and the user says go. DP1's earlier plan (v3.1, already built as Stops 1a-2) is kept as `plans/devmode-plan-v3.1.html` / `.md`.

## Audit (section 25 on staging-pad)
- Works: clock, Take me to, Mark/Undo/Copy real game, Speed card, Step 3 beats, the Engine Specialist beats (t4, t4res, t4badge, t4move), mentoring, Calder's question (landing only).
- Partly: traditions (any one started, but no cake/invitation/flag and nothing tied to an event; no "go to its real next showing"); Set career (Days 0-30 only, stops before the vessel, crossing back, ending); ranks (by day; by hand only Junior/Officer); Step 5 (Next step only, no landing); first-week meetings (play-once recipe); the career arrow (silent after the Deck 2 move).
- Missing: ship-wide events (Big events tab is a placeholder), running-event controls (eventFinish is ready, unused), the Monday briefing, nights 1-3 (Reyes, the reactor, the coil swap), the ending (offer, answer, address, goodbye, end page, staying on).
- Not in scope: the Diplomatic visit (still a draft, off).

## The plan
- One new tab, **Jump to** (replaces the empty Big events tab), about 40 jumps in four groups: Career, Nights, Ship events, The ending.
- A jump = Set career with a landing: a fresh Dev game run forward day by day to the moment; events happen on their own calendar days by the game's own rules; your choices on the way (Calder's question, the offer) go through the game's own functions (`cqAnswer`, `endOfferDone`, `endSay`); clock stops a few minutes before; you're placed in the room.
- Set career: Day range 30 -> 40, rank buttons (Cadet Day 2, Officer Day 11, Senior Day 17, Engine Specialist Day 23).
- Running event card: Next phase, Its meeting, End it now (`eventFinish`). No events off their calendar day.
- Traditions card: Go to its next showing (clock jump, up to 14 days).
- Career arrow: follows nights, briefing, Basil, Calder's question and the ending from each piece's own Schedule rows (`p5nItems`, `m23Items`, `m24Items`, `mtItems`, `cqItems`, `endItems`); optionally event meetings ("Event:").
- Safety: real save never written; no R(); two identical jumps give the same save; planner reads only the game's own settled records (SHIP_DAYS cleared where one is settled); nothing without #dev; section 26 untouched.

## Turns (about 20 hours)
- J0 (A, 3h): `DM_JUMPS` + `devmodeJump({...})`, the tab, the runner, DM_MAXDAY 40, rank buttons, Day 1 try, empty blocks J1-J3, stub check parts; measure a Day 36 jump.
- Then side by side: J1 (A, 4h) career + nights, part `beats`; J2 (B, 4h) ship events + running card, part `events`; J3 (C, 4h) ending + answers row + next showing, parts `ending`, `trad`; J4 (first free, 3h) the arrow, dev_arrow_check `s6`, `ev`, `end`.
- J5 (A, 2h): DEV_NOTES, design-doc, build table, full round on six runners.

## Questions (recommended answer first)
1. Fresh Dev game for every jump: yes.
2. Events on other days: no; calendar day only, plus Next phase / End it now.
3. Diplomatic visit: not until it's on in the game.
4. Answers on the way: an answers row (Engines/Bridge/Teach/Unsure; Stay/Go/Unsure), Engines and Go to start.
5. Setting the storm's result: not now.
6. First-week meetings: try in J0, else keep the recipe.
7. Senior/Specialist by hand: no, rank buttons on Set career.
8. Arrow at event meetings: yes, labelled "Event:".
9. Slow long jumps: measure in J0; if slow, start from an earlier Mark.
10. Builders: three side by side after J0.
