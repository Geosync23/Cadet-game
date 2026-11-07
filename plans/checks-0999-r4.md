# 0.99.9 round 0999: R4 notes

Runner R4 (session_01GKuymmzABL4xHF9xBhM9fE, fresh; predecessor's note plans/handover-r4.md), 2026-11-07. Build master
BM27, lead 51. Notes on claude/checks-0999-r4.

- Candidate: claude/staging-0999 8d8073a, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16
  (matches the GO), build 0.99.9 = 0.99.8 + EV1's Last Light pale blink (EV999_BLINK_ON). Check files at 8d8073a.
- OLD: 0.99.8, main 33c737b, 13681748...59fd3. No FAILs, so no OLD runs were needed.
- Started ~04:44 UTC in two lanes (/tmp/work-r4, /tmp/work-r4b). The container restarted once (~05:25 UTC) during
  p926; files and logs survived, both sha256s rechecked, p926 rerun from the start.

## R4's own share

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 322s | DAY CHECK OK |
| day_check 8 | PASS | 319s | DAY CHECK OK |
| day_check 23 | PASS | 327s | DAY CHECK OK |
| day_check 24 | PASS | 304s | DAY CHECK OK |
| day_check 16 | PASS | 326s | DAY CHECK OK |
| career_check | PASS | 219s | CAREER CHECK OK |
| cr1_check | PASS | 15s | CR1 CHECK OK |
| appt_check | PASS | 802s | APPT CHECK OK (only its usual 4 planted lines) |
| saves_check | PASS | 246s | SAVES CHECK OK |
| title_check | PASS | 408s | TITLE CHECK OK |
| device_check (whole) | PASS | 212s | device_check: OK |
| fixtap_probe (off copy) | PASS | 44s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 21s | only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 73s | all 10 cases the same off and on; errors [] |

## Taken from R2

| Check | Result | Key lines |
|---|---|---|
| fresh_walk BUILD 3 (FW_TRACE 'd2-booths:said') | PASS, all five points (347s) | briefing 08:20, "Ready when you are." 08:52, clock 08:53; Day 2 08:45 solo arrow and toast 08:46; booths arrow 18:06, never Booth 1 (the one Booth 1 tap is the day's call at 12:32); 'd2-booths:said' 18:16; errors [], stuck [], long []. Every key of the record identical to 0.99.8's plans/fw-0998b-r4.json. Record: plans/fw-0999-r4.json |
| p926_check | PASS (664s) | P926 CHECK OK |

## Extra (BM27 for lead 51): fresh_walk BUILD 4, FW_UNTIL=14:30

PASS (405s). errors [], stuck [], long []. No first-morning card ("You wake ... Bunk 1") anywhere in the walk; between
Day 4 14:00 and 14:20 only the Last Light: 14:00 walk to the bow lounge, 14:01 join tip and toast, joins via a tap on
Sato, **14:08 toast "A pale light blinks past the windows: the Last Light."** (once). So RV34's d6_pair.png card came from
its reload probe, not normal play. Record: plans/fw4-0999-r4.json.

## Taken from R6 (R2's perf_check; R6's container restarted; agreed with R6, BM27 and lead 51 copied)

Running (started 05:37 UTC, alone, BUILD vs OLD); result to follow.
