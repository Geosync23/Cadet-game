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

## Taken from R2 (handed over by R2, 16:25 UTC): perf_check BUILD OLD

`python3 perf_check.py c052cc8 d7ad4c58`, strictly alone on R6's machine, 16:26-17:31 UTC: **PERF CHECK OK** (2 skipped:
P5_STEP6 not in either build; 0 waiting), exit 0. No frame-time spike flagged, so no re-measure was needed.
- Draw calls: every scene within 1 of OLD (largest change -1 call, e.g. Sunday dinner portrait 172 -> 171); none over budget.
  Highest: storm all-clear party portrait-wide 311c (OLD 312).
- New scene: film night, auditorium Sat 20:40 (AV1's REC_FILM, skipped on OLD): portrait 100c/159gl, portrait-wide 135c,
  landscape 103c; 17 crew.
- Crew counts the same except Sowing/harvest morning 10:00, 33 -> 29 people (the 0.99.7 calendar).
- Memory: a week of play 470/41/93 -> 472/41/93 and deck round trips 470/41/93 flat, the same as OLD.
- File 8.58 -> 8.84 MB; load 7.3-7.8 s (OLD 7.1-7.8 s).
