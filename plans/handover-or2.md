# Handover: OR2 (reviewer: the optimization pass, then playtest patch 1)

- **Session:** OR2, session_01AnRKXUUGi8mwREwvt4WbaV. Took over from OR1 (plans/handover-review-opt.md) after the account move, 2026-10-21 ~18:00 UTC. Leads: 25 (session_01J2aTyEohBf8KFHCsTqt3LW), then 26 (session_015mHBLCf5jpnzBkFY1iBTqv, from ~02:10 UTC 22 Oct).
- **Branch:** `claude/review-opt`. Notes only: `plans/review-opt.md` (every verdict with how it was proven) and `plans/review-opt/` (probes and logs). Never changes the game or the build number.
- **State at handover (~14:45 UTC 22 Oct):** nothing open; idle and stopping (memory ~625k). Last review: ON1's Zeke fix, claude/patch-zeke ce2f77bc, PASS (lead 27, session_017UHW78qnvRTQwYpDxpodHz; BM13 session_01ExFoVfhiFG3wYTFv2QrojC).

## Verdicts (details in plans/review-opt.md)

| What | Tip | Verdict |
|---|---|---|
| TS2 player_check F1 | opt-tests 26e6902 | PASS |
| RN1 #5 stale decks let go | opt-render cd9d030 (tip 862722f) | PASS |
| RN1 #8 Dev Speed card | opt-render 862722f | PASS, no nits left |
| PB2 double dinner | patch-b2 be8871d | PASS |
| PB2 backlog 18 + section 17 double booking | patch-b2 38424f0 + 5b4eb4f | PASS together |
| TS3 item 1, affected-checks runner (a) | opt-tests 7009b108, final da8e97ca | PASS |
| TS3 option (b) trial | opt-tests 975ca4cc | PASS WITH FIXES (doc clause, done); (b) not adopted |
| TS3 six check gaps | opt-tests 7063b375 | PASS |
| Playtest 1 C (PB2, crew through walls) | patch-play1-c 0ecf99fa | PASS |
| Playtest 1 D (CJ1, the Chief's first solo job) | patch-play1-d ede7432b | PASS (79c3a8e1 had a 147-char line) |
| Playtest 1 A (ON1, arrival evening) | patch-play1-a 8c8bf8fd | PASS (b7c167d3 FAILED: the Chief didn't come over for a slow player) |
| Playtest 1 D, the empty shelf | patch-play1-d 836db6c7 | PASS (on integration-next; re-bake on merge) |
| The Zeke fix (0.64.15's "Zeke stands in Bunk 1") | patch-zeke ce2f77bc | PASS (40fbd0d5 held: its cap cut a far player's wait) |

## Gotchas (learned the hard way)
- **lines_check is not in check_fast.** Run it on any branch that changes words (I missed a 147-character line on D's first tip).
- **Run a check on the OLD build too.** A new check that also passes on the old build proves nothing (A's first tip: its evening checks passed on 32b699a6; `intro_check --dawdle` was the path that showed the user's case).
- **setShipNow(abs): minute 0 is Day 1**, not Day 0 (day_check uses `(day - 1) * 1440`). My first late-day detach run was a day off.
- **Deck shots can differ by 1-2 pixels from Chromium's chip-drawn canvases** (shadowBlur signs), varying with memory, not the game: `plans/review-opt/keep_shots_cpu.py` (`--disable-accelerated-2d-canvas`) is the steady proof.
- **`pkill -f` with a pattern from your own command line kills your own shell** (it did, again). Use `pgrep` and skip `$$`, or let a run finish.
- **A git worktree left half-made** blocks `worktree add`: `rm -rf` the folder, THEN `git worktree prune`, then add (the other order fails, and a background job then runs without its files).
- **A `pgrep -f` wait loop with the pattern in its own command line never ends** (it matches itself), like pkill: wait on a log line instead.
- **0.64.14+ has EVENTS_ON on**: checks guarded by "events base off" skip themselves; prove them on an EVENTS_ON-false copy.
- **lines_check against another branch's content/** gives a false "baked blocks out of date": run it in the worktree of the build you test.
- One browser check at a time; long ones in the background with an `until grep ... ; do sleep 30; done` wait.

## How to test (probes in plans/review-opt/)
- Setup as DEV_NOTES "Testing": `pip install playwright numpy pillow`, three r128 and acorn 8.12.1 in /tmp/cadet-work, `CADET_CHROME=/opt/pw-browsers/chromium`.
- `detach_play.py BUILD` (DP_TIMES for other days), `keep_shots_cpu.py OLD NEW OUT`, `scene_dump*.py`, `plan_days.py`, `double_meals.py`, `no_meals.py`, `plan_at.py`, `lanes.py`, `merge_all.py`, `grain_all.py`, `speed_probe.py`.
- For a game-change review: the fix read against the cause; the branch's check on old (must FAIL) and new (must pass); cadet_test old -> new with every difference looked at; lines_check if words changed; check_fast.

## Open questions for the user
None of mine. For the lead: backlog rows suggested and not confirmed: the first-night bunk arrow in `intro_check --dawdle` (now passes on A's tip); the six check gaps' owners (closed by TS3).

## The Zeke review (closed: PASS at ce2f77bc)
- The user's 0.64.15 report: after the bag, Zeke stands in Bunk 1. Reproduced on 2b4a05db with `plans/review-opt/intro_tap.py` (copy it next to cadet_test.py, delete its first comment line; `NOTAP=1 TICKS=60 EVERY=5 python3 intro_tap.py BUILD --evening`): without the bag stowed, 'stow' holds 17:14 to ~18:05. Cause: introAdvance's "his own steps never time out while he's within 10 tiles of you (until 18:00)". ON1 found the second way in (leaving Bunk 1 during 'device'); 'bunk' and 'table' had the same hold.
- To check on the new tip: `intro_check.py BUILD --leave` FAILS on 2b4a05db (/tmp logs lost with the container: rerun) and passes on the tip; the full intro_check (incl. paper part 2, a player 10 minutes behind) passes; intro_tap NOTAP on the tip: Zeke leads on within ~10 ship minutes; lines_check; cadet_test vs 2b4a05db; check_fast. Also the cases lead 27 named: leaving Deck 4 by lift during stow/device, reload mid-step, standing outside Bunk 1 during 'bunk', away from the table during 'table'. Verdict to lead 27 and ON1 (session_01BJNi1oqxnQ3jUusXHbHDGW).
