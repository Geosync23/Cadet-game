# Handover: lead 33 → lead 34

## START HERE (lead 34)
1. Read CLAUDE.md, this note, plans/patch-0.92.4.md, then the bottom of TEAM.md on claude/lead-33 (from "~04:02 UTC: LEAD 33 took over").
2. Branch: start `claude/lead-34` from `claude/lead-33`. Push only there (integration moves only with the user's OK or by the build master on the lead's go).
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session, minute 57), then disable lead 33's trig_01VnX1r7j3qP6ebfWP2v6kZJ.
4. Message every working seat with your session id (use priority "next", NOT "now": "now" interrupts in-flight tool calls and BM16 read the interruption as "the user said STOP" and froze for 2.5 h). Tell lead 33 (session_014VXwRc3QfqM3cgp1w6VJah) you've taken over.
5. The user is AWAKE (overnight mode over, from ~14:00 UTC 10-24). Times in US Eastern (EDT, UTC-4), plain words, no emojis, few messages.

Lead 33 = session_014VXwRc3QfqM3cgp1w6VJah, branch claude/lead-33; took over 2026-10-24 04:02 UTC; handed over ~15:00 UTC at ~75% memory.

## Done under lead 33
- **0.92.3 PUBLISHED** 12:34 UTC (8:34 AM Eastern): all 29 playtest notes (plans/patch-0.92.3.md). From claude/staging-0.92.3 d9a387b6 (records 3866c8f3), game sha256 f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853. **NEW pages (the user wanted new links to keep their save):** Playtest https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ, Dev https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr (PUB1 sources in its scratchpad play-0.92.3/, dev-0.92.3/). Old Version 11 (0.92.2) pages untouched: Wn6mUGcxatoWVqhCNTa1vs, 6daNCLCJAcsLCZn27CEthq.
- claude/integration and claude/integration-next = 3866c8f3 (user OK, 14:05 UTC).
- Round 1 found mech_check m3d (stale "Clock in" arrow after 12:30): AC3 fix 4928271f (help only 08:00-12:30), RV12 PASS; round 2 all six OK.
- Backlog 15 (arrows week guide m6) was a TEST gap: FX10's FOLLOW fix b75dcf81 (in). arrows_check `week guide` now in CR1's share.

## In progress: 0.92.4 (plans/patch-0.92.4.md; base claude/integration 3866c8f3)
- A trays (FX12 session_01DfkfrfvdT2bW2Q1Y7b2AA5 → RV12 session_013JmdoWWEDQde8y1bwrMGnY): tray goes away on get-up and when leaving the mess unseated; only pick-your-own travels. Update design-doc.
- B dirty clothes (FX4 session_01BueJ4UzQkn8HcC1TXd1KrW, ~57% → RV11 session_01EdBKAgQFMexMSs3JbgH5H7): keep new tip, drop old pop-up, add a next-day reminder.
- C crew stand-up hop smoothing (FX8 session_01GQ33Xh5J5WxwXieiWPwPq1 → RV11).
- D warn when a repair's part runs past a lesson start (FX10 session_01Sb2kaWj2xPBRQC4o7FkLSo → RV13 session_016ioWtxM6NJRV4Ck3ADwozc).
- BM16 session_01MB7n4yvCAeGyWN4WZCAGPh (~22%) stages claude/staging-0.92.4, then six-runner round (OLD 3866c8f3). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg publishes; ask the user whether 0.92.4 updates the 0.92.3 NEW pages (default) or gets new links again.
- Runners CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk.

## Waiting on the user
- Needs pace: the user is testing and will report (now a normal day needs gym + call home + three chats to stay above 30).
- Sim bay plan: https://claude.ai/artifact/Hmg44se58wGkZaGCMFyRWL (FX14 session_01LHwo6kgrymCA7rBdacbqXe idle).
- Crew stories go in later, separately (claude/crew-stories-pitch 9e95786b; reading page https://claude.ai/artifact/2MdTVzoD5J1ectdZb1zqf5). Controller still off.
- The user approved: bedtime tip wording, pick-your-own toast, dinner heads-up waiting behind the beam strip.

## Idle seats (memory)
BM15 (~71%, done; handover plans/handover-bm15.md), AC3 (~70%, done), DS1 30%, DV1 40%, FX9 10%, FX11 30%, FX13 25%, writers CS1/SW1/SW2/SW3/ZW1, lead 32.

## Small backlog for 0.92.4+ (not started)
FX8 typeof guard nit in interactions_check; the cancelled/withdrawn FX11-1 (not a bug).

## Gotchas
- Never send priority "now" to a seat mid-task (see step 4).
- Split shares between runners crossed once: let the runner who owns the share decide, the BM confirms.
- Game-file change after a round = fresh full round (user rule). Test-only fix = re-run the affected check.
