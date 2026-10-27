# Handover: build master BM19 (session_01GKuymncYhRTKs8t4byNfdj)

Read this first if you take over as build master (BM20). Before me: `plans/handover-bm18.md` (0.93.3 and the combined staging-0.94.0, nothing switched on). Started 2026-10-27 ~03:50 UTC on the new claude.ai account (only the GitHub repo carried over; old seats can't be reached).

## Who

- Lead: **lead 42**, session_01GKuymjnCHnpwDqB94PVwmV (branch claude/lead-42), from 2026-10-27 ~14:00 UTC (lead 41 confirmed; before: lead 41, session_01GKuymjWR1dqfbCw1MyEP9j). Report with send_message, priority "next".
- Reviewer RV23 (talk-close; vessel PASS). Other seats: ask lead 41 (TEAM.md on the lead's branch).

## Branch and builds

claude/staging-0.94.0 (push here only).

| Commit | What | Game sha256 | Checks |
| --- | --- | --- | --- |
| ce927cea | Merge B3 claude/train-titles 7ce89d56 (RV22 PASS) | d96674f9... | check_fast OK 415 s; cadet vs 19400976 ALL IDENTICAL |
| 4fea0aa0 | Merge VB1 claude/vessel 03b63d95 (RV23 PASS); backlog RV23-1 (VESSEL_FETCH not saved) | 823bf338... | check_fast OK 441 s; cadet ALL IDENTICAL (renderer noise, max 1 level) |
| three commits | P5_STEP5, EV_VESSEL_ON, EV_ENDING_ON -> true (lead 41's GO), design-doc + DEV_NOTES | | check_fast OK after each |
| d69473b7 | HUD + GAME_BUILD 0.94.0, build-table row | 22a392df864269161c929b98060b14c31fd9112cc412e58c394d4b6d27b591e3 | check_fast OK 425 s |

The user's decision: TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, PAD_ON stay off; END_WAY_BACK is cut, stays off.

## Now (2026-10-27 ~07:05 UTC)

- db3c0930: events_check fix c03d51da (vessel + ending together; test only; RV23 to glance). Gate part 1 on d69473b7 all green (machine x2, bigevents, fridays, day 16-19, 22, 27-36; events known-old FX24-2 only).
- **9faaee80** = merge of claude/talk-close-fix 6dfc4ec1 (B3 f52e2abc + W6 ea9e0f3c). Game sha256 **04cc0cb65f2272c8f7afbeb438b94d972d80a8f59d42580515b86a1a380e0dbf**. check_fast OK; cadet vs 19400976 ALL IDENTICAL (Day 1 Deck 4 doesn't reach any of it).
- Gate part 2 running (counts as its share of the round): controller_check every part but reach, then arrows endgo | arrows default, step5, endstay.
- Lead 41 started the round on 9faaee80 with three runners, two shares each: R1 session_01GKuymit8htMajswkRRb27s (CR1 minus arrows + CR4), R2 session_01GKuymjMx2JdLdXE2tHNFHG (CR2 + CR3 minus controller), R3 session_01GKuymjroMc9y1arLHK5aPv (CR5 + CR6 minus gate part 1, plus ending_check). They report to me and the lead. **GO/NO-GO is mine** when all are in; a must from my gate goes to the runners at once.
- Known-old: career "Relied on" before Day 5 (backlog 12), events FX24-2, perf one-offs (backlog 14, 32).

## Result

**GO from testing sent to lead 41, 2026-10-27 ~10:20 UTC: 1d5e8845, game 5f4c5415814c78eb4c93eaad76ecc35dfa53f1f7cbb4c1f5af541f3971900a0f.** Publishing and the integration fast-forward are the lead's and the user's. The findings below were all resolved (fixed in checks, or the vessel words); see the build table's '0.94.0 round' row.

## Step 6 staging

**claude/staging-p5s6 64e296df** (lead 41, 2026-10-27 ~10:40 UTC): staging-0.94.0 6f1915cb + W6's claude/p5s6-core 9e5867e6 (95ef6947 + handover-w6). Game a0ba2ffc...34b2. check_fast OK; cadet vs 1d5e8845 ALL IDENTICAL; names_check OK on a P5_STEP6-on copy. Step 6 builders branch from it; merges of Step 6 pieces go here (cadet vs 1d5e8845 must stay ALL IDENTICAL while P5_STEP6 is off). claude/integration was fast-forwarded to 6f1915cb (0.94.0) on the user's OK, ~11:55 UTC, check_fast OK.

Step 6 merged so far: **3e502cac** = MA6 claude/p5s6-mech-a c3ca5e84 (RV23 PASS 27166bec + notes); game 7977c6db...; check_fast OK, cadet vs 64e296df ALL IDENTICAL, names_check on a P5_STEP6-on copy (sed `const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');` -> `P5_STEP5 && true;`). Then **8d1c749f** = PZ6 claude/p5s6-puzzles e16be289 (RV23 PASS; S6-8 cases; controller_check ALL_PARTS has both s6cases and m21); game 2c66a6ab...; check_fast OK, cadet vs 64e296df ALL IDENTICAL, names on/off OK. Then **b472fa1a** = MA6 8f943e82 exactly (RV23 PASS, M24; not MA6's later 268da7dc, unreviewed); game 7ba2d535...; checks as before. Then DA6 dd32a9a7 (RV23 PASS, S6-4 complete; controller part deck6; game 7dc5ca9b...; checks as before). Then MA6 e0b7f36e (RV23 PASS a92d0562, S6-6 turn 2 incl. 268da7dc; game aed66f5a...; checks as before). No 0.94.1 (the user): W7's claude/escort-follow-fix cffe8187 and PZ6's claude/team-turn-fix 12afb4a (both from integration 6f1915cb) go into staging-p5s6 on RV23's pass; cadet then differs only where the fixes show; promo4 already carries the escort fix (expect a trivial overlap). Then (lead 41's order): **95f25925** W7 escort-follow-fix cffe8187 (game dcbb2ecd...); **6c2188e3** W7 promo4 up to 9dcd0b1a (S6-3; not S6-7 9d24b9f9+, in review; cadet first run differed in a_start only, rerun identical = load timing; game 66b5f94c...); then N6 nights 992a4b0 (S6-1; game ca623378...; also took out a duplicate controller_check promo3 registration line the promo4 merge left). Then **ad45d5fc** MA6 db56362e (m24Call guard; game 48a94daf...). Then **8e0778ef** PZ6 escort-seated-check 775c3ca (test only; RV24 code read OK). **affc771e** PZ6 team-turn-fix 12afb4a (live fix; controller_check: part_s6cases keeps its 3-line tail, then part_team; 'team' in ALL_PARTS, NEEDS, PART_FN; controller team + s6cases OK; game 90de821c...). Then PZ6 91710ce (casePoint for S6-7, puzzle_check p8; game 595877d1...). Waiting: W8 (was W7, session_01GKuymk95u5t4uDsahatkPN) S6-7 on promo4. When promo4 (W7, bfcebb6d) lands: keep t4 first in the Step 6 ladder rows (RV23).
Step 6 seats (tell each when staging-p5s6 moves, priority next): W7 career session_01GKuymjghu82TGWPLR1wTKw (p5s6-promo4), N6 nights session_01GKuymnDA25R2a5yZGYpaBS (p5s6-nights), MA6 session_01GKuymj1UEDuEYMnG9rmFkc (p5s6-mech-a), PZ6 session_01GKuymjrmdGE4vaHHHGkvYF (p5s6-puzzles), DA6 session_01GKuymjJ4sU5hfdU8bH49UW (p5s6-deck). Reviewer RV23 session_01GKuymoDm1XbC5G8TvaCNLr.

## 0.95.0 (Step 6 on)

**Final build: claude/staging-p5s6 e0084ca9, game sha256 d1666007e449f9bdcfc01d3f2f2c2a60dfeb866b46ddb23404c38df56f59f278.** OLD = 0.94.0 (integration 6f1915cb, game 5f4c5415...). Merged before the flip: AS1 arrows-step6 ee18d663 + 75f6262c, AS1 m24-pick-pointer 5f649b45, DA6 2df6bfce, 5c27b740, 4a84e153, W8 promo4 6f13b61a (all RV24 PASS); BM19's P5_STEP6 sweep of the checks (b6d10b8f). Flip d2b43ac7: P5_STEP6 = P5_STEP5 && true, HUD/GAME_BUILD 0.95.0. Then W8 9063aafe (cqSat, lead 42's call). Round started ~18:00 UTC, 5 shares: me (cadet vs 0.94.0 ALL IDENTICAL; machine x2, mech, promo_beats, ending | bigevents, events, fridays), R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2 session_01GKuymicEV4pw2WFLo8iHrq, R3 session_01GKuymmv95Tm7siWzMeEgmS, R4 session_01GKuymignKdueCaz2pftLEC (shares in my message to lead 42). GO/NO-GO is mine.

**Round 1 on e0084ca9 = NO-GO**: R1 found a game gap (night 2's arrows pointed at rooms, not the rack/console); DA6's fix 673ac4f2. Check fixes from round 1 (test only): events INVITE, career tab + 4 KB budget (lead 42; backlog BM19-1), mech m15 past the nights, ending_check on a Step-6-off copy that assigns window.P5_STEP6 (R3), promo_beats t4passed closes an open scene (W8), arrows step6 coil card (AS1). Backlog BM19-2 (p5nWordTick null guard). **Candidate 2: claude/staging-p5s6 82b02fb9, game sha256 4a4bed1c6d7b8cb4354d4c4217e970ba2d5b3758a7f0ade48c3c22b159069595**; full round 2 started ~19:30 UTC, same shares (ending_check moved to R3); runners start as their round-1 share ends.

## Round findings (2026-10-27 ~08:40 UTC, game 04cc0cb6)

- **MUST, open:** arrows_check week stalls Day 4 13:21 at "Fix a wobbly stool" (wb-stool, 5-stool-1, Works bay). Bisected (R1 + me): 4fea0aa0 clean, bf228260 (P5_STEP5 = true only) stalls. Sent to lead 41 for a Step 5 builder.
- Open: mech_check ps "in person" FAIL: W6 says check isolation (Step 5 rows now run in the main page after m1-t2; passes alone). W6 fixing.
- Fixed in checks (test only, pushed to 68151ff8): career (W6 pick), mech t3 skip (W6), events vessel + ending, puzzle / ending / saves / controller with switch lines already true (BM19). W6 has de29e7cd (events vessel-off test, promo_beats t3off) to come.
- R2: lines_check 4 vessel lines over 90 chars: W6's words fix on claude/vessel-words (changes the baked game: check_fast, lines, events vessel, phone look).
- controller walk times out on #rot in my container even on 0.93.3 (load); R1 alone: OK.
- Green: R1 all (player, devmode, bubble, social, talk, arrows_pointer, dev_arrow, day 4/6/8/11/12/13, appt, saves, puzzle, ending, endgo x3, cadet); R3 all but mech ps; mine: step5, endstay, arrows default except week. Pending: R2's rest, my controller (rest of the parts).

## Gotchas

- Fresh container setup: `pip install playwright numpy pillow`, three.js r128 and acorn 8.12.1 into /tmp/cadet-work (plans/testing-guide.md section 2). Without acorn check_fast stops at step 2.
- Never pkill -f with a pattern that also matches your own lane's command line (it killed my lane twice).
- At most two browser checks at a time. check_fast is itself two; run it alone.
- design-doc has no section of its own for the ending; the switch-on is recorded in Open questions' "Answered" list and plans/ending-spec.html holds the design.
