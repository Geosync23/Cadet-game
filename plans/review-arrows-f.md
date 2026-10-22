# Review: arrows pieces F3 and F4 (AC1), claude/arrows-c (RV6)

Reviewer RV6 (session_018Jzc4LeoHvuahsS7VHAzn3), 2026-10-22, routed by lead 28. Builder AC1 (session_01LDmfZ93ttCJ4XfoSDkJqx2).
What: AC1's own commits `git diff 0ec58bc bd18997` (9524671 the game, bd18997 arrows_f_check.py), then the tip 1f2ce27d
(merges FX3's 360801c; the one clash, FX2's and FX3's edits to ixJobStep's label line, kept both).
- 19 slot: `POINT_WATCH`, per-frame watchers while POINT_ON (the lift's pointer moved onto it).
- 24f (FX3's lines, M2 seat): `incGoalSet(g, by)` / `incGoalClear` as a level-1 queue entry `inc:m6` while GUIDE_ON;
  `incGoalNow` points at Calder herself while she's on your deck and the pipe isn't; `incStopWord` through the incident
  kind's `goal` hook; the valve card pointer (`incValveWatch`); one extra argument on FX3's follow line.
- 24k (seat H): slot `caseNextGoal`, `f3ScanWatch`, `f3CaseWatch`; one line in `caseAct`'s 'next' branch.

## Verdict: FIXES NEEDED

## What was run
| Check | Result |
|---|---|
| cadet_test 0ec58bc vs bd18997, alone | ALL IDENTICAL |
| arrows_f_check on bd18997 and on 1f2ce27d | arrows_f_check: OK (both) |
| check_fast on 1f2ce27d | QUICK CHECK OK in 261 s |
| Planted faults, arrows_f_check (af_*, 10) | 6 caught, 4 missed (item 3) |
| Play, Day 5 (the scanner), queue and pointer on, following the arrow | stuck 09:25-17:14 at "Look over the climbing holds"; no pointer ever; m7 not learned (item 2) |
| Play, Day 8 (the burst pipe), same | "Follow Ines to the burst pipe" on Calder; she stood at the lift 10:38-11:03 with you beside her; the 30-minute follow ran out, m6 back to "ask" (item 1) |

The play builds are 1f2ce27d with `POINT_ON = true` in a copy and GUIDE_ON switched on at the start (arrows_check's
`real_game`); the follower is arrows_check's (it also presses the pointer's element). Probes and logs:
`plans/review-arrows-f/`.

## Numbered list

1. **"Follow Calder" on Calder herself loses the lesson (must fix).** Day 8: the follow started 10:32 in the Works bay;
   the arrow was on Calder (`crew`), the follower stayed beside her, and from 10:38 both stood at the main lift (Deck 5
   tile 17,8, Calder; 17,7, you) until 11:03, when the follow timed out (INC_FOLLOW 30) and the training went back to
   "ask". She never took the lift while you stood at her. The same thing happened to E's first T1 on Day 2 (Zeke stalled
   in the corridor beside the player), fixed there by pointing at the room. Fix: point at Calder only while you're more
   than a few tiles from her, else onward (the lift to Deck 4, then the valve panel), or drop the person target and
   keep FX3's valve-panel arrow; then a check line for it (af_follownow, below, is not caught today).
2. **An arrow-only player can't open the Scanner (must fix; F3 or FX2, the lead to route).** Day 5, m7 at 'do': T3
   gave way to the held job (correct), whose arrow says "Look over the climbing holds" (FX2's scan first). Tapping the
   panel runs "Inspecting" (jobBegin's scanFirst branch) but the Scanner never opens, and F3's Scanner pointer only
   starts once the Scanner is already open (`f3ScanWatch` needs `DEV.app === 'scanner'`). Nothing points at the Device
   button and the Scanner tile, so the follower stood there 8 hours; m7 not learned on Day 5. The plan's line is "The
   Scanner opens: a device pointer on the bars". Either FX2 opens the Scanner after the look-over, or F3 adds the path
   Device -> Scanner while a scan-first job is in hand at its machine.
3. **The check misses 4 of 10 planted faults (must fix).** Caught: the valve pointer on the wrong valve, tracking not put
   back by Where next?, stop words while off, the Scanner's 3-second wait gone, the follow at level 3, the follow never
   cleared. Missed: `af_follownow` (the follow never points at Calder: incGoalNow untested), `af_scanhs` (the Scanner
   pointer on a head-scratcher, which it must skip), `af_call2` ("Call it" offered with two suspects left), `af_nextdone`
   (Where next? not gone on the call: the test finds every clue before calling, so `got` ends it first). Add a line for each.
4. **Two names for one person in a row (small, words; FX3's labels).** Day 8: T1 says "10:30 meet Calder: Works
   Chief's office", then 24f's arrows say "Meet Ines" and "Follow Ines to the burst pipe, Deck 4" (worksFirst). Use the
   same name (E's guideWho gives "Calder").
5. **Owners (process).** F4 edits FX3's lines in 24f (M2 seat) and the incident kind's registration; F3 adds a line in
   24k's caseAct (seat H). Each owner reviews before merge (plans/owners.md); FX3 should see the `incGoalSet(g, by)`
   change.
6. **Small.** A watcher that throws is dropped for good and noted only in `DEV.errors` (seen in Dev mode only); fine,
   but a console.warn once would make it visible in a normal game too. `f3ScanWatch` sorts `j.scan` every frame while
   the Scanner is open (a handful of rows: no cost worth fixing).

## Checked and fine
- Off: every new path waits on GUIDE_ON or POINT_ON; `incStopWord` returns null off (the `goal` hook then falls back,
  as before); `caseNextGoal` returns the real setGoal off; identical as above.
- The valve pointer's "last valve" matches incStepDone's right answer (`line[line.length - 1]`).
- Where next? restores tracking exactly as it was before the old path cleared it, and its entry has a 3-hour limit.
- The merge on 1f2ce27d: ixJobStep's label line keeps FX3's chore title first, then scan first / Tune; check_fast and
  arrows_f_check pass there.

## Re-check of items 1 and 2 (lead 28 / AC1 could not reproduce item 2), 2026-10-22 ~16:20

**Item 2 is withdrawn: my probe's mistake.** The follower tapped the item nearest the pin, the "Climbing wall", which
started a climb (recClimb) each time instead of the job; the look-over never ran. With one real screen tap at the pin
(`p_scan.py tap`): 09:25 "Inspecting" -> 09:28 the Scanner opens by itself -> F3's pointer `p:scan` is up (my first log
read `pointNow().id`, but pointNow() returns the id string, so it showed '-'). AC1's path works.

(Side note, not F3's: on the rec deck the climbing holds' pin sits on the Climbing wall, so tapping the thing under the
arrow starts a climb. A real tap on the floor at the pin works. Worth a look by whoever owns the rec deck's machines;
not filed.)

**Item 1 stands, checked two more ways (`p_inc2.py`, `p_inc_off.py`):**
- Real screen taps at the pin while the arrow says "Follow ..." (no follower walk): the taps land on Calder and don't move
  you; Calder walked from the office to the Works bay (14,4) by 10:35 and stood there until 11:03, 4 tiles from you; the
  follow timed out, m6 back to "ask". So it isn't only the follower standing in her way.
- The same day with the switches off (FX3's arrow on the valve panel, Deck 4): at 10:32 the follower took the lift to
  Deck 4, Calder came down after, and at 10:33 the training moved on to your turn ('do'). The lesson goes on with the
  panel arrow and stalls with the arrow on Calder.

## Re-check of AC1's fixes (claude/arrows-c 3519abab): PASS

| Check | Result |
|---|---|
| cadet_test 1f2ce27d vs 3519abab, alone | ALL IDENTICAL |
| arrows_f_check on 3519abab | arrows_f_check: OK |
| My 10 planted faults (af_*) | 10 of 10 caught (were 6) |
| Day 8 played, queue and pointer on, the follower (`p_inc.py`) | lift to Deck 4 at 10:32, Calder follows, your turn ('do') at 10:33 |
| Day 8, real screen taps at the pin (`p_inc2.py`) | the same: lift 10:32, 'do' 10:33 |

Item 1 fixed (INC_NEAR: on Calder only while more than 4 tiles away, else onward); item 3 fixed (the four missing
lines); item 4 fixed ("Calder" in the call and the follow with the queue on; off as before); item 6 fixed (console.warn).
Item 2 withdrawn (above). Item 5 is with the lead (owners of 24f and caseAct's line; FX3 to see incGoalSet(g, by)).
AC1's own extra: Call it now comes before Where next? once one suspect is left.

Note, not F4's: after the follow, the burst job is your turn while you still hold the vent job, so the job's arrow
stays on the vent (the same "another job in hand" pattern as Rounds' board arrow on Day 2); the follower didn't reach
the pipe job by 10:41. For FX3 / the lead.
