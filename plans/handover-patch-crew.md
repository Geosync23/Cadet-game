# Handover: patch builder PT1, the crew rotation and the camera (claude/patch-crew)

Role: patch builder PT1 under lead 23, then lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r). Reviewer PR7 (session_01LyKAVtCEedL1bP73vqzu9v); owner review for sections 13/14/10: PB (session_01FWW2piuXkFYaRRzLXZiqYb). Branch `claude/patch-crew`, made from `claude/integration` at 0.64.8. The build lines are untouched (the build master sets them).

## What the user decided (2026-10-21) and what was built

| Turn | Commit | What |
|---|---|---|
| T1 | 1badd51 | The first crew rotation moves from Day 35 to **Sunday Day 21** (`ROSTER_ROTATIONS`, Theo Teague `aboard: [null, 21]`, Basil Bramwell `[21, null]`, `ROTATION_DAYS` in plans/crew-roster-gen.py). Camera's opening zoom a step closer. |
| T2 | 4dbdca8 | New hand's tea on the **first Thursday** after every rotation (Day 25 for the first). New tradition **Off the Tern** (k 454, checked free by EC1). `ROT_TERN` (on): arrivals step out of the Tern's aisle at 17:40, one every 3 minutes, walk down the ramp to a held crowd spot; a greeter (Zeke for Works, else the department's most senior aboard and off shift) at the ramp's foot; the ramp shuts at 17:36 and opens at 17:40 with Dev Raman's line. Camera to **1.85 upright / 1.40 wide** (the user: "another 10-15 percent"; was 1.5/1.15). |
| T3 | a5e78d3 | **Leavers board the Tern up its ramp** (the user's yes), one every 3 minutes, the last at 15:00; the ramp stays shut from 15:00 until the arrivals at 17:40 (never with you inside). |
| T3b | d66f568 | My T3 bug fixed (the ramp shut at 17:36 every day); events_check 9d2 checks the Tern scene on paper (PR7's ask); a leavers-only day reopens the ramp at 17:40; Off the Tern's thanks line reworded. |

Also: the shots in `plans/patch-crew-shots/` (camera before/after, the ramp scene, the boarding; force-added, `*.png` is in .gitignore); DEV_NOTES "Crew rotations off the Tern" plus a hook-register row; design-doc (the rotation calendar, Off the Tern, leavers, the Camera line); build-table rows "patch crew T1/T2/T3/T3b (PT1)"; a backlog row (the Tern's tap text while it's away).

## Where the code is

- Section 14: `ROT_TERN` beside `ROTA_OFF`/`ROTA_ON`; guestTrim's arrival branch (`rotTernIndex`) and leaver branch (`rotTernBoard`); one line each in `gatherings` (`rotTernGreet`), schedData (`rotTernPools`: key `5|@tern-foot`) and shipDay (`rotTernHold`); the `rotTern*` functions at the bottom of the Sim engineer's slot (all pure: the roster's aboard days and `shiftBlocks`).
- Section 10: `crewArrive` starts an arrival from away at a Tern place inside the Tern; `CrewAgent.update` lets a leaver finish walking into the Tern, then removes them; `updateDeckCrew` calls `rotTernTick` (live ramp state, not saved).
- Section 18's loader skips `off-the-tern` with `ROT_TERN` off. Section 6: the opening zoom line.
- Content: `content/traditions/off-the-tern.trad` (new), `crew-welcome-tea.trad` (`rotation thursday`), baked by content_gen.py.
- Checks changed: events_check (9d pins the tea to Thursday; 9d2 Off the Tern on paper and the ramp), join_check (Basil@22), social_check (the moved-on test leaves out the roster's own leavers).

## How to test

`day_check.py BUILD 21` (and 20, 22, 25, 161), `events_check.py BUILD` (9d, 9d2), `join_check`, `social_check`, `intro_check`, `cadet_test` (Day 1 is unaffected by the rotation; the camera moves every shot), `check_fast.sh`. A Deck 5 probe: skipTo Day 21 14:40 or 17:33, goToDeck(5), stand the player two tiles east of `5-tern-ramp-foot`, step frames (50 frames = 1 ship minute) and read `ternRampOpen()` and `DECK_CREW`.

## Gotchas

- The ramp isn't saved: a reload finds it open, then rotTernTick shuts it again in its window (visible as a swing).
- `ROT_TERN_MAX` is 3 (the most arrivals or leavers on one rotation today); more than 3 fall back to the lift.
- A comment added after code with `//` inside a check's JS string ends the line for the browser: use `/* */` (it broke social_check once).
- Only one arrival on Day 21; the stagger was checked on deck on Day 161 (three each way).

## Loose ends / open

- Backlog: the Tern's tap text doesn't say it's away 15:00-17:40 on a rotation day (section 4d's words).
- FR3 (claude/fridays) knows: Day 21 (15:00 out, 17:40 in), the tea Thursday Day 25; 18f's weekly address names Basil and Theo on Day 26.
- Waiting: PR7's confirmation of T3b, and BM12's merge into claude/integration.
