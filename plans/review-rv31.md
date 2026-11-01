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
