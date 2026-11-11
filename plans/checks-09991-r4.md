# Round 09991: R4's share (session_01GKuymmDPNyaTSDSCiHCDFj)

Candidate: claude/staging-09991 4d8869ec, game sha256 475bac8605fe9e26d2cd6035bcbd924dff315bac7eecdd39be12ff287f5b453e (0.99.91).
OLD: 0.99.9 main bfbcbdf, game 583d99ba...bd16. Both sha256 checked. Started 00:06 UTC (2026-11-11), two lanes, then perf alone.

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 418s | DAY CHECK OK |
| day_check 8 | PASS | 436s | DAY CHECK OK |
| day_check 23 | PASS | 439s | DAY CHECK OK |
| day_check 24 | PASS | 419s | DAY CHECK OK |
| day_check 16 | PASS | 452s | DAY CHECK OK |
| career | PASS | 236s | CAREER CHECK OK |
| cr1_check | PASS | 16s | CR1 CHECK OK |
| appt | PASS | 1011s | APPT CHECK OK (only its 4 planted FAIL lines) |
| saves | PASS | 258s | SAVES CHECK OK |
| title_check | PASS | 459s | TITLE CHECK OK |
| device_check (whole) | PASS | 259s | device_check: OK |
| fixtap_probe (off copy) | PASS | 56s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 38s | only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 95s | all 10 cases the same off and on; errors [] |
| fresh_walk BUILD 3 | **FAIL: stuck not empty** | 348s | stuck [[3785, 'Food', 3]]; errors [], long [], trace d2-booths:said Day 2 18:16 |
| p926 | PASS | 679s | P926 CHECK OK |
| perf_check BUILD OLD | queued (alone) | | |

## fresh_walk (NEW vs 0.99.9's record plans/fw-0999-r4.json, which had stuck [])

Day 1 and Day 2 identical to 0.99.9's record. First differences: Day 2 18:00 the Mail now names Sim night 19:30 (expected),
then the Day 3 drill (expected: Calder's talk). Then, Day 3:
- 15:03 Calder's talk, "Trained: the drill"; 15:04 toast "You stand on the muster line with the Works team till the all-clear at 15:15."
- 15:04 the arrow moves on to "Food" (Deck 3, the servery); from 15:05 to 16:09 "tap Trays and cutlery: false" every 3 minutes,
  toast "Servery: Closed. Dinner from 17:00 ... The grab-and-go shelf usuall[y]..."; 15:15 "All clear" while at the servery.
- 16:09 "Food (working)", 16:10 queue, 16:11 Grab and go true; the lamp job resumes 16:17.
In 0.99.9 the drill held the player (extinguisher, hatch, extinguisher back) till 15:15. Sent to BM28 and lead 51 at ~00:50 UTC.
