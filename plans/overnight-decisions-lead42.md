# Overnight decisions: lead 42 -> lead 43 (night of Oct 27-28, 2026)

The user, ~02:03 UTC Oct 28 (10:03 PM Eastern): "Ok, for overnight mode let's jump forward to the controller update. Going to bed, night"

Overnight mode (as in plans/overnight-decisions-lead41.md): no questions to the user; the lead takes the recommended answer to every question and logs it in the table below, so the user can change it in the morning. Milestones still get a PushNotification (it waits on their phone). Cap: at most 5 seats actively working. Dev mode update stays ON HOLD (the user, 00:57 UTC). No balance fixes (the user hasn't answered the report).

## The controller update (the user's words, 27 Oct overnight-decisions-lead41: "make sure the controller support is current with all added features since it was made", then PAD_ON on)
Scope: audit EVERY panel, button, scene, job, card, app, setting and interaction added since controller support was made (0.9x builds through 0.95.0: Step 5, Step 6, the vessel, the ending, traditions/events, saves slots, the Works app tabs, the patch-E features switched on today: rank on crew cards, the time clock confirm + Undo, the storekeeper buy menu, etc.); the pad must reach and use all of them; controller_check covers each; then PAD_ON switched on (it's the last deliberately-off switch besides the cut ones).
Recommended shape (lead 42's call; change if the audit says otherwise):
1. An audit seat (CA1) reads the game + controller_check, lists every feature with pad status (works / partly / missing) into plans/controller-audit.md, proposes waves. No game change.
2. Builders by area (at most 3 at once + reviewer + build master = 5), each with controller_check parts; RV reviews; build master merges into a new staging branch from b5199dc3 (e.g. claude/staging-pad), everything behind PAD_ON until the switch-on turn.
3. Switch-on: PAD_ON true; sweep checks for its off line; full round (5 shares).
4. Publish: NOT overnight. Have it ready and green; publish in the morning after the user's OK (they will be playing 0.95.0 on those links).

## Decisions
| # | Question | Decision (recommended) | Why |
|---|---|---|---|
| 1 | Publish the controller update overnight? | No: build + full round overnight, publish after the user's OK in the morning. | The current links just got 0.95.0; the user should choose when PAD_ON reaches them. |
| 2 | Keep BM19 as build master? | Hire a fresh build master (BM20) from handover-bm19.md; archive BM19. | BM19 stalled twice tonight waiting for a human yes; memory ~50%+. |
| 3 | Dev mode update? | Stays on hold. | The user, 00:57 UTC. |
