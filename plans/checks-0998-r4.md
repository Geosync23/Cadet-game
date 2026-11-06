# 0.99.8 round 0998: R4 notes

Runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-06. Share: R4 row (round-0997.md + "Round 0997b"), check
files at d7f5bd6. Notes on this session's own branch claude/checks-0996-r4. Build master BM27, lead 50.

- Candidate: claude/staging-0998 d7f5bd6, game sha256 298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462
  (matches the GO). 0.99.8 = 0.99.7 (1b17203d) + TP1 913ba6c (TP998_ARROW_ON, TP998_BOOTH_ON).
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8.

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 289s | DAY CHECK OK |
| day_check 8 | PASS | 307s | DAY CHECK OK |
| day_check 23 | PASS | 299s | DAY CHECK OK |
| day_check 24 | PASS | 289s | DAY CHECK OK |
| day_check 16 | PASS | 301s | DAY CHECK OK |
| career_check | PASS | 193s | CAREER CHECK OK |
| cr1_check | PASS | 14s | CR1 CHECK OK |
| appt_check | PASS | 779s | APPT CHECK OK (only its usual 4 planted lines) |
| saves_check | PASS | 231s | SAVES CHECK OK |
| title_check | PASS | 349s | TITLE CHECK OK |
| device_check (whole) | PASS | 212s | device_check: OK |
| fixtap_probe (off copy) | PASS | 49s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 33s | 311 rows; only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 67s | every case the same off and on; errors [] |

R4's own share: **OK**.

## Taken from R2 (agreed with R2, copied to BM27 and lead 50)

| Check | Result | Key lines |
|---|---|---|
| p926_check | PASS | P926 CHECK OK; item 15: Brennan at the spice shelf 19:20, 7 lines, 7 bubbles, guess card held 3 min |
| fresh_walk BUILD 3 (with FW_TRACE on 'd2-booths:said') | **FAIL (point 5), NEW** | Points 1-4 pass: Day 1 briefing walked to 08:20, played to "Ready when you are.", then the clock 08:53; Day 2 08:45 solo meeting; Day 2 booths arrow from 18:00 to the floor pin, never Booth 1 (TP998_ARROW_ON); 'd2-booths:said' at 18:16; errors []. Point 5: stuck [] but long = [[2738, 'The call booths'], [3929, 'The call booths, Deck 3']] (an arrow up over 3 ship hours; 0997b had long []). |

### fresh_walk point 5: NEW (P)

After the day's one call home (Day 2 12:32; Day 3 06:00), the Social need's "Missing people" toast ("...or call home
from the booths on Deck 3. Follow the marker.", Day 2 21:38, Day 3 17:29) points at the booths, which under
TP998_BOOTH_ON now give nothing. The walker taps Booth 1 every 3 minutes, Day 2 21:38-22:30 and Day 3 17:29-22:30
(about 5 hours); the need is never met; Day 3 also "Every booth is busy, so you join the line" (18:27, 18:30, 18:54).
BM27 confirmed it in the code: NEED_FIX.social = ['callhome'] only, so the marker loops. Reported to BM27, lead 50,
TP1 as a NEW game FAIL. Record: plans/fw-0998-r4.json.

Result: **R4: OK** for its own share; **FAIL: fresh_walk (from R2): the Social marker loops on the booths after the
day's call (TP998_BOOTH_ON), NEW**; p926 OK.
