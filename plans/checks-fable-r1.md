# Round "fable" (0.99.92-review, candidate 1): runner R1

- Candidate: `claude/staging-fable-review` c4999dae, game sha256
  `d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0` (matched the GO), label 0.99.92-review.
  Check files at c4999dae.
- OLD: 0.99.91, main cdd9efd (not needed: nothing failed).
- Hired by lead 52, build master BM29. Each check run once, on the candidate. Two browsers at most (/tmp/work-r1,
  /tmp/work-r1-b); player_check alone at the end, after both lanes.
- frp_check: not run by R1 (BM29 runs it, per the GO).
- "skipped" lines (`grep -c skipped`): 0 in every log.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (35s; off copy, P5_RETRY_ON false, 1 line changed); no page errors |
| bubble | OK | BUBBLE CHECK OK (746s) |
| puzzle (whole) | OK | PUZZLE CHECK OK (171s) |
| social | OK | SOCIAL CHECK OK (38s) |
| talk | OK | TALK CHECK OK (52s) |
| arrows_pointer | OK | arrows_pointer_check: OK (257s) |
| day_4 | OK | DAY CHECK OK (484s) |
| day_11 | OK | DAY CHECK OK (471s) |
| day_25 | OK | DAY CHECK OK (451s) |
| day_26 | OK | DAY CHECK OK (484s) |
| day_2 | OK | DAY CHECK OK (385s) |
| day_9 | OK | DAY CHECK OK (259s) |
| arrows_check default parts | OK | ARROWS CHECK OK (1799s); week Day 3 learned ['m1', 'm3d', 'm4'], stuck 0 through Day 8 |
| arrows step5 | OK | ARROWS CHECK OK (308s) |
| arrows step6 asis teachoff track skiptea (one run) | OK | ARROWS CHECK OK (530s); asis 697/0/0, teachoff 697/0/0, track 697/0/0, skiptea 692/0/0 (due/missed/stuck) |
| arrows endstay | OK | ARROWS CHECK OK (842s) |
| player_check | OK | PLAYER CHECK OK (415s, alone) |

Every check: exit 0 and its OK line; no FAIL line in any log.

Notes (not FAILs):
- arrows_check promo part prints "(not the promotion) stuck from Day 12 18:20 at "A toilet"": the same note as on
  0.99.91 and before (see plans/checks-09991-r1.md).
- step6 skiptea: minutes due 692 and Calder's question at Day 26 19:35 (the 0.99.91 round recorded 703 due). Missed 0,
  stuck 0, the check passes; noted only so BM29 can compare if wanted.

**R1: OK on candidate 1, c4999dae (game d6b9ce81...a1c0).** All 17 checks of the share pass (frp_check is BM29's).
