# The Fable review version: the full round (BM29 for lead 52, 2026-11-15)

The user asked for a thorough review of the live game (0.99.91) and a SEPARATE version carrying the review's fixes, on its
own link. main and claude/integration do not move. This page is the round's plan and record, whole on one page: every
check, who runs it and how, with no "same as the round before" (FR1's review, B10, asked for one list).

## What is being tested
- **Candidate** = claude/staging-fable-review at the GO commit BM29 names. Your file's sha256 must match the GO's.
  Label on screen: 0.99.92-review.
- **OLD** = 0.99.91, main cdd9efd, game sha256 b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3
  (`git show cdd9efd:starship-cadet.html > old.html`).
- **Piece 1, FR1** claude/fable-review-code (safety and speed; plans/review-fable-code.md section A): LOOP_GUARD_ON (A1),
  SAVE_KEEP_ON (A2), SAVE_TELL_ON (A3), LIB_SAY_ON (A4; its line is indented, inside the page's first script),
  SLEEP_SAFE_ON (A5), LOAD_SAFE_ON (A6), EVON_MEMO_ON (A7), WALLS_STILL_ON (A8), SAVE_TAB_ON (A12). **TEX_READ_ON (A9)
  stays OFF** (it changes pictures; a question for the user). New check robust_check.py. tools/one_byte.py (A10) is run
  LAST on the merged file by BM29.
- **Piece 2, FR2** claude/fable-review-play (play fixes; plans/review-fable-play.md): FRP_LINE_ON, FRP_FOOD_ON,
  FRP_TRAY_ON, FRP_PINTAP_ON, FRP_LEAD_ON, FRP_PANELS_ON, FRP_LABEL_ON, FRP_BLINK_ON, FRP_THANKS_ON, FRP_TIPS_ON,
  FRP_SAY_ON, FRP_WORDS_ON. New check frp_check.py.
- Reviewer RV37. Each piece is merged only on lead 52's word, at the commit lead 52 names.
- **Expected differences vs 0.99.91:** written here by BM29 at the GO (from the two pieces' build-table rows and the
  reviewer's notes). Anything not on that list is NEW.

## The six shares (every check of the round)

Setup: plans/testing-guide.md section 2 (playwright, numpy, pillow; three r128 and acorn 8.12.1 in your own CADET_WORK;
`CADET_CHROME=/opt/pw-browsers/chromium`). BUILD = the candidate's starship-cadet.html. Two browsers at most at once.
Every check: exit 0 AND its OK line. Start long runs detached (`setsid nohup`), each lane under 90 minutes.

| Share | Seat | Checks, in order |
|---|---|---|
| R1 | runner | player_check; bubble; puzzle (whole); social; talk; arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea (one run), arrows endstay; arrows_pointer; day_check 4, 11, 25, 26, 2, 9; p5retry_probe (on a copy with P5_RETRY_ON false); **frp_check (whole; new)** |
| R2 | runner | cadet_test OLD BUILD (first, alone); intro_check whole, --dinner, --firsts; path; arc; lines_check and lines_check --day; day_check 0, 1, 5, 7, 21, 22; arrows endgo; plans/rv31-probes/pf_f1_same.py OLD BUILD 10 and its all-off proof (below) |
| R3 | runner | controller_check (every part but reach; background scripts under 90 min); sound_check; promo_sight; arrows_d; arrows_f; ending_check; devmode_check (all parts); dev_arrow_check |
| R4 | runner | career; appt; saves; title_check; device_check (whole); day_check 6, 8, 23, 24, 16; fixtap_probe (on a copy with FIXTAP_ON false); plans/rv31-probes/fixtap_reach.py BUILD; fixtap_click.py OFF BUILD; cr1_check; p926_check; plans/rv32-probes/fresh_walk.py BUILD 3 (five points, "long []" needed); **robust_check (whole; new)** |
| R5 | BM29 | check_fast.sh; machine x2; mech (judge by the full run); bigevents; fridays; events; disc; tiles; join; food 1 7 and 11 4; clothes; stories 36; promo_beats; day_check 12, 13, 17, 18, 19, 27, 3; weekend; plans/rv31-probes/p5retry_break.py OFF BUILD; cr2_check; plans/tb7-probes/drill.py; plans/tp2-probes/tp9991_probe.py (on a copy with TP9991_SD_ON false); plans/ev2-probes/simprobe.py (read by eye); **tools/one_byte.py --check BUILD (0 to change); cadet_test before-one_byte vs after (ALL IDENTICAL)** |
| R6 | runner | interactions_check (whole, alone, no time limit, about an hour); then perf_check BUILD OLD alone, last of everything; **day_check 10, 14, 15, 20 (new this round, see "The list" below; run them on OLD first)** |

Notes that still hold:
- **pf_f1_same** prints FAILED when OLD lacks NEW's switches only if fingerprints differ; the pass is F1 mismatches 0, no
  page errors, and the all-off proof: 0.99.6 (claude/integration d7ad4c58) against the candidate with every switch since
  then false gives 30 same. This round's all-off copy also sets the 9 FR1 switches and the 12 FRP switches false
  (remember LIB_SAY_ON's indented line). R2's handover note has the script.
- **fresh_walk** has no OK line: pass = Day 1's briefing meets and the Chief stays to its end, the Day 1 arrow leads to
  the Works bay before 08:50 then to the clock, Day 2's 08:45 meeting and 18:00 booths each get an arrow and happen, no
  page errors, the follower never stuck an hour, "long []".
- **lines_check** reads the words files of its own checkout: run OLD in its own worktree.
- **cadet_test** "ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)" counts as identical.
- **perf_check** alone on a quiet machine; a one-off spike is re-measured alone twice (backlog 32). FR1 saw its 30
  second page-load limit trip under load: nothing else running while it measures.
- **sound_check** timing flake (backlog BM27-1): alone twice, and on OLD, before calling it.
- **controller_check G2 tiles** failed one run in three before (backlog CP4-1; round 09991b's find G): rerun alone
  twice and on OLD; report it either way, it is not to be waved through as a one-off without the reruns.
- A check run on one part alone can flip against the full run (mech_check m15): judge by the full run.
- Not in the gate: controller_check reach.
- **Any FAIL:** run the same check on OLD. Known old = a backlog row, fails the same way on OLD, message matches: today
  that is backlog 14 (perf "memory grows across deck round trips") and backlog 23 (food_check 7 1 "garden, good").
  Anything else is NEW: to BM29 and lead 52 at once, and to the other runners if it could touch their shares.
- Record your share in plans/checks-fable-rN.md on your own branch (claude/checks-fable-rN): commit, sha256, a table
  `Check | Result | Key lines`, each FAIL with its proof. Report "Rn: OK" or "Rn: FAIL ..." to BM29 and lead 52.
- Whoever finishes early offers to take a check from the slowest share (agree it, copy the lead, never twice).

## The list, and what this round does about FR1's finding B10
FR1 found that the round is bigger than the notes say and is not written in one place. For this round:
1. **This page is the one list.** The table above names every check of the round; nothing is "as last time".
2. **The five round checks that were not in the repository are now in it,** at the paths the runners already use, copied
   unchanged from the review branches (claude/review-rv31 73e5cd80: plans/rv31-probes/pf_f1_same.py, fixtap_reach.py,
   fixtap_click.py, p5retry_break.py; claude/review-rv32 03a33391: plans/rv32-probes/fresh_walk.py). Every runner runs
   the candidate commit's copy.
3. **Checks the test picker (tools/affected.py) does not know** (it lists 51 entries, 274 minutes; its map is from
   0.64.12): appt_check, arrows_check, arrows_d_check, arrows_f_check, controller_check, cr1_check, cr2_check,
   p926_check, promo_sight_check, stories_check, title_check, and now frp_check. All twelve are in the round above. The
   picker is not the gate, so it is not changed in this round (backlog BM29-1: bring the picker's list and the guide's
   table in step with this page, or retire the map).
4. **Days never run by day_check in a round:** 10, 14, 15, 20 (the picker lists 15). Added to R6 this round, OLD first:
   a day that fails the same way on OLD is recorded as old and new to the backlog, not held against the candidate.
5. **"Skipped" guards** (a check that passes while testing nothing): each runner counts the lines containing "skipped"
   in each NEW log (`grep -c skipped`) and puts the count in the notes; a check whose count is not 0 is named in the
   report so BM29 can compare with OLD.
6. Not done in this round (FR1's plan items for later, the lead's to schedule): a WebKit smoke check, the test clock for
   setTimeout, the round as a GitHub job, an expected-parts list per build.

## Sessions
Lead 52 session_01GKuymmPLvgySfNEhDYyACj; BM29 (R5) session_01GKuymivPt7VEMWm4jUuY4G; FR1
session_01GKuymmYzraWXg9ELUMmqri; FR2 session_01GKuymj5amgjHqQCKPsVnFs; RV37 session_01GKuymo8n7x4hGZtoPmWXqX.
R1, R2, R3, R4, R6: to be hired by lead 52 (handover notes plans/handover-rN.md on claude/checks-09991-rN).

## Round record (BM29)

### Setup and rehearsal (before any PASS; nothing of the game pushed to staging)
- claude/staging-fable-review made from main cdd9efd and pushed.
- Rehearsal on a local scratch branch (never pushed): FR1 1155555 then FR2 f038d8d merged. Only plans/build-table.md
  clashed (every row kept, keepboth.py). verify_merge: 0 problems for both. All switches off: game c205ae53...8e85.
- Rehearsal switch-on (21 switches; TEX_READ_ON off), one_byte.py (1,433,472 tokens read the same; 132 characters in
  code escaped, 29 in comments, mark added), label 0.99.92-review (setbuild.py took it): content_gen up to date,
  names_check OK.
- Found in rehearsal:
  1. **lines_check fails on FR2 f038d8d**: bank event.crossingLine.frp.missed is 194 characters (at most 90).
     lines_check is not in check_fast. To FR2.
  2. **lines_check fails after one_byte.py**: "the baked blocks in the game file are out of date", while
     content_gen.py --check says up to date. lines_check does not know the one-byte mark. To FR1 (check-side).
  3. LIB_SAY_ON's switch line is indented (`  const LIB_SAY_ON = false;`), unlike the rest: the switch-on and all-off
     scripts must match it on purpose.
- Rehearsal results on the all-on file (scratch, FR1 1155555 + FR2 f038d8d, escaped, labelled; game 2c3c691e...79dd):
  - events_check OK (884 s). robust_check OK (448 s). The label 0.99.92-review broke nothing.
  - **check_fast FAILED: device_check**, 2 lines, each twice: "tips: once each, a tap closes, the switch" and "tipSeen:
    marks without showing, drops a waiting tip, leaves the one on screen". Still fails with FRP_TIPS_ON alone off;
    FRP_PANELS_ON (a tip card waits while a panel is open) is the likely cause. To FR2: a game fault or the check's
    expectation, and the fix. Blocks the switch-on (never push when check_fast says FAILED).
  - **frp_check cannot run on a switched-on build**: its "off" half fails and then it stops (assert: it looks for
    `var FRP_LINE_ON = false;`). robust_check uses a switch that is already on; frp_check must make its own off copy.
    To FR2.
  - **cadet_test vs 0.99.91: DIFFERENCES FOUND, as expected with FR2's switches on.** No page errors. Views a to d
    identical (0 px). Views e_night to i_tap0: about 584 px, all inside the arrow's label box at the left edge (FRP_LABEL_ON:
    the label's new shape, two lines allowed). Views i_tap1 on: 2,268 to 11,903 px: the needs cards come in a different
    order ("Very hungry" first, was "Missing people": FRP_FOOD_ON), so the arrow and its label differ ("the call
    booths" where 0.99.91 said "A toilet"). FR2's own all-off file is ALL IDENTICAL. To be confirmed at the real build
    with one run with FRP_LABEL_ON and FRP_FOOD_ON off (expected ALL IDENTICAL).
- The label 0.99.92-review: the only check that reads the number is intro_check (major and minor only). See the gates.

### Build
(to come)

### Gates
(to come)

### Every share
(to come)
