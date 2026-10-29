# 0.97.0 full round: runner R1 (AS1)

- NEW: `claude/staging-pad` b9b7e3d7, game sha256 `0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f` (matched; re-checked after a container restart).
- OLD: 0.96.0 fe11cd66, game sha256 `332925003934b49686c080515e154131a07f7fe7a3c14fbe0f6f7684933a129e` (matched; not needed, nothing failed).
- BM20's GO 23:06 UTC 2026-10-28; checks from b9b7e3d7; two browsers, each its own CADET_WORK. The container restarted at about
  23:50 UTC with 14 checks done; arrows_check (default parts) was cut off and re-run whole on its own.

| Check | Result | Key lines |
|---|---|---|
| arrows_check step6 asis / teachoff / track / skiptea | OK x4 | ARROWS CHECK OK each |
| arrows_check step5 | OK | ARROWS CHECK OK |
| arrows_check endstay | OK | ARROWS CHECK OK (1137 s) |
| arrows_check (default parts) | OK | ARROWS CHECK OK (2120 s, the re-run) |
| arrows_pointer_check | OK | arrows_pointer_check: OK |
| player_check (with the night part) | OK | PLAYER CHECK OK |
| bubble_check | OK | BUBBLE CHECK OK |
| puzzle_check | OK | PUZZLE CHECK OK |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |

**R1: OK on b9b7e3d7** (15 of 15).
