# RV9: review of 0.91.0 before its six-runner round

**Role:** reviewer only (notes, never the game). Branch `claude/review-rv9`. Session session_01E31oZQU7DFbZnh2BesWsnM.
**People:** lead 29 session_01A9rNreAGVbsY1HgPucDMA7; BM14 (build master) session_016mhGtsCxEgPCFn9C767yjq; CP1
session_015ZhJRKCEditHrVhwdhszYq (claude/controller).

## Verdict: PASS (2026-10-22, about 21:40), sent to lead 29 and BM14

0.91.0 = claude/integration-next-fe1 **989fd566** (game sha256 da9f1d08...) on CP1's claude/controller **9a8eac0b**
(0.90.9 = the controller, switched off, merged with 0.64.16 b9f053ba; game sha256 0b7b9154...).

An earlier pair (f929c0b0 = controller + 0.64.17, e27b8bfe = 0.91.0 on it) was dropped when the user rolled back
0.64.17's breakfast; the findings below that came from it are marked.

### Part 1: 0.90.9 (9a8eac0b)
- The merge: `git merge-tree --write-tree 521ef086 b9f053ba` conflicts only on the two build lines; resolved to the
  controller's side, it equals 9a8eac0b's game apart from those two lines (0.90.8 -> 0.90.9).
- cadet_test, run alone, 0.64.16 -> 0.90.9: ALL IDENTICAL; 0.64.16 -> 0.90.9 with `const PAD_ON = true`: ALL IDENTICAL.
- controller_check (the branch's own, unchanged since 521ef086), every part but reach, in two lanes: 25 parts OK;
  **touch** and **day** FAIL (both known to lead 29, not blockers).
  - touch is check-only: `seen 57 -> 54` at tap0. The pad run still shows P3's one-time "Controller connected" message
    at tap0 (real-time 5.6 s timer), and SEEN_STATE leaves the message box out (3 elements: #toast, #tt, #tx) only
    when it says that; the no-pad run's box is counted. The pictures are identical. Fix for CTT2: leave the box out in
    both runs, or clear toastTimer before tap0. (probe: review-rv9/probe_touch.py)
  - day: the pad route stops at the lift/ladder (`ladderPanel`); lead 29/CP1 call it a controller-only follow-up.
  - pick failed on the dropped 0.64.17 base ("the ring never offered a seat in the crowded mess") and passes on 0.64.16:
    breakfast moved the crew.

### Part 2: 0.91.0 (989fd566)
- The game file is exactly 9a8eac0b plus the five fixes' own game diffs, applied with `patch` in order (191d1853;
  63710eb2 from its merge base; 6261ecc0 from its merge base; 6b8bb392 from its merge base; 7886bfdf, whose hunks equal
  AR2-passed 02e212f1), apart from the two build lines. No #newgame / newBtn left in the game.
- cadet_test alone 9a8eac0b -> 989fd566: a box of 3638 px in every shot (the HUD New game button gone) and, in e_night
  to i_tap3, about 11,400 px more: the lift arrow's label ("Take the lift to Deck 3: food, Deck 3" becomes "Tap the lift:
  Deck 3 · Food"). Proved apart: base + fixes 1-4 vs 989fd566 differs only in e_night to i_tap3; looked at the crop.
  Crew, taps, errors are the same.
- check_fast (worktree of 989fd566): QUICK CHECK OK in 248 s.
- A copy of 0.91.0 with PAD_ON true: player_check OK, bubble_check OK, interactions_check OK, device_check OK.
- My pad check (review-rv9/rv9pad.py; `python3 rv9pad.py /path/controller_check.py GAME.html`, with cadet_test.py
  beside controller_check.py; it switches PAD_ON on in a copy):
  1. A tray eaten at a long-table seat and a lounge seat by the ring and A: eat, fed, the tray gone, food +9.5. On
     0.90.9 the same script only sits you down (so it catches the bug). A seat someone is in says "X is sitting
     there.": the script tries the next one.
  2. Settings: the New game row with the switch off; the same rows with it on and no pad; with a pad seen, both rows
     (New game, then Controller settings last). By pad: New game asks, Keep playing backs out, Start over starts a new
     game and closes the device; Controller settings opens padsettings, and B goes back to Settings.
  3. Bunk by pad at 10:00: your own bunk lies you down with "Too early to sleep: you can turn in from 20:00..."; another
     bunk in your room says "... Yours is the next one."
  4. The seek chip (z-index 2) with the pad highlight on it, at 390x844 and 1280x800: it has focus, the 4 px teal
     outline shows left, right and above, and nothing covers it (elementFromPoint at its corners and middle).

### Not blockers, for the record
- By pad, standing at 3-mess-1, the ring offers 3-longtable-1 (the long-table seat on the same spot) and never the
  mess seat itself; 0.90.8 does the same (review-rv9/dbg_mess.py), so not from this merge. For the controller
  follow-up.
- reach (the 2-hour sweep) was not run.

## Gotchas
- `pgrep -f NAME` / `pkill -f` match your own shell's command line (it kills the shell: exit 144). Kill by pid.
- Two browser checks at once at most; a third makes screenshots time out (seen once on the wide seek shot; a rerun
  alone passed).
- controller_check's parts run on a copy with PAD_ON true (ON_SRC); a probe must do the same.
