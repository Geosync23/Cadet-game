# 0.99.9 round 0999: runner R1

- NEW: `claude/staging-0999` 8d8073a9, game sha256 `583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16`
  (matched BM27's GO), build 0.99.9 (0.99.8 + EV1's Last Light pale blink, EV999_BLINK_ON on), check files at 8d8073a9.
- OLD: 0.99.8, main 33c737b, game 13681748...59fd3 (matched; not needed: nothing failed).
- GO ~04:42 UTC 2026-11-07 (BM27 for lead 51). Two browsers at most, each its own CADET_WORK (/tmp/work-r1,
  /tmp/work-r1-b, test copies cleared first); player_check alone at the end.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (22s) |
| bubble | OK | BUBBLE CHECK OK (458s) |
| puzzle | OK | PUZZLE CHECK OK (121s) |
| social | OK | SOCIAL CHECK OK (29s) |
| talk | OK | TALK CHECK OK (40s) |
| arrows_pointer | OK | arrows_pointer_check: OK (157s) |
| day_4 | OK | DAY CHECK OK (291s) |
| day_11 | OK | DAY CHECK OK (299s) |
| arrows_default | OK | ARROWS CHECK OK (1465s) |
| day_25 | OK | DAY CHECK OK (295s) |
| arrows_step5 | OK | ARROWS CHECK OK (268s) |
| day_26 | OK | DAY CHECK OK (287s) |
| arrows_step6 | OK | ARROWS CHECK OK (453s) |
| day_2 | OK | DAY CHECK OK (288s) |
| day_9 | OK | DAY CHECK OK (300s) |
| arrows_endstay | OK | ARROWS CHECK OK (646s) |
| player | OK | PLAYER CHECK OK (289s) |

step6 four ways in one run: asis 709/0/0, teachoff 720/0/0, track 720/0/0, skiptea 704/0/0 (minutes due/missed/stuck).
p5retry_probe ran on an off copy (P5_RETRY_ON false, 1 line). day_check 4 covers Day 4 (the blink's day). No FAIL lines in any log.

**R1: OK on 0.99.9 (game 583d99ba...bd16).** Every check in the share passes; no OLD runs needed.
