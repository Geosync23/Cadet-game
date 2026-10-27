# Review log: RV22 (vessel + ending reviewer, replacing RV21)

**Role:** reviewer for "A Veyli vessel needs help" (EV_VESSEL_ON), the ending's checks (EV_ENDING_ON) and B3's M20
shoulds. Lead: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). Notes-only branch `claude/review-rv22` (from
claude/review-rv21 aa8bce7b); I never change the game or push to builders' branches. RV21's full log and verdicts:
plans/review-rv21.md. Verdicts PASS / FIXES NEEDED (must/should) with the exact sha to the builder and lead 40.

**Builders:** VB1 session_01UsjGN26E88zwrNPWwef4iT (claude/vessel), VB2 session_01KRBGtugjBpv5iGcV5WDvCP
(claude/ending-checks on d1a61402), B3 session_014FBmsiTsA9QymoN2qt4NyL (claude/p5s5-m20).

## Queue
1. VB1's next claude/vessel push (now 5f199dd4, handover only): RV21's open shoulds, VB2's 3fb8eac7 merge, arrows_check
   vessel part, controller presets. Re-run bigevents, events, day_check 27-30 on an ON copy; cadet off identical; phone.
2. VB2's claude/ending-checks (not pushed yet): arrows_check endstay/endgo, controller presets, day_check 31/50 ON copy.
3. B3's claude/p5s5-m20 after f57afcbc: m20 checks on an ON copy, teacher name, Tracked row, in person before 06:20 Mail.

## Verdicts
| Branch | Piece | Verdict | Sha |
|---|---|---|---|
| claude/p5s5-promo (B5) | machine_check fix (RV20 M1) | FIXES NEEDED (1 must: mid-line comment kills the sort) | cbca3e3e |
| claude/p5s5-promo (B5) | machine_check fix + RV20 S1-S4 | PASS (1 should: friends' Mail future-dated) | f00d93c1 |
| claude/p5s5-promo (B5) | the should | PASS | c3d36cde |
| claude/vessel (VB1) | RV21's shoulds, VB2 merge, arrows/controller parts | FIXES NEEDED (bigevents, day 28) | 5578c78d |
| claude/vessel (VB1) | the fixes | FIXES NEEDED (1 must: round-one fetch never starts the scene; 2 shoulds) | 0340b6f9 |
| claude/p5s5-m20 (B3) | RV21's 4 shoulds + the turn arrow | PASS | 247420aa |

## Log
- 2026-10-26 ~23:30 UTC: started; told lead 40, VB1, VB2, B3. Test kit in /tmp/cadet-work and /tmp/cadet-work2. No new
  pushes on the three branches yet.
- ~23:36 UTC: VB2: ending-checks not pushed; stay path (asis, teachoff, track) passing locally; change-of-mind, go runs and
  controller_check `ending` still in trial. Will send the sha, then day_check 31/50 ON copy.
- ~23:45 UTC: lead 40: stopping point (the user's call). No review started; wrote plans/handover-rv22.md.
- ~23:43 UTC: VB2 at stopping point: claude/ending-checks c0b800b8 is marked WIP (not for verdict); plans/handover-vb2.md there.
- ~23:45 UTC: B3 sent claude/p5s5-m20 989b1759 (the 4 shoulds). Not reviewed: stopping point. Noted in the handover.
- ~23:50 UTC: VB1 sent claude/vessel 5578c78d (shoulds, VB2 merge, arrows + controller vessel parts). Not reviewed: stopping point. In the handover.
- 00:36 UTC (10-27): VB2 final WIP 6fe92ead on claude/ending-checks (test only, not for verdict). In the handover.
- 01:00 UTC (10-27): lead 40: back to work. NEW USER RULE: everything ships ON. Queue: VB1 claude/vessel 5578c78d (re-review
  from 85f07071), then B3 claude/p5s5-m20 989b1759, then VB2's ending fixes.
- VB1 5578c78d: cadet_test 3fb8eac7 (vessel-sky) vs 5578c78d, vessel off: ALL IDENTICAL. Running: events_check, day_check
  27-30 (ON copy), bigevents (ON copy), arrows_check vessel (+teachoff, +senior), controller_check vessel. Code read of
  ed8b5787..5578c78d: shoulds look done (vesselFetch for Saturday/round one/home, leaveBy 930, VESSEL_TERN_SAID,
  vesselArrival k 360, simTimeout x7). Word note: talk.homeFind "So's Isak, on his day off" genders Isak (crew text uses
  they for Isak; no canon pronoun).
- B3 989b1759 code read: arrOffer through 24f's existing WORK_MECH[].offer hook (no shared change). To check in play:
  with an offer, 24 core's T3 board arrow (guide 'train:m20:do') is skipped for m20 (line ~17335): is your turn still led?
  Stale comment at WORK_MECH.m20.at ("Mori comes in for it all the same (arrHost books her)").
- Lead 40: no E3 seat; I review VB1's 24j hook myself. **24j hook (shopTap -> vesselShopTap): OK.** Fires only when
  vesselNow() is the running veyliVessel (impossible with the switch off; `typeof` guard too), on Monday (k 2), on a lathe
  or fabricator (shopMachineOf), after Calder's job and the helpers (step 1-5) and before the part (made by you, or by the
  helpers at 13:25: bounded). Every other shop tap falls through unchanged. Should (words): the wrong-machine toast says
  "at the bench" for the fabricator.
- bigevents on the ON copy of 5578c78d: **FAILED** (vesselArrival 0 places for 20-31 people; vesselRamp cast calder/zeke/isak not planned at 09:30). Sent to VB1 + lead 40 as a MUST at once.
- 00:46 UTC: lead 40: RV20 handing over; I also take B5's machine_check fix on claude/p5s5-promo (B5
  session_01CgbXRamJJp66pFTP43KYoB; recipe plans/handover-rv20.md on claude/review-rv20). Order: VB1, B5 fix, B3, VB2.
  B5 head now 516333a1 (fix not landed).
  Note from RV20: B3's branch carries 51b1a9c6 (the ladder order that breaks machine_check 'traced faults ... the same twice' on a P5_STEP5 copy): B3's machine_check on an ON copy will fail until B5's fix is merged in.
- 00:55 UTC: **B5 claude/p5s5-promo cbca3e3e: FIXES NEEDED (1 must)**, from the diff: ladderBigP5's new comment is mid-line,
  so `.map().sort().map()` (the higher-tier-first order) is commented out; still parses. Sent to B5 + lead 40.
- VB1 5578c78d on the ON copy: arrows_check vessel OK; controller_check vessel OK.
- 00:59 UTC: B3 now asks for claude/p5s5-m20 **247420aa** (arrTurn: level 2 'Your turn' board arrow for m20, the stale comment). B3 reports cadet vs 989b1759 'identical apart from renderer noise (1 level off)': must re-run myself (regressions must be pixel-identical).
- VB1 5578c78d ON copy: events_check only known-old FX24-2 (OK); day_check 27, 29, 30 OK; **day_check 28 FAILED** (work
  472-476/480 for 8; Works tea 13:00 on 7 went 0). Same two fails on 6d4b519's ON copy (476/480; tea 0): from V-3's chain,
  slightly worse with 85f07071's 09:15 standEasy. A MUST under the ON rule. Sent to VB1.
- B5 ea40ae51 (S1-S4 shoulds on cbca3e3e): the mid-line comment still there (line 59312). Reminded B5; review on the next sha.
- 01:35 UTC: B5 claude/p5s5-promo **f00d93c1** (comment moved; carries S1-S4 ea40ae51). Diff read: ladderBigP5's sort live
  again; S2 (no "reputation down" on a tier change, P5_STEP5 only), S3 (visitor chair words), S4 (Dev presets) fine.
  S1 should: the friends' Mail is sent at the promotion (~08:30) with `at` = 12:30, so it sits in the inbox at once,
  dated in the future (mailSend files it immediately; section 18 clamps such dates with Math.min(shipNow(), at)). Running:
  machine_check ON, promo_beats_check ON, cadet_test 5957d244 vs f00d93c1.
- 01:37 UTC: VB2 says claude/ending-checks is ready (571b073f, test only on d1a61402; arrows endstay/endgo 7 ways OK, controller ending OK, day 31/50 ON OK). Note to check: farewells in a crowd by walking up, not the pad ring. Queued after B3.
- **B5 f00d93c1: PASS (1 should).** machine_check ON: MACHINE CHECK OK, traced faults the same twice True; promo_beats ON OK
  (t3shoulds friends ['13:00','12:30'], no toasts, presets m15:17 m17:- m19:17); cadet 5957d244 vs f00d93c1 ALL
  IDENTICAL; GitHub quick check success. Should: friends' Mail filed at the promotion, dated 12:30 (future-dated).
  The same ladder fix must reach B2 deefa61a and B3 fa1e152c (lead 40 told).
- VB1 **0340b6f9** (df796cab venue/places; 0f53dd16 EV_MEET_TAGS + day_check tea excuse; 0340b6f9 my 3 notes): diff read OK
  (tea excuse narrow: only people with an eventMeetTag segment in the tea hour). Re-running on it.
- VB1 0340b6f9 re-runs: cadet 3fb8eac7 vs 0340b6f9 ALL IDENTICAL; day_check 28 ON OK (tea on 0 easy 7), 28 OFF OK (tea on 7
  went 5), 29 ON OK; events_check only known-old FX24-2. Running bigevents ON, arrows vessel, phone play.
- B5 c3d36cde (S1 fixed: puFriendsTick files the friends' Mail from 12:30 on the result day, dated then; T.res is set
  only by puPromote, so never on a fail). Running promo_beats ON.
- 02:10 UTC: **B5 c3d36cde PASS** (promo_beats ON OK, friends 12:31, early 0).
- **VB1 0340b6f9: FIXES NEEDED (1 must).** bigevents ON OK (108 places); arrows vessel OK; phone play (vb1_play.py, standing
  in the bow lounge): Calder fetched Saturday 10:00/11:30 but no bubble recorded (should); Sunday 12:45 Taavek fetched,
  stopped 4 m away, scene needs 3.2 m: nothing, "missed" at 13:00 (MUST; shot vessel-0340b6f9-roundone-fetch.png); the
  12:40 arrow was the sheet, not the round one (should). Ramp scene with Calder, Monday goodbye, Tern: good.
- 02:44 UTC: B3 asks for claude/talk-close f52e2abc (from staging-0.94.0 ac810e7e; talk only within TALK_NEAR 2.5 tiles, Walk over; section 20 + 10 tapCrew; no switch). Queued after B3 m20 and VB2. B3: controller_check ending 4 FAILs on staging ac810e7e (Day 34 ring None for pell; Monday goodbye, end page) with or without it.
- 02:55 UTC: **B3 247420aa PASS**: cadet f57afcbc vs 247420aa alone ALL IDENTICAL (beside another check: f/g/h max-1 noise); mech_check m20 wstap m19 OK; controller m19 m20 OK; live Day 19 (probe m20_live2.py) Calder teaches, one row, notice+Mail 09:30, turn arrow from 10:13.
- 02:55 UTC: VB1 **705c6fc5** (the must + 2 shoulds): diff read OK (roundFetch 12:30, Taavek waits at the bench till then; vesselNear 6 m while fetching; vesselFetchTick says the words on arrival or within 6 m; sheet arrows dropped while the round one is pending). Possible should: VESSEL_FETCH is not saved: a reload mid-fetch leaves the flag set, reach back to 3.2, Taavek back to their plan. To run: cadet off, events, arrows vessel, phone play.
