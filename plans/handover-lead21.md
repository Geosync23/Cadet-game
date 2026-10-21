# Handover: lead 21

Lead session session_01KYPEbF745ZQ9g9kr4XJgre, branch `claude/lead-21` (push only there). Took over from lead 20 at 18:12 UTC 2026-10-20. Hourly check-in: trig_01JLTVsSNP1Udi9Qs7kJxvyt (minute 9) — a successor disables it and makes its own. Read CLAUDE.md, this note, TEAM.md (bottom = newest), plans/handover-lead20.md (standing rules, links), plans/roadmap-after-recdeck.md.

## Standing user rules (unchanged from lead 20, plus)
- **Seats: up to 5 working at once** (the user: "3-4 steady", then "or even 5 really"). No 6-7 bursts.
- Handover at 500k/600k for every seat; notify on published build / decision / results; never in overnight mode; "Identity verification is required" → tell the user at once; every published page has answer/comment boxes; cut things parked, not deleted; main and the main game link untouched without the user's go.
- The user is often on the phone/driving: keep messages short, one decision at a time, "recommended" answers welcome.

## Pages published this session (answers in each page's db, collection `answers`)
- Short Fridays plan https://claude.ai/artifact/8UwSCYe3LsQGoDBgxYeJQp (scratch file scratchpad/fp/fridays-plan.html; docs fridays-plan, fridays-plan-v2). Final rev 4 claude/patch-plan cdeb1ff. Decided: auditorium, skeleton crew, bubbles, expected (small rep dip), shape, both, 16:00 sign-out; four addresses Days 5/12/19/26, ~16 lines, normal clock (slowed clock parked).
- Friday addresses lines https://claude.ai/artifact/JhJzq5CTnVj2NSDedZ63DW (scratchpad/ad/friday-addresses.html; doc friday-addresses): q1 keep 16-19 lines over 16:00-16:48, q2 "borrowed this room" yes, q3 keep the wink, q4 names = the Pale Shoals / Tavessa (given in chat).
- Save script: appended before </body> (copy from the fp page); form#answers data-collection/data-doc; div.q[data-qid]; radios by qid; <qid>-comment.

## The playtest patch (step 2) — state at writing (00:10 UTC 10-21)
- claude/integration: 0.64.5 7958332 (batch E: #25 #21 #6 #24 #5 ladder, #30 mug, #29, #26 First Light Cocoa; events_check fix); 0.64.6 being pushed by BM11 (patch-b 16df5bd: D #7 #9 #10 #8, F #16 #20 #22 #27, #10 lane ease, #31 Ask Zeke parked behind INTRO_ASK_ON=false).
- Left: PR2's re-review of claude/patch-a 75aa54a (A-C + fix round; OR1 PASS on all hooks). Then the **release round** (plan sent to BM11): merge patch-a (efba55a) + patch-b 319f541 (revert of 'relied' 48 → 40, machine_check 3-7, backlog row 17) + bake EW1's cocoa name swap (claude/events-lines fdf4339: plans/events-ready/firstLightCocoa/... over content/meetings/firstLightCocoa.meet, plus content/facts.md) + switch ON LADDER_ON, MUG_ON, FLC_ON (REC_DECK already on; EVENTS_ON, INTRO_ASK_ON off) + full round alone, intro_check in pieces (--evening, --week, --firsts; part 12 is >1.5 h).
- Then publish: a NEW page for the patch build (integration starship-cadet.html), republish the Dev page https://claude.ai/artifact/EWB21cTQnXc8ZT71zCeEzf (its scratch file was lead 20's: integration build + a first-line script forcing location.hash '#dev'; rebuild it the same way), notify the user with what changed (the 30 items + #31 + names), ask them to play.
- Reputation: no change (PB measured: early words did not speed up; "Trusted Day 3"/"Relied on Day 4" predate F = backlog row 12; the user's later balance pass).

## Step 4 (ship-wide events) started early (the user, 23:27 UTC)
- EV1 session_014ckxYgG3KA6eHksEMi6Eru, claude/events-base: brief plans/events-base-brief.md (OR1 PASS WITH FIXES, folded 6e71069); F0a 835ab24 (calendar, Friday hold) awaiting PR2; then F1a. User answers: old saves skip past events (decided once, saved); Day 20 Captain's table 19:00-20:15 on night weeks; Day 12 auditorium opens for the address. Lead: F6 Dev buttons with Dev Stop 3; bigevents_check.py outside check_fast; F8 calls home only. EV1 bakes each event's lines in the turn that builds it.
- EW1 session_01KkAhg7eVhPenBBVfLufPU1, claude/events-lines: addresses + all four events' lines done, PR2 PASS (407fd07); ready files in plans/events-ready/; idle. Open with EV1: myrank, myshift:night, {leavers}, .address bake.
- The Fridays build (~8 turns, plan cdeb1ff) comes after the patch, before the first event.

## Seats (session_...)
PA 01Jka314UJ2Yto5XxbcQnB8H (done, ~477k, on call; handover on patch-a efba55a) · PB 01FWW2piuXkFYaRRzLXZiqYb (done, ~53%, handover plans/handover-patch-builder-b.md) · PE 01H7weuTSkTfuSAqhxvdx1EK (stopped, handover-patch-e.md) · PR2 013ttt3gV3DaF9y4caBtFnh9 (patch + content reviewer, ~390k) · OR1 01W7AHxrcgBM3rJNtCFKwp9W (owner stand-in reviewer, ~38%) · BM11 01W7NHRM4JjqaNEJQUWNxgcE (build master, ~200k) · EV1, EW1 above · stopped: PP1, DR1, DB1, lead 20 019UJSCUCdtC1kTpYiABWKhs.

## Gotchas learned
- A seat in one long turn doesn't act on new messages until the turn ends (PA ran 6 h). Re-send one consolidated list when it goes idle.
- Some seats kept reporting to lead 20; lead 20 forwards. Tell new seats the lead's session id in their first brief.
- get_session context_usage often reads 0 for helpers; they estimate.
- intro_check takes >2 h whole: run it alone and in pieces; browser checks side by side time out (page reload 16-18 s on 0.64.5).
- list_sessions / list_events results are big; prefer get_session per seat.
- Reload time rising (14 s → 16-18 s in the container): note for step 7 (optimization).
