# Review: arrows piece D, the shift chain (AC2), claude/arrows-c 4ef580e (RV6)

Reviewer RV6 (session_018Jzc4LeoHvuahsS7VHAzn3), 2026-10-22, for lead 29. Builder AC2 (session_015uhdrDuE49CJ8iWWX2SEeP).
What: `git diff 30e43ce 4ef580e` (game commit 07df591): `guideShift()` in 15b's slot, once a ship minute from guideTick:
S2 clock in (level 4), S3 take a job (level 4, `guideTakeable`, a held job first), S6 an empty board said once an hour,
S7 clock out from the shift's end for an hour or to friAutoOut, over a held job (T3 gives way via `guideShiftOver`);
pointers (POINT_ON) on Clock in / Take it / Turn it in / Clock out (3 times each), S8 the Work log, S9 a reputation toast
and the Training tab. Also: B's `guideGoal` now passes over an entry with an empty goal to the next live one (my E note);
section 15's `clockRmPoint` sets no direct clock-out arrow while the queue is on; 15b's `ixWorkStep` points at the board
only for a job with a Take it while the queue is on. arrows_d_check.py (new); arrows_check's shift reads clocked-out
from careerClockedOut.

## Verdict: PASS (three small notes)

| Check | Result |
|---|---|
| cadet_test 30e43ce vs 4ef580e, alone | ALL IDENTICAL |
| check_fast on 4ef580e | QUICK CHECK OK in 240 s |
| arrows_d_check | arrows_d_check: OK |
| My planted faults (ad_*, 6) | 5 caught: S7 at level 5, T3 not giving way at the shift's end, no pass-over, the empty-board line every minute, the direct clock-out arrow back; missed: `ad_heldfirst` (item 1) |
| arrows_check shift guide, Day 9, queue and pointer on: 4ef580e vs 30e43ce | 4ef580e: 11 jobs, clocked out by the player; one FAIL, stuck at "Take clean linen to the laundry, Deck 4" from 14:42. 30e43ce: the same linen FAIL **and** "not clocked out by the player". D fixes the clock-out; the linen stop is not D's (FX1/FX3, as AC2 said) |

## Small notes
1. **"A held job first" isn't tested.** `guideTakeable` puts a held training job first, so the Take it pointer lands on
   it; with that order removed the check still passes. A line: with a held job and an ordinary one on the board, the
   pointer is on the held one's Take it.
2. **S9 also fires on a drop.** The toast says "Works reputation: <word>" whenever the band changes to a word not seen
   before, down as well as up (arrows_d_check's own case goes relied -> steady). If the plan means "reaches", only an
   upward change should toast; the lead or the writer to decide the words for a drop.
3. **S6 doesn't wait for a busy moment.** "Board's empty for now..." comes once an hour while you're clocked in with no
   job, even in a meeting, a training's watch, or a dialogue (it goes through the pop-up queue, so it doesn't wipe
   another, but it can interrupt). Consider skipping it while DIALOGUE or ACT is up or a training is at 'watch'.

## Checked and fine
- Off: everything new runs from guideTick (GUIDE_ON) or checks GUIDE_ON (clockRmPoint, ixWorkStep); identical.
- guideGoal's pass-over stops at a direct goal or a level 5-6 entry when the job has a step, as the rules say, and
  re-checks each passed-over entry's done.
- S7's end: min(shift end + 60, friAutoOut) in minutes of the day (friAutoOut gives 960 on a short Friday, else
  CAREER.autoOut), as the check's short-Friday case shows (15:30-16:00).
- Not in yet (waiting on FX1): S1 and trainTell's direct arrow into the queue (my E item 5).
