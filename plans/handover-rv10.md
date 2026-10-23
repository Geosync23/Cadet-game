# Handover: RV10, reviewer (0.92.0 late tweaks, 0.92.1, 0.92.2)

Written 2026-10-23 by RV10 (session_01XeJ6bvySekD1V8Sfh1tzgb). Leads: lead 31 (session_0118SXBCdg87nDiXdtrGNVSR), then
lead 32 (session_01GFHMDsQK3TfPfH7Paapyog) from ~20:30 UTC. Build master for 0.92.1/0.92.2: BM15 (session_01EH5qkoYriK2Gsrp7hHRoso).
Read CLAUDE.md, DEV_NOTES ("Rules that keep it working", "Testing"), plans/handover-rv8.md, then this and plans/review-rv10.md.

**Role:** reviewer. Never edits the game. Notes only on `claude/review-rv10` (push only there). Each verdict to the builder,
the build master (BM15) and the lead with send_message: plain words, numbered, PASS / FIXES NEEDED.

## Verdicts (details in plans/review-rv10.md)
DV1 dev-career-arrow 9f51257a PASS; FX7 tiles-sit 0a58748e PASS; FX6 hygiene-cool cbd41548 FIXES NEEDED -> 50fd3f2a PASS;
FX5 booth-arrow 771c9ff2 PASS; FX5 day0-table 153084a1 PASS; AC3 join notices 54169e4c PASS; FX4 save trim 06a989e6 PASS;
FX7 bike-tap 9328dc76 PASS; CP5 controller-follow2 f293d672 PASS; FX5 day0-trickle 0e392cf3 FIXES NEEDED -> de475883 PASS;
FX6 m8-fix 54efee21 PASS; FX5 day0-stay 3df51ee9 PASS, 583af9ed PASS (then dropped by the user for FX8's day0-sim);
FX6 arrows-week e1f1ec97 PASS; FX7 mess-taps 980c2591 PASS. Handed to RV11: FX3 relay-shelf 85b6250a, FX6 team-restore
28bcc102, DV1 d2-solo-tap 292f4f77. Handed to RV12: FX6 tray-seat arrow. FX8 day0-sim 87e3174a: see below.

## How I tested (probes in plans/review-rv10/; each takes GAME.html, a folder with cadet_test.py, and its own args)
- Builds: `git show SHA:starship-cadet.html > /tmp/x.html`; worktrees for each commit's checks (`git worktree add --detach`).
- Real taps: my own Playwright context with has_touch=True at 320x640 and 390x844 (cadet_test's Game has no touch);
  dv_probe, fx6_probe, fx7_probe, fx5_probe (Day 0 Track it + the Tracked row), join_probe, bike_probe, meal_probe,
  counter_probe. Day 0 crew plans on paper: trickle_probe, stay_probe, sim_probe (others changed, double-booked places,
  gaps, the same twice); trickle_live (Deck 3 live at an 18:40 goodnight: who changes goal).
- Planted faults: sed a copy (e.g. EV_LINE_ON false, TEAM_RESTORE 0, a worksUse line removed) and run the check on it.

## Gotchas
- 4 cores: interactions_check, join_check, devmode_check, intro_check stall or time out with 3-4 browsers at once; run
  them alone or two at a time. Page.goto timeouts = load (or orphan browsers: kill the specific PIDs, never pkill -f on a
  pattern that matches your own shell: it killed my shell twice).
- `git worktree add X && (A) & (B)` races: B starts before the worktree exists. Add the worktree in its own command.
- Pop-up timing (TOAST_AT, the queue) runs on the test's virtual clock: step frames, don't wait real time.
- intro_check full takes over 50 minutes per build; --evening or --firsts parts are enough for most changes.
- Teleporting the player works with player.obj.position.copy(cellPos(...)) on an open cell; a spot inside a wall does nothing.
- At 06:00 the Deck 4 showers are full; test at 14:00 (skipTo).
- Day 0 planning reads SHIP.intro.done.free (the live goodnight) through day0Free/day0Trickle only; any change there:
  check nobody but the table's diners changes (sim_probe) and look live.

## Open items
- FX8 day0-sim 87e3174a: paper probe done (18:20, 19:10): others changed none; no diner changed before standing; no
  gaps; same twice; first steps gym/lounge/call home/shop/garden/lift; only new overlaps are toilets (3 and 2 pairs; 54
  toilet overlaps exist without the live minute). Checks running at handover time: see plans/review-rv10.md.
- Backlog notes: FX6's Day 9 'Food' arrow stuck with the Line on (lead has it); FX7 counter check should re-test
  "not on them" right before each click.

## Open questions for the user
None from me.
