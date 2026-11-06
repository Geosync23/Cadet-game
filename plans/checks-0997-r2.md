# 0.99.7 full round: share R2 (2026-11-06)

- Candidate (NEW): waiting for BM25's GO.
- OLD: 0.99.6, main = claude/integration d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matched); names_check on OLD OK.
- Setup: playwright (pip) with CADET_CHROME=/opt/pw-browsers/chromium; three.js r128 and acorn 8.12.1 (npm pack) in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b); numpy, pillow; two browsers at most.
- Share: as plans/round-0997.md names for R2 (not written yet).

## Result: waiting for the GO

## fresh_walk: how it is judged (BM25, 2026-11-06)
Run: `python3 plans/rv32-probes/fresh_walk.py BUILD 3 $CADET_WORK/fw.json` (Days 0-3, sleep 22:30). It prints no OK line; pass when all five hold:
1. Day 1: the briefing meets (d1-briefing:met) and the Chief stays until it ends.
2. The Day 1 arrow leads to the Works bay before 08:50, then to the clock.
3. Day 2's 08:45 solo meeting and the 18:00 booths each get an arrow and happen.
4. No page errors.
5. The follower is never stuck for an hour.
