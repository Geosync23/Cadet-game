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
- cadet_test switches off vs 8976965e: ALL IDENTICAL. check_fast: QUICK CHECK OK 317 s. mech_check m1 m7: (below).
- Note (not blocking): after the last stop Zeke says "Right, onward." just before "That's the tour" (the look line fires on
  every stop, the last too; the same order as 0.99.4's round).
