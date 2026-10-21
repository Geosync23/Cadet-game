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

## FINAL STATE at handover, ~01:12 UTC 2026-10-21 (lead 21 at 517k)
Lead 22 takes over. Read CLAUDE.md, this whole note, TEAM.md bottom (everything since 18:12 is logged there), plans/roadmap-after-recdeck.md (newest section: optimization after events; overnight rule).

**The user's latest decisions (00:50-00:56):** overnight mode tonight (the user will say when it starts): **take the recommended answer to every plan question and log it** in plans/overnight-decisions-lead22.md ("as always"); no phone notifications overnight. Up to **7 working seats**. Ship-wide events one at a time in story order (Crossing the Line → storm → comet → visit), each plan AND build adversarially reviewed. The first events should have "a really interesting little story". **Optimization pass right after ship-wide events** (not tonight).

**In flight:**
1. **Playtest patch release round (BM11, 0.64.7, local f60bd92):** patch-a efba55a + patch-b 319f541 + cocoa names (Pale Shoals / Tavessa) + LADDER_ON/MUG_ON/FLC_ON on. So far: check_fast, day, events, food OK; cadet_test differences all explained (ladder texts; FLC changes Monday crew plans). Running player/career/interactions/bubble/join/lines, then perf + intro pieces, + day_check Day 12 vs 0.64.6 (FR1 found Day 12 fails on 0.64.6 itself: backlog #18). When BM11 pushes clean: **publish the patch as a NEW page** (integration starship-cadet.html; title e.g. "Starship Cadet Playtest 0.64.7"), **republish the Dev page** https://claude.ai/artifact/EWB21cTQnXc8ZT71zCeEzf (integration build + a first-line script forcing location.hash '#dev'; publish to that URL), tell the user what changed (30 notes + #31 Ask Zeke removed + new names + rec deck on). Notify unless overnight.
2. **Events base (EV1, claude/events-base):** F0a, F1a, F1b/F1c, F2 PASS (PR2). Next F3a (device schedule; hooks s19/s15b → OR1). F0b (called-in) needs PB's section 14 planner call: eventGatherings(d) has no caller, and named crew must be brought into meetings even when on shift (Tomas, Day 7). Asked EV1: event cues unlock right away (not at hour end); lines_check 90-char cap off for event.* Mail/toasts; answer FR1 on the Friday hold. EV1 must not edit bigevents_check.py (EC1 owns it).
3. **bigevents_check.py (EC1, claude/bigevents-check 0c48458):** PASS (PR3). Idle until EV1's next pieces.
4. **Fridays (FR1, claude/fridays):** brief ac5236a PASS (PR3); turn 1 b1720a1 pushed → PR3 + PB reviewing; turn 2 next. Waiting on EV1's hold answer by turn 5.
5. **Crossing the Line plan (EP2, claude/event-plan-line 85d49ce):** story A "Who answers the oath" recommended (line-q9), q1-q8 recommendations; ER2 reviewing. When it passes: publish the page with the save script (copy from scratchpad/fp of lead 21: not available to you, so re-create: form#answers data-collection="answers" data-doc="event-line-plan", Save button, script reading div.q[data-qid] radios + <qid>-comment, db capability), tell the user; overnight take the recommendations and log them; then building (5-6 turns behind EV_LINE_ON, after the storm update per the plan) by a builder, ER2 reviews the build.
6. **Writer EW1 (claude/events-lines):** all lines PASS; ~440k; ~30 story lines for Crossing the Line after the user's answer/overnight recommendation.

**Seats (session_...):** BM11 01W7NHRM4JjqaNEJQUWNxgcE · EV1 014ckxYgG3KA6eHksEMi6Eru · EC1 01QgShGXD6P24DDxTp8npN41 · FR1 01FXFdUaCbBurQbdY9E58HKs · EP2 01GpiqZ9jCYbS9XTNPF8adHr · ER2 01S8pboNujAzZgMSWFK84CxD · PR2 013ttt3gV3DaF9y4caBtFnh9 (~320k) · PR3 01EtHMLLsjDYDHPG3JgCMbGi · OR1 01W7AHxrcgBM3rJNtCFKwp9W (~42%) · EW1 01KkAhg7eVhPenBBVfLufPU1 (~440k) · PB 01FWW2piuXkFYaRRzLXZiqYb (~53%, section 13/14/10 owner) · done: PA, PE, PP1, DR1, DB1. Lead 21 = 01KYPEbF745ZQ9g9kr4XJgre (idle after handover).
**Check-in:** disable lead 21's trig_01JLTVsSNP1Udi9Qs7kJxvyt (lead 21 does it) and create your own hourly one.
