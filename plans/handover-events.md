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

## Pillar 3: where it stands at 0.34.13 (the second events engineer, session_01GW9QtevJxaMQzzCGPBHaxb)

Read plans/pillar3-plan.md (on `claude/lead-pillar1`): Part 2, Part 4, "Shared formats" section 18, rows C6 and C10. DEV_NOTES "Ship-wide events" has every detail; this is the short version.

- **Branch and builds:** `claude/ship-events`, 0.34.8 to 0.34.13. Merged ship-integration 0.41.5 at 5ad87e8. Report to the lead, session_015QoyPWBdMPM4ywf5W2jMMs.
- **The ion storm is ON (0.34.12):** `SHIP_EVENTS.ionStorm`, due on the first day from 8 on when Calder is on shift (day 10 in a new game). It has the full data: phases to the end of day 5, systems, routines, needs, galley, jobs, news, moments, meetings, address, mail, threads, traces, dressing and the debrief.
  - Thread scorers: blackout (systems 0.33.26), spoiled and bridgeHungry (galley 0.29.21), calls (here, `stormCallBacklog`).
- **Meetings (0.34.9-10):** `MEETING_SCRIPTS.calderStorm` and `captainAllClear`.
  - `meetingsTick` plays a script when you're in its room. `meetingCast` fills 'works:2'.
  - The panel is section 19's `deviceDialogue(view)`, and its taps call `dialogueNext`, `dialogueChoose(k)` and `dialogueClose`. The plain strip `DIALOGUE_EL` stands in until it lands.
  - Walking out or missing a meeting mails its gist (after skips too).
- **Felt everywhere:** `eventFeel` -> the performance engineer's `shipFeel(kinds, len)`, else my stand-in `eventFeelFrame` (shake, light dip, flicker).
- **The address:** `captainAddress` -> section 19's `deviceAddress({ from, text })` when it exists, else a plain banner.
- **Joined up:**
  - `newsAdd` (section 20). I expand 'dept:'/'all' seeds to ids myself.
  - `dressShow` (the deck architect's DECK_DRESS ids: signupWorks, partyLounge, stormRosterTeaCorner, relayScorch, tapedPanel).
  - For section 14: `eventOn(d)`, `eventGatherings(d)`, `eventRoutines(t)`, `callOwed`, `eventGuestDays(g)`.
  - The party goes through `eventPlan` (`EV_SHIPWIDE`).
  - `eventOneOff` for section 20's story beats, with `host: true` on the host's plan entry.
  - `eventMod(kind, key, t)` takes a minute; `eventModAt` was dropped.
- **Occasions (C10, 0.34.11):** `OCCASIONS`: readyRoom (summons), captainsTable (every 28 days), progressTalk (`occasionAsk`). `SHIP.occasions` and `SHIP.commendations` are saved. `occasionDoorOpen` is for section 14's `doorOpenFor`; `occasionMod` is the table's galley batch through `eventMod`. design-doc has the rules.
- **Tests:** events_check now also runs:
  - the paper storm twice (identical);
  - a live storm (briefing, front, all-clear, end);
  - the occasions;
  - the hooks (party, routines, guests, one-off).
  Before each push, run deck_check, day_check 1 (and 11 or 13 for storm days), player_check, food_check and cadet_test against the previous build.

### Loose ends

- The sim engineer (session_01R6RBwwBM9aorpsqDCrztDU) builds the storm routines from `eventRoutines`. They should seat a one-off's host first (`host: true`). Doors for occasions: `doorOpenFor` should read `occasionDoorOpen`.
- The systems engineer should set `j.eventJob` on posted storm jobs, and claim for 'you' when `SHIP.event.mine['wants:<job>']` is set (the briefing choice).
- The device engineer: `apptAdd` for occasions, Record reading `SHIP.occasions` (kept) and `SHIP.commendations`. A lasting count of your jobs is needed (`yourJobsDone` reads `SHIP.jobs`, which may be pruned).
- The conference table (Part 4) waits for an event with a senior briefing (the diplomatic visit). Officers' quarters invitations are section 20's.
- Known: the warning Mail goes at 06:00, before Calder's 08:15 briefing. The debrief arrives at the end of the afterglow.
- Next events: the diplomatic visit (guests through `eventGuestDays`, `guestsArrive`, the greeting meeting at the shuttle-bay venue, formal dinners as occasions or meetings), then down the plan's list.

### Gotchas

- `eventNow(t)` is pure: running event, then the log, then the next due. Never let it read live-only state. It never runs past `days`.
- `MEETINGS` dedups by id and minute. events_check saves and restores it, because the in-play storm registers the same meetings.
- `newsAdd` is section 20's real function in merged builds. Tests can't stub it (it's not on window), so events_check reads `NEWS` and removes what it added.
- Something added to `evTable()` adds pools to `schedData`. `eventOneOff` clears `SCHED_DATA` and later plans.
