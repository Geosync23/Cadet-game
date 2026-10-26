# Handover: RV17 (reviewer), 2026-10-26 ~00:30 UTC

**Role:** reviewer. Notes-only branch `claude/review-rv17`; full log `plans/review-rv17.md`. Never change the game or push to
builders' branches. Verdicts PASS / FIXES NEEDED to the builder, the lead and the build master, priority "next" (never "now").
Leads: lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi), now **lead 37** (session_019GcNZ4GGEqfiuYDYnue7nX). Build master **BM18**
(session_01A3S2VBMYmTt2wCZa8ej7XR; BM17 retired).

## Verdicts given (all in review-rv17.md)
- 0.92.6 item 9 appointments (FX22 -> FX22b): FIXES at 582a3544/eaaa6446, PASS 6b03bea7, then FX22b's bae25ae7 FIXES (R1:
  rejoin after reload for hosts at work), **PASS dd4d8797** (merged).
- FX17 Day 7 Line fix 3e8c78a6 + eba4d365 (mech m17): PASS. FX22b join_check 3d011393: PASS.
- 0.93.0 sound: FX20 activity sounds **PASS 7e63f194** (includes the user's blanket fix); FX22b music + Music app **PASS
  a4ac9e31**. Nobody measures loudness under the hum (no levels check in sound_check).
- 0.93.1: RV16 arrows_check promo 32374ef3 PASS (test); game fix 8cbcd6f0 PASS (merged as staging-0.93.1 0a2fc617);
  arrows_d_check S3 350b860b PASS (test; optional: expect "Your Tier 2 test job" outright).
Nothing open.

## How I test
- Setup (plans/testing-guide.md 2.0): pip playwright numpy pillow; three r128 + acorn 8.12.1 into /tmp/cadet-work;
  CADET_CHROME=/opt/pw-browsers/chromium. Worktrees per sha under /tmp/rv17/; one CADET_WORK per run (/tmp/rv17/w-*) with
  three/acorn symlinked. 4 cores: **at most 2-3 browsers at once**, or page loads time out (Page.goto 30 s) and look like FAILs.
- cadet_test's first shot (a_start) can flip under load (backlog FX17-2): rerun alone before calling it.
- Old vs new check: copy the old check AND cadet_test.py into their own folder (the checks exec cadet_test by replacing
  their own file name, so a renamed check can't find it).
- Saving on (for reload tests): open without ?nosave and step frames while waiting for window.__sc (rAF is mocked);
  probes in /tmp/rv17/probe (reload.py, play.py, matrix.py, musapp.py; not in the repo).
- Never `pkill -f` a pattern that's in your own command line (it kills your own shell).
- player_check has 3 "reserved job" FAILs that are old (same on 0.92.6 5898c190).

## Open questions for the user
None from me.
