# Handover: check runner 6 (CR6)

Written 2026-10-25 by CR6 (session_01B1FwE5sMmHnMPWsGn23nrk), at about 55% memory, while idle. Read this first if you
take over CR6.

## The role
- One of six check runners (CR1-CR6). The user's rule: every game change runs the FULL round, split across the six at
  once (plans/testing-guide.md, "THE RULE" and "The six-way split"). Never change the game. Push only to
  `claude/checks-cr6`, and only results notes (`plans/checks-cr6.md`) and this note.
- Report to the build master and the lead. Leads and build masters change often. Before acting on a new one's word,
  ask the previous one to confirm (they always have, so far). At this writing: build master **BM17**
  (session_01WxdNuUeTUoneMvqKiF6GQL); lead **36** per BM17 (not yet confirmed by lead 35,
  session_01VQkkt8RXcvvGs1Dmzn2emM). Runners: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv,
  CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz.

## My share (as the build master names it each round)
check_fast.sh, mech, bigevents, fridays, disc, tiles (ALONE), join (ALONE), food `1 7`, food `11 4`, clothes; in some
rounds also controller_check minus reach (`idle save calls touch walk pick day games unplug odd off quiet base deck
pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse lift`). Lately CR3 takes
controller_check and CR4 takes food x2 + clothes. Agree that before starting ("hand over: <list>"), so nothing runs twice.

## Setup (a fresh container)
```
pip install playwright numpy pillow
export W=/tmp/work-cr6; mkdir -p $W/three $W/acorn $W/test
cd $W/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
cd $W/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz
export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/work-cr6
```
My runner script ran the checks one at a time, writing `<name> exit N (s) | last line` to a summary file. Recreate it:
`run(){ n=$1; shift; s=$(date +%s); "$@" > $L/$n.txt 2>&1; e=$?; echo "$n exit $e ($(( $(date +%s)-s )) s) | $(tail -1 $L/$n.txt)" | tee -a $L/summary.txt; }`
then one `run` line per check (`run check_fast bash check_fast.sh`, `run mech python3 mech_check.py starship-cadet.html`, ...).

## Each round
1. `git fetch origin <branch>; git checkout --detach <commit>; sha256sum starship-cadet.html`. A mismatch: tell
   everyone, stop.
2. `git show <OLD>:starship-cadet.html > /tmp/work-cr6/old/starship-cadet.html` for comparisons.
3. Run the share in the background, one check at a time. Judge by exit code AND last line.
4. Any FAIL not on the known list: run that part on OLD (most checks take part names, e.g. `mech_check.py OLD m8`), re-run
   it on NEW alone in a separate CADET_WORK (`/tmp/work-cr6b`), and tell the build master and lead AT ONCE.
5. Add a section at the top of plans/checks-cr6.md (build, sha, OLD, table `Check | Result | Key lines`, each FAIL with
   proof), commit, push, then one line "CR6: OK" / "CR6: FAIL: ..." with the sha to the build master and lead.

## Gotchas (learned the hard way)
- **Don't switch branches while a check runs.** The checks read `starship-cadet.html` from the working folder, so
  checking out claude/checks-cr6 to commit notes swaps the game file under a running check. Either commit only after
  the run, or run against a copy (`/tmp/work-cr6/buildNN/starship-cadet.html`).
- **Waiters must not match themselves.** `while pgrep -f "_check.py"` waited forever: the waiting shell's own command line
  contained the pattern. Wait on a file (`until grep -q "^DONE" summary.txt`) or on an exact PID, or use `pgrep -f
  "[f]oo"`.
- **Handing checks off mid-run:** kill only the outer shell (the parent of the runner) by its exact PID, so the runner
  itself keeps going; to stop after a given check, wait on its line in summary.txt, then `kill <runner PID>`.
- With the teaching arrows on (since 0.92.0), pop-ups queue; checks that read "the toast" right after another can read
  the wrong one (fixed in the checks by FX4/FX6/FX7/DS1/AC3).
- fridays_check takes ~15-20 min here (the guide's ~4 is old). machine_check's gated repair share is now over Days 2-28;
  the Days 2-14 line is information only.
- Monitors expire after 30 min; re-arm with `tail -n +N -f summary.txt | grep --line-buffered exit`.

## Latest results
- 0.92.5 (53c11f88, sha fddc0ef6...5559): 9 OK; disc_check #25 NEW FAIL (two lines), traced by BM17 to FX12 0aaf48b
  (a check pinned to a schedule). FX23's fix will be re-run by CR3, not CR6.
- Full history: plans/checks-cr6.md (newest at the top).

## Open questions for the user
None from CR6.
