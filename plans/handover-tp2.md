# Handover: TP2 (tips and fixes seat, after TP1), session_01GKuymmrDSKcr6yPNqBWPda

Role: TP2, hired by lead 51 on 2026-11-10 to build backlog TP1-1 for 0.99.91; then BM28's find E. Both are published
in 0.99.91 (game b321a4ec...95f3, main cdd9efd), both switches on. Stood down by BM28, 2026-11-11.
Predecessor's note: plans/handover-tp1.md (read it for TP1's earlier work: the 0.99.7 tips, Pockets, first-week arrows).

## What I built
1. **TP9991_SD_ON (backlog TP1-1): a shutdown booking keeps clear of your night shift.** Branch claude/p9991-tips
   (f2ea6eb, then f9ff643 with RV35's fix). Section 24w's slot: `sdHourOk(day, at)` (an hour is fine unless p5nOf(day)
   is a night and (day - 1) * 1440 + at + SD_LEN > N.from - 15) and `sdHourNear(day, at, dir, step)` (the nearest fine
   hour). Read by sdDraft's clamp, the hour stepper, the quiet pick and sdBook. Also one line in 28b's m21Raise(0): the
   Monday briefing's own booking on a night day is sdHourNear(day, 1200, -1) = 19:00 (it was 20:00). Only 20:00 on
   Days 23 and 24 is ever out (nights from 21:00); Day 22's night is 22:45.
   Known and left (RV35's note): a save already holding a Day 23/24 20:00 booking keeps it; reopening that job's
   Shutdown screen shows the draft at 19:00 until Book is pressed again.
2. **MC9991_REW_ON (BM28's find E): the week's rewire stays Tier 2.** Branch claude/p9991-rewire (dc0ae57, from
   staging 4d8869ec). Section 24q's rewBoxes leaves out a junction whose rewire jobTier would put above Tier 2 (its
   room or panel): 6-junction-1 and 6-junction-2 drop out, five stay. 24q has no owner listed (header: seat E2).

## Tests and tools
- Probe: `python3 plans/tp2-probes/tp9991_probe.py BUILD.html` (switch on in its own copy when the line says false;
  on 0.99.91, where it is already on, only the "off" half applies, so change the probe's OFF_LINE first).
- mech_check.py m21: expects 19:00 on a night day with TP9991_SD_ON on, 20:00 off.
- mech_check.py m15 alone and the full mech_check show find E (0.99.9 fails m15 on Day 46, 6-junction-1 Tier 3).
- arrows_check step6 (four ways, about an hour) covers the night days and the briefing.

## Loose ends
None open. Fresh container setup: plans/testing-guide.md section 2 (three and acorn in CADET_WORK, CADET_CHROME).
