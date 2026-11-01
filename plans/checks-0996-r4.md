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

## Checks taken from other shares (agreed with the owners, copied to lead 49)

Same candidate and sha256. p926_check was offered to R4 by R2 but in the end run by R6 (lead 49's decision); R4 did
not run it.

| Check | From | Result | Time | Key lines |
|---|---|---|---|---|
| arrows_check endstay | R1 | PASS | 823s | ARROWS CHECK OK; said [[34,'go'],[35,'stay']], settled day 35 stay, minutes due 353, missed 0, stuck 0 |
| arrows_pointer_check | R1 | PASS | 192s | arrows_pointer_check: OK |
| perf_check BUILD OLD (alone) | R2 | PASS after re-measure (backlog 32) | 3873s | 2 problems, both one-off frame-time spikes; draw calls, triangles, particles the same as OLD in every scene and layout; memory 470/41/93 -> 472/41/93 a week, round trips flat, same as OLD; load 7.5-7.7 s (OLD 7.4-7.9); 2 skipped (P5_STEP6 not in this build, same as OLD) |

perf_check's two PROBLEM lines, each re-measured alone twice (`PERF_SCENES=... python3 perf_check.py BUILD OLD`):
- "the Line ceremony, bow lounge Sun 14:45 trifold-folded: js 1.23 -> 2.32 ms": re-measures NEW 2.59 (OLD 2.36) and
  1.63 (OLD 1.74); both PERF CHECK OK. Not repeated: noise.
- "Veyli vessel: the parts chain, shuttle bay Sun 13:30 landscape: js 1.35 -> 2.56 ms": re-measures NEW 1.38 (OLD 1.84)
  and 1.49 (OLD 1.52); both PERF CHECK OK. Not repeated: noise.
Both are one-off spikes that do not repeat, the known pattern of backlog 32; no NEW FAIL.
