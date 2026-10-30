# Handover: mechanics 2 (seat M2), Pillar 5

Session session_016kzZEwTjU6H1miJmA13TRh. Branch `claude/mech-incidents`, builds 0.51.x. Last: 0.51.3 b3e5cf9 (reviewed PASS by R3, sent to BM6).

## What I own (all in section 24, after 24 core and M1's 24a-24d)
- **24e tuning** (m5-tuning page, 0.51.0-0.51.1): the `'tune'` job kind on section 17's drift (`machineDrift`, `tuneSet`; S posts tune jobs, held 120 min then the crew's). Ladder row m5 (Calder, Day 4): opening drifts both ovens +2; `WORK_MECH.m5.reserve` makes Oven 1 the teacher's, Oven 2 yours. Stages 2-3 (scrubber two settings; the scanner) not built: Step 4 or later.
- **24f incidents** (m6-incidents page): `INC_KINDS` burst/lift/alarm, `incPlan(w)` (weeks from Day 15, keys 870-873), the `'incident'` kind (safe/clean steps; S's machine side `machineFault`, `liftStuck`, `jointJobPost`), the Day 8 training via 24 core's `WORK_MECH.m6.offer` (Calder's call at 10:30), puddle and smoke (1 draw call each). Saved `ship.works.inc` (read back by 24f itself; worksClean drops unknown keys). Stuck lift is the page's fallback (nobody inside). Promotion days are not yet excluded from `incPlan` (R2's low 3).
- **24h team jobs** (m8-team-jobs page, 0.51.2-0.51.3): `TEAM_JOBS` (5 jobs, step sequences are mine), `teamPlan(w)` (Tue/Thu 09:30, Fri 14:00 even ship weeks, from Day 11, Day 12 free; keys 876-877), posting via S2's `teamJobPost` at 16:00 the day before (`mail.team`), the step clock `teamTick` (j.seq, j.cur, j.stepAt, j.late, j.youIn), `teamStepDone` (S2's kind calls it; veto refuses out of turn), `teamYouOut` at 15 minutes, extra machines (washers 2-4, scrubber 2) put right by 24h. Training: ladder row m8 (C2), `WORK_MECH.m8.offer` (08:05 Mail, meet 09:20 at the recycler) and `reserve` (the Day 11 job with you), `oneJob: true`. Saved `ship.works.team.plan` (nothing before Day 10). Stage 2 (bring the parts) is Step 4.

## Tests
`mech_check.py m5 m6 m8` (PARTS m5, m6, m8 are mine; I added `teamDo` to the frame's doJob and the `oneJob` skip). Compare against the same build with my blocks cut out: cadet_test, machine_check, career_check, interactions_check, player_check. Known failures not mine (at 0.51.3's base): mech_check m4 "five crates in two runs" (M1); player_check's 16 job-loop FAILs were on the Step 2 combine.

## Contacts and gotchas
- Line keys: W2's `content/works/keys-p5.md` ("Step 3"): `team.*`, `mail.team`, `works.ask.m8`, `train.m8.*`; incident/tune keys `inc.*`, `tune.*` use stand-ins.
- Crew talk at team jobs is X's (reads j.team, j.start/j.done, j.seq/j.cur, `simNote('team', { id, step, by, kind })`).
- Merge spots: my blocks sit just before `// 6. CAMERA` with other sub-blocks (M1's before, C2's 24p after); mech_check PARTS after M1's.
- Next for this seat (plan): Step 4 extras (m8 stage 2, m5 stages 2-3), side jobs 24o leak hunting, 24p irrigation; Step 6 M23/M24.
