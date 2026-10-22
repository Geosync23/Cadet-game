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

# Round 2: 0.64.14 (claude/integration 8e239328, 2026-10-22)

Checked out as is (no merging). **sha256 of starship-cadet.html: `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`**
(matches the lead's). `SHORT_FRIDAY = true` (line 9128), `EVENTS_ON = true` (line 36673). Each check run alone, one CADET_WORK.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 1173 s | PLAYER CHECK OK |
| intro_check --week | **OK** | 231 s | all beats heard; d5-mug (Day 5 13:01, plan [5, intro, 5-tea-1]): heard 3/3 |
| intro_check --firsts | **OK** | 26 s | OK |
| intro_check --evening | **OK** | 249 s | OK |
| interactions_check | **OK** | 398 s | INTERACTIONS CHECK OK |
| clothes_check | **OK** | 80 s | ALL OK |
| bubble_check | **OK** | 251 s | BUBBLE CHECK OK |
| devmode_check | **OK** | 230 s | DEVMODE CHECK OK |
| events_check | **OK** | 237 s | EVENTS CHECK OK |
| fridays_check | **OK** | ~25 min | FRIDAYS CHECK OK |
| day_check 0 | **OK** | 258 s | Deck 4 up to 53 crew, worst stuck 1.8 min, draw peak 250; Decks 5-7 peaks 209/149/211; DAY CHECK OK |
| day_check 5 | **OK** (run by CR3) | | draw peak 267, worst stuck 0.8 min (plans/checks-cr3.md) |
| day_check 7 | **OK** (run by CR3) | | draw peak 260, worst stuck 3.7 min (plans/checks-cr3.md) |

No FAILs, so no comparison runs on 0.64.13 (a7477a9) were needed. day_check 0 started late because of a bug
in CR1's own wait script (it waited on itself), not the game.
