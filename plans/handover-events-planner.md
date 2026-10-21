# Handover: events planner (EP1)

**Role:** plan the ship-wide events up to the end of the career. This was a planning job only: I never touched `starship-cadet.html`, main, or the playable link.

**Session:** EP1. It was started by lead 20 (session_019UJSCUCdtC1kTpYiABWKhs) and reports to it.

**Branch:** `claude/events-plan`, started from `claude/rec-cand-s1` (build 0.64.2). The last commit is the one that adds this note.

**Reviewer:** ER1 (session_01CU43dzWJe5PGBQWTtKH4C3), on branch `claude/events-plan-review`, in `plans/events-plan-review.md`. The review covers v1 (a2020fd), v2 (6e12af6) and v3 (05f1163).

## What's on the branch
- **`plans/events-plan.html`:** the plan page, v3.2, finished. Every question is answered. The lead publishes it, and the answers are saved in the page database.
  - Sections: 1 the calendar (F0, day by day, with how the Captain's scenes are spaced), 2 the ion storm's changes, 3 Crossing the Line, 4 the comet and the visit, 5 the shared base F0-F8 with order and turns, 6 the user's answers, 7 the parked events, and builder notes.
- **`plans/events-plan.md`:** a short summary, with v3.1 and v3.2 change logs at the end.
- **`plans/events-plan-shots/`:** 5 phone-size shots of the storm running in 0.64.2. They're force-added, because `.gitignore` excludes `*.png`.
- **`plans/events-plan-run-log.json`:** the storm run's log. Mail days in it count from 0.
- **`design-doc.md`, "Ship-wide events":** records every decision. The events after the career's end are marked **parked** in the events table and none is deleted. The decisions are also listed under "Answered" in Open questions.

## The user's decisions, by round
- **Scope (lead 20's brief, 2026-10-20):** only events up to the end of the career. The later ones are parked, kept on record.
- **v2 answers (05:47 UTC):**
  - Add one more short event.
  - The storm moves one day later, to Days 11-15, with a shorter afterglow.
  - The comet is on Tuesday Day 16 at 21:30.
  - The visit is a weekend finale on Days 26-30. Vance's memo comes on Day 22, the warning on Friday Day 26 after Calder's question, the greeting on Saturday Day 27, a dinner on Sunday Day 28 and the farewell on Monday Day 29.
  - Events go by the calendar, not by rank.
  - Prep jobs and help move the storm's threads: left alone it comes out bumpy, and with good help smooth.
  - The rec deck's first all-hands is unhooked from the storm, and the rec deck closes from the front to the all-clear.
  - The Captain's scenes stay separate and are spaced out.
  - A small crew arrival on Day 21, for Pillar 5's mentoring.
- **v3.1 answers (12:25 UTC):**
  - The extra short event is **Crossing the Line**, on **Sunday Day 7**, so Saturday stays free. Saturday 17:00 is the fallback.
  - People called in on a day off are mentioned in their own lines and in crew chatter.
  - Crowds of up to about 60.
  - Rec talent night moves a week, and Lap of the Wren moves to Monday Day 15 at 20:30.
  - The commendation comes at the all-clear.
- **Other user asks relayed by the lead:**
  - More large-group moments ("Love the moments with large groups").
  - The build order: Dev mode, then the playtest patch, then the Talk-a-while pack, then the **events (storm first, then Crossing the Line, then the comet, then the visit)**, then Pillar 5 steps 5-6, character arcs, optimisation and polish.

## What the builders need (in this order)
1. **The shared base F0-F8 (12-15 turns):**
   - **F0, the event calendar:** fixed days; one main event at a time; casts can be called in off rota and are marked so their lines can say so; the comet's and other gatherings registered in `EV_SHIPWIDE`, which is built at load.
   - **F1, `eventDay(d)` and the career-beat guard, in hours:** `eventDay(d)` is narrow (front, escalation and all-clear only). It's already called at about line :43839, but nothing defines it yet. The guard holds today's beats (Days 9-11) plus Pillar 5's beats reserved now, with their hours: the night shifts from 21:00 on Days 19-20, Day 18's training, and Day 29's 08:30 briefing before the gift exchange. Its rules: at most one of the Captain's scenes a day, none on a test day, never across a night shift.
   - **F2:** a phase note at each phase, so crew react. The 89 storm cue lines are dead today.
   - **F3:** the device: meetings in the Schedule and Tracked, closed places hidden, a Ship status line, and the Record.
   - **F4:** phases replay after skips and jumps; a meeting comes back after a reload; moments aren't replayed.
   - **F5:** small parts by rank.
   - **F6:** only phase jumps and "End and keep". Dev mode's Stop 3 builds starting an event, the threads view and "End and undo".
   - **F7:** one data-driven events check, covering jumps, reloads, casts and perf_check scenes.
   - **F8:** calls read `eventMod('effect','commsDown')`, not the phase.
2. **The ion storm update (9-11 turns):**
   - **Dates:** the briefing on Day 11 at 14:00, after the 09:30 team job and the 13:00-14:00 tea, with the jobs posted after the briefing and your pick held for you. The front on Friday Day 12 at 14:00. The lantern supper on Saturday Day 13. The all-clear on Sunday Day 14 at 10:00, with the call-ins, the commendation and the threads stopping, and the party from 19:00 to 21:00. The debrief on Day 15 at 18:00, and the commendation summons on Day 18 at an hour clear of the training.
   - **Threads you can move.** The calls thread is a fixed formula today, and full power still gives about 157 blackout minutes.
   - **The rec deck:** unhook its first all-hands before Crossing the Line is built. Blackouts still skip the rec deck (the 0.83.2 call). The rec seat owns the two film-night flags.
   - **The banner on phones,** and the other items 1-13 on the page.
3. **Crossing the Line (4-5 turns).** Pieces from other seats:
   - the gold hull-light state (performance);
   - the plaque and certificate (deck architect);
   - the oath scene and the called-in lines (writer);
   - the supper replacing the Sunday table (galley and traditions);
   - 44 mess seats plus standing places.
4. **The comet (2-3 turns).** The draft is in `plans/comet-viewing-draft.js`. Make it one day long, drop its gap/need scheduling in favour of F0, and register its gatherings in `EV_SHIPWIDE`.
5. **The visit (9-11 turns).** It needs:
   - shortening;
   - guest escorts;
   - the Veyli look;
   - the dinner as a meeting;
   - the senior memo;
   - casts checked against the rotas.

**Total:** about 36-45 turns, plus the head writer's lines.

## Open items for Pillar 5 (steps 5-6, built after the events)
- Read F1's reserved-days list, and fit the Tier 3/4 beats around the events' fixed days.
- Add "not before" days: the Tier 3 test on Day 15 at the earliest, the Tier 4 test on Day 22.
- Make the reputation pace reachable: a new Officer needs about 2.5 workdays to reach "Relied on".
- Vance is off on Day 17, the evening of the toast.
- Day 26 has no Works Friday tea: "four weeks aboard" takes its 18:40 slot, and "Calder's question" is set at the Friday tea.
- Build the Day 21 crew arrival: one in, using the built rotation traditions.
- The Day 22 Monday briefing takes over Vance's memo about the visit.
- The Day 20 Captain's table must end by 20:30, before the 21:00 night shift, or the seat moves to the next table.
- career_check fails one line on 0.64.2: the busy player reaches "Relied on" on Day 4.

## Facts checked in 0.64.2 (so nobody re-derives them)
- **Who works when:**
  - Marrow, Calder, Sato and Holt work Monday to Friday.
  - Vance is off on Days 11, 17-18 and 21 (his pattern: off Wednesday and Thursday, varying).
  - Brennan is off on Day 6 and works Day 7.
  - Torres's id is `torres-zeke`.
- **The bridge invite** needs the eve of a bridge hour (Days 23, 51...), so it stays on Day 22. Leave the code alone.
- **Crowd places:** the plaza has 71, the mess 44 seats, the bow lounge 181 and the shuttle bay 124. The party measured 236/367 draw calls with 64 crew on the deck.
- **The hash-key range** for Pillar 6 is 950-999, skipping 951-952.

## How to rerun the storm
Load the build through cadet_test's `Game` class at 390×844. Then call `skipTo(t)` to jump the clock, place the player with a `put(deck, placeId)` helper (see events_check LIVE), and step the ship minutes with `setShipNow(t); eventsTick()`.

Give the run its own `CADET_WORK`, and point `CADET_CHROME` at `/opt/pw-browsers/chromium`. three.js r128 goes in `$CADET_WORK/three`.

The Captain's banner hides after 20 real seconds, so in tests that run on the virtual clock it stays up.
