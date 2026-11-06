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
| R1 | | |
| R2 | | |
| R3 | | |
| R4 | | |
| R5 (BM27) | | |
| R6 | | |

### Finds

| Item | Check (share) | Cause | Closed by |
|---|---|---|---|
| P | fresh_walk point 5 (R2's, run by R4): two arrows up over 3 ship hours, 'The call booths', Day 2 21:38-22:30 and Day 3 17:29-22:30 (0997b: none) | NEW, game, TP998_BOOTH_ON: section 15's needs marker for Social only knows the booths (NEED_FIX.social = ['callhome']); after the day's call a repeat booth now gives nothing, so a lonely player is sent to a booth that won't call, again and again (in 0.99.7 the repeat still gave +40 social) | open: sent to lead 50 + TP1 ~19:58 UTC (suggested: behind TP998_BOOTH_ON, no booth marker once today's call is used) |

Round notes: BM27's first R5 run hit the 30-minute background limit after machine, mech and bigevents (all OK); the rest
restarted 19:54 UTC (plans/build-master/bm27/r5rest.sh). R2 gave fresh_walk and p926 to R4 (agreed, lead copied).
