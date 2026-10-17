# Handover: adversarial reviewer 1d

- **Role:** adversarial reviewer for the Career engineer (session_01862tURG1qXAVGj2sdUrVCw, branch `claude/leave`). Report to the lead (session_01KPJMYjXAPkNUcrQ8VRkhLE) and the engineer with send_message. Never change game code; never contact the user.
- **Branch:** `claude/reviews-4` (from claude/reviews-3), notes only under `plans/reviews/`. Format as reviewer 1c's (plans/handover-reviewer-1c.md): PASS / PASS WITH FIXES / FAIL, a severity per finding, a concrete fix, a probe where it matters.
- **Cost rules (the user):** in-depth reviews only for behaviour and save changes; run the checks you need, not the whole set.

## Done (2026-10-17)
| Item | Note | Verdict |
| --- | --- | --- |
| claude/leave 492364d (0.61.0-0.61.2) | leave-492364d.md (+ two probes) | PASS WITH FIXES: MEDIUM, an old save loaded mid-morning gets a false miss; MEDIUM, a summons can be booked on your leave day; lows: Pell absent from the send-off, late-every-day reaches the Chief (design call), leave_check's late notes never score, a latent q overwrite, leave lost at the cap |

**Done:** the fixes, 8f1f88a (0.61.3), PASS (leave-8f1f88a.md); the user's chiefRun rule, 90272ef (0.61.4), PASS (leave-90272ef.md). **Pending (the lead, 17:35):**
1. Career 0.61.5 (a second route to the Chief's talk) first.
2. Light reviews of perf engineer 3's claude/poses f9c6faa8 (0.27.36, seated hands and busy-work animation) and the speech bubbles (dialogue 0.43.30): check the sim and timing are unchanged and the draw calls and perf steady.
3. **Rare sickness** (for 0.60.6) by the same engineer; check `careerSick` against a day already marked missed, and sick on a booked leave day.

## How I test
- `pip install playwright`; three r128 in /tmp/cadet-work/three (DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- Copy the build and the checks into the scratchpad (`git show origin/claude/leave:<file>`), run there. One browser job at a time.
- leave_check about a minute; events_check about 15 minutes; day_check one day about 15 minutes.
- Probes exec cadet_test.py's harness (`Game(pw, html)`, `ev`); see leave-492364d-probe.py.
- Gotcha: section 20 scores `shiftStart` notes only in its social hour; call `repNote(kind, d)` directly in a paper test.
