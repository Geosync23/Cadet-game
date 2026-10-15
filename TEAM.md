# Starship Cadet: team board

The project lead session keeps this file current. A new lead session reads it first, together with CLAUDE.md and DEV_NOTES.md.

**Lead:** session_01HV1JuhWgKASQNmvLA2AXD3, branch `claude/mobile-session-linking-3es9z2`. Starts and briefs helper sessions, reviews their branches, merges, and keeps this board and the dev notes up to date.

## Rules for helper sessions

- One job per session, one branch per job. Touch only the files the brief names.
- `starship-cadet.html` (the build) has one writer at a time, and the lead says who. Right now that's the deck architect (Decks 6, 1, 2).
- Follow CLAUDE.md "How we work". Plan pages live in `plans/`.
- Report to the lead with `send_message` after each push: files, what changed, open questions.
- The user sends every request through the lead, and the lead hands out the work.
- Before closing a session, the lead checks that it's idle and has no unfinished request.

## Roster

| Session | Job | Branch | Status |
| --- | --- | --- | --- |
| session_011Gh8MbJgkYYWwWk2s3oA4y | Deck 3 builder (builds 0.6.7–0.7.0, repo tidy) | `claude/deck-building-workflow-iayt67` | On hold (user's request). Merged into the lead branch at 8390434 |
| session_01JScnVG158eYAHYvKDz3jZG | Deck planner: plans for Decks 1, 2 and 6 | `claude/deck-plans-1-2-6` | Working: Deck 2 Sketch 5, all bedrooms in the stern half, science in the bow half, lift doors split between them |
| session_01UFZoEaoHa3Tz1RrypCRzNx | Deck architect: build Decks 6, 1 and 2 into the game | `claude/deck-architect` | Building Deck 6, turn 1 (the shell) |

## Done

- Deck 2 plan Sketch 4 (589505e) merged: 12 crew bedrooms plus 2 visitor rooms to port, science to starboard, 50 × 18, lift [21, 9].
- Deck 3 signed off by the user at 0.7.0 ("ok for now").
- Merged the deck plans through 355648a (Decks 1, 2 Sketch 3, 6) into the lead branch, then moved them into `plans/`.
- Merged the Deck 3 builder's branch: Deck 3 turn 5 (crew, 0.6.7), promenade dressing and fixes (0.6.8–0.7.0), the repo tidy (stable file names, `plans/`, CLAUDE.md, deck_check.py).
- Plans for Decks 1, 2 and 6: Sketch 1 (36cce9d, 09f1feb, 68a8bc8); Deck 2 Sketch 2 (b4cfbc6); Deck 2 Sketch 3, 50 × 18 with the Captain's quarters as the biggest room (4fe97c4); Deck 6 reactor door off the lobby (355648a).

## Plan of work (agreed with the user, 2026-10-15)

1. **Build the ship (DEV_NOTES 6e):** Deck 6, then 1, then 2, with a review after each. Deck architect only. Shell, rooms and furniture; no crew or machines.
2. **Then:** crew on the new decks, and step 7 (machines, supplies, job list).

## Queue

- Design doc updates listed at the top of DEV_NOTES.
