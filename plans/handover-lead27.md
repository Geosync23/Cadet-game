# Handover: lead 27

## START HERE (lead 28)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-27` (from "~10:12 UTC: LEAD 27 took over").
2. Branch: start `claude/lead-28` from `claude/lead-27`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session), then disable lead 27's `trig_011FyDwZoLc4NAv5VhKyHV52` (update_trigger enabled=false).
4. Message every working seat below with your session id so they report to you. Send reassignments with priority "now" and ask for an acknowledgement (a split message to FX1 was missed once today).

Lead 27 = session_017UHW78qnvRTQwYpDxpodHz, branch `claude/lead-27`. Took over 2026-10-22 ~10:12 UTC.

## The user's standing rules (new today in bold)
- Plain language, no jargon, no emojis. Safety of the code first. Phone notification for every new build, milestone or question.
- Memory: from ~60% judge case by case (hand over before a big task); 80% hard cap.
- Full round on every game change, six runners at once (plans/testing-guide.md).
- **At most 12 helpers working at once (daytime).** Idle seats don't count. Pause controller seats that are only waiting while the six runners work.
- main and published links change only for a passed build; PRs/merges to main only on the user's go.
- **Run cadet_test strictly alone** (a second browser alongside gives 1-level HUD noise; BM13 is adding this to testing-guide.md).

## Game pages
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq, both Version 4 = **0.64.15** (claude/integration 2b4a05db, game sha 0c1f6fb4...259d2e). PUB1 session_01GnpjFR6oumvuvTrmcXSqeg republishes from a named commit + sha.
- Arrows plan page for the user: https://claude.ai/artifact/7rKvXwbZLRsJj8k7yrXXkK (Version 5), published by lead 27 from claude/arrows-plan's plans/arrows-pillar5-plan.html (copy kept in lead 27's scratchpad). Republish by fetching the branch's file, checking no new script/URLs, and publishing to the same URL (a new session must pass `url`).

## Builds in flight (order: 0.64.16, 0.64.17, then FX1-3, then arrows B/C)
- **0.64.16 = the Zeke fix** (user's bug: after the bag Zeke stopped leading). ON1 session_01BJNi1oqxnQ3jUusXHbHDGW, claude/patch-zeke final **ce2f77bc** (handover plans/handover-on1.md). OR2 session_01AnRKXUUGi8mwREwvt4WbaV reviewing (near its memory limit; hands over after). BM13 session_01ExFoVfhiFG3wYTFv2QrojC rebuilds 0.64.16 on ce2f77bc + testing-guide notes 3cf7dd2d. Then six-runner round (CR1-CR6 ids in plans/handover-lead26.md), PUB1 publishes, notify the user.
- **0.64.17 = breakfast at 07:00** (user's go to SC1 in its own session). SC1 session_01BBC5dx3LtPPiWkTdurPTmJ, claude/patch-play1-f (b006ad08 local: night shift back to old order; crew wake unchanged 05:30-07:15; meals/galley moved). Reviewer RV3 session_01Uct2TvRPoFYViyU1X9Fpjx (briefed). Merges on top of 0.64.16. Own full round.
- **BM13 hands over after 0.64.17** (~52% memory): start BM14 to read plans/handover-build-master.md.

## Pillar 5 Steps 1-2: "very little of the career is working" (the user, ~12:00)
- Analysis: AR1 session_01XcfcbFvi4nMVUPZgT2BcmE (claude/arrows-plan: plan page, notes, briefs, arrows_check.py with parts queue/shift/week that play by following only the arrow; shift/week FAIL on 2b4a05db with lines naming FX1/FX2/FX3) and AR2 session_015pnwa5oK7TDF5gZXNFLLvx (claude/arrows-plan-2, done, idle; bring back for lesson arrows F1-F4).
- User's answers: "go with the recommendations" (fixes first; shift arrows always while tracked, panel pointers first 3 times; a meeting takes the arrow from **15 min** before; Settings "Teaching arrows" all/first/off, default first; burst pipe job taken at the pipe); **scan first** on every faulty job once you have the scanner; **Tomas** warns about the inspection Wednesday evening.
- Fixers (reviewer PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db):
  - FX1 session_01WmdPR5B5QC56Hid3F5M1wv, claude/p5-fix1 (1433e5f = fixes 1+2; note it used 30 min, user said 15): the arrow/tracking lifecycle list (career arrows clear; On shift → clock from 08:00; device "go"/Dev "Set career" keep tracking; fresh game tracking on; clock-out at 17:00; empty board word; shower need-arrow into Chief's cabin; missed lesson not at 06:00; Tracked picks training, names teacher/place). Its WIP for 3-6 went to FX2/FX3 as a patch to compare.
  - FX2 session_01JRCSTi6r1qQ51mTgwgJ7es, claude/p5-fix2: fire drill/side jobs in myJob; scanner training + scan-first rule + scanner use counted + teacher's job not takeable + clue "undefined"; tuning wording, Hauling "Main storage", Tune label, inspection 06:30; galley plant calibrate; dropped part left in hand.
  - FX3 session_01UZWrZRivwQJPKL3x7c8Ft9, claude/p5-fix3 b063f86 (five fixes: lift service place, Making it safe flow at the pipe, small lessons + uniform word, reputation shown + "Works team's standing", Record) → PR9; then HAULING any day (crates kept back; re-asked via its own 11:00 meeting), promo.officer talk, hauling per-stop words.
- Arrows build (both switched off): piece B arrow queue + toast queue (AR1, game commits on claude/arrows-plan 5c798b5, c0ab64c, tip 5dd6b6f) and piece C panel/device pointer (AC1 session_01LDmfZ93ttCJ4XfoSDkJqx2, claude/arrows-c d7a55699, arrows_pointer_check.py). Reviewer RV2 session_01E1TTHbhLzy2U6pAoGh7E9a (B then C, then hands over ~60%). Settings switch is AC1's: SHIP.device.settings.teach. Next: D shift chain (AR1, after FX1 lands), E training arrows, F1-F4 lessons (AR2/AC1 candidates).
- **Merge clash to watch:** arrows C and controller P4 both rewrite the last line of section 19's Settings view; whoever merges second keeps both.

## Controller team (claude/controller)
- All five packages passed review. claude/controller 5010eaf9 = 0.90.5 (P1+P2+P3), sha a1ab63b1...9854; CP1 session_015ZhJRKCEditHrVhwdhszYq merging P4 (f904532), P5 (4892a0b), then the pickfix (8d68ad51, RV5 reviewing) and CP4's first-use/drift fix (claude/controller-firstuse, RV5).
- RV5 session_01DdhmKNwjve4tpJ1zq6ozyv (tests + combined build). CTT2 session_011yMob9ZzgmCFENoNhjJ44z (single controller_check; next: day part, reach sweep, RV5's 5 small fixes). CP2, CP3, CP4, CP5 done/idle (handover notes for CP3, CP5).
- Then a six-runner round on claude/controller, merge into integration switched off; switch-on is its own reviewed step on the user's go.
- User decisions: suggested name "George", no rename for now; reconnect resume stays Start/A (user didn't ask otherwise); left-hand layout zoom left as CP5's backlog row.

## Gotchas
- Messages cross: when you change someone's scope, send priority "now" and ask them to confirm.
- AR1 can only push to claude/arrows-plan (builds B there as game commits on top of docs).
- Some seats can't create new branches (FX1 only pushes claude/p5-fix1).
- Check every fix: its new check part must FAIL on the old build.
