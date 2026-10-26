# Handover: RV22 (reviewer: vessel, ending checks, B3 M20 shoulds), 2026-10-26 ~23:45 UTC

**Role:** reviewer, replacing RV21. Lead: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). My session:
session_011wAn842cKDVWvoH8Cr9geD. Notes-only branch `claude/review-rv22` (from claude/review-rv21 aa8bce7b); log in
plans/review-rv22.md. Never change the game or push to builders' branches. Stopped at the user's stopping point (lead 40)
before any review started: **no verdicts given.**

Read first: plans/handover-rv21.md (how to test, probes in plans/rv21-shots/, gotchas, user answers C1-C3 and Q1-Q3)
and the verdict table in plans/review-rv21.md.

## Queue (nothing started)
1. **VB1 (session_01UsjGN26E88zwrNPWwef4iT), claude/vessel 5578c78d is ready for review** (sent ~23:50). 85f07071: RV21's
   V-2 shoulds (ramp crowd = gathering vesselArrival k 360, ~20, rampCrowd bubbles; Taavek's goodbye notice+arrow from
   14:30 at the ramp's foot, Tern waits to 15:30, Calder fetches 15:00; round-one fallback, Taavek brings it 12:45, notice
   13:00; Saturday vesselFetch 10:00/11:30; pilot toast once; setTimeout -> simTimeout); VB2's 3fb8eac7 merged (ed8b5787).
   cdf2685f: goodbye arrow; **a one-line hook in 24j's shopTap (lathe/fabricator tap does the making step: 24j's owner
   must review)**; arrows_check vessel part. 72b5f9dd: controller_check vessel part (the four presets).
   VB1 reports: check_fast OK, cadet off ALL IDENTICAL vs vessel-sky; on an ON copy events_check vessel, bigevents,
   day_check 28/29, arrows_check vessel, controller_check vessel OK. **Not yet run by VB1:** arrows teachoff and senior,
   day_check 27/30 on the latest copy, join_check, interactions_check. Reviewer: re-run all of these, cadet off vs its
   base, events_check (known-old FX24-2 only), and play the beats at 390x844 (RV21's probes v2_probe.py, v34_probe.py,
   vsky_bow.py).
2. **VB2 (session_01KRBGtugjBpv5iGcV5WDvCP), claude/ending-checks** (c0b800b8 = WIP at the stopping point, not for verdict; see plans/handover-vb2.md there). At ~23:36
   VB2 said: stay path (asis, teachoff, track) passes; change-of-mind, go runs and controller_check `ending` still in
   trial; will send the sha, then day_check 31/50 ON copy. Review: arrows_check endstay/endgo, controller presets (Days
   32, 34, 35, 36), day_check 31/50 ON copy, any game fixes on top of d1a61402 (cadet off identical vs d1a61402).
3. **B3 (session_014FBmsiTsA9QymoN2qt4NyL), claude/p5s5-m20 989b1759 is ready for review** (sent ~23:44; row 0.93.4-ar.4,
   DEV_NOTES "The sensor array, M20", plans/handover-b3-m20.md; B3 reports cadet off identical vs f57afcbc, check_fast OK,
   mech_check m19/m20/wstap and controller_check m19/m20 OK on an auto-switched copy, ladder order merged). Verify: m20 check parts run on an ON copy (not
   "not yet"); one teacher name (Calder teaches Day 19, Mori is off); no doubled Tracked row; in person before the 06:20
   Mail; recheck the Day 19 opening after the ladder-order merge deefa61a.

All three builders and lead 40 know RV22 is their reviewer; a successor should tell them its own session id.

## Setup done in this container (lost when it ends)
/tmp/cadet-work and /tmp/cadet-work2 per testing-guide section 2 (three r128, acorn 8.12.1, playwright).

## Open questions for the user
None.
