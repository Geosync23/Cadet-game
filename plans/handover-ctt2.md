# Handover: CTT2, the controller test builder (after CTT)

**Handed over 2026-10-22 ~20:00 (lead 29's call, memory ~65%).** CTT3 (session_0197zJtQyLkNz6dxc3NgoNgy) takes over:
the reach sweep, and touch/pick/day on CP1's 0.64.16-based 0.90.9 (4514f19a). The file to use: claude/controller-tests
tip (ad28a369 for the check). The 0.64.17 route fixes, for both 0.64.16 and 0.64.17 builds: f717b80b (message box counted
not compared; B for a panel opened on the way; crowded mess at 07:20/07:40/08:00/08:20), 738667fb (sweep SKIP dropped),
f5613f56 (the lift button by deckLabel's rule), ad28a369 (the ride waits 20 s for the lift panel). Not yet run on a
0.64.16-based build. **Open finding, 0.64.17 only (for when its breakfast/ladders come back):** by the Deck 4 lift door
the ring says "Lift" but A walks you to the Spine ladder and its panel opens (day: breakfast "the lift panel never
opened"; repro on 54a5c5a8 or e27b8bfe; sent to CP1).

**Role:** writes and proves `controller_check.py` (plans/controller-plan.html section 10). Tests only: never changes the game.
Branch `claude/controller-tests`. Session session_011yMob9ZzgmCFENoNhjJ44z. Read CTT's note first
(`plans/handover-controller-tests.md`: how the check works, the pretend pad, gotchas); this note is what changed since.
**People:** lead 27 session_017UHW78qnvRTQwYpDxpodHz (report to it). Reviewers: RV5 session_01DdhmKNwjve4tpJ1zq6ozyv (lead 27:
"your reviewer is now RV5"; send tips to RV5 and the lead), also PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db and RV2
session_01E1TTHbhLzy2U6pAoGh7E9a. Builders: CP1 session_015ZhJRKCEditHrVhwdhszYq, CP2 session_016zb2DTsTLqNNNeuegePDgE,
CP3 session_01AkfeDe7MBN8RYd5n6obGRm, CP4 session_01VTXDwLqWGJVRh95HozqhCu, CP5 session_01VcdDgzyHa1dqdmcRLELbiS.
CTT (idle) session_01SgEbMMMNPRP2E7DbiDyiw4.

## What CTT2 changed
1. **Crowded seat (PR9 c7) is caught.** The miss was the check's: after the check moves the player, the ring's search
   (`padSearch`, a little each frame) needs about 2 s, and every D-pad press restarts it. The check read the ring after 12
   frames and pressed every 4, so it only saw the old list from the lift. Now `part_crowded` (called by pick): Deck 3 mess at
   07:40, stand by a free seat beside someone seated, wait 72 frames, list the ring by D-pad, then (RING_PICK_CROWDED) take a
   "Sit" whose screen point has a person on it at that moment, make it the ring's choice (as the D-pad does) and press A at
   once. A must not open a chat. Faulty (c7): chat with Olu Farouk, caught. Good 1ec1612: no chat.
   The same 72-frame wait is now used for every pick target and the facing test. Two findings stay with it, so they are
   real (CP1 says turn 3, CT1's; passed to lead 27): facing the Wardrobe on Deck 4 the ring starts on "Bed"; the lift door
   is not offered from about 2 m.
2. **The builders' old-shape parts are folded in** through `legacy_parts(GAME, ON, fails)`: their functions copied as they
   are (indented one step), with their own `check`/`fail` that collect into a list (so a planted fault fails only its own
   run), `Pad` making its Game through `old_game` (adds CT1's pretend pad, OLD_FAKEPAD, to INIT for that page only).
   `legacy(name)` writes the off and on copies of whatever build it is given and runs `part_<name>`. Names:
   off quiet base deck **pick1** (CT1's pick) panels api lists (CP1), tiles disc screens (CP2), marks **touch3** drop (CP3),
   settings (CP4), a11y (CP5). Needs in OLD_NEEDS (CTT's naming: games, marks, settings; a11y needs panels + pick).
   **To update a builder's part:** the generator in the scratchpad was `gen_legacy.py` (takes CP1's file from `class Pad` to
   `PARTS`, then each builder's names not in CP1's file); by hand: replace that builder's `# ---- CPn (...)` block inside
   legacy_parts with its new functions, indented 4, and the tip in the heading.
3. **CTL_BUILT=pkg,pkg** counts packages as built (a builder's branch before PAD_BUILT names them).
4. Every builder's planted faults registered (MUTANTS[...] with the builder and tip in a comment), each line checked once
   in its builder's game.

## Results (2026-10-22, each on the builder's own tip)
| Builder (tip) | Parts clean | Planted faults |
|---|---|---|
| CP1 (claude/controller-p1 cff5bab) | off quiet base deck pick1 panels api lists: all OK | 7/7 caught |
| CP2 (claude/controller-p2 67df90a, parts as e62efcc) | disc OK, screens OK, tiles unsteady (failed once: "A on your hold should pick its tile and keep the highlight there (None)"; passed alone on rerun; Tiles redraws on a real-time timer) | 8/11: NOT caught 'the stick also moves the highlight' (disc), 'a turn card asking again jumps back' (screens); 'a redraw loses your place' only differs from the clean failure by its message. Told CP2. |
| CP3 (47d71ff) | marks, drop OK; touch3 unsteady (2 of 3 runs fail on a speech bubble's pixels; fix proposed to CP3: hide .bubw in its shots) | 5/5 caught (incl. the new 'Controller connected over another message') |
| CP4 (7631ab6) | settings OK | 7/7 caught |
| CP5 (4892a0b) | a11y OK | 7/7 caught |
| this check's pick on 1ec1612 | FAIL only on the two real findings above | PR9 c7 caught |

## Results after RV5's fixes (14:30)
- pick on 1ec1612: c7 caught; crowded talk OK (A talks to the one named, Olu Farouk, with Emeka on its point); lone seat on
  Deck 3: A = tap. Fails only on the two real turn-3 findings.
- CT1's parts on cff5bab: off quiet base deck pick1 OK; 9/9 new faults caught.
- day on claude/controller 0.90.5 (after three check fixes: steering by the view's axes, your own bunk via MY_BUNK, wait for
  the alarm card): talk OK, bedtime + Set alarm OK; breakfast and the job board blocked by the lift not being offered.
- CP1's 3dfe6579 (pick1 PAD_MARK, settings PAD_LAYOUTS): copied in.

## The full file on claude/controller 0.90.8 (fda82c1a), 16:00-17:30
CP1 replaces claude/controller's merged copy with this file (lead 28's call; RV5 checks it). Added for it: CP4's
part_firstuse and the newer part_settings word for word from fda82c1a; CP4's 'padTick ignoring the map' fault on 0.90.8's
line. Results: idle OK 3 runs alone (+7/7 faults; the welcome-message fix in Run holds), save OK, calls OK, pick OK, unplug
OK, games OK, day OK (a whole day by pad), walk OK + odd OK (11/11 faults) after in_use() (B before a measured walk: CP4's
first use counts a push on an unused pad after 0.15 s, by design); all 17 builders' parts OK. touch: fixed to leave out P3's
one-time "Controller connected" message (by design, real-time timer); rerun alone pending. reach: running.
Leads since: lead 28 (session_01S7AdxK1ZyXiEFowP3k5gng), now lead 29 (session_01A9rNreAGVbsY1HgPucDMA7): report to lead 29.

## 0.64.17 in the controller (0.90.9, claude/controller-p1 54a5c5a8) and the 0.91.0 candidate (claude/integration-next-fe1 e27b8bfe), 19:30-
CP1 found 3 FAILs on 0.90.9 (touch, pick's crowded seat, day): all the check's routes meeting 0.64.17. Fixed: touch's view
counts the message box but doesn't compare its text/classes (hidden welcome text vs "Controller connected"); the day's
lift picks the deck button by DECK_ORDER (labels are deckLabel now); walk_to presses B when a panel opens on the way
(ladder hatches); the crowded mess tried at 07:20/07:40/08:00/08:20. The sweep's SKIP {'#newgame'} dropped (gone in 0.91.0).
Results on the 0.64.17-based 0.90.9 (54a5c5a8) and 0.91.0 candidate (e27b8bfe): touch OK (+3/3 faults), pick OK; day: talk,
the job board, bedtime OK; breakfast FAILS: "the lift panel never opened": by the lift door the ring says "Lift" but A
walks you south and the ladderPanel opens (A's point reaches a ladder hatch on 0.64.17's ladders): a controller finding,
sent to CP1. Then the user rolled back 0.64.17's breakfast: the controller is redone on 0.64.16 (CP1's 4514f19a, not
pushed at this writing). Next: run touch (alone), pick, day on it; fixes must pass on both (breakfast comes back).
Also since: the day's lift button found by its label (deckLabel's rule, 'R' for deck 7: DECK_ORDER/deckLabel live in a
script the check can't reach); the ride waits up to 20 s for the lift panel and says so if it never opens.
CTT3 (session_0197zJtQyLkNz6dxc3NgoNgy) has taken over the reach sweep (lead 29).
Send the results and the commit to CP1 and BM14 (session_016mhGtsCxEgPCFn9C767yjq); BM14 builds 0.91.0 on CP1's 0.90.9.
The reach sweep on 0.90.8 (stopped partway): its pad half missed Roster, two Tracked rows, Calendar's 2nd "Don't" and
the Maps plan svg. CP1 showed all four buttons are reachable (the zigzag covers a dozen rows only): now a second chance
steers straight at each (pad_to, 40 presses); the plan svg is in PAD_COVERED (covered by the Rooms list, PR9's ruling).
A full sweep to confirm: ~2-3 h alone, not yet run.

## Loose ends
- CP3 says the Pause card's line now has id="pauseLine": the unplug part could read it instead of the card's whole text.
- The day part now runs (STEER by the view's axes, next cell, through people if no way round; MY_BUNK; FREE_SEAT).
- The sweep: alike things with the same label pressed twice only (the map's pins made it dive); it still gets lost in
  Tracked (replays); reach faults never run yet.
- PAD_BUILT on claude/controller (0.90.3): ['base','deck','pick','panels']; CP1 will add 'games' (P2), 'marks' (P3),
  'settings' (P4); P5 gets no name.

## RV5's review (PASS WITH FIXES, 13:34) and what was done
C1 the tap run waits as long as the pad run read the line (pick_one's presses); C2 facing and the crowded seat FAIL as
"not proven" when their case doesn't come up; the lone seat is searched on every deck (found on Deck 3, 3-visit-1); C3 faults for CT1's
off, quiet, base, deck, pick1; C4 is CP2's (tiles' real-time wait: told CP2); C5 below; C6 one frame between choosing
and reading the line in the crowded seat; C7 part_crowded_named: "Talk to X" with Y on its point, A must talk to X.

## How to run (as CTT's note), plus
**idle, calls and touch compare pictures: run them with no other browser check running** (RV5's C5; two at once is
fine for the rest).
`CTL_BUILT=games CADET_CHROME=/opt/pw-browsers/chromium python3 controller_check.py g2.html tiles disc screens --mutants`.
Two checks at once at most, each with its own CADET_WORK (copy `three/` into it). Builders' games:
`git show origin/claude/controller-pN:starship-cadet.html > gN.html`.
