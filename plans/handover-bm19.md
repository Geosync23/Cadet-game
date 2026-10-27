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

## Still to do

1. Gate part 1 (on d69473b7, running): machine_check twice, bigevents, events, fridays, day_check 16-19, 22, 27-36. Logs in my scratchpad (gone with the session).
2. On lead 41's word (RV23 PASS): merge B3's claude/talk-close f52e2abc. It is on with no switch, so cadet_test vs 19400976 will differ: explain each difference (with the three switches on, the copies of 0.93.3 differ anyway; compare against a d69473b7 copy too, to see talk-close's own part).
3. Gate part 2 after talk-close: check_fast, cadet vs 19400976 (each difference explained), controller_check (all but reach, with ending, m19, m20, s5cases, vessel, shut, door), arrows_check incl. step5, vessel, endstay, endgo.
4. Tell lead 41 the commit + game sha256 for the six-runner round (OLD = 19400976). Known-old: career "Relied on" before Day 5 (backlog 12), events FX24-2, perf one-offs (backlog 14, 32).

## Gotchas

- Fresh container setup: `pip install playwright numpy pillow`, three.js r128 and acorn 8.12.1 into /tmp/cadet-work (plans/testing-guide.md section 2). Without acorn check_fast stops at step 2.
- At most two browser checks at a time. check_fast is itself two; run it alone.
- design-doc has no section of its own for the ending; the switch-on is recorded in Open questions' "Answered" list and plans/ending-spec.html holds the design.
