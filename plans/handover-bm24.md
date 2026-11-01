# Handover: build master BM24 (session_01GKuymnYTNkfxgLvtfFRg7w)

For lead 49 (session_01GKuymjPvM7XFzxM7XqFREd). Predecessors: plans/handover-bm23.md and plans/handover-bm22.md (on
claude/handover-bm23): their tools, steps and gotchas all still hold. Read them first.

## State: 0.99.6 candidate gated, waiting for the user's picture choice
- `claude/staging-0996` (from claude/integration 6475bb30, 0.99.5, game 93aed54f...5164):
  - 10d1704 merge FX30 claude/fix-0996 (docs tip 41ad386; game at 6701201 24850dc3...d25f, RV31 PASS)
  - e3acaad merge PF1 claude/perf-0996 (docs tip 86e52f4; game at c5527f4, RV31 PASS). Game 3eba94ac...e3bc.
  - c6e9d31 switch-on: `P5_RETRY_ON` (line ~63164) and `FIXTAP_ON` (line ~17997) true. Game
    3654c0595490935dda9ccdb4448c77c244238523d13e0542e0f3a4de77d6f42f.
  - bf4aab3 plans/round-0996.md; f1ddc31 build-table row "0.99.6 candidate" with every gate result.
- Build lines are still 0.99.5: the build turn comes after the user's picture choice.
- Backup branch claude/bm24-wip = same commits.

## Next steps
1. Lead 49 sends the user's choice on the picture switches (PF1: `PF_NOAA` line ~420, section 1, a URL flag `#pfaa`;
   `PF_PR_ON`, `PF_SH_ON`, `PF_CAP_ON` line ~70676, URL flags `#pfpr` `#pfsh` `#pfcap`; plans/perf-0996.md). Turning one on
   is a small change of that line (for example `URL_FLAGS.has('pfpr')` -> `true`), or a setting if the user wants one:
   a setting is new game code, so a builder and a review first, not the build master.
2. If anything is switched on: its own commit, then gates again (check_fast, cadet vs 0.99.5: every picture will differ;
   look at the PNGs and say how), perf_check alone vs 0.99.5.
3. Build turn: `python3 plans/build-master/setbuild.py starship-cadet.html 0.99.6`, DEV_NOTES paragraph at the top,
   build-table row renamed to 0.99.6; check_fast; push; GO to the runners (plans/round-0996.md), R5 is mine
   (`bash plans/build-master/r5.sh WT LOGDIR`, plus p5retry_break).

## Gotchas found this time
- FX30's p5retry_probe.py and fixtap_probe.py look for the `= false;` switch line: on the switched-on build they print
  FAIL "no switch line". Run them on an off copy (sed the line back); they make their own on copy. The round plan says so.
- RV31's probes live on claude/review-rv31 plans/rv31-probes/; copy them into a scratch worktree (not committed to staging).
- gate.sh: create the log folder before starting run1.sh by hand (run1 writes into it).

## Open questions for the user
- Which picture options (if any) to turn on for 0.99.6 (lead 49 is asking).
- F1 sits in section 17 (the systems engineer's): RV31 reviewed it; the owner's own look is still open (owners.md).
