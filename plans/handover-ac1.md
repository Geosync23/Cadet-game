# Handover: AC1, arrows builder (pieces B, C, E; D-F callers next)

Started 2026-10-22 by AC1 (session_01LDmfZ93ttCJ4XfoSDkJqx2), kept up as work goes. Lead: lead 28
(session_01S7AdxK1ZyXiEFowP3k5gng). Read CLAUDE.md, DEV_NOTES ("The panel pointer", "The arrow queue"),
plans/arrows-briefs.md and plans/handover-ar1.md first.

## Branch and state
`claude/arrows-c` (from claude/integration 2b4a05db, 0.64.15, with claude/arrows-plan merged in). All three pieces are
switched off (`POINT_ON = false` in section 19's slot, `var GUIDE_ON = false` in 15b's slot); cadet_test vs 2b4a05db
ALL IDENTICAL; check_fast OK.
- **B, the arrow queue** (AR1's, 15b slot): RV2 PASS WITH FIXES; the two check cases added (5dd6b6f's review), plus
  `guideGoal` clears `GUIDE.shown` on an empty goal.
- **C, the panel pointer** (mine, 19 slot): `pointAsk` and its helpers; the lift's deck picker pointer; Settings'
  Teaching arrows (`teachMode()`, B reads it via `guideMode()`). One hook outside 19: 15b ixBoard `row()`'s data-job.
  RV2 reviewing (asked for the covered-target case: added, 5a783387).
- **E, the training arrows T1-T3** (AR1's, fixed by me for RV6, 15b slot): RV6 PASS on d99a9e50.

## State at 1f2ce27d (2026-10-22 ~15:45)
- C: RV2 PASS (game d99a9e50, check 5a783387). B's follow-ups: RV2 fine. E: RV6 PASS (d99a9e50).
- arrows-c now also carries FX2 (p5-fix2 cc2bb2b) and FX3 (p5-fix3 e6bcf82, then 360801c) as merge commits (lead 28's
  option (a)); merge their new tips in again if they push more, never rewrite. One FX2/FX3 clash resolved: ixJobStep's
  machine label (FX3's chore title first, then FX2's scan first / Tune).
- F3 and F4 (my commits 9524671, bd18997, then RV6's fixes to 5557122e): RV6 PASS. Off: ALL IDENTICAL.
  Check: `arrows_f_check.py` (about 3 min). On 1f2ce27d: check_fast, arrows_f, arrows_pointer, arrows_check queue,
  mech_check all OK.
- Next: D (shift chain, trainTell into the queue, T3's empty-goal pick) once FX1's tip comes; F1/F2 per lead 28.

## State at 3519abab (~16:20)
- RV6's F3/F4 review (plans/review-arrows-f.md on claude/review-arrows) answered: 1, 3, 4, 6 fixed; 2 found to be the
  rec deck's climbing wall taking the tap for the climbing holds' job (7-wall-holds) with the arrows on or off: routed
  to lead 28 (rec deck / systems), not ours. 5 (owners' reviews) with the lead.
- arrows_check's follower calls `pointNow().el()`, but pointNow() returns an id: it never presses a pointer. One-line
  fix offered to the lead (use `POINT.aim`).
- Memory ~49%: suggested a fresh session takes D.

## State at 5557122e (~16:35) — for AC2 (piece D)
- F4's follow points where the teacher is going (the valve panel / the lift), never at her (RV6 played it: an arrow
  on a walking teacher stalls; taps at the pin land on her). Keep that in mind for D and any "follow" arrow.
- arrows_check's follower presses pointers now (POINT.aim). The climbing holds / climbing wall tap clash is FX3's.
- D is AC2's (lead 28). Start: merge FX1's tip into claude/arrows-c (merge commit), then read "Loose ends" below.

## State at the watch arrow (~17:50) — AC1 stopping here (lead 29)
- New (lead 29, AR2's find with FX1-FX3 together): `trainWatchArrow` in the 24p slot (Works career engineer's, beside
  FX1's trainArrow), a WORK_TICKS tick: with the queue off, while W.cur.st === 'watch', a direct arrow on the training
  job's spot ("Watch Yara: Cargo hold"; what trainNear counts), over the board/job fallback arrows; another direct arrow
  is left alone and ours comes back; down at 'do'; none with GUIDE_ON (E's T2). arrows_check part queue checks it on paper.
  Played Day 3 (follower, arrows off, on AC2's 82b92a9 + this): watch done 12:29-12:44, 'do' reached. AR2 reviews.
- Not proven yet (lead 29 asked): Days 4-5 (tuning, scanner) reach 'do' with arrows off and on. Probe:
  scratchpad-style `p_day.py BUILD DAY [guide]` = arrows_check's Page/real_game/Follower over one day, logging arrow,
  stage, job, activity (copy in this note's commit message history; easy to rewrite from arrows_check.py).
- Open, handed to FX2 (lead 29): Day 3 'do': after the watch, the arrow says "Take a job at the job board" from 13:38
  and the follower finds nothing to take until the drill; m4 goes to 'again' at 17:01 (trained m1, m3d only).
- D is AC2's (session_015uhdrDuE49CJ8iWWX2SEeP).

## Checks
- `arrows_pointer_check.py BUILD.html` (about 5 min): C, off and on, four sizes, screenshots in CADET_WORK/test.
- `arrows_check.py BUILD.html queue` (about 4 min): B and E. Parts `shift` and `week` fail by design until FX1-FX3.
- Mutants: write each as an exact-string replace on a copy, run the part, expect one FAIL naming it.

## Loose ends (for D-F)
- RV6: while T3 returns a null goal (you hold another job) it is still the queue's pick, so lower entries (D's level 4,
  e.g. clock out) can't show then either. D should make guidePick skip an entry whose goal() is empty, or T3 drop itself.
- RV6 item 5: trainTell's direct setGoal still wins over T1 when nothing is tracked: moves to the queue in D (after FX1).
- RV6 (Checked and fine): when D makes clock-out a level-4 entry, T3 (level 3, `until` sliding 8 h) would beat it at the
  shift's end: D must order these.
- T4 (the device pointer for "Trained") not built: use `pointAsk({ path: [...pointToApp('works', ...), tab step] })`.
- Lead 28's merge note: section 19's Settings last line clashes with controller P4: keep both.
- The galley plant's calibrate pin is FX3's, not ours.

## Gotchas
- Tips (`#devTip`, top 128 px) sit just under the Device button; the pointer hides only if a tip covers the ring itself.
- A check that opens the device gets the 'device' tip first: `while (TIP_Q.length) tipDone()` before pointer asserts.
- `myJob()` needs `status: 'claimed'` and `claimedBy: 'you'`.
- `worksInit()` refuses before WORKS_START: pass `WORKS_START` in tests.
