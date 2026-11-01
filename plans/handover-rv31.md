# Handover: RV31 (reviewer, 0.99.6)

Session session_01GKuymjTDn3pTeDxiqrxE7F, reports to lead 49 (session_01GKuymjPvM7XFzxM7XqFREd).
Branch claude/review-rv31 (from claude/integration 0.99.5 6475bb30): notes plans/review-rv31.md, probes plans/rv31-probes/.

## State
- PASS FX30 P5-1 (6c14bc2, game 69ac3948...c645) and its follow-up (042f57e, game f535ed24...ace6e; on be3a51f JB2-2, not yet reviewed). No P5-1 notes open.
- JB2-2 (FIXTAP_ON, be3a51f): safe while off, FAIL for switching on (any thing near a small job's stop does the job: toilet,
  washers; 75 stops). FX30 to narrow it; re-review with fixtap_reach.py ON.html and fixtap_click.py OFF.html ON.html.
- PASS PF1 67acc5b (game 90dbc4f2...46a7): F1 same answers (pf_f1_same.py), the four picture switches off (pf_switches.py).
- Next: FX30's narrowed JB2-2, and anything else the lead sends.

## Setup and gotchas
- pip install playwright numpy pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work (npm pack), CADET_CHROME=/opt/pw-browsers/chromium.
- Probes that exec cadet_test.py must run from the repo root (or with cadet_test.py beside them).
- A save/reload probe needs newGameStart first (a bare fresh page's save doesn't load back to the same time).
- check_fast uses the repo's starship-cadet.html: run it in a git worktree of the builder's commit.
- plans/rv31-probes/p5retry_break.py OFF ON: run from the repo root; D expects the one-time reset (042f57e on).
