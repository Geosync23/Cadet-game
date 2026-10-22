# Review notes: RV5, the third controller reviewer

Lead 27 (session_017UHW78qnvRTQwYpDxpodHz). Branch claude/review-controller-3 (notes only). Started 2026-10-22 ~12:15.

My share (lead 27's brief):
1. CTT2's single `controller_check.py` on claude/controller-tests (5aaa680 and later): does each part test what it
   says, does it catch its planted faults, does it pass on the good builds, no flaky waits. (Taken over from RV2.)
2. CP1's fixes for the two issues CTT2 found (facing the Wardrobe the ring starts on "Bed"; the lift not offered from
   2 m) and CP5's five small fixes from RV2's P5 review, when they land.
3. Each merge into claude/controller (0.90.3 = P1 + P2, then P3, P4, P5): controller_check full; cadet_test with no
   pad ALL IDENTICAL, switch off and on, alone; check_fast; device_check; player_check; a save without controller
   changes byte-identical; old saves load.

How I run things: each controller_check run in its own CADET_WORK; pixel runs (idle, calls, cadet_test) strictly alone.
Builds used (game file from each commit): g1ec = 1ec1612 (turn 3, 0.90.2); g090 = a2c80df (claude/controller, turn 4
WIP); gp1 = P1 cff5bab; gp2 = P2 67df90a; gp3 = P3 958421a; gp4 = P4 db80eb0; gp5 = P5 8216ad4.

## 1. controller_check.py (CTT2, claude/controller-tests 109c0b9)

### Code read (109c0b9, then the diff to 548ede7)
Sound: the pretend pad (fresh frozen copies, hidden-until-press mode a, drift), a browser per run, seeded Math.random,
the virtual clock (no real-time waits in the new-shape parts), every `r"""..."""` script parses (checked with node),
every 'src' planted fault's line is there exactly once in its builder's game (checked for all 36 at 109c0b9), a fault
counts as caught only by a failure the clean run didn't have.
Findings (for CTT2; none makes a part pass something broken today, but each can hide a fault later):
- C1 pick_one: the tap run always steps 9 x 7 = 63 frames before the tap, the pad run stops as soon as the line names
  the thing (often at once). The comment says "frame for frame the same"; it isn't (up to 2 s apart: the crew moves).
  Fix: in the tap run step 7 frames per hint the pad run read (run the pad run first and pass its count).
- C2 part_facing passes with no failure when no spot is found ("no spot on Deck 4 ..."); part_crowded falls back to a
  plain Sit when no seat with a person on its point comes up, and passes. Both should say "not proven" as a FAIL (or a
  RESULTS 'n/a' line), so a deck change can't quietly turn the c7 / t3_noface cases off.
- C3 No planted faults for CT1's old parts off, quiet, base, deck, pick1 (CP1's api/panels/lists got theirs at 35c2c51).
- C4 CP2's tiles waits 1.5 s of real time (`wait_for_timeout(1500)`) for the board's own timer: under load (two checks
  at once, load 9 on 4 cores) that can be short. Wait for the condition (`TL_GAME.s.over` and the end row drawn) with a
  timeout instead.
- C5 'calls', 'touch' and 'idle' compare pictures with a 1-level allowance; fine, but say in the note they must run
  with no other browser (as cadet_test).

- C6 part_crowded prints the bottom line read in the same moment the check sets PAD_PICK.sel, before a frame has
  redrawn it, so its message can name the old choice ("A on 'Talk to Olu Farouk' (place:3-longtable-2...)"). The
  test itself is right (it judges by the chat card); read the line after one frame for the message.
- C7 Seen while running: the ring offered "Talk to Olu Farouk" with its screen point on Emeka Halloran (crowded mess).
  A re-finds the person when pressed, so this is likely fine, but nothing tests it: a pick case "Talk to X" whose point
  is on Y should check A talks to X. (Question for CP1, not a check bug.)

### Runs (each controller_check in its own CADET_WORK, at most two at once; the pixel parts with a 1-level allowance)
| Build | Parts | Clean | Planted faults |
|---|---|---|---|
| 0.90.2 (1ec1612) | walk | OK | 10/10 caught (CTT's 6 + PR9 c1, c2, c3) |
| 0.90.2 | touch | OK | 3/3 (incl. PR9 c4) |
| 0.90.2 | pick | FAIL only on the two known findings (Wardrobe starts on "Bed"; the lift never named) | 7/7 (PR9 c5, c7; RV2 t3_noop_crew, t3_noface; 3 of CTT's) |
| 0.90.2 | odd | OK | 2/2 |
| P2 67df90a (CTL_BUILT=games) | games | OK (Tiles 9 moves, Done; Lightdisc how-to, stick, B) | not run here (CP2 moved to 5b4d9f0; CTT2 reports 11/11 on it with 1855bae) |
| 0.90.4 (95b6129) | pick | FAIL on the same two findings | - |
| CP1 pickfix 8d68ad5 | pick | OK (Wardrobe right, the lift named, A = tap for crew, item, sealed door, lift) | 7/7 |
RV2's t3_noface and PR9's c7, missed before, are now caught on both 0.90.2 and the fix.

### Verdict on controller_check (109c0b9 parts run; 548ede7/3b1cade/1855bae read as diffs): PASS WITH FIXES
None of C1-C7 lets a broken build through today. Fixes for CTT2: C1 (frame-for-frame pick), C2 (not-proven cases as
failures), C3 (faults for CT1's old parts), C4 (CP2's real-time wait), C6 (message). Not yet run by anyone: day, the
reach faults, the full reach sweep (about 2 h alone).
