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
