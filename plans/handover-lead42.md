# Handover: lead 42

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on **claude/lead-42** from "LEAD 42 started" (every line after). Then plans/overnight-decisions-lead42.md (tonight's overnight mode). Older: plans/handover-lead41.md, plans/overnight-decisions-lead41.md.
Lead 42 = session_01GKuymjnCHnpwDqB94PVwmV, branch claude/lead-42, hourly check-in **trig_016zcYSSwXEKiD4zNuLoL9p9** (53 * * * *): make your own (copy its prompt, renamed, overnight wording) and tell lead 42 its id so lead 42 disables its own. Lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j) is idle; it is W8's parent and relays W8's messages if they go to it.

## State at writing (~02:05 UTC Oct 28 = 10:05 PM Eastern Oct 27)
- **0.95.0 PASSED its full round** (round 3, all 5 shares; known-old only: career backlog 12, events FX24-2, perf backlog 32 order noise). Build: claude/staging-p5s6 **b5199dc3**, game sha256 **b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a**. All of Step 6 + both live fixes + night-2 arrow fix + the 3 patch-E features (RANK_CARD_ON, CLOCK_UNDO_ON, SHOP_MENU_ON). Off on purpose: TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, PAD_ON (the controller project), END_WAY_BACK (cut; the user re-confirmed: keep the ending as is).
- **Publishing now**: lead 42 sent PUB2 (session_01GKuymkDxLVyt4rjtcJxdab) GO at 02:01 UTC: over the CURRENT links (Playtest https://claude.ai/artifact/7hQ14AcwZHCi5EvL1AKiMU , Dev https://claude.ai/artifact/KEyaHvon6ZaVHHFRdAe18m), {downloads}, 390x844 test; never 6daN. **When PUB2 reports it live: send the user a PushNotification** (they asked for one; they're asleep, but it waits on their phone) and log it. Then: claude/integration fast-forward to b5199dc3 waits for the user's OK (morning).
- Test-only check fixes still to merge into staging (game unchanged): R3 claude/checks-s6-r3 88999f2 (arrows_d), AS1 claude/arrows-step6 238c46d8 (arrows_pointer). Both: a 30-step wait before tapping the time clock (CLOCK_UNDO's 500 ms tap guard).
- **Balance report done** (BAL1 session_01GKuymkWEsWv2Y3NqePc8DP, idle): https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm , branch claude/balance-research. The user will read it; NO balance fixes until they answer. Key: the Tier 4 Trusted-55 cliff; late Specialists lose night set pieces (m23/m24) silently; "Four weeks aboard" words on a moved Calder question; never-Tier-4 = no ending.

## THE USER'S ORDERS (latest first)
1. **Overnight (the user, ~02:03 UTC Oct 28, going to bed): "for overnight mode let's jump forward to the controller update."** See plans/overnight-decisions-lead42.md for the scope and the calls made.
2. **Dev mode update: ON HOLD** (the user, 00:57 UTC): do not start until they say.
3. Push notifications for questions AND important milestones (a release live, a report ready).
4. Plan after the controller: optimization (incl. backlog BM19-1 trim SHIP.works Step 6 records) -> playtest patches (backlog: BM19-2 p5nWordTick null guard, W8-1 Calder misses Four weeks aboard, W8-2, W8-3, PZ6-1, N6-1 ended-career save won't load, Day 22 briefing-skipped 13-min seam, Taavek sketch heads-up wording, balance-report items the user picks).

## Seats (cap: at most 5 ACTIVELY working; overnight the same)
- BM19 build master session_01GKuymncYhRTKs8t4byNfdj (~50%+ memory). **It stopped acting on the lead's word tonight and waits for a human yes** (stalled twice). Recommend: hire a fresh build master (BM20) for the controller project from plans/handover-bm19.md (on claude/staging-p5s6) and archive BM19.
- Round runners: R1 = AS1 session_01GKuymmdgtDvbd8P7URXd4z (good memory; owns arrows_check step6; ran the interactions check twice), R2 session_01GKuymicEV4pw2WFLo8iHrq, R3 session_01GKuymmv95Tm7siWzMeEgmS, R4 session_01GKuymignKdueCaz2pftLEC, R5 session_01GKuymmpT2HG9LzzUGNqDpp (BM19's share). All idle now; archive R2-R5 once 0.95.0 is live (their notes: plans/checks-s6-rN.md on claude/checks-s6-rN). Hire fresh runners for the controller round.
- RV24 reviewer session_01GKuymnJuoJTWnmYunbN7EP (~40%, idle; notes claude/review-rv24).
- Builders idle: W8 session_01GKuymk95u5t4uDsahatkPN (career/24 core), DA6 session_01GKuymjJ4sU5hfdU8bH49UW (decks), N6 session_01GKuymnDA25R2a5yZGYpaBS (~56%, no big jobs). Archive after publish unless needed.
- BAL1 balance researcher (above), PUB2 publisher (above).
- Archived on 27 Oct: RV23, MA6, PZ6.

## Gotchas
- Every game change = full round (CLAUDE.md). Words-only = word checks. Test-only = no game re-run.
- Checks written for a switch being off break when it goes on: sweep for the off line (PAD_ON will need this). ending_check/controller ending need a Step-6-off copy (assign window.P5_STEP6 in the copy; the script is wrapped in a function).
- More than ~2 browsers per machine gives false timeouts: re-run alone before calling a FAIL. Containers restart now and then and kill detached runs: runners should use tracked background jobs, no short time limits (interactions ~35 min alone, perf ~77 min alone).
- perf: whichever build is measured second runs slower under load; swap the order to test (backlog 32).
- Seats sometimes wait for a human yes on a peer's word (BM19 tonight): check each GO actually started; if not, send GO to the runners yourself or replace the seat.
- W8 can only reach its parent (lead 41) sometimes; lead 41 forwards.
- Times for the user in US Eastern. No emojis. Plain words.
