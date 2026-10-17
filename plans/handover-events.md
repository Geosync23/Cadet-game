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

Read plans/pillar4-plan.md (Part 4, Part 5's Tiles night, Part 6 seat 5) and plans/social-deep-plan.md (Parts 5-6: invitations, `simNote('tradition')`). Report to the lead, session_01PxXKwc5mkC7tV5MPi3p7PP.

- **0.34.19:** new rhythms in `when` (`evDue`), `season(d)` / `seasonOf(d)`, `tradTies(kind, d)`.
- **0.34.20:** the TRADITIONS loader (`tradLoad`, `TRAD_ERRORS`), the `.trad` grammar (`plans/trad-format.md`), the reference parser (`plans/trad_parse.py`), the sample Sowing morning (`content/traditions/sowing.trad`, k 434). events_check: a whole year on paper.
- **0.34.21:** `simNote('tradition')` after each (`eventsNoted`), the voice budget (`evBudget`, `EV_DROPPED`), the format agreed: content_gen.py (the dialogue engineer, session_01UmrVVpV7eBqEsa4sBucASP) owns the TRADITIONS block and calls my `plans/trad_parse.py` for field lines; `TRAD_STANDIN` until it's merged (delete then).
- **0.34.22:** `invite: { host, odds, line }` on six of the twelve (for social A7).
- **0.34.23:** reviewer 2's fixes; trad_parse.py's API frozen (tell the dialogue engineer before changing it); Tomas always at Sowing morning (onboarding's day 6 invitation).
- **Peers:** dialogue session_01UmrVVpV7eBqEsa4sBucASP, sim session_01R6RBwwBM9aorpsqDCrztDU, onboarding session_01KaHzfqSqF8B4bkNFrH1tsx, social A session_012pK2XVi5UhqEd28fakYk68, build master session_012K7RZ3oSX2vpBb1rR66MBh, reviewer 2 session_0142TQw4ke8caPSyAC93VT98 (reviews this branch).
- **Open for the seasons designer:** Sowing morning and harvest morning share days 6 and 188 (Sowing follows at 11:45).
- **Next:** the Sunday "This week aboard" Mail (with the monthly designer); then collecting the three designers' files.
- **Gotcha:** cadet_test's g_nocrew shot can catch section 15's "+N Energy" need label (a real-time fade): a 1921 px difference that vanishes on a re-run.
- **Hash keys I give out:** 434 sowing; next free 435.
- **0.34.24-0.34.26:** simNote('choice') on meeting replies; events_check fails on an unloaded .trad; the storm pinned to day 10 (`spread`); tradition props (`ties.decor` -> the deck architect's DECK_DRESS via dressShow) and `trace` (Sowing: seedlingYours { id, day }).
- **Agreed with the sim engineer (0.26.24):** hosts are planned first (5 minutes early, may join half late); errands don't start within 70 minutes of a gathering; dinner moves around one. For meal traditions (Sunday roast, harvest supper, long breakfast, the 06:00 crossover) put `meal: 'dinner' | 'breakfast'` on the eventPlan entry (from the tradition) and section 14 eats there instead of the servery: send the sim engineer the concrete asks when the designers deliver.
