# 0.99.6 full round: R4 notes

Runner R4 (session_01GKuymmvXPrmsnyaH858XoJ), 2026-11-01. Share: R4 in plans/round-0996.md without interactions_check
whole (R6 runs that): career, appt, saves, title_check, device_check (whole), day_check 6, 8, 23, 24, 16, fixtap_probe
(on an off copy), fixtap_reach, fixtap_click.

- Candidate: claude/staging-0996 f3dbd11 (game the same as at the GO commit 5ac6864; BM24 later named b97cb98, docs only
  after 5ac6864), game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches the GO).
- OLD: 0.99.5 claude/integration 6475bb30, sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matches).
- Two lanes side by side, each its own CADET_WORK (/tmp/work-r4: the day checks; /tmp/work-r4b: the rest).
- Off copy for the fixtap probes: `sed 's/^var FIXTAP_ON = true;/var FIXTAP_ON = false;/'` (one line changed).
- Setup gotcha: Python playwright was not installed in this container (`pip install playwright`, 1.64.1, uses the
  preinstalled /opt/pw-browsers/chromium with CADET_CHROME set).

| Check | Result | Time | Key lines |
|---|---|---|---|
| day_check 6 | PASS | 315s | DAY CHECK OK |
| day_check 8 | PASS | 333s | DAY CHECK OK |
| day_check 23 | PASS | 325s | DAY CHECK OK |
| day_check 24 | PASS | 303s | DAY CHECK OK |
| day_check 16 | PASS | 329s | DAY CHECK OK |
| career_check | PASS | 193s | CAREER CHECK OK |
| appt_check | PASS | 805s | APPT CHECK OK |
| saves_check | PASS | 243s | SAVES CHECK OK |
| title_check | PASS | 400s | TITLE CHECK OK |
| device_check (whole) | PASS | 126s | device_check: OK |
| fixtap_probe (off copy) | PASS | 32s | FIX TAP PROBE OK |
| fixtap_reach BUILD | PASS | 23s | 311 rows; exactly one thing takes a job: oj-d3gym-locker 3-gym-1 Treadmills (ixStop); page errors [] |
| fixtap_click OFF BUILD | PASS | 55s | all 10 cases the same off and on (w5-tap, la-lint, jc-kettle, gy-bench, jc-lamp, each with and without the job); errors [] both |

appt_check prints its usual 4 `FAIL planted ...` lines (scope x3, teach-me x1): its own planted-fault runs on a broken
copy, proving it catches them; the check ends OK (same as 0.99.5).

fixtap_reach and fixtap_click print no verdict line of their own; judged against round-0996.md's expectations by
reading their output (the job-taking items listed above; off/on lines compared one by one).

No real FAILs, so no OLD comparison runs were needed. Result: **R4: OK**.
