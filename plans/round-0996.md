# 0.99.6 full round: the shares (BM24 for lead 49, 2026-11-01)

Same split as plans/round-0995.md, plus the areas the 0.99.6 pieces touch. Five shares: BM24 runs R5, lead 49 hires
R1-R4 (CLAUDE.md asks for six runners; lead 49 said to reuse 0.99.5's split; a sixth share can be made by moving
interactions_check whole out of R4 on its own if the lead hires one more).

Candidate = the claude/staging-0996 tip BM24 names in its GO: 0.99.5 (6475bb30, game 93aed54f...5164) + the pieces below
at the exact commits RV31 passed + the switch-on commit + (once the user has chosen) the picture choice + the build turn
(build 0.99.6). Your file's sha256 must match the GO's.
OLD = 0.99.5, claude/integration 6475bb30 (game sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164).

Pieces (RV31 PASS, plans/review-rv31.md on claude/review-rv31):
- FX30 claude/fix-0996, game at 6701201: P5-1 and its follow-up (`P5_RETRY_ON`: the first "Follow the line" case is
  tried again each ship hour, not given up; a save stuck at 'none' waits again once) and JB2-2 narrowed (`FIXTAP_ON`:
  with "Unstick a gym locker" yours, a tap on the Treadmills at its stop does the job). Both switched ON (lead 49).
- PF1 claude/perf-0996, game at c5527f4: F1, shipEffectsAt keeps fxFrom's answers on the hour's record (always on, same
  answers; section 17, the systems engineer's). Four picture switches `PF_PR_ON`, `PF_SH_ON`, `PF_CAP_ON`, `PF_NOAA`:
  OFF unless the user chooses one before the build turn; BM24 will say in the GO which (if any) are on.

Expected cadet differences vs OLD: none with the picture switches off (the switched-on pieces show only with a job held
or in the first p5 case, which cadet_test doesn't reach). If the user turns a picture option on, every picture differs
(that is the option); BM24 says so in the GO. Anything else is NEW.

Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM24 + lead at once). Notes in
plans/checks-0996-rN.md on your own branch claude/checks-0996-rN. Known old: backlog 14 / perf one-off spikes
(re-measure alone twice, backlog 32). Known check flakes, rerun before reporting (backlog BM22-2, BM22-3): player_check
Saving, devmode_check "real". stories_check always with 36 days (`python3 stories_check.py BUILD 36`, backlog BM22-1).

| Share | Seat | Checks |
|---|---|---|
| R1 | fresh | player_check, bubble, puzzle (whole), social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, 25, 26, 2, 9, arrows endstay, **p5retry_probe (on an off copy, below)** |
| R2 | fresh | intro_check (whole), intro_check --dinner, --firsts, perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend, arrows endgo, **pf_f1_same OLD BUILD 10** |
| R3 | fresh | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, title_check, device_check (whole), day_check 6, 8, 23, 24, 16, **fixtap_probe (on an off copy), fixtap_reach BUILD, fixtap_click OFF BUILD** |
| R5 | BM24 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories (36), promo_beats, day_check 12, 13, 17, 18, 19, 27, 3, **p5retry_break OFF BUILD** |

Added for 0.99.6 (bold):
- FX30's probes need the switch's off line (they make their own on copy). On the candidate, make an off copy first:
  `sed 's/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/' BUILD > $CADET_WORK/off_p5.html; python3 p5retry_probe.py $CADET_WORK/off_p5.html`
  `sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/' BUILD > $CADET_WORK/off_ft.html; python3 fixtap_probe.py $CADET_WORK/off_ft.html`
- RV31's probes, from `git show origin/claude/review-rv31:plans/rv31-probes/NAME.py > NAME.py` into your checkout's
  plans/rv31-probes/ (run from the repo root): `fixtap_reach.py BUILD` (exactly one thing takes a job: the locker's
  Treadmills), `fixtap_click.py $CADET_WORK/off_ft.html BUILD` (every click the same on and off), `p5retry_break.py OFF BUILD`
  (OFF = an off copy with both switches false), `pf_f1_same.py OLD BUILD 10` (0 mismatches, the fingerprint the same).
- Already in a share and touched this time: puzzle (P5-1), interactions and arrows week (JB2-2), perf_check (F1 and the
  picture switches), day checks and machine (F1 is read by the planner's mood and needs each hour).
- If the user turns a picture option on: perf_check's draw-call and frame numbers change by design (R2 says which), and
  cadet_test differs everywhere; every other check should be unchanged.
Not in the gate: controller_check reach (non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).
Sessions: lead 49 session_01GKuymjPvM7XFzxM7XqFREd; BM24 session_01GKuymnYTNkfxgLvtfFRg7w; R1-R4: the lead hires and lists them in TEAM.md.
