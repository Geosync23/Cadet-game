# Review RV36 (0.99.91, for lead 51)

OLD = main bfbcbdf (0.99.9, game 583d99ba...bd16). Probes in plans/rv36-probes/ (run with CADET_CHROME=/opt/pw-browsers/chromium
when pip's playwright is newer than the browser in /opt/pw-browsers).

## B. Sim night in week 1 (EV2, claude/p9991-flightsim 1c46077 + 6625e41, game 46abc462...9fdd, EV9991_SIM_ON)

Checked:
- sha256 of the game matches the brief.
- Off: cadet_test OLD vs the branch: ALL IDENTICAL, no errors. names_check OK (off and on).
- On (a copy with the switch on): events_check OK, day_check 3 OK, weekend_check OK, devmode_check trad OK, bigevents_check OK.
- EV2's probe: sim nights on Days 3, 25, 39 (19:30-20:30); Day 2's Mail in the Wren's "Ship traditions tomorrow" digest with
  the first-showing words; Dev's card "First time in the pod?"; you fly in pod 2; the run ends 20:12 and the pod goes back.
- RV36's probe (sim_more.py): tapping a non-host (Holt) joins too; Day 25 (no card) joins; walking away mid-run hands the pod
  back within a minute; save mid-run and reload with real saving: the run ends (activities aren't saved), the pod goes back
  to the pilot, "joined" is kept. In every case no two people (or you) within 0.35 m of each other in the sim bay, and no place
  held by two.
- sim_spots.py / sim_giver.py: the pilot who gives you their pod (Zofia) walks to her next planned place, the queue bench, which
  Rina already holds, so she stands just beside the bench (about 1.2 m from Holt) until your run ends. Not stuck, no overlap.
- Words on a phone (390 x 844): the tip, the star label, the "Tap Dev to fly an approach on sim night" pill and Dev's card all
  fit (shots/d3-before.png, d3-card.png, d3crowd-mid.png).

Notes (not fixes):
1. The give toast ("Zofia climbs out of a pod...") comes the moment you tap, while she's still seated, so you go on "Waiting
   your turn" for about a minute, then "You're up." and the climb-in. Four toasts in a row; it reads fine, a little busy.
2. DEV_NOTES says the giver goes on to their plan; in practice that plan is the queue bench, which is full, so they stand by
   it. design-doc's "waits on the bench" is close enough.
3. Seen in passing, not EV2's: skipTo to Day 3 19:40 shows Calder's "Drill at three. Works bay, ten to." toast (the old
   drill's toast caught up by the jump). Piece C replaces that toast behind its own switch.

Verdict: PASS (2026-11-10). Notes 1-2 are optional polish for EV2; nothing blocks.
