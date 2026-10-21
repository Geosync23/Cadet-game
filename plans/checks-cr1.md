# CR1: release-candidate checks (2026-10-21)

Check runner CR1, for lead 25 and release reviewer PR9. Results only; the game was not changed.

## The build
- From `claude/integration` a4a5735 (0.64.12), merged `claude/storm-update` 0b77dfc, then `claude/fridays` 3bd9b2c
  (the lead confirmed 3bd9b2c: fridays' later 2078010 failed review and is being reverted).
- Conflicts: only `plans/backlog.md` (both sides kept, exact duplicate rows 22-23 dropped). build-table.md merged clean. Nothing else.
- `day_check.py` is storm-update's (EV4's 4fa198f rec-deck skip present, plus 829f242).
- Switches as both branches already set them, matching PR9's `plans/review-9.md`: `SHORT_FRIDAY = true`,
  `EVENTS_ON = true`, `EV_STORM_ON = EVENTS_ON`. No edits by CR1.
- **sha256 of starship-cadet.html: `23fb9118abc3679fd1eea658a072817fd6f2831a9560f1bf86358ada768cb7df`**

## Results (each run alone, CADET_CHROME=/opt/pw-browsers/chromium, one CADET_WORK)

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 1211 s | PLAYER CHECK OK |
| intro_check --week (Fridays on) | **OK** | 230 s | every beat heard in full; d5-mug (Day 5 13:01, plan [5, intro, 5-tea-1]): heard 3/3 |
| intro_check --week, Fridays-off copy (SHORT_FRIDAY flipped) | **OK** | 212 s | OK |
| intro_check --firsts | **OK** | 34 s | OK |
| intro_check --evening | **OK** | 262 s | OK |
| interactions_check | **OK** | 408 s | INTERACTIONS CHECK OK (only a Python SyntaxWarning on line 495's `'\|'` string, harmless) |
| clothes_check | **OK** | 78 s | ALL OK |
| bubble_check | **OK** | 248 s | BUBBLE CHECK OK |
| devmode_check | **OK** | 236 s | DEVMODE CHECK OK |

No FAILs, so no runs on plain a4a5735 were needed.
