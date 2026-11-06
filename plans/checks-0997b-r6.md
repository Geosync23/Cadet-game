# 0.99.7 round 0997b (candidate 2): R6's share (interactions_check whole)

- Candidate: claude/staging-0997 c052cc8, GO from BM26 (lead 50's call).
- Game sha256: 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9 (matches the GO).
- Check file: interactions_check.py as at c052cc8 (with CL1's store change).
- OLD: 0.99.6 d7ad4c58 (f6ff5ec1...db8a8); not needed this time, nothing failed.
- Setup as in plans/checks-0997-r6.md; run alone, one browser.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole) | OK, exit 0, 15:47-16:24 UTC (about 37 min) | `INTERACTIONS CHECK OK`; no FAIL lines; draw-call peak while doing things 220 (as 0.99.6) |

Both FAILs from candidate 1 (plans/checks-0997-r6.md) are gone: "the Orange tree off the pin: ixGarden" (EV1's fix), and the
arrival week's beats part passes with CL1's updated check (briefing, Chief's office, booths; no store, by design).

R6: OK.
