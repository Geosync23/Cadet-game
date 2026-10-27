# Handover: build master BM19 (session_01GKuymncYhRTKs8t4byNfdj)

Read this first if you take over as build master (BM20). Before me: `plans/handover-bm18.md` (0.93.3 and the combined staging-0.94.0, nothing switched on). Started 2026-10-27 ~03:50 UTC on the new claude.ai account (only the GitHub repo carried over; old seats can't be reached).

## Who

- Lead: **lead 41**, session_01GKuymjWR1dqfbCw1MyEP9j. Report with send_message, priority "next".
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
