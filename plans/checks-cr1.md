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

## Round 8 extra: controller_check on 0.91.0 (taken from CR3, agreed with CR3, lead 30's ask)

`python3 controller_check.py starship-cadet.html idle save calls touch walk pick day games unplug odd off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse`
on 989fd566 (sha256 da9f1d08…4aee), 1709 s. Exit 1, CONTROLLER CHECK FAILED, **only on the two known items** (BM14's
known list: touch and day, RV9/CP1). The other 25 parts OK: idle, save, calls, walk, pick, games, unplug, odd, off,
quiet, base, deck, pick1, panels, api, lists, tiles, disc, screens, marks, touch3, drop, settings, a11y, firstuse.

The known FAIL lines, for matching against RV9/CP1's:
- touch (6): after B / after UP+DOWN / after UP: `tap0.seen.seen: 54 -> 51` and `tap0.seen.seenHash: -1403106251 -> -1508090985`
- day (4): `breakfast: the lift's Deck 3 button: not there`; `talk: no crew member to walk to`;
  `the job board: could not walk to the lift by the stick`; `bedtime: could not walk to your bunk by the stick (bed [-15.5, -8.5]; you at [4, -4.5, 1.5, 'null', False, 'ladderPanel'] ...)`

# Round 9: 0.92.0 (claude/integration-next 4147f03d, then 33c8639e's checks, 2026-10-23)

**sha256 of starship-cadet.html: `c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286`** (matches BM14's;
the same game file at 4147f03d, 25a90ced and 33c8639e). OLD = 0.91.0 989fd566 (da9f1d08…4aee). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check (4147f03d's) | **FAIL** | 383 s | 13 FAIL lines (below) |
| player_check (33c8639e's, AC3's test fixes) | **FAIL, 1 line** | ~6 min | `job loop: a tier-1 service job to take` (BM14 bisecting) |
| devmode_check | **OK** | 263 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 314 s | BUBBLE CHECK OK |
| puzzle_check (4147f03d's) | **FAIL** | 66 s | `the first note with the job, Where next? to the panel: ['n0'] None`; `Where next? points at the panel: None vs 4-washer-1-svc` |
| puzzle_check (33c8639e's) | **OK** | ~1 min | PUZZLE CHECK OK |
| social_check | **OK** | 25 s | SOCIAL CHECK OK |
| talk_check | **OK** | 31 s | TALK CHECK OK |
| arrows_check (default parts) | **OK** | 588 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 133 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 36 s | DEV ARROW CHECK OK |

## The player and puzzle FAILs, compared (4147f03d's checks)

| Game | player FAIL lines | puzzle |
|---|---|---|
| NEW 0.92.0 | 13 (twice, the same) | 2 FAIL (twice) |
| NEW with `POINT_ON` and `GUIDE_ON` false (a copy) | 1: `job loop: a tier-1 service job to take` | OK |
| OLD 0.91.0 | 7, all lines for features 0.91.0 lacks (hygiene cooldown, tea armchair, table words once, main-lift service arrow, bunk and tea arrows, the save's shower cooldown); **not** the tier-1 job line | OK |

So 12 of the 13 player lines and both puzzle lines were the checks meeting the teaching arrows (pop-ups queued, the goal
taken by the arrow); AC3's test-only fixes (33c8639e) clear them. The one left, `job loop: a tier-1 service job to take`,
is new in 0.92.0 and not from the arrows (it fails with them off too, and passes on 0.91.0). NEW, not known old.

The 13 lines on 4147f03d: the bunk before 20:00 too early; the bunk at 21:00 sleep to 06:00; not enough credits toast;
crawlway; sit anywhere; the servery closed at 12:00; job loop tier-1 service job; reserved job bracket made not kept;
job loop new job announced; work steps x4 (ok(v), "ready at", tapped too soon, r.say).

## Round 9 rerun: player_check on the new 0.92.0 game (claude/integration-next 4e324417)

**sha256 of starship-cadet.html: `f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd`** (matches BM14's;
FX5's Day 0 table fix). 4e324417's player_check.py (AC3's arrows-on fix + FX6's job-loop fix), alone: **PLAYER CHECK OK**
(exit 0, 384 s, no FAIL lines). The tier-1 job line is gone.

# Round 10: 0.92.1 (claude/integration-next 51a1bb34, 2026-10-23)

**sha256 of starship-cadet.html: `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c`** (matches BM15's).
OLD = 0.92.0 685af944 (f2329b62…1ebd). One at a time, CADET_WORK=/tmp/work-cr1. Switches as BM15 named (POINT_ON, GUIDE_ON true; EV_LINE_ON = EVENTS_ON; PAD_ON false).

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 367 s | PLAYER CHECK OK |
| devmode_check | **OK** | 263 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 312 s | BUBBLE CHECK OK (41.1 px, at most 45) |
| puzzle_check | **OK** | 69 s | PUZZLE CHECK OK |
| social_check | **OK** | 24 s | SOCIAL CHECK OK |
| talk_check | **OK** | 31 s | TALK CHECK OK |
| arrows_check (default) | **FAIL (NEW)** | 638 s | queue and shift OK (join notice kept, hook); week: 3 FAIL lines (below) |
| arrows_pointer_check | **OK** | 136 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 36 s | DEV ARROW CHECK OK |

## arrows_check week: NEW, from Crossing the Line being on

The FAIL lines: `Day 5: the scanner never counted as used (fix: FX2)`; `Day 8: "m6" not learned by following the arrow
(fix: FX3 (the burst pipe) and FX2 (the scanner count)); training None, opened ['m2']`; `Day 8: Making it safe did not open`.

| Run (week part only, 51a1bb34's check) | Result |
|---|---|
| NEW 0.92.1 (twice) | FAIL, the same 3 lines |
| OLD 0.92.0 (f2329b62…) | OK |
| NEW with `EV_LINE_ON = false` (a one-line copy) | OK: Day 8 learned m6, clocked 548 min (as 0.92.0) |

So the Line being on causes it. Sent to BM15 for FX6 (BM15 bisects if needed; CR1 not bisecting).

## Round 10 rerun: arrows_check (whole) on claude/integration-next e1f1ec97 (FX6's test-only fix)

Game sha256 unchanged: `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c`. e1f1ec97's arrows_check.py, all parts, alone:
**ARROWS CHECK OK** (exit 0, 718 s, no FAIL lines). Week: the scanner first used Day 8, m2 learned Day 8, m6 (Making it
safe) learned Day 9; nobody stuck.

# Round 11: 0.92.2 (claude/integration-next ee974894, 2026-10-24)

**sha256 of starship-cadet.html: `ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4`** (matches BM15's).
OLD = 0.92.1 e03505fd (2dbb11b8…59b18c). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 286 s | PLAYER CHECK OK |
| devmode_check | **OK** | 221 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 205 s | BUBBLE CHECK OK (41.1 px, at most 45) |
| puzzle_check | **OK** | 54 s | PUZZLE CHECK OK |
| social_check | **OK** | 20 s | SOCIAL CHECK OK |
| talk_check | **OK** | 26 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 675 s | ARROWS CHECK OK; week: m2 Day 8, m6 Day 9; shift: Day 9, 22 jobs, stuck 0 |
| arrows_pointer_check | **OK** | 100 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 30 s | DEV ARROW CHECK OK |

No FAILs, so no OLD runs were needed.

# Round 12: 0.92.3 candidate 1 (claude/staging-0.92.3 0dd4e2e2, 2026-10-24)

**sha256 of starship-cadet.html: `4e6538447d13e4c5398fc74844748e1e9d41776afa7bcc83bc99d5eff87cd0a2`** (matches BM16's).
OLD = 0.92.2 364c80cb (ca2f908d…06e7e4). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 377 s | PLAYER CHECK OK |
| devmode_check | **OK** | 260 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 304 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 67 s | PUZZLE CHECK OK |
| social_check | **OK** | 26 s | SOCIAL CHECK OK |
| talk_check | **OK** | 34 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 713 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 130 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 35 s | DEV ARROW CHECK OK |
| arrows_check week guide, NEW | **OK** | 599 s | m6 learned Day 9 |
| arrows_check week guide, OLD 0.92.2 (with 0dd4e2e2's check) | **OK** (expected FAIL, backlog 15) | 612 s | m6 learned Day 9 on OLD too |

Note: BM16 expected OLD's week guide to fail at Day 9 m6 (backlog 15). With 0dd4e2e2's arrows_check.py it passes on
0.92.2's game too (m6 learned Day 9, clocked 540 min). Reported to BM16; not a NEW FAIL.

## Round 2: 0.92.3 candidate 2 (claude/staging-0.92.3 d9a387b6)

**sha256 of starship-cadet.html: `f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853`** (matches BM16's;
AC3's m3d fix 4928271f). Whole share again, one at a time. OLD's week guide reused from candidate 1 (BM16: OLD passing is
expected, backlog 15 was a test gap).

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 353 s | PLAYER CHECK OK |
| devmode_check | **OK** | 267 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 317 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 69 s | PUZZLE CHECK OK |
| social_check | **OK** | 25 s | SOCIAL CHECK OK |
| talk_check | **OK** | 35 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 714 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 135 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 34 s | DEV ARROW CHECK OK |
| arrows_check week guide, NEW | **OK** | 612 s | m6 learned Day 9 |

No FAILs.

# 0.92.4 (claude/staging-0.92.4 5bad724d, 2026-10-24)

**sha256 of starship-cadet.html: `2aa6427fde381f3ddf746900ed9e7a62f51aa27f0bb6460f73c557836fa313a2`** (matches BM16's).
OLD = 0.92.3 3866c8f3. One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 372 s | PLAYER CHECK OK |
| devmode_check | **OK** | 257 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 301 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 68 s | PUZZLE CHECK OK |
| social_check | **OK** | 28 s | SOCIAL CHECK OK |
| talk_check | **OK** | 37 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 771 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 145 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 36 s | DEV ARROW CHECK OK |
| arrows_check week guide, NEW | **OK** | 658 s | m6 learned Day 9 |

No FAILs, so no OLD runs were needed.
