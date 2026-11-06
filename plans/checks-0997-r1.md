# 0.99.7 full round: runner R1

- NEW: `claude/staging-0997` 7fd8f6b (build turn 363107d; later commits docs only), game sha256
  `b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d` (matched the GO), build 0.99.7, every 0.99.7
  switch on. arrows_check.py later taken from staging-0997 3a98019 (TP1's clockin fix 6050082; game unchanged, sha256
  checked again) for the clockin rerun and endstay.
- OLD: 0.99.6 `claude/integration` = main d7ad4c58, game sha256 `f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8` (matched).
- GO from BM25 ~13:00 UTC 2026-11-06; build master BM26 from ~13:00, lead 49 then lead 50 (~13:40). Two browsers at
  most, each its own CADET_WORK (/tmp/work-r1, /tmp/work-r1-b); player_check alone at the end. arrows_check week ran
  once, inside the default parts (BM25).

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe on an off copy (P5_RETRY_ON false, 1 line) | OK | P5 RETRY PROBE OK (23 s) |
| bubble_check | OK | BUBBLE CHECK OK (448 s) |
| puzzle_check (whole) | OK | PUZZLE CHECK OK (120 s) |
| social_check | OK | SOCIAL CHECK OK (29 s) |
| talk_check | OK | TALK CHECK OK (41 s) |
| arrows_check (default parts, check from the GO) | FAIL, check-side (A) | clockin Day 1 only; queue, shift, week, promo, vessel OK (1463 s) |
| arrows_check clockin, check from 3a98019 | OK | ARROWS CHECK OK (16 s) |
| arrows_check step5 | OK | ARROWS CHECK OK, no FAIL lines |
| arrows_check step6 asis teachoff track skiptea | **FAIL, NEW (H)** | asis OK; teachoff, track, skiptea: Day 23 20:45 shutdown arrow leads, missed 84, stuck 1 (452 s) |
| arrows_check endstay | OK | ARROWS CHECK OK (754 s) |
| arrows_pointer_check | OK | arrows_pointer_check: OK (156 s) |
| day_check 4 | OK | DAY CHECK OK (273 s) |
| day_check 11 | OK | DAY CHECK OK (284 s) |
| day_check 25 | OK | DAY CHECK OK (291 s) |
| day_check 26 | OK | DAY CHECK OK (278 s) |
| day_check 2 | OK | DAY CHECK OK (287 s) |
| day_check 9 | OK | DAY CHECK OK (303 s) |
| player_check (alone) | OK | PLAYER CHECK OK (297 s) |

## A: arrows_check clockin (check-side, cleared)

    FAIL clockin: Day 1 into the Works bay: Clock in tracked, and no clock-in tip before Zeke says it ({'tip': 'board', 'clockTips': [], 'trk': None})
    FAIL clockin: Day 1 after Zeke's line: the clock-in tip on screen at once ({'tip': 'board', 'clockTips': [], 'trk': None})

Repeated alone on the candidate (the same two lines, 'walk' tip in front). On OLD: OK (Day 1 Clock in tracked, then
career.clock.1 after Zeke's line). Cause (TP1, BM26 agreed): the check entered the Works bay at Day 1 08:30, before
the Chief's briefing that 0.99.7 (TP997.nd1) puts first by design. TP1's check fix (6050082, merged as 3a98019) enters
at 09:06 when TP997.nd1 is on. With it: clockin OK on the candidate (16 s). The other default parts had passed in the
full run and the fix touches only clockin.

## H: arrows_check step6 (NEW)

On the candidate, three of the four ways, about 84 minutes each:

    FAIL step6:teachoff: Day 23 20:45: ['p5n:in:23'] due, but the arrow leads with sd:day:23:1200 ('Your shutdown, 20:00: switch it off')
    (the same for step6:track and step6:skiptea)
    step6: minutes due 709, missed 0, stuck 0 / teachoff 796, missed 84, stuck 1 / track 796, 84, 1 / skiptea 791, 84, 1

On OLD d7ad4c58, the same check file: ARROWS CHECK OK (555 s); asis 694/0/0, teachoff 715/0/0, track 703/0/0, skiptea
698/0/0. The shutdown arrow (guideAsk 'sd:day:', line 69127) exists on 0.99.6 too; on the candidate it wins over the
Day 23 night check-in (p5n:in:23) in the three non-default ways. Reported to BM26 and lead 50 at once; lead 50 picks
the fixer.

**R1: FAIL on 0.99.7 (game b14421f8...cf7d): arrows_check step6 (teachoff/track/skiptea), NEW.** Everything else in
the share passes, arrows_check default parts with TP1's clockin check fix.
