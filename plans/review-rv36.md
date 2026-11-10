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

## C. The Wednesday drill as Calder's talk (TB7, claude/p9991-drills 40569965, game 258ad821...2920, TB9991_DRILL_ON)

Checked:
- Off: cadet_test vs 0.99.9 ALL IDENTICAL.
- On (a copy): mech_check (TB7's version, all rows) OK; day_check 3 OK; devmode_check (all parts) OK; TB7's drill probe OK
  (Days 3 fire, 10 pressure, 17 power, at phone size).
- RV36's drill_more.py (Day 3): a tap on Calder at 14:52 gets "Three o'clock, on the muster line. Not yet." and nothing counts;
  at 15:02 it opens her talk and counts the turnout (note, reputation, the first trains it). A tap on Halloran joins the same.
  Closing her card with the X: still counted, you're sent to the line, a second tap does nothing. Save with the card open and
  reload with real saving: the card is gone, the turnout kept, no star, nothing stuck, holds let go at 15:15. Off the deck at
  15:00: the missed note, no reputation, her "We ran the drill without you". No errors in any case.
- Simple? Yes: a toast at 14:50 and an arrow, a star over Calder from 15:00, tap her, her card (six lines on the drill and its
  danger, one crew line, her close; no question), then you walk to the line and it ends at 15:15. No side job, no stopwatch.

Notes (not fixes):
1. On the phone the card's header "FIRE DRILL · Chief Ines Calder" runs up against the close X (shots/c-card-header-fire.png);
   "PRESSURE DRILL · ..." wraps to two lines and is fine. It's the shared meeting card (section 13's skin, its header has no
   room kept for the X), so any long title does it: a backlog row, not TB7's.
2. mech_check run with only some rows (e.g. `m19 fx3`) fails promo, m6 and fx3 on 0.99.9 as well: m19 leaves state the later
   rows trip on. The full run is fine. Worth knowing when re-running single rows; a backlog row for the check's owner.
3. Lead 51 asked TB7 to bring Zeke to the line or drop his line from the card (he's not on Deck 5 at 15:00). Re-check that
   change when it lands.

Verdict: PASS on 40569965, with the Zeke change to re-check (2026-11-10).

### C re-check: ff9f1e42 (game 8e1e86b4...18c7, last game change 5b86d4fa)

- Off: cadet_test vs 0.99.9 ALL IDENTICAL. On (a copy): full mech_check OK; TB7's probe OK on Days 3, 10, 17 (Calder,
  Zeke and Halloran all on their spots); drill_more.py all six cases sane, no errors.
- Header: "FIRE DRILL · Calder" clears the X (shots/c2-card-fire.png). Fixed.
- Zeke at the line: he's there, and after 15:15 he walks back to the lift and his own plan; Halloran (already on Deck 5)
  walks over and back. But with you on Deck 5, Zeke (on Deck 6 at 14:54) appears on his spot out of nowhere at 14:55
  (drill_zeke.py: off-deck one frame, standing at 5-muster-2 the next). crewScene's 'wait' places someone from another
  deck straight on their spot. The game already has a walk-in by lift for this: crewComeTo (section 14, Pillar 4's
  visits: "a crew member walks to a place on the deck you're on (by lift if they're elsewhere)").

Verdict: FIXES NEEDED (one, small): Zeke should walk in from the lift, not appear on the line (crewComeTo, or another way
TB7 prefers), checked with plans/rv36-probes/drill_zeke.py (`drill_zeke.py ON.html 893 15:01`). Everything else passes.
