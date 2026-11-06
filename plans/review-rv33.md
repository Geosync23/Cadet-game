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

### SC1 social and crew stories (claude/p997-social), switch P997_SOCIAL_ON
**85442de, game e19f1d10...41db (sha256 matched): FIXES NEEDED (one item).** Sections 20, 20c, 22 (generated words).
- Off: cadet_test vs 0.99.6 ALL IDENTICAL. check_fast on the commit: OK (257 s); on a switched-on copy: OK (275 s).
- Note 17 (sc1_card.py: fresh save, manifest signed, introSkip, core crew warmed, Day 9, beside them on their deck, 390x844):
  off: Say hello, Sit with them, Talk a while, Ask about, Help?, Meet up; Sit with them gone after Say hello.
  on: Say hello, Get to know, Talk a while, Help?, Meet up, Do you know...?; Get to know stays after Say hello and opens
  the beat (moment:brennan:1, moment:halloran-emeka:1). Good.
- Note 32 after talking: arrow later that day: off 2 samples (kovac Day 11: 22), on 0. Good.
- **FIX: note 32 shuts the arrow on any flicker.** p997WordOk sets shut when the beat stops being ready, so a person
  walking off a calm spot ends the arrow for the day though you never talked. sc1_arrow2.py (Days 9-22, every 5 ship
  min, never opening a card): off the arrow covers every ready minute; on, kovac Day 9 ready 580 / arrow 35, Day 16
  555/15, Day 18 305/10; torres-zeke Day 10 625/75, Day 13 695/125 (files sc1_arrow2_*_85442de.txt). Note 17 asks the
  story to appear consistently. Suggested: shut only on opening their card.
- Note 38: 575 talks have listen2 (the 4 without are smalltalk fillers); sample of 12 all answer the ask, then ask back;
  commonest opener "Not yet." 10 of 575. content_gen and lines_check changes are small and right.
- Area checks on the switched-on copy of 85442de: TALK CHECK OK, SOCIAL CHECK OK, lines_check PASS (0 errors, 112 warnings, as before).
- Note 39: joined hosted tradition rec-all-hands (marrow): 0 -> 3.2 (her relGain on +4); again same day: no change; not
  joined: no change; off: no change.
