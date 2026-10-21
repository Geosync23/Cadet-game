# Handover: turn reviewer 4 (PR4)

**Role:** the events team's turn reviewer for Starship Cadet (the storm update; EC1's bigevents_check). The job is adversarial: does a turn do what its plan says, does it break anything, are the checks run and green, does it work on a phone?
- Started 2026-10-21 ~04:50 UTC, taking over from PR3 (plans/handover-reviewer-3.md on claude/review-3).
- Reports to **lead 23** (session_01XXiKm9iPgm565SZ4n1knmU). Overnight mode: questions go to the lead, never the user.
- Pushes only to **claude/review-4**: notes in `plans/review-4.md` (every verdict with its evidence); probes and mutants in `plans/review-4/`; shots in `plans/review-4/shots/` (force-added: `*.png` is in .gitignore).
- Owner hooks: PB (session_01FWW2piuXkFYaRRzLXZiqYb) reviews sections 13, 14 and 10. PR4 stands in for the others: 15r, 16, 17, 19, 20, 4d, 8b.
- The Fridays turns (FR2, claude/fridays, from 8415d1e) moved to **PR5**. ER2 does the build review of the storm update (f32d901) in parallel.

## Who's who

- EV4, the storm builder now, claude/storm-update: session_01MqpjPG6mDFe5avrDxcNWTU. EV3 (session_01ReekSsFi1ToaTpSq926Drq) has handed over: plans/handover-storm-builder.md.
- EV2, S4/S8 on claude/storm-s4s8: session_017S7eVMgX34nSt8fxZ5kat9.
- EC1, bigevents_check on claude/bigevents-check: session_01QgShGXD6P24DDxTp8npN41.
- FR2 (Fridays, now PR5's): session_019m7hCEtBsPA3ascA2Bqu9V.

## Verdicts so far (details in plans/review-4.md)

| What | Commit | Verdict |
|---|---|---|
| EV3 storm S1 | 9561f48 | PASS WITH FIXES, then the fixes (3367aab, 4476186) PASS |
| EC1 turns 7, 8 | cdf80ce, f9b2b0b | PASS (mutants c1-c6) |
| EV2 storm S4 | f2a0eaa/af568f9 | PASS |
| EV3 storm S3/S5/S6/S7 | d3bf237 | PASS WITH FIXES (sent to EV4): 1, the dressed Lap not joinable; 2, crowds; 3, Day 14 dinner wait; 4, the check's filter (EC1) |
| EV4 day_check R6 skip | 4fa198f | PASS |
| EV4 standing diners | b9aa775 | PASS (section 18; section 10 is PB's) |

## In flight when this was written (results in the scratchpad's res/, see "How to test")

- **EV2 S8 (5cb698a).**
  - Checked: cadet_test off ALL IDENTICAL against af568f9; check_fast OK. Code read OK: scriptBy from officer up; addrBelowHud in the 19 skin, `#devAddr`.
  - Still to come: the banner shots at 390/360 (`s8_banner.py`, run last in the queue).
  - Nit to send: addrBelowHud sets the top once, when the banner shows (no re-layout on rotation). EV2's shots never reached the branch (*.png ignored).
- **EV4 props + 8b hook (96bb2c6).**
  - Checked: code read OK (no R(), col()/dressMat, overlapping parts, 2 draw calls each; the 8b hook is lamp eased toward stormSupperDim, 0 while off).
  - Live: the props probe at Day 13 18:23 gives 60 in the mess and 219-220 calls. The shot timed out twice; it's re-running with a 180 s timeout (`props_probe.py`).
  - Judgement call for the lead: **the whole of Deck 3 dims, the plan says the mess.**
  - Still to come: pr_ct, pr_cf.
- **EV4 f32d901 (S3-S7 fixes, crowds, S9 framedMenu).**
  - Code read OK: evIsTrad plus x.base; party.stay [30, 60] on its 34 seats; the stormScripts fallback; framedMenu behind `on()`.
  - Nit: framedMenu's card plane sits 0.003 in front of the frame's face. Check for shimmer on a phone.
  - Queued: cadet_test against 74c216e, events_check on, bigevents, lap_d15, day_check 14, food_check 11-14, check_fast.
  - Open: the supper has 63 meaning to go, against EC1's CROWD of 60 (peak 54 at once). This needs the lead's call or EV4's trim.
- **EC1 turns 9-11 (ac32382, e3f1da9, 037a149).**
  - Code read OK: isTrad by id; CROWD 60; peak at once; stay gatherings judged by peak.
  - Queued: ec10_own (the branch), ec9_mut (isTrad reverted to includes: the planted dressed clash must go uncaught, so exit 1), ec10_f32, and game mutants in res/../mut10 (p1 party who 1, p2 party stay [110, 120], p3 supper who .95). Each must add a FAIL beyond f32d901's baseline (the supper's 63).

## Open items to follow

1. The S1 nits are left as is (EV4's call): "There's a commendation in your Mail" comes 12 minutes before the Mail; `allclear.you.jobs` can't be reached.
2. The supper's means-to-go (63) against the check's 60: the lead's call.
3. The S8 banner shots; the props shot.
4. Backlog: #18 (day_check Day 12 rec guard, fails off too); 18b (perf_check scenes in the wrong room, confirmed by OP1); 18c (join_check first-light).

## How to test (this container)

- Setup:
  - `pip install playwright`;
  - three and acorn in /tmp/work-RV4 (`npm pack three@0.128.0`, `acorn@8.12.1`, untar);
  - `CADET_CHROME=/opt/pw-browsers/chromium`;
  - PR3's probes need /tmp/rv/pp.py (from claude/patch-plan plans/patch-plan-probes/pp.py) and a /home/user/Cadet-game symlink to /home/user/cadet-game.
- My probes load `plans/review-4/pp.py` (cadet_test.py's top).
- Worktrees per head in the scratchpad's `w/<x>`. A switched-on copy: `sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/'`.
- Runs go one at a time through resumable runner scripts: each step writes `res/<name>.log` plus `.done`, and an `ALLn` file chains the runners. The container restarts now and then.
- Probes: `s1_hours.py`, `s1_pick.py`, `s4_help.py`, `s37_probe.py`, `props_probe.py`, `s8_banner.py`, `lap_d15.py`. Mutants: `ec_mutants.py` (c1-c6 added).

## Gotchas

- **The calendar and saves:**
  - A save that starts after an event's day passes that event over (F0c: evFrom = the load day). Put `'evFrom': 0` in the save's ship.
  - The device's heads-up replaces a meeting's own toast, so `told:` stays unset.
- **The storm's machinery:**
  - machinesNow runs an hour as soon as its first minute comes, so jobs with `at` later in that hour are posted early with a future `posted`. jobsBoard hides them (the S1 find).
  - events_check's LIVE part runs the storm on Day 10, a Works drill day, so the briefing pick stays open there by design.
  - EV_DAY_DRESS copies are new objects: compare by id or `ev.base` (evIsTrad), never by identity.
  - The Captain's banner on a phone is `#devAddr` (section 19's skin), not ADDRESS_EL.
- **Tooling:**
  - `pkill -f <name>` / `pgrep -f` also match your own shell's command line: kill by PID from `ps -eo pid,args`.
  - Never edit a runner script while it runs (bash reads it as it goes): kill it and write a new one.
  - Screenshots of the mess with 60 crew can take over 30 s in software rendering: pass `timeout=180000`.
  - cadet_test sometimes prints "renderer noise: 1 level": documented, not a change.

## Memory

About 460k of 1M when this was written (2026-10-21 ~09:35 UTC).
