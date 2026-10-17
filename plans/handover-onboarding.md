# Handover: the onboarding engineer (Pillar 4, seat 1)

Written 2026-10-17 by session_01KaHzfqSqF8B4bkNFrH1tsx, after wave 2, before wave 3. A fresh session taking over this role reads this first, then CLAUDE.md, DEV_NOTES.md ("The arrival (section 21)" and "Hook register"), plans/pillar4-plan.md Part 1 and Part 5, and plans/social-deep-plan.md Part 7.

## Role, branch and builds

- **Seat 1, the onboarding engineer:** the arrival and the first week (plan Part 1), then newcomers and your assignment to guide one (Part 5, wave 4).
- **Branch:** `claude/arrival` (push only there). **Builds:** 0.42.x. The last one at writing: **0.42.17** (see git log).
- **Owns:** section `// 21. ARRIVAL` in `starship-cadet.html` (after section 20, before section 6), the one hook line in section 12's main loop (`introTick()` after `socialTick()`), `intro_check.py`, `plans/shots/arrival-*.jpg`, this note.
- **Report to:** the lead, session_01PJtmxWgAPLebXSZKP6ZRpG (took over from session_01PxXKwc5mkC7tV5MPi3p7PP). Tell the build master (session_012K7RZ3oSX2vpBb1rR66MBh) each commit. Reviewer 1 (session_01HK4m33sUiLuVim8VWaCPMs) reviews this seat. **Only the lead talks to the user** (the user's rule).

## What's built

- **Wave 1a (0.42.0-0.42.4), on paper:** `SHIP.intro` (+ `save.intro`), `INTRO_STEPS` (the evening, A0-A13), `INTRO_MEETINGS`, `INTRO_WEEK` (Days 1-7 + the week's flags at 06:00), `SETTLE` (15 items) + `settleNote`, `introBegin/Advance/Done/End/Skip`, `escortPlan`, `introBeats`, `introArrival`, `introWanted`, `introNewGame`, `introSig`, `INTRO_FLAGS`.
- **Wave 2 (0.42.5-0.42.15), the evening in play:** `introTick` (the manifest screen, steps from where you are, meetings on arrival, Torres's bubbles from `INTRO_LINES`, the goal arrow on him, "This way!" calls), stand-in meeting scripts (`INTRO_STUB_SCRIPTS`, used only while the writers' `MEETING_SCRIPTS` of the same id are missing), first launch from the first frame (`INTRO_BOOT` -> `newGameStart(true)`), Torres stays your escort until 19:00 (`introEscorting`), dinner seats (`introSeat`).
- **Walked in the real game** (intro_check part 8): ramp 17:40 -> haulway -> Works door -> lift -> junior wing -> Bunk 1 (meeting, device) -> mess -> table, Calder 18:30 -> released 19:00 -> bed 20:00. Nothing missed, draw calls 192/209/292.
- **Decisions made here** (all recorded): skip = "I know the ship" (the evening's points, every gate open, no scripted week; design-doc "Arriving by shuttle"); waits count from the last minute you got nearer, 5 minutes once you're missing steps; the first-launch design is one path (section 21 decides).

## Shared formats others read (keep stable, or tell them)

- `SHIP.intro = { on, step, since, near, day, done: { stepId: shipMin }, missed: [ids], settle: { itemId: shipMin, all }, skipped, ended, escort, flags }`. `done` is a MAP, not a boolean (social A once misread it).
- Step ids: manifest, ramp, hello, haulway, works, lift, wing, bunk, toMess, servery, chief, free, tomas, night; week: d1-wash, d1-briefing, d1-shadow, d1-lead, d1-dinner, d2-solo, d2-health, d2-booths, d3-pick, d3-store, d3-pell, d4-mail, d4-favour, d4-quiz, d5-mug, d5-invite, d6-sowing (11:45, after harvest), d7-calder, d8-done, dN-flag.
- `introStep` notes: each evening step, d1-briefing, d6-sowing, d1-shadow / d1-lead (from section 17's job turn-in of reserved slots 1 / 2, `introJobNote`), done / ended.
- Flags (section 13's store): `escort.torres-zeke`, `week1`, `intro.device`, `met.calder`, `week1.d2`..`d7` (06:00), `week1.done`, `mug`, `seedling`.
- Read by others: player engineer 3 (`bagTick`: step 'ramp', `done.bunk`, `missed`; `deviceLocked`: `intro.device`), device engineer 2 (SETTLE, `settle`, `introEnd`, `introSkip`), social A (`socIntroOn` uses `introOn`; `escort.<id>`), traditions (`introArrival`), sim (`introBeats`, `escortPlan`, `introSig`, `introNewGame`, `introWanted`, `introSeat`).

## Loose ends and what's next

- **Wave 3, done so far (0.42.16-0.42.17):** the week's jobs held at Monday 05:00 (`d1-jobs`, not at the arrival: a new game's clock rewind wipes SHIP.jobs), `jobRelease` on end, the week's meetings in play (`introWeekMeetings`), Torres follows on the shadow shift and talks it through (`INTRO_JOB_LINES` or the writers' `walk.job.*` lines), dinner seats live (Torres waits at his seat and sits; Calder via `crewComeTo`), absent cast trimmed from meetings (`introScriptHere`), writers' walking lines via `lineFor`. intro_check part 10 covers Monday (with section 17).
- **Wave 3 (still to do):** the first week in play. Monday 07:50 briefing (meeting `introBriefing`, needs a stand-in script or the writers'), the shadow shift: call systems' `jobReserve('lights', 1, 480, 1)`, `jobReserve('washer', 1, 780, 2)`, `jobReserve('lights', 2, 465, 3)` from `introBegin` (not on skip), `jobRelease()` from `introEnd`; Torres follows (`INTRO_WEEK` d1-lead has `escort: 'follow'`) and talks you through the stops (section 17's `job` notes: take, stop with tag fetch/make/job, done, turnin); Tuesday's solo job (slot 3) from Calder's meeting `introSoloJob`; mark job-loop tips seen when Torres teaches them (the interactions engineer's tips); the Tuesday health check appointment `intro-health` (section 14's `apptKept`). Then intro_check: the week in the real game (reserved jobs reachable and completed, the follow switch).
- **Watch:** section 10's `escortGoal` looks up `{ deck, room }` in `ROOM_TILES[to.room]`, which may be keyed by room letter, not name: the Monday beats give names. Check before relying on it.
- **Wave 4:** newcomers arriving on the Sunday shuttle (the same code with a crew member as the guided one) and your assignment to guide one (you as the escort; social A10 has the mentee bond).
- **Waiting on others for wave 2's polish:** the writers' scripts and lines (seat 12), player 3's device lock/kit bag/name save/sitting, device 2's Settling-in app and `deviceChoose`, sim 0.26.25 (New game choice, first-launch pair) and seating Torres/Calder at dinner.
- **cadet_test's `g_nocrew` shot is flaky in these containers** (the build against itself differs in about 2 of 3 runs): rerun once before chasing it.

## How to test

- Setup as DEV_NOTES "Testing" (`pip install playwright numpy pillow`; three.js 0.128 in /tmp/cadet-work/three).
- `CADET_CHROME=/opt/pw-browsers/chromium python3 intro_check.py starship-cadet.html` (about 5 minutes; parts 0-7 on paper, 8 the real walk, 9 the first launch and a Day 0 reload). One browser check at a time.
- cadet_test against the previous build (identical: the intro is off at test URLs); deck_check when places change.
- Screenshots: the walk in intro_check part 8 is the base for `plans/shots/arrival-*.jpg` (a scratch script took a JPEG at each step and each meeting line).

## Open questions for the user (through the lead)

- None open. Wave 2's check-in A is the lead's to run.
