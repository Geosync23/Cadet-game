# R4's checks: 0.95.0 full round (Pillar 5 Step 6 on)

Runner R4 (session_01GKuymignKdueCaz2pftLEC). Build master BM19, lead 42. 2026-10-27.

- **Candidate 2 (the one that decides):** claude/staging-p5s6 **82b02fb9**, game sha256
  `4a4bed1c6d7b8cb4354d4c4217e970ba2d5b3758a7f0ade48c3c22b159069595` (confirmed). Checks from 82b02fb9.
- OLD = 0.94.0, claude/integration 6f1915cb, game sha256 `5f4c5415814c78eb4c93eaad76ecc35dfa53f1f7cbb4c1f5af541f3971900a0f`.
- Two browsers at a time (BM19's limit), each in its own CADET_WORK (/tmp/work-r4a, /tmp/work-r4b), on 4 cores.

## Candidate 2 (82b02fb9)

| Check | Result | Key lines |
|---|---|---|
| career_check | known old only | `FAIL busy: "Relied on" before Day 5` (backlog 12); worksTabAdd passes (tabs end 'Test', 'Team'); ship.works 3111 B at Day 30, 3297 B at Day 120 (under the 4 KB budget, lead 42) |
| day_check 6 | OK | DAY CHECK OK |
| day_check 8 | OK | DAY CHECK OK |
| day_check 12 | OK | DAY CHECK OK |
| day_check 13 | OK | DAY CHECK OK |
| day_check 16 | OK | DAY CHECK OK |
| day_check 19 | OK | DAY CHECK OK |
| day_check 25 | OK | DAY CHECK OK |
| day_check 26 | OK (run by R1) | DAY CHECK OK; in plans/checks-s6-r1.md |
| day_check 27 | OK (run by R1) | DAY CHECK OK |
| appt_check | OK (run by R1) | |
| saves_check | OK (run by R1) | |
| stories_check | OK (run by R1) | |
| clothes_check | OK (run by R1) | ALL OK |
| food_check 1 7 | OK | FOOD CHECK OK |
| food_check 11 4 | OK | FOOD CHECK OK |
| disc_check | OK | ALL OK |
| tiles_check | OK | ALL OK |
| interactions_check | handed to R1 (AS1) | My run was cut at 90 min by my own lane script's time limit (288 lines, 0 FAIL, at "real taps by the exercise bikes"): not a result. AS1 runs it whole, alone. |
| join_check | OK (run by BM19, alone) | My two runs beside another browser: every test passes up to "Sunday table's long tables", then join_check.py line 153 (the save part, a real reload without `?nosave`): `Page.goto: Timeout 30000ms exceeded`. BM19: OLD and candidate 2 both time out there with two browsers at once, and both give JOIN CHECK OK alone. Load, not the build. |

### The join_check crash

Run 1 ran beside interactions_check (load average about 8.7); run 2 beside disc_check only, no leftover browsers. Same
line both times. The page loaded fine with `?nosave` earlier in the check; the hang is the first load that reads the
check's own save (Day 7, after the Sunday table and deck changes). Settled by BM19: the same timeout on OLD with two
browsers at once, and JOIN CHECK OK on both builds alone. Run join_check alone.

## Round 1 (e0084ca9, game d1666007...f278), stopped early for candidate 2

career_check FAILED with backlog 12 plus three: worksTabAdd (the Team tab sorts after the check's test tab: a stale
check) and ship.works over the 3 KB budget (3111 B at Day 30, 3297 B at Day 120). BM19 and lead 42 fixed the check
only (c971f124: 4 KB budget, tab order); candidate 2 passes both. Days 6, 8, 12, 13, 16, 19, 25: DAY CHECK OK.
interactions ran 85 min with 0 FAIL before I stopped round 1 (BM19's call). The rest was not run on e0084ca9.

## Lessons

- join_check also times out on its real reload with a second browser beside it (both builds): run it alone.
- interactions_check with a second browser beside it takes more than 90 minutes on 4 cores: give it no time limit
  per check, or run it alone.
