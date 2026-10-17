# Handover: adversarial reviewer 1d

- **Role:** adversarial reviewer, started for the career engineer (session_01862tURG1qXAVGj2sdUrVCw, branch `claude/leave`). The lead (session_01KPJMYjXAPkNUcrQ8VRkhLE) also sent other seats' work. Report to the lead and the owning seat with send_message. Never change game code; never contact the user.
- **Branch:** `claude/reviews-4` (from claude/reviews-3), notes only under `plans/reviews/`. The format is as reviewer 1c's (plans/handover-reviewer-1c.md):
  - PASS / PASS WITH FIXES / FAIL;
  - a severity per finding;
  - a concrete fix;
  - a probe where it matters (saved next to the note).
- **Cost rules (the user):** in-depth reviews only for behaviour and save changes; run the checks you need, not the whole set.
- **Stopped at about 70% memory** (18:50), with the queue empty. The next review goes to a fresh reviewer.

## Done (2026-10-17)
| Item | Note | Verdict |
| --- | --- | --- |
| claude/leave 492364d (0.61.0-0.61.2), leave and being let go | leave-492364d.md (+ two probes) | PASS WITH FIXES: two MEDIUMs (an old save's false miss; a summons on your leave day) and lows. All fixed in 8f1f88a. |
| 8f1f88a (0.61.3) | leave-8f1f88a.md | PASS |
| 90272ef (0.61.4), the Chief's talk after 3 missed in a row (the user's rule) | leave-90272ef.md | PASS; design note: 2 missed, 1 worked never warned |
| b097097 (0.61.6), the Chief's talk also under 15 | leave-b097097.md | PASS (can go into 0.60.5 alone) |
| b0c0f37 (0.61.5), rare sickness | sick-b0c0f37.md (+ probe) | PASS, three lows (all fixed later) |
| 4dd0409 (0.61.7 words) + 6bc69ea | sick-6bc69ea.md (+ probe) | PASS (skim) |
| 9268f00 (0.61.8) and 1612d2b (0.61.9) | sick-9268f00.md | PASS WITH FIXES: the missed tip fell into a `//` comment |
| f7fb180 (0.61.10), c093b15 (0.61.11), 8d5b084 | sick-f7fb180.md | f7fb180: leave_check flickered (random `gs` on `?nosave`); c093b15 PASS (3 runs the same); 8d5b084 test only, PASS. **6bc69ea..8d5b084 cleared for 0.60.6.** |
| perf 3's claude/poses f9c6faa + 257b3ea (0.27.36-37) and dialogue 33b1366 (bubbles 0.43.30) | poses-257b3ea-bubbles-33b1366.md | PASS, light. Low: the trays' +2 calls unconfirmed by day_check. |
| sim 0.26.41 d59c30b (meal traditions through the line), on social-fixes afbb5c9 | sim-d59c30b.md (+ table probe) | PASS: Sunday table 90% by 18:12, the last by 18:21, waits under 4 min. Low: one diner sits with no tradition line visit. |

**Coming (not mine to start):** perf 3's fork-and-eating motion, 0.27.38 on claude/poses.

## How I test
- Setup: `pip install playwright`; three r128 in /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- **Files:** copy the build and the checks into the scratchpad (`git show <hash>:<file>`) and run there. One browser job at a time.
- **Merges:** use `git worktree add --detach <scratch>/mrg <base>`, then merge. When only build lines conflict, keep the base's. Remove the worktree after.
- **Timings:**
  - leave_check: about a minute;
  - events_check: about 15 minutes;
  - day_check: about 15 minutes a day;
  - food_check: about 15 minutes.
- **Probes** exec cadet_test.py's harness (`Game(pw, html)`, `ev`); see leave-492364d-probe.py.
- **Gotchas:**
  - Section 20 scores `shiftStart` notes only in its social hour. Call `repNote(kind, d)` directly in a paper test.
  - Run a check 3 times when anything random (`Date.now`, `Math.random`) is near the code.
  - In the plans, tradition segments are tagged `ev-<id>-...`, not the event's `tag`.
  - `plans/reviews/*.png` is git-ignored.
