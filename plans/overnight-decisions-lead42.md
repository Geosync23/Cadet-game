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
| 4 | Who does the controller audit and builds? (lead 43) | CA1 audit seat first (read-only, waves), BM20 fresh build master on claude/staging-pad from b5199dc3; builders hired per the audit's waves (at most 3 + reviewer + BM20). | Lead 42's recommended shape; keeps the cap of 5. |
| 5 | Fold the two test-only check fixes (R3 88999f2, AS1 238c46d8) in now? | Yes, into claude/staging-pad first (game byte-identical). | Test only; needed for the controller round anyway. |
| 6 | Which "sound samples" for the morning report? (the user, 10:13 PM ET, did not say which) | One new page, Wren Sounds: Round 3 (SD2): tradition music samples (the held pick from 25 Oct), the Veyli farewell song, and A/B/C sounds for features added since the 0.93.0 sound build. Nothing into the game. | These are all the open sound items in plans/sound/audio-todo.md and handover-sound.md; the user can say if they meant something else. |
| 7 | Dev mode update | Off hold (the user, 10:13 PM ET): starts right after the controller update passes its round. | The user's words. |
| 8 | Sound for a pad-only player (audit Q1) | Start sound from the first pad press where the browser allows; a once-only note where it doesn't. | CA1's recommendation; a pad-only player otherwise hears nothing. |
| 9 | Time clock Undo with a pad (audit Q2) | Land on the close cross during the 5 s Undo window. | A double A press can't undo a punch by accident; keeps the touch layout. |
| 10 | Dev mode by pad (audit Q3) | Add the Dev card to the screen-edge buttons when #dev is in the link. | The user and testers use Dev mode. |
| 11 | On-screen keyboard for memos / Dev search (audit Q4) | No, leave as is. | About 4 hours; the user's earlier answer was about the name only. |
| 12 | Save file Download/Load from a pad (audit Q5) | Needs a test on the user's real controller before the switch-on goes live; wave C adds a one-line hint meanwhile. | Can't be tested headless; ask the user in the morning. |
| 13 | Wave C timing | After SD2's sound page is done (cap of 5). Merge order A, B, C. | Cap; C touches the sound section SD2 knows best. |
| 14 | Where should the Saves app land with a controller? (RV24 found it lands on Slot 2's New game) | On the slot you're playing (its Play/Continue, or the first safe choice); never another slot's New game. PA1, in wave A. | A first A press must never start a new game by accident. |
| 15 | Start anything on Dev mode before the controller passes? | Only the scope plan (a read-only plan page for the user to read in the morning); no building until the controller round is green. | Uses a free seat; every deck/feature starts with a reviewed plan page anyway. |
