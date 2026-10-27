# Handover: lead 42

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-42** from "LEAD 42 started" (every line after). Older: plans/handover-lead41.md, plans/overnight-decisions-lead41.md.
Lead 42 = session_01GKuymjnCHnpwDqB94PVwmV, branch claude/lead-42, hourly check-in **trig_016zcYSSwXEKiD4zNuLoL9p9** (53 * * * *): disable it when you take over and make your own (copy its prompt, renamed). Lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j) is idle; it is W8's parent and relays W8's messages if they go to it.

## State at writing (~21:55 UTC Oct 27 = 5:55 PM Eastern)
- **0.95.0 (Step 6 ON) final candidate 3**: claude/staging-p5s6 **b5199dc3**, game sha256 **b18d2b6487e71ba5...238a**. Contents: all of Step 6 (P5_STEP6 + 9 sub-switches), both live fixes (escort-follow-fix, team-turn-fix), DA6's night-2 arrow fix 673ac4f2, and the 3 patch-E features the user switched on today (RANK_CARD_ON, CLOCK_UNDO_ON, SHOP_MENU_ON). Off on purpose: TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, PAD_ON (controller project), END_WAY_BACK (cut; user re-confirmed today: keep the ending as is).
- **Round 3 (full round) running on candidate 3** from ~21:40 UTC: BM19 + R1 AS1 + R3 + R4; R2 joins after finishing its candidate-2 share. Rounds 1-2 found only check gaps (all fixed test-only) + one real game gap (night-2 arrows, fixed). Known-old only: career backlog 12, events FX24-2, perf one-offs backlog 32. Load false alarms: controller walk/idle, join reload timeout (run alone).
- **Publish**: USER: over the CURRENT links (Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU , Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m), {downloads}; never 6daN. PUB2 session_01GKuymkDxLVyt4rjtcJxdab is ready, waits for BM19's GO on candidate 3. ETA ~7 PM Eastern. Then: claude/integration fast-forward waits for the user's OK.

## Right after publish (the user's orders)
1. **Hire a balance researcher (BAL1)**: analyze balance only, NO fixes. Reads the numbers (needs decay, rep, job/lesson times, promotion gates, prices/wages) against design-doc.md; runs paper/sim players (styles: does every job, socialiser, skips meals, misses lessons) through Days 0-30+ with the existing check machinery (career_check-style); report as an artifact page: findings + evidence + suggested ranges, and a list of what only the user's own play can judge. Read-only on the game.
2. **At the same time start the Dev mode update**: one builder (DM1) first writes a short scope plan for the user (Dev mode jumps/presets/Set career for every tradition, ship-wide event, Step 5/6 beat, vessel, ending; devmode_check + dev_arrow_check covering each), then builds after the user OKs it; RV24 reviews; BM19 merges; full round before publish.
3. Plan order after that: controller update (its own project: audit every feature since controller support was made, pad reaches all, then PAD_ON on) -> optimization (incl. backlog BM19-1 trim SHIP.works Step 6 records) -> playtest patches (backlog: BM19-2 p5nWordTick null guard, W8-1 Calder misses Four weeks aboard, W8-2 section 10 tea-seat cases, W8-3, PZ6-1, N6-1 ended-career save won't load, Day 22 briefing-skipped 13-min seam, Taavek sketch heads-up wording).

## Seats (cap: at most 5 ACTIVELY working)
- BM19 build master session_01GKuymncYhRTKs8t4byNfdj (~50%+ memory: watch it; it may need a handover after publish).
- Round runners: R1 = AS1 session_01GKuymmdgtDvbd8P7URXd4z (also owns arrows_check step6; good memory), R2 session_01GKuymicEV4pw2WFLo8iHrq, R3 session_01GKuymmv95Tm7siWzMeEgmS, R4 session_01GKuymignKdueCaz2pftLEC. Archive R2-R4 after GO (keep AS1).
- RV24 reviewer session_01GKuymnJuoJTWnmYunbN7EP (~40%, idle; notes claude/review-rv24).
- Builders idle for round fixes: W8 session_01GKuymk95u5t4uDsahatkPN (career/24 core; replies reach lead 42 now, sometimes via lead 41), DA6 session_01GKuymjJ4sU5hfdU8bH49UW (decks, S6-4/5), N6 session_01GKuymnDA25R2a5yZGYpaBS (nights; ~56%, don't give it big jobs). Archive when Step 6 is published if nothing is pending.
- PUB2 publisher (above).
- Archived today: RV23, MA6, PZ6.

## Gotchas
- Every game change = full round (CLAUDE.md). Words-only = word checks (decision 5). Test-only = no game re-run.
- Checks written for a switch being off break when it goes on: sweep for the off line; ending_check/controller ending need a Step-6-off copy (assign window.P5_STEP6 in the copy, the script is wrapped in a function).
- More than ~2-3 browsers per machine gives false timeouts: re-run alone before calling a FAIL.
- Questions for the user: also a PushNotification. Times in US Eastern.
