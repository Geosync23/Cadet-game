# 0.96.0 full round: runner R1 (AS1)

- NEW: `claude/staging-pad` 6db1cdd2, game sha256 `c62d63999e6b596d21806d1cb14fa9ab3168a50c5038dfcc1c04f3163d37a74e` (matched).
- OLD: 0.95.0, `claude/integration` b5199dc3, game sha256 `b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a` (matched).
- BM20's GO 15:24 UTC 2026-10-28; checks from 6db1cdd2; two browsers, each its own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| arrows_check step6 asis / teachoff / track / skiptea | OK x4 | ARROWS CHECK OK each |
| arrows_check step5 | OK | ARROWS CHECK OK |
| arrows_check (default parts) | OK | ARROWS CHECK OK (1758 s) |
| arrows_check endstay (moved from BM20's share, lead 44) | OK | ARROWS CHECK OK |
| arrows_pointer_check | OK | arrows_pointer_check: OK |
| dev_arrow_check | OK | DEV ARROW CHECK OK |
| player_check (with the night part) | OK | PLAYER CHECK OK |
| devmode_check | OK | DEVMODE CHECK OK |
| bubble_check | OK | BUBBLE CHECK OK |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |
| puzzle_check | **FAIL (NEW)** | "cases were posted over Days 5-26 on paper: 0"; "p9: a clash found in the last fortnight's plans and staged: None none" |

## puzzle_check: NEW (OLD passes), caused by the Diplomatic visit being on

- OLD b5199dc3: PUZZLE CHECK OK (2 cases posted; p9 finds Navarro's "Brennan's tasting table", trips Day 10 and Day 17,
  staged on 4-washer-3).
- A copy of 6db1cdd2 with only `if (EVENTS_ON) delete V.draft;` -> `if (false) delete V.draft;` (the visit back to a
  draft, EV1's f48171a8): PUZZLE CHECK OK with exactly OLD's numbers.
- So: with the visit on (Days 16-19), Day 17 is the greeting; the crew trip p9's clash used doesn't happen, so p9's
  search finds no repeating clash in its fortnight, and the paper case sample over Days 5-26 rolls none. R1's read: the
  game behaves as designed and the check's fixed expectations need updating for the visit (puzzle_check's owner, 24k's
  seat); the lead's call. Reported to BM20 and lead 44 at once.

**R1: one NEW FAIL (puzzle_check, the visit), everything else OK.**
