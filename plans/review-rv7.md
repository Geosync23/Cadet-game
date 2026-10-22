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
