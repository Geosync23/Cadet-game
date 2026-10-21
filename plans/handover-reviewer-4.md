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
| EV4 props + 8b hook | 96bb2c6 | PASS WITH FIXES (the mess only, not all of Deck 3) |

## The queue left for PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i): re-run in your own container

My runners were stopped at the handover. None of the items below has a result yet, apart from what's listed as done.

1. **EV2 storm S8 (claude/storm-s4s8 5cb698a, base af568f9).**
   - Done: cadet_test off ALL IDENTICAL; check_fast OK; code read OK (scriptBy officer/senior/specialist → calderStorm.officer; addrBelowHud in section 19's skin on `#devAddr`, under 600 px only, behind EV_STORM_ON).
   - Left: the phone shots, `plans/review-4/s8_banner.py S8_ON.html` (the save has 'evFrom': 0; Day 12 13:55; it checks the banner top against devBtn/pauseBtn/trkBtn at 390 and 360). Then the verdict to EV2 and the lead.
   - Nit to send: the top is set once, when the banner shows (no re-layout on rotation). EV2's own shots never reached the branch (*.png ignored).
2. **EV4 props (96bb2c6): verdict sent, PASS WITH FIXES** (dim the mess only, lead 23's call; the framedMenu 0.003 nit).
   - Left: one phone shot of the supper with the lanterns (`props_probe.py PR_ON.html`, shot timeout 180 s) and FEEL_S.lamp ≈ .85 there.
   - Check EV4's mess-only dimming when it lands.
3. **EV4 f32d901 (S3-S7 fixes, S9 framedMenu) and 2228a05 (crowd caps), base 74c216e.**
   - Code read: OK for both (evIsTrad plus x.base replaces the four identity tests; party places plus stay [30, 60]; supper .73; the stormScripts fallback; framedMenu behind `on()`).
   - Left to run:
     - cadet_test off (74c216e→2228a05);
     - events_check on;
     - bigevents_check (EC1's 037a149);
     - `lap_d15.py ON.html` (D15 Lap joinable:true expected);
     - day_check 13 and 14 on;
     - food_check on, 11 4 (Day 14 dinner wait must be ≤ 5);
     - check_fast;
     - phone shots of the framed menu (S9; deck 4, your bunk).
   - EV4 reports: the supper 59 mean to go, at most 51 at once; the party 45 come, at most 27 at once, 94 places, **416 calls at zoom 0.7** (watch the 450 budget).
4. **EC1 turns 9-11 (claude/bigevents-check ac32382, e3f1da9, 037a149):** check-only; EC1 reports check_fast OK.
   - Code read: OK (isTrad by id; CROWD 60; peak at once from the plans; stay gatherings judged by the peak; a planted dressed copy in the party's room in the self-test).
   - Left: the check on its branch, and on 2228a05 (expect OK). Then the mutants:
     - (a) isTrad reverted to `SHIP_TRADITIONS.includes(e.ev)`: exit 1 (the planted dressed clash uncaught);
     - game mutants on 2228a05: party `who: .7` → 1, party.stay → [110, 120] (peak over places), supper `.73` → .95 (over 60). Each must FAIL.

## Open items to follow

1. The S1 nits are left as is (EV4's call): "There's a commendation in your Mail" comes 12 minutes before the Mail; `allclear.you.jobs` can't be reached.
2. The crowd rule is settled (lead 23): at most 60 meaning to go; never more at once than its places, standing counted. 2228a05 follows it.
3. The props: the mess dimmed only (lead 23), not all of Deck 3.
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

About 485k of 1M at the handover (2026-10-21 ~09:55 UTC). Handed to PR6 on lead 23's word; PR4 is idle.
