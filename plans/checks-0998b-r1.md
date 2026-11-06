# 0.99.8 round 0998b (candidate 2, P fixed): runner R1

- NEW: `claude/staging-0998` bbb7bb0, game sha256 `13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3`
  (matched BM27's GO), build 0.99.8, check files at bbb7bb0.
- OLD: 0.99.6 d7ad4c58, game f6ff5ec1...db8a8 (not needed: nothing failed).
- GO ~21:28 UTC 2026-11-06 (BM27 for lead 50). Two browsers at most, each its own CADET_WORK (/tmp/work-r1,
  /tmp/work-r1-b, test copies cleared first); player_check alone at the end. This container ran about 1.5x
  slower than earlier rounds (times below).
- Also ran five of R5's checks for BM27 (its container restarted; lead 50 asked; BM27 took them out of its own
  script, so each ran once): the R5_ rows. p5retry_break's OFF copy: FIXTAP_ON and P5_RETRY_ON set false (2 lines).

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (34s) |
| bubble | OK | BUBBLE CHECK OK (673s) |
| puzzle | OK | PUZZLE CHECK OK (158s) |
| social | OK | SOCIAL CHECK OK (35s) |
| talk | OK | TALK CHECK OK (48s) |
| arrows_pointer | OK | arrows_pointer_check: OK (215s) |
| day_4 | OK | DAY CHECK OK (415s) |
| arrows_default | OK | ARROWS CHECK OK (1653s) |
| arrows_step5 | OK | ARROWS CHECK OK (324s) |
| day_11 | OK | DAY CHECK OK (447s) |
| day_25 | OK | DAY CHECK OK (449s) |
| arrows_step6 | OK | ARROWS CHECK OK (535s) |
| day_26 | OK | DAY CHECK OK (437s) |
| arrows_endstay | OK | ARROWS CHECK OK (816s) |
| day_2 | OK | DAY CHECK OK (423s) |
| R5_food_1_7 | OK | FOOD CHECK OK (98s) |
| R5_food_11_4 | OK | FOOD CHECK OK (108s) |
| day_9 | OK | DAY CHECK OK (399s) |
| R5_p5retry_break | OK | RV31 P5 BREAK OK (106s) |
| R5_day_13 | OK | DAY CHECK OK (355s) |
| R5_day_3 | OK | DAY CHECK OK (224s) |
| player | OK | PLAYER CHECK OK (365s) |

step6 four ways in one run: asis 720/0/0, teachoff 720/0/0, track 709/0/0, skiptea 704/0/0 (minutes due/missed/
stuck; candidate 1 had asis and teachoff at 709: more minutes with an arrow due, none missed, which fits P's change to
what points you after a call home). p5retry_probe ran on an off copy (P5_RETRY_ON false, 1 line). No FAIL lines in any log.

**R1: OK on 0.99.8 candidate 2 (game 13681748...59fd3).** Every check in the share passes, and the five R5 checks
run for BM27 pass; no OLD runs needed.

## Two more R5 checks for BM27 (its container restarted again; asked ~22:45 UTC, run only here)

| Check | Result | Key lines |
|---|---|---|
| R5_day_12 (day_check 12) | OK | DAY CHECK OK (416s) |
| R5_day_17 (day_check 17) | OK | DAY CHECK OK (426s) |

Same candidate bbb7bb0 and check files; side by side, each its own CADET_WORK.
