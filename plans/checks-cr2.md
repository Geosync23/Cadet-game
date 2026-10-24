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

# Round 4: 0.64.15 re-run (claude/integration-next 31c44cb9, 2026-10-22), CR2's share — **OK**

NEW 31c44cb9, sha256 `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e` (matches lead 26's).
OLD claude/integration 32b699a6 (0.64.14), sha256 `94f32868...881e9` (matches).

| Check | Result | Key lines |
|---|---|---|
| intro_check (whole) | OK | `OK` (part 14: "step by step (0 on the shelf): Make a relay ...", accepted) |
| perf_check NEW OLD | known old only (backlog 14) | `memory grows across deck round trips` 521 → 521 → 523. First run also `lantern supper, the mess Sat 18:30 trifold-folded-turned: js 1.77 -> 2.91 ms`; **re-measured: doesn't repeat** (OLD 2.14, NEW 1.78 ms; `PERF CHECK: 1 problem(s)`, backlog 14 only). Two rounds, two one-off spikes in different scenes: renderer timing noise. |
| cadet_test OLD NEW | DIFFERENCES, all explained | Pixel counts identical to round 3 (patch C's crew lanes); state/collide = patch H's ladder rooms. |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings) |
| lines_check --day | OK | PASS (0 errors) |

# Round 5: 0.64.16 (claude/integration-next b9f053ba, 2026-10-22), CR2's share — **OK**

NEW b9f053ba, sha256 `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7` (matches BM13's).
OLD claude/integration 2b4a05db (0.64.15), sha256 `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e`.
Split by agreement (copied to lead 28 and BM13): path, arc, lines, lines --day → CR4 (all OK, plans/checks-cr4.md
725c250f); cadet_test → CR3 (ALL IDENTICAL, claude/checks-cr3 890ef899). CR2 ran intro and perf.

| Check | Result | Key lines |
|---|---|---|
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | known old only (backlog 14) | `memory grows across deck round trips` 521 → 521 → 523. First run also `the Line supper, the mess Sun 18:30 trifold-open-turned: js 2.05 -> 3.08 ms`; **re-measured: doesn't repeat** (OLD 2.27, NEW 2.04 ms; `PERF CHECK: 1 problem(s)`). Third round running with a one-off spike in a different scene. |

# Round 6: 0.64.17 (claude/integration-next 8193458e, breakfast at 07:00, 2026-10-22), CR2's share — **OK**

NEW 8193458e, sha256 `225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5` (matches BM13's).
OLD claude/integration b9f053ba (0.64.16), sha256 `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7`.
Order this time: cadet_test first (alone), path, arc, lines, intro, perf, lines --day. Results to BM14 and lead 29.

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW | DIFFERENCES, expected | Breakfast's moved mornings: needs and taps differ from tap1 on ("Very hungry" / "Bursting" vs the old), walks, state tris, state_end; g_nocrew only 149 px; no page errors (A [] B []). RV3 proved ALL IDENTICAL with patch F's section 14/16 code reverted. |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings) |
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | OK (accepted baseline + backlog 32) | `the Line ceremony, bow lounge Sun 14:45 portrait: draw calls 301 -> 335` (49 people, was 59; every view up ~20-34), repeats exactly on the re-run. **Lead 29 accepts it as 0.64.17's new baseline**: perf_check stands you on the free tile nearest the room's middle, which with breakfast's crowd is (44,10) not (46,9), so the camera sits ~2 m aft and the mess, galley and spine come into view (SC1's finding; under 450; backlog LEAD29-1: a fixed tile per scene). One-off js spikes, a different scene each run (backlog 32): all-clear party portrait 1.55 → 3.16 ms (run 1, gone in run 2), quiz night portrait-wide 1.79 → 2.85 ms (run 2 only). Backlog 14's +2 geometries didn't show this time (521/521/521 both runs). |
| lines_check --day | OK | PASS (0 errors) |

# Round 7: 0.64.17 (claude/integration-next 1498dbf4: + SC1's Line supper fix, CP4's bubble slides), CR2's share — **OK**

NEW 1498dbf4, sha256 `ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306` (matches lead 29's).
OLD b9f053ba (0.64.16), sha256 `70f94273...e6a5c7`. perf_check handed to CR3 (agreed, copied to BM14 and lead 29).

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW | DIFFERENCES, expected | Every DIFF line and pixel count identical to round 6 (8193458e, breakfast); BM14: 8193458e vs 1498dbf4 ALL IDENTICAL. No page errors. |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings) |
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | OK (CR3, accepted baseline) | Only `the Line ceremony ... portrait: draw calls 301 -> 335` (the accepted baseline); no backlog-14 memory flag, no js spike (claude/checks-cr3 4a681ec1) |
| lines_check --day | OK | PASS (0 errors) |

# Round 8: 0.91.0 (claude/integration-next 989fd566: CP1's controller, PAD_ON off, + fresh-eyes batch 1), CR2's share — **OK**

NEW 989fd566, sha256 `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee` (matches BM14's).
OLD b9f053ba (0.64.16), sha256 `70f94273...e6a5c7`. perf_check and lines_check --day handed to CR4 (agreed, cc BM14, lead 30).

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW | DIFFERENCES, exactly as BM14 expected | 3638 px in all 15 shots (the old HUD New game button); extra only in e_night..i_tap3 (15023-15633 px: the lift-panel arrow's label); no DIFF in state, paths, collide, crew or taps; no page errors. |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings) |
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | known old only (CR4) | backlog 14 (521/521/523, the same on OLD); all scenes identical to OLD; the Line ceremony back to 301 calls (no breakfast) |
| lines_check --day | OK (CR4) | PASS |

# Round 9: 0.92.0 (claude/integration-next 4147f03d: teaching arrows on, breakfast back, Zeke's tour, dinner spread), CR2's share — **FAIL (2 new)**

NEW 4147f03d, sha256 `c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286` (matches BM14's).
OLD 989fd566 (0.91.0), sha256 `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee`.

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW | DIFFERENCES, expected | The same DIFF lines as round 6's breakfast build (needs/taps from tap1, walks, state tris, state_end), pixel counts within a few dozen of round 6; g_nocrew 149 px; no page errors. |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | **FAIL, NEW** | `ERROR lines/torres-zeke [mail.zeke.land] "Before you land \| New hand, I'm writing this befor": 475 characters (at most 400)` (Zeke's device hand-over Mail, cb57522d). 0.91.0: 0 errors. |
| intro_check (whole) | **FAIL, NEW** | part 13 only: `FAIL someone took the booth the call arrow was on, and it stayed there (FX5): ['3-callhome-1', '3-callhome-1']`. Repeats with `--firsts` alone. |
| perf_check NEW OLD | OK (accepted baseline) | Only `the Line ceremony ... portrait: draw calls 301 -> 335` (49 people), = lead 29's accepted breakfast baseline from 0.64.17 (breakfast is back). No memory growth (521/521/521), no js spike. |
| lines_check --day | OK | PASS (0 errors) |

## intro part 13 (FX5): why it fails

A probe at the check's moment (Day 0 Sunday 18:26): crew already hold booths 3-callhome-2, -3 and -4 (`heldBy`); only -1
is free. The check puts a stand-in on -1, so all four are taken, and `introCallTick` keeps the arrow as it was, by its
own rule ("all taken: as it was, where the line forms"). So the check's assumption that a free booth exists doesn't hold
at 18:26 in 0.92.0 (the later arrival / tour / dinner spread puts crew on the booths). Looks like a check-setup issue,
not a game bug; the arrows/FX5 owner's call. Not fixed.

# Round 9b: 0.92.0 re-run (claude/integration-next 4e324417: FX5's Day 0 table fix), BM14's two checks — **OK**

NEW 4e324417, sha256 `f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd` (matches BM14's). OLD 989fd566 (0.91.0).

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW (alone) | DIFFERENCES, expected | Every DIFF line and every shot's pixel count identical to round 9 (4147f03d): the breakfast pattern; no page errors. |
| intro_check (whole, 4e324417's check) | OK | `OK`, 0 FAIL lines (part 13's FX5 booth FAIL gone) |

# Round 10: 0.92.1 (claude/integration-next 51a1bb34: the Line switched on, + fixes), CR2's share — **OK**

NEW 51a1bb34, sha256 `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c` (matches BM15's).
OLD 685af944 (0.92.0), sha256 `f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd`.
perf_check and lines_check --day handed to CR4 (agreed, cc BM15, lead 31).

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW (alone) | OK | `ALL IDENTICAL` |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings; the same count as 0.92.0) |
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | OK (CR4) | exit 0; the Line ceremony 335 calls (KP1); vs OLD only Sunday dinner 66 people vs 69, junior wing +5k triangles, storm all-clear +2 calls |
| lines_check --day | OK (CR4) | PASS |

# Round 11: 0.92.2 (claude/integration-next ee974894), CR2's share — **OK**

NEW ee974894, sha256 `ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4` (matches BM15's).
OLD e03505fd (0.92.1), sha256 `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c`.
perf_check and lines_check --day handed to CR4 (agreed, cc BM15, lead 32).

| Check | Result | Key lines |
|---|---|---|
| cadet_test OLD NEW (alone) | OK | `ALL IDENTICAL` |
| path_check | OK | `PATH CHECK OK` |
| arc_check | OK | `ARC CHECK OK` |
| lines_check | OK | PASS (0 errors, 50 warnings; the same as 0.92.1) |
| intro_check (whole) | OK | `OK`, 0 FAIL lines |
| perf_check NEW OLD | known old only (CR4) | backlog 32: Sunday dinner landscape js 1.66 -> 3.28 ms, gone on 2 re-measures; everything else identical to OLD; the Line ceremony 335 calls (KP1) |
| lines_check --day | OK (CR4) | PASS |
