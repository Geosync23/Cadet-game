# Check runner CR4: results

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
