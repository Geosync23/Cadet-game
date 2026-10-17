# Review: claude/arrival 7cca991..9de4291 (0.42.25 reviewer 1's lows; 0.42.26 the week in play, the pilot on the frame clock)

Reviewer 1c, 2026-10-17. Diff: `git diff 7cca991 9de4291` (section 21, intro_check parts 8, 10 and 12, DEV_NOTES, the handover). Tested on **arrival 9de4291 + decks-p3 cad5c89 (the Tern) + the sim branch head 8f4d49f (0.26.38-0.26.40, including 0.26.39's dinner seats)**, content caecb7d baked. Only build-line conflicts, plus player_check's washer case.

**Verdict: PASS WITH FIXES.** Everything new works. One finding is about the evening's timing with everything combined.

## Works (checked)
- **The week in play (part 12, `--week`):** every beat heard in full: Mon wash 4/4, Mon dinner 5/5, Tue booths 4/4, Wed pick 5/5, Wed store 5/5, Thu quiz 5/5, Fri invite 4/4, Sat Sowing 5/5; Tomas brought to the garden (3-tend-3).
  - `introBeatTick` keeps the teacher stopped through section 10's `talking` countdown, which counts seconds.
  - Leaving the room drops the rest of the beat; each beat plays once (`:said`).
- **The health check (part 10):**
  - missed on Tuesday, it's rebooked once for the next day: `[['14:00', 1, 'missed', 'checkup'], ['14:00', 2, 'yes', 'checkup']]`, with Rina's Mail;
  - the device sends `apptMissed`, and `'checkup'` is a known kind on every branch;
  - New game doesn't double-book.
- **Seek-ask Mail:** Pell's Wednesday ask with you away sends "Quiz tomorrow" once. It matches social's `seekAsks` by the exact `from`.
- **The pilot on the frame clock:** the ramp is open 5 s after signing, with his line. `done.pilot` is saved, so a reload at 'ramp' before he speaks shuts the ramp again and he speaks. My setTimeout low is fixed.
- **The dinner seats** (0.26.39 in this merge): you 3-mess-10 (your `ACT.placeId`, part 8's new stop-and-sit assert), Torres 3-mess-12, Calder 3-mess-9.

## SHOULD FIX (medium, a design call for the lead): the arrival evening has almost no slack before 19:00
- **intro_check FAILs on this merge:** "following Torres, some core tour lines are never heard: servery" (26/27; servery 2/3).
- With the Tern start and today's sim, the walk runs later than on the 0.60.3 build:

  | | 0.60.3 combine (no Tern) | This merge (Tern + sim head) |
  | --- | --- | --- |
  | servery step | 18:39 | 18:49 |
  | table | 18:47 | 18:56 |
  | free | 18:50 | 18:59 |
  | night | 19:00 | 19:01 |

  The servery's last core line was still waiting when 'night' came at 19:00, and the tour queue only finishes during 'free'. Onboarding's own run, on sim b9089d9, had dinner at 18:55 and passed: one minute either way decides it.
- **Why it matters:** intro_check's follower keeps pace with Torres. A real player who stops to look, misses a lift or wanders reaches the table nearer 19:00 or after it. Then the dinner chat and Calder's visit are missed and only come as Mail gists, and so do the tour's last lines. That's the scene the user plays first.
- **Fix (pick one; it's the evening's schedule, so it's the lead's call):**
  - move 'free' (and so 'night' and Tomas) later, e.g. 19:30;
  - or start the arrival earlier (17:30);
  - or cap the tour's total pause, so the walk can't run past about 18:45.
  - Then make intro_check part 8 fail if the table step starts later than about 18:50, so the slack is guarded.
