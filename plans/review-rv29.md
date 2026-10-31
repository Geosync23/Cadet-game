# RV29 review notes (patch 0.99.5; lead 47)

Queue (lead 47, ~09:50 UTC): PL2 claude/p995-player (notes 3, 12, 13), CT5 claude/p995-controller (notes 2, 5, 6).
JB2 went back to RV28 at 09:50 (my brief predates that); what I had already checked on JB2 is below, sent to RV28 as
input, no verdict from me. Base for every review: claude/staging-0994 8976965e (game a01d1a4c...bc4a).

## JB2 claude/p995-jobs c6dc9ac (game ed43ee2c...d293, verified) -- input for RV28, not a verdict
- cadet_test vs 8976965e, all three switches off (sed copy): ALL IDENTICAL (15 shots 0 px, no state diff).
- cadet_test as built: f/g/h differ only in Oona's Day 2 bubble (the washer's-fixed line), crew placed the same; j_steer1
  6 px level 1 (another browser was running). Same as RV28 found.
- Real-game probe (plans/rv29-probes/tour_play.py, Dev jump Day 2 08:35 Works bay): Zeke's tour talk plays (7 cards + the
  choice); the tour job "Your first rounds: a tour of checks" is held for you; route chk:c5-ext, 5-cartdock-1, chk:c5-clock,
  4-junction-1, chk:c4-door; each stop's card: the thing's name, its reading, "Tick it off.", one button Checked; tips
  RG_TOUR at each step; save + reload after stop 2 keeps route, marks and stepsDone, and the tour goes on; turned in:
  "Trained: rounds". No page errors.
- **Finding RV29-J1 (words; not covered by SW4's 7e30feb):** on the tour Zeke still says the old round's lines: after
  every stop "Your turn. Stand still a sec. Listen first." (train.m1.follow.look, onSim 'job' in 24 core), at the end
  "That's a round. Anything worn's on the board now. Yours." (train.m1.follow.done), and the toast "Round done. Anything
  worn is on the board, found by you." (roundDone, round.done). The same lines play in 0.99.4's first round (base probe
  identical), but on a tour with no judging they contradict Zeke's talk ("Tick it off"). Fix idea: with CHECKS_ON and
  j.train, the follow keys and roundDone's toast take tour versions (e.g. train.m1.follow.tour.look / .done,
  round.tour.done), SW4 for the words.

## JB2 re-review (RV28's FIXES NEEDED ~10:05: W1, F1, J1), waiting for JB2's new commit
What to check (lead 47, 10:08): W1 words baked (content_gen --check, check_fast); F1 option (a): the scanner's first job
rotates over the water recycler / pumps / irrigation (Tier 2 machines), never a washer, held for you with { tier: 2 } as
the Tier 2 test job is, takeable at Tier 1, work within the 40-minute cap (rv28/jb_scan.py, days 6-30, plus a take at
Tier 1); J1 the tour's own lines (tour_play.py); machine_check, mech_check; switches off still identical to 8976965e.

### JB2 re-review on claude/p995-jobs 1e056bd (game ef0941da...7d04, verified; game last changed 21552d1)
- Code read c6dc9ac..1e056bd: fixScanMachine up to Tier 2 (never a washer); fixScanTick reserves it with { tier: 2 } (jobReserve's
  test-job path); the tour's follow keys train.m1.follow.tour.look/.done (onSim 'job', m1 + CHECKS_ON) and roundDone's
  round.tour.done on j.train; SW4's words baked.
- F1: rv28/jb_scan.py: Days 6-30 rotate over all nine Tier 2 pump machines (4-pump-1/2, 5-pump-1/2, 3-pump-1, recycler,
  irrigation, nutrient, heater), never a washer. scan_take.py (Tier 1 player, Days 6/9/14/17): on your board, claimJob true,
  work 24 min (board says 24), cause pump, no made part (make dropped with a cause): within 40.
- J1: tour_play.py in the real game: after each stop "Ticked. Good look, that. Right, onward."; at the end "That's the tour.
  Five checks, all done properly. Anything not right is on the board." and the toast "Tour done. Anything that wasn't right is
  on the board, noted by you." No old round lines. Save/reload mid-tour fine; no page errors.
- W1: content_gen up to date (check_fast's words baked OK); SW4's talk, tips, cards in the real game.
- cadet_test switches off vs 8976965e: ALL IDENTICAL. check_fast: QUICK CHECK OK 317 s. mech_check m1 m7: MECH CHECK OK (the tour row: 5 kinds, 3 checks, Decks 5,5,5,4,4).
- Note (not blocking): after the last stop Zeke says "Right, onward." just before "That's the tour" (the look line fires on
  every stop, the last too; the same order as 0.99.4's round).
- **Verdict (~10:55 UTC): PASS claude/p995-jobs 1e056bd (game ef0941da...7d04).** W1, F1, J1 fixed; nothing new found.

## PL2 claude/p995-player 6b2f135 (game commit 938f8b85; game e462d177...bf80b, verified), from 8976965e. Notes 3, 12, 13
No feature switch (fixes live); SEAT_BTN_ALL = !NOSAVE || ?seatbtn (the no-tray seat button off at test URLs).
- Code read: 13: jobDoorOpen's "let you out" only inside a room lockedBehind (BFS from the lift through doors, open edges, the
  lift, service hatches; YOU_LOCKS shut; cached on EDGES); adoorMineLocked (c): a locked door open to you follows the Doors
  setting (private: tap); crewNearDoor's player branch asks adoorShut; tap() tries adoorTap on a closed door. Crew code untouched.
  12: talkPlanEnd(C) walks the remaining talk slots; talkStep caps T.mins at E and fills T.u (0-15) over E; meter shows E - mins.
  Not a pack talk: E = 15 as before. 3: seatBtnSeat no tray: nearest free public SIT_TYPES seat in your room within 2.2 m; tray
  path unchanged. No R(), nothing saved.
- Doors (door_sweep.py, Day 3 10:00, junior; every 'closed' door side on Decks 1, 2, 4, 5, 6 x all/private/none):
  0.99.4: every locked door on Decks 2 (34 sides), 4 (50), 5 (Works Chief's office, bay booth) and 6 (reactor) lets you in
  from the corridor, all three settings. PL2: none lets you in; every one lets you out. Deck 1's bridge-ready room door
  (both sides locked rooms) as before. Rooms now shut: Deck 2's cabins + guest/visitor rooms, Specimen store, Probe bay;
  Deck 4's port supply closet; Deck 5's office, booth, bay door gear; reactor. Features into them have their own door rules
  (visits name their doors; the office is an occasion; reactor m23DoorOpen); promo_beats_check OK, career_check OK.
- Crew (crew_doors.py, Day 3 06:40-07:25 Deck 4, you in the officers' corridor): every crew member's room each minute
  identical to 0.99.4 (hash fd386dfd8776bbec both); doors drawn open: the same owner openings; 0.99.4 also held h,34,6 open
  the whole time because you stood by it, PL2 doesn't.
- Talk (talk_play.py, Day 3 12:35 mess hall, three talks, both builds): 0.99.4 counts 15..9, the question, 8, then jumps to
  "A good talk" (the user's note). PL2 counts 8..1 and ends on the goodbye, the same lines and end time; friendship +6/+5/+6
  and social the same as 0.99.4.
- Seats (seat_sweep.py, SEAT_BTN_ALL on): every public seat on Decks 1-7 offers the button and sits you there (16/16/110/20/
  4/4/2 = 172); no private seat ever offered; rec deck seats out (117 rec:seat etc.); off with SEAT_BTN_ALL false.
  seat_shot.py real game (Dev, a save): the button by a common-room chair and a plaza bench, a real click sits you, the card
  "You sit down. Tap anywhere to get up."
- cadet_test (PL2's) ALL IDENTICAL; check_fast, talk_check, social_check: (below).
- Not probed by me: an invited friend's cabin (shares the own-cabin path PL2 probed); controller X on the seat button.
- For the lead (PL2 flagged it): Stop partway now pays the share of the real length (6 of ~8 min = 2 friendship; was 1).
