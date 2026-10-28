# Handover: EV1, events engineer (the Diplomatic visit switched on)

For a fresh session taking over the events seat. Written 2026-10-28 by EV1 (for lead 43, then lead 44).

## Role, branch, builds
- Events engineer: section 18 (ship-wide events), its slots, and the event checks (events_check.py; bigevents_check.py is EC1's).
- Branch `claude/visit-on`, from `claude/staging-pad` e158dcf (0.95.0 plus the controller waves, PAD_ON off). Final commit a1917dd (game last changed in 8c91437). RV25: PASS. BM20 is merging it into the controller switch-on round. Build-table row: `0.95.0-vis.1`.

## What I built (the user, 2026-10-28: "Turn it on")
- **The visit runs in a real game, Days 16-19.** It had `draft: true` since 0.93.2, so the calendar passed it over even with `EV_SWAP_ON` on. The event-swap block (section 18, `if (EV_SWAP_ON) {`) now does `if (EVENTS_ON) delete V.draft`. Without the storm update or the swap it stays a draft.
- **Times on Friday Day 19:** the gift exchange is at 09:00 and the farewell at 09:30 (they were 08:20 and 09:00, when the Captain and Saruth were still at breakfast). The Veyli leave at 10:00 (GUEST_AT, section 14).
- **Farewell places:** the farewell uses `places: [{ deck: 5, pool: '@gather-shuttle-bay' }]`, because the bay has no seats (before, it had 0 places).
- **`eventGuestDays`:** if the event isn't running, logged or due, it falls back to `evCalPlan()`. Plans made early then show the Veyli aboard Wednesday 10:00 to Friday 10:00. Taavek's days, for the Veyli vessel, now show on paper from Day 1 the same way.
- **xp (lead 43, option b):** in the swap block, `onSim('job')` adds `SHIP.works.tier - 1` when you turn in a `j.event === 'diplomatic'` job, so the visit's jobs earn your tier's worth. A steady Senior is Trusted by Day 19 again (60).
- **Words:**
  - The greeting's gist says "until Friday".
  - Teshavi is they/them ("the Speaker's aide", "they have rarely been made so welcome").
  - One formal dinner: content/reactions/guests.lines, the debrief, and the thread label "The dinner on time".
- **Kept as designed (lead 43):** the greeting day, Day 17, pauses that day's evening traditions (`pause: ['onset']`).

## Checks changed
- **events_check:**
  - The visit runs as the build has it. If it is still a draft, the check is skipped, or failed when the swap is on.
  - The storm's paper run stops at its own end.
  - The live storm may be followed by the visit.
  - On Day 16, eventOn shows the visit's warning.
  - Rec-deck days paused by an event are allowed for.
  - An event guest's own `ev-<event>-...` steps aren't counted as traditions.
- **bigevents_check (EC1's file, reviewed by RV25):**
  - Someone with no rota (Saruth, a guest) is never "off" or called in.
  - A guest arriving off the shuttle (`tag: 'arrive'`) counts as at the greeting.

## Loose ends
- **Backlog after 0.96.0 (RV25 note 1):** the xp listener's comment says section 24 pays first, but it's registered earlier and runs first. The xp total is the same, but the reputation toast could show twice.
- **Possible follow-ups (lead 44 has them for the user):**
  - A seated formal dinner. Today Day 18's dinner is only the galley's 10 extra meals, and nobody sits in the Captain's quarters.
  - A nod to the visit in the Veyli vessel's words (Days 27-30). Today they neither assume nor deny it.
- **Old failures, also on e158dcf:**
  - career_check: "busy: Relied on before Day 5".
  - events_check: "not reached farouk-olu>3-lounge-28 16:00" (reading corner, Day 7).

## Gotchas
- Four checks at once on a 4-core container makes pages time out on load (Page.goto 30000 ms). Run at most 2 or 3 at once, each in its own CADET_WORK.
- `pgrep -f` / `pkill -f` patterns match your own shell's command line: don't wait on a pattern that's in your own command.
- Run cadet_test from a scratch folder: it writes screenshots into the current folder.
- Don't commit while check_fast runs: a push at its end takes the new commit too.

## How to test the visit
- `bigevents_check`
- `events_check`
- `fridays_check`
- `day_check` Days 16, 17, 18, 19 and 22
- `career_check` (s5)
- `arrows_check` and `arrows_check step6`
- `cadet_test` against the base (Day 1 identical)
- `check_fast`

## Open questions for the user
None of mine.

## Second job: the visit's pointers (claude/visit-pointer, 0.96.0; RV25 PASS at 6db1cdd)
- Greeting (Wed 10:00) and gift exchange (Fri 09:00): the Schedule's heads-up 15 minutes before with Go there (the storm meetings' pattern). The gift exchange gained `notify` (shown only with heads-ups off).
- Farewell (Fri 09:30): tap to join, host Envoy Saruth (TRAD_JOIN.farewell; the moment's `host` so the planner brings them; `tradJoinable` admits `when.ship === 'diplomatic'`). Words `join.farewell.tip/notice` in content/banks/join.lines, because shortName("Envoy Saruth") is "Envoy".
- Real-play probes I used: scratchpad look2.py / look3.py (not in the repo). Note cadet_test's Game hides `#devHu`: read `DEV.hu` / `HU_Q` instead. Heads-ups wait behind queued tips (`devHuBusy`).
