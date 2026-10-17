# Cost tracking (the user's ask, 2026-10-17 ~17:18 UTC)

Each session's `usage.cost_usd` from get_session (the platform's own estimate, API-equivalent dollars, not the user's real bill).
Method: snapshot every active session now; snapshot again at each release; the difference (plus any new or archived sessions' totals) is that build's cost.

## Baseline, 17:18 UTC (after 0.60.4, during 0.60.5)

| Session | Role | cost_usd |
|---|---|---|
| session_01KPJMYjXAPkNUcrQ8VRkhLE | Lead (since 04:32) | 172.48 |
| session_01F8ph7FKqViF3heRn94YgBr | Build master 2 (since 04:46) | 90.87 |
| session_01Do3HU5Rh96tgUsPTUbsF8a | Sim engineer 5 (since 11:36) | 38.83 |
| session_01YcSJkhhJ2MnCjsJs7QV8ud | Reviewer 1c (since 08:15) | 33.13 |
| session_01MWyyMaXv6D7yKtDNy9VbCA | Head writer 4 (since 16:29) | 11.18 |
| session_01RvxnkWWPF4SF5ygWT4CvQE | Social & traditions eng (since 16:43) | 10.00 |
| session_01862tURG1qXAVGj2sdUrVCw | Career engineer (since 16:29) | 9.04 |
| session_01S8FWAPFnpaAAUN1wpDQbbo | Perf engineer 3 (since 12:57; ~16:05 reading) | ~8.49 |
| session_01FDy4na3u2FS8L8vEjR6gAR | Pillar 5 designer (since 16:54) | 4.23 |
| session_01SyRmwPxQEVKab6re9UgyrD | Player engineer 5 (since 15:54) | not reported yet |
| session_01AxGXvu4gwTfNVGRKeYbBPw | Reviewer 1d (since 17:11) | ~0 |
| | **Total (reported)** | **~378** |

Archived earlier today (for reference): head writer 3 ended at 108.03.
