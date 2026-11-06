# Review RV33 (0.99.7 playtest patch)

Reviewer RV33, session_01GKuymoAK9gACR31MRd1CMX, branch claude/review-rv33 (notes and probes only).
Lead: lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Brief: plans/patch-0997.md on claude/lead-49.

Reviews: SC1 (claude/p997-social), CL1 (claude/p997-calendar), EV1 (claude/p997-events),
GM1 (claude/p997-games), TB6 (claude/p997-traditions), AV1 (claude/p997-av).
EV1 and CL1 also checked merged together for first-week clashes.

## Setup
- Base: claude/integration d7ad4c58, game f6ff5ec1...db8a8. cadet_test base vs itself: ALL IDENTICAL.
- Kit: playwright, numpy, pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.

## Week-1 calendar probe (lead 49's rule: fresh save, intro ON)
- plans/rv33-probes/week1_cal.py BUILD [--json OUT]: fresh save, newGameStart(true), then Days 0-8: traditions (eventsOn),
  events-base beats, call-in meetings, the intro week's timed beats; prints every overlap (the shift and seek-anywhere beats left out).
- Base listing: plans/rv33-probes/cal_base_f6ff5ec1.json. Base overlaps of note (already there before 0.99.7):
  Day 2 call-home booths 18:00-19:00 x Spice shelf supper 18:15-19:15 x rec wall night 18:30-19:45 (TB6's note 51);
  Day 2 knit-and-natter x tiles night 20:00; Day 3 store visit 16:30 x open door 16:40; Day 5 jam x tap night;
  Day 6 Saturday run 07:00 (note 30 cuts it), tiles ladder x cook-along, film x observatory; Day 7 rec WSO 11:30-16:30
  under the Line ceremony and reading corner. Parallel optional evenings are not faults by themselves; what matters is
  anything the intro or an arrow asks the player to be at landing on top of something else asked of them.

## Results
(none yet: waiting for the first build)
