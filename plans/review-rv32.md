# RV32 review notes (0.99.7 playtest patch)

Reviewer RV32 (session_01GKuymkDX3gviqiGJcKLWuS), reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn).
Base: claude/integration d7ad4c58, game f6ff5ec1...db8a8 (0.99.6). Plan: plans/patch-0997.md on claude/lead-49.
Reviewing: CH1 (claude/p997-chars), MV1 (claude/p997-move), TP1 (claude/p997-tips), CR1 (claude/p997-career), JB3 (claude/p997-jobs).

For each build: does it do what the user's note asks (probed in the real game, phone size where it matters); switch off =
identical (cadet_test.py vs 0.99.6); switch on: the area's checks plus check_fast; sections touched (tools/section.py --diff).

## Setup
Kit ready 2026-11-06: playwright, numpy, pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.
Smoke test: cadet_test 0.99.6 vs itself ALL IDENTICAL (64 s).

## Lead 49's rule for this round
For every week-1 note (tips 6/9/11, the Day 1 briefing, the Day 8 promotion, week-1 jobs): probe from a fresh save with
the intro ON, following the arrows like a player (a 0.99.5 fix passed with the intro off and failed on a fresh save).
Tool for it: arrows_check.py's Follower walker (see plans/rv30-probes/arrow_walk.py on claude/review-rv30).

## Verdicts

### 1. CH1 batch A (claude/p997-chars 3d07e66): notes 37, 35, 10, 1
Game sha256 180e78d4f891df4362c33aa050a071dfa24eecf8965a00e385a0da41f3b86179 (matches). Switches CH_SOLE_ON, CH_POSE_ON,
CH_RELAY_ON, CH_HAIR_ON (CH_SEAT_ON declared, note 4 not built: batch B). Sections: 4d (1 line), 8 (slot), 8b (1 line), 8c (1 line).
- Off: cadet_test 0.99.6 vs 3d07e66 ALL IDENTICAL.
- On (all four): cadet_test vs 0.99.6: only triangles and the pictures differ; paths, collisions, crew walks and taps the same; no page errors.
- Note 1 hair (plans/rv32-probes/ch1_look.py, magenta skin, close crew and crowd, 5 views; results/hair_sheet-3d07e66.jpg):
  skin showing through hair (magenta pixels) in 0.99.6: short/buzz/curls/bun/ponytail/long, worst on crowd buzz (5400 px
  from the game's angle) and curls (3286). On: 0 for every crowd view; close crew at most 19 px (buzz and bun, from straight above).
  The crowd's near caps come out about 8% fuller than before (the cos correction plus the pad); looks fine to me.
- Note 37 soles (results/feet_sheet-3d07e66.jpg): the flat plate is gone, the rounded boot still meets the floor (no float).
- Note 35 pose (ch1_seats.py, the rec deck's auditorium seats and beanbags filled with 'sit:slump'; results/seat_sheet-3d07e66.jpg):
  0.99.6 forearms held out in front (the bike handles); on: arms down, hands on the seat by the hips. The hands-behind-head
  variant unchanged. Nothing seen through the seat or beanbag.
- Note 10 relay cabinet (ch1_relay.py; results/relay_sheet-3d07e66.jpg): 0.99.6 the cabinet's back (z 9.87) pokes over the
  hull rim from outside; on (z 9.08-9.52) it stands inside. Fault lamp: lamp z moves with the cabinet (in front of its face by
  0.06 both builds). Junior wing cabinet (closet k) checked too: already inside, unchanged.
- check_fast on a copy with all four switches on: QUICK CHECK OK in 337 s (deck_check's draw calls included).
- Verdict: PASS for notes 37, 35, 10, 1. Note 4 (CH_SEAT_ON) still to come in batch B.

### 2. TP1 (claude/p997-tips 9c7a288): notes 6, 7, 9, 11, 28, 33, 53, 54: PASS
Game sha256 0e63713ce88f2bd43fe54fee90a0079b8388ce797c44d30d1ea0fe0e5d445759 (matches). Switch TP997_ON (section 13; `?tp997`), TP997.nN each.
Sections: 13 (switch), 19 (GLYPH key + Mail wrap in the Device slot), 15 (teachTick 1 line, actEnd pay 1 line, playerNew 1 line + slot),
15b (slot), 22 (generated words, content/banks/tp997.lines), 18 (tradWords, tradJoinMinute ixTip, tradJoin notice, eventJoin Mail + slot), 11 (HUD slot).
Lines outside slots: owners to look (player engineer, device engineer, traditions engineer).
- Off: cadet_test 0.99.6 vs 9c7a288 ALL IDENTICAL. On: check_fast on a switched-on copy QUICK CHECK OK in 343 s. TP1's tp997_probe: TP997 PROBE OK (all 15 lines).
- Fresh save, intro ON, phone size 390x844, arrows_check's follower (plans/rv32-probes/fresh_walk.py; results/fresh_walk-tp1-9c7a288.json):
  real sleep each night (sleepGo, alarm 06:00), the device closed after a moment, and at 08:25 on Day 1 a real tap on the
  tracker's "Morning briefing" row (see the note below). Tips as shown:
  - note 9: 't:tp997-trk' Day 1 06:10 (the first morning, right after the clothes tip).
  - note 11: 't:devwork' Day 1 08:38, as the first long work step starts (0.99.6, the same walk: Day 2 08:26 near the job's end).
  - note 6: 't:tp997-call' Day 2 12:30, after the walker's own call home (it called at 11:58 for Missing people; the call ended 12:19);
    the earlier walk without a midday call: Day 2 19:00. 't:eve-call' (Day 4) marked seen.
  No page errors, nobody stuck.
- Note 33 Pockets (plans/rv32-probes/tp1_pockets.py, a page that really saves): bought through the store menu's handler and the
  counter's pay step: 4 into the pocket, the 5th (cold tea) drunk at the till (pocket full), chocolate into your hands as a
  gift (unchanged). saveGame, page reloaded: pocket and hands kept. Pockets at 390 px lists them (Eat / Drink), the hands
  section shows the chocolate with "Tap a crewmate to give it" and Eat; a real tap on Drink: pocket 4 -> 3, hunger up 4.
- Notes 7, 28, 53, 54: TP1's probe (real taps on the tracker row and Mail's button; every deck's nearest bathroom; 81
  traditions' words). I read the words: plain, no doubled colons; "Food up" / "Fitness up" match what joining gives
  (also.hunger, act gym/rec). The tracker panel redraws once a ship minute while open; the row's findPath per toilet is cheap.
- Lessons (for my own probes): a walk must really sleep (sleepGo) and close the device; my first walk sat up with Mail open
  from the arrival evening and all of Day 1 held every tip, which looked like a game fault and wasn't.

Note for the lead (not TP1's, there in 0.99.6 too): from a fresh save with the intro on, at Day 1 08:45 there is no arrow
at all (goalNow null, IX_GOAL null, GUIDE_ON true): not to the 08:50 briefing, not to the clock. The tracker lists "Morning
briefing with the Chief 08:50" and "Clock in 09:00". The follower, with no arrow, ate and wandered; "Still not clocked in"
at 10:15 (results/fresh_walk-0996-day1-0845.json). Worth a look by whoever owns the week-1 arrows (MV1's note 2 is the briefing).

### 3. CR1 (claude/p997-career 2f2b93e): notes 25, 48, 49, 55, 56: interim, FIXES NEEDED likely
Game sha256 3c293c568e4c45af48bb9a240e334acb81201001cae4569df11f65e0c6a5f590 (matches). Switches CR_DAY8_ON, INC_REDO_ON, CART_FIRST_ON,
BOARD_NEW_ON (vars in 24p's slot) are committed TRUE on the branch (the round's rule: off on the branch).
Sections: 15b (doable, boardLessonName, ixJobStep label, ixHold), 17 (gardenCarry, jobRun stop loop, boardTopUp), 22 (words), 24d (1 line), 24p.
- Off (the four set false in a copy): cadet_test vs 0.99.6 ALL IDENTICAL. cr1_check: CR1 CHECK OK.
- Fresh save, intro ON, 390x844, follower with real sleep, Day 0 to Day 8 (results/fresh_walk-cr1-2f2b93e.json): no Day 8 test.
  Day 2 10:32 the arrow "10:45 meet Zeke: Works bay"; 10:42 a needs arrow "Somewhere to sit and unwind" took over; the meeting
  was missed (m1 'ask', no arrow to it the rest of the day). The ladder then ran a day late: m1 Day 3, m4 Day 4, m5 Day 5,
  m7 over the weekend to Day 8; m6 needs m7 used once, so Day 9 at the earliest. tr at Day 8 17:00: m1 3, m3d 3, m3i 4, m4 4,
  m5 5, m2 8, m7 8. Note 55's Day 8 test holds only when week 1 has no slip; CR1's Day 8 runs start from a Dev-set career.
