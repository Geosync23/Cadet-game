# Handover: lead 43

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-43** from "LEAD 43 started" (every line after). Also plans/overnight-decisions-lead42.md (decisions 1-18, overnight and day).
Lead 43 = session_01GKuymjoDoY2kA9yCK12NG1, branch claude/lead-43, hourly check-in **trig_016hWJy9BqDVX2tpcnNbzTdR** (57 * * * *): make your own (copy its prompt, renamed) and tell lead 43 its id so lead 43 disables its own.

## State (keep this section current; last update ~10:58 UTC Oct 28 = 6:58 AM ET)
- **0.95.0 LIVE**: Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU v2, Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m v2. Never publish over 6daN (the user's save). claude/integration = b5199dc3 (0.95.0; the user's OK).
- **0.96.0 (claude/staging-pad, BM20)** = controller update (waves A, C merged at e158dcf; B merged locally e01bcee, pushing) + the Diplomatic visit really running (EV1, claude/visit-on, in checks; it never ran: SHIP_EVENTS.diplomatic draft: true) + PAD_ON true (switch-on turn, sweep per plans/controller-audit.md section 4) -> FULL round (BM20 + 4 runners; AS1 ready as R1; hire 3 fresh at the gate). Publish only after the user's OK AND their real-controller save-file test (plans/pad-device-tests.md, the user "will soon").
- **Dev mode update** (DM1, plan v4.4 https://claude.ai/artifact/X2GVBU4c5hZdt1R3dNxqy4, the user's answers: full plan ~50 jumps / ~24 h): trunk claude/devmode-j0 (J0 PASS eef5b56); J1 claude/devmode-j1 d9b7b3c in review; DM1 on J3 (ending + traditions); J2 ship events waits for visit-on; J4 arrow last. BM20 takes the whole Dev mode update into staging after the 0.96.0 round.
- **Sound update** (SD3, claude/sound-r3, SND_R3_ON off; plan plans/sound/r3-build-plan.md): T1 event music PASS (64077a69 + farewell A dc3014b6 PASS); T2 mess hall a09b32b7 and T3 watcher FX f58803b1 in review; T4 six hook lines in progress. All Round 3 picks in (design-doc Sound): room B door C (told in chat; the page save failed), test fit B, farewell A (page answer later than chat B), shop none. Mess hall: D without voices + "warm" voices, scaled by people, silent when empty (alone = silent: lead call, told the user).
- Pages: Round 3 https://claude.ai/artifact/CzoYwmjJgVZoYDm2S1QTYs, Mess hall https://claude.ai/artifact/11WXFue17xQsVrShWejD21, balance report https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm (NO balance fixes until the user answers).

## THE USER'S RULES TODAY
- Cap stays 5 helpers actively working (asked 09:41 UTC: "Keep 5").
- Order: 0.96.0 (controller + visit) round -> Dev mode -> sound; Dev mode and sound building already started (the user, 09:47 UTC).
- Push notifications for questions and milestones. Times in US Eastern. No emojis. Plain words.

## Seats
- BM20 build master session_01GKuymiwDEgkwGmjJ2nokvg (~18%), staging-pad. Merges only on lead's word; sometimes goes quiet on long checks: ask for progress lines.
- RV24 reviewer session_01GKuymnJuoJTWnmYunbN7EP (~51%): priority EV1 > Dev mode > sound. Hire RV25 at ~60%.
- EV1 events session_01GKuymmJANJaZkFuhsM9bBt (claude/visit-on).
- DM1 Dev mode session_01GKuymkR7Z42FfTQyt2VWe3 (~40%).
- SD3 sound session_01GKuymir9eBj7X6kLtwLRmq (~15%).
- Idle: AS1 session_01GKuymmdgtDvbd8P7URXd4z (R1 for the round), PB1 session_01GKuymjKdckiLtUUUNFvMdu (reach sweep still running on b33d894; archive after it reports), W8, DA6, N6, BAL1, PUB2 session_01GKuymkDxLVyt4rjtcJxdab (publisher).
- Archived today: R2-R5, BM19, CA1, PA1, SD2, lead 42 idle.

## Backlog added today
PB1-1 birthday cake can't be tapped (touch too; tap box inside the table's). PB1-2 controller_check ring_and_A reads a stale list. DM1-1 Set career re-set wipes milestones (fixed in J0). DM1-2 clockLog survives New game in same page. DM1-3 first run in a page differs (storm bridgeHungry). SD2-1 fixed.

## Gotchas
- Check that each "on" switch really runs the feature (the visit was "on" for days but a draft flag skipped it; events_check forced the flag).
- Waves' check parts all append to controller_check.py: merges conflict there; keep both.
- controller_check idle flake fixed (CA1 e139f74a, toast class).
