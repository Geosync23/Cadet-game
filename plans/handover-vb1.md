# Handover: VB1 (session_01UsjGN26E88zwrNPWwef4iT)

Role: events builder for "A Veyli vessel needs help" (Days 27-30), pieces V-1, V-2, V-3, V-4 (all built, behind the
switch). Hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Reviewer RV21 (session_01AmTyMHLr5UuCY9zo3nQcwS).
Partner: VB2 (deck and sky, V-5 and V-3's spots, own slot 'Vessel sky') session_01KRBGtugjBpv5iGcV5WDvCP on
claude/vessel-sky. Writer: SW4 session_01DgMynb62u2rTUA9RocZi65 (inactive since ~21:00 UTC; ask lead 39 for a new
writer). Planner: EP2 session_01Hos4fCBxgEXxP8nR9E2iMq. Build master BM18.

## Branch and builds: claude/vessel (from claude/staging-0.93.3)
- V-1 dd043a00 (+ staging d6bb0aba merged: 581fc84f): the event and its calendar.
- V-2a f7a32c4a (+ SW4's claude/vessel-words 7dd2eb5d merged), V-2b 73942e8a (+ VB2's claude/vessel-sky c070862c and
  FX29's claude/events-check-swapfix 8a91f1dc merged).
- V-3 85bdb51c the parts chain; V-4 6d4b5192 making the round one.
- Everything is described in DEV_NOTES "A Veyli vessel needs help" and the build-table rows "vessel V-1" to "vessel V-4".

## Switch
`const EV_VESSEL_ON = URL_FLAGS.has('evvessel');` (section 13, after P926_APPT). Test copies switch it on by text:
`sed "s/^const EV_VESSEL_ON = URL_FLAGS.has('evvessel');/const EV_VESSEL_ON = true;/"`.
The user's answers (2026-10-26): C1 yes, C2 yes, C3 they wait at the ramp up to an hour. Each a one-line switch in
`vesselData()` (commend, sky, rampWait).

## What's where
- Section 18: the data block after the comet's (`if (EV_VESSEL_ON && EVENTS_ON)`): SHIP_EVENTS.veyliVessel, the
  calendar row, the gatherings vesselLights (k 358) and vesselChain (k 359), routines, TRAD_JOIN entries.
- Slot 'Vessel builder' after the Comet builder's: everything else (vesselTick is the in-play hub: scenes, chain,
  making, test fit, shelf, Tern, talk). VB2's code is in its own slot 'Vessel sky' (after the Appointments builder's).
- Hooks: section 14 guestTrim (vesselGuestTrim), section 15 devDay (vesselItems), section 18 eventsTick (vesselTick,
  vesselChainHands), tradJoinTap (vesselTap), tradWhere (vesselWhere), tradJoinable and evBdaySlot (the vessel's
  gatherings count), DEV_NOTES hook register rows.
- Planning-only meetings (vesselSheet, vesselRamp, vesselJob, vesselHome): `ranks: []` and a script that doesn't exist,
  so the meetings' own tick shows no panel and sends no Mail; they only put the cast in place (called in).

## Checks
- events_check.py: the vessel part at the end (a copy switched on when the build has it off; the build off: nothing),
  paper + live (V-2, V-3, V-4). A quick runner: cut the file at '# A Veyli vessel needs help (VB1' (see git log).
- bigevents_check.py: VESSEL_ON (late saves Day 23, 27, 28). day_check 28 OK (V-2 copy); 29 failed once on Taavek stuck
  at 5-make-1 (fixed: an event spot; VB2 asked for 5-vbench-1..3 and 5-vshop-1..3).
- Switched off: cadet_test identical (known-old Oona bubble shots and a moving a_start bubble come and go: rerun).

## State at the stopping point (lead 40, 2026-10-26)
- Shas: V-1 dd043a00 (RV21 PASS on 581fc84f); V-2 73942e8a; V-3 85bdb51c; V-4 6d4b5192; RV21's V-2 fixes 85f07071
  (+ VB2's claude/vessel-sky 3fb8eac7 merged: ed8b5787); the goodbye's arrow at the ramp's foot, the 24j hook
  (vesselShopTap) and arrows_check's vessel part cdf2685f; controller_check's vessel part (the last commit).
- RV21's V-2 list, all done: the must (lights over places) fixed in V-3; the arrival crowd (~20, vesselArrival k 360);
  the goodbye not missable (from 14:30, the Tern waits to 15:30, Calder fetches you at 15:00); the round one's fallback
  (Taavek brings it at 12:45, notice + gist at 13:00); Saturday Calder comes to find you; the pilot's word once;
  simTimeout everywhere; 3fb8eac7 merged. Needs RV21's re-review of 85f07071 onward.
- Passing on the last build: check_fast OK; cadet off ALL IDENTICAL (vs vessel-sky); events_check vessel part OK;
  bigevents OK (switched-on copy); day_check 28 and 29 OK; arrows_check vessel (the arrow-follower) OK;
  controller_check vessel OK.

## Loose ends (in order)
1. arrows_check vessel with `teachoff` and with `senior` (written, not yet run); day_check 27 and 30 on the latest copy.
2. join_check and interactions_check on a switched-on copy; a phone-size screenshot set for the review.
3. Making the round one is quick (done by about 09:50 when you follow the arrows: steps of 3+2+10+3+5 minutes): the
   spec's 09:30-13:00 may want longer holds (VESSEL_STEPS minutes) if the user wants it to fill the morning.
4. The stand-in words (marked in content/banks/event-veyliVessel.lines, "VB1's stand-ins") for a writer to polish.
5. tools/affected.py: day28-30 at the switch-on turn.

## Gotchas
- The data block runs at load before MEETING_SCRIPTS and the slot's consts: functions or vars only there.
- skipTo never goes back in time: test runs go forward through the days (the events part is ordered).
- deviceChoose refuses while a dialogue panel is up: a card after a scene waits a moment (setTimeout).
- The guide queue keeps entries across a test's "fresh" runs: drop vessel:* entries between runs.
- `pkill -f name` kills your own shell: use pids. At most three browser checks at once on this machine.
