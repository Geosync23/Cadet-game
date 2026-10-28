# 0.95.0 full round: runner R2

- OLD: 0.94.0, claude/integration 6f1915cb, game sha256 `5f4c5415814c78eb4c93eaad76ecc35dfa53f1f7cbb4c1f5af541f3971900a0f` (matched).
- Share: intro_check (whole), perf_check BUILD OLD (alone), path, arc, lines, lines_check --day, p926; day_check Days 21, 22, 23, 24.
- Each candidate ran with its own checks, two browsers at a time, each in its own CADET_WORK (`/tmp/work-r2`, `/tmp/work-r2b`), and perf_check alone afterwards.

## Candidate 3 (the one to publish): claude/staging-p5s6 b5199dc3

Game sha256 `b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a` (matched). Run 2026-10-27 23:04 UTC to
2026-10-28. Two earlier starts (22:05 and 22:56) were lost to container restarts (only lines had finished each time);
the run below is a fresh, complete one.

| Check | Result | Key lines |
|---|---|---|
| lines_check | OK | lines_check: PASS (0 errors, 112 warnings) (6 s) |
| lines_check --day | OK | lines_check --day: PASS (0 errors) (751 s) |
| day_check 21 | OK | DAY CHECK OK (526 s) |
| day_check 22 | OK | DAY CHECK OK (521 s) |
| day_check 23 | OK | DAY CHECK OK (525 s) |
| day_check 24 | OK | DAY CHECK OK (523 s) |
| intro_check (whole) | OK | OK (3771 s) |
| path_check | OK | PATH CHECK OK (111 s) |
| arc_check | OK | ARC CHECK OK (28 s) |
| p926_check | OK | P926 CHECK OK (1146 s) |
| perf_check BUILD OLD (alone) | known old (backlog 32), see below | PERF CHECK: 6 problem(s) (4617 s), all JS frame time; draw calls, triangles and memory fine (round trips 521 -> 521 -> 521, a week 521 -> 522, as OLD) |

## Candidate 2: claude/staging-p5s6 82b02fb9

Game sha256 `4a4bed1c6d7b8cb4354d4c4217e970ba2d5b3758a7f0ade48c3c22b159069595` (matched). Superseded by candidate 3.

| Check | Result | Key lines |
|---|---|---|
| lines_check | OK | PASS (0 errors, 112 warnings) |
| lines_check --day | OK | PASS (0 errors) (710 s) |
| day_check 21 / 22 / 23 / 24 | OK x4 | DAY CHECK OK (485-501 s each) |
| intro_check (whole) | OK | OK (3617 s) |
| path_check | OK | PATH CHECK OK |
| arc_check | OK | ARC CHECK OK |
| p926_check | OK | P926 CHECK OK (1109 s) |
| perf_check BUILD OLD | not finished | first run cut by the 2-hour job limit after 57 min alone (it prints only at the end); the rerun stopped when candidate 3 came |

## Candidate 1: claude/staging-p5s6 e0084ca9

Game sha256 `d1666007e449f9bdcfc01d3f2f2c2a60dfeb866b46ddb23404c38df56f59f278` (matched). Superseded.

| Check | Result | Key lines |
|---|---|---|
| lines_check | OK | PASS (0 errors, 112 warnings) |
| lines_check --day | OK | PASS (0 errors) |
| day_check 21 / 22 / 23 / 24 | OK x4 | DAY CHECK OK |
| intro_check (whole) | OK | OK (3111 s) |
| path_check | OK | PATH CHECK OK |
| arc_check | OK | ARC CHECK OK |
| p926_check | OK | P926 CHECK OK |
| perf_check BUILD OLD | not finished | stopped at 50 min on lead 42's word (candidate 2 had come) |

## FAILs

Only perf_check on candidate 3, and it is the known one-off frame-time noise (backlog 32), not this build. The proof:

1. **Full run** (b5199dc3 vs OLD, alone, 77 min): 6 JS frame-time problems: Sunday dinner (portrait 1.91 -> 3.06 ms),
   lantern supper (landscape 2.19 -> 3.92), the Line supper (trifold-open-turned 2.07 -> 3.59), Bread day (portrait-wide
   2.26 -> 3.67; trifold-folded-turned 1.96 -> 2.99), the big jigsaw (portrait 1.06 -> 2.24). Every view has exactly
   OLD's draw calls, GL calls and triangles. Memory flat, as OLD.
2. **Re-measure alone** (`PERF_SCENES='Sunday dinner|lantern supper|the Line supper|Bread day|big jigsaw'`, 16 min):
   Bread day and the jigsaw clean (Bread day's average NEW 2.34 ms vs OLD 3.00). The three mess dinners flagged again,
   each on **other views** than before (Sunday dinner landscape 3.21 -> 4.95; lantern supper portrait-wide 2.33 -> 4.4,
   trifold-folded-turned, trifold-open-turned; the Line supper portrait 2.2 -> 3.95, landscape 2.68 -> 4.55). OLD's own
   averages moved from run to run (Sunday dinner OLD 2.07 ms, then 3.83).
3. **Order swapped** (`PERF_SCENES='the mess'`, `perf_check.py OLD.html BUILD.html`, so 0.95.0 is measured first and
   0.94.0 second, 15 min): now **0.94.0** gets the problems, in the same mess scenes: Friday dinner portrait 1.58 -> 3.24,
   lantern supper x3 (portrait-wide 2.45 -> 3.65), the Line supper landscape 2.47 -> 4.69. Averages, 0.95.0 then 0.94.0:
   lantern supper 2.36 / 2.97 ms, the Line supper 2.34 / 3.05, Friday dinner 1.85 / 2.18, Sunday dinner 2.61 / 2.75,
   breakfast 1.67 / 1.60.

Whichever file is measured second is slower in the busy mess scenes; the build doesn't matter. So these are the
run-order / one-off timing noise of backlog 32, not a regression in 0.95.0. Suggested addition to backlog 32: the
second build measured runs warmer/slower on this machine (load average about 8 on 4 cores during the full round), so a
flagged scene can repeat on a re-measure without being real; swapping the order is the test.

Nothing else failed in any candidate, so nothing else needed re-running on OLD.

## Verdict

**R2: OK on candidate 3 (b5199dc3)**: 10 checks OK, perf_check's only problems are backlog 32 noise (proof above).

## Notes for the next runner

- perf_check prints nothing until it ends and now takes over an hour alone; give it a long limit.
- intro_check's "#8 at line 14, the pair already said" and "#8 never walked far enough" lines are progress notes it
  prints, not failures.
- In a cloud session, a run started detached (setsid/nohup) is lost when the container is reclaimed while the session
  is idle; a tracked background job (Bash run_in_background) kept the container alive here.
- Never `pkill -f` / `pgrep -f | kill` a pattern that is in your own command line: it kills your own shell.
