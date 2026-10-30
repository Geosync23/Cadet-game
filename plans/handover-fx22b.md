# Handover: FX22b (session_01Lzi6Fe2HQJsVbaJBFxXtyx)

Role: fix builder under lead 37 (session_019GcNZ4GGEqfiuYDYnue7nX). Reviewer for the swap: RV18 (session_01PMfvrCN6StPzwVSPGX7ijH).
Earlier work (all reviewed and passed): the 0.92.6 appointments fixes (claude/p926-fx22, dd4d8797), join_check (claude/p926-fx22b-join), the 0.93.0 music and Music app (claude/sound-music a4ac9e31; DEV_NOTES "Music").

## The event swap (0.93.2): claude/event-swap, from claude/integration b957b92d (0.93.1)
- 56fa0ca5 (s.1) and 49cf5dc5 (s.2). DEV_NOTES "The event swap", build-table rows 0.93.2-s.1 and s.2.
- Switch: `EV_SWAP_ON = URL_FLAGS.has('evswap')` (section 13, next to P926_APPT). Off = 0.93.1 (cadet_test identical), except Basil's beat 4 (below).
- One block `if (EV_SWAP_ON) { ... }` in section 18 just before "the ship-wide events' gathering moments" (EV_SHIPWIDE is built from SHIP_EVENTS there at load, so anything with moments must exist before it):
  calendar (storm 11, visit 16, comet 22, veyliVessel 27 parked: no SHIP_EVENTS entry), EVENT_ORDER + comet, EV_BEATS mondayBriefing Day 16 08:30 and seniorBriefing Day 19 08:00, the visit reshaped to 4 days (guestStay: 2, read by eventGuestDays), a DRAFT comet (from plans/comet-viewing-draft.js, moments k 354/355, still dated as the draft: onset 21:15, gatherings 21:30), the Friday addresses' Mail lines.
- Elsewhere: crew-welcome-tea skipped in the TRAD_LIST loop when on (FX24 leaves the tea to this switch); friCond `swap` key; content_gen ADDR_KEYS `swap` (bare, like commended); content/addresses friday-d19/d26 `? swap` / `? !swap` lines (drafts for SW2); Kowalczyk's waiting story DAY lines on nights 19-20.
- Basil's beat 4 (content/stories/bramwell.arc, CS1's words): a welcome dinner, `crescendo: meal:dinner`, `where: meal`. Not behind the switch (the lead's call).
- Checks: events_check and bigevents_check read the switch (SW / SWAP / PASSED). Event days: day17 and day22 (testing guide CR4/CR5, tools/affected.py, plans/opt-cover/cov_run.sh).

## Next: the comet, switched ON for 0.93.2 (the user)
- Design: plans/events-plan-2.html Part A (A1-A8) on claude/events-plan-2 bda11cc8, by EP1 (session_01LjeoeX6qpCuwTV5UNVNwV5). Defaults for its two open questions: own music track (SD1 can make it), the knot cord stays.
- Build it as A7 says behind EV_COMET_ON (on): replace the draft SHIP_EVENTS.comet in the swap block (or move the comet out of the block so it runs with EV_SWAP_ON off too, if the user wants the comet without the swap: ask the lead; the calendar row for Day 22 lives in the swap block today). Keys 354-357 are free (checked).
- Words: EP1's samples (A4), then CS1/SW2. Raman's story: DAY 22, beat 4 Days 8-21; Pell's practical avoids Day 22.
- Checks to add (A8): events_check's comet block (replace the draft's COMET), bigevents_check, day_check Day 22, deck_check draw calls, interactions_check joins, bubble_check, stories_check.

## Gotchas
- A page reload in a check: `page.goto(..., wait_until='commit')` then `wait_for_function(..., polling=500)`; the default rAF polling never fires under the test clock (appt_check's lesson).
- fridays_check hangs in this container with no output, on 0.93.1 too: have a runner run it.
- Two checks writing to one log garble it: one log file per run.
- `pkill -f name` matches your own shell command; kill by pid.
- Messages from the lead often reach this session an hour or more late: re-read before acting on an old one.
