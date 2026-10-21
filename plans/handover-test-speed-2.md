# Handover: test-speed engineer 2 (TS2, the optimization pass's test-speed seat)

- **Role:** make the checks faster without changing what they find (plans/opt-plan.html on claude/opt-plan: items 0, 1, 2, 11, 12). Test-only: no game changes.
- **Session:** TS2, from 2026-10-21 ~11:40 UTC. Lead 23, then lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r). Reviewers: PR7 for item 0, then **OR1** (session_015np4rHB2UHzet5Y1zFrBzm, the optimization reviewer) for everything since.
- **Branch:** `claude/opt-tests`, from `claude/integration` 3a48846 (0.64.8). Push only there. The build number is the build master's.
- **The user's rules for test speed:** the affected-checks runner first; saved-game fixtures with caution and never the only check (and **not in this pass**: the user's answer to the plan); results must stay identical; **checks play the real, drawn game**, with **one exception: player_check's polling steps may skip drawing (user OK, 21 Oct); everything else draws** (written into DEV_NOTES "Testing"). The cadence (the plan's question 3): each turn runs check_fast plus the affected checks; the full round at every release and at least once a day.

## Done

| Item | Commits | State |
| --- | --- | --- |
| 0: perf_check stands you in the right room | c2a32e2 (fix f5d6815) | **PR7 PASS.** `cellPos` before `nearestOpen`; each view records `stood` and a view outside its room is a PROBLEM. New baseline at 0.64.8 in DEV_NOTES and the build table. RN1 built the event scenes on it (claude/opt-render 3af9f15): **start from RN1's perf_check** if you touch it again. |
| 2: player_check 18 → 5.6 min | 4775488 (A), e4acbf8 (B), 26e6902 (F1) | **OR1: PASS WITH FIXES; F1 done (26e6902)**: each activity and the servery check `renderer.info.render.frame` moved (else FAIL), so a stale draw-call count can't pass. Proof on 0.64.8: PLAYER CHECK OK, 310 s, output the same as A+B; OR1's mutant pmA (`with drawn()` removed from run_activity) now FAILS ("Shower: drawn ... frame 1 -> 1", exit 1). check_fast not re-run for it (stopped for the account handoff; the change is player_check only, which check_fast doesn't run). Tell OR1 if I couldn't. Earlier: A: three places stepped `window.__step` with every frame drawn; now only the last of each batch, as `Game.step`. Output identical, 1083 → 859 s. B (the user's OK): a `drawn()` guard; steps draw only in `run_activity`/`servery_seat` (the 450 budget) and the phone-layout block. 335 s, output identical except "phone, at rest", which now sets the toast itself (it depended on a real-time 5.6 s `setTimeout`). FR3's player_check edit (claude/fridays 208581c8) 3-way-merges cleanly. |

Profile tools used (in the session's scratchpad, not committed): a wrapper that times every playwright call by the check's line. Finding: a drawn frame is ~0.65 s of a 0.72 s `step` in SwiftShader, set by draw calls, not pixels (a quarter of the pixels saves 25%). RN1's find: `gl.finish()` returns at once here, so drawing time is billed to the next sync call; time a drawn frame with a 1-pixel `readPixels` after it.

## In progress: item 1, the affected-checks runner

- `tools/affected.py [A [B]] [--why] [--cmd] [--map FILE]`: the checks a change needs, on top of check_fast. The union of (1) RULES: DEV_NOTES's "run it whenever" lines by section (the planner's list, reviewed by ER2; an unknown section runs everything) and (2) the map from real runs. Files outside the game: a check's file picks it; cadet_test.py picks all; content/ picks section 22's rules.
- `tools/check_cover.py OUT.json CHECK.py ARGS`: runs a check unchanged with Chrome's **block** coverage on every page it opens; writes the game lines that ran after the page was up (`run`) and those that ran only while it opened (`load`). Coverage roughly doubles a short check's time.
- `tools/fn_index.js`: the game's top-level declarations by line, and `uses`: the lines where each name is read.
- `python3 tools/affected.py --merge OUT.json COMMIT cov/*.json` makes the map (it refuses a cover made on another game than COMMIT's).
- **How the map picks:** the old side's changed lines (a pure insertion: the lines either side), moved into the map's own game by a diff, and every check that ran one of them. For a changed table or other top-level value, every check that ran a line reading it. Lines that only ran while pages opened pick LOAD_CHECKS (cadet, deck).
- **Why line level:** the first map was by top-level function (function coverage). It picked ~18 of 23 checks for small changes, because a function every check runs usually mentions some table in a branch that never runs (WORK_BANDS, for one).
- **The map run:** every check once under check_cover on 0.64.8 (`cov_run.sh` in the scratchpad: a frozen copy of the branch via `git archive`, then `check_cover.py` per check; cadet = `cadet_test.py G G`, day1 = `day_check.py G 1`, perf without OLD). Batch 1 = the 22 shorter checks (about 70 min); batch 2 = perf, interactions, day1, intro, player (about 60 min). One browser at a time. Covers done are pushed to `plans/opt-cover/` as they finish.
- **The validation set:** a search of the notes found 40 real check failures caught at review or merge, each with its cause. The causing commit still exists for 17 of them (listed in `plans/opt-cover/failures.md`). The rules alone miss 3: mech_check for First Light Cocoa (1c4bc67), and intro_check --evening for patch-a #17 (155f0d4, ee48072). The map has to catch those. Commits bd3db3f, 6c26c72, 9fa60da and 0cdde89 are notes-only or whole-repo imports: not usable.
- **Batch 1 done and pushed** (15:20-16:15): `plans/opt-cover/<check>.json` for 22 checks, merged into `plans/opt-cover/map-0.64.8-batch1.json` (`--merge ... origin/claude/integration`). Batch 2 (perf, interactions, day1, intro, player) **not run** (lead 24, the account move).
- **Replay with batch 1** (`--map plans/opt-cover/map-0.64.8-batch1.json`):
  - Last 20 game commits: rules alone 2-11 checks (25-72 min; one turn 23, the clock-and-save one); rules + map 8-20 checks (40-107 min), mostly 15-19, out of 23 (131 min).
  - Failures: the map catches mech for 1c4bc67, which the rules missed. intro for 155f0d4/ee48072 is still missed, as expected without batch 2. Everything else was caught by both.
  - **Why the map is broad even at line level:** code every check runs (the HUD, the device, the hourly ticks) really reads most tables and calls most helpers. For example, WORK_BANDS (319f541) is read by the reputation band that every check's HUD shows. "This check ran a line that reads the change" is true for ~17 checks, but most of them can't fail on it. The map is right about data flow; it just isn't a sharp filter.
  - **Options to put to the lead and the user:** (a) rules + map as is: safe, ~15 checks / ~60 min a turn, half of the full round's 131 min; (b) rules + map, counting only lines a check ran **outside** the shared every-frame code (lines that ≥ 18 of 22 checks run are "everyone's" and pick through the rules only): sharper but less safe, so it needs its own replay; (c) the rules alone for most turns plus the map's extra checks only for the sections whose failures the rules missed in the past (14, 18, 10/11): the planner's 28 min plus a little. My lean is (b), proven by a replay with batch 2's checks in it (it must still catch intro for 155f0d4/ee48072 and mech for 1c4bc67).
- **Next:** run batch 2; settle (a)/(b)/(c) with the lead; replay the last 20 game commits (picks, minutes; the planner's rules-only average was 4.2 checks, 28 min) and the 17 failures (every one must be picked); then DEV_NOTES "Testing" (how to use it, the cadence, regenerating the map at each full round in a run that doesn't count) → OR1.

## Gotchas

- Background jobs stop at their time limit (default 30 min). Give long runs `timeout` up to 2 h, and split longer ones.
- `pkill -f player_check` also kills the shell running it.
- A session worker restart re-runs a running background command from the start.
- `career_check` exits 1 on 0.64.8: known (backlog row 12). `perf_check` exits 1: the known +2 geometries.
- Two plain player_check runs give identical output, so a diff is meaningful. Anything reading `#toast`'s `show` class depends on real time.

## How to test

Setup as DEV_NOTES "Testing" (three r128 and acorn 8.12.1 in /tmp/cadet-work; `pip install playwright numpy pillow`; `CADET_CHROME=/opt/pw-browsers/chromium`). `bash check_fast.sh` before every push. For player_check: run the integration copy and this one on the same build and diff the output.
