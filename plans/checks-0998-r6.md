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
