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

## Pillar 3 (C6, C10's occasions, meetings): where it stands at 0.34.7

Read plans/pillar3-plan.md (on `claude/lead-pillar1`): Part 2 in full, "Shared formats" section 18, the workstream rows C6 and C10. DEV_NOTES "Ship-wide events (0.34.7)" has the format.

- **Done (0.34.7):**
  - The traditions array is now `SHIP_TRADITIONS`.
  - `SHIP_EVENTS` is the object of ship-wide events.
  - The machinery: `eventNow`, `eventMod`, `eventScore`/`eventMine`, `eventStart`/`eventAdvance`/`eventDueDay`, bands, traces (`traceOn`), the save.
  - Stand-ins: `captainAddress`, `MEETING_SCRIPTS`/`meeting`/`dialogueShow`/`dialogueClose`, and `upcomingTraditions`.
  - events_check runs the storm's skeleton from day 10, twice.
- **Next (the lead's order, step 2): the ion storm's data**, all in `SHIP_EVENTS.ionStorm`:
  - the warning, onset, escalation, resolution and afterglow (the afterglow should last a day or two; `days` is 4 now, so it gets only 6 hours: raise `days` or move the end);
  - the address lines for onset and the all-clear;
  - the Works notice Mail;
  - jobs (secure the lounge, shielded ballasts, battery packs to the bridge);
  - news seeds for the social engineer (session_01DzZ669spGpdSdVMYzUog2N, section 20);
  - routines (double shifts on the bridge, the lounge closed, call-home booths closed) for the sim engineer;
  - galley (storm stew, trays to the bridge) for the galley engineer;
  - threads (blackout minutes, food spoiled, bridge tiredness, call-home backlog);
  - traces; the debrief by band.
  Then remove `draft: true`, so it starts in play about day 8-10.
- **Meetings:** Calder's storm briefing (Works bay, day 0, 08:15, with one choice: the bridge battery run, the lounge, or nothing) and the Captain's all-clear (observation room, day 3, 10:00, at the same moment as the all-clear address), as `MEETING_SCRIPTS` entries. The device engineer (session_014TpEMbWarRFJM8BHC9WM8c, section 19) draws the panel: agree with them on `deviceDialogue(script, i)` and on how a choice reports back (relationship and job).
- **Other owners add their own inert checks (C7):** systems read `eventMod('wear', system)` and `eventMod('effect', 'flicker')`; sim reads `eventMod('routine', ...)`; galley reads `eventMod('galley', ...)`. Tell them the keys once the storm's data is fixed.
- **Open for you:**
  - Traditions should pause or change during a ship-wide event (no observatory night in a storm). Do it so plans stay deterministic: decide from `SHIP.event`'s start day and the event's phases, never from live state that changes during a day.
  - Who scores the threads (systems for blackout, galley for spoilage).
  - The C10 occasions: the summons, briefings, invitations, the Captain's table.
