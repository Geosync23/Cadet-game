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
