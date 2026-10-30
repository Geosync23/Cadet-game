# Handover: build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh)

Read this first if you take over as build master (BM17). Before me: `plans/handover-bm15.md` (0.92.1-0.92.3).

## Who

- Lead: **lead 35**, session_01VQkkt8RXcvvGs1Dmzn2emM (branch claude/lead-35). Earlier: lead 33, lead 34.
- Publisher: **PUB1**, session_01GnpjFR6oumvuvTrmcXSqeg.
- Check runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk.
- Reviewers: RV11 session_01EdBKAgQFMexMSs3JbgH5H7, RV12 session_013JmdoWWEDQde8y1bwrMGnY, RV13 session_016ioWtxM6NJRV4Ck3ADwozc, RV14 session_01RwUYVcYt2PP7B7g3ogduFZ (weekend).

## Builds I made

| Build | Commit | Game sha256 | Notes |
| --- | --- | --- | --- |
| 0.92.3 | d9a387b6 (integration 3866c8f3 with records) | f18e8540…7853 | Round 1 on 0dd4e2e2 found mech m3d (AC3 item 6, fix 4928271f); round 2 all OK. Published on NEW pages: Playtest https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ, Dev https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr |
| 0.92.4 | 5bad724d (integration ba836359 with records) | 2aa6427f…13a2 | A trays (FX12), B dirty clothes (FX4), C crew glide (FX8), D repair-vs-lesson (FX10). Round all OK. Published as an update of the same pages. |
| 0.92.5 | claude/staging-0.92.5, in progress | | see below |

## 0.92.5 right now (2026-10-25 ~04:35 UTC)

`claude/staging-0.92.5` pushed at **0aaf48b7**. In, in this order (each on its reviewer's PASS, check_fast + area checks after each):
FX9 84e14d89 (1), FX9b f67dd971 (6, 7), DV1 81e9065c (18, promotion), sim bay 328f678a (FX14, merged dormant), FX13 04a9385d (5), **sim bay switched ON e9ce3351** (the user's "Put the Sim bay in."; RV13 PASS), FX9c 8777fc44 (21), FX11 c97fbef0 (2, 3, 14, 17), DS1 a99453d8 (11, 12, 15), FX13b 5e1d82d5 (20, Tiles ladder), backlog RV14-1, FX12 91b97ee9 (4, 9, 10) with DV1's Day 9 arrows_check fix e823a74f.

**Merged locally in /tmp/wt-p5, not pushed:** 139471e6 = the weekend branch claude/p925-weekend **3307ded5** (WEEKEND_ON on; items 16, 19 and the 8c crewDetail line; RV14 FINAL PASS). Five files clashed and were resolved by hand (game: two blocks in the Traditions slot kept; join_check: both lines; design-doc's first-week line: both edits; DEV_NOTES: both sections; build-table: 6 new rows). Checks were running on it (check_fast, cadet_test, day 6/7, events, weekend_check, food 1 7, tiles, join alone). If you take over: re-create that merge from 0aaf48b7 the same way if /tmp/wt-p5 is gone, re-run those checks, push after check_fast.

**Still to come:** FX15 claude/p925-fx15 **87ab69e6** (= ccf77d05 + a text-only nit) (item 22, every lesson's job marked; with RV13). Merge only on RV13's PASS. ZW1's words for items 8/10 (claude/p925-zw1 62f89173): check with the lead whether they're still wanted (FX12's 0.92.5 piece may already carry them).

**Then:** freeze (build 0.92.5: header `build` line ~291 and `GAME_BUILD` ~9076; a `| 0.92.5 |` row after 0.92.4's with `Checks: FULLROUND |`; DEV_NOTES "Where things stand"), check_fast + cadet_test vs ba836359, send lead 35 the sha256, and on the go the six-runner round, NEW = candidate, OLD = **ba836359** (0.92.4).

## Round notes for 0.92.5

- Shares as plans/testing-guide.md; **weekend_check is new, in CR3's share** (FX16 added it to the guide).
- Expected, not new: **perf_check prints 7 PROBLEM lines on the weekend scenes** (jigsaw and story draw calls, Bread day landscape js; more people, all under budget 450, max 342; RV14). The sim bay's frame-time flags were machine noise (two alone runs disagreed; lead 35: CR2's round perf decides). cadet_test vs 0.92.4 will differ: the sim bay (crew plans change with the sim-pilot habit: e_night onward, g_nocrew and a-d identical; RV13 proved it with SIM_BAY false = identical), FX9b's Deck 4 lounge seats (most shots, same pixels as FX9b alone), FX9c's walking stride (j_steer1/2).
- Known old: backlog 12, 14, 23, 32, KP1, RV14-1 (food_check 7 7 'garden, good'), FX8-1.
- join_check must run ALONE (it times out at save/reload side by side). arrows_check can false-FAIL under load (the Dev-sheet tap; DV1's fix is in): re-run alone before calling it.

## Gotchas I hit

- Background commands stop at 2 hours (the tool's limit): split long check lists. A chain waiting on another run's output dies with it; restart the chain, not just the dead run.
- Run checks from a side worktree (`git worktree add --detach /tmp/wt-x <sha>`) and never merge into a folder whose checks are running: the scripts are read from it.
- `cd` into a scratch folder for cadet_test / perf_check (they write files in the current folder); give scripts by full path then.
- Merging the build table: "keep both" can double rows; dedupe ONLY the incoming side's rows already present (the table has 9 legit repeats; don't dedupe the whole file).
- Two pieces appending to the same slot of the game file: keep both blocks, each with its own closing brace (look at where git put the shared `}`).
- A "user doesn't want this, STOP" tool result can be a lead's priority-"now" message interrupting a call, not a person (lead 33). Message other seats with priority "next".
- Overnight / user-awake: no messages to the user from the build master; the lead talks to the user.

## Test kit

`pip install playwright numpy pillow`; `npm pack three@0.128.0 acorn@8.12.1` untarred into /tmp/cadet-work/three and /tmp/cadet-work/acorn (with `package/`); `CADET_CHROME=/opt/pw-browsers/chromium`; each parallel run its own CADET_WORK (/tmp/w-sb, /tmp/w-sc, /tmp/w-sd) with symlinks to those two. Merge helper: see handover-bm15.md (resolve.py).
