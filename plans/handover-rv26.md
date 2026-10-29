# Handover: RV26 (second reviewer, 0.98 / 0.99)

Session session_01GKuymjwVsweGh8p9EbTGHU. Hired by lead 45; now reports to **lead 46 (session_01GKuymiks9CC1WYr2may5nM)**.
0.99 verdicts go to lead 46 and **BM21 (session_01GKuymkAoLNTFXef9RgiYLn, claude/staging-099)**; BM20
(session_01GKuymiwDEgkwGmjJ2nokvg) only finishes 0.98.0. Every verdict also goes to the builder. Branch:
`claude/review-rv26` (notes only: plans/review-rv26.md, probes in plans/rv26-probes/, this file). Push only that branch.

## State at handover (2026-10-29 ~13:50 UTC): queue empty, nothing running
All verdicts are in plans/review-rv26.md. In short, all PASS:
- 0.99: TB1 title-099 8d2a708, title-on-099 b980518; SD3 title-music-099 19798c3, title-music-c febdf8a (the user's C);
  EV2 visit-099 b21a531 -> 60287f2 -> 3dda559 (seated Veyli dinner; a.early read in section 14's apptWhere, OP1 did the
  owner read); BAL2 balance-099 96dd584 -> 6eacbe1; OP1 nights-dayarrow 79a87ea (Day 22 day-sleep arrow); RB1 turn 4
  e7bce5a (furniture colours merged; only the user-approved corner pixels differ).
- 0.98: RB1 turn 3 8d7a314 (one draw per body, 0 px); OP1 join-timeout c27ebb8; OP1 s5cases-fix 34adecc + 1086518
  (controller s5cases, puzzle_check p6; checks only); RB1 222ec28 (controller day, toast cleared; check only).
- BB1 FX8-1 swim look on backlog-triage 564b8a5: no wall glide (RV25's handover item).

## Open notes nobody has to act on (all sent)
- EV2-1 in plans/backlog.md: Dev mode's "formal dinner, from the galley" jump is out of date (no Dev work, the user).
- OP1 s5cases: the regex is built from case ids; caseSus(c, s).label would be exact (P4 'sensor' vs "Temperature sensor").
- OP1 nights-dayarrow: a Day 22 with no day shift at all but the night on would get the sleep arrow from 05:30.
- RB1 turn 4: DEV_NOTES names "17's machine looks" among exclusions; the code excludes GD.leaves, RK.film, PULSES.
- With the title on, only title_check ever shows it (all other checks run under webdriver).

## How I review (what worked)
1. Fetch the branch, `git worktree add --detach <scratch>/wt-x <commit>`, check the game sha256 the builder sent.
2. Code read of `git diff <base> <head>`: switches off -> identical; who else reads the changed shared functions.
3. **Run each build's own checks** (from its worktree), never the ones on this branch: I once ran an older day_check and
   got a false FAIL on 0.98 (caught, no wrong verdict sent). This branch was then merged up to staging-pad.
4. cadet_test vs the base (run alone for render work: noise of 1 level otherwise), then targeted checks, then a probe
   in the real game when behaviour changes (plans/rv26-probes):
   - vd_play.py: Dev jump to Day 18 18:40 (VD_AT, VD_WHERE, VD_PRE env), logs diners' chairs, the arrow, the scene.
     VD_PRE "(flagSet('promo.sight.home', 18), guideDrop('promo:home'))" clears a Dev-jump-only arrow.
   - tm_flow.py / tm_flow2.py: the title switched on (or as built), tap, hum bus gain, New game hand-over.
   - pix_rb.py OLD NEW OUT: 7 busy scenes x 2 views old vs new pixels (render work).
   - swim_up.py: RV25's, fixed to follow the drawn spot (rdx/rdz). Draws every frame: run it ALONE.
5. Verdict PASS / FIXES with exact reasons; notes that don't block are marked so.

## Gotchas
- Setup: pip install playwright numpy pillow; three r128 and acorn 8.12.1 into each CADET_WORK (/tmp/cw-w1, w2, w3);
  CADET_CHROME=/opt/pw-browsers/chromium. Two browsers at a time at most.
- names_check needs CADET_WORK set (acorn). Checks that exec cadet_test by their own file name must be run from a
  worktree, not a renamed copy.
- `a && b && cmd &` backgrounds the whole chain; `pgrep -f name` inside a wait loop matches the loop itself; never
  `pkill -f` a name that is in your own command line (it killed my shell once). Wait on a log line instead.
- Headless frames are slow: a reading 2-4 s after a hand-over can still show the old state; read again.

## Open questions for the user
None from me.
