# Handover: the traditions engineer (seat 5, Pillar 4): START HERE

Written at **0.34.34** (claude/ship-events a597a37, 2026-10-17 ~04:40) by session_018WZccmSvEfz2LC7DCfxdii, handing over at about 70% memory. The older notes further down (Pillars 2-3, the storm, the diplomatic visit) still hold.

## Update at 0.34.37 (traditions engineer 2, session_01WEEoe5DyRegEqVMZgKRHWB)
- **Lead now session_01KPJMYjXAPkNUcrQ8VRkhLE** (from ~04:35). Items 1-2 below are done:
  - 0.34.35: the bridge invite. `OCCASIONS.bridgeInvite` is a `chance` occasion (no appointment, notice or Mail first). Its `slot(d)` is Vance's mess breakfast (`occMealSlot`), and it's due on the day before a bridge hour (`occBridgeEve`). The occasion's `flag` is set when it closes (kept or missed). Meeting replies now set their `flag:`. The .meet file is copied unchanged from claude/content.
  - 0.34.36: weekly e9a88ff and monthly a93bf36 collected.
  - 0.34.37: `tradOn(id, t)` for social B's calls home.
  - 0.34.38: reviewer 2's LOW notes: TALLY_MEMO cleared on a flag change; guestStay guarded.
  - 0.34.39 (b13bf54): merged ship-integration f28e48e (0.60.1); the one-week-aboard tea moved to 17:15 (Zeke works until 17:00); `evEvening` (an evening's tradition starts from 17:00 and runs past 18:00); events_check allows a host 5 minutes early (section 14's rule). Waiting: the seasons designer to take the .trad change. 0.34.40: Tiles night's tally dropped (weekly c19adf9; results are section 23's).
  - 0.34.40-0.34.41: weekly c19adf9 (no Tiles tally) and seasons 976a8d4 collected.
  - 0.34.42 (0c40589): upcomingTraditions gives `deck` and `room` (device engineer 3, session_01SskqNx45iEGyQq2W9Fjg5Y, schedule heads-ups).
  - 0.34.43 (234a454): crew rotation traditions (farewell supper, crew welcome tea): `when.rotation`, `evRotation`, the words friends/dept/bunk-of-honoree, events_check 9d. All the seasons designer's traditions are now baked (23).
  - 0.34.44-0.34.46 (latest 0.34.46): an occasion gives no toast when the device is in (it lists SHIP.occasions itself; apptAdd exists nowhere). A cake at the crew welcome tea. The seasons designer's 0e757b1 and 92bb1c9 (plural names, longTables at the farewell supper, a cake line).
  - 0.34.47-0.34.48 (latest 4631a97, reviewer 2 passed up to 774eeb7): {first} per speaker with several honorees; the long-table seats (`where: 3 pool @long-table`, the deck architect's a71ac47) at the Sunday table, harvest supper and farewell supper.
- **Designers:** the weekly (session_01Wr9Jcc4nRUHHWdfJDUwb3X) and seasons designers are inactive. Their branches lack my later edits to their files: sunday-table, one-week-aboard, farewell-supper, crew-welcome-tea and harvest-supper. A successor merges claude/ship-events first.
- **Superseded below:** the seasons designer and the galley are answered. Night-shift honorees are fixed in sim engineer 4's (session_01EJUGywZv9BpcUezjXES9AC) 0.26.31, not yet combined: re-run events_check 9d after the next combine. Still waiting: the deck architect on extra long-table seats (with sim 4) and on longTables for rotation Saturdays.
- **Waiting (0.34.43):**
  - The seasons designer: merge 234a454; the farewell Mail's "{names} leaves" with 2-3 leavers; decor; the jam dropped on welcome-tea Fridays.
  - The galley: the supper's favourite dish.
  - The lead: successors for the sim engineer (night-shift honorees get no gatherings) and the dialogue engineer (heads-up only); both sessions are inactive.
- **People:** social B2 = session_014A3w2gK8FBNWs66YC3LfME (owns the calls home; offered tradOn plus start/end hooks, waiting for their shape). Head writer 2 = session_01HNrh3xCtczeZM5NVFrE6pa (told about the invite).
- **Open:**
  - EV_MAILBOX's cap is 40, not 20 as its comment says. events_check part 3 passes with it (days 2-8). Fix the comment in the next build; raise the cap if part 3 ever says "no Mail for".
  - The cut decor (mendingTable, rummageCrates) appears nowhere here.
- **Gotcha:** events_check's later parts leave the clock past day 30, so a part that needs an earlier day must set the clock (`setShipNow` + `eventsTick`), not `skipTo` backwards.

## FIRST, for the fresh session (open items after 0.34.34)
1. **Play the bridge invite** (the lead, 04:20): the head writer's `content/meetings/bridgeInvite.meet` (claude/content aa50647) bakes into `MEETINGS_BAKED` and reaches `MEETING_SCRIPTS` through section 22's `linesMeetings` (hook already in section 18). Schedule it as a section 18 meeting: Vance at breakfast in the mess on day 22 (the Monday before the first possible bridge hour, day 23), or the first meeting with Vance from day 15; every reply sets `flag:bridge.invited`. Bridge hour is already gated on that flag (0.34.34). Pattern: `meeting({ id, where, at, who, script })` as the storm's briefing does, or an occasion in `OCCASIONS` (kind 'meeting'); test in events_check like the briefing (the flag set after a reply; bridge hour then due on day 23 if it's a week-4 Tuesday: check).
2. **Collect** claude/trad-weekly e9a88ff (late piano's texts for two nights) and claude/trad-monthly a93bf36 (notes only); re-bake.
3. **The deck architect's tally props:** cupBoard takes `{ id, lines }` like tastingTable (decks-p3 021a553); `tradDecor` already sends title and lines for any decor with a tally.
4. **The galley** (944f520) relies on `tradTies`' `{ id, from, to }` and the tally choices' dashed ids: keep both. It reads the crossover dish too, but crossover supper is cut.

## Role, branch, builds, people
- **Role:** section 18 SHIP EVENTS: the ship traditions (hand-written `SHIP_TRADITIONS` + the designers' baked ones), ship-wide events, meetings, occasions; `events_check.py`; the `.trad` grammar (`plans/trad-format.md`, `plans/trad_parse.py`); collecting the three tradition designers' files; the Traditions calendar page.
- **Branch:** `claude/ship-events` only (never push elsewhere without the user's explicit permission: the lead once asked for a side branch; I sent the build master a diff instead). Builds 0.34.19-0.34.34; next **0.34.35**. Combined builds are the build master's (session_012K7RZ3oSX2vpBb1rR66MBh): 0.60.0 had up to 0.34.24; 0.60.1 = ca8c040 + the birthday diff; 0.60.2 should take a597a37.
- **Chain of command:** the user -> the lead (session_01PJtmxWgAPLebXSZKP6ZRpG) -> everyone. Never contact the user. Talk sideways to owners directly; copy the lead on decisions only.
- **Reports to you:** the designers: weekly session_01Wr9Jcc4nRUHHWdfJDUwb3X (claude/trad-weekly, k 435-454), every few weeks session_015dAEQhLUgkxejuzQF5CsV9 (claude/trad-monthly, 455-474), seasons/year/life session_01GnWSW6a2D1XdABqpCpVjaY (claude/trad-seasons, 475-499). Head writer (tone): session_016i7YYgZd6puKxfBSkLggRF.
- **Peers:** dialogue session_01UmrVVpV7eBqEsa4sBucASP (content_gen.py bakes TRADITIONS by calling trad_parse.read_all; tell them before changing trad_parse's functions or output), sim session_01R6RBwwBM9aorpsqDCrztDU, galley session_018cicfPQZQXbxmtn6ygmL84, deck architect session_01ToE6RJFCw9deB3HcJRLKxS, social A session_012pK2XVi5UhqEd28fakYk68, social B session_019aEJaAGyZir9oq47CBRfA3, onboarding session_01KaHzfqSqF8B4bkNFrH1tsx, Tiles session_01DG3in6CvFFta6NrLpoVCJV, reviewer 2 session_0142TQw4ke8caPSyAC93VT98.

## What section 18 has for Pillar 4 (see the DEV_NOTES rows 0.34.19-0.34.34)
- **Rhythms** (`evDue`): weekday (one or a list), every week/2/4 weeks with a week index, quarter, year, after arrival (`introArrival()`), season/from/until filters. **Seasons:** `season(d)`, `seasonOf(d)`. **Flag gate:** `ev.flag` (bridge hour: 'bridge.invited').
- **Loader:** section 22's generated `TRADITIONS` (array) -> `tradLoad` -> `SHIP_TRADITIONS`. Rules as data (`tradIs` words incl. night-shift/day-shift), texts with placeholders, nobody names themselves, `TRAD_ERRORS`.
- **Voice budget** (`evBudget`, `EV_DROPPED`): two an evening, never two at once on a deck; prio, rarity, earlier start, order. Birthdays exempt, and only for crew aboard that evening (not their leaving day).
- **Ties:** `tradTies(kind, d)`; decor via the deck architect's `dressShow` (`tradDecor`); traces (`traceAdd`, `{ id, day }`: seedlingYours, mugYours); `meal` on eventPlan entries (the sim builds it); tallies (`tallyOf`, `tallyVote`, `tallyLast`; per, mode=teams).
- **Mail:** evening-before Mail, one per evening (bundled); the Sunday "This week aboard" (`WEEK_MAIL`: a copy of content/traditions/this-week-aboard.mail; events_check fails if they differ).
- **Notes on the bus:** `simNote('tradition', { id, day, at, came, you, host, src, tally })`, `simNote('choice', {...})`. Hooks for 20c: `onPick`/`onEnd` on moment scripts (moments don't count as meetings).
- **The storm** stays on day 10 (`spread`). The ready room's replies carry `mem`.

## How to collect a designer's batch
`git fetch origin claude/trad-<x> && git merge origin/claude/trad-<x>` -> fix leftovers -> `python3 plans/trad_parse.py` -> `python3 content_gen.py` -> `python3 lines_check.py` -> bump the build -> events_check (it plans each tradition's first day of the year, a whole year on paper, the budget, flags, tallies, decor/trace ids against DECK_DRESS + its ANNOUNCED list, the Sunday Mail) -> cadet_test against the last build (label matched) -> a day_check on a busy day -> DEV_NOTES row -> commit, push -> the lead (summary), the build master (commit), the designers and owners. Regenerate the calendar: `python3 plans/traditions-calendar-gen.py`.

## Loose ends (as of a597a37)
1. **Pre-existing:** events_check fails on day 231's dayReport double booking (3-store-1, esposito-yara/ishikawa-orla at 14:30), in 0.60.0 too. The sim engineer has it.
2. **Meal traditions** are thinly attended until the sim engineer makes `meal` BE dinner/breakfast (asked).
3. **The galley** (asked: pancakes, the tasting batch, Sunday's side via tallyLast, the suppers, cakes): their plan is in their messages; they read tradTies and tallyLast.
4. **The deck architect** is building the decor (longTables, harvestTables, cupBoard, talentStage, yearsEnd, openLab), and has built places (rummage places now unused since rummage day was cut: tell them), mugYours. If they rename an id, update the files and events_check's ANNOUNCED.
5. **The designers' next steps:** the head writer's tone pass; the weekly designer to check late piano's texts for two nights; the monthly designer to check talent night's texts for once a year; the seasons drafts (farewell supper, crew welcome tea) wait for crew rotation triggers (`when: rotation -1`, honorees from ROSTER_ROTATIONS, words friends-of-honoree etc.): build them when the lead says.
6. **Tiles night's results:** asked the Tiles engineer whether they live in section 23 (suggested) and what function to read for the note.
7. **Your vote:** `tallyVote` is ready; the device will call it later (the lead's ruling).
8. **This week aboard:** copy WEEK_MAIL again whenever the monthly designer changes the .mail file.

## Gotchas
- cadet_test's g_nocrew shot sometimes catches section 15's "+N Energy" label (about 1921 px): re-run; compare a build with itself to prove it.
- Run browser checks one at a time. events_check takes 6-10 minutes now; run it in the background and wait for the notice.
- Merging ship-integration: only the HUD line (198) and GAME_BUILD clash; take theirs, then set your build.
- `typeof X` is safe for function declarations anywhere and for consts defined earlier in the file; section 22 sits before 18.
- Don't put a `// comment` inside a one-line object literal.

# Handover: the events engineer (ship traditions)

Written at build 0.34.6 and updated at **0.34.7** (Pillar 3, C6 step 1, on top of combined 0.41.4) so a fresh session can take over. **The next events engineer starts here.** The full notes are in DEV_NOTES.md, "Ship events (section 18)". This page is the short version.

## Role, branch, builds

- **Role:** the ship's small recurring traditions: quiz night, the jam, birthdays, Founding Day and so on. The user calls them **ship traditions**; the big story ones (the ion storm) are **ship-wide events**, Pillar 3.
- **Branch:** `claude/ship-events`. Builds 0.34.0 to 0.34.7; the next is 0.34.8.
- **In the game file:** section 18, `// 18. SHIP EVENTS`, after section 17 and before section 6. Outside it, only typeof-guarded one-liners:
  - section 14 (the sim engineer's): `eventPools(shared)` in `schedData`, and `gatherings(p, d, F)` turning `eventPlan` entries into gatherings; the reservation in `shipDay` reads `eventPlaces(e)`;
  - section 10: the tap toast reads `eventLine(p, t)`;
  - the main loop: `eventsTick()` after `worksTick()`.
- **Test script:** `events_check.py` (mine).

## What's built

- `SHIP_EVENTS`: 12 traditions (see the table in DEV_NOTES). Each has when, time, where (pools of places), who (a chance per person), what they do (anim), hold, cake, decor, and the texts (Mail, tap lines, the thanks toast).
- `eventsOn(d)`, `eventPlan(p, d)`, `eventPools`, `eventPlaces(e)`, `eventLine(p, t)`, `eventsTick()`, `EV_MAILBOX` (the last 20 announcements, for the Pillar 3 calendar), `SHIP.events` (sent and joined, saved as `ship.events`).
- Mail the evening before at 18:00 ("Ship tradition: Quiz night, Thursday 20:00"), quiet before 06:30 on Day 1 and after skips.
- The player joins by being in the room for 5 ship minutes: social +12, a toast, a quiet thank-you.
- Decor: swap-meet stalls; a stand-in cake only when section 16 (the galley) is absent.

## Agreements with other roles

- **Sim engineer** (section 14): one events system, mine. Their `gatherings()` takes my entries; their old birthday and observatory night are gone. They hold `eventPlaces(e)` for each event's window (0.26.12). Hash keys: mine 320-333 and 420-433; theirs 500-515 and 9100/9200; the galley 301 and 310+.
- **Galley engineer** (section 16, 0.29.15): bakes for any event with `cake: true` (birthdays, Founding Day), cake out on the servery 19:30-21:30; the noon Mail gives the gathering time; harvest days add a garden salad to dinner.
- **Crew designer:** `ROSTER[i].birthday` (1-364); `birthdayOf` falls back to a stand-in only without it.

## Gotchas

- Section 18 runs after section 14 in the file. `eventPools` and `eventPlan` return nothing until `EV_READY` (a `var`), and section 18 clears the plan caches once when it loads.
- Tags are `ev-<id>` or `ev-<id>-<anim>`; `eventTags()` registers them in section 10's `TAG_ACT` on the first tick. `eventLine` and joining read them back from `planDay`, so gatherings must pass the tag through unchanged.
- `hold` decides what's reserved: default the first `where` entry; big events (`founding`, `hull-lights`, `quiet-watch`) hold nothing, or they'd empty the mess at dinner.
- events_check resets `SHIP.galley` before each deck run (jumping weeks ahead with no carts empties the cold store), and draws settled frames (one frame straight after a camera jump over-counts draw calls).
- `.gitignore` has `*.png`: screenshots in `plans/shots/` need `git add -f`.

## How to test

`CADET_CHROME=/opt/pw-browsers/chromium python3 events_check.py BUILD.html [DAYS]` (about 5 minutes). Good looks like "EVENTS CHECK OK": every tradition when due and never otherwise, people at it, only its places and window, dayReport clean, same plans twice, everyone reaches their place on the deck, draw calls under 450, decor on and off, one Mail each at 18:00 the evening before, one cake (the galley's), the player joins the quiz, a tap line. Run the others one at a time too (deck, day, food, machine, player, cadet_test).

## Open questions for the user

- Should more traditions come in (a first-shift welcome for new arrivals, a card night, a Captain's tea)?
- Should joining a tradition do more than a little social (friendship with those there, once relationships exist)?
- Pillar 3: the device's Calendar reads `eventsOn` / `EV_MAILBOX`; ship-wide events may reuse the gathering machinery.

## Pillar 3: where it stands at 0.34.18 (the second events engineer, session_01GW9QtevJxaMQzzCGPBHaxb, on standby)

The user, 2026-10-16: finish the diplomatic visit, keep it switched off, and stop: "we will do the rest later". Read plans/pillar3-plan.md (on `claude/lead-pillar1`): Part 2, Part 4, "Shared formats" section 18, and rows C6 and C10. DEV_NOTES "Ship-wide events" and the build table (0.34.8-0.34.18) have every detail. This is the short version.

- **Branch:** `claude/ship-events`, builds 0.34.8 to 0.34.18. ship-integration 0.41.5 and 0.41.6 are merged in. Report to the lead, session_015QoyPWBdMPM4ywf5W2jMMs.

### What's built

- **The ion storm is ON (0.34.12)** in `SHIP_EVENTS.ionStorm`. It's due on the first day from 8 on when Calder is on shift (day 10 in a new game). It has the full data: phases to the end of day 5, systems, routines, needs, galley, jobs, news, moments, meetings, address, mail, threads, traces, dressing and the debrief.
  - Thread scorers: blackout (systems 0.33.26+), spoiled and bridgeHungry (galley 0.29.21), calls (here, `stormCallBacklog`).
  - The all-clear party reaches plans through `eventPlan` (`EV_SHIPWIDE`). The sim engineer runs the routines from `eventRoutines`.
- **The diplomatic visit is built, `draft: true` (0.34.16-0.34.18).** `SHIP_EVENTS.diplomatic` would start day 25 in a new game: 7 days after the storm, on a day Vance works.
  - Vance's Mail on day 0.
  - The greeting in the shuttle bay at 10:00 on day 2 (meeting `veyliGreeting`).
  - Formal dinners on days 3 and 5 (the galley's `batch` of 10, a function of the day).
  - The gift exchange on day 7 at 09:00 (meeting `veyliGiftExchange`), then the farewell gathering at the shuttle bay.
  - The guests (GUESTS with event 'diplomatic') are aboard days 2-7 (`guestsArrive: 2`, their stay 5). `eventMod('effect', 'guests')` is on for those days.
  - Threads:
    - dinnersLate and noHerbs: the galley agreed the shape and will build them (with the `herbs` key) when the lead says go. `extra` and `batch` already work.
    - coldCabins: systems 0.33.31, done.
    - discourtesy: social 0.36.16, done (Holt's warmth toward the guests), plus meeting choices here.
  - Trace `veyliCordSculpture`: done by the deck architect (0.38.5, claude/decks-p3 d34bfe3): a brass ring of knotted cords on the bow lounge's west wall. The shuttle bay's 3 leads are the Captain, Saruth and the Speaker.
  - **To switch it on:** remove `draft: true` (the lead's call, ideally after the user plays the storm). Then run events_check, food_check, day_check 1 and 27 (the greeting day), deck_check, player_check and cadet_test.
- **Meetings:** `MEETING_SCRIPTS` holds calderStorm, captainAllClear, veyliGreeting, veyliGiftExchange, readyRoomFirst, captainsTable and calderProgress.
  - `meetingsTick` plays a script when you're in the room. `meetingCast` fills casts from ROSTER, the guests (`evPerson`) and 'works:2'.
  - Section 19's `deviceDialogue(view)` draws the panel, and its taps call `dialogueNext`, `dialogueChoose` and `dialogueClose`.
  - A choice can nudge relationships (`relAdd`), take an event job (`eventTakeJob` always records 'wants:') and nudge a thread (`thread`).
- **Felt everywhere:** `eventFeel` -> the performance engineer's `shipFeel`, else my stand-in.
- **The address:** `captainAddress` -> section 19's `deviceAddress`.
- **Occasions (C10, 0.34.11):** readyRoom (the summons after your first commendation), captainsTable (every 28 days), progressTalk (`occasionAsk`). Commendations at an event's end. `occasionDoorOpen` is read by the sim's `doorOpenFor`.
- **Hooks for others:**
  - section 14: `eventOn(d)`, `eventGatherings(d)`, `eventRoutines(t)`, `callOwed`, `eventGuestDays(g)`;
  - section 20: `eventOneOff` (Pell's show, host first);
  - the galley: `eventMod(kind, key, t)` with a minute;
  - systems: `eventJob` and the 'wants:' claim;
  - `newsAdd` and `dressShow`.
- **Hash keys (mine):**
  - 320-333 and 420-433: traditions;
  - 336: callOwed;
  - 337: meetingCast;
  - 340: the storm's party;
  - 341: one-offs;
  - 351 up: other ship-wide gatherings (the Veyli farewell is 351);
  - 4242: due days.
  Section 20 has 600-643, sim 500-515 and 9100/9200, the galley 301 and 310+.

### What's left (later, when the user says)

- **Comet viewing** (the short event between the storm and the visit): drafted and tested on paper, then held back. It's all in `plans/comet-viewing-draft.js`: the data block and the events_check parts, with how to paste them in.
- **The rest of the plan's list, in order:** crew rotation day (short), something in the garden, power surge (short), shipboard illness, the Founding Day festival (short; only once the phone test allows big crowds), nebula drift, the late supply shuttle (short), salvage, a Veyli vessel needs help (short), the déjà vu day. The full order is in the plan's Part 2.
- **The conference table** (Part 4) waits for an event with a senior briefing. Officers' quarters invitations are section 20's.
- **Known:** the storm's warning Mail goes at 06:00, before Calder's 08:15 briefing. A debrief comes at the end of the afterglow.

### Open threads with other roles

- Galley: dinnersLate, noHerbs and the `herbs` key for the visit: agreed, waiting for the lead's go.
- Device: `apptAdd` for occasions; Record reading `SHIP.occasions` (kept) and `SHIP.commendations`; a lasting count of your jobs (`yourJobsDone` reads `SHIP.jobs`).
- The player now has two days off a week (Sat/Sun; the sim's `playerShiftOn`). Meetings and occasions still play on days off. Missing one is never missed work.

### Tests

events_check covers:
- the traditions;
- the storm on paper twice (identical);
- a live storm (briefing, front, all-clear, end);
- the occasions;
- the hooks (party, routines, guests, one-off);
- the diplomatic visit on paper twice, plus a live greeting (it lifts the draft for the run).

Before each push, also run cadet_test against the previous build, deck_check, day_check 1 and 13, player_check and food_check.

### Gotchas

- `eventNow(t)` is pure: running event, then the log, then the next due. It never runs past `days`.
- `MEETINGS` dedups by id and minute, and events_check saves and restores it.
- `newsAdd` and `dressShow` live in the game's scope (not on window). events_check reads `NEWS` and wraps `dressShow` in scope.
- Anything added to `evTable()` adds pools to `schedData`. `eventOneOff` clears `SCHED_DATA` and later plans. Tests that lift a draft must clear `SHIP_DAYS`.
- Never put a `// comment` in the middle of a one-line object literal: it swallows the rest of the line. I did this twice; it breaks the game's start-up silently.
- Meeting scripts must be added after `const MEETING_SCRIPTS` (below the meetings section), or the game won't start.

## Pillar 4: the traditions engineer (seat 5), from 0.34.19 (session_018WZccmSvEfz2LC7DCfxdii)

Read plans/pillar4-plan.md (Part 4, Part 5's Tiles night, Part 6 seat 5) and plans/social-deep-plan.md (Parts 5-6: invitations, `simNote('tradition')`). Report to the lead: session_01PJtmxWgAPLebXSZKP6ZRpG from 2026-10-17 ~02:40 (before: session_01PxXKwc5mkC7tV5MPi3p7PP). Chain of command: the user -> the lead -> everyone; helpers never contact the user.

- **0.34.19:** new rhythms in `when` (`evDue`), `season(d)` / `seasonOf(d)`, `tradTies(kind, d)`.
- **0.34.20:** the TRADITIONS loader (`tradLoad`, `TRAD_ERRORS`), the `.trad` grammar (`plans/trad-format.md`), the reference parser (`plans/trad_parse.py`), the sample Sowing morning (`content/traditions/sowing.trad`, k 434). events_check: a whole year on paper.
- **0.34.21:** `simNote('tradition')` after each (`eventsNoted`), the voice budget (`evBudget`, `EV_DROPPED`), the format agreed: content_gen.py (the dialogue engineer, session_01UmrVVpV7eBqEsa4sBucASP) owns the TRADITIONS block and calls my `plans/trad_parse.py` for field lines; `TRAD_STANDIN` until it's merged (delete then).
- **0.34.22:** `invite: { host, odds, line }` on six of the twelve (for social A7).
- **0.34.23:** reviewer 2's fixes; trad_parse.py's API frozen (tell the dialogue engineer before changing it); Tomas always at Sowing morning (onboarding's day 6 invitation).
- **Peers:** dialogue session_01UmrVVpV7eBqEsa4sBucASP, sim session_01R6RBwwBM9aorpsqDCrztDU, onboarding session_01KaHzfqSqF8B4bkNFrH1tsx, social A session_012pK2XVi5UhqEd28fakYk68, build master session_012K7RZ3oSX2vpBb1rR66MBh, reviewer 2 session_0142TQw4ke8caPSyAC93VT98 (reviews this branch).
- **Open for the seasons designer:** Sowing morning and harvest morning share days 6 and 188 (Sowing follows at 11:45).
- **Next:** the Sunday "This week aboard" Mail (with the monthly designer); then collecting the three designers' files.
- **Gotcha:** cadet_test's g_nocrew shot can catch section 15's "+N Energy" need label (a real-time fade): a 1921 px difference that vanishes on a re-run.
- **Hash keys I give out:** 434 sowing. Blocks for the designers: weekly 435-454, every few weeks 455-474, seasons/year/life 475-499 (each designer numbers within their block; I check they're unique). The three designers report to me; I summarise for the lead.
- **0.34.24-0.34.26:** simNote('choice') on meeting replies; events_check fails on an unloaded .trad; the storm pinned to day 10 (`spread`); tradition props (`ties.decor` -> the deck architect's DECK_DRESS via dressShow) and `trace` (Sowing: seedlingYours { id, day }).
- **Agreed with the sim engineer (0.26.24):** hosts are planned first (5 minutes early, may join half late); errands don't start within 70 minutes of a gathering; dinner moves around one. For meal traditions (Sunday roast, harvest supper, long breakfast, the 06:00 crossover) put `meal: 'dinner' | 'breakfast'` on the eventPlan entry (from the tradition) and section 14 eats there instead of the servery: send the sim engineer the concrete asks when the designers deliver.
- **0.34.28-0.34.30 and the calendar:** on top of 0.60.0; TRAD_STANDIN gone (the loader reads section 22's TRADITIONS; re-bake with `python3 content_gen.py` after merging designers). The `meal` field. Designers collected: weekly (claude/trad-weekly, session_01Wr9Jcc4nRUHHWdfJDUwb3X, k 435-454), monthly (claude/trad-monthly, session_015dAEQhLUgkxejuzQF5CsV9, 455-474), seasons (claude/trad-seasons, session_01GnWSW6a2D1XdABqpCpVjaY, 475-499): 24 baked. How I collect: `git merge origin/claude/trad-<x>`, fix `// meal:` style leftovers, `python3 plans/trad_parse.py`, `python3 content_gen.py`, `python3 lines_check.py`, bump the build, events_check (it also plans each tradition's first day of the year), cadet_test, a day_check on a busy day; DEV_NOTES row; tell the lead (summary), the designers (notes) and owners (asks). The Traditions calendar: `python3 plans/traditions-calendar-gen.py` -> plans/traditions-calendar.html (the lead publishes).
- **Open (0.34.30):** garden hour loses Mondays (weekly to move it); the sim's `meal` work; props asked of the deck architect (events_check's ASKED list); the tallies (tasting, tiles-night, cup, harvest-best); the Sunday "This week aboard" Mail (content/traditions/this-week-aboard.mail, monthly's words); crew rotation triggers for the seasons drafts (farewell supper, crew welcome tea); day 231's pre-existing store double (sim).
- **0.34.31-0.34.32:** the Sunday "This week aboard" Mail (`WEEK_MAIL` is a copy of content/traditions/this-week-aboard.mail: events_check fails if they differ, so copy again when monthly changes it); tallies (`tallyOf`, `tallyVote`, `tallyLast`, `per`, `mode=teams`; on the ship note and on a tally decor's chalkboard). Waiting: the Tiles engineer (session_01DG3in6CvFFta6NrLpoVCJV) on Tiles night's results; a way for you to vote (device or interactions engineer, `tallyVote`); the lead's answer on passing the galley's asks directly.
