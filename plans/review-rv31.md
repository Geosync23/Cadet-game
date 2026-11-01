# RV31 review notes (0.99.6)

Reviewer RV31 (session_01GKuymjTDn3pTeDxiqrxE7F), reports to lead 49. Base: claude/integration 0.99.5 = 6475bb30, game 93aed54f...5164.

## 1. FX30, P5-1 (P5_RETRY_ON, off): PASS
claude/fix-0996 6c14bc2, game sha256 69ac3948669fb99011f601fae5fc7e4357e16927b2215304ff02562d14a4c645 (matches).
- Switch off: cadet_test 0.99.5 vs 6c14bc2 ALL IDENTICAL.
- FX30's p5retry_probe.py: P5 RETRY PROBE OK.
- My probe plans/rv31-probes/p5retry_break.py (results/break.txt), switched-on copy: RV31 P5 BREAK OK.
  A. Line held low 3 ship days (216 calls): never given up, nothing booked; every p5Stage call leaves SHIP.machines,
     SHIP.jobs, the flags, the case state and R()'s seed exactly as they were; caseSolve runs once per clock hour
     (73 for 73 hours). Fixed: the next hour stages 3-pump-1's seal, slot 29.
  B. Real save mid-wait, page reloaded: same time, still waiting, pump not left at 40; after the fix it stages.
  D. A save already at 'none' stays 'none'.
- Code read: p5Pick, p5Clues, p5Flow, caseSolve, caseReachable: no R(), no caches, no writes; the dry run restores cond
  and state in a finally. P5_RETRY.h is not saved (a reload may dry-run once more in the same hour: harmless).
- puzzle_check whole: OK switched off and OK switched on (no FAIL lines). check_fast on 6c14bc2: QUICK CHECK OK in 301 s.
Notes (not blocking):
- C. The dry run is a little stricter than the real set-up: with an ordinary unclaimed fault job open on 3-pump-1 whose
  cause is on no line (bearing), the real set-up replaces that job (jobReserve drops it) but the dry run still sees it, so
  lineShare reads the pump as full and caseSolve says 'answer'. Off stages at once, on waits until the crew fixes the
  bearing. Only a delay, never lost. Optional: ignore open, unclaimed, unreserved jobs on the pump in the dry run, as
  jobReserve does. (The pump's own flow also differs, 0.71 dry vs 0.6 real, both under 0.8: same outcome.)
- Saves already given up ('none') by the old behaviour stay given up; a one-time clear is the lead's call.

## 2. FX30, P5-1 follow-up (still P5_RETRY_ON, off): PASS
claude/fix-0996 042f57e (on be3a51f JB2-2, not reviewed here), game sha256 f535ed24a5fa8942e342952ced80ed1dbb827993d3eb234b2397b869632aca6e (matches).
Changes: p5Ready calls machinesNow first and leaves the pump's open, unclaimed, unreserved jobs out of the dry run (SHIP.jobs
swapped, put back in the finally): my note C. p5Unstick (lead 49's ask): a save at 'none' with p5 not learned and no open
p5 case goes back to waiting once (case.p5.reset = 1). flagSet(key, null) deletes the flag, so p5Stage's "!== undefined" gate opens.
- Off: cadet_test 0.99.5 vs 042f57e ALL IDENTICAL (covers JB2-2's switch off too).
- FX30's p5retry_probe: OK (new cases: bearing job, stuck save resets once, learned stays).
- My probe, updated (results/break-042f57e.txt): OK. A now runs the hour's machinesNow catch-up before each snapshot (the dry
  run's own machinesNow is the same catch-up any later call would do); then each call leaves everything as it was. C: on now
  matches off (stages, the bearing job dropped). D: an old 'none' save waits again once, 'none' after the reset stays.
- puzzle_check whole OK off and on. check_fast on 042f57e OK (265 s).

## 3. FX30, JB2-2 (FIXTAP_ON, off): safe while off; FAIL for switching on
claude/fix-0996 be3a51f (game a11a6788...69cd); reviewed as part of the tip 042f57e (game f535ed24...ace6e).
- Off: fixThingTap returns at once; cadet_test 0.99.5 vs 042f57e ALL IDENTICAL; check_fast OK on 042f57e. FX30's fixtap_probe OK.
- On: too wide. fixThingTap takes any tappable thing in the stop's room within IX_NEAR (2.4) of the stop's spot whenever
  ixKind(stopPlace, it) is non-null, and for most stop types that is true of any thing (a gym stop: always 'gym'). It runs
  first in PLAYER_TAPS, ahead of ixTap's own exclusions (IX_SKIP, lifts, ixTheirs, ixMachine) and the other taps.
  plans/rv31-probes/fixtap_reach.py: 75 small repair / odd job stops reached, every thing near each one taken (results/fixtap_reach-042f57e.txt).
  Real clicks (fixtap_click.py, results/fixtap_click-042f57e.txt), job yours, switch on:
  w5-tap: the Toilet does the job (off: the toilet). la-lint: Washer 3 does the job (off: starts a load). jc-kettle: the
  kettle does the job (off: tea; arguable, it's the thing being fixed). Without the job: as off.
  This also turns round the 0.28.55 rule (the lead: at a chore's stop a thing you can use does its own thing) for every
  small job, not just the gym locker.
- To change: narrow it to the case JB2-2 is about. Options: fix the locker row's stop (a place whose nearest thing is the
  lockers, or a "Lockers" thing to tap); or a short list of rows where the thing at the stop is the thing being fixed; at
  the least, apply ixTap's exclusions and never take things with a use of a different kind (toilets, washers, showers,
  basins, tea, the rotas and boards).

## 4. PF1, performance (claude/perf-0996 67acc5b; tip 08edb7a docs only): PASS
Game sha256 90dbc4f2c3f02f3dd170a4836312bbfbdaec1e789900a894baf744a0715346a7 (matches, at 67acc5b and 08edb7a).
- F1 (section 17, shipEffectsAt kept on the hour's record in a WeakMap): code read: fxFrom reads only the deck, the record
  and tables fixed at load (machineList, MACHINE_FX, MACHINE_KINDS, MACH_BRANCH, SYSTEMS); machRecord makes a new record
  each hour and nothing writes into one after; no caller of shipEffectsAt changes the answer it gets. No R(); the planner
  reads nothing new. plans/rv31-probes/pf_f1_same.py (results/pf_f1_same-67acc5b.txt): a new game skipped 10 ship days, three
  samples a day: 23,674 cached answers equal to a fresh fxFrom, 0 mismatches; and the ship's fingerprint (time, machines,
  jobs, flags, crew state, needs, R()'s seed, MACH_REV) identical to 0.99.5 at all 30 samples. Owner (systems engineer)
  still to look, per owners.md.
- The four picture switches, off by default: cadet_test 0.99.5 vs 67acc5b ALL IDENTICAL (renderer noise only).
  pf_switches.py (a fresh page at pixel ratio 2): none -> [2, 2048, antialias on], 120 renders in 120 frames at 120 Hz;
  #pfpr.pfsh.pfcap.pfaa -> [1.5, 1024, off], 60 renders; #pfcap-30 -> 30 renders; the ship clock keeps time; no page errors.
- check_fast on 08edb7a: QUICK CHECK OK in 486 s. perf_check NEW vs 0.99.5 is PF1's.
