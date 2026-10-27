# Balance research (BAL1, 2026-10-27)

Research only: nothing here changes the game or a shared check. Build studied: 0.95.0 candidate 3,
claude/staging-p5s6 b5199dc3, game sha256 b18d2b64...238a. Report: https://claude.ai/artifact/R1NgKLKRoP2Gu5sfgmMumm
(answers the user saves on it are in its `answers` store).

- `career_sim.py BUILD DAYS plan...`: the Works career on paper (career_check's own run, read from career_check.py, plus a
  time budget per shift hour and per-day records). Plans: quick, steady, relaxed, half, lazy, slacker (misses Mon+Fri),
  skipper (misses 1 workday in 3). `BANDS3=... TAG=_x` runs a what-if on Tier 3's bands in the page only.
- `needs_sim.py`: the seven needs over 28 days for play styles (a copy of section 15's arithmetic);
  `needs_verify.py BUILD` checks it against the game's needsDrain (identical); `needs_sweep.py` the what-ifs.
- `trads_sim.py BUILD 56` + `trads_stats.py`: the traditions calendar from eventsOn(d).
- `build_report.py`: makes `report/balance-report.html` from `report/template.html` and `data/`.
- `data/`: every run's raw output (career_<plan>.json, needs*.json, trads*.json, machine_check_28.log).
Setup as for the checks (CADET_CHROME, three.js in CADET_WORK); each career run takes about 30 s.
