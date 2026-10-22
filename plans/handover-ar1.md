# Handover: AR1, the arrows analyst (then builder of piece B)

Written 2026-10-22 ~13:05 UTC by AR1 (session_01XcfcbFvi4nMVUPZgT2BcmE, about 46% memory) for whoever takes the role.
Lead: lead 27 (session_017UHW78qnvRTQwYpDxpodHz). Read CLAUDE.md, DEV_NOTES ("The arrow queue"), then this.

## Branch and what's on it
`claude/arrows-plan`, from claude/integration 2b4a05db (0.64.15). This session may push only to this branch, so the
plan docs and piece B's game commits share it (the lead agreed). Commits, oldest first:
- d5a6ca9 .. 9030158, 2cae985: plan docs only. `plans/arrows-pillar5-plan.html` (the plan page, published by the lead at
  https://claude.ai/artifact/7rKvXwbZLRsJj8k7yrXXkK), `plans/arrows-pillar5-notes.md` (raw notes: my tracked-shift
  play, how the arrow works today, four helpers' notes A-D, Steps 3+ kept at the end), `plans/arrows-tools/` (the play
  harness, bot and honest shift player), `plans/arrows-briefs.md` (briefs for pieces B and C, and the arrows check),
  design-doc.md ("Teaching arrows" under the player, and an Answered entry).
- 5c798b5, c0ab64c: **piece B, the arrow queue**, switched off (`var GUIDE_ON = false`, section 15b's slot). Checks:
  arrows_check OK, names_check OK, check_fast OK (246 s), cadet_test vs 2b4a05db ALL IDENTICAL (run alone).

## Who's who (2026-10-22)
- AR2 (session_015pnwa5oK7TDF5gZXNFLLvx, claude/arrows-plan-2, plans/arrows-p5-step2-notes.md): Step 2 in play. Sends
  a drop-in HTML section for the page's `section id="week"`; the shape was agreed (my two messages to AR2). Its four new
  broken items are on the page already (2cae985).
- AC1 (session_01LDmfZ93ttCJ4XfoSDkJqx2, claude/arrows-c): piece C, the pointer. **Owns the Settings row**
  (`SHIP.device.settings.teach`, `teachMode()` in 19's slot); B reads it via `guideMode()`. AC1 writes its own
  `arrows_pointer_check.py`.
- FX1 (session_01WmdPR5B5QC56Hid3F5M1wv): arrow and tracking lifecycle fixes (my broken 1-4, 8, empty board). Asked
  which lines it edits; no answer yet. B touches goalNow, the ixFrame goal line and toast: possible small clash.
- FX2 (drill and side jobs, the scanner job, Tuning words, Calendar 06:40, "at the hold", "Repair"), FX3 (lift, burst
  pipe, small lessons, reputation shown, Record, the uniform rule).

## Piece B in one paragraph
`guideAsk({ id, level 1-6, goal, from, until, done, once, tip, owner })`, `guideDrop`, `guideNow`, `guideList`;
`goalNow()` shows the queue's pick first when on. Lowest level wins; ties by from (else ask time), then ask order.
Tracking off: levels 1-2 only. A direct setGoal goal stays over 2-6; a level 1 borrows it. 5-6 after the job's step.
`once` counted in `SHIP.guide.seen` (saved only while on, 300 ids kept); 'all' ignores once for level 3, 'off' drops
level 3. Done helpers guideAt/Near/Met/Taken/Clocked/Trained/Stage. Pop-up queue `guideToast` (asked by section 11's
`toast(t, x, o)`: HUD seat to review the line). Not done: moving the 31 setGoal callers (pieces D-F; the list is in the
brief).

## Next (as agreed with the lead)
- Merge AR2's section into the page when it arrives; tell the lead the tip to republish.
- Piece D, the shift chain (S1-S9) as queue entries: **wait for FX1** (it is fixing clock out and the empty board), then
  build the world-arrow half; the pointer half once AC1's `pointAsk` lands.
- Rebase B onto FX1 when FX1 is merged.

## Gotchas
- Dev mode's Set career switches job tracking off (track = null): a bot run from Dev mode sees arrows a real player
  doesn't. Set `SHIP.player.track` to a stale id to play honestly (shift.py does).
- The game caps a frame's time step: run the clock by checking shipNow(), not by counting frames (harness run_min).
- Dev mode's clock skip marks skipped workdays as excused.
- Parallel browser runs from one harness file collide on the temp file name: copy the harness per process.
- `GUIDE_ON` must stay a `var`: goalNow (above it) and toast (far below) may ask before its line runs.
- The auto-mode safety check refused a commit that wrote "the user said" from a relayed message: attribute relayed
  decisions ("as passed on by lead 27").

## Open questions for the user
None of mine; the five plan questions are answered.
