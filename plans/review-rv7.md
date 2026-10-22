# Reviews by RV7 (Pillar 5 fixes and the guiding arrows; taking over from AR2)

Reviewer RV7 (session_01RLTBGbbdRbUkKME189xL4k), for lead 29 (session_01A9rNreAGVbsY1HgPucDMA7). Branch `claude/review-rv7`
(notes only; the game is never edited here). Earlier verdicts: AR2's `plans/review-fx2.md` (claude/arrows-plan-2) and
RV6's `plans/review-arrows-*.md` (claude/review-arrows). Probes used are in `plans/review-rv7/`.

## 1. AC2 6610dc7 on claude/arrows-c (base d2dade6): PASS WITH FIXES (check lines only)

What it does: (a) 15b `ixBoard`'s `doable` gives a Take it to a registered job kind that isn't a side job (a round, a
haul), exposed as `ixBoard.doable` and used by D's `guideTakeable`; (b) the 14:50 drill arrow is FX2's own line again
(no `trk` tag); (c) S9 says "Works reputation down: <word>" on a drop; (d) FX1's "Nothing on the board" word waits
through a meeting, a training's watch or turn, or a dialogue.

The code is right and small. `doable` keeps the old rule and adds `(chore || registered non-side kind) && jobStepDone`;
`JOB_KINDS` is only read at run time (no load-order problem). `drillGoal`/`drillClose` still clear the drill arrow at
the last stop, at the all-clear and after a day jump, so dropping FX1's `trk` doesn't bring back "the arrow stayed up
for days". S9 marks a word as reached only on the way up (or the word the game loads with), so a word first met by a
drop still gets its "Works reputation: ..." when reached upward later. The board's word isn't marked said while held, so
it comes once the meeting / training / dialogue ends.

| Test | Result |
| --- | --- |
| cadet_test d2dade6 -> 6610dc7, alone | ALL IDENTICAL (no differences to explain) |
| interactions_check on 6610dc7 | INTERACTIONS CHECK OK ("a round on the board": offered, Take it, haul doable, drill not) |
| interactions_check on d2dade6 | crashes with `TypeError: ixBoard.doable is not a function` (counts as a failure, but see fix 3) |
| arrows_d_check on 6610dc7 | OK |
| arrows_d_check on d2dade6 | FAILED on exactly the two new lines (S6 held in a meeting; S9 the drop) |
| Planted faults (9, `plans/review-rv7/mut.py`) | caught: the old `doable` (interactions), `doable` without the side test (interactions), no drop toast (arrows_d), no meeting hold (arrows_d). NOT caught by any check: no dialogue hold, no training watch/turn hold, `guideTakeable` back to its own copy of the old rule, the drill line with FX1's `trk` tag back (arrows_d and mech_check m3d both OK), S9's old "seen" marking |
| "Trained: rounds" toasts | once, in every week run (arrows off and on; toasts logged only when they reach the screen) |
| Other kinds the new rule opens | incident, leak, nozzle, tracedemo (tune and rewire have a machine, so already had a Take it). None was on the player's board Days 2-8 in any run |

**arrows_check week** (the follower: goes where the arrow points, taps what it names):

| Build | Arrows off | Arrows on |
| --- | --- | --- |
| d2dade6 (base) | learned: m3d, m2 only. Rounds never learned (stuck at "Take your first round at the job board", the board's "coming soon") | the same |
| 6610dc7 | m1 (Day 3, not Day 2: the follower took "Clean a vent: laundry" at 11:20 Day 2 and stuck there), m3d, m2 | m1 on Day 2, m3d, m2 |
| 6610dc7 + FX3's 2cdc1df (fix 14 cherry-picked; a full merge of p5-fix3 conflicts in the burst pipe lines) | m1 Day 3, m3d, m2: still stuck at the laundry, because the follower calls `playerTap` directly (no screen tap, so fix 14's ray test can't see it) | m1 Day 2, m3d, m2 |
| the same, my follower with a real screen tap at every chore pin (`arrows_check_rt.diff`) | m1 Day 2, m3d, m2; the haul lesson's run taken from the board (19:21 Day 3), then stuck on its stops | the same |

So in no combination are Hauling (m4), the inspection (m3i), Tuning (m5), the scanner (m7) or p3 learned on Days 2-8
by following the arrows. What's in AC2's diff is the step that lets the round (and the haul's turn) be taken at all:
"Take your first round at the job board" (red on base, Days 2, 3 and 8) is gone, and Rounds is learned. The rest is
outside this commit:

- **The laundry stop's pin over Washer 1:** FX3's fix 14 (real taps). The arrows_check follower doesn't make real taps
  there, so its week stays red at the laundry until the follower does (or the stop moves off the washer).
- **The haul's cart stop (new to the player now that hauls can be taken):** the pin is on the floor beside Cart dock 1.
  Tapping the dock itself says "Cart dock 1: in good order." and starts nothing (a restock's cart does start from the
  dock tap, via cartTap). A floor tap at the pin works (`p_cart.py`, both builds). The same trap as the laundry; FX3's
  area (Hauling).
- **With real taps, the haul and delivery drops stick:** "Crew store stock to the crew store, Deck 3", "Linen to the
  laundry, Deck 4", "Pick up a crate of linen", "Take medical supplies to the infirmary, Deck 3". Not traced further.
- **The haul lesson's run is taken late** (19:21 on Day 3 in my runs, after the shift): the follower is busy with other
  board jobs all afternoon; the training's turn isn't put first on the board for it.

Fixes (checks only, no game change):
1. Lines for what's untested: the board's word held during a dialogue and during a training's watch and turn;
   `guideTakeable` with only a round (or a haul) on the board gives "Take a job at the board"; the drill arrow is
   still up after you reach the Works bay at 14:55 (the reason the `trk` tag came out); a word first met by a drop
   is said ("Works reputation: ...") when it's later reached going up.
2. arrows_d_check's header says a drop shows "the pointer to the Works app's Training tab"; the code (rightly) only
   toasts on a drop. Fix the words.
3. interactions_check's new part: guard `ixBoard.doable` with `typeof` so an older build prints a FAIL line, not a
   crash that stops the rest of the check.

For the lead (not AC2's): is it wanted that incidents, leaks, nozzles and the trace demo also get a Take it when one
is on your board? The rule allows it; none showed up in the week.

## 2. FX3 2cdc1df on claude/p5-fix3 (fix 14, on 8aae063 which AR2 passed): PASS

What it does: `choreRayTap` in 15's `playerTap`, after `jobTap`: if you hold a chore (`ixChore`, which includes the
registered kinds), the tap landed on a machine (real or stand-in) and the tap's line passes within `JOB_RAY` (0.6 m)
of your chore's next stop, the stop starts there (`ixChoreTap` at the stop's spot). The linen drop and the laundry vent
stop (4-laundry-1) stand by Washer 1, which took the tap before. `stubTap` only looks a stand-in up (no side effect).

| Test | Result |
| --- | --- |
| interactions_check on 8aae063 | FAILED on the new line only: the camera turn with Washer 2 under the pin starts nothing (linen and vent) |
| interactions_check on 2cdc1df | INTERACTIONS CHECK OK: all 8 taps (2 chores x 4 camera turns) start the stop |
| cadet_test 8aae063 -> 2cdc1df, alone | ALL IDENTICAL (renderer noise only: up to 46 px one level off) |
| clothes_check, player_check on 2cdc1df | ALL OK, PLAYER CHECK OK |
| Planted: no ray test (any machine tap does the stop) | caught ("a lamp chore in the laundry: Washer 1 does its own thing") |
| Planted: no machine test (any tap on the line to the pin) | not caught (small: worth one line, e.g. the hamper or a seat on the line still does its own thing) |

Notes: (1) the arrows_check follower calls `playerTap` directly with no screen tap, so this fix can't help its week
(it stays stuck at the laundry); a real tap does work (my follower variant). (2) The same trap is now on the haul's cart
stop (pin beside Cart dock 1: a tap on the dock says "in good order"), see item 1. `choreRayTap` helps only when the
tap's line passes within 0.6 m of the pin.

## 3. claude/arrows-c 69d1ed9 + 78fef90 (AC2: the FX3 merge, the tea arrow, my 6610dc7 fixes, follower changes): PASS

In it: 00f4436 merges p5-fix3 2cdc1df (FX3 fixes 10-14); 695cf6e the tea arrow carries FX1's trk window (gone when tea's
over, 14:00, or once you reach the Tea corner); 78fef90 the board's Take it only for rounds and hauls (`BOARD_KINDS`,
lead 29) and the check lines I asked for; c26f194 / 7ff2c27 / 69d1ed9 the arrows_check follower only (a job held for
you first at the board; a tap that answers but starts nothing, or starts a sit-down or laundry, is followed by a real
tap at the pin; up from a sit-down once its minutes are in).

The merge's one clash (the burst pipe) keeps both sides: AC1's F4 queue entries and `incGoalNow`, FX3's `incPark` and
its WORK_TICKS, `incWho` "Calder" with the queue off too, and FX1's trk window on the call's arrow.

| Test | Result |
| --- | --- |
| cadet_test 6610dc7 -> 69d1ed9, alone | differs in e_night ... i_tap3 only (up to 12k px): the other-deck arrow's words, "Take the lift to Deck 3: food, Deck 3" -> "Tap the lift: Deck 3 · Food" (FX3's fix 10, passed by AR2). Same place, same arrow. Intended |
| cadet_test 69d1ed9 -> 78fef90, alone | ALL IDENTICAL |
| player_check on 695cf6e~1 | FAILED on "tea not taken: the arrow goes when tea is over" only |
| player_check on 69d1ed9 | PLAYER CHECK OK |
| Planted: tea's trkTo a day late | caught (player_check) |
| interactions_check on 69d1ed9 | OK |
| arrows_d_check on 78fef90 | OK |
| My planted faults on 78fef90: no dialogue hold, no training hold, the drill trk tag back, S9's old seen marking, guideTakeable's old rule (arrows_d); any non-side kind takeable (interactions) | all 6 caught |
| Week (`p_week.py`, 78fef90's own follower), arrows off | learned m1 Day 2, m3d and m4 Day 3, m5 Day 4, m2 Day 8. Not: m3i, m7, p3, m6. "Trained" toasts once each |
| the same, arrows on | m1 Day 2, m3d and m4 Day 3, m5 Day 4. **No "Trained: ..." toast reached the screen at all** (see A) |

A. **The pop-up queue drops "Trained: ..." (arrows on; piece B, AR1's design, not this commit).** At most 3 wait; the
oldest waiting is dropped. At 11:00 on Day 2 six arrive at once (Round done, Zeke's line, "That's a round", Work done,
Trained: rounds, Job complete) and "Trained: rounds" is pushed out before its turn (`p_toast.py`). Earlier runs showed
it only by luck of timing. Suggest: a training's toast is never dropped ({ now: true }, or the queue drops the least
important first, or merges a job's own run of toasts).
B. **Day 5 lost to the climbing wall (the follower):** it taps the Climbing wall nearest the holds' pin and climbs all
day (recClimb isn't one of the sit-downs 69d1ed9 ends), so the scanner meeting is missed (m7 meet -> ask). A player
tapping the floor at the pin gets the job (FX3 fix 8/12). Follower fix: end any activity that isn't the job's stop.
C. **"Put the seal back: main storage" up from Day 6 05:50 over the weekend** (seals left in hand from the abandoned
holds job; FX3's put-back arrow, fix 9). Over 3 hours on a day off. FX3's call whether it should wait for a workday.
D. Still stuck once: "Linen to the laundry, Deck 4" (a haul drop; with FX3). The inspection (m3i) isn't reached on
Day 4 (the arrows plan's Day 4 warning).
E. A real rewire job has a machine, so it gets a Take it through the old machine rule (as before 6610dc7; tier 2). The
interactions line tests `{ kind: 'rewire' }` without a machine, so it doesn't prove "never a rewire". Lead 29's call.

## 4. claude/arrows-c 86faa86 + 5160b81: the game change PASS; the follower change FIXES NEEDED

86faa86 (game): 15b `ixJobStep` returns null once you've clocked out today, so there's no job arrow (steps, Turn it in,
Take a job) after clock-out; a job you hold stays in Tracked; a put-back part keeps its arrow.

| Test | Result |
| --- | --- |
| cadet_test 78fef90 -> 86faa86, alone | ALL IDENTICAL |
| arrows_d_check on 86faa86 | OK; my planted fault (clocked out "tomorrow" instead of today) caught ("after clock-out: no job arrow") |
| Week with 78fef90's follower on 86faa86's game, off / on | the same as 78fef90 (m1, m3d, m4, m5 learned; m2 off) |

86faa86 + 5160b81 (follower): a real floor tap at the pin whenever the arrow is your job's own step (5160b81: not
when the goal names an item, i.e. the board). With it the week collapses:

| Follower | Arrows off | Arrows on |
| --- | --- | --- |
| 86faa86 | stuck at "Clock in at the time clock" every workday from Day 2 08:04: never clocks in; only m3d learned | stuck at "Turn it in at the job board" every day; only m3d |
| 5160b81 | the same: stuck at Clock in (the clock's goal has a place, no item) | stuck at "Turn it in at the job board" from Day 2 10:50; nothing learned |

A floor tap at the clock's or the board's pin opens neither. Fix: keep the real tap for a job's own stop (a chore's
stop, a machine's spot) and tap the clock and the board by name, or tap the thing first and the floor only when nothing
started (78fef90's order already does that).
