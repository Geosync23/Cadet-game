# Handover: CTT3, the controller tester (after CTT2)

**Role:** proves `controller_check.py` and runs it for the builders. Tests only: never changes the game.
Branch `claude/controller-tests-3`. Session session_0197zJtQyLkNz6dxc3NgoNgy. Read CTT's and CTT2's notes first
(`plans/handover-controller-tests.md`, `plans/handover-ctt2.md` on claude/controller-tests): how the check works.
**People:** lead 31 session_0118SXBCdg87nDiXdtrGNVSR (report to it). AC3 (arrows) session_01DiLRzrXgkeoAZCoX1mVJn9.
BM14 (build master) session_016mhGtsCxEgPCFn9C767yjq. CP1 (controller builder) session_015ZhJRKCEditHrVhwdhszYq: has
stopped. CTT2 session_011yMob9ZzgmCFENoNhjJ44z: handed over.

## What was done (2026-10-22/23)
1. **The five places CTT2's 0.90.8 sweep never highlighted** (scratchpad walk5.py, straight D-pad walks on 0.91.0
   e27b8bfe): Roster tile (Y + 10 presses), Tracked "Dawn swim" (View + 8 down), "The job board" (View + 11 down),
   Calendar's 2nd "Don't" (Y, down, A, down, down): all REACHED. The appointment map's Deck plan (role=img) can't take
   the highlight by design; all 12 buttons beside it reached: covered (PAD_COVERED, PR9's ruling). Sent to CP1 and leads.
2. **A game finding, fixed by CP1** (claude/controller-follow1 3f17ac95): by the Deck 4 lift door the ring said "Lift"
   but A climbed the Spine ladder: padWhat didn't ask ladderAimed(h) as tap() does. On 0.64.16 too. Planted fault in
   MUTANTS['day'].
3. **touch, pick, day on CP1's 3f17ac95: all OK**, planted faults caught (commit 2a76b818 went to BM14/claude/controller).
   pick's crowded seat now tries all four views at each breakfast time before "not proven"; CP1's mess-seat case
   (part_mess_seat, 3-mess-1) with its planted fault.
4. **Round 10 (IM1's claude/trial-p5-on-controller, arrows on): the 8 FAILs were all the check's** (the arrows' pop-up
   queue, 2.5 s REAL time, held messages the check had put away by hand). Fixed: marks/drop/pick set TOAST_AT = -1e9 and
   empty GUIDE.tq where they put the message away; hint_now presses B for each queued message (up to 4). marks, drop,
   pick OK on round 10; day: see the bottom.
5. **The reach sweep** (needed before the controller is switched on):
   - CTL_DEPTH (default 6) beside CTL_PRESSES (700). The full run used CTL_DEPTH=8 CTL_PRESSES=2000.
   - Touch half on 3f17ac95 (~1.5 h): 42 screens, 189 pressable things, 758 presses. Depth 8 reached only in the
     appointment-making chain (deck buttons N/R, then a room): the same 14 things each step.
   - Pad half fixes (all check-side): the second chance finds a missed thing by its key (KEY_MARK, works off screen) and
     re-finds it before every press (pad_to_key: the device home redraws as the clock ticks and dropped the mark one press
     short of Roster); from the top again if steering bounces; a screen's things read as it arrives, plus those in the
     panel below its edge (read after the zigzag, a list it scrolled dropped rows from both count and misses: an old
     hole); the zigzag stops once everything has had the highlight (was ~600 presses a screen).
   - CTL_STATES=file saves/reads back the touch half; CTL_PADDONE=file keeps each screen's pad result and skips done
     screens on a rerun (the container restarted twice mid-run).

## Running the sweep (it survives a restart)
Scratchpad (this session's): `run_reach.sh GAME LOG STATES PADDONE` (CADET_WORK=w_reach, CTL_DEPTH=8, CTL_PRESSES=2000),
started detached: `setsid nohup run_reach.sh ... &`. With STATES and PADDONE files present, a rerun goes straight to the
pad half and skips finished screens. In a fresh session: write the same with the check from this branch; the touch half
must be redone (the files are in the old scratchpad).
**Gotcha:** `pkill -f 'w_reach/controller_check.py'` matches your own shell command and kills it (exit 144): write the
pattern as `'[w]_reach/controller_check.py'`. Two browser checks at once at most; idle/touch/calls alone.

## State at this writing
- Sweep on 3f17ac95 (pad half): __SWEEP__
- day on round 10: __DAY__

## Open
- The full list of anything unreachable to lead 31 when the sweep ends (Deck plan counted as covered).
- Tracked's rows and the device's Works tile change with the clock: the pad half names what the touch half listed but
  isn't there this time (not a miss).
- The sweep's "could not get back from Tracked" (replays) is old, harmless.
