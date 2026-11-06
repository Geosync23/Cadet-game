# 0.99.8 round 0998: runner R1

- NEW: `claude/staging-0998` d7f5bd6, game sha256 `298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462`
  (matched BM27's GO), build 0.99.8 (0.99.7 + TP1 913ba6c: TP998_ARROW_ON, TP998_BOOTH_ON), check files at d7f5bd6.
- OLD: 0.99.6 d7ad4c58, game f6ff5ec1...db8a8 (not needed: nothing failed).
- GO ~19:23 UTC 2026-11-06 (BM27 for lead 50; BM27 checked in lead 50's TEAM.md). Two browsers at most, each its
  own CADET_WORK (/tmp/work-r1, /tmp/work-r1-b, test copies cleared first); player_check alone at the end.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (22s) |
| bubble | OK | BUBBLE CHECK OK (460s) |
| puzzle | OK | PUZZLE CHECK OK (121s) |
| social | OK | SOCIAL CHECK OK (29s) |
| talk | OK | TALK CHECK OK (40s) |
| arrows_pointer | OK | arrows_pointer_check: OK (154s) |
| day_4 | OK | DAY CHECK OK (288s) |
| day_11 | OK | DAY CHECK OK (284s) |
| arrows_default | OK | ARROWS CHECK OK (1467s) |
| day_25 | OK | DAY CHECK OK (292s) |
| arrows_step5 | OK | ARROWS CHECK OK (276s) |
| day_26 | OK | DAY CHECK OK (286s) |
| arrows_step6 | OK | ARROWS CHECK OK (453s) |
| day_2 | OK | DAY CHECK OK (285s) |
| day_9 | OK | DAY CHECK OK (292s) |
| arrows_endstay | OK | ARROWS CHECK OK (631s) |
| player | OK | PLAYER CHECK OK (282s) |

step6 four ways in one run: asis 709/0/0, teachoff 709/0/0, track 709/0/0, skiptea 704/0/0 (minutes due/missed/stuck).
p5retry_probe ran on an off copy (P5_RETRY_ON set false, 1 line). No FAIL lines in any log.

**R1: OK on 0.99.8 (game 29829196...c462).** Every check in the share passes; no OLD runs needed.
