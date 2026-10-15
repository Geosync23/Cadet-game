# Starship Cadet: team board

The project lead session keeps this file current. A new lead session reads it first, together with CLAUDE.md and DEV_NOTES.md.

**Lead:** session_0158BCCswtdujm3t5d2LXsFz, branch `claude/lead-pillar1` (started 2026-10-15 from the Pillar 1 plan commit 149a455, which is `main` plus the plan). Starts and briefs helper sessions, reviews their branches, merges, and keeps this board and the dev notes up to date.

**Retired lead:** session_01HV1JuhWgKASQNmvLA2AXD3 (branch `claude/mobile-session-linking-3es9z2`), handed over 2026-10-15 because its context was getting long. Helpers report to the new lead.

**Integration branch for Pillar 1:** `claude/ship-integration` (= `main`, 707b696, at the start). Combined builds are numbered 0.23.0, 0.24.0 and so on. Pull requests to `main` only when the user approves a milestone, and merged only with their OK.

**Playable build (the one link the user uses):** https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y, owned by the Deck 6 architect. New builds are republished to this same link.

## Rules for helper sessions

- One job per session, one branch per job. Touch only the files the brief names.
- `starship-cadet.html` has several writers in Pillar 1, each limited to its own sections (see `plans/pillar1-plan.md`). The lead merges.
- Follow CLAUDE.md "How we work". Plan pages live in `plans/`.
- Report to the lead with `send_message` after each push: files, what changed, open questions.
- The user sends every request through the lead, and the lead hands out the work.
- Before closing a session, the lead checks that it's idle and has no unfinished request.

## Roster

Pillar 2, all started 2026-10-15 (see `plans/pillar2-plan.md` for the workstreams, formats and build numbers). A helper session can only push to the branch it was created with. Pillar 1 (done, 0.25.2) roles are in git history.

| Session | Job | Branch it pushes to | Builds | Status |
| --- | --- | --- | --- | --- |
| session_0158BCCswtdujm3t5d2LXsFz | Lead | `claude/lead-pillar1` | 0.40.0+ (combined) | Active |
| session_01S5xTHRBpJ9kqytfrwKipUG | Sim engineer: A1, every room in use (crew free time across the ship, crew needs, activity choice, galley-rota hook) | `claude/sim-engineer` | 0.26.x | Briefed |
| session_01TiBtENVFJV7RqEQ7YkxH1Z | Performance engineer: A2, activity poses and props (run, lift, call, browse, pay, play, water, cook, wash, fold, drink, read, talk) | `claude/crowd-render` | 0.27.x | Briefed |
| session_01Q9xiH4P2jjftpwBSrMyr42 | Player engineer (new): A3, player needs (fitness and energy slow you), activities, placeholder device, save v2 | `claude/player-needs` | 0.28.x | Hired |
| session_0182LPGeQR8Cix6rhf6op5Qv | Galley engineer (new): A4, food and cooking (chef from 04:30, batches, servery, shelf, dish pit) | `claude/galley-food` | 0.29.x | Hired |
| session_01UFZoEaoHa3Tz1RrypCRzNx | Deck 6 architect: A5a. First 0.30.1, the shared turn: `service: true` hatches (player and Works crew pass, only into built rooms), `still` floors, deck_check machine and place rules. Then the utility rooms on Decks 4, 5 and 6 (plan c20fa6b approved: 29 machines, no room changes size). Also the treadmill belt animation. Owns the playable link | `claude/deck-architect` | 0.30.x | Working |
| session_015BoZMMp5b4A4F51dMcZ3ax | Bridge architect: A5b, Deck 3 activity furniture (weights, till, baskets, anim on places), then utility rooms on Decks 1 and 3 (sketch first) | `claude/deck1-scale` | 0.31.x | Briefed |
| session_014DMHpLuFyNknrAcZZGGNhU | Command architect: A5c, Deck 2 activity anims (0.32.1), then its utility rooms (plan 15e5dbb approved by the lead: gas plant, utility closet, cable crawl, array machines; no room changes size) | `claude/deck2-command` | 0.32.x | Working |
| session_01JScnVG158eYAHYvKDz3jZG | Crew designer: A6, galley staff shifts and habits for the new activities | `claude/deck-plans-1-2-6` | 0.16.x | Briefed |
| session_0134zewqwGV9hdGK6PqsaZ36 | Systems engineer (new): B1 now (machines, wear, systems, consequences, machine_check; no drawing), B2 and B3 later | `claude/ship-systems` | 0.33.x | Hired |
| session_011Gh8MbJgkYYWwWk2s3oA4y | Deck 3 builder | `claude/deck-building-workflow-iayt67` | — | Archived |

## Context check (2026-10-15, 17:10)

How full each helper's memory is (out of 1,000,000): crew designer 84k and Deck 6 architect 199k (both already compacted), bridge architect 570k, command architect 525k, performance engineer 510k; sim engineer not reported while working. Sessions compact themselves automatically, but lose detail when they do. Plan: no new hires for the end of Pillar 1. For Pillar 2, give big new jobs to fresh sessions, and retire the bridge and command architects (idle, work merged) once the user agrees, after the usual idle check.

## Done

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
