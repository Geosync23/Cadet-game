# 0.99.6 full round: runner R1

- NEW: `claude/staging-0996` f3dbd11 (the GO commit is 5ac6864; f3dbd11 and b97cb98 after it change notes only), game
  sha256 `f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8` (matched the GO). Build 0.99.6, P5_RETRY_ON
  and FIXTAP_ON on.
- OLD: 0.99.5 `claude/integration` 6475bb30, game sha256 `93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164`
  (matched). Not needed: nothing failed.
- BM24's GO 16:18 UTC 2026-11-01. Two browsers at most, each lane its own CADET_WORK (/tmp/work-r1, /tmp/work-r1-b);
  player_check alone at the end with nothing else open. R4 ran two of my checks on its own machine (agreed before
  either started, lead 49 copied): arrows endstay and arrows_pointer. R6 offered arrows default; declined, it had already run.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe on an off copy (sed P5_RETRY_ON false, 1 line changed) | OK | P5 RETRY PROBE OK (28 s), no page errors |
| bubble_check | OK | BUBBLE CHECK OK (561 s) |
| puzzle_check (whole) | OK | PUZZLE CHECK OK (148 s) |
| social_check | OK | SOCIAL CHECK OK (32 s) |
| talk_check | OK | TALK CHECK OK (50 s) |
| arrows_check (default parts) | OK | ARROWS CHECK OK (1844 s) |
| arrows_check step5 | OK | ARROWS CHECK OK |
| arrows_check step6 asis teachoff track skiptea | OK | ARROWS CHECK OK (750 s, one run) |
| arrows_check endstay (run by R4) | OK | ARROWS CHECK OK (823 s); settled day 35 stay; minutes due 353, missed 0, stuck 0 |
| arrows_pointer_check (run by R4) | OK | arrows_pointer_check: OK (192 s) |
| day_check 4 | OK | DAY CHECK OK (353 s) |
| day_check 11 | OK | DAY CHECK OK (375 s) |
| day_check 25 | OK | DAY CHECK OK (361 s) |
| day_check 26 | OK | DAY CHECK OK (359 s) |
| day_check 2 | OK | DAY CHECK OK (363 s) |
| day_check 9 | OK | DAY CHECK OK (348 s) |
| player_check (alone) | OK | PLAYER CHECK OK (351 s) |

No FAIL lines in any log. (step5's exit code wasn't recorded: its driver script was stopped to drop the two checks
handed to R4 while step5 kept running; its log ends ARROWS CHECK OK with no FAIL lines.)

**R1: OK on 0.99.6 (game f6ff5ec1...db8a8).** Every check in the share passes; no runs on OLD were needed.
