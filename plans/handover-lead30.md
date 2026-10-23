# Handover: lead 30

## START HERE (lead 31)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-30` (from "~21:30 UTC: LEAD 30 took over").
2. Branch: start `claude/lead-31` from `claude/lead-30`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 30's `trig_01C4xaMNkCBn2wv7cqfJQrXD` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you (priority "now"; ask for a one-line acknowledgement).
5. Tell the user in one short message that you've taken over.

Lead 30 = session_016evGvfNY88TNKgaHErG9Q8, branch `claude/lead-30`. Took over 2026-10-22 ~21:30 UTC; handed over 2026-10-23 ~03:00 UTC at the user's request (the user starts lead 31 as a fresh, top-level session so the session chain resets; lead 30 was at depth 5 of 8). Lead 30 memory at handover ~45%.

## The user's standing rules (new in bold)
- Plain language, no jargon, no emojis. Few messages to the user: published builds, questions only they can answer, milestone summaries; "Noted." (one line) for routine helper news. Phone notification (PushNotification) only for a published build, a milestone or a question.
- **Whenever next steps are discussed, remind the user of everything still built but switched off (the user, 02:55).** After 0.92.0 that is: the controller (PAD_ON) and Crossing the Line (EV_LINE_ON).
- **Hire whatever is needed; usage resets soon; don't use more than needed (the user, 01:08).** The old limit of 18 helpers is lifted.
- **One combined build for the morning (the user, 01:50): 0.92.0.** Cut-off 07:00 UTC for each piece's reviewer PASS; late pieces go to the next build.
- **Teaching arrows ON in 0.92.0 (the user, 02:5x).** Settings "Teaching arrows" (Always / First times / Off, default First times). Lead's rule for Off: it removes teaching-only pointers/entries; the everyday goal/job arrow stays.
- **Zeke's Day 0 tour (the user, 00:45-01:10):** the dinner part (down to the mess with Zeke, sitting with him, the Chief, the linger, the goodnight) works perfectly and must NOT change; only the front end changes. Details under "0.92.0" below.
- **Day 0 dinner (the user, 01:45):** arrival 17:15; diners leave gradually at every meal, all the time (definitely the Sunday long tables); on Day 0 the table stays full until Zeke's goodnight, then thins; the long table stays on Day 0.
- **Breakfast comes back (the user, 00:58):** the Zeke problems weren't breakfast's.
- Pillar 5: the user considered ripping out or switching off Steps 1-4 (talked through only, no change). After 0.92.0 the user starts testing Steps 1 and 2 thoroughly. A "career steps" switch (one gate on CAREER_LADDER) was explained as cheap if ever wanted.
- Full round on six runners for every game change. main and published links change only for a passed build. Memory: judge from ~60%, never above 80%.

## Pages for the user
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq: both **Version 8 = 0.91.0** (claude/integration 989fd566, sha da9f1d08…4aee; controller off). PUB1 republishes from a named commit + sha.
- Fresh-eyes findings https://claude.ai/artifact/7GFQ8pZZxmZnTW3o6RHd6k (v21; items 1, 3, 4, 5, 16 = Done in 0.91.0). Batch 2 items (24, 25, 27, 29, 33, 38, 40, 41) are still "building": mark Done when 0.92.0 ships (25 = not a bug). Always read the live page first (Artifact read the url), edit the state JSON, publish with url.
- Game preview PDF (PW1): claude/game-preview 192f44b, plans/starship-cadet-preview.pdf (v2.1, 11 pages, 16 images; written from 0.91.0). Sent to the user. PW1 updates the first-evening page after 0.92.0 (17:15 arrival, Zeke's hand-over in bubbles + his Mail).

## 0.92.0: the combined morning build (BM14)
Base: BM14's staging claude/integration-next-fe1 **01b237f4** = 0.91.0 + controller follow-up dcdfe944 (controller off; cadet_test identical to 0.91.0). Merge order:
1. **claude/arrows-c** final tip, named by **AC3**: Pillar 5 fixes, teaching arrows (switch ON commit coming from AC3), fresh-eyes batch 2 (all PASS), FB1 delivery fixes (191bee5 PASS), FX3 15-18, FX5 p3 fix (c5eb7119, RV9 PASS, in at c68731c3), AC3's follower 8dd03049 (RV7 PASS). Waiting: FX4 m7 2e5581f9 + "Wait here for Calder" fc2e1c6d (RV9); FX3's Day 4 hydroponics vent + Day 8 "Mop up (2 of 2)" fix (cause: a nearby crew member's tapCrew takes the tap; fix in section 11's tap; RV7); FB1 test-setup fix 8438e7f + stale-line guard bd291e4 (RV8); the arrows ON switch commit (RV7; RV7 + AC3 week-test the shipped default POINT_ON + GUIDE_ON). Week status (AC3, arrows off and on): m1-m7 + p3 learned on their days, m6 reaches 'do' Day 8; only FX3's two items left.
2. **claude/breakfast-back** 0cd37b1b (SC1; reverts the rollback revert 2cabe96b): **RV8 PASS**.
3. **claude/zeke-tour** (DS1; built on breakfast-back; reviewer RV9 with a timed Day 0 recorder): 17:15 arrival; officers' corridor walk-and-talk; Bunk 1 wardrobe lines said while walking; Zeke walks up, faces you, 13 hand-over bubbles (words FINAL in plans/zeke-words.md on claude/zeke-words cb57522, the user chose the mix); the device opens on his Mail "Before you land" (mail.zeke.land); "Right, onward..." after it closes; the ship clock holds during the hand-over and while his Mail is open (like the manifest hold); wardrobe arrow drawn above bubbles and held while you're in Bunk 1 with the bag. Dinner part proven identical. Not pushed yet at handover.
4. **claude/dinner-spread** 0672133b (SC1; on breakfast-back): diners at meal traditions keep their seat for their own meal + linger (35-75 min), not until the tradition's end; Day 0 table full until Zeke's goodnight (introStepById('free')), then thins. Round running; then RV8. Numbers: Day 0 table worst minute 7 → 4; spice-shelf supper 22 in one minute → 4; ordinary dinners already staggered; breakfast's 09:00 peak = day shift leaving (kept).
5. **claude/tip-clear** feb2e54a (FX5; on breakfast-back): a device tip card never covers the goal arrow's target (moves below the pin, or lets taps through). → RV8. If PASS by 07:00, in.
Then: BM14 sets 0.92.0, build-table row, own checks (switch commit's differences checked alone) → **RV7 reviews the whole merge** → six-runner round (reach on its own runner; known: backlog 14, 23, 32; FB1's Folding-table interactions part may flake under load if 8438e7f isn't in: re-run alone) → fast-forward claude/integration on the lead's go → PUB1 publishes → notify the user → **FE2 plays Days 0-8** (send FE2 the commit + sha256) → findings page.
IM1 trial-merges all pieces as they land (latest local r7 41e9a420: arrows-c + breakfast-back + dinner-spread merge cleanly, build-table rows only).
ETA told to the user: 0.92.0 live ~08:00-10:00 UTC.

## Still switched OFF after 0.92.0 (remind the user)
- **Controller** (PAD_ON false). claude/controller dcdfe944 (follow-up 1: 3-mess-1 seat + Lift/ladder fix, RV9 PASS) is in 0.92.0's base, off. Open before any switch-on: CTT3's full reach sweep (running); 21 of 44 mess seats not offered from beside them (cause not proven). CP1 stopped (plans/handover-cp1.md on claude/controller-p1).
- **Crossing the Line** (EV_LINE_ON false): needs one check against the new dinner/tradition timing (dinner-spread) before switch-on; a couple of hours; suggested for the build after 0.92.0.

## Seats (session ids)
- Build master BM14 session_016mhGtsCxEgPCFn9C767yjq (~50%; handover section written). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg.
- Runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk (all idle, low memory).
- Assembly: **AC3** session_01DiLRzrXgkeoAZCoX1mVJn9 (owns claude/arrows-c). IM1 session_01PL57XDQC6t5hx7NtJ1pDMo (trial merges, ~44%).
- Builders: DS1 session_01MZBSf7MZeb9C89wpoavLko (zeke-tour); SC1 session_01BBC5dx3LtPPiWkTdurPTmJ (breakfast-back, dinner-spread; ~62%, writing handover-sc1.md); FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (vent + mop); FX4 session_01BueJ4UzQkn8HcC1TXd1KrW (m7, Wait here; free after); FX5 session_01LGRr55ZQCd11PuqhJEn9Jj (tip-clear); FB1 session_01C12k89pPRvZ63JHS3C2e1a (test fix + guard; ~56%).
- Writers: ZW1 session_01QY7V7HVtAbiX64cyVKL1Am (Zeke words, done, standing by); PW1 session_01Kpg4fqV2FgfYYeGuQTU5NV (preview PDF; standing by for the 0.92.0 update).
- Reviewers: RV7 session_01RLTBGbbdRbUkKME189xL4k (arrows-c, FX3, the switch, the whole 0.92.0 merge; ~42%); RV8 session_01Q6uHYWus4ncyEgqWEYhJh5 (breakfast, dinner, FB1, tip-clear; ~55%, handover-rv8.md pushed); RV9 session_01E31oZQU7DFbZnh2BesWsnM (zeke-tour first, FX4; ~30%).
- Controller tests: CTT3 session_0197zJtQyLkNz6dxc3NgoNgy (reach sweep).
- Fresh eyes: **FE2** session_01FYu2AXA4x4P4x5XVC66Qcz (claude/fresh-eyes-2; harness ready; waits for 0.92.0's commit + sha; plays Days 0-8 as a new player at phone size).
- Stopped: AC2 (handover-ac2.md), CP1, CP4, SS1 (screenshots on claude/preview-shots b56676e), lead 29.

## Backlog added (lead 30)
- LEAD30-1/3: FB1's "tap within reach of a stop does the stop" and the lift line: a future stop placed beside a lift or door would be caught; FB1's bd291e4 tightens the lift line to the tap's line only.
- LEAD30-2: the "tap at the pin" rule reads the last screen tap's ray (FB1's guard bd291e4 addresses it).
- FX3: the head-scratcher's arrow never points at Fault notes; the lathe arrow always picks 5-make-1.
- A teaching arrow nicety noted by RV7: the pop-up queue planted fault "drop newest instead of oldest" not caught (minor).

## Gotchas
- Every branch carries the rollback revert 2cabe96b; breakfast came back by reverting that revert (SC1). Don't merge claude/patch-play1-f directly.
- The repo's .gitignore ignores *.png: screenshots must be pushed as .jpg (SS1 lost its first push to this).
- Messages cross constantly; resend decisions if a seat asks again; use "now" for scope changes.
- arrows_check's follower uses real taps; many "stucks" were the follower, not the game: always ask for a real-tap repro before calling something a game bug (FX3's 32/32 pin check, FX4's m6 case).
- People near a stop take taps (tapCrew is generous): FX3's fix makes the job win when the floor under the finger is your job's stop.
- Day 0 timing: a new game arrives 17:15 (was 16:30); the dinner table ~18:15-18:20 with the clock hold.
