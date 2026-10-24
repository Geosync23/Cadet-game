# Handover: lead 34 → lead 35

## START HERE (lead 35)
1. Read CLAUDE.md (note the new "current save" Dev link rule), this note, plans/patch-0.92.5.md, then the bottom of TEAM.md on claude/lead-34 (from "~15:00 UTC: LEAD 34 took over").
2. Branch `claude/lead-35` from `claude/lead-34`; push only there. **Read the game from origin/claude/integration (or staging), never the lead branch's copy: lead branches carry a STALE starship-cadet.html** (lead 34 wrongly told the user promotion wasn't built because of this).
3. Make your own hourly check-in (create_trigger, cron `57 * * * *`, into your session), then disable lead 34's trig_01QbNB6JYStQZ6FeUxqErxfN.
4. Message every working seat with your session id (priority "next", NEVER "now"). Tell lead 34 (session_019RdVfeRPRiJpHGjKujZZJA) you've taken over.
5. The user is awake (US Eastern, EDT = UTC-4). Plain words, no emojis, few messages. **Cap: at most 8 seats working at once today** (lead + idle seats not counted). The 0.92.5 round = BM16 + 6 runners = 7, so at most 1 other seat during it; pause the rest.

Lead 34 = session_019RdVfeRPRiJpHGjKujZZJA, branch claude/lead-34; took over 15:00 UTC 10-24; handed over ~00:00 UTC 10-25 at ~62%.

## Done under lead 34
- **0.92.4 PUBLISHED** 20:08 UTC (4:08 PM Eastern) as Version 2 of Playtest https://claude.ai/artifact/3HqM5XiXaHXzgrpq7JbesJ and Dev https://claude.ai/artifact/9ZWAgqiZCvkJvVjjhjVkEr (from staging-0.92.4 5bad724d, sha 2aa6427f…13a2). Trays, dirty-clothes reminders, crew stand-up glide, repair-vs-lesson warning. **claude/integration + integration-next = ba836359** (user OK).
- **The user's "current save" Dev link = https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq** (v11 = 0.92.2, longer playthrough). Never publish over it (in CLAUDE.md; PUB1 knows). Old Playtest v11 Wn6mUGcxatoWVqhCNTa1vs also untouched.
- **Sim bay** (FX14, plan Hmg44se58wGkZaGCMFyRWL): built S1-S7, RV13 PASS, merged into staging-0.92.5 and **switched ON** at the user's word ("Put the Sim bay in", 21:19 UTC; RV13 PASS switch-on e9ce3351; BM16 re-running perf alone). Preview page G1fpE2YeMtPukqTZ2J3u77 (can be left).
- **Sim flight landing PROTOTYPE** (standalone, NOT in the game): https://claude.ai/artifact/RMgibsuh2KdxcF3kd8vuJr v2 (claude/simflight 7bf86392; FX13; prettier + steering inverted). **User: ON HOLD** ("Hold the landing prototype off for now"). Plan page MPxYJgsid5HEVq2qBsynda (answers all recommended).
- **Promotion**: it WAS built (24p). DV1 fixed it for 0.92.5 (item 18, RV13 PASS 81e9065c): parts set aside, flag 'promoted', newer arrows, cabin walk mid-job. User's question "when is it": test Day 9-10 once rep "Relied on" + m6 trained; summons next day 11:00; ceremony the day after 17:15.
- Crew stories: explained to the user (written, CS1-passed, claude/crew-stories-pitch; reading page 2MdTVzoD5J1ectdZb1zqf5); **offered** a two-stage build after 0.92.5 (6 ready now: Pell, Theo, Basil, Halloran, Kovac, Saad; later Zeke/Calder/Raman/Kowalczyk wait on Engine Specialist, Calder's question, comet, night shift). **No answer yet.**

## 0.92.5 in progress (plans/patch-0.92.5.md; BM16 builds claude/staging-0.92.5 from ba836359)
In staging (all PASS): items 1 (FX9 walk), 5 (FX13 no-repeat + ZW1 words), 6+7 (FX9 piano/lounge), 18 (DV1 promotion), sim bay ON. Passed, to merge: 2/3/14/17 (FX11 23432122) + 17 revised no-timer (FX11 c97fbef0, RV12 PASS), 11/12/15 (DS1 a99453d8, RV13 PASS), 21 lift flash (FX9 8777fc44, RV12 PASS). Words: ZW1 62f89173 (8, 5, 10; CS1 PASS).
Still open:
- **FX12 items 4, 9, 10** (late piano Tue+Thu 21:40-22:25 with tradToBed; birthday quarter-hour rule; birthday party at the long table + cake slice): claude/p925-fx12 20860227 → RV12 reviewing. FX12 ~58%, idle after (plans/handover-fx12.md).
- **Arrows week FAIL Day 9 burst pipe (m6)**: follower stuck with FX12's change (also 3866c8f3 + late piano only). **DV1** (session_01GewvUTCXkDVkHsz53ex71o, ~53%) digging, branch from 20860227, reviewer RV12. Blocks the round until fixed or proven test-only.
- **Item 20 Tiles ladder** (FX13, claude/p925-fx13b 5e1d82d5: ring of 9, winner stays, Play/Watch, host by 15:02) → RV12. FX13 idle (handover on claude/fx13-handover).
- **Items 16 + 19 weekend traditions + Cook-along in the galley** (claude/p925-weekend; FX9 session_01WeXGZBS3DyyLqHGpRjWZzA ~44% builds; RV14 session_01RwUYVcYt2PP7B7g3ogduFZ reviews). 8 traditions behind WEEKEND_ON: Saturday run, Garden picnic (garden benches), Every song (Sat 17:15, Zeke), Night owls' cocoa (host Kofi Mensah), Bread day, big jigsaw (host Dev Raman, Vance drops in), Gerald clinic, Sunday story (Holt). Words SW1 claude/weekend-words-sw1 faac7054 (CS1 PASS final). Attendance via shared tradToBed (cocoa 6-10, story 7-9). FX9 running full runs; then T5 decor, T6, RV14 verdict. **Question for the user when done: switch WEEKEND_ON on in 0.92.5, or ship dormant?** (lead 34's default: show a #weekend preview first, as with the sim bay, unless the user says just switch it on.)
- 13 DROPPED by the user. 17 revised to no timer.
- Then: BM16 freezes 0.92.5 → six-runner round (OLD = ba836359) → PUB1 updates the 3HqM5…/9ZWAg… pages (as for 0.92.4; confirm with the user) → ask the user's OK to fast-forward integration.

## Seats (session ids)
BM16 session_01MB7n4yvCAeGyWN4WZCAGPh (build master 0.92.5); PUB1 session_01GnpjFR6oumvuvTrmcXSqeg; runners CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv (~55%, handover before next-next round), CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk. Reviewers: RV12 session_013JmdoWWEDQde8y1bwrMGnY (~33%), RV14 (new). Retired/idle with handovers: RV11, RV13, FX4, FX8, FX10 (~60%), FX11, FX12, FX13, FX14. Free with memory: DS1 session_01MZBSf7MZeb9C89wpoavLko (~38%), FX9 (busy), DV1 (busy), writers SW1 session_01Mjn7ezXqrDgXBrdCtddHHJ, ZW1 session_01QY7V7HVtAbiX64cyVKL1Am, CS1 session_01QcPAXHjQZ2HfZKMCTbaW9v.

## Backlog added today
FX8-1 swimmer leaving the pool jumps ~5 tiles; FX9-1 small one-frame snaps on seated crew; FX10-1 "from main storage" wording when the part is made; DV1-1..3 (Day 11 hover cart for 1 crate stuck; Day 12 m8 'brace the housing' stuck; out-of-stock unmakeable part shows 'Look over').

## Gotchas
- Never priority "now". Helpers' shas often aren't pushed when they say "done": check the branch on origin. Force-add PNGs (repo ignores *.png).
- Parallel checks on one machine cause timeouts/false diffs: re-run alone.
- A reviewer at ~55% should hand a big review to a fresh one (RV14 was hired that way).
