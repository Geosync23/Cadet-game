# 0.99.91 round 09991: R6's share (interactions_check whole)

- Candidate: claude/staging-09991 4d8869ec, build 0.99.91, GO from BM28 (for lead 51).
- Game sha256: 475bac8605fe9e26d2cd6035bcbd924dff315bac7eecdd39be12ff287f5b453e (matches the GO).
- Check file: interactions_check.py as at 4d8869ec. perf_check is R4's this round (round-09991.md).
- OLD: 0.99.9 main bfbcbdf (583d99ba...bd16, checked).
- Setup: CADET_WORK=/tmp/work-r6, CADET_CHROME=/opt/pw-browsers/chromium, three r128 via npm pack; two browsers at most.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole), candidate | FAILED, exit 1, 00:06-00:47 UTC | one FAIL (below); draw-call peak 220 |
| the same check on OLD bfbcbdf | OK, exit 0, 00:48-01:32 UTC | `INTERACTIONS CHECK OK`; "pod 1 tagged out each evening before: {'7-sim-2': 48}" |

## The FAIL (NEW: not on OLD)

`FAIL a pod tagged out the evening before is never planned; the other still is ({'7-sim-2': 48, '7-sim-1': 1})` (the sim bay
part). With sim pod 1 tagged out each evening before (days 1-6), one crew plan still used pod 1.
- Piece: EV9991_SIM_ON (EV2's Sim night also Wed Day 3). EV2: the planner's seat picker didn't apply simPlanShut to a
  tradition's pod seats (Day 3, varga-tariq, 7-sim-1).
- Confirmed here with a probe of the sim-bay block (interactions_check.py lines 1-58 + 1291-1396, unchanged): candidate FAIL
  2 of 2; candidate with only `var EV9991_SIM_ON = false;` PASS 2 of 2 ({'7-sim-2': 48}).
- EV2's fix, claude/p9991-flightsim 5f9aa4a (game 24af9479...411f off; d830f5ab...9005 with the switch on by EV2's sed):
  the same block on the ON copy PASS 2 of 2 ({'7-sim-2': 48}, nobody in 7-sim-1); pilots in the pods days 1-6 unchanged
  ({'7-sim-1': 27, '7-sim-2': 33}).

R6: FAIL on 4d8869ec (one NEW FAIL, owned by EV2, fix tested OK). Re-run whole on the next candidate.
