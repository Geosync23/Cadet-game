# Checks R3: 0.98.0 full round (R3's row, as in plans/round-0970.md; BM20's GO)

- Build: claude/staging-pad at 7a2ae7d2d5913acb4c05e5a746ca80bb560ccf26, `starship-cadet.html` sha256
  22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f (matches BM20's).
- OLD: 0.97.0, 610ad7f1, game sha256 0bd1b5b6...b36f (matches).
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium,
  CADET_WORK /tmp/work-r3 and /tmp/work-r3b, two browsers at most, the controller groups one at a time.
  controller_check.py is the same file in OLD and NEW, so every OLD and narrowing run used the same check.

## Result: FAIL, two NEW FAILs (both narrowed down to one merge)

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1875 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (957 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (396 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (42 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (166 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (74 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (285 s) | ENDING CHECK OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (632 s) | all 6 OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | **FAIL**, exit 1 (3374 s) | 12 OK; **s5cases FAIL** (NEW 1) |
| controller G2: shut off ... saves words (26 parts) | OK, exit 0 (2522 s) | all 26 OK (a rerun: the first run was stopped at part screens by my runner's 2-hour limit, with no FAIL lines) |
| controller G1, first part: idle save calls touch | OK, exit 0 (807 s; run again alone, after the first G1 run stopped) | all 4 OK |
| controller G1, the rest: walk pick lift door day games unplug odd | **FAIL**, exit 1 (1353 s) | 7 OK; **day FAIL** (NEW 2) |

The first G1 run stopped in part walk on a Playwright timeout (clicking #rot, 30 s) while devmode_check ran beside it:
load, as in 0.97.0 and BM19's notes. walk passed when run with no other controller check beside it.

### NEW 1: controller s5cases (from OP1's walk-time fix, 2b79af3d)

    FAIL s5cases: the D-pad never reached a suspect in Fault notes (focus 'Close'; device [True, 'works', 'faults', True])
    FAIL s5cases: the D-pad never reached Call it

The board by pad works ('Old mysteries', 'Take this one' taken). Then P4's first case is opened in the Works app's Fault
notes tab, and the D-pad never reaches a suspect button (Seal / Compressor / Bearing / Temperature sensor); focus stays
on Close. s5cases alone on each game:

| Game | Result |
|---|---|
| OLD 610ad7f1 (0.97.0) | OK (58 s) |
| 0b9541c9 (+ the sound tick) | OK (62 s) |
| 2b79af3d (+ OP1's walk-time fix FX24-2 + FX12-1) | FAIL, the same two lines (91 s) |
| c7953218 (+ RB1's render turn 3) | FAIL (101 s) |
| 7a2ae7d2 NEW | FAIL (in G3, and alone, 95 s) |

### NEW 2: controller day, bedtime (from RB1's render turn 3, c7953218)

    FAIL day: bedtime: the ring never offered your own bunk (item:1)
    FAIL day: bedtime: Set alarm by pad (None, no alarm card)

At Day 1 22:35; the breakfast, talk and job board steps before it pass. day alone on each game:

| Game | Result |
|---|---|
| OLD 610ad7f1 | OK (448 s) |
| 0b9541c9 | OK (442 s) |
| 2b79af3d (OP1's fix) | OK (434 s) |
| c7953218 (+ RB1's one draw per full body) | FAIL, the same two lines (475 s) |
| 7a2ae7d2 NEW | FAIL (in G1's rest, and alone, 476 s) |

Not fixed here (neither is R3's to fix): reported to BM20 and lead 45 as each was found.

## Follow-ups (BM20's and lead 45's asks), each alone on the machine

| Build | Part | Result |
|---|---|---|
| hedge (d): claude/staging-098d 37b858b4, game sha256 81c07a05...59b1 (matches; 0.97.0 + the sound tick + OP1's walk fix + check fixes, no RB1 turn 3) | controller day | OK, exit 0 (480 s) |
| the same | controller walk | OK, exit 0 (188 s) |
| the same, its fixed controller_check | controller s5cases | OK, exit 0 (34 s) |
| claude/staging-pad 10865180 (game = 7a2ae7d2's, sha256 22f8939d...918f), its fixed controller_check (check-only fix) | controller s5cases | OK, exit 0 (35 s) |

So NEW 1 (s5cases) was the check's, now fixed. NEW 2 (day bedtime) remains with RB1's render turn 3 (RB1 has the repro);
the hedge build without that turn passes day, walk and s5cases.
