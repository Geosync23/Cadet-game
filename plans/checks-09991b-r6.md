# 0.99.91 round 09991b (candidate 2): R6's share (interactions_check whole)

- Candidate: claude/staging-09991 844f3c23, build 0.99.91, GO from BM28 (for lead 51).
- Game sha256: b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (matches the GO).
- Check file: interactions_check.py as at 844f3c23. perf_check is R4's.
- OLD: 0.99.9 main bfbcbdf (583d99ba...bd16); not needed, nothing failed.
- Setup as in plans/checks-09991-r6.md; run alone.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | **OK, exit 0**, 03:54-04:29 UTC (about 35 min) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak 220 |

Candidate 1's sim-pod FAIL is gone: "pod 1 tagged out each evening before: {'7-sim-2': 48}" (EV2's fix), as on OLD.

R6: OK.

## Taken from R4 (handed over by R4 at 04:30 UTC; R4's copy never started): perf_check BUILD OLD

- First attempt 04:31 UTC lost to a container restart (~04:37); restarted from scratch, alone, 04:39-05:38 UTC:
  `PERF CHECK: 1 problem(s)` (2 skipped: P5_STEP6), exit 1. The one problem: `PROBLEM Tiles night, bow lounge Tue 20:30
  landscape: js 1.67 -> 2.71 ms a frame`. Re-measured that scene alone twice (`PERF_SCENES='Tiles night'`, backlog 32):
  re-run 1 `PERF CHECK OK`, exit 0 (landscape OLD 2.02 / NEW 2.11 ms); re-run 2 `PERF CHECK OK`, exit 0 (OLD 1.98 / NEW 2.42 ms).
  Not repeated: a one-off spike, known old (backlog 32).
- Draw calls: identical to OLD in all 27 scenes and every view; none over budget (highest 311). The Last Light blink scene
  (bow lounge Thu 14:08): portrait 217c, portrait-wide 288c, landscape 200c, the same on both builds.
- Memory: week of play 470/41/93 -> 472/41/93, deck round trips 470/41/93 flat, as OLD. File 8.87 MB (OLD 8.84 MB).

R6 total for round 09991b: OK (interactions_check OK; perf_check OK after the backlog-32 re-measures).
