# Turn reviews: PR8

Second Fridays reviewer, from 2026-10-21 ~14:30 UTC (lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r). Builder: FR3
(session_01935gmiyLoy5fgvs3xQd7QC). PR5 (session_01Eh4drBZjJ82DjYx6XaTt1F) keeps turns 7, 8, 9 and 11b2220.
Pushes only to claude/review-8 (from claude/fridays 0dc4562).

Method (PR3's, as PR5 uses it): build lines untouched; cadet_test off against the base; check_fast alone; the area's
checks on; a code read; a live probe on a real save at 390x844. Checks run one at a time through
`plans/review-8/runner.sh` (resumable, res/<name>.log). Probe: `plans/review-8/p8_fri.py`; shots in
`plans/review-8/shots/` (`git add -f`).

Copies: `t10` = 0dc4562 as pushed (SHORT_FRIDAY on, EVENTS_ON off); `t10off` = the same with SHORT_FRIDAY false;
`t10ev` = on with EVENTS_ON true; `base9` = 11b2220 (the turn-9 tip).

## FR3: turn 10, switch on (0dc4562)

(in progress)
