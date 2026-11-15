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
- **Expected differences vs 0.99.91** (FR2's list, RV37's review). Anything not on this list is NEW.
  - FR1's nine: nothing in ordinary play. Only when something goes wrong: an error card instead of a frozen game, an
    unreadable save kept and offered in the Saves app, a notice when saving fails, the title saying the 3D library
    could not be fetched, damaged saves loading. A tab in the background does not save over a newer one.
  - LINE: Day 7 from 14:15 a gold arrow "The Line oath, 14:40: the bow lounge"; a missed oath's Mail says "We read the
    oath without you..."; an invitation heads-up adds the tradition's name.
  - FOOD: with Food under 10, "Very hungry" again at 07:00 and 17:00; the Food arrow returns whenever no other arrow
    shows. (This is what changes cadet_test's later pictures and its taps list.)
  - TRAY: tray in hand in the mess, no other arrow: "A seat for your tray" on the nearest free seat.
  - PINTAP: a tap at the arrow's pin, its label or the floor beside it, with someone standing there, does the arrow's
    thing, not their card.
  - LEAD: on the arrival a tap on Zeke from afar, or on his arrow, walks you to him.
  - PANELS: solid job board and alarm card; tips wait for a person's card, the job board, the alarm card, the time
    clock and Ship health to close (not for the device).
  - LABEL: arrow labels too long for one line wrap to two; short labels are drawn exactly as before.
  - BLINK: Day 4 14:11-14:30, a softer Last Light blink about every 11 s of play.
  - THANKS: no form thank-you Mail after one-offs, birthdays, event gatherings or the Captain's address.
  - TIPS: view, needs and pause tips on the arrival evening after dinner; "Slept well?" only before 09:00.
  - SAY: three reworded messages (job gone back to the board; board heading over a finished job; clock after 09:00).
  - WORDS: "is/are running" by the machine's name, "Calibrate oven 2", the deck once in Job taken, small-job pop-ups
    without the repeated title, "Cargo hold", "a covered plate", the Calendar button "Don't remind me".
  - No switch: quiz question 34 says "rec deck" (lead 52 accepted).

## The six shares (every check of the round)

Setup: plans/testing-guide.md section 2 (playwright, numpy, pillow; three r128 and acorn 8.12.1 in your own CADET_WORK;
`CADET_CHROME=/opt/pw-browsers/chromium`). BUILD = the candidate's starship-cadet.html. Two browsers at most at once.
Every check: exit 0 AND its OK line. Start long runs detached (`setsid nohup`), each lane under 90 minutes.

| Share | Seat | Checks, in order |
|---|---|---|
| R1 | runner | player_check; bubble; puzzle (whole); social; talk; arrows_check (default parts), arrows step5, arrows step6 asis/teachoff/track/skiptea (one run), arrows endstay; arrows_pointer; day_check 4, 11, 25, 26, 2, 9; p5retry_probe (on a copy with P5_RETRY_ON false); **frp_check (whole; new)** |
| R2 | runner | intro_check whole, --dinner, --firsts; path; arc; lines_check and lines_check --day; day_check 0, 1, 5, 7, 21, 22; arrows endgo; plans/rv31-probes/pf_f1_same.py OLD BUILD 10 and its all-off proof (below) |
| R3 | runner | controller_check (every part but reach; background scripts under 90 min); sound_check; promo_sight; arrows_d; arrows_f; ending_check; devmode_check (all parts); dev_arrow_check |
| R4 | runner | career; appt; saves; title_check; device_check (whole); day_check 6, 8, 23, 24, 16; fixtap_probe (on a copy with FIXTAP_ON false); plans/rv31-probes/fixtap_reach.py BUILD; fixtap_click.py OFF BUILD; cr1_check; p926_check; plans/rv32-probes/fresh_walk.py BUILD 3 (five points, "long []" needed); **robust_check (whole; new)** |
| R5 | BM29 | **as gates, counted as the round's runs (wave 1):** check_fast.sh, events, cadet_test OLD BUILD; **then:** machine (once; it also runs inside check_fast); mech (judge by the full run); bigevents; fridays; disc; tiles; join; food 1 7 and 11 4; clothes; stories 36; promo_beats; day_check 12, 13, 17, 18, 19, 27, 3; weekend; plans/rv31-probes/p5retry_break.py OFF BUILD; cr2_check; plans/tb7-probes/drill.py; plans/tp2-probes/tp9991_probe.py (on a copy with TP9991_SD_ON false); plans/ev2-probes/simprobe.py (read by eye); **tools/one_byte.py --check BUILD (0 to change); cadet_test before-one_byte vs after (ALL IDENTICAL)** |
| R6 | runner | interactions_check (whole, alone, no time limit, about an hour); then perf_check BUILD OLD alone, last of everything; **day_check 10, 14, 15, 20 (new this round, see "The list" below; on the candidate only, OLD only for a day that fails)** |

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

## Keeping the round's cost down (agreed with lead 52, 2026-11-15; no check dropped, six runners kept)
a. **Runners do not read DEV_NOTES.md** (about 190,000 tokens). A runner reads this page and its own handover note.
b. **No check twice.** BM29's gates (check_fast, events_check, cadet_test vs 0.99.91) are the round's runs of those
   checks; R2 does not repeat cadet_test. machine_check runs once outside check_fast. The condition: every check of the
   round runs once on the final candidate's exact sha256, and the record names the seat that ran it.
c. **OLD only on a FAIL.**
d. **Two waves.** Wave 1 is BM29 alone on the candidate: the gates, then lines_check, frp_check, robust_check and
   device_check as an early look (about 35 minutes; R1, R2 and R4 still run these in their shares only if wave 1's
   run was not on the final sha256: otherwise wave 1's run is the round's run and the record says so). Only when wave
   1 passes are the five runners hired. Wave 2: R6 and R3 start first, R1, R2, R4 about ten minutes later.
e. **Runners stay silent** between the start and the final report unless there is a FAIL or a sha256 mismatch, and
   look at their background lanes rarely.
f. A second candidate means the full round again (the user's rule), so wave 1 exists to get candidate 1 right.

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
4. **Days never run by day_check in a round:** 10, 14, 15, 20 (the picker lists 15). Added to R6 this round, on the candidate only; OLD is run for a day that fails:
   a day that fails the same way on OLD is recorded as old and new to the backlog, not held against the candidate.
5. **"Skipped" guards** (a check that passes while testing nothing): each runner counts the lines containing "skipped"
   in each NEW log (`grep -c skipped`) and puts the count in the notes; a check whose count is not 0 is named in the
   report so BM29 can compare with OLD.
6. Not done in this round (FR1's plan items for later, the lead's to schedule): a WebKit smoke check, the test clock for
   setTimeout, the round as a GitHub job, an expected-parts list per build.

## Sessions
Lead 52 session_01GKuymmPLvgySfNEhDYyACj; BM29 (R5) session_01GKuymivPt7VEMWm4jUuY4G; FR1
session_01GKuymmYzraWXg9ELUMmqri; FR2 session_01GKuymj5amgjHqQCKPsVnFs; RV37 session_01GKuymo8n7x4hGZtoPmWXqX.
Hired by lead 52 at 09:11 UTC: R1 session_01GKuymidX8V6F2KKDcoZ5LE, R2 session_01GKuymigbASLB86pjcbY5LY, R3
session_01GKuymjwGjfNXnjezjs87rS, R4 session_01GKuymnZfZ6qmpeytQExvGQ, R6 session_01GKuymjzQWrtt6PCGyfmQUB. Results on
claude/checks-fable-rN, plans/checks-fable-rN.md.

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
- FR1's piece merged on lead 52's word: claude/fable-review-code a077808 (RV37 PASS A1-A8, A12 and tools/one_byte.py; also
  the owner check). Only plans/backlog.md clashed (every row kept; RV37's FR1-3 and FR1-4 added). verify_merge 0
  problems; the game file is exactly FR1's (all off, sha256 923b6c64eb73e510cf9396f6ea74fa654b6a30eef3c8f9255db69a8e944a1c5d).
  content_gen up to date, names_check OK, lines_check PASS (0 errors), check_fast QUICK CHECK OK in 262 s.
- FR2's piece merged on lead 52's word: claude/fable-review-play fe156c8 (RV37 PASS F1-F12). Only plans/build-table.md
  clashed (all 14 of FR2's rows kept). verify_merge 0 problems on the game, DEV_NOTES, design-doc and CLAUDE.md. All
  off: game 9eda598866aa30a33dd54174f7c2e8a2f54a7fe2988d42c03ca735a0fd6dc8f1; content_gen, names_check, lines_check OK.
- Switch-on: the 21 switch lines only (plans/build-master/bm29/switchon.sh; TEX_READ_ON checked off).
- tools/one_byte.py last: 1,433,183 tokens read the same; 132 characters escaped in code, 29 in comments; --check: 0 left.
- Build turn: label 0.99.92-review (setbuild.py), DEV_NOTES paragraph, build-table row. content_gen up to date,
  names_check OK, lines_check PASS (0 errors).
- **Candidate 1: claude/staging-fable-review 75d1b8339dba9e30f0179f685c1a8082a9ed8888, game sha256
  d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0.** Later docs-only commits do not change the game.

### Gates and wave 1 (BM29, on candidate 1's exact file d6b9ce81...a1c0; these are the round's runs of these checks)

| Check | Result |
|---|---|
| check_fast | QUICK CHECK OK in 254 s (words, names, deck, device, machine, leave) |
| lines_check | PASS (0 errors) |
| tools/one_byte.py --check | 0 characters outside Latin-1; the mark is there |
| events_check | EVENTS CHECK OK (812 s) |
| cadet_test vs 0.99.91 | DIFFERENCES FOUND, as expected, no page errors. Views a_start to i_tap0 (nine pictures): 0 px. i_tap1 to j_steer1: 1,760 px; j_steer2: 11,693 px; taps 1 and 2 show "Very hungry" where 0.99.91 showed "Missing people". Cause: FRP_FOOD_ON (Food is under 10 in that scene, so the warning is said again and the Food marker takes the free arrow) |
| cadet_test vs 0.99.91, with only FRP_LABEL_ON and FRP_FOOD_ON off | ALL IDENTICAL: the other 19 switches and the escape step change no picture |
| cadet_test, before the escape step vs after | ALL IDENTICAL |
| robust_check (whole) | ROBUST CHECK OK (560 s) |
| frp_check (whole, fe156c8's file) | OK (486 s); run again with ab130f2's file (the words part walks every machine name) as R5's first item |
| device_check (whole, alone) | OK (124 s) |

After the build commit: FR2's ab130f2 merged on lead 52's word (frp_check.py, a DEV_NOTES line, FR2's handover note; the
game is unchanged, checked). **GO commit: claude/staging-fable-review c4999dae, game sha256
d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0. Check files: this commit's.**

**Because wave 1 ran on the final file, these are done and are NOT run again** (cost rule b): cadet_test (was R2's),
lines_check without --day (R2 runs only `lines_check --day`), robust_check (was R4's), device_check whole (was R4's),
frp_check (was R1's; R5 runs it with the final check file), check_fast and events (R5's).

### Every share (candidate 1, c4999dae, game d6b9ce81...a1c0)

| Share | Result | Notes |
|---|---|---|
| R5 (BM29) | OK, 28 of 28 exit 0 with the OK line: frp_check (ab130f2's file), one_byte --check, cr2, drill, tp9991, simprobe (by eye: Days 3, 25, 39 19:30-20:30; tap, card ev9991.sim, a pod), machine, mech (full), bigevents, fridays, disc, clothes, promo_beats, food 1 7 and 11 4, join, weekend, stories 36, tiles, day 12 17 13 3 27 18 19, p5retry_break. Plus wave 1 (table above). "skipped" lines: day 12 and 13 one each (the rec deck's evening comparison on the storm days, by design); food_check one each ("Schedules: not using the rota yet ... skipped": a part of food_check that tests nothing, old, for the B10 list); stories 78 that are only the word in its own printout | logs /home/user/bm29/logs (scratch) |
| R2 | OK: intro whole/--dinner/--firsts, path, arc, day 0 1 5 7 21 22, arrows endgo, pf_f1_same (F1 0 mismatches; all-off proof with 60 switches false: 30 same). lines_check --day: FAIL once beside another browser (1 s of overlap), the same on OLD (3 s), PASS alone: check-side, backlog R2-1 | plans/checks-fable-r2.md, claude/checks-fable-r2 |
| R4 | OK: career, appt, saves, title, day 6 8 23 24 16, fixtap_probe, fixtap_reach, fixtap_click, cr1, p926, fresh_walk (long [], stuck [], errors []). title_check stopped once on timing under load, then OK three times and on OLD (backlog R4-1). fresh_walk's Day 2 booths observation: old-equivalent (RV37's probe, FR2's probe agree; backlog RV37-2) | plans/checks-fable-r4.md, claude/checks-fable-r4 bda8520a |
| R6 | OK: interactions_check (2205 s); day 10, 15, 20; perf_check BUILD OLD alone, last: PERF CHECK OK (4281 s, no PROBLEM line, deck round trips 470 -> 470 -> 470; 2 scenes skipped, both Step 6, the same 2 as round 09991b). Day 14 FAIL, the same line word for word on OLD: old, backlog R6-1, not held against the candidate | plans/checks-fable-r6.md, claude/checks-fable-r6 000d68f |
| R3 | OK, every check once, no reruns: controller_check (57 parts, all but reach, first time with the switches on), sound, promo_sight, arrows_d, arrows_f, ending, devmode (all parts), dev_arrow | plans/checks-fable-r3.md, claude/checks-fable-r3 7965b01 |
| R1 | OK, 17 of 17 once: player, bubble, puzzle, social, talk, arrows default, step5, step6 four ways (692 minutes due, 0 missed, 0 stuck), endstay, arrows_pointer, day 4 11 25 26 2 9, p5retry_probe | plans/checks-fable-r1.md, claude/checks-fable-r1 |

Closed along the way (none is a NEW fault of the candidate):
- R4's fresh_walk, Day 2 18:00 at the call booths (five taps open Davi Keane's card): old-equivalent (RV37's probe; FR2's
  three-build probe). R4's three extra walks: the candidate repeats itself; with only FR1's nine switches off the walk
  is identical, so FR1's switches do not change a player's day; candidate and 0.99.91 first differ at Day 0 18:26, "A
  seat for your tray" (FRP_TRAY_ON), then the Food arrow (FRP_FOOD_ON): intended. Backlog RV37-2.
- Check-side timing, each passing alone and the same on OLD: title_check (R4-1), lines_check --day (R2-1).
- Old game bug found by the new day: Day 14, Theo stuck 20 minutes (R6-1).
- food_check holds a part that tests nothing ("Schedules: not using the rota yet ... skipped"), for the B10 list.

**Result: round fable OK, all six shares. FINAL GO (BM29, 2026-11-15 ~11:25 UTC): claude/staging-fable-review, game
commit c4999dae (later commits are docs only), game sha256
d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0, build 0.99.92-review. Every check of the round ran
once on this exact file; the tables above name the seat. main and claude/integration are untouched (cdd9efd).**

For the user's notes (not faults): a player who follows the arrows has a different first three days than in 0.99.91
(the tray seat, the Food marker); TEX_READ_ON (A9) is built but off, a question for the user; quiz question 34's
"rec deck" has no switch; backlog R6-1, RV37-2, FR1-3, FR1-4, R4-1, R2-1, BM29-1.
