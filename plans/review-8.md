# Turn reviews: PR8

Second Fridays reviewer, from 2026-10-21 ~14:30 UTC (lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r). Builder: FR3
(session_01935gmiyLoy5fgvs3xQd7QC). PR5 (session_01Eh4drBZjJ82DjYx6XaTt1F) keeps turns 7, 8, 9 and 11b2220.
Pushes only to claude/review-8 (from claude/fridays 0dc4562).

Method (PR3's, as PR5 uses it): build lines untouched; cadet_test off against the base; check_fast alone; the area's
checks on; a code read; a live probe on a real save at 390x844. Checks run one at a time through
`plans/review-8/runner.sh` (resumable, res/<name>.log). Probe: `plans/review-8/p8_fri.py`; shots in
`plans/review-8/shots/` (`git add -f`).

Copies: `t10` = 0dc4562 as pushed (SHORT_FRIDAY on, EVENTS_ON off); `t10off` = the same with SHORT_FRIDAY false;
`t10ev` = on with EVENTS_ON true; `base9` = 11b2220 (the turn-9 tip).

## FR3: turn 10, switch on (0dc4562)

**Checks (each alone):**
- cadet_test base9 → t10off: ALL IDENTICAL (81 s).
- check_fast on 0dc4562: QUICK CHECK OK in 300 s.
- fridays_check t10: OK (613 s). Day 5 16:10: 49 seated, lectern Marrow + Vance. **Day 12 16:10: 51 seated, lectern []**
  (Marrow and Vance on the storm's double shift). The live fill: 26 seated at 16:00, 48 at 16:05.
- fridays_check t10ev (EVENTS_ON true): OK. Same Day 12 empty lectern; the storm's lines still never fill (no
  EV_STORM_ON in this build, so the check leaves them out; FR3's note that it fails there applies to a build with it).
- lines_check: PASS (0 errors, the 6 old warnings).
- events_check t10: OK. t10ev: FAILED, 21 FAILs, all the events base's own (ionStorm-stormBriefing / allClear "not on",
  the storm not due on day 10, ready room, Captain's table, all-clear party, eventRoutines, eventGuestDays,
  rec-slow-stretch missing Day 14, the film night move). The control copy (EVENTS_ON on, Fridays off) is queued to
  confirm that none is Fridays'.
- day_check 5 OK; 19 OK; 12 FAILS only backlog #18 (also with EVENTS_ON).
- bigevents_check t10: OK. t10ev: 3 FAILs, all in its own "switch off" parts (it flips the switches itself from an
  EVENTS_ON-off build): a check limit, not the game.
- join_check: OK.
- The rest of the broad round (bubble, interactions, clothes, talk, social, intro, devmode, career, mech, puzzle, food,
  perf, arc, path, tiles, disc) was dropped for lead 24's account-move window: FR3's row lists them run.

**Finds so far:**
1. **Day 12 says nothing.** With EVENTS_ON off or on, 51 people sit in the auditorium and nobody is at the lectern
   (the storm's double shift keeps Marrow and Vance on the bridge). friAddressTick waits for the line's speaker in
   DECK_CREW, so no line is ever said; a player there still counts as heard (no Mail). EVENTS_ON alone doesn't fix it:
   it needs EV4's storm update (Marrow released from 15:30, Vance from 15:45). So the "switch on together" release has
   to carry Fridays, EVENTS_ON **and** the storm update; with Fridays alone, Day 12 is a silent hall (and its Mail
   describes a storm that isn't happening).
2. **Day 19 announces an arrival that doesn't happen.** "And at dinner a new junior comes up the Tern's ramp…" and the
   Mail's "a welcome this Sunday for our new junior" are unconditional, but this build's first rotation is Day 35
   (ROSTER_ROTATIONS). Only the {sunleavers} line drops. Fix: give the welcome line a slot or condition that empties
   when no one arrives Days 20-21 (e.g. `{sunarrivals}`, as {sunleavers}), and the same for the Mail sentence; or keep
   turn 10 off the release until claude/patch-crew lands. Also "talent night … a week late" and Days 12/19/26's storm,
   comet and Veyli lines all assume the events base (find 1).
3. (being probed) An old save without the fri part loaded on a Friday after 16:50: FRI.heard/mailed are 0, so the
   first frame gives the missed-it dip, banner and Mail for an address that didn't exist when it was saved.

(verdict pending: the Day 5 phone probe, the upgrade probe, the Day 12 probe)
