# Handover: RV22 (reviewer: vessel, ending checks, Step 5 items), 2026-10-27 ~03:10 UTC

**Role:** reviewer, replaced RV21 and took RV20's last item. Lead: lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). My
session: session_011wAn842cKDVWvoH8Cr9geD. Notes-only branch `claude/review-rv22`; full log and verdict table:
`plans/review-rv22.md`. Never change the game or push to builders' branches. Stopped because the user is moving the
project to another account (lead 40, ~03:00 UTC).

Read first: plans/handover-rv21.md (how RV21 tested, user answers C1-C3 / Q1-Q3), then the verdict table in
plans/review-rv22.md. User rules for every verdict: works with a game controller; tons of arrows, super obvious
progression; key moments are staged scenes with dialogue; phones first; NEW (lead 40, 2026-10-27): everything ships
ON, so the checks on a switched-on copy are the ones that count.

## Verdicts given
| Branch | Verdict | Sha |
|---|---|---|
| claude/p5s5-promo (B5) machine_check fix + RV20 S1-S4 | PASS (its should fixed next) | f00d93c1 |
| claude/p5s5-promo (B5) the should (friends' Mail at 12:30) | PASS | c3d36cde |
| claude/p5s5-m20 (B3) RV21's shoulds + turn arrow | PASS | 247420aa |
| claude/vessel (VB1) | FIXES NEEDED (bigevents, day 28) | 5578c78d |
| claude/vessel (VB1) | FIXES NEEDED (1 must: round-one fetch; 2 shoulds) | 0340b6f9 |
| 24j hook vesselShopTap in shopTap (no E3 seat; lead 40 asked me) | OK | 5578c78d on |
| claude/ending-checks (VB2) arrows endstay/endgo + controller ending | PASS on what I re-ran (below) | 571b0737 |
| claude/train-titles (B3) | PASS (GitHub quick check on 7ce89d56 was still running at the move: confirm it's green) | 7ce89d56 |

## Open items (exact state)
1. **VB1 claude/vessel 705c6fc5 (handover-only head 03b63d95): NOT reviewed** (lead 40: leave for the next account). It answers my 0340b6f9 verdict:
   roundFetch 12:30 (Taavek waits at the bench, then comes to you), vesselNear 6 m while fetching, vesselFetchTick
   (words on arrival or within 6 m), sheet arrows dropped while the round one is pending, ring.roundFind. Diff read only:
   looks right. Possible should: VESSEL_FETCH isn't saved, so a reload mid-fetch leaves the flag set, reach 3.2, Taavek
   back to their plan. VB1 reports on 705c6fc5 (handover 03b63d95): arrows vessel OK, controller vessel OK, cadet off
   vs 0340b6f9 ALL IDENTICAL, check_fast OK. To run on it (vessel ON copy: sed the `EV_VESSEL_ON = URL_FLAGS.has('evvessel')` line to `true`):
   cadet_test 3fb8eac7 vs 705c6fc5 (off), events_check (known-old FX24-2 only), arrows_check vessel, day_check 28,
   and the phone play `plans/rv22-shots/vb1_play.py <wt>/starship-cadet.html <outdir> main` (stands in the bow lounge;
   check Saturday Calder's words + sheet scene, Sunday 12:30 Taavek's words + round-one scene, Monday goodbye).
   Everything else on the vessel passed on 0340b6f9 (bigevents, day 27-30, controller vessel, arrows teachoff/senior,
   join/interactions by VB1). VB1's day_check edit (Works tea excuses an eventMeetTag in the tea hour): reviewed OK.
2. **B3 claude/talk-close f52e2abc: NOT reviewed** (lead 40: leave). From staging-0.94.0 ac810e7e; the user's "talk only up
   close" (TALK_NEAR 2.5 tiles, Walk over); section 20 chatOpen/chatShow/chatDo/chatTick far mode (the social
   engineer's hooks), section 10 tapCrew. No switch. Check: cadet, player_check, interactions, arrows week guide,
   controller pick/promo3/day/ending, and that the ending's goodbyes (VB2's controller ending: walk up within 1.8) and
   the vessel's taps (vesselTap through tradJoinTap) still work.
3. **VB2 claude/ending-checks 571b0737**: my re-runs passed (controller ending OK in full; arrows endstay x4 and endgo asis
   to Day 36 with no FAIL). Not re-run by me: endgo teachoff/track (VB2: OK), day_check 31/50 on an ending-ON copy
   (VB2: OK), and VB2's controller ending on staging (B3 saw 4 FAILs there on ac810e7e: Day 34 ring None for pell,
   Monday goodbye, end page). Every arrows run prints "stuck 1": ask VB2/its successor what that counts. With talk-close
   merged, re-run controller ending (goodbyes are by walking up within 1.8).
4. B5's S1-S4 and machine_check fix: done. B3's S5-4 98460d79: not mine (B3 asked lead 40 who re-checks it).

## How I test
Setup per plans/testing-guide.md section 2 in /tmp/cadet-work and /tmp/cadet-work2 (two lanes, at most 2 browsers).
Worktrees per sha under /tmp/rv22/wt-<sha>. Queues as one background bash script per lane. cadet_test beside another
check can show "max 1" renderer noise: rerun alone (it went to ALL IDENTICAL every time). Probes: plans/rv22-shots/
(vb1_play.py, m20_live2.py) and plans/rv21-shots/. In a probe never name a global HOOK, run, D etc. that cadet_test's
exec defines (HOOK broke my first probe); a page needs `#dev` for devmodeRun. A probe's player dropped in the lift car
('@') has no free places for crewComeTo: stand them in a room.

## Open questions for the user
None from me.
