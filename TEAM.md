# Starship Cadet: team board

The project lead session keeps this file current. A new lead session reads it first, together with CLAUDE.md and DEV_NOTES.md.

**Lead:** session_01WHXNp9A1WHAD2EHJw384Qp, branch `claude/lead-pillar1` (took over 2026-10-16 ~04:20 UTC, mid answers pass, from session_0158BCCswtdujm3t5d2LXsFz; brief: `plans/handover-lead.md`). Starts and briefs helper sessions, reviews their branches, merges, and keeps this board and the dev notes up to date.

**Retired leads:** session_0158BCCswtdujm3t5d2LXsFz (handed over 2026-10-16 ~04:20 to keep a clean memory; `plans/handover-lead.md`); session_01HV1JuhWgKASQNmvLA2AXD3 (branch `claude/mobile-session-linking-3es9z2`), handed over 2026-10-15 because its context was getting long. Helpers report to the new lead.

**Integration branch for Pillar 1:** `claude/ship-integration` (= `main`, 707b696, at the start). Combined builds are numbered 0.23.0, 0.24.0 and so on. Pull requests to `main` only when the user approves a milestone, and merged only with their OK.

**Test branch (approved by the user 2026-10-16):** `claude/integration-test` holds unfinished, unchecked combined attempts (the lead's lead-wip) so helpers can reproduce and fix failures on their own machines in parallel, and check-runner sessions can run one check each at the same time. Helpers never push to it. Only builds that pass every check go to `claude/ship-integration`.

**Playable build (the one link the user uses):** https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y, owned by the Deck 6 architect. New builds are republished to this same link.

## Rules for helper sessions

- One job per session, one branch per job. Touch only the files the brief names.
- `starship-cadet.html` has several writers in Pillar 1, each limited to its own sections (see `plans/pillar1-plan.md`). The lead merges.
- Follow CLAUDE.md "How we work". Plan pages live in `plans/`.
- Report to the lead with `send_message` after each push: files, what changed, open questions.
- The user sends every request through the lead, and the lead hands out the work.
- Before closing a session, the lead checks that it's idle and has no unfinished request.
- **Resume fast after a usage limit (the user's rule, 2026-10-16).** The account's usage limit stops the lead and every helper at once. The lead keeps a REPEATING hourly check-in (create_trigger with a cron, e.g. trig_01NKBjg2UJa1tXFjWU5Zd29L), never only a one-shot reminder (a one-shot that fires while blocked is lost: that cost 2.5 hours on 2026-10-16). Each check-in resumes stopped workers, nudges stalled helpers, and carries on.
- **Handover before auto-summarizing (the user's rule, 2026-10-16).** The user prefers our handover method to the automatic summary. Every session (lead and helpers) warns early when its memory is getting full, or when the next task looks big enough to fill it: helpers tell the lead, and the lead tells the user in plain words. Don't wait for the automatic summary. Then write a handover brief for a fresh session in our usual style (role, branch, build numbers, current state, open work, the user's decisions, how to test) and keep TEAM.md current, so the new session starts clean.

## Roster

Pillar 2, all started 2026-10-15 (see `plans/pillar2-plan.md` for the workstreams, formats and build numbers). A helper session can only push to the branch it was created with. Pillar 1 (done, 0.25.2) roles are in git history.

| Session | Job | Branch it pushes to | Builds | Status | Handover note |
| --- | --- | --- | --- | --- | --- |
| session_01WHXNp9A1WHAD2EHJw384Qp | Lead (from 2026-10-16 ~04:20). Also republishes the playable link (https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y, version 11 = 0.40.8; steps in the Deck 6 architect's note, section 3) | `claude/lead-pillar1` | 0.41.x (combined) | Active | — |
| session_0158BCCswtdujm3t5d2LXsFz | Lead (2026-10-15 to 2026-10-16 ~04:20) | `claude/lead-pillar1` | 0.40.x–0.41.2 (combined) | Retired 2026-10-16 (~460k) | `plans/handover-lead.md` |
| session_01S5xTHRBpJ9kqytfrwKipUG | Sim engineer: crew time, schedules, needs, day_check (sections 10, 13, 14) | `claude/sim-engineer` | 0.15, 0.21–0.22, 0.26.x | Working (answers pass, 0.26.8+) | `plans/handover-sim.md` |
| session_01TiBtENVFJV7RqEQ7YkxH1Z | Performance engineer: crowd, poses, props, draw calls (sections 8, 8b) | `claude/crowd-render` | 0.20, 0.27.x | Working (answers pass, 0.27.7+) | `plans/handover-performance.md` |
| session_015BoZMMp5b4A4F51dMcZ3ax | Bridge architect: Decks 1 and 3 | `claude/deck1-scale` | 0.18, 0.31.x | Working (answers pass, 0.31.6+) | `plans/handover-bridge-architect.md` |
| session_01JScnVG158eYAHYvKDz3jZG | Crew designer: roster, habits, generator (section 9) | `claude/deck-plans-1-2-6` | 0.16.x | Working (answers pass, 0.16.6+) | `plans/handover-crew-designer.md` |
| session_01FtwFYLBjAB9zFvPSpLezaR | Systems engineer (new, answers pass): faults for the player, visible faults hook, tiers, machine taps, shortages to Mail, cart job (section 17) | `claude/ship-systems` | 0.33.16+ | Working | `plans/handover-systems.md` |
| session_0134zewqwGV9hdGK6PqsaZ36 | Systems engineer: machines, wear, jobs, supplies, carts (section 17) | `claude/ship-systems` | 0.33.x | Retired 2026-10-16 (~600k) | `plans/handover-systems.md` |
| session_01MiQtjmdEa4CXsCsiCh6zWV | Deck 6 architect (new, answers pass): Decks 4-6, hull byFace 4-5, health board, tiers, plates, crawl tiles, cargo hatch, touches | `claude/deck-architect` | 0.30.11+ | Working | `plans/handover-deck6-architect.md` |
| session_01UFZoEaoHa3Tz1RrypCRzNx | Deck 6 architect: Decks 4, 5, 6, utility kit, deck_check | `claude/deck-architect` | 0.17, 0.30.x | Retired 2026-10-16 (~690k) | `plans/handover-deck6-architect.md` |
| session_01BQjtEzvKXuvPZNzGRRRwpZ | Player engineer (new, answers pass): long days, bed skips night, need bonuses, Mail, social, shopping, crouch (section 15) | `claude/player-needs` | 0.28.9+ | Working | `plans/handover-player.md` |
| session_01Q9xiH4P2jjftpwBSrMyr42 | Player engineer: player needs, device, job loop, save (section 15) | `claude/player-needs` | 0.28.x | Retired 2026-10-16 (~560k) | `plans/handover-player.md` |
| session_01AVGVnj4Q1jFmVoD6xi5asT | Galley engineer (new, answers pass): spoilage, menus, queues, birthday cakes (section 16) | `claude/galley-food` | 0.29.11+ | Working | `plans/handover-galley.md` |
| session_0182LPGeQR8Cix6rhf6op5Qv | Galley engineer: cooking, servery, food by cart (section 16) | `claude/galley-food` | 0.29.x | Retired 2026-10-16 (~490k) | `plans/handover-galley.md` |
| session_01EhJv6dqovqhQyruMveFuRR | Command architect (new, answers pass): Deck 2 plates, observatory night, window seats, touches, wear | `claude/deck2-command` | 0.32.3+ | Working | `plans/handover-command-architect.md` |
| session_014DMHpLuFyNknrAcZZGGNhU | Command architect: Deck 2 | `claude/deck2-command` | 0.19, 0.32.x | Retired 2026-10-16 (~670k) | `plans/handover-command-architect.md` |
| session_01YXDbUmtB1mg4kiJyuToqKA | Events engineer (new): small recurring ship traditions, Stardew-style (section 18 SHIP EVENTS, events_check.py) | `claude/ship-events` | 0.34.x | Working | — |
| session_01FvJicF3TPx3ZV84fiZGUyU | Pillar 3 planner (new): drafts `plans/pillar3-plan.md` (device, ship-wide events, social, progression); no game code | `claude/pillar3-plan` | — | Working | — |
| session_01GGbtSiy4tDygCzrSUBDMYa | Interactions engineer (new): player can use everything the crew use, job-board pick and take, on-screen goal arrow (section 15b) | `claude/player-interactions` | 0.37.x | Working | — |
| session_014TpEMbWarRFJM8BHC9WM8c | Device engineer (Pillar 3, new): the device's two layers, the old-school CRT skin, apps, tips look, calendar reminders (section 19, C1/C2/C11/C13) | `claude/device` | 0.35.x | Working (wave 1) | — |
| session_01DzZ669spGpdSdVMYzUog2N | Social engineer (Pillar 3, new): relationships, affinity, news, chat cards, favours, crew seeking you out (section 20, C4/C5) | `claude/social` | 0.36.x | Working (wave 1) | — |
| session_011Gh8MbJgkYYWwWk2s3oA4y | Deck 3 builder | `claude/deck-building-workflow-iayt67` | — | Archived | — |

**Hiring for a retired role:** start a fresh session on `claude/ship-integration`, have it read its predecessor's handover note first, and give it a new branch and build range (the old branch can be reused if the new session is created with it).

## Context check (2026-10-15, 17:10)

How full each helper's memory is (out of 1,000,000): crew designer 84k and Deck 6 architect 199k (both already compacted), bridge architect 570k, command architect 525k, performance engineer 510k; sim engineer not reported while working. Sessions compact themselves automatically, but lose detail when they do. Plan: no new hires for the end of Pillar 1. For Pillar 2, give big new jobs to fresh sessions, and retire the bridge and command architects (idle, work merged) once the user agrees, after the usual idle check.

## Done

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

## Lead 20 (new account, started 2026-10-20) — finishing the rec deck 0.64.0
Lead: session_019UJSCUCdtC1kTpYiABWKhs, branch `claude/start-here-review-3qoht9`. Briefs from `plans/start-prompts-lead20.md` (on `claude/lead-pillar1`).
| Seat | Session | Branch | Job |
|---|---|---|---|
| Rec engineer RE20 | session_019auXkZkQG3gnNjmArAauLx | `claude/rc-wip` → `claude/rec-cand-s1` | RC's fix, day_check 3-8, item A (Maeve's rides on-shift), item B (career pace), rebase |
| Build master BM10 | session_01KpcQGJvrAz57dmKp6AFg4w | `claude/rec-cand-s1` | the full 0.64.0 check round, DEV_NOTES row, green hash |
| Reviewer R8 | session_01GdhqdLeZuGFQSTX7RL92U5 | `claude/reviews-r8` | reviews RE20's hashes |
| Split architect SA1 | session_019ZX8LqsYayXnK4baFaEs8C | `claude/split-plan` | the step 2 plan page (`plans/split-plan.html`) only; no game edits |
| Split reviewer SR1 | session_011v45ss6jgs29Y68mkhZz35 | `claude/split-plan` (after SA1 hands over) | adversarial review of the plan, then its own pass; `plans/split-plan-review.md` (the user's ask) |
| Split rehearsal SX1 | session_01Ppc31k1KyVmB5tBQKkJTAh | `claude/split-rehearsal` (throwaway) | the user asked to test the plan for real: build the tools, cut a copy, replay real past combines, attack scenarios, a real GitHub check on its branch only, full checks; `plans/split-rehearsal-report.md` |
| Split reviewer 2 SR2 | session_01QraTY3MgjnQdbbeUEQP2ds | `claude/split-review-2` | fresh-eyes review: is splitting right at all vs. process changes without it; `plans/split-review-2.md` |
| Events planner EP1 | session_0183vbQyL2CzMHAS3AZ9kivj | `claude/events-plan` | planning only: the ship-wide events up to the end of the career (the user, 2026-10-20), ion storm audit, `plans/events-plan.html`; an adversarial review follows |
| Ways-of-working WW1 | session_0192KVdPtywdv7sp3mXUXGHU | `claude/ways-of-working` | step 2, no cut: port the rehearsal's checks/tools to the one file, section finder, GitHub check (disabled until the user settles emails), owners/map/backlog, drafts of CLAUDE.md/DEV_NOTES changes; no game edits until the rec deck is published |
After the green hash: the lead has the file read in full and publishes it as a new page "Starship Cadet Rec Deck", then stops and asks the user.
**The user's calls (2026-10-20):** career pace / balance waits for a big balance pass later (item B dropped; career_check's busy-pace fail is known and accepted for now). Fix the wall climb queue bug in 0.64.0 (RE20, item C). The ways of working in `plans/roadmap-after-recdeck.md` are set up in step 2, alongside the file split.
**More of the user's calls (2026-10-20):** a dev mode (move the clock, set career progress, start any ship tradition to test) comes after the split and clean-up; before the split, the whole one-file game is tagged and kept. Both are in `plans/roadmap-after-recdeck.md` (copied to this branch).
**The user's call (2026-10-20):** on phones the Tracked button sits under the Needs bar's left end (option 1 of two mock-ups), under the activity bar when one shows; in 0.64.0 (RE20, item D).
**For the backlog (lead 20, 2026-10-20):** on phones the tip card (.devtip, fixed top 128 px) lies over the needs strip / Tracked / activity bar while it shows (pre-existing; RE20's note). Told the user; not changed in 0.64.0 unless the user asks.
**The user's calls (2026-10-20, later):** no cut for now: step 2 = the new ways of working on the one file (see the roadmap's note). Phone notifications: when the Rec Deck is published, when a decision is needed, and the results of a test or investigation like the split testing; none in overnight mode.
**The user's rules (2026-10-20):** events after the career's end are out of scope but kept on record ("parked"), never deleted, in case we expand. Every plan, survey or results page published for the user leaves a place to comment (and answer questions on the page).
**0.64.2 Rec Deck published (2026-10-20 ~04:55 UTC):** https://claude.ai/artifact/7ZHXGUSvgJzAc1mYmfPt1K from claude/rec-cand-s1 c575a8e (BM10 green, R8 PASS, 8 readers clean). Main and the main game link untouched. Playtest Update 0.63.5 republished on this account: https://claude.ai/artifact/9m3jP4HBL8ix3oyZaJoo9p. Events plan (questions for the user): https://claude.ai/artifact/Qi1Uvev6p4TbPwYFQvRB1P (answers saved in its db, collection `answers`, doc `events-plan`). Split plan (shelved): https://claude.ai/artifact/9v7C1oRCJUUTGkAujsAoUt. Next: WW1's "Later" (slots, whole-file copy, rules), then Dev mode.

## Step 2 (new ways of working, no cut) — status (lead 20, 2026-10-20)
Built by WW1 on `claude/ways-of-working` (928d49a..4bcbaa9 + R8's arc_check fix), reviewed by R8 (PASS WITH FIXES → PASS once the fix lands). Whole file kept: `archive/starship-cadet-0.64.2-whole.html` + frozen branch `claude/whole-file-0.64.2` (c575a8e). Per-seat code slots (17), `names_check.js`, `check_fast.sh` (~5 min, run before every push), exit codes fixed in the checks, `tools/section.py`, `tools/shared.js`, `plans/owners.md`, `plans/map.md`, `plans/backlog.md`, build table moved to `plans/build-table.md`, CLAUDE.md/DEV_NOTES rules (build master sets the build number; early merging into `claude/integration`; owners; the user's two rules), start messages in `plans/start-prompts-step2.md`.
Shared branch: `claude/integration`, started from the reviewed `claude/ways-of-working` tip. Every new seat starts from it; the build master merges reviewed work into it.
GitHub check: ON for every push to claude/** and main (the user, 2026-10-20; the user mutes GitHub's Actions emails, and the lead reports failures that matter).
**Step 2 DONE (2026-10-20 ~05:25 UTC):** `claude/integration` created at 5dd740c (= `claude/ways-of-working` tip, R8 PASS, GitHub check run #1 green in 5 min 30 s). From now on every seat starts from `claude/integration` and follows CLAUDE.md's new rules (check_fast before every push; the build master sets the build number; owners; slots). Next: Dev mode (plan page with answer/comment boxes + adversarial review).
| Dev mode planner DP1 | session_01HvjJKxBhqXwvnVKUfFQCLq | `claude/devmode-plan` (from claude/integration) | step 3 plan page only: clock, career, traditions, jump to any career day, events; adversarial review follows |
| Day-jump engineer DJ1 | session_01Ud7J18L1xbrwMP2yiCiqp6 | `claude/devmode-dayjump` | helps DP1: measures day-jump options, clock jumps, tradition/event start on the real game (the user: "hire help") |
| Dev mode reviewer DR1 | session_01WfFmjT31bVcy4mvsNVi5Mz | `claude/devmode-review-1` | adversarial technical review of the Dev mode plan, runs everything |
| Dev mode reviewer DR2 | session_012GxodCR3fkT9KyQCeLTd4D | `claude/devmode-review-2` | fresh-eyes review: usable on a phone for the user's real tests |
| Patch planner PP1 | session_01QfLuMmrJSgMQ3A4tBtXAmf | `claude/patch-plan` | the user's 28 playtest notes: reproduce, cause, fix, owner, order, questions; `plans/patch-plan.html` |
**Overnight mode (the user, ~05:35 UTC 2026-10-20): 5 working seats at most; no phone notifications; calls logged in `plans/overnight-decisions-lead20.md`.**
| Head writer TW1 | session_019ek4xmi5Yp9xijbzuAo2kN | `claude/talk-pack` | Talk a while pack, content only (~1,300 lines; no repeats; pool + own; keep the question) |
**Status ~11:50 UTC 2026-10-20 (normal mode):** Dev mode plan v2 (claude/devmode-plan 97da6b9) → DR1 + DR2 re-checking. Events plan v3 (claude/events-plan f399143f, design-doc updated) → ER1 reviewing. Patch plan (PP1) in progress (WIP 6e342fa). Talk pack (TW1): 140 talks / 1,260 lines so far (claude/talk-pack f8ecd40).
| Talk pack reviewer TR1 | session_01T93VUcBukQwhBLu8vCNUhV | `claude/talk-pack-review` | reviews every line of TW1's pack (f6005cf: 160 talks, 1,468 lines) |
**Dev mode plan v2.1 published (~12:00 UTC):** https://claude.ai/artifact/2ugbTkkAFkEsgTZa3bbFdH (from claude/devmode-plan 6c37f52; DR1 + DR2 re-checks passed; answers in its db, collection `answers`, doc `devmode-plan`).
**Talk a while lines page (~12:30 UTC):** https://claude.ai/artifact/BEWR9Y2uywFZ7FjNDwuJE4 (from claude/talk-pack 95bb299 after TR1's review; comments in its db, collection `answers`, doc `talk-pack`).
**Events plan COMPLETE (v3.2, claude/events-plan f6996d86; handover 5b679633).** All user questions answered; design-doc updated. Crossing the Line on Sun Day 7; storm Days 11-15; comet Tue Day 16; visit finale Days 26-30. EP1 idle (62% memory).
| Patch plan reviewer PR1 | session_01J7kHfFrG8Syjmz8XYK9USU | `claude/patch-plan-review` | reviews PP1's patch plan (claude/patch-plan 2f8976c: 27/28 reproduced, 6 batches ~19 turns, 17 questions) |
**Patch plan page (~12:47 UTC):** https://claude.ai/artifact/BrEniitA4gGKf1wFMvwy2s (claude/patch-plan 2f8976c; published before PR1's review at the user's request; answers in db answers/patch-plan).
| Dev mode engineer DB1 | session_01R4RFu3mPaq4qj1L2TXEoza | `claude/devmode` (from claude/integration) | builds the lean Dev mode, Stop 1a first (D1-D4); the user answered all questions (12:58 UTC) |

**Status ~13:25 UTC:** DB1 pushed Dev mode D1 (claude/devmode fffb8e2; cadet_test ALL IDENTICAL, new devmode_check.py OK, check_fast OK 387 s); now on D2. DR1 now also stands in as owner reviewer for the section 13 and 21 hooks (c9cc785, 55add3f; the D2 section 13 hook to follow). Waiting on the user's pick of the first-Monday bow-lounge tradition for the patch plan.

**Handover protocol reinstated (the user, ~13:52 UTC):** every seat checks its memory (`get_session`, `context_usage.used_tokens` of 1,000,000) after each job: tell the lead at 500k; at 600k (or before a job big enough to reach it) write `plans/handover-<role>.md`, push, report, stay idle. The lead warns the user at 500k and hands over at 600k (`plans/handover-lead20.md`, written now). The hourly check-in checks this first. Patch plan rev 3 answered (cocoa: bar only; mug: ~20 ship min).

**~14:00 UTC, the user: "Hire extra helpers".** Patch build started in parallel with Dev mode (both from claude/integration):
| Seat | Session | Branch | Job |
|---|---|---|---|
| Patch builder PA | session_01Jka314UJ2Yto5XxbcQnB8H | `claude/patch-a` | batches A, B, C (Day 2, arrival evening, training day); sections 21/21b |
| Patch builder PB | session_01FWW2piuXkFYaRRzLXZiqYb | `claude/patch-b` | batches D then F (crew life, needs tuning); sections 13/14/10 |
| Build master BM11 | session_01W7NHRM4JjqaNEJQUWNxgcE | `claude/integration` | merges reviewed work, sets build numbers; first: Dev mode Stop 1a |
PP1 now reviews patch turns. Batch E (small features incl. First Light Cocoa, the mug) waits for DB1 to finish Dev mode. Working: DB1, DR1, PA, PB (+ PP1/BM11 on call).

**~14:17 UTC, the user: start the Talk a while wiring alongside the patch (it ships with the patch).** Talk pack engineer TE1, session_01MnQHVrsK5wnTwfEi2QFm4W, `claude/talk-wire` (from claude/integration + claude/talk-pack 8692459): T1 reader + content_gen check, T2 picker + save (shape to lead first) + talk_check.py, T3 hook into Talk a while + phone shots. Dev mode Stop 1a done (claude/devmode bb6e78a); DB1 doing the review-fixes commit, then BM11 merges as 0.64.3 and lead publishes. Working: DB1, DR1, PA, PB, TE1 (5); PP1 and BM11 on call.

**~14:35 UTC, the user: add "work pools" to Talk a while** (one pool per type of work, a bit more personal; in addition, keep all 160 talks). TW1 writes the plan page `plans/work-pools-plan.html` on claude/talk-pack with answer forms; TR1 reviews it first; TE1 told to leave room in the picker. DB1 idle (Dev mode Stop 1a complete at claude/devmode 305b572); DR1 on the final pass.

**~14:55 UTC:** work-pools plan published (https://claude.ai/artifact/42zY17Rc3ePiKZEVHVv8KZ, claude/talk-pack 1235f51) and answered (all recommended: mixed order, per save, nine pools, ~120 talks, friend tier = meaning, Works = workmate). TW1 writes the pools (hands over at 600k to a fresh writer). TE1 finished T1-T3 (claude/talk-wire f053df0; Talk a while plays the pack); TR1 reviewing it; then TE1 T4 = work-pool wiring.
