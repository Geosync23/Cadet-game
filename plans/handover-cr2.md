# Handover: check runner CR2

**Role:** CR2, one of six check runners in the full round (plans/testing-guide.md). Never changes the game or the
checks; pushes only results notes to `claude/checks-cr2`. Reports to the lead (now lead 35,
session_01VQkkt8RXcvvGs1Dmzn2emM) and the build master (now BM16, session_01MB7n4yvCAeGyWN4WZCAGPh).

**Results so far:** `plans/checks-cr2.md` on `claude/checks-cr2` (rounds 1-12 and 0.92.4, each with the commit,
sha256, a Check | Result | Key lines table, and any FAIL's proof).

## The share

intro_check (whole), perf_check BUILD OLD, cadet_test OLD BUILD (strictly alone), path, arc, lines, lines_check --day.
About 75 minutes alone; perf (~37 min) and intro (~27-32 min) are the long ones.

## How I run it

1. `git fetch origin <branch>`; `git worktree add $SCRATCH/rNNN <commit>`; `sha256sum` the game: must match the
   build master's (mismatch: tell everyone and stop). `git show <OLD>:starship-cadet.html > $SCRATCH/oldNNN.html`
   and check its sha too (it should be the last build signed off).
2. Setup once per container: `pip install playwright`; three.js r128 and acorn under `/tmp/cadet-work`
   (DEV_NOTES "Testing"); own work folder `/tmp/work-cr2` with `three` and `acorn` symlinked;
   `CADET_CHROME=/opt/pw-browsers/chromium`.
3. A small runner script (one check at a time, exit code + last line to `summary.txt`, and a `skip` file: any check
   name listed in `OUT/skip` is passed over, so a handover never runs twice):
   order cadet (from a `shots/` folder, alone, first) → path → arc → lines → intro → perf → lines_day.
   Re-create it from this list if the scratchpad is gone.
4. Handovers: early finishers (CR3/CR4/CR6) offer; reply "hand over: <list>" only for checks not started, add them
   to `skip`, copy the build master and the lead. Fill their results into the notes when they report.

## What to expect (gotchas)

- cadet_test: the build master says what differences to expect; compare DIFF lines and per-shot pixel counts with the
  last round's run (a `diff` of the two outputs). No page errors (`errors A [] errors B []`) is a must.
- perf_check: backlog 14 (+2 geometries a lap) and backlog 32 (a one-off js spike in one scene) are known; re-measure
  a spike once (a second run). KP1: the Line ceremony at 335 draw calls (accepted when breakfast is in).
  A draw-call rise that repeats is NOT noise (0.64.17 case, explained by where perf stands you: LEAD29-1).
- intro_check: part 12's new-game click can time out under load: re-run it once alone. To test one part quickly,
  exec the check up to `RELOAD_MS = ` and call its function (`solo(g)`, `firsts(g)`), or use `--firsts` / `--week`.
- lines_check: compare the warning count with OLD; warnings never fail.
- Bisect a new FAIL over the candidate's first-parent merges (`git log --first-parent OLD..NEW`), using the NEW
  commit's check file on each merge's game.

## Loose ends

None open. Last round: 0.92.4 5bad724d OK (claude/checks-cr2 a0008108). Waiting for 0.92.5.
