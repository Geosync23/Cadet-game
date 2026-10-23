# Handover: FB1 (fresh-eyes builder 1, pins and taps)

Written 2026-10-23 at about 60% memory, by the session that held the role (session_01C12k89pPRvZ63JHS3C2e1a).
Leads: 29, then 30, now lead 31 (session_0118SXBCdg87nDiXdtrGNVSR). Reviewers: RV8 (session_01Q6uHYWus4ncyEgqWEYhJh5),
now FX4 (session_01BueJ4UzQkn8HcC1TXd1KrW). arrows-c merges: AC3 (session_01DiLRzrXgkeoAZCoX1mVJn9; was AC2).

## Branch and builds

`claude/fe-cartdock`, on `claude/p5-fix3` 3b7b13d (FX3's fix 15). Build number never touched (the build master's).
Commits, oldest first (each has a row under "fe-cartdock" in `plans/build-table.md`):

| Commit | What | Review |
| --- | --- | --- |
| a52aad0 | A tap on the thing under the arrow does a haul's or a delivery's stop (Cart dock 1, the Folding table, every pick-up and drop) | RV8 PASS |
| 228de58 | No-job stow: a part goes back from the storage spot nearest the tap (Day 6 "Put the seal back") | RV8 PASS |
| ebf456b | A tap on the line to any chore's next stop does it, whatever caught it (Day 4 hydroponics vent) | RV8 PASS |
| 191bee5 | `jobRayDist` looks from the floor to 1.7 m (the drawn dot); section 11: a lift door/panel tap over your stop does the stop (Day 2 galley drop) | RV8 PASS; in arrows-c |
| bd291e4 | `rayIsThisTap`: the pin rule uses the screen tap's line only when it is this tap's; section 11's lift line, the tap's line only | sent to FX4 and AC3 |
| 8438e7f | Test only: the Folding table part sets its haul at 10:00, clear of Yara's 12:00 lesson (the flake beside check_fast) | sent to FX4 and AC3 |

Checks on 8438e7f: 5 full interactions_check runs beside check_fast all green; player_check OK; cadet_test vs 191bee5
alone ALL IDENTICAL. Open: FX4's review of bd291e4 + 8438e7f, and AC3's merge, before the 07:00 UTC cut-off.

## What I own and built (section 15 unless said)

- `choreThingTap(it, at, point)` after FX3's `choreRayTap`, called from `playerTap`. Three rules, in order:
  a tap on the line to your chore's next stop (`jobRayDist < JOB_RAY`, the line being this tap's: `rayIsThisTap`) does it,
  whatever caught it; carrying for a haul (any stop) or a delivery chore (pick-up, drop), anything within `JOB_REACH`
  (1.5 m from its edge, `ixDist`) of the next stop does it; for other registered kinds (round, tuning) a machine in reach
  does it. Other chores off the pin keep 0.28.55's rule.
- `rayIsThisTap(p)`: p on the line, or within 1.6 + JOB_RAY of where it meets the floor (15b's `ixPinTap` passes the thing
  nearest the pin, not a hit point).
- `jobRayDist` (shared; FX3 is section 15's owner and agreed): samples 0 to 1.7 m (was 1.2). Do not raise it: a tap on a
  thing far behind a stop would count (FX3's caution: about 2.8 m in plan at 2 m height).
- `jobTap`'s no-job stow uses `jobPlaceNear('storage', 'r', at)`, like the fetch.
- Section 11 `tap()`: before `enterLift`, a lift door/panel tap tries `jobHere({ x: Infinity, z: Infinity }, true)` (line only).
  Section 11 has no active owner; the reviewer reviews it.

## interactions_check parts (all mine, each fails on the commit before its fix)

"FB1: the hover cart at Cart dock 1"; "FB1: every pick-up and drop of a haul and a delivery, real taps" (128 taps);
"FB1: put a part back from the arrow's pin"; "FB1: a tap at a chore's pin does the stop, whatever is under it (vents and
lamps)" (+ the Lemon tree stale-line line); "FB1: a tap on the top of the drawn dot..." (92 taps, + off-pin things,
lift with no job, a person at the stop). To run one part alone: copy the header up to the first `with sync_playwright()`
plus that part into a scratch file (cadet_test.py path made absolute), as I did.

## Gotchas

- Module-level names in interactions_check are shared: my vent part once used `st` as a loop variable and broke the later
  "tracked" part (`st` is a helper there). Use fresh names.
- Real taps: the arrow's anchor is 1.2 m above the stop; the dot (`#ixGoal .ixpin`) is 19-24 px above that and bobs 5 px.
  Tap the dot, not the anchor, to test what a player does. A first-time tip card (`#devTip`) can sit over a pin: hide it.
- `pgrep -f` in a watcher loop matches the loop's own command line; `pkill -f` with a pattern in your own shell kills it.
- arrows_d_check and arrows_check's newest follower live on `claude/arrows-c`; run them on a scratch worktree merge.
- The week follower's runs are not repeatable; a scene set inside a training (Yara's 12:00 lesson on Day 3) gets taken
  over at timing-dependent moments, so set test scenes at quiet times.
- Never trust one cadet_test run's a_start alone: RV8 saw the same one-off start-up wobble (a speech bubble a few px off).

## Loose ends and questions

- FX4's review of bd291e4 and 8438e7f; AC3's merge into arrows-c before the 07:00 UTC cut-off.
- Still stuck in arrows_check's week (not mine): Day 4 inspection m3i, Day 5 scanner m7/p3, Day 8 m6 (FX3/FX2).
- Merging p5-fix3 into arrows-c conflicts in `ixJobStep` (FX3's lathe line vs scanFirst); not mine.
