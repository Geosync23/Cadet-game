# 0.99.7 round 0997b (candidate 2): runner R1

- NEW: `claude/staging-0997` c052cc8, game sha256 `1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9`
  (matched BM26's GO), build 0.99.7, with the check files at c052cc8 (A and H fixes in arrows_check).
- OLD: 0.99.6 d7ad4c58, game f6ff5ec1...db8a8 (not needed: nothing failed).
- GO ~15:46 UTC 2026-11-06 (BM26 for lead 50). Two browsers at most, each its own CADET_WORK (/tmp/work-r1,
  /tmp/work-r1-b, test copies cleared first); player_check alone at the end.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (21s) |
| bubble | OK | BUBBLE CHECK OK (430s) |
| puzzle | OK | PUZZLE CHECK OK (118s) |
| social | OK | SOCIAL CHECK OK (28s) |
| talk | OK | TALK CHECK OK (39s) |
| arrows_pointer | OK | arrows_pointer_check: OK (158s) |
| day_4 | OK | DAY CHECK OK (276s) |
| day_11 | OK | DAY CHECK OK (289s) |
| arrows_default | OK | ARROWS CHECK OK (1398s) |
| arrows_step5 | OK | ARROWS CHECK OK (269s) |
| day_25 | OK | DAY CHECK OK (295s) |
| day_26 | OK | DAY CHECK OK (284s) |
| arrows_step6 | OK | ARROWS CHECK OK (443s) |
| day_2 | OK | DAY CHECK OK (281s) |
| day_9 | OK | DAY CHECK OK (293s) |
| arrows_endstay | OK | ARROWS CHECK OK (642s) |
| player | OK | PLAYER CHECK OK (287s) |

step6 four ways in one run: asis 709/0/0, teachoff 709/0/0, track 709/0/0, skiptea 704/0/0 (minutes due/missed/stuck).
p5retry_probe ran on an off copy (P5_RETRY_ON set false, 1 line). No FAIL lines in any log.

**R1: OK on 0.99.7 candidate 2 (game 1b17203d...0bff9).** Every check in the share passes; no OLD runs needed.
