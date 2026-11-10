# Review notes: RV35 (reviewer, 0.99.91 pieces A and D; lead 51)

OLD = main bfbcbdf (0.99.9, game 583d99ba...bd16).

## A. TP2 claude/p9991-tips f2ea6eb (game 3b5df861...8bd2), TP9991_SD_ON: FIXES NEEDED
- Off: cadet_test vs 0.99.9 ALL IDENTICAL (errors none).
- The change itself (sdHourOk, sdHourNear, the clamp, Later/Earlier, Quietest, sdBook) reads right: only 20:00 on
  Days 23 and 24 is out (night from 21:00, check-in arrow from 20:45); Day 22 (22:45) and other days untouched.
- **Fix needed: the Monday briefing's own shutdown booking.** Section 28b's m21Raise(0) (the "a shutdown" choice at
  Day 22's briefing) books tomorrow at 20:00 on a night day on purpose ("before the night (Day 23)"), through sdBook.
  With the switch on, sdBook refuses it, so the briefing books nothing and the Captain says the no-job line
  ("Approved. When a job needs the power off, book the hour in Works.") although a job is waiting.
  Probe plans/rv35-probes/m21probe.py: off books Day 23 20:00 ("Tomorrow at 20:00: the galley circuit"); on, booked
  null. mech_check m21 on the switched-on copy: FAIL "m21: the job waiting for a shutdown booked for tomorrow (20:00,
  before the night) (None)", MECH CHECK FAILED.
  Suggested: in m21Raise, with TP9991_SD_ON, the hour is sdHourNear(day, 1200, -1) (19:00 on Day 23); mech_check's
  expectation 1140 when the switch is on (1200 off). 28b is mechanics seat A's (owner review).
- Notes, not fixes: a save that already holds a 20:00 Day 23/24 booking (made before the switch, or by the briefing
  with it off) keeps it; opening that job on the Shutdown screen shows the draft at 19:00 (the clamp) while the booking
  says 20:00, until you press Book again.

### A re-check: f9ff643 (game 082c1d86...0665): PASS
- The fix: m21Raise books sdHourNear(day, 1200, -1) on a night day with the switch on (19:00 on Day 23; "Tomorrow at
  19:00: the galley circuit"); off 20:00 as before. The only other sdBook caller is the Book button (already guarded).
- On copy: m21probe books Day 23 19:00; branch's mech_check m21 OK; tp9991_probe OK; machine_check OK; arrows_check
  step6 asis, teachoff, track, skiptea all ARROWS CHECK OK.
- Off: cadet_test vs 0.99.9 ALL IDENTICAL; mech_check m21 OK (20:00); check_fast QUICK CHECK OK in 260 s.
- Still open for the lead to mention (in TP2's build-table row): an old save's 20:00 booking is kept. 28b's line
  needs mechanics seat A's owner review.
