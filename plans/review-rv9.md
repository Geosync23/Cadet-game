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

## Verdict: CP1's claude/controller-follow1 3f17ac95: PASS (2026-10-22, about 23:10), to CP1 and lead 30

Two commits on 9a8eac0b, section 26 only (8 game lines): (1) padFind, for a place key, tries 4 rings of 8 screen points
(10-40 px) around the spot when the usual points miss; (2) padWhat returns 'ladder' where ladderAimed(h) (tap()'s next
step after a walker).
- cadet_test alone vs 9a8eac0b: ALL IDENTICAL, switch off and PAD_ON true. check_fast OK (224 s).
- controller_check (CTT3's claude/controller-tests-3 2bead1b5 file), all but reach: 26 OK; pick FAIL "crowded seat: not
  proven", the same on 9a8eac0b with that file (CTT3's check-side item). touch and day OK.
- Mess seats by pad (review-rv9/dbg_mess2.py: stand at each of the 44 mess seat spots, 72 frames, Monday 06:00):
  offered 7/44 before, 23/44 after, none lost. Still missed: 3-mess-2..6, 12, 14, 18-22, 24, 25, 27-32, 39 (not
  proven why: the 8-item cap in a crowded mess, or a person on the point). rv9mess.py: 3-mess-1 offered, A with a tray
  eats there (ACT.placeId 3-mess-1).
- Ladder (review-rv9/dbg_ladder.py): by the Spine ladder's hatch on Decks 4 and 3, five spots each, the ring's targets
  are the same on both builds (Spine ladder still offered as item:N), plus place:3-bench-2 from (1). padWhat says
  'ladder' whatever ladderTap would do; tap() takes that step only if ladderTap(null) succeeds, which fails only with
  the ladder off, mid-ride, or with no way to the ladder room and no hatch.

## Verdicts, 2026-10-23 (lead 30, then lead 31 session_0118SXBCdg87nDiXdtrGNVSR)
- **FX5 claude/p5-fix5 c5eb7119: PASS** (to FX5 session_01LGRr55ZQCd11PuqhJEn9Jj, AC3 session_01DiLRzrXgkeoAZCoX1mVJn9,
  the lead). WORK_MECH.p3.open trains when W.use.p3 > 0 (worksUse's small-row rule: a use trains only once the row is
  open); worksTrained can't train twice. mech_check: OK on the fix; on 46e594cd only the new 24k line fails. cadet_test
  ALL IDENTICAL; check_fast OK.
- **FX4 claude/p5-fix4 tip fc2e1c6d: PASS** (to FX4 session_01BueJ4UzQkn8HcC1TXd1KrW, AC3, the lead).
  e38eba4d: trainArrow's busy needs the held job taken before the window (j.start, set at every claim). career_check
  (p2) fails on 5f7e91cd, all OK after; intro_check all OK (part 14: the solo job keeps the arrow to 10:40); cadet_test
  ALL IDENTICAL; check_fast OK. FX4 + FX5: the game merges cleanly; mech_check on the merge OK.
  fc2e1c6d: Calder's call arrow trkFrom = the meeting's end, and "Wait here" in her office. IX_GOAL === INC_GOAL.g holds
  (incGoalSet stores IX_GOAL); the follow arrow (m6.reserve) is set after the meeting starts, so the new block never
  relabels it. career_check (p3) fails on its parent, all OK after; cadet_test ALL IDENTICAL; check_fast OK.
- **DS1 claude/zeke-tour:** not pushed yet. Ready: review-rv9/zeke/addlog.py (adds a timed log of bubbles, the box,
  panels, Mail, goals and both positions to intro_check part 8: `python3 addlog.py intro_check.py`, then
  `RV9_LOG=out.json python3 intro_check.py GAME.html --evening`) and compare.py (`python3 compare.py before.json
  after.json`: lines lost, how each is given, the dinner part from toMess identical, Zeke's still spans). The before
  run on 989fd566, twice: the same 91 lines, the dinner part identical in ship time. Zeke stands still on Deck 4 at
  (19,9) 16:59-17:03 and (14,5) 17:08-17:10; in the bunk room (8,4) 17:15-17:17 before the device.

## zeke-tour 99687fc8 (DS1 session_01MZBSf7MZeb9C89wpoavLko): interim, FIXES NEEDED as it stands (to DS1, lead 31)
Before = 2b81d8a0 (0.91.0 + breakfast back), after = 99687fc8 (arrival 17:15). Recorder: review-rv9/zeke/addlog.py on
each build's own intro_check; after-run a2 also patches WALK_TICK so the follower stays while introHandDue()/introHandBusy()
(part 8's own follower walks to toMess's checkpoint at once, so the bubble scene never plays there: F6).
`python3 dinner.py before.json after.json`: scripted events from the lead-off (the hand-over's last line).
- F1 dinner part: Sunday long table toast + Brennan's "Thanks for coming" Mail at 18:20 (table step, before you sit
  with Zeke); before 18:06 (tomas step, after the Chief). introDinner/introChief identical; seats; steps within ~1.5 min.
- F2 Deck 4: off the lift fixed (was ~8 s at (19,9)); the wing stop (16,5) now ~9 s (13 samples) vs ~4 s (6 at (14,5)).
- F3 bunk room ~65 s real (scene lines 38.5 s + after 5.6 s + Mail; ~7 s at the device step; ~7 s before line 1).
- F4 introDeviceGive's toast still mid-bubbles. F5 tour extras inside the scene. F6 part 8 never plays the scene.
- Lines kept: the old introDevice panel's lines in the bubbles; its question and three answers in "Before you land".
- Next: DS1's bag commit (the user rejected the auto-stow); then the full set, his facing, the recorder again.

## Verdict: DS1 claude/zeke-tour de637c74: PASS (2026-10-23 ~06:50 UTC, to DS1 and lead 31)
Before 2b81d8a0 (16:30) vs after de637c74 (17:15), recorder on each build's own intro_check part 8 (de637c74's follower
stays with Zeke for the hand-over). Dinner part from the lead-off: scenes word for word, same seats, steps in order
(tomas +38.0/+40.5, night +102.1/+101.8), the Sunday long table back after his goodnight. Deck 4: no stop of 3+ samples.
Hand-over 15/15 lines, clock held, Mail opened, no toast, no extras; facing 0 rad on 70 samples (a copy c2 logs it).
Slow bag (c2: the bag held 59 samples, 17:55-18:18): Zeke waits, arrow "Put your bag in your wardrobe" throughout.
intro_check all OK; clothes, player, bubble OK; check_fast OK; cadet_test ALL IDENTICAL vs 2b81d8a0.
Notes: "Washrooms" line not heard on a straight walk; slow player misses the arrival dinner's Sunday long table;
"Ship traditions tomorrow" Mail now in the bunk room; DS1's Monday bag put-away is DS1's call (flagged to lead 31).
