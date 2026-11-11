# Round 09991b: R4's share (session_01GKuymmDPNyaTSDSCiHCDFj)

Candidate 2: claude/staging-09991 844f3c23, game sha256 b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (0.99.91).
OLD: 0.99.9 main bfbcbdf, game 583d99ba...bd16. Both sha256 checked. Started 03:54 UTC (2026-11-11), two lanes.
perf_check handed over to R6 at ~04:30 UTC (not started here; lead 51's suggestion; R6 started it 04:31).

| Check | Result | Key lines |
|---|---|---|
| day_check 6 | exit 0, 418s | DAY CHECK OK |
| day_check 8 | exit 0, 433s | DAY CHECK OK |
| day_check 23 | exit 0, 422s | DAY CHECK OK |
| day_check 24 | exit 0, 418s | DAY CHECK OK |
| day_check 16 | exit 0, 446s | DAY CHECK OK |
| fresh_walk | exit 0, 341s | errors [] |
| career | exit 0, 245s | CAREER CHECK OK |
| cr1 | exit 0, 16s | CR1 CHECK OK |
| appt | exit 0, 976s | APPT CHECK OK |
| saves | exit 0, 259s | SAVES CHECK OK |
| title | exit 0, 456s | TITLE CHECK OK |
| device | exit 0, 263s | device_check: OK |
| fixtap_probe | exit 0, 54s | FIX TAP PROBE OK |
| fixtap_reach | exit 0, 37s | page errors [] |
| fixtap_click | exit 0, 98s | on errors [] |
| perf_check | handed over to R6 | see R6's notes |

Notes on reading: appt prints only its 4 planted FAIL lines. fixtap_reach: only oj-d3gym-locker 3-gym-1 Treadmills (ixStop)
takes a job. fixtap_click: all 10 cases the same off (off copy, FIXTAP_ON false) and on.

## fresh_walk (BUILD 3)

errors [], **stuck []**, long [], trace d2-booths:said at Day 2 18:16. Day 1 and Day 2 identical to 0.99.9's record
(plans/fw-0999-r4.json on claude/checks-0999-r4) apart from the expected Day 2 18:00 Mail naming Sim night 19:30. Day 3 drill
(expected): 14:54 arrow "Fire drill, 15:00: Chief Calder at the Works bay"; 15:00 "Tap Chief Calder to join the drill", the tap
on Calder, her talk, "Trained: the drill"; 15:01 arrow "On the muster line till the all-clear, 15:15", held (the follower at the
Kit lockers by the line) to 15:15 "All clear. Drill over."; then the lamp job at 15:15. Candidate 1's Food stuck (15:05-16:09)
is gone. The walk ends Day 3 22:05.

## Result

**R4: OK so far** (p926 still running; perf_check by R6).
