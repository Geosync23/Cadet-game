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
| tiles_check | **FAIL (old)** | One line: `FAIL phone 390: opening the board adds nothing to the 3D scene`. Rules, balance (full and quick), the game by taps, How to play, the seated game, night odds and news all pass. **Plain a4a5735 fails the same line** (and a second RC run too), so it's not new to the release. No backlog row found for it. |
| disc_check | **OK** | 34 ok lines; the game view draws in 129 calls (under 200); 60/30/20 fps the same game; ALL OK |
| puzzle_check | **OK** | PUZZLE CHECK OK |
| deck_check | **OK** | Draw calls by the lift: D1 156, D2 146, D3 209, D4 176, D5 168, D6 122, D7 169; DECK CHECK OK |

## For the lead

- Nothing new to the release fails in these seven checks.
- tiles_check's "adds nothing to the 3D scene" fails on 0.64.12 too and has no backlog row; suggest one (CR3 didn't add it: brief says results only).
  The line compares the scene's memory counts before and after `tilesPlay` + `step(2)`, so something else in the scene changing
  in those two steps would trip it as well as the board.
- perf_check has no storm scene other than the lantern supper (storm on: 351 calls, same as plain's Saturday dinner).
