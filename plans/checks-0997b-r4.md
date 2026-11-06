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

## Update: career_check cleared check-side

BM26: M's cause is EV1 b374343 (the steady Senior at 54 by Day 19, Trusted needs 55); EV1's career_check.py fix
2325c5e on claude/staging-0997. Re-run with that file on candidate 2 (game unchanged, 1b17203d...bff9): exit 0,
CAREER CHECK OK, no FAIL lines.

## Checks taken from R2 (agreed with R2, copied to BM26 and lead 50)

| Check | Result | Key lines |
|---|---|---|
| fresh_walk BUILD 3 (RV32) | 4 of 5 points PASS, 1 for BM26/TP1 to judge | (1) Day 1 briefing walked to at 08:20, its scene played 08:50-08:53 to "Ready when you are.", then the clock (no d1-briefing:met flag in the json itself); (2) Works bay arrow before 08:50, then "Clock in at the time clock" 08:53; (3) Day 2 08:45 solo meeting: arrow 08:31, scene 08:45-08:46, "Your first solo job" toast; 18:00 booths: arrow 17:46 "Leila shows you how", Booth 1 used 17:45 and 18:08, calls 18:08 and 18:29, but no Leila line in the record (the player had called home at 12:32); (4) errors []; (5) stuck [], long []. Record: plans/fw-0997b-r4.json |
| p926_check | **FAIL, NEW** | item 15 only: "Brennan at the spice shelf by 18:40 (None)", "she opens, names three jars and says whose (0 lines)", "the mess guesses out loud (0 bubbles)", "joined, your guess card ([])", "the guess card is still open 3 ship minutes later (None)". OLD d7ad4c58: P926 CHECK OK, item 15 all ok (Brennan at the shelf 18:20, 7 lines, 7 bubbles, spice.guess). Likely TB6's note 51 (TRAD997_ON moves the supper after dinner); for TB6 to judge. |
