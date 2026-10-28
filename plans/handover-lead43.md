# Handover: lead 43

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-43** from "LEAD 43 started" (every line after). Also plans/overnight-decisions-lead42.md (decisions 1-18, overnight and day).
Lead 43 = session_01GKuymjoDoY2kA9yCK12NG1, branch claude/lead-43, hourly check-in **trig_016hWJy9BqDVX2tpcnNbzTdR** (57 * * * *): make your own (copy its prompt, renamed) and tell lead 43 its id so lead 43 disables its own.

## State (last update ~13:02 UTC Oct 28 = 9:02 AM ET)
- **0.95.0 LIVE**: Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU v2, Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m v2. Never publish over 6daN. claude/integration = b5199dc3.
- **0.96.0 (claude/staging-pad, BM20)**: controller waves A+B+C merged (e01bcee, cadet identical, controller_check 57 OK). To add: EV1 visit-on (claude/visit-on; RV25 reviewing; lead calls: the visit's jobs earn xp at the player's tier, Day 17 evening traditions pause kept; EV1 final checks running), then sound update claude/sound-r3 tip e748f560 (T1-T4 PASS; 667ad05e room B chime + r3_copy switch-on fixes 451e00e5/e748f560 with RV25), then switch-on turn: PAD_ON true AND SND_R3_ON true (the user: sound ON when published), sweep both off lines, build 0.96.0 -> FULL round (BM20 + 4 runners; AS1 = R1 ready; hire 3 fresh). reach sweep = non-blocking extra (PB1 cap fix claude/pad-reach-fix). Publish only after the user's OK + their real-controller save-file test (plans/pad-device-tests.md).
- **Dev mode**: trunk claude/devmode-j0 2b88ad2 (J0, J1, J3 PASS). J4 c7489b5 with RV25: on PASS fast-forward trunk (git push origin c7489b5:refs/heads/claude/devmode-j0). J2 (ship events incl. visit jumps) + J5 (notes + round) -> hire DM2 from plans/handover-dm1.md (on claude/devmode-j4) once visit-on passes. Then into staging after 0.96.0 (0.97.0).
- Pages: Round 3 https://claude.ai/artifact/CzoYwmjJgVZoYDm2S1QTYs, Mess hall https://claude.ai/artifact/11WXFue17xQsVrShWejD21, Dev mode plan https://claude.ai/artifact/X2GVBU4c5hZdt1R3dNxqy4, balance report https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm (no balance fixes until the user answers).

## THE USER'S RULES TODAY
- Cap stays 5 helpers actively working (asked 09:41 UTC: "Keep 5").
- Order: 0.96.0 (controller + visit) round -> Dev mode -> sound; Dev mode and sound building already started (the user, 09:47 UTC).
- Push notifications for questions and milestones. Times in US Eastern. No emojis. Plain words.

## Seats
- BM20 build master session_01GKuymiwDEgkwGmjJ2nokvg (~18%), staging-pad. Merges only on lead's word; sometimes goes quiet on long checks: ask for progress lines.
- RV25 reviewer session_01GKuymnnpKvNH4Ki69KEzwG (RV24 archived). Priority visit-on > sound > Dev mode.
- EV1 events session_01GKuymmJANJaZkFuhsM9bBt (claude/visit-on).
- DM1 Dev mode session_01GKuymkR7Z42FfTQyt2VWe3 (~60%, handed over, idle; archive after J4 PASS).
- SD3 sound session_01GKuymir9eBj7X6kLtwLRmq (~22%): r3_copy fix + SND_R3_ON-on sweep.
- Idle: AS1 session_01GKuymmdgtDvbd8P7URXd4z (R1 for the round), PB1 session_01GKuymjKdckiLtUUUNFvMdu (reach sweep still running on b33d894; archive after it reports), W8, DA6, N6, BAL1, PUB2 session_01GKuymkDxLVyt4rjtcJxdab (publisher).
- Archived today: R2-R5, BM19, CA1, PA1, SD2, lead 42 idle.

## Backlog added today
PB1-1 birthday cake can't be tapped (touch too; tap box inside the table's). PB1-2 controller_check ring_and_A reads a stale list. DM1-1 Set career re-set wipes milestones (fixed in J0). DM1-2 clockLog survives New game in same page. DM1-3 first run in a page differs (storm bridgeHungry). SD2-1 fixed.

## Gotchas
- Check that each "on" switch really runs the feature (the visit was "on" for days but a draft flag skipped it; events_check forced the flag).
- Waves' check parts all append to controller_check.py: merges conflict there; keep both.
- controller_check idle flake fixed (CA1 e139f74a, toast class).

## Handover moment (13:02 UTC)
Lead 43 at ~53% memory, handing over before the 0.96.0 switch-on + full round (a big task). Next steps for lead 44: (1) RV25 visit-on PASS -> GO BM20 merge visit-on; (2) RV25 sound PASS (667ad05e + e748f560) -> GO BM20 merge sound-r3; (3) GO BM20 switch-on turn (PAD_ON + SND_R3_ON true, build 0.96.0) and the full round: BM20 + AS1 + hire 3 fresh runners (cap 5: other seats idle during the round); (4) RV25 J4 PASS -> fast-forward claude/devmode-j0 to c7489b5; hire DM2 for J2 + J5 after the round frees seats; (5) when the round is green: PushNotification to the user; publish only after their OK + controller save-file test (PUB2 publishes over 7hQ1/KEya, never 6daN). Decisions log: plans/overnight-decisions-lead42.md rows 1-21.
