# Handover: lead 26

## START HERE (lead 27)
1. Read CLAUDE.md (60%/80% memory rule, six-runner full round on every game change, no emojis, plain language), this note, then the bottom of TEAM.md on `claude/lead-26` (from "~02:15 UTC: LEAD 26 took over").
2. Branch: start `claude/lead-27` from `claude/lead-26`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 26's `trig_012kj7K8rQoenVdySbkUcoKa` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you.

Lead 26 = session_015mHBLCf5jpnzBkFY1iBTqv, branch `claude/lead-26`. Took over 2026-10-22 ~02:10 UTC; handed over ~10:15 UTC at ~64% memory.

## The user's standing rules (new tonight in bold)
- Plain language, no jargon, no emojis. Safety of the code first. Phone notification for every new build, milestone or question.
- **Memory: from ~60% judge case by case (hand over before a big task); 80% is the hard cap.**
- Full round on every game change, six runners at once (plans/testing-guide.md). The test picker is only a quick aid.
- **Usage: once 20% of the weekly allowance is used, pare teams down when able.** The lead can't see the weekly %; the five-hour status was "allowed" all night. The user may give a time instead.
- **Overnight: at 2am Eastern the user asked for at most 8 workers at once, patch first.** It's daytime now: ask the user if a cap still holds (lead 26 asked; no answer yet).
- **Hire as many as needed for the patch** (the user, 03:30). Ideal size used: one builder per area, ~3 reviewers.
- main and the published links change only for a passed build; PRs/merges to main only on the user's go.

## Game pages
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq, both version 3 = 0.64.14. PUB1 session_01GnpjFR6oumvuvTrmcXSqeg republishes to the same URLs from a named commit + sha256.
- Also published tonight: look test (bunk room) https://claude.ai/artifact/XL3oEyLn2eBrJWzhZnQzLT (LT1; answers in its store, collection "answers"); testing guide page https://claude.ai/artifact/F9sUw2gpR5bMjiLjQ75YbM (TS3).

## 0.64.15 = playtest patch 1 (plan: plans/patch-playtest1.md on claude/lead-26)
- Candidate: `claude/integration-next` **31c44cb9**, game sha256 **0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e**. OLD = claude/integration 32b699a6 (0.64.14).
- In it: A arrival 16:30 + Zeke/Chief (ON1), B pointer/tea arrow/"Tracked" (FR4), C wall clipping (PB2: signed shift `>> 3` → `>>> 3` from patch #10 a67ea08e, 0.64.6), D Chief's first solo job tracked + clear lines (CJ1), E ladder taps + rower (LD1), G more jobs on the board (JB1; extras give no Works reputation), H open ladder rooms (LR1), I toilet queue (TQ1), J clock in/out reminders (CK1), K repeating lines in "Talk a while" (DL1), plus the Line merge (claude/line-update cee209a4) switched OFF. All reviewed (OR2: A C D; RV3: B E J; RV4: G H I K).
- **NOT in it: F breakfast at 07:00.** SC1 (session_01BBC5dx3LtPPiWkTdurPTmJ) built it (option A: 07:00-09:00, galley an hour later, early starters grab from a shelf open at 06:00, shifts unchanged) but also built a toilet queue by mistake, and refuses to remove it and push without the user's OWN go in its session. Lead 26 started SC2 (session_015EQaSLpYenb4uVabuNrw7i) to redo it, then stopped SC2 before it did anything because the auto-mode check flagged that as routing around SC1's request. **The user decides:** tell SC1 "go" in its session, or tell the lead to have SC2 redo it. RV3's notes (claude/review-play1, plans/review-play1.md) list everything tied to the 06:00 opening; ON1: check Tomas's Day 1 06:00 wash scene against the later wake time.
- First full round (c5c43293) found 2 new FAILs, both fixed and re-reviewed: J's reminder toast covered the busy-washer answer (CK1 4bc3e39c: never over a toast + 10 s gap); intro_check part 14 expected "Fetch a relay" but since A's 16:30 arrival the Lights shelf is empty by 10:40 (CJ1 836db6c7: check accepts fetch or make; the Chief's line covers both).
- **Re-run on 31c44cb9: CR1 OK (225b1e9, incl. fridays), CR3 OK, CR4 OK, CR5 OK, CR6 OK; CR2 still finishing** (intro OK incl. part 14; path/arc/lines OK; cadet_test differences explained; perf: backlog 14 + a one-off spike that moves scene each run, re-measuring). **When CR2 reports OK:** tell BM13 to fast-forward claude/integration to 31c44cb9 (it said it would), tell PUB1 to republish both pages from 31c44cb9 (sha above), notify the user's phone with a plain summary.
- Known-old FAILs now: backlog 14 and 23 (12 no longer shows). Run tiles_check alone (it times out under load). fridays_check takes ~20 min (the guide's 4 is out of date: ask TS3 to fix the guide's timings).
- Next-patch backlog from tonight: B nits (rows 30-31: "Clock in" lingers a ship minute; manual untrack leaves job tracking off), LD1-1 (Deck 5 lift brake takes ladder taps), LD1-2 (interactions_check part for ladder taps), TQ1-1 (crew stand in a toilet line while one is free), JB1-1 (same extra chore twice a day), K-1 (a small-talk line says "the stairs"), OR2's slow-walk Day 1 bunk arrow, the 09:00 clock reminder can be dropped if a toast is showing, and for the user's balancing pass: extras' reputation, upkeep topping out ~Day 11, talks giving full social in ~8 ship minutes.

## Controller team (the user: "start the controller team", then "write the split yourself")
- Split by lead 26: plans/controller-team.md on claude/lead-26 (31151143), from CT1's plan plans/controller-plan.html (claude/controller). All from claude/controller a2c80df6 (CT1's turns 1-3 + turn 4 WIP).
- CP1 panels + merges into claude/controller: session_015ZhJRKCEditHrVhwdhszYq, claude/controller-p1 (API pushed 93093a8b). CP2 mini-games/special screens: session_016zb2DTsTLqNNNeuegePDgE. CP3 button pictures + connect/disconnect: session_01AkfeDe7MBN8RYd5n6obGRm. CP4 settings page: session_01VTXDwLqWGJVRh95HozqhCu. CP5 accessibility + docs: session_01VcdDgzyHa1dqdmcRLELbiS. CTT tests: session_01SgEbMMMNPRP2E7DbiDyiw4 (fixing 3 check gaps PR9 found). Reviewers: PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db (P1, P2; turn 3 game PASS), RV2 session_01E1TTHbhLzy2U6pAoGh7E9a (P3-P5, CTT; turn 3 also OK).
- CT1 (session_019sqDowb6QNf3KZAYMSx1jM, ~44% memory) built turns 1-3 but kept working solo and never wrote the team page; it waits for its own user's go. Treat it as idle/advisory.
- Into claude/integration only after all five pass, a six-runner round, and switch-on is its own reviewed step on the user's go.

## Other seats
- BM13 build master session_01ExFoVfhiFG3wYTFv2QrojC (claude/integration, claude/integration-next): waiting on CR2, then fast-forward.
- CR1-CR6: session_01CsWNjCsy8u5mrHJgTVgCst / session_01BgMQaB1LQmhfU1rSJ2ATvv / session_016oCbvvzgcqzzCTsBFCkYRB / session_01636CfY2MhB3DzrzZ59dhXz / session_01CHoEsvv7zMPZDr1ir7uAiz / session_01B1FwE5sMmHnMPWsGn23nrk.
- Idle with handover notes: OR2, RV3, RV4, PB2, ON1, JB1 (plans/handover-*.md on their branches); idle: FR4, CJ1, CK1, DL1, LD1, LR1, TQ1, LB3, PR10, LT1, TS3, EP2, P5P, CS1, PUB1. SC1/SC2: see breakfast above.
- The Line: merged into 0.64.15 switched OFF (EV_LINE_ON false). L6 switch-on only on the user's go.

## Gotchas learned tonight
- Seats often miss reassignment messages while mid-turn: send with priority "next" (or "now" to interrupt) when it matters, and check get_session's task_summary for drift.
- Some seats won't act on lead messages for risky steps and wait for their own user (SC1, CT1). Don't route around that; ask the user.
- Ask builders to label backlog rows (e.g. LD1-1) to avoid numbering clashes across branches.
- lines_check isn't in check_fast: run it on anything touching content/.
- Every check fix: prove it fails on the old build.
