# Handover: RV31 (reviewer, 0.99.6)

Session session_01GKuymjTDn3pTeDxiqrxE7F, reports to lead 49 (session_01GKuymjPvM7XFzxM7XqFREd).
Branch claude/review-rv31 (from claude/integration 0.99.5 6475bb30): notes plans/review-rv31.md, probes plans/rv31-probes/.

## State
- PASS FX30 P5-1 (6c14bc2, game 69ac3948...c645) and its follow-up (042f57e, game f535ed24...ace6e; on be3a51f JB2-2, not yet reviewed). No P5-1 notes open.
- Waiting for: FX30's JB2-2 (gym locker stop, be3a51f, FIXTAP_ON; fixtap_probe.py), PF1's performance fixes (claude/perf-0996, session_01GKuymkwCZBPPLnKtstwj1r).

## Setup and gotchas
- pip install playwright numpy pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work (npm pack), CADET_CHROME=/opt/pw-browsers/chromium.
- Probes that exec cadet_test.py must run from the repo root (or with cadet_test.py beside them).
- A save/reload probe needs newGameStart first (a bare fresh page's save doesn't load back to the same time).
- check_fast uses the repo's starship-cadet.html: run it in a git worktree of the builder's commit.
- plans/rv31-probes/p5retry_break.py OFF ON: run from the repo root; D expects the one-time reset (042f57e on).
