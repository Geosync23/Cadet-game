# Lead handover (2026-10-16, ~04:20 UTC, mid answers-pass)

From the outgoing lead (session_0158BCCswtdujm3t5d2LXsFz, ~460k of 1M after one summary) to the new lead. You are the PROJECT LEAD for Starship Cadet. Read this, then CLAUDE.md, TEAM.md, plans/answers-pass-plan.md, plans/answers-pass-decisions.md, then skim DEV_NOTES.md's build table.

## The user

New to Claude Code and git: plain language, no jargon, short updates. Asleep tonight; they gave the lead sole authority to interpret their answers. Every request comes through the lead. PRs to main only when they approve a milestone; merge only with their explicit OK. They like PushNotification pings when something they're waiting for is ready. Our rule (CLAUDE.md): warn early and hand over before auto-summarizing.

## Tonight's job (the "answers pass"), and what the user expects in the morning

1. **The new playable build** at the same link: https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y (owned by the user's account; version 11 = 0.40.8). Republish ONCE at the end, from the final combined build. Steps: plans/handover-deck6-architect.md section 3. Caution: publishing to it needs a full Read of the current 10.5k-line page first (very costly in memory). Consider delegating the republish to a fresh helper session with those steps.
2. **A report of the design decisions faced and what was decided** (plans/answers-pass-decisions.md is the running log; turn it into a clear page). The user also asked mid-night for: sitting anywhere, small Stardew-like traditions, player can use everything crew use, job board pick-and-take with an on-screen arrow, more jobs, crew seat alignment. All are assigned (below).
3. **The Pillar 3 plan and pitch.** The Pillar 3 planner (session_01FvJicF3TPx3ZV84fiZGUyU, branch claude/pillar3-plan) has pushed plans/pillar3-plan.md (52568ac) and plans/pillar3-pitch.md (16f9fba). NOT YET REVIEWED by the lead. Review, give feedback, then publish the pitch as an artifact for the morning. The user's must-haves: personal device with Schedule, Appointments, Maps, Memos (+ more), the start of ship-wide events and how they run ambiently ("everyone talks about them") vs traditional missions, plus the lead's ideas.
4. The **real-phone test checklist** for the user (only they can do it).

## Where the build is

- Combined builds on `claude/ship-integration`: 0.41.0 (99de199), 0.41.1 (f29fa93), **0.41.2 (e806e7b, latest, pushed)**. All checks pass on 0.41.2 (deck, day 1, food, machine, player, events); cadet_test differences explained in the commit message.
- Work in a local branch (`lead-wip`), push ship-integration only after all checks pass (the stop hook nags about unpushed commits otherwise).
- Merge tooling in `tools/` on the lead branch: `resolve.py <build>` (auto-resolves HUD build line, GAME_BUILD and DEV_NOTES unions), `fixrate.py <file>` (auto-resolves the GAME_BUILD + SHIP_RATE conflict block every helper branch now hits; keeps HEAD's), `kitdup.py <file>` (duplicate KIT piece names: last definition silently wins). Also scan duplicate top-level declarations: `grep -oE "^(const|let|var|function) +[A-Za-z_$][A-Za-z0-9_$]*" starship-cadet.html | awk '{print $2}' | sort | uniq -d`.
- DEV_NOTES build table: dedupe, sort by version, append the combined row, update "## Current build".
- Checks: CADET_CHROME=/opt/pw-browsers/chromium; three.js in /tmp/cadet-work/three; run ONE AT A TIME: deck_check.py, day_check.py BUILD 1, food_check.py, machine_check.py, player_check.py, events_check.py, cadet_test.py old new. ~25 minutes for all.

## Waiting to merge (pushed but not yet in a combined build)

- deck1-scale 0.31.10 (Deck 1 handover/walk places)
- deck-architect 0.30.13 (machineMarks removed, look overrides, plates read ROSTER plate)
- systems 0.33.16 (jobs left for the player 3-6/day, cart run as a player job, jobStops)
- crowd-render 0.27.11 (stool footrests, ?seats view)
- galley 0.29.12 is in; player 0.28.10 is in.

## Who is doing what (all report to the lead by send_message)

| Helper | Session | Branch | Remaining |
| --- | --- | --- | --- |
| Sim engineer | session_01S5xTHRBpJ9kqytfrwKipUG | claude/sim-engineer | Remove observatory/birthday gatherings (section 18 owns them), numeric `face` + per-place `y` in placeSpot. |
| Performance engineer | session_01TiBtENVFJV7RqEQ7YkxH1Z | claude/crowd-render | Done; standby (may check architects' seat fixes). |
| Bridge architect | session_015BoZMMp5b4A4F51dMcZ3ax | claude/deck1-scale | Tiers on 7 hatches, bridge health board (reuse Deck 6's healthBoard kit), look overrides (NO machineMarks), seat fixes for Decks 1 and 3 from the performance engineer's list. |
| Crew designer | session_01JScnVG158eYAHYvKDz3jZG | claude/deck-plans-1-2-6 | Done; standby. |
| Systems engineer | session_01FtwFYLBjAB9zFvPSpLezaR | claude/ship-systems | 0.33.17 machineLook/shipHealthRows/shipMoodAt/chiller; 0.33.18 machineUse, tier locks (e.tier on hatch edges), shortages to Mail; MANY MORE JOB TYPES + openJobs(forWho) for the interactions engineer. |
| Deck 6 architect | session_01MiQtjmdEa4CXsCsiCh6zWV | claude/deck-architect | Seat fixes for Decks 4-6; check Deck 6 crawl trays once the cableTray rename lands. |
| Player engineer | session_01BQjtEzvKXuvPZNzGRRRwpZ | claude/player-needs | 0.28.11: squeeze past settled crew (fixes the blocked galley plant panel), machine tap (machineUse), cart run (jobStops), crouch on crawl tiles, SIT ANYWHERE. |
| Galley engineer | session_01AVGVnj4Q1jFmVoD6xi5asT | claude/galley-food | One line: meals the PLAYER pushes land on unload. Otherwise done. |
| Command architect | session_01EhJv6dqovqhQyruMveFuRR | claude/deck2-command | Seat fixes for Deck 2 (0.32.6). Messages to them crossed several times: be explicit. |
| Events engineer | session_01YXDbUmtB1mg4kiJyuToqKA | claude/ship-events | 0.34.1: reconcile with the sim engineer (section 18 is the ONE events system), one observatory night day/time, announcement mails quiet on Day 1 morning (they covered the intro toast). |
| Interactions engineer | session_01GGbtSiy4tDygCzrSUBDMYa | claude/player-interactions | Section 15b: player can use everything crew use (treadmill, rower, bar, music, garden, laundry, games...), job-board pick-and-take, on-screen goal arrow (setGoal/clearGoal). No push yet. |
| Pillar 3 planner | session_01FvJicF3TPx3ZV84fiZGUyU | claude/pillar3-plan | Draft done; waiting for the lead's review. |

## Decisions already made (don't relitigate)

See plans/answers-pass-decisions.md. Highlights: SHIP_RATE 1080/1800; energy lasts ~16-18 h; bed after 20:00 skips to 06:00; need bonus table (tuned); machine trouble doesn't slow the player; visible faults drawn ONLY by the performance engineer's central system (architects add `look` overrides); shipHealthRows shape; place type 'event' + `event` tags; one events system in section 18; Tier 1 player; squeeze past settled crew; seats fixed by place data (y, xy, numeric face).

## Lessons from tonight

- Messages reach a helper only between its turns, so a changed decision arrives late. Settle who-does-what before work starts.
- Three architects built the same machine lamps because of that; two KIT names collided (cableTray, relayRack). Run kitdup.py on every merge.

## Safety net

A self check-in was scheduled into the old lead's session; cancel it if the old lead hands over (trigger trig_01Xz7RrwGS2BNT274jDYKs8U). Schedule your own with send_later (~60 min) while helpers work.
