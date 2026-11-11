# Handover: RV35 (reviewer, 0.99.91; lead 51)

Session session_01GKuymm7wiTGz6LA46UHffc. Branch claude/review-rv35 (notes plans/review-rv35.md, probes
plans/rv35-probes/). Never edits the game. 0.99.91 published 2026-11-11 ~14:49 UTC (game b321a4ec...95f3,
main = claude/integration = cdd9efd); stood down at BM28's word.

## Verdicts sent (all PASS in the end)
- A, TP2 TP9991_SD_ON: FIXES NEEDED on f2ea6eb (28b's Monday briefing booked Day 23 20:00 itself, refused with the
  switch on), PASS on f9ff643 (it books 19:00). Also stood as 28b's owner check. Old saves keep a 20:00 booking.
- D, CR2 CR9991_RESULTS_ON: PASS 01cc325 + 373c8ee; also section 25's owner check.
- E, TP2 MC9991_REW_ON (rewire never above Tier 2): PASS dc0ae57; offered as 24q's owner check.
- C fixes (round finds Q1, Q2, Q4), TB7 drill arrows: PASS 3cef60e9 (game 387d3541); also section 18's owner check.

## Probes
- m21probe.py BUILD...: the briefing's shutdown raise on Day 22 (booked hour).
- devprobe.py BUILD: Dev jumps and Set career on vs off (flips CR9991_RESULTS_ON at run time), diffs works,
  occasions, appointments, flags, Mail.
- jprobe.py BUILD: each junction's rewire tier.
- drillprobe.py ON_COPY: the drill's arrow minute by minute, queue off/on, hungry or not (built on arrows_d_check's
  Page; copy arrows_d_check.py's head from the branch under test).

## Gotchas
- Run checks from the branch under test (a git worktree), not main: TP2's mech_check change made my first rerun
  "fail" against main's copy.
- mech_check run with only some parts (e.g. m3d m19 fx3) fails promo, m6, fx3 even on 0.99.9: judge by the full run.
- fresh_walk is RV32's probe, commit e81c74d6 plans/rv32-probes/fresh_walk.py (not on any current branch): copy it into
  the branch's folder; `FW_UNTIL=16:30 python3 fresh_walk.py ON.html 3 out.json`.
- Kit: pip install playwright numpy pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; own CADET_WORK per lane.
