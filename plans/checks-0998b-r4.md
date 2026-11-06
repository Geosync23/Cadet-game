# 0.99.8 round 0998b (candidate 2, P fixed): R4 notes

Runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-06. Check files at bbb7bb0. Notes on this session's own branch
claude/checks-0996-r4. Build master BM27, lead 50.

- Candidate 2: claude/staging-0998 bbb7bb0, game sha256 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3
  (matches the GO). Change vs candidate 1: only P's fix (TP1 cc44f94 + 91a75b4).
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8. No FAILs, so no OLD runs were needed.

## R4's own share

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 294s | DAY CHECK OK |
| day_check 8 | PASS | 304s | DAY CHECK OK |
| day_check 23 | PASS | 297s | DAY CHECK OK |
| day_check 24 | PASS | 286s | DAY CHECK OK |
| day_check 16 | PASS | 305s | DAY CHECK OK |
| career_check | PASS | 191s | CAREER CHECK OK |
| cr1_check | PASS | 14s | CR1 CHECK OK |
| appt_check | PASS | 765s | APPT CHECK OK (only its usual 4 planted lines) |
| saves_check | PASS | 227s | SAVES CHECK OK |
| title_check | PASS | 392s | TITLE CHECK OK |
| device_check (whole) | PASS | 218s | device_check: OK |
| fixtap_probe (off copy) | PASS | 45s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 30s | only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 73s | every case the same off and on; errors [] |

## Taken from R2 (agreed with R2)

| Check | Result | Key lines |
|---|---|---|
| fresh_walk BUILD 3 (FW_TRACE 'd2-booths:said') | PASS, all five points | briefing 08:20/08:52 then the clock 08:53; Day 2 08:45 solo meeting; Day 2 booths arrow from 18:00 to the floor pin, never Booth 1; 'd2-booths:said' at 18:16; errors []; stuck [], long [] (P fixed: 2 Booth 1 taps in the whole walk; 21:38 toast "Really missing people. Find some company: the mess or the bow lounge."). Record: plans/fw-0998b-r4.json |
| p926_check | PASS | P926 CHECK OK |

## Taken from R5 (BM27 asked, lead 50's call; removed from BM27's script)

| Check | Result | Time | Key lines |
|---|---|---|---|
| tiles_check | PASS | 139s | ALL OK |
| join_check | PASS | 379s | JOIN CHECK OK |
| weekend_check | PASS | 583s | WEEKEND CHECK OK |
| day_check 27 | PASS | 294s | DAY CHECK OK |
| day_check 18 | PASS | 226s | DAY CHECK OK |
| day_check 19 | PASS | 173s | DAY CHECK OK |

Result: **R4: OK** (own share, R2's fresh_walk and p926, R5's six; no FAIL lines anywhere).
