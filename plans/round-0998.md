# 0.99.8 full round: the six shares (BM27 for lead 50, 2026-11-06)

0.99.8 = 0.99.7 (claude/staging-0997 1baafc1, game 1b17203d...bff9, FINAL GO, never published) + TP1's claude/p997-tips
913ba6c, both switches on: `TP998_ARROW_ON` (Day 2's booths arrow from 18:00, at Leila or the booths room, never Booth 1)
and `TP998_BOOTH_ON` (after today's one call home a booth shows only its "You've had your call home today" screen: no
15 minutes, no +40 social, no goodbye line). The lead's plan: plans/patch-0998.md on claude/lead-50. Reviewer: SC1.

Candidate = claude/staging-0998 at the GO commit BM27 names (the merge of 913ba6c, the switch-on commit, the build turn
0.99.8; later docs-only commits don't change the game). Your file's sha256 must match the GO's.
OLD = 0.99.6, claude/integration d7ad4c58 (game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8),
the published build. BM27 also runs cadet_test vs 0.99.7 (1b17203d...bff9): only the arrow and booth differences.

**The shares, commands and notes are round-0997.md's** (the table at its top, "Round 0997b" changes and its known-old
list), unchanged: R1-R4 and R6 the same runners, R5 the build master (BM27). Record each share in
plans/checks-0998-rN.md on your own branch. Any FAIL: run it on OLD; a NEW FAIL to BM27 and lead 50 at once.

Expected differences vs 0.99.6: everything round-0997.md's record explains for 0.99.7 (cadet: hair caps, soles, the
tracker ring, Fonseca's bunk, the Day 2 crew from ~07:45), plus 0.99.8's two: from 17:45 on Day 2 no booth arrow (from
18:00 the arrow at Leila or the booths room), and a second booth use on a day gives only its screen. Anything else is NEW.
Touched by 0.99.8: player_check (its new booth case), arrows_check (week: the d2-booths arrow), intro_check, fresh_walk
(Day 2's 18:00 booths), interactions_check (the booths), cadet.

Sessions: lead 50 session_01GKuymmoEriV3ugms2s3hsn; BM27 session_01GKuymjy5t3QwM8whGj2QFE; R1 session_01GKuymnpcUSBmpZYiDK67GH,
R2 session_01GKuymmnJnzWMxP769P9Edd, R3 session_01GKuymo7sJwyufjkoEsCacB, R4 session_01GKuymmvXPrmsnyaH858XoJ,
R6 session_01GKuymjS1cBK12RvWv7L5ka.

## Round record (BM27)

### Build
- claude/staging-0998 from claude/staging-0997 cac711d (= 1baafc1 + docs only: BM26's handover, the perf placement).
- Merge 913ba6c: only plans/build-table.md clashed (both rows kept). content/banks/tp997.lines unchanged from staging
  (CL1's shortenings kept); `content_gen.py --check` up to date; names_check OK.
- Switch-on: the one TP998 line, `false ||` -> `true ||` for both. The file then is exactly TP1's own both-on file
  (sha256 8c2ebe77643c6879c460a89227dec9d8e48055cf047f260beff7717504ca3803).
- Build turn 0.99.8 (setbuild.py: header and GAME_BUILD), DEV_NOTES 0.99.8 paragraph, design-doc "Calling home".
  Game sha256 298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462.

### Gates (BM27, before the GO)

| Gate | Result |
|---|---|
| check_fast | QUICK CHECK OK in 329 s |
| player_check | PLAYER CHECK OK (693 s), with TP1's new booth case (a booth again the same day: its screen only) |
| arrows_check default (all parts, week among them) | ARROWS CHECK OK (1617 s) |
| fresh_walk to Day 2 19:10 (FW_UNTIL=19:10) | no errors, nothing stuck; the d2-booths arrow from 18:00 ("Calling home, the booths on Deck 3: Leila shows you how"), no booth tapped; a trace run: d2-booths met 18:00, Leila's lines said 18:11; the walker had called home at 12:33, so no second call |
| cadet_test vs 0.99.7 (1b17203d) | ALL IDENTICAL (0 px in every view, no page errors, same taps): no view reaches Day 2's 18:00 or a second booth use |

SC1's review (2026-11-06 ~19:22 UTC): **PASS** on claude/p997-tips 913ba6c (off identical by reading and by cadet vs
0.99.7; edge cases: a day's first call untouched, save/load mid-day holds, Dev clock, mid-call). SC1's small note, not a
fix (for the user): the booth guard is at the top of actStart, so a booth tapped from across the room shows its "had your
call" screen without walking over.

**GO round 0998 (BM27, ~19:25 UTC):** claude/staging-0998 at this commit; the game last changed at the build turn 3616cd4;
game sha256 298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462, build 0.99.8. OLD = 0.99.6 d7ad4c58
(f6ff5ec1...db8a8). Check files: this commit's.

### Round 0998, every share

| Share | Result | Notes |
|---|---|---|
| R1 | OK, all 17 (player alone, bubble, puzzle, social, talk, arrows default parts, step5, step6 four-way missed 0 stuck 0, arrows_pointer, endstay, day 4 11 25 26 2 9, p5retry_probe) | plans/checks-0998-r1.md, claude/checks-0998-r1 e34d198 |
| R2 | OK, own checks: intro whole/--dinner/--firsts, path, arc, lines (0 errors) and --day, day 0 1 5 7 21 22, arrows endgo, pf_f1_same (F1 0 mismatches; all-off proof: 0.99.7 switches + TP998 false, 30 of 30 same), cadet vs 0.99.6 (same 15 views, pictures identical to 0.99.7's). fresh_walk and p926 by R4 (P), perf by R6 | plans/checks-0998-r2.md, claude/checks-0998-r2 59206328 |
| R3 | OK, every check: sound (alone), devmode (all parts), dev_arrow, promo_sight, arrows_d, arrows_f, ending, controller 57 of 57 | plans/checks-0998-r3.md, claude/checks-0998-r3 a24d034 |
| R4 | OK, every check (day 6 8 23 24 16, career, cr1, appt, saves, title, device, fixtap_probe, fixtap_reach, fixtap_click); also R2's p926 OK; R2's fresh_walk: FAIL point 5 = P (NEW) | plans/checks-0998-r4.md, claude/checks-0996-r4 |
| R5 (BM27) | OK, all 24: check_fast (gate), machine x2, mech, bigevents, disc, events, fridays, clothes, promo_beats, food 1 7 and 11 4, tiles, join, weekend, stories 36, day 12 17 13 3 27 18 19, p5retry_break; cadet vs 0.99.6: the same 15 views as R2, no page errors, same taps (explained) | /tmp logs; plans/build-master/bm27/r5.sh, r5rest.sh |
| R6 | OK: interactions_check whole (19:24-20:02 UTC, exit 0, no FAIL lines, draw-call peak 220; booths row as 0.99.7); also R2's perf_check OK (one frame spike in the full run, not on two alone re-measures: known-old backlog 32; draw calls as 0997b, within 1 of OLD, memory flat) | plans/checks-0998-r6.md, claude/checks-0998-r6 4a60f7b |

### Finds

| Item | Check (share) | Cause | Closed by |
|---|---|---|---|
| P | fresh_walk point 5 (R2's, run by R4): two arrows up over 3 ship hours, 'The call booths', Day 2 21:38-22:30 and Day 3 17:29-22:30 (0997b: none) | NEW, game, TP998_BOOTH_ON: section 15's needs marker for Social only knows the booths (NEED_FIX.social = ['callhome']); after the day's call a repeat booth now gives nothing, so a lonely player is sent to a booth that won't call, again and again (in 0.99.7 the repeat still gave +40 social) | game: TP1 cc44f94 (MV1 PASS): behind TP998_BOOTH_ON, no booth marker or booth tips once today's call is had, new lonely words; + 91a75b4 (MV1 PASS, backlog TP1-4): the Needs app's Social line names company; tp998.social.2 shortened by BM27 (lead 50's wording, 97 -> 70 chars, lines_check max 90). Candidate 2. |

Round notes: BM27's first R5 run hit the 30-minute background limit after machine, mech and bigevents (all OK); the rest
restarted 19:54 UTC (plans/build-master/bm27/r5rest.sh). R2 gave fresh_walk and p926 to R4 (agreed, lead copied).

**Result of round 0998 (candidate 1, d7f5bd6, game 29829196...c462): every share OK except P (NEW, game, TP998_BOOTH_ON).**
By lead 50's call the round ran to the end, then the fixes went into candidate 2 and a full round again (0998b).

## Round 0998b: candidate 2 (BM27 for lead 50)

Candidate 2 = candidate 1 + TP1 cc44f94 + 108fe12 (docs) + 91a75b4 (both MV1 PASS) + tp998.social.2 shortened; frozen at
f26070c (lead 50). Game sha256 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3, build 0.99.8. Same six
shares, commands and notes as round 0998 (round-0997.md's). Record each share in plans/checks-0998b-rN.md. OLD = 0.99.6
d7ad4c58. By lead 50's call the GO goes after player_check and check_fast; arrows default, fresh_walk to Day 3 22:30
(long [] needed: P) and cadet vs candidate 1 and vs 0.99.7 are the first items of R5, beside the runners; any FAIL there
stops the round.

Expected vs candidate 1: only P's fix (after today's call, a low Social: no marker to the booths, the toasts and the Needs
app name company; no booth tips). Expected vs 0.99.6: as round 0998.

| Gate (candidate 2) | Result |
|---|---|
| player_check | PLAYER CHECK OK (622 s) |
| check_fast | QUICK CHECK OK in 271 s |

**GO round 0998b (BM27, 21:27 UTC):** claude/staging-0998 at this commit (game last changed at f26070c); game sha256
13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3, build 0.99.8.

| Share | Result | Notes |
|---|---|---|
| R1 | OK, all 17 (step6 four-way missed 0 stuck 0; player alone); from R5: food 1 7, food 11 4, day 13, day 3, p5retry_break OK | plans/checks-0998b-r1.md, claude/checks-0998-r1 6cfcf42 |
| R2 | OK (own checks): intro whole/--dinner/--firsts, path, arc, lines (0 errors) and --day, day 0 1 5 7 21 22, arrows endgo, pf_f1_same (F1 0 mismatches; all-off proof 30 same), cadet vs 0.99.6 (pictures identical to c1); by R4: fresh_walk all five points (long [], P fixed), p926 OK; perf by R6 | plans/checks-0998b-r2.md, claude/checks-0998-r2 345966ac |
| R3 | OK, every check: sound (alone), devmode (all parts), dev_arrow, promo_sight, arrows_d, arrows_f, ending, controller 57 of 57 | plans/checks-0998b-r3.md, claude/checks-0998-r3 a7daa75 |
| R4 | OK, every check (day 6 8 23 24 16, career, cr1, appt, saves, title, device, fixtap_probe, fixtap_reach, fixtap_click); from R2: fresh_walk all five points (long [], P fixed), p926 OK; from R5: tiles, join, weekend, day 27 18 19 OK | plans/checks-0998b-r4.md, claude/checks-0996-r4 |
| R5 (BM27, with R1, R3, R4 after two container restarts) | OK, all 24: gates player, check_fast, arrows default, fresh_walk Day 3 (long []), cadet vs c1 and vs 0.99.7 ALL IDENTICAL; BM27: events, machine x2, mech, fridays, clothes, promo_beats, cadet vs 0.99.6 (15 views, pixel counts identical to candidate 1's); R1: food 1 7, food 11 4, day 13 3 12 17, p5retry_break; R4: tiles, join, weekend, day 27 18 19; R3: bigevents, disc, stories 36 | checks-0998b-r1/r3/r4.md; /tmp logs |
| R6 | OK: interactions_check whole (21:29-22:06 UTC, no FAIL lines, draw-call peak 220, booths row as 0998); perf_check from R2 OK (no spike; draw calls as 0998, within 1 of OLD, none over budget, memory flat) | plans/checks-0998b-r6.md, claude/checks-0998-r6 8e6e50d |

**Result: round 0998b OK, every share, no new finds. FINAL GO: claude/staging-0998 at the commit of this record, game sha256
13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3, build 0.99.8** (the game last changed at f26070c).

For the user (not faults): SC1's note, a booth tapped from across the room after your call shows its screen without walking
over; after today's call a lonely player is pointed to company (the mess, the bow lounge), never the booths; backlog TP1-1
(old: a shutdown booked into your night shift's clock-in). Container notes: BM27's machine restarted twice (~21:35 and ~22:44
UTC); R1, R3 and R4 took over R5 checks so each ran once (listed in the R5 row).
