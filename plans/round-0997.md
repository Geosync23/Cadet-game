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

## Round record (BM26, build master from ~13:00 UTC; BM25 before)

### Candidate 1: claude/staging-0997 7fd8f6b, game b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d
Gated before the GO by BM25: check_fast, machine, events OK. Round 0997 found new FAILs A-L (each passed on 0.99.6, or
a check expected the 0.99.6 game). Each one, its cause and how it was closed:

| Item | Check (share) | Cause | Fixed by |
|---|---|---|---|
| A | arrows_check clockin, Day 1 (R1) | TP1's clock-in waits for the 08:50 briefing; the check set it at 08:30 | check: TP1 6050082 |
| B | mech_check m4, #22, #15 (R5) | CR1's own cart (m4) and Make it safe again (#22): by design; #15: a lapsed lesson waited for Making it safe on a day it couldn't open | game (#15, crCarryPark) and check: CR1 9dfbb70 |
| C | appt_check, Brennan's book (R4) | EV1's Last Light closed the bow lounge 13:40-14:40, so Brennan's break took her far off, late for the 14:30 booking | game: EV1 b374343 (lounge open; no booking over the Last Light's hour) |
| D | devmode_check (R3) | trad: Dev mode refused a tradition on the Last Light's day; set/career: Dev mode's table and Day 8 test beat still on Day 9 | game (section 25): EV1 b374343, CR1 9dfbb70 + 93eb0e4; check: CR1 |
| E | arrows_d_check S3, pass-over (R3) | the check's day became the Day 8 test day | check: CR1 9dfbb70 (an ordinary Tier 1 Day 9) |
| F | disc_check #25 (R5) | TB6's Spice supper move (note 51) sends Erik to the gym at 17:22 on Day 2; the pair plays at 21:30 | check: GM1 3966a4a (the moment read from the plans) |
| G | interactions_check (R6) | store row: CL1's note 15 (not a tradition); Orange tree: Elif at the tree in the Last Light's lead-up | check: CL1 adf96c5; game: EV1 b374343 |
| H | arrows_check step6, three ways (R1) | each way loaded the previous way's Dev save from the shared browser | check: TP1 042949a (a browser per way); the old shutdown/night-shift clash: backlog TP1-1 |
| I | controller_check ending by pad (R3) | the check's pad steering bounced around a full-width button (SC1's two-button row); DOWN reaches it in the game | check: SC1 2ce2a48 |
| J | controller_check tiles by pad (R3) | GM1's tutorial has 15 steps; the check pressed A 12 times | check: GM1 3966a4a |
| K | lines_check (R2) | 17 new lines over 90 characters; {item} unknown to the check | words: CL1 4bd36a1 (+ two tweaks c72cff9); check knows {item} |
| L | weekend_check (BM25's gate) | the Saturday run is parked (CL1, note 30) | check: CL1 cce2169 |

Explained, not faults: pf_f1_same's fingerprints differ by design (F1's own test 0 mismatches; with every 0.99.7 switch
off, 30 of 30 fingerprints equal 0.99.6). interactions_check's garden camera turns vary run to run on 0.99.6 itself
(R6). EV1's own events and machine FAILs came from its branch's stale check files.

cadet_test vs 0.99.6 (R2 and BM26, alone, pixel counts identical): all 15 views differ; no page errors, taps the same,
state differs only in memory, draw calls and triangles. Every difference explained: hair caps and boots without the
flat sole on every person (CH1); the Schedule tracker's ring (TP1); Fonseca 0.1 m over in a bunk on Day 1 night (CH1);
from Day 2 ~07:45 the scheduled crew elsewhere with other bubbles (TRAD997_ON alone: TB6's Spice supper move to 19:15,
note 51; with only that move undone 0 of 75 Day 2 plans differ; the mornings' basins and seats shared out differently,
same activities). The player's path the same in every view.

### Candidate 2 (round 0997b): claude/staging-0997 c052cc8, game 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9
Gates: check_fast OK, devmode_check OK, events_check OK. Full round again (lead 50). New in 0997b:

| Item | Check (share) | Cause | Closed by |
|---|---|---|---|
| M | career_check s5 (R4) | EV1's lounge change ripples through the board's job mix: a steady Senior has 54 xp at Day 19, Trusted needs 55 (0.99.6: 59-63) | check: EV1 2325c5e (within 5 xp), lead 50's call; a career-pace note for the user |
| N | p926_check item 15 (R2's, run by R4) | the Spice supper's fixed old times, and Brennan's new host card unanswered (TB6, note 51) | check: TB6 ba33d0c |
| O | fresh_walk Day 2 booths (R2's, run by R4) | Leila's 18:00 scene does play (18:13, SC1's trace); fresh_walk's record doesn't log bubbles | explained; TP1's arrow improvements go to the next build |

cadet_test on candidate 2: every NEW picture pixel-identical to candidate 1's (R2), same counts in BM26's own run.

Round 0997b, every share on candidate 2 (check files at claude/staging-0997 after each check fix; the game unchanged at 1b17203d...bff9):

| Share | Result | Notes |
|---|---|---|
| R1 | OK, every check (step6 four-way: missed 0, stuck 0) | plans/checks-0997b-r1.md, claude/checks-0997-r1 60f32da |
| R2 | OK: intro whole/--dinner/--firsts, path, arc, lines and lines --day (0 errors), day 0 1 5 7 21 22, arrows endgo, pf_f1_same (F1 0 mismatches; switches-off proof 30 same), cadet explained | plans/checks-0997b-r2.md, claude/checks-0997-r2 e2472ba |
| R3 | OK, every check; controller_check 57 of 57 | plans/checks-0997b-r3.md, claude/checks-0997-r3 1f3099b |
| R4 | OK, every check (career with 2325c5e); also R2's fresh_walk (five points) and p926 (with ba33d0c) | plans/checks-0997b-r4.md, claude/checks-0996-r4 57bcc3d |
| R5 (BM26) | OK: check_fast, machine x2, mech, bigevents, fridays, events, disc, tiles, join, food 1 7 and 11 4, clothes, stories 36, promo_beats, day 12 13 17 18 19 27 3, p5retry_break, weekend; cadet alone | this record |
| R6 | OK: interactions_check whole; also R2's perf_check (draw calls within 1 of 0.99.6, none over budget, memory flat) | plans/checks-0997b-r6.md, claude/checks-0997-r6 456a627 |

**Result: round 0997b OK. FINAL GO: claude/staging-0997 at the commit of this record, game sha256
1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9, build 0.99.7.**

For the user's notes (not faults): a steady Senior can be a point short of Trusted on Day 19 (M); Lightdisc's Day 2 pair
plays at 21:30, not 17:18 (F); the Saturday run is parked (L, note 30); backlog TP1-1 (a shutdown booked into your night
shift's clock-in, old, in 0.99.6 too).
