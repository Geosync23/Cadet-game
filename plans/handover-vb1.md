# Handover: VB1 (session_01UsjGN26E88zwrNPWwef4iT)

Role: events builder for "A Veyli vessel needs help" (Days 27-30), pieces V-1, V-2, V-3, V-4 in that order. Hired by
lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Partner: VB2 (deck and sky, V-5 and V-3's spots) session_01KRBGtugjBpv5iGcV5WDvCP
on claude/vessel-sky. Writer: SW2 session_017dLaLFBnRUQin3PQEQq6so. Planner: EP2 session_01Hos4fCBxgEXxP8nR9E2iMq.
Reviewer: named by lead 39.

## Branch and builds: claude/vessel (from claude/staging-0.93.3 d9c7e5f0)
- V-1: the event and its calendar (build-table row "vessel V-1"; DEV_NOTES "A Veyli vessel needs help").

## Switch
`const EV_VESSEL_ON = URL_FLAGS.has('evvessel');` (section 13, after P926_APPT). Test copies switch it on by text:
`sed "s/^const EV_VESSEL_ON = URL_FLAGS.has('evvessel');/const EV_VESSEL_ON = true;/"`.
Questions C1-C3 unanswered: built as recommended, each a one-line switch in `vesselData()` (commend, sky, standIn).

## Shared names (agreed with VB2, see the message of V-1)
VESSEL (var), VESSEL.seen / VESSEL.lights, vesselFrame() (VB2's, called from eventsTick under a typeof guard), the
marker line in the slot (VB2 below, VB1 above), DECK_DRESS ids vesselPartOld/New, vesselCrate, vesselSketch,
vesselSketchYours; places 5-vchain-N, 5-vsheet, 5-vbench-N; hash keys 358-363.

## Loose ends
- The staging switch-on of the visit (BM18's 026278be) was not on origin when I started: merge claude/staging-0.93.3 when BM18 says.
- tools/affected.py: add day28-30 for the vessel at its switch-on turn (they mean nothing while it's off).
- Pell "if he stayed": ask the social engineer for the flag (V-4).

## Gotchas
- The data block runs at load before MEETING_SCRIPTS and the slot's consts exist: functions or vars only; scripts are made in the slot's top-level if.
- `pkill -f name` kills your own shell: use pids.
- A named meeting cast must be on shift or called in, and free at its minute (bigevents_check): the Captain's scene moved to 08:45 Saturday, after her breakfast; Saruth (no work) can't be called in.
