# Handover: lead 29

## START HERE (lead 30)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-29` (from "~16:21 UTC: LEAD 29 took over").
2. Branch: start `claude/lead-30` from `claude/lead-29`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 29's `trig_016wDkGXk2rZX121DeBTWQT3` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you (priority "now"; ask for an acknowledgement).
5. Tell the user in one short message that you've taken over.

Lead 29 = session_01A9rNreAGVbsY1HgPucDMA7, branch `claude/lead-29`. Took over 2026-10-22 ~16:21 UTC; handed over ~21:35 UTC (memory in the judge zone, two big merges ahead).

## The user's standing rules (new today in bold)
- Plain language, no jargon, no emojis. Phone notification (PushNotification) for every published build, milestone or question only.
- **Fewer messages (the user, 16:42):** don't write to the user for every helper message. Reply "Noted." (or one line) to routine helper messages; write properly only for a published build, a question only the user can answer, or a collected summary at a milestone. (The user also asked what "Logged" meant: be accurate; TEAM.md lines are written at check-ins and real events, not per message.)
- **Helper limit is 18 for now (the user, 19:10)** and "hire accordingly" when work queues.
- **Fresh-eyes fixes:** collect them on the findings page, review with the user, build as a batch. The user answers on the page (status "Fix agreed" / "Not a problem"); the lead proposes wording for agreed items without wording and asks for one Go.
- **Fresh-eyes run (the user, 18:30):** wait for the fixed build. A NEW fresh-eyes player (FE2) plays Days 0-8 on the Pillar 5 + arrows + batch 2 build, then one review of the whole list with the user. FE1's handover: claude/fresh-eyes 7f2a36f.
- **Build all new work on top of the controller version (the user, 17:47).**
- **Breakfast rolled back (the user, 19:42):** "The breakfast build has problems... build from the build before that; breakfast fix later." Problem named: **Zeke's welcome tour (Day 0) was messed up**; details later from the user. Breakfast (0.64.17) is kept on `claude/patch-play1-f` 7f07d035 (+ m12 fixture fix, Line supper fix, bubble-jump fix `claude/bubble-jump` 36f8abf7). Before it returns: a Day 0 tour check; interactions_check "Deck 3 landing" red seen with 0.64.17 + FX3 fix 10; CTT2's pad finding (ring says "Lift" but A walks to the Spine ladder with 0.64.17's ladders).
- Memory: judge from ~60%, 80% hard cap. Full round on six runners for every game change. main and published links change only for a passed build; PRs/merges to main only on the user's go.

## Pages for the user
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq: both **Version 7 = 0.64.16** (rolled back; from b9f053ba, sha 70f94273…a6c7). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg republishes from a named commit + sha.
- **Fresh-eyes findings** https://claude.ai/artifact/7GFQ8pZZxmZnTW3o6RHd6k (v20; items 1-47). Lead 29's source copy: its scratchpad (not shared). A new lead: Artifact read the url (with `path` for the file), edit the `state` JSON, publish with `url`; ALWAYS read the live page first (the user's saves win; a refused publish hands you the live version: merge and republish).
  - Batch 1 (items 1, 3, 4, 5, 16): in 0.91.0. Item 21 and 22-23, 26, 28, 30-32, 34-37, 39, 42-47: "Not a problem". 
  - **Batch 2 (user's Go 18:5x):** 24 + 41 (CP4), 25 (not a bug: player was in the cubicle behind the glass), 27 (DS1), 29 + 40 (FX2), 33 + 38 (FX3 + CP4). All PASS at RV8 except 38's final pin commit 016fc65e (waiting RV8). Page still says "building" for them: update to "done" when the Pillar 5 build ships.

## Builds in flight (order)
1. **0.91.0 = controller (switched off) + fresh-eyes batch 1**, on 0.64.16. claude/integration-next-fe1 **989fd566** (sha da9f1d08…), on controller 0.90.9 `claude/controller` 9a8eac0b. BM14's checks OK, **RV9 PASS (21:27)**. **Six-runner round started ~21:30 by BM14** (OLD = b9f053ba; controller_check minus reach in one share; known: backlog 14, 23, 32 + controller_check touch/day check-only). On pass: BM14 fast-forwards claude/integration, PUB1 publishes 0.91.0 to both pages, notify the user (controller stays OFF; ask the user before switch-on only after the controller follow-up).
2. **Pillar 5 fixes + arrows (off) + fresh-eyes batch 2**, assembled by **AC2 on claude/arrows-c** (list: plans/arrows-c-assembly.md; tip fb02f02 at 21:19). In: DS1 fe2-player, CP4 24/41, FX2's four cherry-picks, FX3 fixes 10-14, AC2's doable (rounds + hauls only), tea arrow, job arrow rests after clock-out, real-tap follower. Waiting to merge as they pass: CP4 38 (f59b471e + 016fc65e, RV8), FB1 claude/fe-cartdock 228de58 + 776c4ff (all haul/delivery stops by real taps, Day 6 seal stow, any chore: tap on the line over the pin does the stop; RV8), FX3 fix 15/16 + Thursday inspection arrows (piece F2, with AC2) + climbing-wall tap (RV7), AC2's "a training's toast is never dropped" + follower "end any activity that isn't the job's stop" (RV7). Then: week guide on the assembled tip (goal: every lesson Days 2-8 learned, arrows off and on), then BM14 merges arrows-c onto 0.91.0 (IM1's trial: only 2 game conflicts, Settings view and jobEnd repair finish; resolutions in plans/trial-p5-on-controller.md) → RV7 review of the merge → six-runner round → publish → FE2 fresh-eyes run.
3. **Controller follow-up** (before any switch-on): CTT3 proves reach + finishes the sweep (5 earlier "gaps" all reached by direct D-pad walks); CTT3 fixes controller_check touch/day (check-only); mess seat 3-mess-1 ring offers the long-table seat (old). CP1 owns fixes.
4. **DS1 "Start at Day N"** (claude/day-start, RV6 PASS): after the Pillar 5 build; DS1 records the real eight days, then a round.
5. **Breakfast** later (see rules above).

## Seats (session ids)
- BM14 build master session_016mhGtsCxEgPCFn9C767yjq (~35%). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg.
- Runners CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk.
- Arrows/assembly: AC2 session_015uhdrDuE49CJ8iWWX2SEeP (~37%).
- Builders: FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (~15%), FB1 session_01C12k89pPRvZ63JHS3C2e1a (~36%).
- Reviewers: RV7 session_01RLTBGbbdRbUkKME189xL4k (Pillar 5 + merged build, ~30%), RV8 session_01Q6uHYWus4ncyEgqWEYhJh5 (batch 2, ~33%), RV9 session_01E31oZQU7DFbZnh2BesWsnM (0.91.0, ~20%; free now).
- Merge helper IM1 session_01PL57XDQC6t5hx7NtJ1pDMo (~20%).
- Controller: CP1 session_015ZhJRKCEditHrVhwdhszYq (~47%), CTT3 session_0197zJtQyLkNz6dxc3NgoNgy.
- Idle / available: DS1 session_01MZBSf7MZeb9C89wpoavLko (~20%), SC1 session_01BBC5dx3LtPPiWkTdurPTmJ (~50%, breakfast's author), FX2 (~55%, handover-fx2.md), CP4 (~55%, handover-cp4.md), RV3 (~41%).
- Stopped (notes on their branches): FX1, AR2, AC1, RV6, RV5, CTT2, FE1, lead 28.

## Backlog added today (lead 29)
LEAD29-1 perf_check should stand the player on a fixed tile per scene (crowd changes moved the camera; Line ceremony 301→335 accepted as baseline on 0.64.17, now rolled back). Stray branch `claude/controller-p1-0909` (copy of an abandoned merge): harmless, delete when convenient.

## Gotchas
- Messages cross constantly: resend decisions when a seat asks again; use "now" for scope changes.
- Several seats can only push their own branch (FX2 → p5-fix2; cherry-pick their commits).
- arrows_check's follower now uses real screen taps (AC2 5160b81); playerTap-based passes can hide pin/tap bugs.
- Pin-on-a-thing class of bugs (a thing at the job's pin takes the tap): fixed for machines (FX3 fix 14), hauls/deliveries (FB1), any chore when the tap line passes over the pin (FB1 776c4ff), job board pin (CP4 + FX3). Watch for more in the week guide.
