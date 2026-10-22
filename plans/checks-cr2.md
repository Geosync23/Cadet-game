# CR2's check round on the release candidate (2026-10-21)

Check runner CR2, for lead 25 and release reviewer PR9. Notes only: no game or check file changed.

## The build (local, not pushed)

- Start: `claude/integration` a4a5735 (0.64.12).
- `git merge 0b77dfcb` (claude/storm-update): conflict only in `plans/backlog.md` (both sides' rows kept).
- `git merge 3bd9b2c` (claude/fridays): conflict only in `plans/backlog.md` (both kept; row 21 was on both
  sides, the integration copy is the longer one with DB2's "Likely cause and fix", so that one was kept).
  `plans/build-table.md` merged by itself. No conflict in the game or the checks.
- `day_check.py` is storm-update's own (identical to 0b77dfcb's, which has EV4's 4fa198f skip).
- Switches as merged, matching PR9's notes (`plans/review-9.md` on claude/review-8, "The release build"):
  `SHORT_FRIDAY = true`, `EVENTS_ON = true`, `EV_STORM_ON = EVENTS_ON`. No hand edit was needed.
  `GAME_BUILD` still '0.64.12' (the build master's line).
- `content_gen.py --check`: up to date. `names_check`: OK.
- **sha256 of starship-cadet.html: `23fb9118abc3679fd1eea658a072817fd6f2831a9560f1bf86358ada768cb7df`**

Note: claude/fridays' tip is now cc68abd (newer than 3bd9b2c); this round used 3bd9b2c as asked.

## Results (CADET_CHROME=/opt/pw-browsers/chromium, one at a time)

| Check | Result | Key lines |
|---|---|---|
| talk_check | OK | `TALK CHECK OK` (0 FAIL lines) |
| social_check (14 days) | OK | `SOCIAL CHECK OK`, errors [] |
| join_check | OK | `JOIN CHECK OK` |
| lines_check | OK | `lines_check: PASS (0 errors, 49 warnings)`; plain integration has 6. The 43 new are all "the same line is also in meeting ..." in the storm's meetings (calderStorm.officer 14, captainAllClear.smooth 13, captainAllClear.rough 13, calderStorm, introChief, introBunk 1 each). Warnings only. |
| lines_check --day | OK | `lines_check --day: PASS (0 errors)` |
| food_check 11 4 (the build master's release run) | **FAIL** | `FAIL harvest salad: {... 'h': 20, ... 'salad': "Theo's favourite, for the farewell"}` |
| food_check 1 7 (defaults) | OK | `FOOD CHECK OK` |
| mech_check | OK | `MECH CHECK OK` (m1-m17) |
| career_check | FAIL (known) | `FAIL busy: "Relied on" before Day 5` only: backlog 12, known and accepted. The same on plain integration a4a5735. |

## The food_check 11 4 FAIL: old, not new to the release

- The same FAIL on plain claude/integration a4a5735 (events off).
- Bisected on integration: OK at 422ba6b (just before the crew patch), FAIL at 376469c (the crew patch merge,
  0.64.11). With the first crew rotation on Day 21, Day 20 is the farewell supper, and food_check's harvest
  day for `11 4` is Day 20 (`'h': 20`): the galley's dinner note becomes "Theo's favourite, for the farewell"
  (section 16, `galleyFav`, ~line 16095 in the release), so part 4g's `'salad' in ev['salad']` fails.
  `food_check 1 7` (harvest Day 10) passes.
- **No backlog row found** for it (searched "salad", "farewell"). Not fixed here. Whether it's a check case to
  move (a harvest day that isn't a farewell) or the farewell should keep the salad is for the food/crew owners.

## Not run

Nothing else from the brief was skipped.

# Round 2: 0.64.14 (claude/integration 8e239328, 2026-10-22)

Checked out as is (no merging). sha256 of starship-cadet.html `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`
(matches lead 25's); `SHORT_FRIDAY = true`, `EVENTS_ON = true`. Each check run from that commit's own check files, one at a time.

| Check | Result |
|---|---|
| talk_check | OK |
| social_check | OK |
| join_check | OK |
| lines_check | OK: PASS (0 errors, 49 warnings, the same as round 1); `--day` PASS (0 errors) |
| food_check 11 4 | OK (round 1's harvest-salad FAIL is gone) |
| food_check 1 7 | OK |
| mech_check | OK |
| machine_check | OK |
| career_check | FAIL (known): only `FAIL busy: "Relied on" before Day 5`, backlog 12. The same on 0.64.13 a7477a9. |
| bigevents_check | OK |
| day_check Days 1, 12, 13, 16 | OK, OK, OK, OK |

# Round 3: 0.64.15 candidate (claude/integration-next c5c43293, 2026-10-22), CR2's six-way share

NEW c5c43293, sha256 `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25` (matches lead 26's).
OLD claude/integration 32b699a6 (0.64.14), sha256 `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9` (matches).
Share (plans/testing-guide.md): intro (whole), perf NEW OLD, cadet_test OLD NEW, path, arc, lines, lines --day. CADET_WORK=/tmp/work-cr2.

| Check | Result | Key lines |
|---|---|---|
| intro_check (whole) | **FAIL, NEW** | part 14: `FAIL the solo job's arrow does not walk its steps like a board job: ['Make a relay in the machine shop', 'Take the lift to Deck 4: look over the light relays', 'Take the lift to Deck 4: repair the light relays', 'Turn it in at the job board']` (the only FAIL) |
| perf_check NEW OLD | FAIL, known old (backlog 14) | `memory grows across deck round trips` 521 → 521 → 523 geometries. First run also had `storm all-clear party ... landscape: js 1.61 -> 3.39 ms`; **re-measured: doesn't repeat** (1.52 → 1.65 ms; second run `PERF CHECK: 1 problem(s)`, backlog 14 only) |
| cadet_test OLD NEW | DIFFERENCES, all explained | Shots differ (a_start 3799 px ... h_crewback 40517, e_night/j_steer 0): the same counts already at d64d4495 (patch C alone), = PB2's recorded crew lanes; OLD vs OLD: ALL IDENTICAL. State edges/blocked/roomTiles/closed/doors + collide probes: first at c89f3f3f (patch H), = LR1's recorded ladder-room change (lead 26 and BM13 confirm). |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings; 0.64.14 had 49: new "Attendance looks like a name" in event.crossingLine.mail.warning, and a "(Just nod)" repeat moved from introBunk to introDevice) |
| lines_check --day | OK | PASS (0 errors) |

## intro_check part 14: NEW, a merge interaction of patches A and D

- Part 14 alone (a driver running only intro_check's `solo(g)`, c5c43293's check, ~40 s) on each integration-next merge:
  OK at a8e989d2, 2570df99, 17384f27, 313c8ace, e33d8ac8, fb2f95d5, c665e1c6; FAIL at 1fc77140 (patch A, ON1 8c8bf8fd),
  c89f3f3f, 52e5c347 and c5c43293. Patch D's own tip ede7432b with its own check: OK.
- Cause: the solo job (reserve3:4-junction-2) needs a relay and a bracket. Lights shelf relays at 08:59: 3 on both;
  at 10:41 (after the check's walk to 10:40, crew running): 1 before A, **0 after A**, so the arrow rightly falls
  back to "Make a relay in the machine shop" (section 15b's goal: stores empty → make).
- Not fixed. CJ1 is on it (lead 26). Owners' call: keep a relay for the solo job, or the check takes make as step 1.
