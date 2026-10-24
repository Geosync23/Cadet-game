# Handover: lead 32

## START HERE (lead 33)
1. Read CLAUDE.md, this note, then the bottom of TEAM.md on `claude/lead-32` (from "~20:32 UTC: LEAD 32 took over"; the lines from ~03:16 UTC on 2026-10-24 are the current state). Then plans/patch-0.92.3.md (the user's 29 playtest notes, owners, reviewers).
2. Branch: start `claude/lead-33` from `claude/lead-32`. Push only there.
3. Make your own hourly check-in scheduled task (create_trigger, cron, into your session, minute 57), then disable lead 32's `trig_01Ns6SpEXoSHpWyhwLyoJMBY`. Lead 32's two one-shot reminders (trig_01J917EjzHDkn7ZbWtVonAwh 06:30 UTC wind-down; trig_018sATp3wizwbpcvLsF3s317 08:00 UTC cap) fire into lead 32's session: make your own copies with send_later (same times, text below) and then delete lead 32's two with delete_trigger.
4. Message every working seat with your session id (priority "now"; ask for a one-line acknowledgement). Tell lead 32 (session_01GFHMDsQK3TfPfH7Paapyog) you've taken over.
5. **OVERNIGHT MODE**: do NOT message the user (no phone pings). One morning summary when the user is back (plain language, no emojis, US Eastern times).

Lead 32 = session_01GFHMDsQK3TfPfH7Paapyog, branch claude/lead-32; took over 2026-10-23 20:32 UTC; handed over 2026-10-24 ~04:00 UTC (midnight Eastern) at ~57% memory.

## The user's standing rules (new in bold)
- Plain language, no jargon, no emojis; times in US Eastern (EDT, UTC-4). Few messages: published builds, questions only they can answer, milestones. Remind them of everything built but switched off when next steps come up (now: the controller).
- Deadlines are goals; quality first. Full round on six runners for every game change. Memory: judge from ~60%, never above 80%.
- **Hiring:** the user lets the lead hire workers (fixers, reviewers, testers, writers) and start the next lead itself; hire only what's needed; record every hire in TEAM.md; brief each fully (role, branch, what to read, reviewer, who to report to, memory rule; new sessions attach the repo with add_repo owner Geosync23 repo Cadet-game access push, clone, register_repo_root).
- **OVERNIGHT (the user, 03:27 UTC 10-24, "off to bed"):** keep going; **at 4 AM Eastern (08:00 UTC) at most 10 workers working at once**, intelligently; wind down early so workers finish by 4 AM, but if not, let them finish. Idle seats don't count; the lead isn't counted. No messages overnight; one morning summary.
- No more automatic (FE) playtests for now: the user playtests themselves.
- Findings page items 51-81: "Not a problem" (the user's answer).
- Crew stories: WRITTEN (all ten PASS; reading page https://claude.ai/artifact/2MdTVzoD5J1ectdZb1zqf5; combined on claude/crew-stories-pitch 9e95786b; build notes plans/crew-stories-build-notes.md). They go into the game **later, separately** (the user). NOT in 0.92.3.

## Pages
- Playtest https://claude.ai/artifact/Wn6mUGcxatoWVqhCNTa1vs and Dev https://claude.ai/artifact/6daNCLCJAcsLCZn27CEthq: **Version 11 = 0.92.2** (claude/integration 364c80cb, game sha256 ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4), published 00:54 UTC 10-24.
- Findings https://claude.ai/artifact/7GFQ8pZZxmZnTW3o6RHd6k (51-81 Not a problem).
- Rec room pitch https://claude.ai/artifact/SFBYiCUXgBh7C2EnKWi4xW (decided: idea 4).
- **Sim bay plan for the user's morning answer:** https://claude.ai/artifact/Hmg44se58wGkZaGCMFyRWL (FX14 idle until the user answers; answers in its db, collection answers, doc user).

## 0.92.3 (in progress; BM15 session_01EH5qkoYriK2Gsrp7hHRoso, claude/staging-0.92.3 from 364c80cb)
In staging: DEV_NOTES refresh; FX13 own-talks engine bc976e7d (RV13 PASS + section 20 sign-off); item 15 talk content (CS1's 22 files from stories-sw1 01293d50, sw2 bf1496ff, sw3 15215f8f; 575 talks; NO crew-story files). Checks running.
Pieces (see plans/patch-0.92.3.md):
- DS1 claude/p923-ds1 (1, 7, 8, 9, 10) → RV11. AC3 claude/arrows-c 55ec3474 (6 only: Days 1-3 clock-in tip + auto-track; ~64%, handing over after) → RV12.
- FX4 claude/p923-fx4 (2, 12, 14, 20, 26 incl. ZW1's words 0c0ea582 + 69aaa40e) → RV11. **The "Schedule tracker" rename (14) merges first** with every check updated.
- DV1 claude/p923-dv1 6aeae8c1 (13, 23) → RV13; Zeke's explain lines SW2 2bd054f3 (on bf1496ff; CS1 recheck) go in with DV1's merge.
- FX8 claude/p923-fx8 (22: tap the person you have a due appointment with keeps it; 28: no magic: galley crew walk in from 05:29) → RV11. **Offer for the user (morning):** smooth the ~0.7-tile hop when crew get up from a place (all crew, section 10).
- FX9 claude/p923-fx9 needs (approved: fitness 1.4/0.35, leisure 2.4 awake + work extra 3.0, social 4.5/0.5, hunger asleep 6) → RV12.
- FX10 claude/p923-fx10 (21, 24, 29: 194 'fix' small repairs, 66 science, two rotations, FIX_ON; ZW1 words f849588d; machine_check repairs-share line widened to Days 2-28 as a test-only commit, lead's ruling) → RV13.
- FX11 claude/p923-fx11 (17 swim camera follow; 25 light disc rally + lone practice, visual only; 16 lockers tip with AC3's one-liner) → RV13.
- FX12 claude/p923-fx12 (19: the tray now travels off Deck 3 [lead's overnight call, reversible: confirm with the user] + drawn in hand during activities; 27: pick-your-own gives a tray + arrow) → RV12.
- Then the six-runner round (CR1-CR6 idle and ready; OLD = 364c80cb), your go, PUB1 publishes Version 12.

## Seats (session ids)
- BM15 session_01EH5qkoYriK2Gsrp7hHRoso; PUB1 session_01GnpjFR6oumvuvTrmcXSqeg.
- Runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk.
- Reviewers: RV11 session_01EdBKAgQFMexMSs3JbgH5H7 (DS1, FX4, FX8), RV12 session_013JmdoWWEDQde8y1bwrMGnY (AC3, FX9, FX12), RV13 session_016ioWtxM6NJRV4Ck3ADwozc (DV1, FX10, FX11, FX13, FX14).
- Builders: DS1 session_01MZBSf7MZeb9C89wpoavLko; AC3 session_01DiLRzrXgkeoAZCoX1mVJn9; FX4 session_01BueJ4UzQkn8HcC1TXd1KrW; DV1 session_01GewvUTCXkDVkHsz53ex71o; FX8 session_01GQ33Xh5J5WxwXieiWPwPq1; FX9 session_01WeXGZBS3DyyLqHGpRjWZzA; FX10 session_01Sb2kaWj2xPBRQC4o7FkLSo; FX11 session_016StvTZyiC644u21Q1ZUR3c; FX12 session_01DfkfrfvdT2bW2Q1Y7b2AA5; FX13 session_01KVmjkTUis1ktZ3U7Ryc3jr; FX14 session_01LHwo6kgrymCA7rBdacbqXe (idle: sim bay waits for the user).
- Writers (all idle now): CS1 story lead session_01QcPAXHjQZ2HfZKMCTbaW9v; SW1 session_01Mjn7ezXqrDgXBrdCtddHHJ; SW2 session_017dLaLFBnRUQin3PQEQq6so; SW3 session_01MRMAfR4taMKEXeR5qa4Wpq; ZW1 session_01QY7V7HVtAbiX64cyVKL1Am.
- Idle/done: PW1, CP5, FX6, FX3 (stopped), FX7 (stopped), RV10 (stopped), CTT4 (stopped), BM14 (stopped), lead 31.

## Reminder texts (for your send_later copies)
- 06:30 UTC: "Wind-down start: at 4 AM Eastern (08:00 UTC) go down to 10 workers working at once, intelligently; tell seats whose work won't finish by 08:00 to reach a clean push point; start no new non-priority work; plan which 10 keep going (0.92.3 pieces + their reviewers + BM15 first; the six runners count when the round runs). Overnight mode: no messages to the user."
- 08:00 UTC: "4 AM Eastern: cap 10 workers working at once (idle seats don't count; lead not counted). Let anyone mid-task finish; start nothing that takes it over 10. Record in TEAM.md. No messages to the user."
Note for the cap: the six-runner round needs BM15 + 6 runners = 7; schedule it so builders/reviewers are mostly done first.

## Morning summary for the user (when they're back)
0.92.3 status (published or not, what's in), the sim bay plan link + its questions, FX8's hop offer, FX12's travelling-tray call (confirm), FX10 machine_check ruling, crew stories still waiting to go in separately, the controller still off.

## Gotchas learned (lead 32)
- Seats' self-reported memory can be wrong; check get_session context_usage.
- Messages cross: two seats fixed the same thing three times tonight (Kovac line, counter recheck, dirty-clothes tip). Before assigning, check who owns the line; when moving work, tell BOTH seats and make the old one stop.
- Writers' branches carry several jobs: BM15 takes named files only.
- Facts: quote the game line a number comes from (the breakfast-hours slip, LEAD31-6: breakfast really is 07:00).
