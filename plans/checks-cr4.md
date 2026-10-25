# Check runner CR4: results

## 0.92.6 full round (2026-10-25; all six switches ON incl. odd jobs)

- **Candidate:** `claude/staging-0.92.6` b78e1e22 (the final candidate; a first run on defc327f was stopped in Day 12 on BM17's word and discarded)
- **starship-cadet.html sha256:** `88f4cc8db099337d1ae61cf05e58be93af6577abea5458ba1449a27733f16fe4` (matches BM17's)
- **OLD:** 39f7741d (0.92.5), sha256 `fddc0ef6...b595559`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, 6, 8, then appt_check (new). One at a time, alone, at b78e1e22, `CADET_WORK=/tmp/work-cr4`. Reported to BM17 and lead 36.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 286 s) | `DAY CHECK OK`; plans the same twice; storm skip as designed; draw calls peak 249 / 450; nobody stuck; 0 arrivals drawn elsewhere |
| day_check 13 | OK (exit 0, 280 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 289 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 264 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 267 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 278 / 450 |
| day_check 8 | OK (exit 0, 271 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 278 / 450 |
| appt_check | OK (exit 0, 617 s) | `APPT CHECK OK`; no FAIL line outside its self-test; last parts: RV17 7a/7b/7c reload and Decline fixes OK, "on paper: no page errors" |

**CR4: OK.** No FAILs. (CR2's arc_check stall with STORIES_ON is outside this share.)

### Extra days for the new traditions (0.92.6 b78e1e22, same sha256)

Asked by BM17 and lead 36 at 16:02 (first finisher); nobody else runs them. All switches on as shipped. One at a time, alone.

| Check | Result | Key lines |
|---|---|---|
| day_check 29 (Tool night) | OK (exit 0, 284 s) | `DAY CHECK OK`; plans the same twice; nobody stuck; 0 arrivals drawn elsewhere; draw calls peak 259 / 450 |
| day_check 42 (Six weeks aboard) | OK (exit 0, 299 s) | `DAY CHECK OK`; plans the same twice; nobody stuck; draw calls peak 270 / 450 (Deck 3) |
| day_check 53 (Open house) | OK (exit 0, 294 s) | `DAY CHECK OK`; plans the same twice; nobody stuck; draw calls peak **350** / 450 on Deck 3 (71 crew): the highest seen in my checks so far (others 247-281), still under budget |

## 0.92.5 full round (2026-10-25)

- **Candidate:** `claude/staging-0.92.5` 53c11f8
- **starship-cadet.html sha256:** `fddc0ef61c68ac012409a0f88e4ded2a62098b28377760461d99fb144b595559` (matches BM17's)
- **OLD:** ba836359 (0.92.4), sha256 `2aa6427f...13a2`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, then 6 and 8 for Crossing the Line (still on; BM17 confirmed at 05:49 nobody else has them). One at a time, alone, with 53c11f8's day_check.py (+7 lines: the new "arriving" check, the user's item 21), `CADET_WORK=/tmp/work-cr4`. Reported to BM17 (took over from BM16), copy lead 35.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 244 s) | `DAY CHECK OK`; plans the same twice; storm skip as designed; draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 237 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 235 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 224 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 222 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 278 / 450 (was 296 on Deck 3 in 0.92.1-0.92.4: lower) |
| day_check 8 | OK (exit 0, 232 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |

New "arriving" line: 564 / 647 / 638 / 677 / 598 / 601 crew came onto a deck on Days 12 / 13 / 16 / 19 / 6 / 8, **0 drawn anywhere else on their first frame** every day. FX8's get-up line: biggest step 0.19 tiles every day (limit 0.35); the rec deck's swimmers/climbers counted apart (FX8-1): 18 / 0 / 99 / 100 / 75 / 76.

**CR4: OK.** No FAILs.

## 0.92.4 full round (2026-10-24)

- **Candidate:** `claude/staging-0.92.4` 5bad724d (build 0.92.4)
- **starship-cadet.html sha256:** `2aa6427fde381f3ddf746900ed9e7a62f51aa27f0bb6460f73c557836fa313a2` (matches BM16's)
- **OLD:** 3866c8f3 (0.92.3), sha256 `f18e8540...07853` (the same file as 0.92.3 round 2); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, 6, 8 with 5bad724d's day_check.py (FX8's get-up line, +10 lines), then CR6's food 1 7, food 11 4, clothes (CR6 handed them over at 18:58, not started there). One at a time, alone, `CADET_WORK=/tmp/work-cr4`. Reported to BM16 and lead 34.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 260 s) | `DAY CHECK OK`; plans the same twice; storm skip as designed; draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 256 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 264 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 252 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 258 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 296 / 450 |
| day_check 8 | OK (exit 0, 257 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |
| food_check 1 7 (from CR6) | OK (exit 0, 58 s) | `FOOD CHECK OK`; no FAIL lines |
| food_check 11 4 (from CR6) | OK (exit 0, 65 s) | `FOOD CHECK OK`; no FAIL lines |
| clothes_check (from CR6) | OK (exit 0, 85 s) | `ALL OK` |

FX8's new line ("getting up from a place: ... the drawn body's biggest move in that step"): 0.06-0.19 tiles on every deck of every day (limit 0.35). The rec deck's "off a place drawn moving (8c), not counted" (swimming lane, climbing wall; backlog FX8-1) was 18 / 0 / 100 / 111 / 76 / 74 on Days 12 / 13 / 16 / 19 / 6 / 8, counted apart as designed; 0 on every other deck.

**CR4: OK.** No FAILs.

## 0.92.3 Round 2 (2026-10-24, new candidate after AC3's item 6 fix)

- **Candidate:** `claude/staging-0.92.3` d9a387b6
- **starship-cadet.html sha256:** `f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853` (matches BM16's)
- **OLD:** 364c80cb (0.92.2); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, 6, 8, then CR6's food 1 7, food 11 4, clothes (CR6 handed them over at 10:37, not started there). One at a time, alone, at d9a387b6 (day_check.py unchanged), `CADET_WORK=/tmp/work-cr4`. Reported to BM16 and lead 33.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 229 s) | `DAY CHECK OK`; plans the same twice; storm skip as designed; draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 226 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 224 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 218 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 204 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 296 / 450 |
| day_check 8 | OK (exit 0, 207 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |
| food_check 1 7 (from CR6) | OK (exit 0, 55 s) | `FOOD CHECK OK`; no FAIL lines |
| food_check 11 4 (from CR6) | OK (exit 0, 59 s) | `FOOD CHECK OK`; no FAIL lines |
| clothes_check (from CR6) | OK (exit 0, 69 s) | `ALL OK` |

**CR4: OK.** No FAILs.

## 0.92.3 full round (2026-10-24)

- **Candidate:** `claude/staging-0.92.3` 0dd4e2e2 (build 0.92.3)
- **starship-cadet.html sha256:** `4e6538447d13e4c5398fc74844748e1e9d41776afa7bcc83bc99d5eff87cd0a2` (matches BM16's and lead 33's TEAM.md)
- **OLD:** 364c80cb (0.92.2); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, 6, 8; one at a time, alone, at 0dd4e2e2 (day_check.py unchanged since ee974894), `CADET_WORK=/tmp/work-cr4`. Reported to BM16 (took over from BM15) and lead 33.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 236 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 213 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 221 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 212 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 208 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 296 / 450 |
| day_check 8 | OK (exit 0, 224 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |

**CR4: OK.** No FAILs. Draw-call peaks identical to 0.92.2.

## 0.92.2 full round (2026-10-24)

- **Candidate:** `claude/integration-next` ee974894 (also claude/staging-0.92.2)
- **starship-cadet.html sha256:** `ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4` (matches BM15's)
- **OLD:** e03505fd (0.92.1), sha256 `2dbb11b8...59b18c`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, 6, 8; one at a time, alone, at ee974894 (day_check.py unchanged since 51a1bb34), `CADET_WORK=/tmp/work-cr4`. Reported to BM15 and lead 32.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 204 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 195 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 197 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 191 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 | OK (exit 0, 185 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 296 / 450 |
| day_check 8 | OK (exit 0, 183 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |

**CR4: OK.** No FAILs. Draw-call peaks identical to 0.92.1.

### Taken over from CR2 (0.92.2 ee974894, same sha256)

BM15's idea at 00:09; CR2 handed both over (off its list, neither started; it kept intro). Run one at a time, alone.

| Check | Result | Key lines |
|---|---|---|
| perf_check vs OLD e03505fd | exit 1 on one problem, **known old (backlog 32)** (1967 s) | `PROBLEM Sunday dinner, the mess 18:30 landscape: js 1.66 -> 3.28 ms a frame`, a single-scene game-time spike. Re-measured that scene alone twice (`PERF_SCENES='^Sunday dinner'`, NEW vs OLD): `PERF CHECK OK` both times; landscape NEW 2.08 / 2.34 ms vs OLD 2.13 / 2.59 ms, so it doesn't repeat: backlog 32's one-sample spike. Nothing else: all 16 scenes' draw calls, triangles and people identical to OLD (the Line ceremony 335c = KP1); deck round trips 521 -> 521 -> 521 (backlog 14 didn't show); week 521 -> 523 in both; file 6.04 MB vs 6.03. |
| lines_check --day | PASS (exit 0, 277 s) | `lines_check --day: PASS (0 errors)` |

## 0.92.1 full round (2026-10-23; Crossing the Line ON)

- **Candidate:** `claude/integration-next` 51a1bb34 (also claude/staging-0.92.1)
- **starship-cadet.html sha256:** `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c` (matches BM15's)
- **OLD:** 685af944 (0.92.0), sha256 `f2329b62...1ebd`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, plus 6 and 8 for the Line (BM15); one at a time, alone, at 51a1bb34 (day_check.py unchanged since 4147f03d), `CADET_WORK=/tmp/work-cr4`. No controller reach this round (lead 31). Reported to BM15 and lead 31.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 271 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 260 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 274 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 281 / 450 |
| day_check 19 | OK (exit 0, 260 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| day_check 6 (the Line's eve) | OK (exit 0, 261 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 296 / 450; nobody stuck |
| day_check 8 (the day after) | OK (exit 0, 267 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450; nobody stuck |

**CR4: OK.** No FAILs.

### Taken over (0.92.1 51a1bb34, same sha256)

On BM15's suggestion (17:12). CR6 handed over food 1 7, food 11 4, clothes (none started; it kept fridays, disc, tiles, join). CR2 handed over lines_check --day and then perf_check (never started; it kept intro; path, arc, lines already OK there). Run one at a time, alone.

| Check | Result | Key lines |
|---|---|---|
| food_check 1 7 | OK (exit 0, 56 s) | `FOOD CHECK OK`; no FAIL lines |
| food_check 11 4 | OK (exit 0, 69 s) | `FOOD CHECK OK`; no FAIL lines |
| clothes_check | OK (exit 0, 89 s) | `ALL OK` |
| perf_check vs OLD 685af944 | **OK** (exit 0, 2195 s) | `PERF CHECK OK`; no problem at all this time: deck round trips 521 -> 521 -> 521 (backlog 14 didn't show), week of play 521 -> 523 in both. The Line ceremony portrait 335c (= KP1's accepted 335, same as OLD); the Line supper 261c. Differences from OLD, all small and explained: Sunday dinner 66 people vs 69 (FX5's Day 0 trickle), junior wing +5k triangles, storm all-clear +2 draw calls (289c vs 287c); every other scene identical. File 6.03 MB vs 6.02. |
| lines_check --day | PASS (exit 0, 377 s) | `lines_check --day: PASS (0 errors)` |

## 0.92.0 full round (2026-10-23)

- **Candidate:** `claude/integration-next` 4147f03d
- **starship-cadet.html sha256:** `c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286` (matches BM14's)
- **OLD:** 989fd566 (0.91.0), sha256 `da9f1d08...aee`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19 plus `controller_check.py starship-cadet.html reach`. Reach in its own `CADET_WORK=/tmp/work-cr4r`, started first; the days alongside it in `/tmp/work-cr4` (two browsers on 4 cores, BM14's OK at 08:33). Reported to BM14 and lead 31.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 515 s, alongside reach) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450; nobody stuck |
| day_check 13 | OK (exit 0, 522 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 524 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |
| day_check 19 | OK (exit 0, 575 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |
| controller_check reach | **NOT FINISHED** (stopped at the 2-hour limit for a background command, 08:32-10:31) | No verdict. It finished the touch sweep (41 states, e.g. the Tiles table) and had started the D-pad half: `#pauseBtn` 1 of 1, `#devBtn` 16 of 16 (`Works` app not on the screen that time), `Tracked` 9 of 9, `Appointments` 4 of 4 highlighted. No FAIL or error line printed before it stopped. Needs a longer-than-2-hour run (see the report to BM14). |

**Reach re-run (BM14's option a):** started detached 10:36 UTC (same file, same CADET_WORK, no CTL_STATES / CTL_PADDONE). By 12:34 it had redone the touch half (41 states) and 5 screens of the D-pad half, all fully highlighted (`#pauseBtn` 1/1, `#devBtn` 16/16, `Tracked` 9/9, `Appointments` 4/4, `Appointments > New appointment` 11/11); no FAIL or error. Too slow to finish soon, so **stopped at 12:35 on lead 31's and CTT4's word**: CTT4 owns the full sweep (on the published game with a fixed check that saves its progress); CTT4 says the 5 screens agree with its own. Reach does not block 0.92.0 (lead 31).

**CR4: days OK; reach handed to CTT4 (no FAIL seen in what ran).**

## 0.91.0 full round (2026-10-22)

- **Candidate:** `claude/integration-next` 989fd566 ("0.91.0: the controller (0.90.9 on 0.64.16, switched off) + fresh-eyes batch 1")
- **starship-cadet.html sha256:** `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee` (matches BM14's)
- **OLD:** b9f053ba (0.64.16); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at 989fd566 (day_check.py unchanged since 1498dbf4), `CADET_WORK=/tmp/work-cr4`. Reported to BM14 and lead 30 (took over from lead 29).

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 206 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 250 / 450 |
| day_check 13 | OK (exit 0, 200 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450 |
| day_check 16 | OK (exit 0, 204 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 194 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs. Peaks identical to 0.64.16 (b9f053ba), as expected with breakfast rolled back.

### Taken over from CR2 (0.91.0 989fd566, same sha256)

Lead 30's idea at 21:42; CR2 handed these over at 21:43 (off its list; it kept intro). Run one at a time, alone on this machine.

| Check | Result | Key lines |
|---|---|---|
| perf_check vs OLD b9f053ba | exit 1, **known old only** (2066 s) | `PROBLEM memory grows across deck round trips` 521 -> 521 -> 523 geometries (textures 40, heap 87 MB): **backlog 14**, and OLD shows exactly the same 521/521/523 in the same run. No other problem: no draw-call or frame-time regression, no backlog 32 spike. Every scene's draw calls identical to OLD (e.g. the Line ceremony portrait 301c, as CR2 expected without breakfast). Week of play 521 -> 523 in both. File 5.87 MB (OLD 5.79), load ~6.2 s in both. |
| lines_check --day | PASS (exit 0, 281 s) | `lines_check --day: PASS (0 errors)` |

**perf_check counts as OK for the round:** its only FAIL is backlog 14, the same way on OLD.

## 0.64.17 full round, second candidate (2026-10-22)

- **Candidate:** `claude/integration-next` 1498dbf4 ("Merge claude/bubble-jump 36f8abf7 ... into the 0.64.17 candidate")
- **starship-cadet.html sha256:** `ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306` (matches lead 29's)
- **OLD:** b9f053ba (0.64.16); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at 1498dbf4 (day_check.py unchanged since 8193458e), `CADET_WORK=/tmp/work-cr4`. Reported to BM14 and lead 29.

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 272 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450 |
| day_check 13 | OK (exit 0, 257 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 268 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |
| day_check 19 | OK (exit 0, 262 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |

**CR4: OK.** No FAILs. Same peaks as the first 0.64.17 candidate (8193458e).

### Taken over from CR6 (0.64.17 1498dbf4, same sha256)

Lead 29 assigned these at 18:13; CR6 confirmed them off its list and not started (it kept fridays, disc, tiles, join). Run one at a time, alone, at 1498dbf4.

| Check | Result | Key lines |
|---|---|---|
| food_check 1 7 | OK (exit 0, 59 s) | `FOOD CHECK OK`; no FAIL lines (backlog 23's `garden, good` did not show: garden good 772 picked, 0 binned, 0 missed) |
| food_check 11 4 | OK (exit 0, 65 s) | `FOOD CHECK OK`; no FAIL lines |
| clothes_check | OK (exit 0, 80 s) | `ALL OK` |

## 0.64.17 full round (2026-10-22; breakfast at 07:00)

- **Candidate:** `claude/integration-next` 8193458e
- **starship-cadet.html sha256:** `225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5` (matches BM13's)
- **OLD:** `claude/integration` b9f053ba (0.64.16), sha256 `70f94273...e6a5c7`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at 8193458e (day_check.py unchanged since b9f053ba), `CADET_WORK=/tmp/work-cr4`
- Reported to BM14 (took over from BM13) and lead 28. The round is held for CR6's m12 FAIL (not in this share).

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 270 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 249 / 450 |
| day_check 13 | OK (exit 0, 251 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 252 / 450 |
| day_check 16 | OK (exit 0, 261 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 279 / 450 |
| day_check 19 | OK (exit 0, 257 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 247 / 450 |

**CR4: OK.** No FAILs. Peaks moved a little from 0.64.16 (breakfast moved), all well under 450.

## 0.64.16 full round (2026-10-22)

- **Candidate:** `claude/integration-next` b9f053ba ("0.64.16: the Zeke patch (ON1's claude/patch-zeke ce2f77bc)")
- **starship-cadet.html sha256:** `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7` (matches BM13's)
- **OLD:** `claude/integration` 2b4a05db (0.64.15), sha256 `0c1f6fb4...8259d2e`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at b9f053ba (day_check.py unchanged since 31c44cb9), `CADET_WORK=/tmp/work-cr4`

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 261 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 250 / 450 |
| day_check 13 | OK (exit 0, 254 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450 |
| day_check 16 | OK (exit 0, 263 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 252 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs. Same peaks as 0.64.15.

### Taken over from CR2 (0.64.16, same commit and sha256)

Agreed with CR2 at 14:23 (lead 28's idea, copied to lead 28 and BM13): CR2 removed these from its run; it kept intro, perf, cadet_test. Run one at a time, alone, at b9f053ba, default arguments.

| Check | Result | Key lines |
|---|---|---|
| path_check | OK (exit 0, 74 s) | `PATH CHECK OK`; every deck 3000/3000 the same; a played day 3165/3165 real calls the same; 4.4x faster |
| arc_check | OK (exit 0, 17 s) | `ARC CHECK OK`; errors []; no theme beat unreachable |
| lines_check | PASS (exit 0, 4 s) | `lines_check: PASS (0 errors, 50 warnings)` (same as 0.64.15 per CR2; warnings never fail) |
| lines_check --day | PASS (exit 0, 365 s) | `lines_check --day: PASS (0 errors)` |

## 0.64.15 full re-run (2026-10-22)

- **Candidate:** `claude/integration-next` 31c44cb9 ("Merge claude/patch-play1-d 836db6c7 ... into claude/integration-next")
- **starship-cadet.html sha256:** `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e` (matches lead 26's)
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868...881e9`; not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19, one at a time, alone, checked out at 31c44cb9 (day_check.py unchanged since c5c43293), `CADET_WORK=/tmp/work-cr4`

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 261 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped, as designed); draw calls peak 250 / 450 |
| day_check 13 | OK (exit 0, 263 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450 |
| day_check 16 | OK (exit 0, 264 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 241 s) | `DAY CHECK OK`; plans the same twice; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs. Same peaks as the c5c43293 round below.

## 0.64.15 full round (2026-10-22)

- **Candidate:** `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ... the Line merged switched off; breakfast (F) not in it")
- **starship-cadet.html sha256:** `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25` (matches lead 26's)
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9` (matches); not needed, no FAIL
- **Share:** day_check Days 12, 13, 16, 19 (testing-guide six-way split), one at a time, alone, `CADET_WORK=/tmp/work-cr4`, Chromium /opt/pw-browsers/chromium

| Check | Result | Key lines |
|---|---|---|
| day_check 12 | OK (exit 0, 263 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (comparison skipped, as designed); draw calls peak 250 / 450; worst stuck 0.0 min |
| day_check 13 | OK (exit 0, 253 s) | `DAY CHECK OK`; plans the same twice; rec deck shut for the storm (skipped); draw calls peak 253 / 450; worst stuck 0.0 min |
| day_check 16 | OK (exit 0, 272 s) | `DAY CHECK OK`; plans the same twice; rec deck traditions rec-dawn-swim, rec-wall-night; draw calls peak 246 / 450 |
| day_check 19 | OK (exit 0, 268 s) | `DAY CHECK OK`; plans the same twice; rec deck mean 7.3 peak 17; draw calls peak 265 / 450 |

**CR4: OK.** No FAILs, so no OLD runs were needed.
