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

# Round 3: 0.64.15 (claude/integration-next c5c43293, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25`**
(matches the lead's). Share from `plans/testing-guide.md`'s six-way split, one check at a time, own CADET_WORK (/tmp/work-cr1).

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 324 s | PLAYER CHECK OK (same 194 output lines as on 0.64.14; faster because player_check.py itself changed in this patch) |
| devmode_check | **OK** | 227 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 234 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 56 s | PUZZLE CHECK OK |
| social_check | **OK** | 21 s | SOCIAL CHECK OK |
| talk_check | **OK** | 28 s | TALK CHECK OK |

No FAILs, so no OLD (0.64.14, 32b699a6) runs were needed.

# Round 4: 0.64.15 re-run (claude/integration-next 31c44cb9, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e`**
(matches the lead's). Share as before plus fridays_check (moved from CR6). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 337 s | PLAYER CHECK OK |
| devmode_check | **OK** | 245 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 265 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 63 s | PUZZLE CHECK OK |
| social_check | **OK** | 25 s | SOCIAL CHECK OK |
| talk_check | **OK** | 29 s | TALK CHECK OK |
| fridays_check | **OK** | 1179 s | FRIDAYS CHECK OK |

No FAILs, so no OLD (0.64.14, 32b699a6) runs were needed.

# Round 5: 0.64.16 (claude/integration-next b9f053ba, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7`**
(matches BM13's). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 320 s | PLAYER CHECK OK |
| devmode_check | **OK** | 249 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 213 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 61 s | PUZZLE CHECK OK |
| social_check | **OK** | 24 s | SOCIAL CHECK OK |
| talk_check | **OK** | 29 s | TALK CHECK OK |
| fridays_check | **OK** | 999 s | FRIDAYS CHECK OK |

No FAILs, so no OLD (0.64.15, 2b4a05db) runs were needed.

# Round 6: 0.64.17 (claude/integration-next 8193458e, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5`**
(matches BM13's). One at a time, CADET_WORK=/tmp/work-cr1. OLD = 0.64.16 (b9f053ba, 70f94273…a6c7).

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 335 s | PLAYER CHECK OK |
| devmode_check | **OK** | 247 s | DEVMODE CHECK OK |
| bubble_check | **FAIL (NEW)** | 264 s | "a bubble jumped 49.8 px more than its speaker moved" (limit 45) |
| puzzle_check | **OK** | 64 s | PUZZLE CHECK OK |
| social_check | **OK** | 23 s | SOCIAL CHECK OK |
| talk_check | **OK** | 29 s | TALK CHECK OK |
| fridays_check | **OK** | 1125 s | FRIDAYS CHECK OK |

## bubble_check: NEW, not known old

| Run | Build | Speakers | Largest move beyond the speaker | Result |
|---|---|---|---|---|
| 1 | NEW 0.64.17 | kim-yusuf, kovac-zainab | 49.8 px | FAILED |
| 2 | NEW 0.64.17 | kim-yusuf, kovac-zainab | 49.8 px | FAILED |
| 3 | NEW 0.64.17 | kim-yusuf, kovac-zainab | 49.8 px | FAILED |
| 4 | OLD 0.64.16 | kim-yusuf, saruth | 30.0 px | OK |

The same every time, so not a flake. bubble_check.py is unchanged between the two builds. The other parts pass on NEW (tail
aim 0.00 px, no shakes, no hide-and-show, no side swaps). Different speakers stand in the scene on NEW: most likely the
breakfast change (07:00) moves who is chatting there at the check's moment, and the 45 px limit is crossed with the new pair.
Whether that is a game bug (a bubble really jumping) or the check's limit meeting a new scene isn't settled here: for the
bubble owner. Not fixed (check runner).

# Round 7: 0.64.17 candidate with the bubble fix (claude/integration-next 1498dbf4, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306`**
(matches lead 29's). Share per lead 29: player, devmode, bubble, puzzle, social, talk (fridays not in it). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 374 s | PLAYER CHECK OK |
| devmode_check | **OK** | 271 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 283 s | BUBBLE CHECK OK; same speakers as round 6 (kim-yusuf, kovac-zainab); largest move beyond the speaker 41.1 px (at most 45; was 49.8 on 8193458e) |
| puzzle_check | **OK** | 68 s | PUZZLE CHECK OK |
| social_check | **OK** | 26 s | SOCIAL CHECK OK |
| talk_check | **OK** | 30 s | TALK CHECK OK |

No FAILs. Round 6's bubble FAIL is gone with CP4's fix (36f8abf7).

# Round 8: 0.91.0 (claude/integration-next 989fd566, 2026-10-22)

Checked out as is. **sha256 of starship-cadet.html: `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee`**
(matches BM14's). OLD = 0.64.16 b9f053ba. One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 314 s | PLAYER CHECK OK |
| devmode_check | **OK** | 221 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 257 s | BUBBLE CHECK OK; largest move beyond the speaker 30.0 px (at most 45) |
| puzzle_check | **OK** | 54 s | PUZZLE CHECK OK |
| social_check | **OK** | 19 s | SOCIAL CHECK OK |
| talk_check | **OK** | 24 s | TALK CHECK OK |

No FAILs, so no OLD runs were needed.
