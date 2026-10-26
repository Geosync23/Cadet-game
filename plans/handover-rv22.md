# Handover: RV22 (reviewer: vessel, ending checks, B3 M20 shoulds), 2026-10-26 ~23:45 UTC

**Role:** reviewer, replacing RV21. Lead: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). My session:
session_011wAn842cKDVWvoH8Cr9geD. Notes-only branch `claude/review-rv22` (from claude/review-rv21 aa8bce7b); log in
plans/review-rv22.md. Never change the game or push to builders' branches. Stopped at the user's stopping point (lead 40)
before any review started: **no verdicts given.**

Read first: plans/handover-rv21.md (how to test, probes in plans/rv21-shots/, gotchas, user answers C1-C3 and Q1-Q3)
and the verdict table in plans/review-rv21.md.

## Queue (nothing started)
1. **VB1 (session_01UsjGN26E88zwrNPWwef4iT), claude/vessel:** head 5f199dd4 is only VB1's handover (plans/handover-vb1.md,
   written 22:39, so a successor may push instead). Review the next push: RV21's open shoulds (no crowd at the ramp /
   talk.rampCrowd unused; Taavek's goodbye arrow only from 14:45; round-one fallback; Saturday sheet: Calder comes to
   you; doubled pilot toast; setTimeout x7 -> simTimeout), VB2's claude/vessel-sky 3fb8eac7 merged, arrows_check vessel
   part, controller presets (Day 27 10:00, Day 28 09:25/12:55, Day 29 09:15). Re-run cadet off vs base, events_check
   (known-old FX24-2 only), bigevents on an ON copy, day_check 27-30 ON copy, phone play 390x844.
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
