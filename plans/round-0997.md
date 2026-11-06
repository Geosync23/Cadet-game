# 0.99.7 full round: the six shares (BM25 for lead 49, 2026-11-06)

Same six shares as plans/round-0996.md (its commands and its notes on FX30's and RV31's probes still hold), plus what the
0.99.7 pieces touch. R1-R4 and R6 fresh runners (lead 49), R5 the build master.

Candidate = the claude/staging-0997 tip BM25 names in its GO: 0.99.6 (claude/integration d7ad4c58, game f6ff5ec1...db8a8)
+ the 0.99.7 pieces at their reviewers' exact PASS commits + one switch-on commit + the build turn (build 0.99.7). Your
file's sha256 must match the GO's. OLD = 0.99.6, claude/integration d7ad4c58 (game sha256
f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8).

Pieces (plans/patch-0997.md has the user's 56 notes and the seats): CH1 characters and seats, MV1 movement and needs, TP1
tips and device, CR1 career, JB3 jobs, SC1 social and stories, CL1 calendar and arrows, EV1 new first-week events, GM1
tiles and Lightdisc, TB6 hosted traditions, AV1 sound and screens. All switched ON in the candidate (the list is in the
switch-on commit and the 0.99.7 build-table row).

Expected cadet differences vs OLD: many, by design (characters' soles, hair, seat poses and seats, the rec deck's
toilets and sofas, the tracker and tips, the film, the calendar). BM25 explains each in the build table before the GO;
anything not explained there is NEW.

Steps for every runner: plans/testing-guide.md "How a runner runs its share" (checkout, sha256 must match, own
CADET_WORK, two browsers at most, any FAIL: run on OLD; NEW FAILs to BM25 + lead at once). Notes in
plans/checks-0997-rN.md on your own branch claude/checks-0997-rN. Known old: backlog 14 / perf one-off spikes
(re-measure alone twice, backlog 32); sound_check "long" under load (backlog BM24-1: run sound_check alone).
Known check flakes, rerun before reporting (backlog BM22-2, BM22-3): player_check Saving, devmode_check "real".
stories_check always with 36 days (`python3 stories_check.py BUILD 36`, backlog BM22-1).

| Share | Seat | Checks |
|---|---|---|
| R1 | fresh | player_check, bubble, puzzle (whole), social, talk, arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea, arrows_pointer, day_check 4, 11, 25, 26, 2, 9, arrows endstay, p5retry_probe (on an off copy, as 0.99.6) |
| R2 | fresh | intro_check (whole), intro_check --dinner, --firsts, perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, arrows endgo, pf_f1_same OLD BUILD 10, **fresh_walk BUILD (RV32)** |
| R3 | fresh | controller_check (every part but reach; long: split into background scripts under 90 min), sound_check, promo_sight, arrows_d, arrows_f, ending_check; devmode_check (all parts), dev_arrow_check |
| R4 | fresh | career, appt, saves, title_check, device_check (whole), day_check 6, 8, 23, 24, 16, fixtap_probe (on an off copy), fixtap_reach BUILD, fixtap_click OFF BUILD, **cr1_check BUILD** |
| R6 | fresh | interactions_check (whole, alone, no time limit; about an hour) |
| R5 | BM25 | check_fast.sh, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food (1 7, 11 4), clothes, stories (36), promo_beats, day_check 12, 13, 17, 18, 19, 27, 3, p5retry_break OFF BUILD, **weekend** |


Added for 0.99.7 (bold) (arrows_check week, already in R1's default parts, covers TP1's week-1 arrows, CR1's Day 8 test, JB3's jobs);
fresh_walk (R2, from `git show origin/claude/review-rv32:plans/rv32-probes/fresh_walk.py`, run from the repo root:
`python3 plans/rv32-probes/fresh_walk.py BUILD 3 $CADET_WORK/fw.json`; no OK line: pass = Day 1's briefing meets and the Chief
stays to its end, the Day 1 arrow leads to the Works bay before 08:50 then to the clock, Day 2's 08:45 solo meeting and 18:00
booths each get an arrow and happen, no page errors, the follower never stuck an hour); cr1_check (R4, new check: it flips its own switches); weekend
(moved to R5 beside events and bigevents: EV1's first Saturday, CL1's cut Saturday run). Already in a share and touched
this time: player (MV1 fitness, TP1), career and promo_sight (CR1), events, bigevents, fridays, join, tiles (CL1, EV1,
GM1, TB6), sound (AV1), lines, talk, social, stories (SC1), perf (AV1's film, CH1), interactions (MV1's rec washroom,
TP1), machine (MV1), day checks (CL1's calendar).
Not in the gate: controller_check reach (non-blocking extra).
Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).
Sessions: lead 49 session_01GKuymjjreuZtZeDMBX79xn; BM25 session_01GKuymnYTNkfxgLvtfFRg7w; R1 session_01GKuymnpcUSBmpZYiDK67GH,
R2 session_01GKuymmnJnzWMxP769P9Edd, R3 session_01GKuymo7sJwyufjkoEsCacB, R4 session_01GKuymmvXPrmsnyaH858XoJ,
R6 session_01GKuymjS1cBK12RvWv7L5ka.
GO (BM25, 2026-11-06 ~13:00 UTC): claude/staging-0997 at the GO commit named in the message (build turn 363107d; later docs-only commits do not change the game), game sha256 b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d. Expected cadet: differences by design (BM25 lists each in the round record); a difference you cannot explain from the 0.99.7 notes, or a page error, is NEW.

## Round 0997b: candidate 2 (BM26 for lead 50, 2026-11-06 ~15:40 UTC)

Candidate 1 (b14421f8) found new FAILs A-L (the list and each cause: the round record below). The game fixes made candidate 2,
so lead 50 (the user's rule: every game change runs the full round) asked for the full round again on it: the same six
shares as above, with the fixed check files. Record each share in plans/checks-0997b-rN.md on your own branch.

Candidate 2 = claude/staging-0997 at the GO commit BM26 names: candidate 1 + the check-only fixes (TP1 6050082 and 042949a
arrows_check: A, H; CL1 adf96c5 interactions_check: G-store; GM1 3966a4a disc_check, controller_check: F, J; CL1 cce2169
weekend_check: L; CR1 mech_check, devmode_check, arrows_d_check, cr1_check: B, D, E) + the game fixes (EV1 b374343: the
Last Light no longer closes the bow lounge, appointments never book over its hour, Dev mode's tradition start on its day:
C, D, G-orange; CR1 93eb0e4: 24p crCarryPark, Dev mode's career table and Day 8 test beat, crTestOpen without the second
playerShiftOn: B #15, D; CL1 4bd36a1: 17 lines shortened, lines_check knows {item}: K). The build stays 0.99.7.
Your file's sha256 must match the GO's.

Same commands, notes and known-old list as above, with these changes:
- arrows_check step6: the four ways in one run are fine now (each way its own browser context, TP1 042949a).
- pf_f1_same OLD BUILD: F1's own test must pass (0 mismatches); the 30 fingerprints differ by design (the 0.99.7
  switches); the proof is OLD vs the candidate with every 0.99.7 switch line set false: 30 same.
- R2's long ones (fresh_walk, p926, pf_f1 proof) go to whoever finishes first (agree it between you, copy BM26 and lead
  50); perf_check alone, last of everything.
- Still to come: SC1's controller_check.py for I (the pad's way to a full-width button). R3 runs the controller ending
  part again with it when it lands; until then the ending part's Day 34 lines are I, known and owned.
