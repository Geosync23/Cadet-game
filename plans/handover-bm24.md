# Handover: build master BM24 (session_01GKuymnYTNkfxgLvtfFRg7w)

For lead 49 (session_01GKuymjPvM7XFzxM7XqFREd). Predecessors: plans/handover-bm23.md and plans/handover-bm22.md (on
claude/handover-bm23): their tools, steps and gotchas all still hold. Read them first.

## State: 0.99.6 full round green, final GO sent to lead 49
- `claude/staging-0996` tip = the round-record commit (see git log). Game sha256
  f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8, unchanged since the build turn 51efac8.
  Chain from 0.99.5 6475bb30: 10d1704 FX30 merge, e3acaad PF1 merge, c6e9d31 switch-on (P5_RETRY_ON, FIXTAP_ON true),
  lead 49's perf-options-doc fb222b3 merge (the user chose no picture option for now), 51efac8 build turn, then docs.
- All six shares OK (the 0.99.6 row of plans/build-table.md has every result). One check-side flake: backlog BM24-1.
- Next is the lead's: publish, then fast-forward claude/integration and main. Branch claude/bm24-wip can then be deleted.

## Gotchas found this time
- FX30's p5retry_probe.py and fixtap_probe.py look for the `= false;` switch line: on the switched-on build they print
  FAIL "no switch line". Run them on an off copy (sed the line back); they make their own on copy. The round plan says so.
- RV31's probes live on claude/review-rv31 plans/rv31-probes/; copy them into a scratch worktree (not committed to staging).
- gate.sh: create the log folder before starting run1.sh by hand (run1 writes into it).

## Open questions for the user
- F1 sits in section 17 (the systems engineer's): RV31 reviewed it; the owner's own look is still open (owners.md).
