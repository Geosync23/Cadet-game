# 0.99.3 full round: R4 notes

Runner R4, 2026-10-30. Same share as 0.99.0 (plans/round-0990.md R4): interactions_check (whole, alone, no time
limit), career, appt, saves, title_check, day_check 6, 8. Changes in this build: mess hall sound; the Day 0 dinner's
Chief on the cards; the call-home card after you eat; the original title song back.

- Candidate: claude/staging-0993 df74ce0fbf33f40bb2cee71369ef589871a1eb94,
  game sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matches BM21's).
- OLD: 0.99.2 claude/integration d180a704, sha256 27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matches).
- Two browsers at most, each its own CADET_WORK; interactions_check ran alone after the rest finished.

| Check | Result | Time | Key lines |
|---|---|---|---|
| career_check | PASS | 219 s | CAREER CHECK OK |
| appt_check | PASS | 862 s | APPT CHECK OK (its usual 4 `FAIL planted` lines are its own planted-fault runs) |
| saves_check | PASS | 269 s | SAVES CHECK OK |
| title_check | PASS | 305 s | TITLE CHECK OK |
| day_check 6 | PASS | 352 s | DAY CHECK OK |
| day_check 8 | PASS | 369 s | DAY CHECK OK |
| interactions_check (whole, alone) | PASS | 2052 s | INTERACTIONS CHECK OK |

No real FAILs, so no OLD runs needed. Result: **R4: OK**.

## perf_check NEW OLD (for R2)

Taken from R2 (agreed with R2, lead 46 and BM21 copied; R2's own copy skipped). Run alone after the share (4251 s):
`perf_check.py NEW OLD`, from a scratch folder.

- Full run: `PERF CHECK: 2 problem(s) (2 skipped: switch not in this build; 0 waiting: not built yet)`, exit 1.
- The two PROBLEMs (frame time only):
  - `Sowing / harvest morning, garden 10:00 landscape: js 1.51 -> 2.85 ms a frame`
  - `Captain's address, auditorium Fri 16:10 trifold-folded: js 1.65 -> 3.03 ms a frame`
- Re-measured both scenes alone twice (`PERF_SCENES='Sowing|Captain.s address'`): both runs `PERF CHECK OK`, exit 0.
  NEW/OLD ms a frame (perf_check prints OLD's block first):

  | Scene, view | full run | re 1 | re 2 |
  |---|---|---|---|
  | Sowing morning, landscape | 2.85 / 1.51 | 1.35 / 1.42 | 1.63 / 1.40 |
  | Captain's address, trifold-folded | 3.03 / 1.65 | 1.34 / 2.46 | 1.66 / 2.20 |

  Neither repeated (the backlog 32 pattern): **noise, not counted**.
- Memory: a week of play 470/41/93 -> 471/41/93; deck round trips 470/41/93 x3 (flat on NEW and OLD).
- Draw calls: the same on NEW and OLD in these scenes (161c landscape, 103c trifold-folded).

perf_check result: **OK** (after the re-measure).
