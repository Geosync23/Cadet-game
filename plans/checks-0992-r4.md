# 0.99.2 full round: R4 notes

Runner R4, 2026-10-29. Same share as 0.99.0 (plans/round-0990.md R4): interactions_check (whole, alone, no time
limit), career, appt, saves, title_check, day_check 6, 8. Plus perf_check NEW OLD taken from R2 (agreed with R2,
lead 46 and BM21 copied; R2's own copy skipped).

- Candidate: claude/staging-0992 60d477e8619a373f8d7e6b27a59236f64d5d2427,
  game sha256 27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matches BM21's).
- OLD: 0.99.1 claude/integration bc4579aa, sha256 8e4ac5459ca78df284390d9438c09b7118ce5448d4c0093dbf9b894bf19e2d9d (matches).
- Two browsers at most, each its own CADET_WORK; interactions_check ran alone after the rest; perf_check alone after it.

| Check | Result | Time | Key lines |
|---|---|---|---|
| career_check | PASS | 238 s | CAREER CHECK OK |
| appt_check | PASS | 940 s | APPT CHECK OK (its usual 4 `FAIL planted` lines are its own planted-fault runs) |
| saves_check | PASS | 266 s | SAVES CHECK OK |
| title_check | PASS | 308 s | TITLE CHECK OK; new steps pass: `no save, New game: the old deck never shows before the manifest (0 frames)`, `Start over: ... (0 frames)`, `Arrive by shuttle: the manifest, and the old deck never shows (0 frames)`, `Skip to Monday morning: the terminal goes onto Monday 06:00` |
| day_check 6 | PASS | 433 s | DAY CHECK OK |
| day_check 8 | PASS | 425 s | DAY CHECK OK |
| interactions_check (whole, alone) | PASS | 2343 s | INTERACTIONS CHECK OK |

No real FAILs in the share, so no OLD runs needed. Share result: **R4: OK**.

## perf_check NEW OLD (for R2)

Run alone after the share (4254 s): `perf_check.py NEW OLD`, from a scratch folder.

- Full run: `PERF CHECK: 1 problem(s) (2 skipped: switch not in this build; 0 waiting: not built yet)`, exit 1.
- The one PROBLEM: `the Line supper, the mess Sun 18:30 portrait-wide: js 2.11 -> 3.14 ms a frame` (frame time only).
- Re-measured that scene alone twice (`PERF_SCENES='Line supper'`): both `PERF CHECK OK`, exit 0; portrait-wide
  NEW/OLD 2.1/2.56 ms (re 1) and 2.83/2.35 ms (re 2) (corrected in 0.99.3: perf_check prints OLD first; first sent the wrong way round). Not repeated, so a one-off spike (backlog 32 pattern): **noise, not counted**.
- Memory: a week of play 470/41/93 -> 471/41/93; deck round trips 470/41/93 -> 470/41/93 -> 470/41/93 (flat on NEW
  and OLD; backlog 14's +2 geometries does not show).
- Draw calls: every scene the same on NEW and OLD.

perf_check result: **OK** (after the re-measure).
