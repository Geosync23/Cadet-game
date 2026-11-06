# 0.99.8: a small patch on 0.99.7 (the user, 2026-11-06 ~12:45 PM ET)

The user asked whether a 0.99.8 was planned and, told there was none, chose "option 2, the small 0.99.8":
0.99.7 (never published; FINAL GO from BM26 at ~17:35 UTC, staging-0997 1baafc1, game 1b17203d...0bff9) plus
TP1's two finished fixes. 0.99.7 is not published on its own. Lead: lead 50 (session_01GKuymmoEriV3ugms2s3hsn).

| Piece | What | Switch | Commit |
|---|---|---|---|
| TP1-2 | Day 2 "Calling home" arrow from 18:00, pointing at Leila (or the booths room), never at Booth 1, so you meet her before your call | TP998_ARROW_ON | claude/p997-tips 913ba6c |
| TP1-3 | After today's one call home, a booth shows "You've had your call home today" and stops: no 15 minutes, no +40 social, no goodbye line (matches the note 6 tip) | TP998_BOOTH_ON | claude/p997-tips 913ba6c |

Steps: review (SC1, fresh read) -> BM26 merges onto staging-0997 1baafc1 as claude/staging-0998, switches on,
build 0.99.8 (HUD + DEV_NOTES row; design-doc: call home once a day, a second booth use gives nothing) -> gates
-> full round 0998 (same six shares as round-0997.md) -> FINAL GO -> the user's OK -> publish Playtest + Dev (v4).
Still on the backlog, not in 0.99.8: TP1-1 (shutdown 'quiet' booking vs your night shift, old).
