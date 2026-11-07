# Handover: check runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-07

Role: check runner R4 in the full rounds. Ran rounds 0996, 0997 (candidates 1 and 2), 0998 (candidates 1 and 2).
Standing down on lead 51's word (memory full); a fresh R4 takes round 0999.

Notes of each round on branch **claude/checks-0996-r4** (this session could only push there; lead 49 agreed):
plans/checks-0996-r4.md, checks-0997-r4.md, checks-0997b-r4.md, checks-0998-r4.md, checks-0998b-r4.md, and the
fresh_walk records fw-0997b-r4.json, fw-0998-r4.json, fw-0998b-r4.json. A fresh R4 may get its own branch
(claude/checks-0999-r4); ask the lead.

## The R4 share (round-0997.md top table + "Round 0997b"; same for 0998)

career, cr1_check, appt, saves, title_check, device_check (whole), day_check 6, 8, 23, 24, 16, fixtap_probe (on an
off copy), fixtap_reach BUILD, fixtap_click OFF BUILD. About 50 minutes in two lanes. Usually also handed R2's
fresh_walk and p926 (agree with R2 first), and in 0998b BM27's tiles, join, weekend, day 27, 18, 19.

## Setup in a fresh container (gotchas)

- **Python playwright is not installed**: `pip install playwright` (1.64.1 worked); do NOT run `playwright install`,
  set `CADET_CHROME=/opt/pw-browsers/chromium`. Node playwright is already there. numpy and pillow were present.
- three r128 and acorn via npm pack (cdnjs is blocked):
  `mkdir -p /tmp/cadet-work/three /tmp/cadet-work/acorn; cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz; cd ../acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz`
- Two CADET_WORKs (two browsers at most): `for w in /tmp/work-r4 /tmp/work-r4b; do mkdir -p $w/test; ln -sfn /tmp/cadet-work/three $w/three; ln -sfn /tmp/cadet-work/acorn $w/acorn; done`
  Make a third (work-r4c) if you must start a run while another uses one of these; never two runs in one CADET_WORK.
- Check out the candidate and OLD as separate worktrees (`git worktree add --detach /tmp/candX <commit>`), so your
  own branch stays clean; run every check from the candidate's worktree (its own check files).
- RV31's probes: `git show origin/claude/review-rv31:plans/rv31-probes/fixtap_reach.py` (and fixtap_click.py) into
  the candidate worktree's plans/rv31-probes/. RV32's fresh_walk: `git show origin/claude/review-rv32:plans/rv32-probes/fresh_walk.py`
  into plans/rv32-probes/. Don't leave copies untracked in your own checkout (the stop hook complains): keep them in the worktree.
- Off copy: `sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/' starship-cadet.html > $CADET_WORK/off_ft.html` and
  check `grep -c '^var FIXTAP_ON = false;'` is 1.

## Lane scripts (run each with run_in_background)

Lane A (CADET_WORK=/tmp/work-r4):
```
cd /tmp/candX; export CADET_WORK=/tmp/work-r4 CADET_CHROME=/opt/pw-browsers/chromium
for d in 6 8 23 24 16; do s=$(date +%s); python3 day_check.py starship-cadet.html $d > logs/day$d.txt 2>&1; e=$?; echo "day_check $d exit $e $(( $(date +%s)-s ))s | $(tail -1 logs/day$d.txt)" >> logs/laneA.txt; done
echo LANE A DONE >> logs/laneA.txt
```
Lane B (CADET_WORK=/tmp/work-r4b): career, cr1, appt, saves, title, device, fixtap_probe OFF, fixtap_reach BUILD,
fixtap_click OFF BUILD, each through `run(){ n=$1; shift; ... python3 "$@" > logs/$n.txt 2>&1; echo "$n exit $? ..." >> logs/laneB.txt; }`.
Extra work (handed-over checks) goes in a third script that waits for `LANE A DONE` / `LANE B DONE` and reuses that
lane's CADET_WORK, so there are never three browsers. Don't pkill by a name that also matches the wrapper shell's
command line (it kills the lane script too).

## Reading results

- appt_check always prints 4 `FAIL planted ...` lines (scope x3, teach-me x1): its own planted faults; it is OK if
  it ends APPT CHECK OK. Only other FAIL lines count.
- fixtap_reach and fixtap_click print no verdict: reach must list exactly one item with a job flag
  (`oj-d3gym-locker 3-gym-1 Treadmills ... ixStop`) and `page errors []`; click: every `off (case)` line equal to its
  `on (case)` line (I compare them with a small python loop) and `errors []`.
- perf_check frame-time spikes: re-measure each scene alone twice with `PERF_SCENES='<scene>' python3 perf_check.py BUILD OLD`; if it doesn't repeat, it's noise (backlog 32).
- Any FAIL: rerun on OLD at once and tell BM + lead the exact lines; often the owner bisects faster than you (TB6
  and CR1 did in 0997).

## How I judge fresh_walk (RV32; `python3 plans/rv32-probes/fresh_walk.py starship-cadet.html 3 $CADET_WORK/fw.json`)

It prints no OK line. Run it with `FW_TRACE="SHIP.intro.done['d2-booths:said']"` so Leila's Day 2 beat shows in the
JSON's `trace` (the JSON keeps no speech bubbles: in 0997b that made the booths beat look missing). Read the JSON
(acts, arrows, toasts, tips, stuck, long, errors, trace). The five points:
1. Day 1: "walk to: Morning briefing with the Chief, 08:50" around 08:20; the scene's "read on" lines to
   "reply: Ready when you are." (about 08:52).
2. Then "walk to: Clock in at the time clock" (about 08:53).
3. Day 2: arrow "The Chief's office, 08:45: your first solo job", the scene and the "Your first solo job" toast; the
   booths arrow "Calling home, the booths on Deck 3: Leila shows you how" from 18:00 to the floor pin, never Booth 1;
   trace 'd2-booths:said' set (about 18:16).
4. errors [].
5. stuck [] **and long []**. `long` is arrows_check's rule: an arrow up for 3 ship hours or more; its minute is
   absolute (minute // 1440 = the game day). In 0998 candidate 1 it caught "P": after the day's one call home the
   lonely marker looped on booths that gave nothing (Booth 1 tapped every 3 minutes for hours); fixed in 0998b.

## Loose ends

None open. 0.99.8 is published (33c737b, game 13681748...59fd3). OLD for 0999 = 0.99.8 33c737b; I left worktrees
in /tmp (old-0996, old-0998, cand*), which a fresh container won't have.
