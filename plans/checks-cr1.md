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

# 0.92.5 (claude/staging-0.92.5 53c11f88, 2026-10-25)

**sha256 of starship-cadet.html: `fddc0ef61c68ac012409a0f88e4ded2a62098b28377760461d99fb144b595559`** (matches BM17's).
OLD = 0.92.4 ba836359 (2aa6427f…13a2). One at a time (arrows_check alone), CADET_WORK=/tmp/work-cr1. The arrow checks
added at BM17's ask (FX15 and DV1 changed the arrows).

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 313 s | PLAYER CHECK OK |
| devmode_check | **OK** | 239 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 219 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 57 s | PUZZLE CHECK OK |
| social_check | **OK** | 22 s | SOCIAL CHECK OK |
| talk_check | **OK** | 31 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 1105 s | ARROWS CHECK OK; now also a promo part (Day 9 junior test passed); shift Day 9, 22 jobs, stuck 0 |
| arrows_pointer_check | **OK** | 108 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 31 s | DEV ARROW CHECK OK |
| arrows_check week guide, NEW | **OK** | 573 s | the scanner first used Day 5; m6 learned Day 8 (Day 9 on 0.92.4) |

No FAILs, so no OLD runs were needed.

# 0.92.6 (claude/staging-0.92.6 b78e1e22, 2026-10-25)

**sha256 of starship-cadet.html: `88f4cc8db099337d1ae61cf05e58be93af6577abea5458ba1449a27733f16fe4`** (matches BM17's;
all six switches on: traditions, appointments, promotion in sight, board trades, crew stories, odd jobs). OLD = 0.92.5
39f7741d (fddc0ef6…5559). The first candidate defc327f was stopped before any check finished (nothing kept).
One at a time (arrows_check alone), CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 347 s | PLAYER CHECK OK |
| devmode_check | **OK** | 255 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 315 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 75 s | PUZZLE CHECK OK |
| social_check | **OK** | 29 s | SOCIAL CHECK OK |
| talk_check | **OK** | 35 s | TALK CHECK OK |
| arrows_check (default) | **OK** | 1136 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 129 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 34 s | DEV ARROW CHECK OK |
| arrows_check week guide, NEW | **OK** | 534 s | m6 learned Day 8 |

No FAILs, so no OLD runs were needed.

# Lead 37's job: player_check on 0.92.6 as published (claude/integration 5898c190, 2026-10-25)

Game sha256 `10f654de56f76598c0747530fe5d05185fcc6eb5e91398584d462aafc8ebf266` (confirmed). Each run alone.

| Check version | Game | Result |
|---|---|---|
| 5898c190's player_check | 5898c190 | **FAIL**, 3 lines (SD1's) |
| 5898c190's player_check | b78e1e22 (88f4cc8d…) | OK |
| b78e1e22's player_check | 5898c190 | **FAIL**, the same 3 lines |
| b78e1e22's player_check | b78e1e22 | OK (round of 0.92.6 above) |

The 3 lines: `reserved job: the bracket made, in your hands, with the progress bar (['relay'], None)`;
`reserved job: the fetch and make stops marked done ([[0], ['fetch', 'make', 'job']])`;
`reserved job: done after fitting both parts and the repair (['claimed', True])`.

So it follows the game, not the check. The only game change between b78e1e22 and 5898c190 is **27ad3cba** (FX17,
section 18, 4 lines): `evMeetClash` and its use in `evArrive` (nobody goes to Winner stays on or a new tradition over a
ship-wide event meeting they're needed at). NEW in the published 0.92.6. Not fixed (check runner).

# 0.93.0 (claude/staging-0.93.0 4f1e52bf, 2026-10-25)

**sha256 of starship-cadet.html: `97f21893d17bce087b2ab4b3a3cd769a2f696da88da263a3f5d4f2ae8c38f6a8`** (matches BM18's).
OLD = 0.92.6 5898c190 (10f654de…f266). One at a time (arrows_check alone), CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 378 s | PLAYER CHECK OK (the 3 reserved-job lines from 0.92.6 pass: FX17's fix works) |
| devmode_check | **OK** | 258 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 289 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 66 s | PUZZLE CHECK OK |
| social_check | **OK** | 27 s | SOCIAL CHECK OK |
| talk_check | **OK** | 34 s | TALK CHECK OK |
| arrows_check (default) | **FAIL (NEW)** | 1120 s | promo: `the arrow queue never led with promo:test (fix: DV1, the promotion's beats on the queue); seen ['promo:ceremony', 'promo:move', 'promo:summons']` |
| arrows_pointer_check | **OK** | 122 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 33 s | DEV ARROW CHECK OK |

## arrows_check promo: NEW in 0.92.6 as published, still in 0.93.0

`arrows_check.py GAME promo` with 4f1e52bf's check (unchanged since 0.92.6), each alone:

| Game | Result | Queue seen |
|---|---|---|
| 0.93.0 4f1e52bf (twice) | FAIL | ceremony, move, summons (no test) |
| 0.92.6 published 5898c190 | FAIL | the same |
| 0.92.6 before the round fixes b78e1e22 | OK | ceremony, move, summons, **promo:test:9** |

The promotion itself still works (test passed Day 9, officer Day 10, ceremony attended); only the arrow to the test is
missing. The only game change b78e1e22 → 5898c190 is 27ad3cba (FX17's evMeetClash in evArrive), the same change behind
0.92.6's reserved-job FAILs; FX17's 0.93.0 fix cured the reserved job but not this. Not fixed (check runner).

# 0.93.1 (claude/staging-0.93.1 0a2fc617, 2026-10-26)

**sha256 of starship-cadet.html: `6cd54ab97f4290aa5665ff40b5db35d0abc485dc8401d011084dfaa2f35a8eee`** (matches BM18's).
OLD = 0.93.0 df8d58b9 (97f21893…f6a8). One at a time (arrows_check alone), CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 370 s | PLAYER CHECK OK |
| devmode_check | **OK** | 250 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 289 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 65 s | PUZZLE CHECK OK |
| social_check | **OK** | 26 s | SOCIAL CHECK OK |
| talk_check | **OK** | 34 s | TALK CHECK OK |
| arrows_check (all parts) | **OK** | 1166 s | ARROWS CHECK OK; promo queue now includes `promo:test:9` (0.93.0's FAIL fixed) |
| arrows_pointer_check | **OK** | 120 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 33 s | DEV ARROW CHECK OK |

No FAILs, so no OLD runs were needed.

## 0.93.1 extra: CR5's events_check and sound_check (agreed with CR5, BM18's ask)

On 0a2fc617 (sha256 6cd54ab9…5a8eee), default args, one after the other, alone: **events_check OK** (exit 0, 589 s,
EVENTS CHECK OK); **sound_check OK** (exit 0, 167 s, SOUND CHECK OK). No FAIL lines. CR5 removed both from its run.

# 0.93.2 (claude/staging-0.93.2 41c8a7e0, 2026-10-26)

**sha256 of starship-cadet.html: `89eafdc1cc2f2cbcc77db9168b009cb19561b9efe9067aeedf6386947a704960`** (matches BM18's).
OLD = 0.93.1 b957b92d (6cd54ab9…8eee). One at a time (arrows_check alone), CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 406 s | PLAYER CHECK OK |
| devmode_check | **OK** | 291 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 433 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 74 s | PUZZLE CHECK OK |
| social_check | **OK** | 29 s | SOCIAL CHECK OK |
| talk_check | **OK** | 37 s | TALK CHECK OK |
| arrows_check (all parts) | **FAIL (NEW)** | 1233 s | week: 7 FAIL lines (below); queue, clockin, shift, promo OK |
| arrows_pointer_check | **OK** | 150 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 40 s | DEV ARROW CHECK OK |
| day_check 4 | **OK** | 286 s | DAY CHECK OK; the inspection walked live, 30 of 46 juniors by their bunks |
| day_check 11 | **OK** | 298 s | DAY CHECK OK |

## arrows_check week: NEW, from the bunk inspection (INSPECT_ON)

FAIL lines: Day 4 `never clocked in following the arrow (fix: FX1)`; Day 4 `"m5" not learned by following the arrow ...;
training m5:ask, opened ['m5', 'm3i']`; Day 5 never clocked in; Day 5 m7 and p3 not learned; Day 8 never clocked in;
`the scanner never counted as used by Day 8`. From Day 4 the follower stays on training m5:ask, clocked 0 min.

| Run (41c8a7e0's check, week part, alone) | Who | Result |
|---|---|---|
| NEW 0.93.2 (twice) | CR1 | FAIL, the same 7 lines |
| OLD 0.93.1 | CR1 | OK (m5 Day 4, clocked 556 min) |
| NEW, INSPECT_ON off | FX20b (and BM18) | OK |
| NEW, TRAD_0932_ON off / STORM_SAT_ON off | CR3 | (CR3's notes) |

Cause, found by FX20b (the inspection's builder): at 06:29 on Day 4 the arrow says "Inspection at 06:30: your berth"
and points at the bunk itself; the follower taps the bunk and lies down, the 'lie' activity never ends, so it counts
itself busy all day and misses Calder's Tuning meeting and the clock-in. FX20b's game fix (the officer's result gets you
up from the bunk) is in testing; the full round runs again on the new sha. Not fixed here (check runner).

## Round 2: 0.93.2 (claude/staging-0.93.2 d9c7e5f0)

**sha256 of starship-cadet.html: `c99ea59cc753e58b98f06f7fbc0d51eb8cac1da39849f881533adb96917dd5d3`** (matches BM18's;
the storm board fix, the inspection fixes incl. up off your bunk, the workbench tap). One at a time, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 383 s | PLAYER CHECK OK |
| devmode_check | **OK** | 260 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 403 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 72 s | PUZZLE CHECK OK |
| social_check | **OK** | 30 s | SOCIAL CHECK OK |
| talk_check | **OK** | 38 s | TALK CHECK OK |
| arrows_check (all parts) | **OK** | 1215 s | ARROWS CHECK OK; week: m5 learned Day 4 (clocked 550 min), by Day 8 m2, m5, m6, m7, p3 (round 1's FAIL fixed) |
| arrows_pointer_check | **OK** | 134 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 38 s | DEV ARROW CHECK OK |
| day_check 4 | **OK** | 246 s | DAY CHECK OK |
| day_check 11 | **OK** | 266 s | DAY CHECK OK |

No FAILs, so no OLD runs were needed.

Extra for CR2 (agreed with CR2, BM18's ask): `lines_check.py starship-cadet.html --day` on d9c7e5f0, alone: exit 0,
381 s, **lines_check --day: PASS (0 errors)**.

Extras for CR6 (agreed with CR6, BM18's ask; CR6 cancelled its own runs first), on d9c7e5f0, each alone:
- `device_check.py starship-cadet.html`: exit 0, 155 s, **device_check: OK** (CR6's timed out under load).
- `events_check.py starship-cadet.html` (CR5's, default args): exit 1, 738 s, EVENTS CHECK FAILED with **one** FAIL line,
  the known-old **FX24-2**: `reading-corner day 7, Deck 3: 2/3 reached ... FAIL not reached: ['farouk-olu>3-lounge-28 16:00']`.
  No other FAIL (the other "not reached" lines are notes, not FAILs).

# Early check: the doors change (claude/doors-3way 3051de4e, 2026-10-26; lead 39's ask, for FX24)

Game sha256 `008d3bd66fc74637ac054422b95553ad0cf3488cf5d037eb801b285299552a23` (matches FX24's). OLD = d9c7e5f0
(0.93.2 live, c99ea59c…). 3051de4e's arrows_check.py, each run alone.

| Run | Result | Key lines |
|---|---|---|
| arrows_check (all parts incl. week), NEW | **OK** (1159 s) | week: m5 Day 4, m6 by Day 8; promo test passed |
| arrows_check week guide, NEW | FAIL (twice, identical) | below |
| arrows_check week guide, OLD d9c7e5f0 | FAIL, identical | below |

The week guide FAIL lines: `week: stuck from Day 6 20:10 at "Theo wants a word" (Deck 4) (fix: FX1 (arrows and
tracking) or FX3 (the lift))`; `week: stuck from Day 7 18:20 at "A toilet" (Deck 4) (fix: section 15 (the needs arrow):
nobody yet)`; `week: the arrow "A toilet" stayed up over 3 ship hours from Day 7 18:20 (fix: FX1 (arrows that never clear))`.

So the doors change is clear. The week guide FAIL is **older, in the live 0.93.2**: week guide last ran in a round on
0.92.6 (b78e1e22, OK). It came in somewhere between 0.92.6 and 0.93.2. Not on the known list; backlog row suggested.
Not fixed or bisected (check runner).

## Doors follow-ups (claude/doors-3way, 2026-10-26)

| Commit (game sha256) | Run | Result |
|---|---|---|
| 329ad201 (13740483…2c28f78) | arrows_check week | OK (554 s) |
| 329ad201 | arrows_check week guide | FAIL, unchanged (the same 3 lines) |
| 329ad201 | arrows_check all parts | stopped unfinished when 1dc48251 came (no result) |
| **1dc48251** (`b0dd6aaa9cdeb1d29e05620a7a0433bba668c94b254d9bc6992a3f61c87399d9`) | arrows_check all parts incl. week | **OK** (1128 s; same arrows_check.py as 329ad201) |
| 1dc48251 | week guide, scratch debug copy (prints actions and position) | FAIL, unchanged; action lines sent to FX30 |

(FX29 wrote "1dc4825e"; the commit is 1dc48251.) The week guide stalls, from the debug copy: Day 6 20:10 the follower
reaches Deck 4 at 20,9 and every 3 minutes taps "Spine trunks" (false) and the floor at the pin "Theo wants a word",
never moving, not busy. Day 7 18:20 it stands at 5,1 on Deck 4 and every 3 minutes taps "Toilet" (true) and the floor
at the pin "A toilet"; nothing starts and the arrow never clears. The week guide stall is known-old (also on d9c7e5f0),
now with FX30.

# 0.93.3 (claude/staging-0.93.3 19400976, 2026-10-26)

**sha256 of starship-cadet.html: `ec93b94dfe01d8a9f392257bb1f026ea8b1ca1c0cc24bce3d154ea3d2bcad085`** (matches BM18's;
doors three ways, the diplomatic visit on). OLD = 0.93.2 d9c7e5f0 (c99ea59c…). One at a time, one browser, CADET_WORK=/tmp/work-cr1.

| Check | Result | Time | Key lines |
|---|---|---|---|
| player_check | **OK** | 338 s | PLAYER CHECK OK |
| devmode_check | **OK** | 226 s | DEVMODE CHECK OK |
| bubble_check | **OK** | 354 s | BUBBLE CHECK OK |
| puzzle_check | **OK** | 58 s | PUZZLE CHECK OK |
| social_check | **OK** | 24 s | SOCIAL CHECK OK |
| talk_check | **OK** | 30 s | TALK CHECK OK |
| arrows_check (all parts) | **OK** | 1060 s | ARROWS CHECK OK |
| arrows_pointer_check | **OK** | 117 s | arrows_pointer_check: OK |
| dev_arrow_check | **OK** | 29 s | DEV ARROW CHECK OK |
| day_check 4 | **OK** | 219 s | DAY CHECK OK |
| day_check 11 | **OK** | 232 s | DAY CHECK OK |

No FAILs, so no OLD runs were needed.
