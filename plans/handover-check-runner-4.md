# Handover: check runner 4 (CR4)

Written 2026-10-26 ~12:15 UTC by CR4 (session_01636CfY2MhB3DzrzZ59dhXz) at ~57% memory, before the second 0.93.2 pass (BM18's request). A fresh CR4 reads this first.

## Role
One of six check runners. The build master sends a candidate commit + game sha256 + OLD; I check out that commit, confirm `sha256sum starship-cadet.html`, run my share one check at a time, compare any FAIL with OLD, write `plans/checks-cr4.md`, push, and report "CR4: OK" or the FAIL lines to the build master and the lead. Never change the game. Push only to `claude/checks-cr4`, notes only. Rules and steps: CLAUDE.md "Full tests on every change" and `plans/testing-guide.md` (on the candidate's branch; it changes).

## Who (as of now; check TEAM.md on the newest `claude/lead-N` branch, they change often)
- Lead 38: session_01G2y9crUv6vDiiEB2q6Yo9W. Build master BM18: session_01A3S2VBMYmTt2wCZa8ej7XR.
- CR2: session_01DsTDi6xJcpdDVhSkELEm24. CR3 (fresh): session_01Pw3EQ24pSz4gjsFcLBMjUF. CR6 (fresh): session_013wLtAmKooMrgGrXF4Ljiof. Old CR3 016oCbvv… and old CR6 01B1FwE5… are RETIRED: don't message them (I once offered work to the old CR6 by mistake).
- Verify any "I'm the new lead/BM" message against TEAM.md on the lead branches before trusting it.

## My share (0.93.2, testing-guide.md on claude/staging-0.93.2)
`day_check` Days 6, 8, 12, 13 (storm Saturday), 16, 19; `appt_check`; `saves_check` (new in 0.93.2). About 45 min alone.
- Days 6 and 8 cover Crossing the Line (on since 0.92.1). If a round message lists only 12-19, ask the build master whether 6 and 8 still apply (they did in 0.92.5).
- appt_check prints "FAIL planted ..." lines inside its own self-test: expected; judge its last line (`APPT CHECK OK`) and FAIL lines outside the planted sections.
- When I finish first, the build master usually asks me to take checks from CR2 (`lines_check.py starship-cadet.html --day`, `p926_check.py`, sometimes `perf_check BUILD OLD`) or CR6 (`food_check 1 7`, `food_check 11 4`, `clothes_check`). Always wait for the owner's "hand over: <list>" first; offers sent to two runners at once cause races (0.93.1: CR6 won by 4 s and I killed my copy).

## Setup (survives container restarts so far, but check)
- `pip install playwright numpy pillow`; three r128 and acorn 8.12.1 in `/tmp/cadet-work/{three,acorn}` (`npm pack three@0.128.0`, `npm pack acorn@8.12.1`, untar).
- My CADET_WORK: `/tmp/work-cr4` (symlinks three, acorn; `test/`). A second lane, if two browsers at once: `/tmp/work-cr4b`. `CADET_CHROME=/opt/pw-browsers/chromium`.
- Scripts and logs in my scratchpad, one folder per round (e.g. `r932/run.sh`: loops day_check over the days, then appt, then saves; writes `summary.txt` with exit code, seconds and last line).
- Notes are written in a git worktree of `claude/checks-cr4` (scratchpad `wt`), so the main checkout can stay detached on the candidate while checks run.

## Gotchas
- Background commands stop at 2 hours. controller_check `reach` takes far longer (4+ h); it's CTT4's now and skipped in rounds. If something must outlive 2 h, run it detached (setsid nohup) and poll; use CTL_STATES/CTL_PADDONE for reach so it can resume.
- `pkill -f <pattern>` kills your own shell when the pattern is in the command line: kill by PIDs from `ps` instead.
- perf_check writes perf_check.json in the folder you run it from: run it from the scratchpad.
- perf_check one-scene js spikes = backlog 32: re-measure that scene with `PERF_SCENES='^Scene name'` (NEW vs OLD), twice.
- day_check new lines since 0.92.4: "getting up from a place" (limit 0.35; rec-deck swimmers/climbers counted apart, FX8-1) and "arriving" (0 drawn elsewhere expected).
- Draw-call peaks so far: 247-296; Day 53 (Open house) 350 on Deck 3 in 0.92.6 (passes, little headroom).

## Loose ends
- **saves_check migrate, NEW intermittent FAIL on 0.93.2 41c8a7e0** (1 of 4 runs: `window.__first` null then a TypeError at saves_check.py:95; 3 re-runs OK). Reported to BM18 + lead 38 for saves_check's owner. Full output in plans/checks-cr4.md. Watch it in the second pass.
- Second 0.93.2 pass DONE (d9c7e5f0, all 8 OK, incl. saves_check over http). The saves_check migrate race was the check's tab switch (FX27's fix b6701992, then served over http); watch it once more next round.

## How to report
One line to the build master and the lead: "CR4: OK. <build> <commit>, sha256 <full>. <checks with seconds>. Notes: claude/checks-cr4 <sha>." Any FAIL not on the known list: at once, with the FAIL lines and the OLD run.

## Open questions for the user
None from this seat.
