# 0.99.91 round 09991b (candidate 2): runner R1

- NEW: `claude/staging-09991` 844f3c23, game sha256 `b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3`
  (matched BM28's GO), build 0.99.91 = candidate 1 + TB7's drill fix, EV2's sim fix, TP2's rewire fix; check files at 844f3c23.
- OLD: 0.99.9, main bfbcbdf, game 583d99ba...bd16 (matched; not needed: nothing failed).
- GO ~03:52 UTC 2026-11-11 (BM28 for lead 51); started 03:53. Two browsers (/tmp/work-r1, /tmp/work-r1-b, test copies
  cleared first); player_check alone at the end, after both lanes.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (24s; off copy, P5_RETRY_ON false, 1 line) |
| bubble | OK | BUBBLE CHECK OK (435s) |
| puzzle | OK | PUZZLE CHECK OK (118s) |
| social | OK | SOCIAL CHECK OK (28s) |
| talk | OK | TALK CHECK OK (41s) |
| arrows_pointer | OK | arrows_pointer_check: OK (144s) |
| day_4 | OK | DAY CHECK OK (279s) |
| day_11 | OK | DAY CHECK OK (282s) |
| arrows_default | OK | ARROWS CHECK OK (1371s); week Day 3 learned ['m1', 'm3d', 'm4'] (candidate 1's FAIL fixed) |
| arrows_step5 | OK | ARROWS CHECK OK (250s) |
| day_25 | OK | DAY CHECK OK (280s) |
| day_26 | OK | DAY CHECK OK (280s) |
| arrows_step6 | OK | ARROWS CHECK OK (426s); asis 697/0/0, teachoff 697/0/0, track 697/0/0, skiptea 703/0/0 (due/missed/stuck) |
| day_2 | OK | DAY CHECK OK (276s) |
| day_9 | OK | DAY CHECK OK (282s) |
| arrows_endstay | OK | ARROWS CHECK OK (604s) |
| player | OK | PLAYER CHECK OK (280s, alone) |

No FAIL lines in any log. The promo part's "(not the promotion) stuck from Day 12 18:20 at "A toilet"" note is the same
as on OLD (see plans/checks-09991-r1.md), not a FAIL.

**R1: OK on 0.99.91 candidate 2, 844f3c23 (game b321a4ec...95f3).** All 17 checks pass.
