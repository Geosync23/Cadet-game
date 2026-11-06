# 0.99.8 round 0998b (candidate 2, P fixed): R6's share (interactions_check whole)

- Candidate: claude/staging-0998 bbb7bb0, build 0.99.8, GO from BM27 (for lead 50).
- Game sha256: 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3 (matches the GO).
- Check file: interactions_check.py as at bbb7bb0.
- OLD: 0.99.6 d7ad4c58 (f6ff5ec1...db8a8); not needed, nothing failed.
- Setup as in plans/checks-0997-r6.md; run alone, one browser.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | OK, exit 0, 21:29-22:06 UTC (about 37 min) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak while doing things 220 (as before) |

Booths row: "in the room {'trk': 'place:calls', 'place': '3-callhome-1', 'room': 'B'} | booth taken, moved
['3-callhome-1', '3-callhome-2'] | the call begun {'act': 'call', 'trk': None}", the same as rounds 0997b and 0998.

R6: OK.
