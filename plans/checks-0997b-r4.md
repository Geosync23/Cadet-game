# 0.99.7 round 0997b (candidate 2): R4 notes

Runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-06. Share: R4 row of plans/round-0997.md (with cr1_check), check
files at c052cc8. Notes on this session's own branch claude/checks-0996-r4. Build master BM26, lead 50.

- Candidate 2: claude/staging-0997 c052cc8, game sha256 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9
  (matches the GO).
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8.
- Two lanes, own CADET_WORK each; fixtap off copy by the usual one-line sed.

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 291s | DAY CHECK OK |
| day_check 8 | PASS | 311s | DAY CHECK OK |
| day_check 23 | PASS | 317s | DAY CHECK OK |
| day_check 24 | PASS | 302s | DAY CHECK OK |
| day_check 16 | PASS | 326s | DAY CHECK OK |
| career_check | **FAIL, NEW** | 190s | 2 FAILs in s5 (below), the same on a second run |
| cr1_check | PASS | 14s | CR1 CHECK OK |
| appt_check | PASS | 788s | APPT CHECK OK (only its usual 4 planted lines): candidate 1's Brennan's-book FAIL is fixed |
| saves_check | PASS | 239s | SAVES CHECK OK |
| title_check | PASS | 383s | TITLE CHECK OK |
| device_check (whole) | PASS | 189s | device_check: OK |
| fixtap_probe (off copy) | PASS | 40s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 31s | only oj-d3gym-locker 3-gym-1 Treadmills (ixStop) takes a job; page errors [] |
| fixtap_click OFF BUILD | PASS | 72s | every case the same off and on; errors [] |

## career_check: NEW FAIL

```
FAIL s5: a steady Senior is "Trusted" by Day 21 (54 reliable)
FAIL s5: a steady Senior is "Trusted" by the end of Day 19 (54 reliable)
```
Twice on candidate 2. On OLD (d7ad4c58): CAREER CHECK OK. On candidate 1 (b14421f8, round 0997): CAREER CHECK OK.
So it came in with candidate 2's game changes: EV1 b374343 (appointments never book over 13:40-14:40) or CR1
2e034d2 / 93eb0e4 (the same-day test without re-asking playerShiftOn). Reported to BM26 and lead 50.

Result: **R4: FAIL: career_check (s5: a steady Senior not "Trusted" by Day 19/21, 54 reliable), NEW.** Everything
else OK.
