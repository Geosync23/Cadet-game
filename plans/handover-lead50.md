# Handover: lead 50 (session_01GKuymmoEriV3ugms2s3hsn), written 2026-11-07 ~03:10 UTC (Nov 6 10:10 PM ET)

## Where things stand
- **0.99.8 LIVE** (published on the user's OK, 2026-11-07 ~02:07 / 03:05 UTC):
  Playtest https://claude.ai/artifact/2Uyqpm6jS9dvUW4ML7mb5H (slug 0c01401d..., v4 = 1794017247-ce65, sha ee526932...8b8e),
  Dev https://claude.ai/artifact/JftiS793gzEPhKRekatcon (slug 8f197d97..., v4 = 1794020745-9bb9, sha b3f4b574...7b70).
  Game 13681748...59fd3 = claude/staging-0998 33c737b; claude/integration = main = 33c737b (fast-forwarded).
  Phone test (tools/publish/phone.js on claude/publish-pub3, needs the __sc hook injected in a test copy and three@0.128
  build/three.min.js): Playtest and Dev both build 0.99.8, sign-on, HUD, Saves (download/load), Dev jump tab, 0 errors.
  Note: with no save the Playtest title goes straight to the sign-on form, so run phone.js with a tag not starting "play".
- 0.99.7 was never published on its own (FINAL GO BM26, round 0997b, staging-0997 1baafc1); 0.99.8 = 0.99.7 + TP1's
  Day 2 Leila arrow (TP998_ARROW_ON) + one call home a day (TP998_BOOTH_ON) + Social marker/words after the call.
- Records: plans/round-0997.md (A-O), plans/round-0998.md (P), plans/patch-0997.md, plans/patch-0998.md, TEAM.md.

## Backlog from today (not in 0.99.8)
TP1-1 shutdown 'quiet' booking can land on your night-shift check-in (old, 24w). Week 1 career pace: a steady Senior
one xp short of Trusted on Day 19 (check margin added; tune if the user wants). tp998.social.1 unused words.

## Seats
All idle. BM27 session_01GKuymjy5t3QwM8whGj2QFE (fresh). Runners R1 ..mnpcUSBmpZYiDK67GH, R2 ..mmnJnzWMxP769P9Edd,
R3 ..o7sJwyufjkoEsCacB, R4 ..mmvXPrmsnyaH858XoJ, R6 ..jS1cBK12RvWv7L5ka. Builders TP1, CR1 (near 60%), SC1 (stood down),
MV1, EV1, GM1, CL1, JB3, TB6 (handovers on their branches). BM26 stood down.
Hourly check-in trig_01AaVWouC3y6e8wSuSepXfoB paused.

## Lessons
- Fixers' branches carry stale check files: always run the staging tree's checks on the merged file.
- A game change after a GO means a full round (user's rule): batch fixes, let the running round finish first.
- Check-only fixes ride along without a new round; freeze the candidate before the GO.
