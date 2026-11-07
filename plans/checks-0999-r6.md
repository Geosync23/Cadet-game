# 0.99.9 round 0999: R6's share (interactions_check whole)

- Candidate: claude/staging-0999 8d8073a9, build 0.99.9, GO from BM27 (for lead 51).
- Game sha256: 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matches the GO).
- Check file: interactions_check.py as at 8d8073a9.
- OLD: 0.99.8 main 33c737b (13681748...59fd3, checked); not needed, nothing failed.
- Setup: CADET_WORK=/tmp/work-r6, CADET_CHROME=/opt/pw-browsers/chromium, three r128 and acorn via npm pack; run alone.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole), first run | OK line, 05:08-05:38 UTC (exit code not captured, see below) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak while doing things 220 (as before) |
| interactions_check (whole), rerun for BM27 (the result) | **OK, exit 0**, 05:39-06:10 UTC (about 31 min) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak 220 |

Notes on the first run:
- The container restarted at about 05:05 UTC and killed the first run (started 04:43) before it gave a result. Set up again
  (three r128 and acorn re-installed; both game files' sha256 re-checked) and restarted from scratch at 05:08.
- The wrapper shell of the second run was stopped by mistake at about 05:10 (a guard meant to cancel the queued perf_check
  matched its command line), so the exit code wasn't captured; the check itself (its own process) ran to the end and its log is
  complete (324 lines, as earlier full runs) and ends `INTERACTIONS CHECK OK`, with no FAIL line anywhere.
- Orange tree off the pin: ixGarden; booths row as in rounds 0998/0998b.

perf_check: not run here. Agreed between R2, R6 and R4 on lead 51's ask after the restart: the new R4
(session_01GKuymmzABL4xHF9xBhM9fE) runs it once, with EV1's blink scene; R6's queued copy was cancelled before it started.

R6: OK.
