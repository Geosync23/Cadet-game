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

# Round on 0.64.14 (claude/integration 8e239328), lead 25's full round, CR3's share

Checked out 8e239328 as it is (no merging); its own checks run (tiles_check has the #26 fix).
sha256 of starship-cadet.html **94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9**, the lead's. Build line 0.64.14;
`SHORT_FRIDAY = true`, `EVENTS_ON = true`. One check at a time, CADET_CHROME=/opt/pw-browsers/chromium.

| Check | Result | Key lines |
|---|---|---|
| perf_check vs 0.64.13 (a7477a9) | exit 1, **1 problem: old** | Only "memory grows across deck round trips" 520→520→522, the same on 0.64.13 (backlog #14). Draw calls identical to 0.64.13 in every scene and view (trifold views included); busiest Sunday dinner portrait-wide 418, lantern supper 417, quiz night 396, storm all-clear party 363 (portrait 271): all under 450. Game code at most 2.12 ms. JS heap 228 → 87 MB (both a week of play and round trips). The Line ceremony and supper skip (EV_LINE_ON not in this build). 1824 s (the machine was slow; load 9.8/7.6/7.5 s). |
| arc_check | **OK** | every arc finished (pell 8/8, rina 7/7, tomas 7/7 ...); errors [] |
| path_check | **OK** | 7 decks x 3000 the same; a played day 3102/3102 |
| tiles_check | **OK** | ALL OK (with the #26 fix) |
| disc_check | **OK** | ALL OK; game view 129 calls |
| puzzle_check | **OK** | PUZZLE CHECK OK |
| deck_check | **OK** | lift draw calls D1 156, D2 146, D3 209, D4 176, D5 168, D6 122, D7 169 |
| day_check 19 | **OK** | DAY CHECK OK; draw calls peak 265; worst stuck 3.7 ship min |
| day_check 21 | **OK** | DAY CHECK OK; peak 258; worst stuck 5.2 |
| day_check 27 | **OK** | DAY CHECK OK; peak 258; worst stuck 3.6 |
| day_check 5 (taken from CR1's share, agreed with CR1) | **OK** | DAY CHECK OK; peak 267; worst stuck 0.8 |
| day_check 7 (taken from CR1's share, agreed with CR1) | **OK** | DAY CHECK OK; peak 260; worst stuck 3.7 |

No FAIL outside the known-old list.

# Round on 0.64.15 (claude/integration-next c5c43293), lead 26's full round, CR3's share

Share (plans/testing-guide.md's six-way split): `day_check` Days 0, 1, 5, 7, on the candidate, checked out as it is.
sha256 of starship-cadet.html **e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25**, the lead's
(OLD 32b699a6 = 94f32868…881e9, 0.64.14, also matched). Own CADET_WORK (/tmp/work-cr3), one at a time.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; draw calls peak 252; worst stuck 0.0 ship min; 276 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 250; worst stuck 0.0; 261 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 267; worst stuck 0.0; 267 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 260; worst stuck 0.0; 257 s |

No FAIL.

# Re-run on 0.64.15 (claude/integration-next 31c44cb9), lead 26's full re-run, CR3's share

sha256 **0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e** (the lead's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 252; worst stuck 0.0; 251 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 250; worst stuck 0.0; 235 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 267; worst stuck 0.0; 237 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 260; worst stuck 0.0; 244 s |

No FAIL. (The same numbers as on c5c43293.)

# Round on 0.64.16 (claude/integration-next b9f053ba), BM13's start (lead 27's go; reported to lead 28), CR3's share

sha256 **70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7** (BM13's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 252; worst stuck 0.0; 283 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 250; worst stuck 0.0; 264 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 267; worst stuck 0.0; 268 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 260; worst stuck 0.0; 270 s |

No FAIL.

## cadet_test for CR2 (agreed with CR2, copied to lead 28 and BM13)

`cadet_test.py OLD NEW`: OLD = claude/integration 2b4a05db (0.64.15, sha256 0c1f6fb4…), NEW = b9f053ba (0.64.16, 70f94273…),
run with b9f053ba's cadet_test.py from a scratch folder, strictly alone (no other browser in the container). Exit 0:
**ALL IDENTICAL**: every shot a_start … j_steer2 0 px different; errors A [] B []; taps the same.

# Round on 0.64.17 (claude/integration-next 8193458e, breakfast at 07:00), BM13's start; reported to BM14 and lead 28

sha256 **225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5** (BM13's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 255 (0.64.16: 252); worst stuck 0.0; 280 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247 (250); worst stuck 0.0; 272 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254 (267); worst stuck 0.0; 266 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 269 (260); worst stuck 0.0; 268 s |

No FAIL. (The draw-call peaks moved a few calls with the breakfast change; all far under 450.)

# Round on 0.64.17 (claude/integration-next 1498dbf4), lead 29's start; reported to BM14 and lead 29

sha256 **ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306** (lead 29's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 255; worst stuck 0.0; 224 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 202 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 200 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 269; worst stuck 0.0; 211 s |

No FAIL. (The same numbers as on 8193458e.)

## perf_check for CR2 on 0.64.17 (agreed with CR2; copied to BM14 and lead 29)

`perf_check.py NEW OLD`: NEW = 1498dbf4 (ff45b427…c306), OLD = b9f053ba (0.64.16, 70f94273…a6c7), 1498dbf4's perf_check.
Exit 1, **1 flag, the one CR2 named as the accepted baseline**: `the Line ceremony, bow lounge Sun 14:45 portrait: draw calls 301 -> 335`
(59 → 49 people in the scene; portrait-wide 391 → 411, landscape 282 → 299, not flagged). Everything under 450 on every view
(busiest 418, portrait-wide). No memory flag this time (round trips 521 → 521 → 521; 0.64.16 was 521 → 523, backlog #14).
No js spike (backlog #32). File 5.80 MB.

# Round on 0.91.0 (claude/integration-next 989fd566), BM14's start (lead 29's go; reported to lead 30 and BM14)

sha256 **da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee** (BM14's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 252; worst stuck 0.0; 267 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 250; worst stuck 0.0; 251 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 267; worst stuck 0.0; 249 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 260; worst stuck 0.0 |
| controller_check (all parts but reach) | **run by CR1** (CR1's offer, agreed before it started; my queued copy cancelled, never ran) | CR1: only touch and day FAIL (the known items: touch check-only, day a controller lift/ladder item); the other 25 parts OK. plans/checks-cr1.md on claude/checks-cr1 c7a59cae |

No FAIL in my part. (Day numbers the same as 0.64.16's: breakfast isn't in 0.91.0.)

# Round on 0.92.0 (claude/integration-next 4147f03d), BM14's start; reported to BM14 and lead 31

sha256 **c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286** (BM14's). Checked out as it is; own CADET_WORK.
Share: day_check 0, 1, 5, 7 + the new arrows_d_check and arrows_f_check (BM14's split), each with its default arguments.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 255; worst stuck 0.0; 262 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 260 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 244 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 269; worst stuck 0.0; 263 s |
| arrows_d_check | **OK** | `arrows_d_check: OK` (off; on: S1-S3, pass-over, S7; S5, S8, S6, S9: the pointer on Clock in, Take it, Turn it in, Clock out); 53 s |
| arrows_f_check | **OK** | `arrows_f_check: OK` (off; F4 follow, stops "Close the valve upstream of the wet", "Mop up (1 of 2)/(2 of 2)"; F3 case); 27 s |

No FAIL. (Day peaks as in 0.64.17: breakfast at 07:00 is back.)

## controller_check on 0.92.0, taken from CR6 (BM14's ask; CR6 "handed over" before I started)

a9823284's controller_check.py (the game file there is the same, sha c2180854…1286), every part but reach. 1894 s. Exit 1:
**26 parts OK, only `day` FAILs, with exactly the two known items** (BM14's list, controller-path only):
`FAIL day: the job board: the ring never named the lift` (KC1) and `FAIL day: bedtime: the lift panel never opened` (KC2).
OK: idle save calls touch walk pick games unplug odd off quiet base deck pick1 panels api lists tiles disc screens marks
touch3 drop settings a11y firstuse. (touch passes this round.)

## Re-run on the new 0.92.0 game (claude/integration-next 4e324417, FX5's Day 0 table fix), BM14's ask

sha256 **f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd** (BM14's). Each alone.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 255; worst stuck 0.0; 298 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 291 s |

# Round on 0.92.1 (claude/integration-next 51a1bb34, Crossing the Line on), BM15's start; reported to BM15 and lead 31

sha256 **2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c** (BM15's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 269 (0.92.0: 255); worst stuck 0.0; 297 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 283 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 263 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 270 (269); worst stuck 0.0; 270 s |
| arrows_d_check | **OK** | `arrows_d_check: OK`; 60 s |
| arrows_f_check | **OK** | `arrows_f_check: OK`; 27 s |

No FAIL. (Day 0's peak is 14 calls higher than on 0.92.0, likely FX5's dinner trickle; far under 450.)

## controller_check on 0.92.1, taken from CR6 (BM15's ask; CR6 "hand over" before I started)

51a1bb34's own controller_check.py, every part but reach (lift included). 1977 s. Exit 0: **CONTROLLER CHECK OK**, all 28 parts OK:
idle save calls touch walk pick day games unplug odd off quiet base deck pick1 panels api lists tiles disc screens marks
touch3 drop settings a11y firstuse lift. **day now passes: KC1 and KC2 fixed** (CP5), as BM15 expected.

# Round on 0.92.2 (claude/integration-next ee974894), BM15's start; reported to BM15 and lead 32

sha256 **ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4** (BM15's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 269; worst stuck 0.0; 257 s (FX8's Day 0 evening: no rule broken) |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 246 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 249 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 270; worst stuck 0.0; 248 s |
| arrows_d_check | **OK** | `arrows_d_check: OK`; 54 s |
| arrows_f_check | **OK** | `arrows_f_check: OK`; 25 s |

No FAIL. (Peaks the same as 0.92.1.)

## Taken from CR6 on 0.92.2 (BM15's ask; CR6 "hand over" before each started)

ee974894's own checks, one at a time, game sha ca2f908d…e7e4.

| Check | Result | Key lines |
|---|---|---|
| controller_check (every part but reach) | **OK** | CONTROLLER CHECK OK, exit 0, all 28 parts OK (marks, now deterministic, OK; lift OK); 1886 s |
| food_check 1 7 | **OK** | FOOD CHECK OK; 58 s |
| food_check 11 4 | **OK** | FOOD CHECK OK; 64 s |
| clothes_check | **OK** | ALL OK; 80 s |

# Round on 0.92.3 (claude/staging-0.92.3 0dd4e2e2), BM16's start; reported to BM16 and lead 33

sha256 **4e6538447d13e4c5398fc74844748e1e9d41776afa7bcc83bc99d5eff87cd0a2** (BM16's). Checked out as it is; own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 269; worst stuck 0.0; 285 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 257 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 255 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 270; worst stuck 0.0; 253 s |
| arrows_d_check | **OK** | `arrows_d_check: OK`; 54 s |
| arrows_f_check | **OK** | `arrows_f_check: OK`; 27 s |

No FAIL. (The same numbers as 0.92.2.)

## 0.92.3 Round 2 (claude/staging-0.92.3 d9a387b6, + AC3's clock-in fix), BM16's fresh round

sha256 **f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853** (BM16's). Round 1's controller/food/clothes
runs on 0dd4e2e2 (taken from CR6) were stopped unfinished at BM16's word; no results from them.

| Check | Result | Key lines |
|---|---|---|
| day_check 0 | **OK** | DAY CHECK OK; peak 269; worst stuck 0.0; 262 s |
| day_check 1 | **OK** | DAY CHECK OK; peak 247; worst stuck 0.0; 250 s |
| day_check 5 | **OK** | DAY CHECK OK; peak 254; worst stuck 0.0; 258 s |
| day_check 7 | **OK** | DAY CHECK OK; peak 270; worst stuck 0.0; 261 s |
| arrows_d_check | **OK** | `arrows_d_check: OK`; 59 s |
| arrows_f_check | **OK** | `arrows_f_check: OK`; 28 s |
| controller_check (every part but reach; taken from CR6, agreed) | **OK** | CONTROLLER CHECK OK, exit 0, all 28 parts OK (marks, lift OK); 1957 s |

No FAIL in Round 2.
