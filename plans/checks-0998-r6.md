# 0.99.8 round 0998: R6's share (interactions_check whole)

- Candidate: claude/staging-0998 d7f5bd6, build 0.99.8, GO from BM27 (for lead 50).
- Game sha256: 298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462 (matches the GO).
- Check file: interactions_check.py as at d7f5bd6.
- OLD: 0.99.6 d7ad4c58 (f6ff5ec1...db8a8, checked); not needed, nothing failed.
- Setup as in plans/checks-0997-r6.md (claude/checks-0997-r6); run alone, one browser.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | OK, exit 0, 19:24-20:02 UTC (about 38 min) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak while doing things 220 (as 0.99.6 and 0.99.7) |

Booths row (TP998 touches the booths): "in the room {'trk': 'place:calls', 'place': '3-callhome-1', 'room': 'B'} | booth taken,
moved ['3-callhome-1', '3-callhome-2'] | the call begun {'act': 'call', 'trk': None}", as in 0.99.7. Orange tree off the pin:
ixGarden, as in 0997b.

R6: OK.

## Taken from R2 (handed over by R2, 20:02 UTC): perf_check BUILD OLD

`python3 perf_check.py d7f5bd6 d7ad4c58`, strictly alone, 20:03-21:10 UTC: `PERF CHECK: 1 problem(s)` (2 skipped: P5_STEP6), exit 1.
- The one problem: `PROBLEM the Line supper, the mess Sun 18:30 trifold-open-turned: js 1.74 -> 2.88 ms a frame` (game code a
  frame, one view of one scene). Re-measured that scene alone twice (`PERF_SCENES='the Line supper'`, backlog 32):
  re-run 1 `PERF CHECK OK` (trifold-open-turned OLD 2.05 ms, NEW 2.08 ms); re-run 2 `PERF CHECK OK` (OLD 2.23 ms, NEW 2.91 ms).
  Not repeated as a problem, so a one-off spike, known old (backlog 32). Note: re-run 2 was near the check's line; the view's
  numbers swing 1.7-2.9 ms on both builds from run to run.
- Draw calls: identical to 0997b (c052cc8) in every scene and view, so TP998's two switches change none. Against OLD within 1
  call (the same -1s as 0997b), none over budget. Crew counts the same as 0997b.
- Memory: week of play 470/41/93 -> 472/41/93, deck round trips 470/41/93 flat, as OLD.
- File 8.84 MB, load 7.3-7.5 s (OLD 7.8-8.1 s this run).

R6 total for round 0998: OK (interactions_check OK; perf_check OK after the backlog-32 re-measures).
