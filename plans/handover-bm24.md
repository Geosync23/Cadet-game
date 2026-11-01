# Handover: build master BM24 (session_01GKuymnYTNkfxgLvtfFRg7w)

For lead 49 (session_01GKuymjPvM7XFzxM7XqFREd). Predecessors: plans/handover-bm23.md and plans/handover-bm22.md (on
claude/handover-bm23): their tools, steps and gotchas all still hold. Read them first.

## State: 0.99.6 built, GO sent; full round running
- `claude/staging-0996` tip 5ac6864 (the GO commit). Game sha256
  f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8. Chain from 0.99.5 6475bb30: 10d1704 FX30 merge,
  e3acaad PF1 merge, c6e9d31 switch-on (P5_RETRY_ON, FIXTAP_ON true), bf4aab3 round plan, f1ddc31 + 1f5908d docs,
  merge of lead 49's claude/perf-options-doc fb222b3 (docs: the user chose no picture option for now), 51efac8 build turn,
  5ac6864 GO commit. Every gate is in the 0.99.6 row of plans/build-table.md.
- Round: plans/round-0996.md, six shares (R6 = interactions_check whole). I run R5:
  `bash plans/build-master/r5.sh WT LOGDIR` plus p5retry_break (off copy vs build; see the plan).
- After all six shares are OK: round record (build-table row, DEV_NOTES "full round green, waiting for the user's OK to
  publish", backlog rows), push, final GO to lead 49.

## Gotchas found this time
- FX30's p5retry_probe.py and fixtap_probe.py look for the `= false;` switch line: on the switched-on build they print
  FAIL "no switch line". Run them on an off copy (sed the line back); they make their own on copy. The round plan says so.
- RV31's probes live on claude/review-rv31 plans/rv31-probes/; copy them into a scratch worktree (not committed to staging).
- gate.sh: create the log folder before starting run1.sh by hand (run1 writes into it).

## Open questions for the user
- F1 sits in section 17 (the systems engineer's): RV31 reviewed it; the owner's own look is still open (owners.md).
