# Handover: lead 28

## START HERE (lead 29)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-28` (from "~14:20 UTC: LEAD 28 took over").
2. Branch: start `claude/lead-29` from `claude/lead-28`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 28's `trig_011DuPdyH9bxYZDpLwwJHCkH` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you (priority "now" for scope changes; ask for an acknowledgement).
5. Tell the user in one short message that you've taken over.

Lead 28 = session_01S7AdxK1ZyXiEFowP3k5gng, branch `claude/lead-28`. Took over 2026-10-22 ~14:18 UTC; handed over ~16:25 UTC at ~55% memory (big merges ahead).

## The user's standing rules (new today in bold)
- Plain language, no jargon, no emojis. Phone notification (PushNotification) for every new build, milestone or question.
- Memory: from ~60% judge case by case (hand over before a big task); 80% hard cap.
- Full round on every game change, six runners at once (plans/testing-guide.md). Run cadet_test strictly alone.
- Helpers: at most 12 working at once; up to 20 while a six-runner round runs. Idle seats don't count.
- main and published links change only for a passed build; PRs/merges to main only on the user's go.
- **Fresh-eyes fixes (the user, 16:17): collect them on the findings page; then one review with the user; then build as one batch. Do NOT start fresh-eyes fixes one by one any more.** Each fix needs the user's own fix wording and go.
- **Fresh-eyes batch 1 = one build with one test round (the user, 16:19).**

## Pages for the user
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq: both Version 5 = **0.64.16** (the Zeke fix; integration b9f053ba, sha 70f94273…a6c7). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg republishes from a named commit + sha.
- Arrows plan https://claude.ai/artifact/7rKvXwbZLRsJj8k7yrXXkK (v6; source plans/arrows-pillar5-plan.html on claude/arrows-plan, a copy in lead 28's scratchpad). Note: the page still says piece E sits in 24 core with T1-T4; AC1 fixed that in the branch copy (claude/arrows-c), republish from there next time.
- Day checklist https://claude.ai/artifact/16fiseF7pPzjbzEK5BMnY6 (from claude/day-start 9f760506; capabilities artifact + comments; the user's ticks/notes live in its `state` JSON block: read with Artifact read).
- **Fresh-eyes findings** https://claude.ai/artifact/7GFQ8pZZxmZnTW3o6RHd6k (v11; capability artifact; the user writes fixes and statuses, Save republishes with a `state` JSON block). Lead 28's source file is in its scratchpad (fresh-eyes-findings.html) and mk_findings.py there shows how items were added. **A new lead has no local copy: Artifact read the url, save the HTML to your scratchpad, edit the `state` JSON, publish with url set. ALWAYS read the live page first so you never overwrite the user's edits.** Items carry "(Diary N)" numbers from FE1's diary.

## Builds in flight (order)
1. **0.64.17 = breakfast at 07:00.** integration-next 8193458e (+ docs 9caa097c), game sha 22583691…c4b5. Round found two FAILs: (a) mech_check m12 = a test-fixture clash, not a game bug (SC1 fix 5640cf5a on claude/patch-play1-f, RV3 PASS; BM14 merged locally). (b) bigevents Line supper (silva-bea eats standing, Day 7) = REAL, a latent gap in tradMeal (fixed set-off ignores walk distance); SC1 2-line fix in section 14, running its full set (~17:45), then RV3 reviews, then BM14 merges both and runs a **full round**, fast-forward, PUB1, notify the user. Runners CR1-CR6 report to BM14. CR3/CR4/CR5/CR6 shares OK apart from (a)/(b); CR1, CR2 were finishing.
2. **Fresh-eyes batch 1** (one build, one round; BM14 assembles on claude/integration-next-fe1 after 0.64.17): eating at any seat (FX2 191d185 on claude/p5-fix2, cherry-pick; AR2 reviewing), New game in Settings (CP4 claude/new-game-settings 63710eb2; RV5 reviews after 0.90.8), no bubbles over the open device (CP4 claude/bubbles-device, building; RV5), bunk "too early, from 20:00" + "Yours is the next one" (DS1 claude/bunk-early, building; RV6), lift panel arrow ("Tap the lift: Deck 4 · …", FX3 on claude/p5-fix3 as its own commit, building; AR2; FX3 also checking the inside-car panel vs the outside keypad FE1 found). BM14 checks the lift commit applies alone.
3. **Pillar 5 fixes + arrows** (own build): FX2 cc2bb2b PASS (AR2), FX3 e6bcf82 PASS (+ 360801c galley/dropped part, with AR2), FX1 lifecycle tip due ~17:15 → AR2, then FX1 hands over (plans/handover-fx1.md). Arrows on claude/arrows-c 5557122e: B, C, E, F3, F4 all PASSED (RV2/RV6), switched off; D (shift chain) by AC2 building, waits for FX1's tip for trainArrow/trkTap lines; F1 (Rounds/Hauling/Tuning) and F2 (drill/inspection/uniform) not started (AC2 after D, or a new builder). arrows-c already merges p5-fix2 cc2bb2b and p5-fix3 e6bcf82/360801c. Agreed clash resolution: FX2/FX3 both edit one ixJobStep label line, keep both (FX3 chore title, then FX2 scan-first/Tune).
4. **DS1 "Start at Day N"** (claude/day-start 1d3f76c3, RV6 PASS): merges AFTER arrows-c + FX1-3 (needs arrows_check.py), then DS1 records the real eight days and a round.
5. **Controller** claude/controller 0.90.8 fda82c1a (sha d055cb1d…6190): CP1 swaps in CTT2's single controller_check (RV5 checks), then merges integration (after 0.64.17), then its six-runner round; switch-on only on the user's go. Hand-merge later: Settings view gets New game row + arrows C "Teaching arrows" row + P4's .concat(padSetBlocks()) (keep all).

## Seats (session ids)
- BM14 build master session_016mhGtsCxEgPCFn9C767yjq (BM13 idle, its note plans/handover-build-master.md).
- Runners CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk. PUB1 session_01GnpjFR6oumvuvTrmcXSqeg.
- SC1 (breakfast) session_01BBC5dx3LtPPiWkTdurPTmJ; RV3 session_01Uct2TvRPoFYViyU1X9Fpjx.
- FX1 session_01WmdPR5B5QC56Hid3F5M1wv (~55%, hands over after its push); FX2 session_01JRCSTi6r1qQ51mTgwgJ7es (~40%); FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (queue: lift arrow → Day 8 "Your bunk" stuck arrow → climbing holds pin on the climbing wall → burst job leads over a held job + OK AC1's 24f touch + "Ines"→"Calder" labels). AR2 session_015pnwa5oK7TDF5gZXNFLLvx reviews FX1-FX3 + eating + lift arrow (~35%).
- Arrows: AC2 session_015uhdrDuE49CJ8iWWX2SEeP (piece D); AC1 session_01LDmfZ93ttCJ4XfoSDkJqx2 (~52%, standby, plans/handover-ac1.md); RV6 session_018Jzc4LeoHvuahsS7VHAzn3 (~44%; reviews arrows, DS1, bunk). AR1, RV2, PR9, OR2 stopped (notes on their branches).
- DS1 session_01MZBSf7MZeb9C89wpoavLko (day-start, bunk-early). FE1 fresh-eyes player session_01Xt5a9oX8KzZMg4kim1hY8T (claude/fresh-eyes, diary plans/fresh-eyes-diary.md; Day 0 done, now Day 1-2 on 0.64.16, then stops; full Day 0-8 replay later on the fixed + arrows-on build). FE1 sends findings as "day | time | where | severity | what".
- Controller: CP1 session_015ZhJRKCEditHrVhwdhszYq, CP4 session_01VTXDwLqWGJVRh95HozqhCu (also doing New game + bubbles), CTT2 session_011yMob9ZzgmCFENoNhjJ44z, RV5 session_01DdhmKNwjve4tpJ1zq6ozyv.
- Seat count: over 12 once the 0.64.17 round ends; pause CTT2's reach sweep and keep AC1/BM13/SC1 idle if needed.

## Backlog added today
LEAD27-1 machine_check repair share over 28 days (it sits at 40%, the edge); LEAD28-1 / backlog 32 perf_check re-samples a one-off spike; LEAD28-2 closing the Scanner without picking can't reopen it. Known-old FAILs for rounds: backlog 14 and 23.

## Gotchas
- Messages cross: "now" priority + ask for an acknowledgement on scope changes.
- Check reviewer claims in play (RV6 withdrew a "Scanner never opens" that was its probe's tap; AC1 found it).
- Integration's arrival is 16:30 (not 17:30 as in old branches); bedtime is 20:00.
- Some seats can only push their own branch (FX1, FX2); cherry-pick their single-commit fixes.
