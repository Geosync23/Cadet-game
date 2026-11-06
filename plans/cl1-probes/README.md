# CL1 probes (0.99.7, claude/p997-calendar)
Run from anywhere with CADET_CHROME=/opt/pw-browsers/chromium and CADET_WORK set up as for cadet_test.py. Give them a
switched-on copy (`const CAL997_ON = true || ...`) to see the patch, or the plain build to see 0.99.6.
- `cal.py BUILD FROM TO`: each day's traditions (eventsOn: id, time, * = Tap to join) and what was left out (EV_DROPPED).
- `day.py BUILD "JS"`: evaluates one expression in a fresh game (?nosave) and prints it (used for the goers per early
  tradition, the party days `cl997Party`, and `cl997Beats()` against INTRO_WEEK).
- `arrow.py BUILD`: phone size (390x844): the goal arrow on Day 3 06:02-06:22 (Pick-your-own, Deck 4 then the garden) and
  Day 6 09:20-09:35 (Harvest morning). `arrow5.py BUILD`: Day 5 15:25-16:10 (the Captain's address: the arrow from 15:30,
  gone in the auditorium; CL997_RATE 0.6 there, ship minutes per 10 real seconds 3.6 against 6.0).
