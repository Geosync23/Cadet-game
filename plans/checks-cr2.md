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
