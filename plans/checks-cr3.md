# Check runner CR3: the release candidate (0.64.12 + storm update + Short Fridays)

Run 2026-10-21 by CR3 for lead 25 and PR9. No game change; this note is the only file on the branch.

## The build (local)

- Start: `claude/integration` a4a5735 (0.64.12).
- `git merge` storm-update 0b77dfc: conflict only in `plans/backlog.md` (both sides kept).
- `git merge` fridays 3bd9b2c: conflict only in `plans/backlog.md` (both sides kept); `plans/build-table.md` merged by itself.
  Nothing else conflicted.
- `day_check.py` is storm-update's own (with EV4's 4fa198f skip): identical to 0b77dfc's.
- Switches, as merged (no edit needed; the same as PR9's review-9 "as merged"): `SHORT_FRIDAY = true` (line 9051),
  `EVENTS_ON = true` (line 36580), `EV_STORM_ON = EVENTS_ON` (line 36586).
- `content_gen.py --check`: up to date. `names_check`: OK.
- **sha256 of starship-cadet.html: `23fb9118abc3679fd1eea658a072817fd6f2831a9560f1bf86358ada768cb7df`**

## Results (CADET_CHROME=/opt/pw-browsers/chromium, one at a time)

| Check | Result | Key lines |
|---|---|---|
| perf_check (vs plain a4a5735) | exit 1, 8 "problems", all explained: **no budget broken** | Busiest on the RC: junior common room portrait-wide 433 calls (same as plain), quiz night 396, Friday dinner 361 (was 378), lantern supper (storm) 351 (same). Game code at most 2.16 ms a frame (Friday dinner landscape). Every scene under the 450 budget on every phone view. Flags: Captain's address 120→174 / 155→209 / 117→171 calls and 0.36→1.63 ms; after the address, rec lift lobby 169→204 / 240→274 / 198→232 calls. Plain 0.64.12 has SHORT_FRIDAY off, so it measures an empty auditorium (5 people) against 49 at the address: the feature itself, not a regression, and well under 450. Memory 520→520→522 across round trips: the same on plain 0.64.12 (backlog #14). Week of play flat (520/40/228 → 522/40/228, both builds). File 5.66 MB (was 5.60). |
| arc_check | **OK** | Every arc finished (brennan 5/5 ... pell 8/8, rina 7/7, tomas 7/7, torres-zeke 6/6); calls 68, beats 24; errors []; ARC CHECK OK |
| path_check | **OK** | 7 decks x 3000 searches the same; a played day 3102/3102 real calls the same; 4.3x faster; PATH CHECK OK |
| tiles_check | **FAIL (old, the check's timing, not the game; backlog #26)** | One line: `FAIL phone 390: opening the board adds nothing to the 3D scene`. Rules, balance (full and quick), the game by taps, How to play, the seated game, night odds and news all pass. **Plain a4a5735 fails the same line** (and a second RC run too), so it's not new to the release. No backlog row found for it. |
| disc_check | **OK** | 34 ok lines; the game view draws in 129 calls (under 200); 60/30/20 fps the same game; ALL OK |
| puzzle_check | **OK** | PUZZLE CHECK OK |
| deck_check | **OK** | Draw calls by the lift: D1 156, D2 146, D3 209, D4 176, D5 168, D6 122, D7 169; DECK CHECK OK |

## For the lead

- Nothing new to the release fails in these seven checks.
- tiles_check's "adds nothing to the 3D scene" fails on 0.64.12 too and has no backlog row; suggest one (CR3 didn't add it: brief says results only).
  The line compares the scene's memory counts before and after `tilesPlay` + `step(2)`, so something else in the scene changing
  in those two steps would trip it as well as the board.
- perf_check has no storm scene other than the lantern supper (storm on: 351 calls, same as plain's Saturday dinner).

## Follow-up (lead 25): what makes tiles_check fail

**Not a game bug, and not the board.** tiles_check opens the device, waits 2 steps, counts the 3D scene's geometries,
opens the Tiles board, waits 2 steps and counts again. On a phone, opening the device slides the camera's view down
(section 19's C11 framing, `deviceFrameStep`) over about a second of *real* time, not ship time, so the view is still
sliding during the check's steps. Something already on the deck slides into view, and three.js loads its shape the first
time it draws it, so the count goes up by one or a few. The same happens with no board at all (a control run: 421 → 422 on
the 390 phone, both with and without the board).

- What gets loaded: on 0.64.12 / the release build (390 phone), one deck mesh (432 points) near (-5.5, 0.35, 8.75);
  on 0.64.11 (320 phone), a door's two leaves and its tap box at (-4.5, 6). Not crew, not the board.
- When it started: every integration build from 8a86e18 (the start of the history) to 0.64.10 passes. It starts with
  **patch crew T2, 4dbdca8** ("the opening view another step closer": phone zoom 1.65 → 1.85), merged in 0.64.11
  (376469c); T1 1badd51 (1.65) still passes. 0.64.12's 1.62 moved what sits at the view's edge, so the failure moved
  from the 320 phone to the 390 one.
- Proof: the release build with only the zoom line back at 1.5 / 1.15 passes; the release build and 4dbdca8 unchanged both
  pass when the check waits for the slide to finish (`DEV.fr === 1`) before its first count.
- So the opening zoom only decides which object is at the edge; the cause is the check counting mid-slide. Not fixed (brief).
  Backlog row 26 (on this branch; fridays has a row 25).

## The fix (lead 25's ask): tiles_check waits for the device's framing

`tiles_check.py` `board()`: after `deviceShow('home')`, it waits until `DEV.fr` reaches its target (`DEV.frOn ? 1 : 0`:
1 on a phone, 0 on the wide screen where the device doesn't slide), up to 10 s of real time (100 x 100 ms, a step each),
draws one more frame, and only then takes the "before" count. If the slide never settles it FAILs out loud:
`<view>: the device's framing settles within 10 s (DEV.fr …, frOn …)`. Check only; no game change.

| Build | Result |
|---|---|
| a4a5735 (0.64.12) | ALL OK |
| the release build (sha256 23fb9118…cb7df), run twice | ALL OK, ALL OK |
| 4dbdca8 (patch crew T2, the first that failed) | ALL OK |
| planted: `tilesPlay` adds a mesh to the scene | FAIL "adds nothing to the 3D scene" on 320, 390 and wide |
| planted: `tilesPlay` adds a mesh inside a deck group, in the middle of the view (the scene's child count unchanged) | FAIL on 320, 390 and wide |
| planted: the framing stops at 0.6 | FAIL "the device's framing settles within 10 s (DEV.fr 0.6, frOn True)" on 320 and 390 |

(A first try of the group plant put the mesh 5 m in front of the camera, nearer than the camera's near plane (about 15 m),
and on a phone the slid view's centre line falls just above the screen; the plant, not the check, was wrong. Placed at the
view's middle (`unproject` of (0, 0, 0)) it fails on every view.) Backlog #26 moved to Fixed.
