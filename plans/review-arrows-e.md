# Review: arrows piece E, the training arrows T1-T3 (RV6)

Reviewer RV6 (session_018Jzc4LeoHvuahsS7VHAzn3), 2026-10-22, for lead 28. Builder AR1 (stopped; the lead routes fixes).
What: `git diff 5d47d1d 14cffba -- starship-cadet.html arrows_check.py` (claude/arrows-plan 14cffba): `guideTrain()` in
section 15b's slot, called once a ship minute from `guideTick`, reading `SHIP.works.cur`; arrows_check's queue part tests T1;
new `guide` option for shift/week.

## Verdict: FIXES NEEDED

Switched off it is truly identical and stays in its slot. Switched on, the hand-over T1 -> T2 -> T3 works, but two of
the three arrows can lose a real player the training (fixes 1 and 2), and the check misses 8 of 11 planted faults (fix 3).

## What was run
| Check | Result |
|---|---|
| cadet_test 2b4a05db vs 14cffba, alone | ALL IDENTICAL (all shots 0 px, paths, state) |
| check_fast on 14cffba | QUICK CHECK OK in 258 s |
| arrows_check queue | ARROWS CHECK OK |
| Scope | only section 15b's slot (lines 16058, 16062-16087); nothing in 24 core, trainTell or FX1's lines |
| Draw calls | none new: no 3D objects, the arrow is a page element |
| Play probe, Day 2 (Rounds), queue on, following the arrow only | T1 shown 10:30 "Meet Zeke: Works bay, 10:45"; meeting **missed** (fix 1) |
| Play probe, Day 3 (Hauling), queue on | T1 11:47, T2 12:02 (follows Yara), T3 12:21; T3 **stuck 2.5 h** (fix 2); cleared at 17:01 when the training went back to "again" |
| Mutants (queue part) | 3 of 11 caught (fix 3) |
| Labels at 390 px | on-deck labels fit except two; every "Take the lift to Deck N: ..." form is cut (item 8) |

Probes and mutant set: scratchpad `p_train.py` (a day, logging arrow / queue / stage each change), `p_meet.py`, `p_spot.py`,
`p_do.py`, `p_lab.py`; mutants `ae_*` added to RV2's `mutants.py`. Copies are kept with these notes' commit under
`plans/review-arrows-e/`.

## Numbered list

1. **T1 points at the teacher wherever they are, so the player can miss the meeting (must fix).** The goal is
   `{ deck, room, crew: c.by }`, and `ixGoalWorld` takes `crew` first. Day 2: at 10:30 Zeke was in Main storage (room r),
   so the arrow led there; from 10:38 he stood in the corridor beside the player and stayed there (in the same run with
   the queue off he walked into the Works bay at 10:43). The player stood at the arrow until 11:15: the meeting was
   missed, Rounds not learned. The plan says "the teacher, if they are there; else the meeting room". Fix: point at the
   meeting room, and at the teacher only once they are inside it (e.g. `crew` only when the teacher's tile is in `r.room`).
2. **T3 sends you to the board while you hold another job, and hides that job's arrow (must fix).** The board offers no
   Take it while you have a job ("You have a job. Finish it or drop it to take another."). Day 3: from 12:19 the follower
   opened the board every 3 minutes, "nothing to take", until the drill at 14:50; the galley-plant job's own arrow
   (`ixJobGoal` "Repair the galley plant") never showed; the training lapsed to "again" at 17:01. Fix, simplest: while
   `myJob()` is a job other than `c.j`, T3's `goal()` returns null (the queue then leaves the arrow to your job), or says
   "Finish your job: then your turn is on the board" and points at the job. A check line for it (item 3).
3. **The check covers T1 only (must fix).** Planted faults caught: T1 too early (`ae_from`), T1 never done
   (`ae_meetdone`), a throw (`ae_throw`). Missed: T1 at level 4, T1 at the wrong room, T2 never asked, T2 not following
   the teacher, T2 at level 6, T3 never asked, T3 not done when taken, and guideTick no longer calling guideTrain (the
   test calls guideTrain itself). Add to the queue part: T1's level and that it points at the room while the teacher is
   elsewhere; T2 shown on 'watch' with `crew` = the teacher and gone at 'do'; T3 at the board, gone when the job is
   taken, and not over another job of yours; one test that lets a ship minute pass with the loop running (no direct call).
4. **Which trainings get T3 (lead to decide).** guideTrain applies to every big row. Two don't fit: m6, the burst pipe
   (decided: the job is taken at the pipe, so "on the board" is wrong; F4 / FX3), and t2, the Tier 2 test (24p's
   `offer` goes straight to 'do': you get "Your turn: the tier 2 test job, on the board", a level-3 learning arrow on an
   exam). Suggest skipping rows whose `WORK_MECH[id].offer` exists, or a per-row opt-out.
5. **Depends on trainTell's direct arrow moving to the queue (not E's fault; owner 24 core / FX1).** trainTell still calls
   `setGoal(...)` when no job is tracked; with the queue on, that direct goal stays in charge (B's rule 6) and T1 shows
   only as "covered", while the old arrow never clears. In the probes it didn't happen because a real game carries a
   stale job id in `track` (trainTell then sets nothing). The migration list in arrows-briefs.md puts this line in piece E;
   the lead's go kept E out of trainTell, so it needs an owner. (From reading the code; not played with track empty.)
6. **Errors in guideTrain are swallowed for good (small).** `try { guideTrain(); } catch (e) {}` in guideTick hides any
   later break (a renamed 24 core field) silently, every minute. Suggest `console.warn` once.
7. **T2's `once` has no day in its id (small).** `train:<id>:watch` counts once ever: after a reload mid-watch, or when
   a training is offered again, T2 does not come back on the default setting. The tip already shows once (ixTip); suggest
   adding `c.d` to T2's id (as T1 has) and keeping `once` per training.
8. **Words and phone width (for the writer; small).** At 390 px the label box is 258 px. On the deck all fit except
   "Your turn: hauling and stores, on the board" (270 px) and the t2 one (261 px). Every off-deck form ("Take the lift to
   Deck 5: meet Zeke: Works bay, 10:45", 324 px) is cut, so T1 loses its time. Calder appears as "Ines" (the plan's
   examples say Calder). Stand-ins until the writer's keys, as AR1 noted.
9. **Record keeping (small).** The plan page says piece E is "in section 24 core" and T1-T4; it was built in 15b's slot
   (lead 28's go) and T4 (the device pointer, needs piece C) isn't built. Note both on the plan page / build table.

## Checked and fine
- Off: guideTick only runs with GUIDE_ON; the new code is function definitions only; identical as above.
- The hand-over: T1 goes when the stage leaves 'meet' (met or missed), T2 when it leaves 'watch', T3 when the job is
  taken or the stage moves; each arrow cleared when its moment ended in the probes.
- Order with the shift's arrows: the clock-in/out and drill arrows are still direct goals, so they stay over T1-T3 (Day 3
  14:50: the drill covered T3, as rule 6 says). When piece D makes clock-out a level-4 entry, T3 (level 3, `until` sliding
  8 hours) would beat it at the end of a shift: D should keep that in mind.
- T2 follows the teacher on her deck (the crew position), and the job's spot when you're on another deck.
- Piece B as E uses it: `guideAsk` re-asked each minute keeps the first-ask time; `guideStage`/`guideTaken` behave.

## Re-check of AC1's fixes (claude/arrows-c d99a9e50, the E fixes in 77548cf): PASS

AC1 took E over from AR1. Read the diff (15b's slot only, plus one line in B's guideGoal: an empty goal clears `shown`).
| Check | Result |
|---|---|
| cadet_test 2b4a05db vs d99a9e50, alone | ALL IDENTICAL |
| arrows_check queue (AC1's new T1-T3 and tick lines) | ARROWS CHECK OK |
| Mutants on the new lines (ae2_*, 10) | 10 of 10 caught (level, crew always, no T2, T2 without the teacher, T2 id without the day, T3 not done when taken, T3 over another job, T3 on an offer row, no tick, B's empty-goal line) |
| Day 2 probe, queue on | T1 "10:45 meet Zeke: Works bay" led to the Works bay: the meeting was **met** (was missed) |
| Day 3 probe, queue on | T1, T2 as before; at 12:21 T3 gave the arrow back to the held galley-plant job (was 2.5 h at the board) |

Items 1-4 and 6-9 are fixed as asked (item 4: no T3 for rows with their own offer, m6 and t2; item 8: time first, "Your turn:
<lesson>", "Calder"). Item 5 (trainTell) moves with piece D (lead 28's call).

Notes for later, not blocking:
- While T3 gives way to another job it is still the queue's pick, so a lower entry (piece D's level-4 shift entries,
  level 5-6) can't show in that time either; the job's own arrow does. Piece D should keep it in mind.
- Day 2 (same probe): after the meeting, Rounds' own direct arrow "Take your first round at the job board" (section 24a's
  setGoal, not E) has the same problem T3 had: it sat at the board from 10:47 to 17:01 while the player held the
  main-lift job, and Rounds went back to "again". For F1 (or FX1).
- Day 3: the training still lapsed, because the follower never finished the galley-plant job (the known calibrate chore,
  "nobody yet" in arrows_check), so T3 never came back. Not E's.
