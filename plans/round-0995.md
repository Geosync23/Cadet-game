# 0.99.5 full round: the five shares (BM22 for lead 47, 2026-10-31)

Same shares as plans/round-0994.md (lead 47), plus the areas the 0.99.5 pieces touch. Cap 5: BM22 (R5) + four fresh
runners R1-R4. Candidate = the claude/staging-0995 tip that BM22 names in its GO (0.99.4 596712bc + the pieces below at
the exact commits their reviewers passed, the switch-on commit, build 0.99.5). Your file's sha256 must match the GO's.
OLD = 0.99.4, claude/staging-0994 596712bc (game sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a),
or claude/integration once 0.99.4 is published (same game).

Pieces (each in only at its reviewer's PASS commit): JB2 jobs (claude/p995-jobs) + SW4's tour words (claude/p995-jobs-words
7e30feb, RV28); PL2 and CT5 (controller) (RV29); SD5 sound (claude/p995-sound), OB2 onboarding (claude/p995-onboarding),
TB3 traditions notes 8, 10, 19 (RV30). Switched ON in 0.99.5: SND_LONG, TRAD995_ON, JB2's JOBCAP_ON / SPREAD_ON /
CHECKS_ON. Stay OFF until the user picks: MESS_SCALE, SND_BUF_ON.

Expected cadet differences vs OLD: only where the switched-on pieces show (jobs and the Works tour, the traditions spots
and seats, the onboarding changes); BM22 explains each in the build table before the GO. Anything else is NEW.

Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM22 + lead at once). Notes in
plans/checks-0995-rN.md on your own branch claude/checks-0995-rN. Known old: backlog 14 / perf one-off spikes
(re-measure alone twice). Known check flakes, rerun before reporting (backlog BM22-2, BM22-3): player_check Saving,
devmode_check "real". stories_check always with 36 days (`python3 stories_check.py BUILD 36`, backlog BM22-1).

| Share | Seat | Checks |
|---|---|---|
| R1 | fresh | player_check, bubble, puzzle, social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, 25, 26, **2, 9**, arrows endstay |
| R2 | fresh | intro_check (whole), **intro_check --dinner, --firsts**, perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, weekend, arrows endgo |
| R3 | fresh | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | interactions_check (whole, alone, no time limit), career, appt, saves, title_check, **device_check (whole)**, day_check 6, 8, 23, 24, **16** |
| R5 | BM22 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories (36), promo_beats, day_check 12, 13, 17, 18, 19, 27, **3** |

Added for 0.99.5 (bold): day 2 (JB2's first rounds tour, TB3 19's dinner seat), day 9 and day 16 (TB3 19), day 3; intro
--dinner/--firsts and device_check whole (OB2). Already in a share and touched this time: sound_check (SD5), controller_check
(CT5/PL2), machine/mech/career (JB2), events/bigevents/food/join (TB3), player/interactions/talk/deck (JB2/TB3/OB2), appt.
New checks the builders add (lead 47): each runs in the share that already holds its area. BM22 fills in the exact commands as each piece is merged, before the GO:
- R5: machine_check part 5z and mech_check round23 (JB2), as parts of machine x2 and mech; TB3's spice / tea / beam probes if they become checks (traditions, beside events and join).
- R3: sound_check's new parts hide, mess_scale and long (SD5), inside sound_check; the controller turn parts (CT5/PL2), inside controller_check.
- R2: OB2's intro probes (beside intro_check whole, --dinner, --firsts). R4: OB2's appt probes (beside appt).
Not in the gate: controller_check reach (non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).
Sessions: lead 47 session_014zyJYM4mt9ZDCD5H9JZDtN; BM22 session_014zyJYNgBPdEPHLxTGrM889; R1-R4: the lead hires and lists them in TEAM.md.
