# Starship Cadet: team board

The project lead session keeps this file current. A new lead session reads it first, together with CLAUDE.md and DEV_NOTES.md.

**Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG, branch `claude/lead-pillar1` (took over 2026-10-17 ~02:40 UTC, at the 0.60.0 gate of Pillar 4, from session_01PxXKwc5mkC7tV5MPi3p7PP; brief: `plans/handover-lead.md`). Repeating hourly check-in: trig_018pRJUMKQr75nKGDHN7ovUp (fires :40). Starts and briefs helper sessions, releases builds, and keeps this board and the dev notes up to date.

**Retired leads:** session_01PxXKwc5mkC7tV5MPi3p7PP (2026-10-16 ~21:40 to 2026-10-17 ~02:40, Pillar 3 to 0.41.10 and Pillar 4 wave 1a, handed over at ~64% memory before the 0.60.0 release; `plans/handover-lead.md`); session_015QoyPWBdMPM4ywf5W2jMMs (2026-10-16 ~15:20 to ~21:40, Pillar 3 to 0.41.8, handed over at ~58% memory before 0.41.9; `plans/handover-lead.md`); session_01WHXNp9A1WHAD2EHJw384Qp (2026-10-16 ~04:20 to ~15:20, answers pass and Pillar 3 start, handed over because its memory was full; `plans/handover-lead.md`); session_0158BCCswtdujm3t5d2LXsFz (handed over 2026-10-16 ~04:20 to keep a clean memory; `plans/handover-lead.md`); session_01HV1JuhWgKASQNmvLA2AXD3 (branch `claude/mobile-session-linking-3es9z2`), handed over 2026-10-15 because its context was getting long. Helpers report to the new lead.

**Integration branch for Pillar 1:** `claude/ship-integration` (= `main`, 707b696, at the start). Combined builds are numbered 0.23.0, 0.24.0 and so on. Pull requests to `main` only when the user approves a milestone, and merged only with their OK.

**Ship integration 0.60.0 "the writers' kit"** (e3ee66b, 2026-10-17 ~02:53): Pillar 4 wave 1a: sim bus + flags + Day 0, device 0.35.20, systems 0.33.37, social A to 0.36.43, social B 0.39.0, traditions to 0.34.24 (loader, seasons, Sowing morning), dialogue 0.43.0 (the writers' kit; Torres baked), arrival 0.42.6. All checks pass; cadet_test identical to 0.41.10. Published to a NEW link (the user's choice, 03:02): https://claude.ai/artifact/FYGHHcT6kc21Hu6BvFphSG version 1. Next: 0.60.1; wave 1b hired.

**Ship integration 0.41.10** (6d91ee1, 2026-10-16 ~23:45): draw calls packed with the same picture (crowd-render 0.27.20-0.27.24; end-of-test calls 358 -> 217), the garden you can see growing (all 15 beds), root beds and a second bean trellis (decks 0.38.7). All checks pass. Published: link version 18. Next: Pillar 3 check-in 1.

**Ship integration 0.41.9** (098e922, 2026-10-16 ~23:00): bathroom need, "+N Need" notes and progress bars, the zoom-out limit (kept by the user), the storm's look and feel, the working garden (grow lights, gardeners, daily pick, carry run, fresh produce), Schedule fix, goal arrow hides under the progress bar. All checks pass. Published: link version 17 = 0.41.9. Next: 0.41.10 with crowd-render 0.27.20-0.27.22 (draw calls halved zoomed out), then Pillar 3 check-in 1.

**Ship integration 0.41.8** (7dd0aa4, 2026-10-16 ~21:33): the user's tweaks — job board on screen with jobs held for you, ship health panel, two days off, Roster, Maps without people, no swipe-to-open, the Schedule only lists what happens, friendship seating; visit still draft. All checks pass. Publishing (publisher session_01TUkgk8CFyttKRa371emQBd).

**Ship integration 0.41.7** (d89a3f5, 2026-10-16 ~20:52): **the ion storm switched on** (day 10 of a new game), occasions, one party via eventPlan, storm routines, patient beds, trays timing, chore props, social arcs and dramas, device apps to 0.35.13. All checks pass. Publishing to the link (publisher session_01LibC3b2PPyHrg7asNMsEb1).

**Ship integration 0.41.6** (9bb9409, 2026-10-16 ~16:55): device 0.35.0-0.35.7, social to 0.36.6, the treadmill fix (0.28.17-0.28.18), job-loop tips, galley storm scores, events 0.34.10, decks to 0.38.3, crowd-render to 0.27.17, crew designer to 0.16.10. All checks pass. Next: 0.41.7 with the storm switched on.

**Closing sessions (the user, 2026-10-16 ~22:30):** the lead may archive finished, idle helpers whose work and handover notes are pushed (`.claude/settings.json` allows it). Archived sessions are kept and can be reopened.

**Pillar 4 started (2026-10-17 ~00:45 UTC)** from the final plan (`plans/pillar4-plan.md`, seats in Part 6; `plans/social-deep-plan.md`). Wave 1a (hooks first): seats 1-6 and 9 = onboarding, dialogue, social A, social B, traditions (new sessions), sim engineer 2 and the crew designer (existing). Gate: combined 0.60.0 "the writers' kit". Then wave 1b: head writer, 3 writers, 3 tradition designers. The old social engineer session_01DzZ669spGpdSdVMYzUog2N stays on standby for questions, then closes.

**Pillar 4 direction (the user, 2026-10-16 ~23:00):** a massive pass: full arrival and first week, much more dialogue, a deep social system, many more traditions; ~15 helpers. Notes: `plans/pillar4-notes.md`. The Pillar 4 planner and the social system designer plan it now; nothing is built until the user approves the plan.

**Helper limit raised (the user, 2026-10-16 ~21:33, after upgrading their plan):** up to about a dozen helpers working at once, plus extra check runners, to finish faster.

**New tweaks from the user (2026-10-16 ~21:10):** zoom-out limit (performance engineer, last job), bathroom need + feedback + progress bars (player engineer 2), a garden that grows food for the galley (galley engineer leads; sim, crew designer, systems help). The user also allowed extra check-runner sessions to speed up testing.

**The user's focus (2026-10-16 ~20:25):** the events engineer finishes the diplomatic visit (kept draft) and then stops; the comet viewing and the remaining events wait for later. Everyone else finishes the user's tweaks (job board, ship health panel, days off, Roster, device pop-up bug) and the personal device. Then the Pillar 3 check-in.

**Closed sessions (2026-10-16 ~16:40, the user's clean-up):** all retired leads and helpers were archived (their work is pushed and their handover notes are on their branches): the three earlier leads, the first sim and device engineers, events 1, the Pillar 3 planner, and the bridge, command and Deck 6 architects. An archived session can be reopened if ever needed. Check-runner sessions are archived as soon as they report.

**Test branch (approved by the user 2026-10-16):** `claude/integration-test` holds unfinished, unchecked combined attempts (the lead's lead-wip) so helpers can reproduce and fix failures on their own machines in parallel, and check-runner sessions can run one check each at the same time. Helpers never push to it. Only builds that pass every check go to `claude/ship-integration`.

**Playable build (the one link the user uses), from 0.60.0:** https://claude.ai/artifact/FYGHHcT6kc21Hu6BvFphSG, published by the lead session_01PJtmxWgAPLebXSZKP6ZRpG from its scratchpad file `pub/starship-cadet.html`. Why a new link (2026-10-17 ~03:00): replacing a page from a session that didn't publish it requires reading the whole live page first, and at ~1.5 MB (~770k tokens) that no longer fits in one session. So the LEAD that published the link republishes it itself (same file path = same link, no read needed). A new lead can't update it in place: it publishes a fresh link and tells the user (the user chose "new link" over deleting). The old link https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y stays on 0.41.10 (version 18) for the Pillar 3 check-in.

## Chain of command (the user, 2026-10-17)

**The user → the lead → everyone else.** The lead is directly under the user, reports only to the user, and is the ONLY session that talks to the user. No helper ever contacts the user (no messages, no notifications); anything for the user goes to the lead.

The lead keeps the highest level of organisation: what gets built and in what order, hiring and retiring, design calls, releasing builds to `claude/ship-integration` and the playable link, and every report to the user. The support roles do the hands-on work and report up:

| Reports to the lead | Who reports to them | What they send the lead |
| --- | --- | --- |
| Build master | check-runner sessions | each combined candidate: what's in, every check result, explained differences, the hash to release |
| Reviewer 1, reviewer 2 | — | every verdict (PASS / PASS WITH FIXES / BLOCK) with its note |
| Head writer (from wave 1b) | the three writers | each merged batch, the Voices sampler, anything needing a decision |
| Traditions engineer | the three tradition designers | collected traditions, the calendar page, open questions |
| Social system designer, Pillar 4 planner | — | design rulings and plan changes |
| Every engineer seat and on-call helper | — | each push (commit, checks, memory %) |
| Phone-speed watchdog | — | perf_check results for each combined build |

Rules: helpers coordinate sideways directly (that's encouraged), but decisions that change the plan, a seat's scope, or the design go up to the lead; a manager (build master, head writer, traditions engineer) summarises for the lead rather than forwarding everything; the lead's word settles disputes between seats.

## Staffing levels (the user, 2026-10-17): how to scale up and back down

The user asked for a bigger team now, and for a ready way back to a smaller one if usage needs reining in. The lead switches levels in one step: tell the user, message the roles below, update this section's "Current level".

**Current level: Full** (from 2026-10-17 ~01:15 UTC).

| Level | Who is active | Who merges and checks | When |
| --- | --- | --- | --- |
| **Full** | All Pillar 4 seats in their waves + **build master** + **2 adversarial reviewers** + **check-runner pool** (short-lived) + performance engineer 2 as **phone-speed watchdog** (+ playtester from wave 2) | Build master combines and checks on `claude/integration-test`; reviewers review each branch before it's combined; the lead approves and pushes `claude/ship-integration` and publishes | Now |
| **Normal** (the structure before 2026-10-17 01:15) | Pillar 4 seats in their waves only | The lead combines with a background helper in `/home/user/si-work` (branch lead-wip), check runners only when needed | Usage getting high |
| **Lean** | The lead + at most 3-4 seats (the ones on the critical path of the current wave); everyone else on standby (idle, handover note current) | The lead combines; checks run one at a time | Usage must drop sharply |

**Scaling down from Full to Normal (the lead):**
1. Build master: finish the current combine, push its state to `claude/integration-test`, write `plans/handover-build-master.md` (what's merged, what's pending, check results), then idle; the lead archives it. The lead takes merging back with a background helper in `/home/user/si-work` (`git worktree add -B lead-wip /home/user/si-work origin/claude/ship-integration` if missing).
2. Reviewers: finish the review in hand, post findings to the lead, then idle and are archived. Helpers self-check against the reviewer checklist (`plans/review-checklist.md`, written by the reviewers in their first turn).
3. Check-runner pool: stop starting new runners; archive the ones that reported.
4. Watchdog: performance engineer 2 goes back to on call.
5. Playtester (if hired): write its findings, idle, archive.
Nothing is lost: every role's work is on its branch and in its handover note, and archived sessions can be reopened.

**Scaling down to Lean:** as Normal, then pause every seat not on the current wave's critical path (message: "finish your current turn, push, update your handover note, idle"). Writers and tradition designers pause first (their work is text and waits safely), then on-call helpers. Resume by messaging them.

**Scaling back up:** reverse the steps; reopen archived sessions or hire fresh ones from the handover notes.

## Rules for helper sessions

- One job per session, one branch per job. Touch only the files the brief names.
- `starship-cadet.html` has several writers in Pillar 1, each limited to its own sections (see `plans/pillar1-plan.md`). The lead merges.
- Follow CLAUDE.md "How we work". Plan pages live in `plans/`.
- Report to the lead with `send_message` after each push: files, what changed, open questions.
- The user sends every request through the lead, and the lead hands out the work.
- Before closing a session, the lead checks that it's idle and has no unfinished request.
- **Resume fast after a usage limit (the user's rule, 2026-10-16).** The account's usage limit stops the lead and every helper at once. The lead keeps a REPEATING hourly check-in (create_trigger with a cron, e.g. trig_01NKBjg2UJa1tXFjWU5Zd29L), never only a one-shot reminder (a one-shot that fires while blocked is lost: that cost 2.5 hours on 2026-10-16). Each check-in resumes stopped workers, nudges stalled helpers, and carries on.
- **Handover before auto-summarizing (the user's rule, 2026-10-16).** The user prefers our handover method to the automatic summary. Every session (lead and helpers) warns early when its memory is getting full, or when the next task looks big enough to fill it: helpers tell the lead, and the lead tells the user in plain words. Don't wait for the automatic summary. **When (the user's rule, 2026-10-16 evening):** helpers hand over at about **70% of memory** (about 700k of 1,000,000). The lead is different: before each bigger step (a new combined build, a check-in, a new pillar or plan), it checks how much memory it has left and whether that step fits; if it doesn't, it hands over first, so a step never starts that can't be finished. Then write a handover brief for a fresh session in our usual style (role, branch, build numbers, current state, open work, the user's decisions, how to test) and keep TEAM.md current, so the new session starts clean.

## Roster

Pillar 2, all started 2026-10-15 (see `plans/pillar2-plan.md` for the workstreams, formats and build numbers). A helper session can only push to the branch it was created with. Pillar 1 (done, 0.25.2) roles are in git history.

| Session | Job | Branch it pushes to | Builds | Status | Handover note |
| --- | --- | --- | --- | --- | --- |
| session_01PJtmxWgAPLebXSZKP6ZRpG | Lead (from 2026-10-17 ~02:40). Publishes the playable link itself (https://claude.ai/artifact/FYGHHcT6kc21Hu6BvFphSG, version 1 = 0.60.0; see "Playable build" above) | `claude/lead-pillar1` | 0.60.x (combined) | Active | — |
| session_01PxXKwc5mkC7tV5MPi3p7PP | Lead (2026-10-16 ~21:40 to 2026-10-17 ~02:40) | `claude/lead-pillar1` | 0.41.9–0.41.10 (combined) | Retired 2026-10-17 (~64%) | `plans/handover-lead.md` |
| session_015QoyPWBdMPM4ywf5W2jMMs | Lead (2026-10-16 ~15:20 to ~21:40) | `claude/lead-pillar1` | 0.41.5–0.41.8 (combined) | Retired 2026-10-16 (~58%) | `plans/handover-lead.md` |
| session_01WHXNp9A1WHAD2EHJw384Qp | Lead (2026-10-16 ~04:20 to ~15:20) | `claude/lead-pillar1` | 0.41.x (combined) | Retired 2026-10-16 (memory full) | `plans/handover-lead.md` |
| session_0158BCCswtdujm3t5d2LXsFz | Lead (2026-10-15 to 2026-10-16 ~04:20) | `claude/lead-pillar1` | 0.40.x–0.41.2 (combined) | Retired 2026-10-16 (~460k) | `plans/handover-lead.md` |
| session_01TqLepvhqDZRwFj7ZuLb6Xa | Systems engineer 3 (hired 2026-10-16 ~20:22): empty job board (with interactions), days-off jobs to crew (section 17) | `claude/ship-systems` | 0.33.32–0.33.39 | Archived 2026-10-17 ~02:43 (done; head aca0102) | `plans/handover-systems.md` |
| session_01R6RBwwBM9aorpsqDCrztDU | Sim engineer 2 (Pillar 3, hired 2026-10-16 ~15:30): guest schedules fix (0.26.15), C7 storm routines, seating by friendship (sections 10, 13, 14) | `claude/sim-engineer` | 0.26.15+ | Active | — |
| session_01S5xTHRBpJ9kqytfrwKipUG | Sim engineer: crew time, schedules, needs, day_check (sections 10, 13, 14) | `claude/sim-engineer` | 0.15, 0.21–0.22, 0.26.x | Retired 2026-10-16 | `plans/handover-sim.md` |
| session_01TiBtENVFJV7RqEQ7YkxH1Z | Performance engineer: crowd, poses, props, draw calls (sections 8, 8b) | `claude/crowd-render` | 0.20, 0.27.x | Retired 2026-10-16 ~21:30 (~60%; final 0.27.18 eeffedf) | `plans/handover-performance.md` |
| session_015BoZMMp5b4A4F51dMcZ3ax | Bridge architect: Decks 1 and 3 | `claude/deck1-scale` | 0.18, 0.31.x | Retired 2026-10-16 (Pillar 3 restaffing) | `plans/handover-bridge-architect.md` |
| session_01JScnVG158eYAHYvKDz3jZG | Crew designer: roster, habits, generator (section 9) | `claude/deck-plans-1-2-6` | 0.16.x | Archived 2026-10-17 ~02:44 (done; 0.16.13 98df62f, note 03e77eb) | `plans/handover-crew-designer.md` |
| session_01FtwFYLBjAB9zFvPSpLezaR | Systems engineer (new, answers pass): faults for the player, visible faults hook, tiers, machine taps, shortages to Mail, cart job (section 17) | `claude/ship-systems` | 0.33.16–0.33.31 | Retired 2026-10-16 ~20:20 (~64%; final 6065854) | `plans/handover-systems.md` |
| session_0134zewqwGV9hdGK6PqsaZ36 | Systems engineer: machines, wear, jobs, supplies, carts (section 17) | `claude/ship-systems` | 0.33.x | Retired 2026-10-16 (~600k) | `plans/handover-systems.md` |
| session_01MiQtjmdEa4CXsCsiCh6zWV | Deck 6 architect (new, answers pass): Decks 4-6, hull byFace 4-5, health board, tiers, plates, crawl tiles, cargo hatch, touches | `claude/deck-architect` | 0.30.11+ | Retired 2026-10-16 (Pillar 3 restaffing) | `plans/handover-deck6-architect.md` |
| session_01UFZoEaoHa3Tz1RrypCRzNx | Deck 6 architect: Decks 4, 5, 6, utility kit, deck_check | `claude/deck-architect` | 0.17, 0.30.x | Retired 2026-10-16 (~690k) | `plans/handover-deck6-architect.md` |
| session_01XAkY9U3mmstHQT2yAMTocA | Performance engineer 2 (hired ~21:33): the storm's look and feel (shake, flicker, sky moods, coarse crowd at gatherings), then zoomed-out decor thinning (sections 8/8b, camera); from 2026-10-17 the PHONE-SPEED WATCHDOG for every combined build + Pillar 4 on-call rows | `claude/crowd-render` | 0.27.19+ | Active | — |
| session_012J4ctzJgFRBaUFU5sJvega | Player engineer 2 (hired 2026-10-16 ~21:14): bathroom need, need-fill feedback, progress bars for timed activities (section 15) | `claude/player-needs` | 0.28.19-0.28.25 | Retiring 2026-10-17 (~62%; handover 933e87b) | — |
| session_01BQjtEzvKXuvPZNzGRRRwpZ | Player engineer (new, answers pass): long days, bed skips night, need bonuses, Mail, social, shopping, crouch (section 15) | `claude/player-needs` | 0.28.9+ | Retired 2026-10-16 ~21:15 (~57%; handover current at c7aab82/bf5b5af) | `plans/handover-player.md` |
| session_01Q9xiH4P2jjftpwBSrMyr42 | Player engineer: player needs, device, job loop, save (section 15) | `claude/player-needs` | 0.28.x | Retired 2026-10-16 (~560k) | `plans/handover-player.md` |
| session_01AVGVnj4Q1jFmVoD6xi5asT | Galley engineer (new, answers pass): spoilage, menus, queues, birthday cakes (section 16) | `claude/galley-food` | 0.29.11–0.29.25 | Archived 2026-10-17 ~02:43 (done; 531c7d9, note e1390c2) | `plans/handover-galley.md` |
| session_0182LPGeQR8Cix6rhf6op5Qv | Galley engineer: cooking, servery, food by cart (section 16) | `claude/galley-food` | 0.29.x | Retired 2026-10-16 (~490k) | `plans/handover-galley.md` |
| session_01EhJv6dqovqhQyruMveFuRR | Command architect (new, answers pass): Deck 2 plates, observatory night, window seats, touches, wear | `claude/deck2-command` | 0.32.3+ | Retired 2026-10-16 (Pillar 3 restaffing) | `plans/handover-command-architect.md` |
| session_014DMHpLuFyNknrAcZZGGNhU | Command architect: Deck 2 | `claude/deck2-command` | 0.19, 0.32.x | Retired 2026-10-16 (~670k) | `plans/handover-command-architect.md` |
| session_01YXDbUmtB1mg4kiJyuToqKA | Events engineer (new): small recurring ship traditions, Stardew-style (section 18 SHIP EVENTS, events_check.py) | `claude/ship-events` | 0.34.x | Working | — |
| session_01FvJicF3TPx3ZV84fiZGUyU | Pillar 3 planner (new): drafts `plans/pillar3-plan.md` (device, ship-wide events, social, progression); no game code | `claude/pillar3-plan` | — | Retired 2026-10-16 (Pillar 3 restaffing) | — |
| session_01GGbtSiy4tDygCzrSUBDMYa | Interactions engineer (new): player can use everything the crew use, job-board pick and take, on-screen goal arrow (section 15b) | `claude/player-interactions` | 0.37.x | Archived 2026-10-17 ~02:44 (done; 0.37.8 6492ead) | `plans/handover-interactions.md` |
| session_014TpEMbWarRFJM8BHC9WM8c | Device engineer (Pillar 3, new): the device's two layers, the old-school CRT skin, apps, tips look, calendar reminders (section 19, C1/C2/C11/C13) | `claude/device` | 0.35.0–0.35.7 | Retired 2026-10-16 (memory ~410k; final 985ff28) | `plans/handover-device.md` |
| session_01LGbDXmiNuSmR6dPGjRj8mX | Device engineer 2 (hired 2026-10-16 ~15:48): Ship news, people on Maps, Calendar appointments and group meetings, Quiet off shift, phone review (section 19) | `claude/device` | 0.35.8–0.35.25 | Archived 2026-10-17 ~03:28 (done; edb320a; open nit: isFinite → Number.isFinite, 2 places) | `plans/handover-device.md` |
| session_01DzZ669spGpdSdVMYzUog2N | Social engineer (Pillar 3, new): relationships, affinity, news, chat cards, favours, crew seeking you out (section 20, C4/C5) | `claude/social` | 0.36.x | Working (wave 1) | — |
| session_01GW9QtevJxaMQzzCGPBHaxb | Events engineer 2 (Pillar 3): ship-wide events, the ion storm, meetings with dialogue (section 18) | `claude/ship-events` | 0.34.8+ | Archived 2026-10-16 ~22:30 (done; events paused by the user) | `plans/handover-events.md` |
| session_014PT5L2QxXYoVhqFP7qhj3y | Deck architect (Pillar 3, all six decks; replaces the bridge, command and Deck 6 architects): gather places, event dressing and traces, ready room, gym kit (C9) | `claude/decks-p3` | 0.38.0-0.38.9 | Retired 2026-10-17 ~01:40 (~55%; handover e8eb838; archived) | the three architect handovers |
| session_01KLFXcNJztCSVLXunD8Jt7R | Pillar 4 planner (hired 2026-10-16 ~23:00): drafts plans/pillar4-plan.md + .html (arrival and first week, dialogue at scale, traditions, staffing); no game code | `claude/pillar4-plan` | — | Active | — |
| session_01SMfS1WKqzQ93X6zyZ7NFpJ | Social system designer (hired 2026-10-16 ~23:00): designs the deep social system, plans/social-deep-plan.md, with the Pillar 4 planner; no game code yet | `claude/social-design` | — | Active | — |
| session_01KaHzfqSqF8B4bkNFrH1tsx | P4 seat 1, Onboarding engineer: arrival and first week, section 21, intro_check.py | `claude/arrival` | 0.42.x | Active (wave 1a) | — |
| session_01UmrVVpV7eBqEsa4sBucASP | P4 seat 2, Dialogue engineer: the writers' kit, section 22, content_gen.py, lines_check.py | `claude/dialogue` | 0.43.x | Active (wave 1a) | — |
| session_012pK2XVi5UhqEd28fakYk68 | P4 seat 3, Social engineer A: section 20, steps A1-A11 (fresh session for the social role) | `claude/social` | 0.36.20+ | Active (wave 1a) | `plans/handover-social.md` |
| session_019aEJaAGyZir9oq47CBRfA3 | P4 seat 4, Social engineer B: sub-block 20c social stories, steps B1-B6 | `claude/social-stories` | 0.39.x | Active (wave 1a) | — |
| session_018WZccmSvEfz2LC7DCfxdii | P4 seat 5, Traditions engineer: section 18, .trad loader, seasons (fresh session for the events role) | `claude/ship-events` | 0.34.19–0.34.34 | Archived ~04:31 (handover ad30f96) | `plans/handover-events.md` |
| session_01WEEoe5DyRegEqVMZgKRHWB | P4 seat 5, Traditions engineer 2 (hired ~04:31): section 18, collects the designers' files; first job the bridge-invite meeting | `claude/ship-events` | 0.34.35+ | Active | `plans/handover-events.md` |
| session_012K7RZ3oSX2vpBb1rR66MBh | Build master (Full level): combines and checks Pillar 4 builds 0.60.x, runs the check-runner pool, keeps the hook register; the lead approves and pushes ship-integration | `claude/integration-test` | 0.60.x (combined) | Active | — |
| session_01HK4m33sUiLuVim8VWaCPMs | Adversarial reviewer 1: sim, onboarding, social A/B, crew designer; writes plans/review-checklist.md | `claude/reviews` (notes only) | — | Archived ~04:30 (~70%) | `plans/handover-reviewer-1.md` |
| session_018XY1NbMBxo2SLDPxooe5yx | Adversarial reviewer 1b (hired ~04:30): sim (13/14/10/17), arrival, social A/B, crew, galley, player | `claude/reviews` (notes only) | — | Active | `plans/handover-reviewer-1.md` |
| session_0142TQw4ke8caPSyAC93VT98 | Adversarial reviewer 2: dialogue, traditions, device, decks, tiles, content | `claude/reviews-2` (notes only) | — | Active | — |
| session_016EJg9DempByUCWwpszyWmV | Player engineer 3 (Pillar 4 on-call: kit bag, device lock, gift tags; section 15) | `claude/player-needs` | 0.28.26+ | Active | `plans/handover-player.md` |
| session_01ToE6RJFCw9deB3HcJRLKxS | P4 seat 8, Deck architect 2: seedling pots, Tiles station + boards, postbox, tasting board, lanterns, calm tags, tradition decor | `claude/decks-p3` | 0.38.10+ | Active | `plans/handover-deck-architect.md` |
| session_01DG3in6CvFFta6NrLpoVCJV | P4 seat 10, Tiles engineer (hired 2026-10-17 ~02:51, ahead of wave 3, at the user's ask: two-player checkers + block matching): design page plans/tiles-plan.html first (rules tested by simulation) for the user's approval; then section 23 + tiles_check.py | `claude/tiles` | 0.46.x | Active (design) | — |
| session_016i7YYgZd6puKxfBSkLggRF | P4 seat 11, Head writer (wave 1b, 2026-10-17 ~02:54 to ~04:07): 2,209 lines, 83 cards, 87 overheard, 45 moments, 12 themes | `claude/content` | 0.48.0–0.48.10 | Archived (~70%) | `plans/handover-head-writer.md` |
| session_01HNrh3xCtczeZM5NVFrE6pa | P4 seat 11, Head writer 2 (hired ~04:07) | `claude/content` | 0.48.11+ | Active | `plans/handover-head-writer.md` |
| session_01DbudMKaYgwjL8yDQpe3DFo | P4 seat 12, Writer: Works and the arrival (reports to the head writer) | `claude/writer-works` | — | Archived 2026-10-17 ~03:58 | `plans/handover-writer-works.md` |
| session_01Cf6D2dFZaKspr9mwUnCrBm | P4 Writer 2 (hired ~03:58): takes over Works + command seats (12, 13); reports to the head writer | `claude/writer-works` | — | Active | — |
| session_01HdsVyhcPUgWse8qpaYqKex | P4 seat 13, Writer: command, Survey, Watch, guests (reports to the head writer) | `claude/writer-command` | — | Archived 2026-10-17 ~03:53 (~55%; hire fresh when the head writer asks) | `plans/handover-writer-command.md` |
| session_01DfadYjSP8skcVF72f6JxBw | P4 seat 14, Writer: Commons and juniors, overheard and reactions banks (reports to the head writer) | `claude/writer-commons` | — | Archived ~04:07 (hire fresh on the head writer's ask) | `plans/handover-writer-commons.md` |
| session_01Wr9Jcc4nRUHHWdfJDUwb3X | P4 seat 15, Tradition designer: weekly (reports to the traditions engineer; keys 435-454) | `claude/trad-weekly` | — | Active | — |
| session_015dAEQhLUgkxejuzQF5CsV9 | P4 seat 16, Tradition designer: every few weeks + Sunday Mail (reports to the traditions engineer; keys 455-474) | `claude/trad-monthly` | — | Active | — |
| session_01GnWSW6a2D1XdABqpCpVjaY | P4 seat 17, Tradition designer: seasons, year, life moments (reports to the traditions engineer; keys 475-499) | `claude/trad-seasons` | — | Active | — |
| session_01VTbXtWeydYbfNw8fKLpkz8 | Pillar 5 planner (hired 2026-10-17 ~03:36 at the user's OK): expanded core gameplay + ship-wide events, each standing alone, overlapping Pillar 4 in steps; plans/pillar5-notes.md (questions) then pillar5-plan.md/.html; no game code | `claude/pillar5-plan` | — | Active | — |
| session_018cicfPQZQXbxmtn6ygmL84 | Galley engineer 3 (hired 2026-10-17 ~03:43, Pillar 4 on call): tradition food (tasting table, Saturday pancakes, suppers), simNote('lateMeal') (section 16, food_check) | `claude/galley-food` | 0.29.26+ | Active | `plans/handover-galley.md` |
| session_01LoFBKtu3Q1k1PEr8QPz1b8 | Crew designer 2 (hired ~04:00, on call): roster fields hobby + since, first-person family (section 9 generator) | `claude/deck-plans-1-2-6` | 0.16.14 (4613d43) | Archived ~04:10 (loose end: reserve Priya Kowal's "old rivalry goes back years" line) | `plans/handover-crew-designer.md` |
| session_01AS3Tzju3TuFbM9XAEYdvPX | P4 Writer 3 (hired ~04:16): Commons and juniors, overheard and reactions banks; reports to head writer 2 | `claude/writer-commons` | — | Active | `plans/handover-writer-commons.md` |
| session_01PGFJbAfDYddQRGYQJktgXj, session_012zFHAS6jkPUhCrpBn2zW9Q, session_01USkJjdw16L4K2tuK8otcc6, session_01V5ghkKLy1XQkZkKS9yKUkr, session_01PPVXqo8s4NvK8JkBWt3WoH, session_01L5Bg1nrCfowojNxeVZJHoi | Standing check runners R1-R6 (2026-10-17 ~02:36, the user's ask): R1 cadet_test, R2 day_check, R3 player+interactions, R4 events+intro, R5 food+machine+deck, R6 social+device+lines+content_gen; report to the build master; no pushes | — | — | Active (Full level) | — |
| session_011Gh8MbJgkYYWwWk2s3oA4y | Deck 3 builder | `claude/deck-building-workflow-iayt67` | — | Archived | — |

**Hiring for a retired role:** start a fresh session on `claude/ship-integration`, have it read its predecessor's handover note first, and give it a new branch and build range (the old branch can be reused if the new session is created with it).

## Context check (2026-10-15, 17:10)

How full each helper's memory is (out of 1,000,000): crew designer 84k and Deck 6 architect 199k (both already compacted), bridge architect 570k, command architect 525k, performance engineer 510k; sim engineer not reported while working. Sessions compact themselves automatically, but lose detail when they do. Plan: no new hires for the end of Pillar 1. For Pillar 2, give big new jobs to fresh sessions, and retire the bridge and command architects (idle, work merged) once the user agrees, after the usual idle check.

## Done

- **PR #2 merged into `main`** (4b2ee4f, 2026-10-16 ~13:05, user-approved): build 0.41.4 plus all docs. `claude/lead-pillar1` was restarted from main (its old history was unrelated to ship-integration). Pillar 3 in progress at full speed for ~2 hours (user's call, until the usage reset), then more careful. User's note on 0.41.4: the player should carry a tray when eating like the crew (player engineer, 0.28.15).

- **Pillar 3 started (2026-10-16 ~12:55),** user-approved staffing: wave 1 = device (new), social (new), events (C6, ion storm, meetings), performance (device pose, chatter bubbles), interactions (jobs at the board, tips triggers), systems (turn-in). Wave 2 later: sim, galley, crew designer, one merged deck architect. At most 5-6 active helpers. Playable link is version 12 = 0.41.4. The user wants the timeline pulled in: target check-in 1 within about a day.

- **Ship integration 0.41.4** (c7598df, 2026-10-16 ~12:55): the answers pass, finished. Food supply fixed (crew take every food run), about 5.6 jobs a day left for you, sit anywhere, squeeze past, use what the crew use, the job board and goal arrow, ship traditions, all 267 seats fixed, #crowd-120. All eight checks pass, run in parallel on claude/integration-test by check-runner sessions. Being republished to the playable link.

- **Answers pass started (2026-10-16, overnight):** the user answered the question board and authorised the lead alone to interpret it. Plan: `plans/answers-pass-plan.md`. Five fresh helpers hired for the retired roles; four standby helpers re-briefed. Combined builds 0.41.x. End: a decisions report and the Pillar 3 plan pitch.

- **Helper handovers (2026-10-16):** all nine helpers wrote handover notes (`plans/handover-*.md`, on this branch and on ship-integration 9efcea0, no game changes). The five fullest (systems, Deck 6 architect, player, galley, command architect) are retired; the lead now owns the playable link. Four stay on standby.

- **Plan (the user, 2026-10-15):** finish Pillar 2 and its end-of-pillar review first; hand over to a fresh lead session after that. Pillar 2 is now complete (0.40.8); next: the review to the user, then the handover.

- **Ship integration 0.40.8** (980e6a9): Pillar 2 final. 0.40.7 plus docked carts that hide while out (systems 0.33.15), the crate in the player's hands (player 0.28.8), galley 0.29.10 (food_check line only). All six checks pass; cadet_test ALL IDENTICAL against 0.40.7. Day check: nobody stuck, draw-call peak 422 (Deck 4, budget 450). Republish asked of the Deck 6 architect.

- **Ship integration 0.40.7** (503bf63): food by hover cart (systems 0.33.13–0.33.14, galley 0.29.9, Deck 6 architect 0.30.10, bridge 0.31.5, performance 0.27.5–0.27.6, sim 0.26.7, player 0.28.7). All six checks pass.

- **Ship integration 0.40.6** (952526d): the player's job loop (take a job, inspect, fetch parts, make a part, repair). All six checks pass. Being republished to the playable link. Remaining for Pillar 2: B3 visible (hover-cart restock runs; food by cart only), with the systems, performance and galley engineers. Then the end-of-pillar review.

- **Ship integration 0.40.5** (dc7bb12): Works crew do their jobs on the decks (parts at Deck 5 storage, then the machine's panel), the live Works bay job board, and the device's Jobs section. All six checks pass. Being republished to the playable link. Next: the player's repair loop (the player engineer with the systems engineer), then the end-of-Pillar-2 review.

- **Ship integration 0.40.4** (9c780ff): Pillar 2 Half A complete. All five checks pass (deck, day 7, food, machine, player). Deck 6's engine room is fixed (hull byFace). Works crew walk to jobs. Being republished to the playable link for the user's Half A check-in. Open with the user: hull stripes on Decks 3–5 (smooth them?); how often the player meets real faults.

- **Ship integration 0.40.3** (f15f8e5): utility rooms on all six decks, crew showing activities, the player's dinner queue, machines' background average day. deck_check, day_check, food_check and machine_check OK; player_check failing on the combined build (the player engineer, 0.28.4). Known: Deck 6's engine-room view is 517 draw calls (the performance engineer). Next: B2's visible half (jobWhere, the job board, the device's jobs).

- **Ship integration 0.40.2** (9022006): the player's needs and device (0.28.2), the galley rota live (0.26.2 + 0.29.x + final roster c02e656), utility rooms on Decks 1–4 (0.31.4, 0.32.2, 0.30.2), poses (0.27.x), jobs on paper (0.33.4). deck_check, day_check and food_check OK. machine_check and player_check fail on test stand-ins and the SAVE_EXTRA hook: the player engineer (0.28.3) and the systems engineer are fixing them. Lead merge fixes: sections 15/16/17 in order, SAVE_V 2, the sim engineer's schedData taken whole. (Local attempts kept on branches `lead-wip-0401` and `lead-wip-0402`, not pushed.)

- **Ship integration 0.40.1** (32c8aee): 0.30.2 (Deck 4 utility rooms), 0.27.0 (activity poses), 0.16.5 (storekeepers, galley roles), 0.31.2, 0.33.1–0.33.2 (jobs and supplies on paper, retuned wear). Lead fixes: Deck 4 panel places carry `machine`; schedDesks and stand-ins skip machine panels. deck_check, day_check and machine_check OK. Still to come: the sim engineer's 0.26.2 (galleyDay reader, poseOf wiring, crewPath `who`), then the galley.

- **Ship integration 0.40.0** (4ac34a3): first Pillar 2 combined build. It merges 0.30.1, 0.26.1, 0.16.4 and the storekeepers (WIP bbede16), 0.31.1, 0.32.1 and 0.33.0. deck_check and day_check OK. machine_check flags the recycler wearing too fast; the systems engineer is retuning it. The galley (0.29.0) is held back: combined with 0.26.1, galley staff miss dinner and the rota doesn't match the plans. The sim engineer is fixing that in 0.26.2 on top of both. A local attempt is kept on branch `lead-wip-0401` (not pushed).

- **Ship integration 0.25.2**: 0.25.1 plus 0.22.4 (overflow skips locked or private rooms) and 0.18.4 (two more infirmary places; Rina works in the infirmary). deck_check and day_check OK. All Pillar 1 work done; every helper idle. Next: talk with the user about what's next (Pillar 2, a pull request of the milestone to main, retiring the bridge and command architects).

- **Ship integration 0.25.1** (6180fcf): 0.25.0 plus 0.22.3 (sleep-tap fix, seat heights, playerBed() from ROSTER_PLAYER). deck_check and day_check OK. Being republished to the playable link. 0.22.4 (overflow skips locked or private rooms) in progress.

- **Ship integration 0.25.0** (51ca655): workstream 6 done (0.22.2: full rigs for nearby story crew, day_check.py). deck_check OK, day_check OK (Deck 3 peak 415 draw calls, 69 crew). Being republished to the playable link. Pillar 1's workstreams are all done; next is the end-of-pillar review with the user.

- **Ship integration 0.24.1** (a881bc3): 0.24.0 plus 0.17.2 (bunk texts), 0.21.2 (sleeping) and 0.22.1 (crew follow their schedules on every deck, drawn by the crowd). Merge fix: PLAYER_BED 4-B1-4. deck_check OK. Being republished to the playable link for the user's check-in.

- **Ship integration 0.24.0** (417cf2d): 0.23.0 plus 0.16.3 (player in 4-B1-4) and 0.20.1 (crowd demo, real crew). cadet_test ALL IDENTICAL against 0.23.0; deck_check OK. For the user's check-in once 0.17.2 (Bunk 1 text) is in.

- **Ship integration 0.23.0** on `claude/ship-integration` (c0b9ac9): Pillar 1 workstreams 1–5 combined (0.15.1, 0.16.2, 0.17.0 + 0.17.1, 0.18.3, 0.19.2, 0.20.0, 0.21.1). deck_check OK on all six decks; cadet_test ALL IDENTICAL against 0.21.1 + 0.17.1 alone, so roster, places and crowd are inert. Not yet published to the playable link.

- **PR #1 merged into `main`** (707b696): all six decks (0.14.0), design-doc.md, team setup. Fully approved by the user. The lead branch was restarted from `main` afterwards.
- **Deck 4 guest cabins, build 0.14.0** (2c47c50, now also the head of `claude/ship-integration`): six guest cabins by the lift, two spares, plan page updated. Crew routes unchanged; Decks 1, 2, 3, 5 and 6 pixel-identical; deck_check OK. Waiting on the user's sign-off along with 0.13.0.
- Decided: six senior officers confirmed on Deck 2; six of Deck 4's officer cabins become guest cabins (design-doc.md updated).

- design-doc.md (fd40490) replaces design-doc-v4.pdf (now in archive/) as the single living design document, with the nine pending updates, six decks as built and the Living Ship merged in. Checked by the lead against the PDF.

- **Ship integration 0.13.0** on `claude/ship-integration` (7e95eae): the user's review fixes for Deck 6 (0.11.0) and Deck 1 (0.12.1). cadet_test ALL IDENTICAL against 0.10.1; deck_check OK on all six decks. Waiting on the user's sign-off, then merge into the lead branch and so into PR #1.
- **Ship integration 0.10.1** on `claude/ship-integration`: Decks 6, 1 and 2 (including Deck 2's 0.9.5 hull fix) merged on top of 0.7.4 plus the lead branch. cadet_test ALL IDENTICAL against 0.7.4; deck_check OK on all six decks. Playable: https://claude.ai/artifact/WRus5tYZ5fqSnn8CijmWQ9 ("Cadet Ship Review 0.10.1"). Waiting on the user's review. Merge it into the lead branch (and so the pull request) once the user signs off.
- Deck 2 plan agreed at Sketch 8 (71642e6): array 106, Captain 60, science trimmed. The lead approved it on the user's instruction.
- Deck 2 plan Sketch 7 (df8de84) merged: 52 × 22 on Deck 3's outline, lift [20, 11], looped senior corridor, sensor array cut to 48 tiles, Captain 60. Earlier: Sketch 6 (cd73525). Earlier: Sketch 5 (67b3f8f): 52 × 20, lift [21, 10], 15 bedrooms aft of the lift, science forward.
- Deck 2 plan Sketch 4 (589505e) merged: 12 crew bedrooms plus 2 visitor rooms to port, science to starboard, 50 × 18, lift [21, 9].
- Deck 3 signed off by the user at 0.7.0 ("ok for now").
- Merged the deck plans through 355648a (Decks 1, 2 Sketch 3, 6) into the lead branch, then moved them into `plans/`.
- Merged the Deck 3 builder's branch: Deck 3 turn 5 (crew, 0.6.7), promenade dressing and fixes (0.6.8–0.7.0), the repo tidy (stable file names, `plans/`, CLAUDE.md, deck_check.py).
- Plans for Decks 1, 2 and 6: Sketch 1 (36cce9d, 09f1feb, 68a8bc8); Deck 2 Sketch 2 (b4cfbc6); Deck 2 Sketch 3, 50 × 18 with the Captain's quarters as the biggest room (4fe97c4); Deck 6 reactor door off the lobby (355648a).

## Plan of work (agreed with the user, 2026-10-15)

1. **Build the ship (DEV_NOTES 6e):** Deck 6, then 1, then 2, with a review after each. Deck architect only. Shell, rooms and furniture; no crew or machines.
2. **Then: the Living Ship** (design-doc.md, agreed 2026-10-15). Crew and simulation as one phase, in four pillars: foundation, ship systems and jobs, social, events.

## Overnight plan (agreed with the user, 2026-10-15)

When the user approves the Deck 2 plan, the lead does this without waiting for them:

1. The Deck 6 architect finishes T4 and its review package, then waits for the user's review in the morning.
2. The lead hires two new architect sessions, both starting from the Deck 6 branch (`claude/deck-architect` after T4) so all three decks share one base:
   - **Bridge architect:** Deck 1, branch `claude/deck1-bridge`, builds 0.8.x.
   - **Command architect:** Deck 2, branch `claude/deck2-command`, builds 0.9.x.
   - Each has a separate range of build numbers so their version bumps never clash.
3. Each architect only edits its own deck's parts of `starship-cadet.html` (its `DECKS[n]`, its dress code, new kit for it). They tell the lead before touching anything shared.
4. Each runs every turn of its deck, then stops with a review package and waits. No new deck starts without the user's review.
5. The lead checks in on a timer through the night, steers anything stuck, and builds `claude/ship-integration` with all three decks merged and tested. In the morning the user can play one build with Decks 6, 1 and 2.
6. If the user doesn't answer the Deck 2 plan's open questions: the six invented officers stay as placeholders, and the 15th room stays a visitors' cabin.

## Meeting brief

- "Starship Cadet: Progress and Next Steps": https://claude.ai/code/artifact/d55752dc-5931-4657-8e28-308bd35c22ba (2026-10-15).

## Queue

- **Pillar 2:** agreed 2026-10-15 in `plans/pillar2-plan.md`. Half A and B1 start now. (Pillar 1 is done: 0.25.2.) Earlier: **Pillar 1 of the Living Ship:** the plan is agreed in `plans/pillar1-plan.md`. Workstreams 1, 2, 3 and 5 started 2026-10-15 (no cap on parallel sessions). Next check-in with the user: the roster page plus a crowd demo, once 2 and 5 are done.
