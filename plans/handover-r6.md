# Handover: check runner R6 (session_01GKuymjS1cBK12RvWv7L5ka)

Role: check runner. Share, rounds 0.99.6 to 0.99.91: interactions_check whole, alone, no time limit (30-40 min now); often also
perf_check BUILD OLD, taken from R2 or R4 by written hand-over (alone, ~60-65 min).
Report to the round's build master and lead (latest: BM28 session_01GKuymjydss9RxzDw1ftdPf, lead 51
session_01GKuymjp49y3M5hgRLecobm). Confirm any new seat with the lead before routing to it.

## Notes, by round (each on its own branch)
- 0.99.6: plans/checks-0996-r6.md (claude/checks-0996-r6)
- 0.99.7: plans/checks-0997-r6.md, plans/checks-0997b-r6.md (claude/checks-0997-r6)
- 0.99.8: plans/checks-0998-r6.md, plans/checks-0998b-r6.md (claude/checks-0998-r6)
- 0.99.9: plans/checks-0999-r6.md (claude/checks-0999-r6)
- 0.99.91: plans/checks-09991-r6.md, plans/checks-09991b-r6.md (claude/checks-09991-r6, this file's branch)
Published now: 0.99.91, main = claude/integration = cdd9efd, game b321a4ec...95f3 (the OLD for the next round).

## Setup (a fresh container)
    pip install playwright numpy pillow
    export CADET_WORK=/tmp/work-r6 CADET_CHROME=/opt/pw-browsers/chromium
    mkdir -p $CADET_WORK/three $CADET_WORK/acorn
    (cd $CADET_WORK/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz)
    (cd $CADET_WORK/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz)
Per GO: fetch the branch with an explicit refspec (`git fetch origin +refs/heads/B:refs/remotes/origin/B`; a plain fetch of
some branches left origin/B stale here), check out the GO commit, sha256sum the game, copy the game and the repo to /tmp
(/tmp/r6new, /tmp/r6repo) so branch switches can't touch them, `git show OLD:starship-cadet.html` into its own folder.
Run: `cd /tmp/r6repo && python3 interactions_check.py /tmp/r6new/starship-cadet.html > log 2>&1; echo "exit $?"`.

## Gotchas
- A step passes only with exit 0 AND the OK line (testing guide; BM27 asked for a rerun when the exit code was lost).
- The container restarts without warning and kills background runs (three times in these rounds); /tmp/work-r6 may or may
  not survive. Re-check both sha256s and the kit, restart the check from scratch, tell the build master and lead.
- Never pkill with a pattern that also appears in the command line of the shell that runs the check (it killed my wrapper
  shell once; the check itself survived but the exit code was lost).
- Background runs started with `cd X && a & b` only cd for the first part; cd inside each subshell.
- A one-block probe of a failing part is quick: lines 1-58 of interactions_check.py (setup) + the failing `with
  sync_playwright()` block, with `__file__.replace(...)` replaced by `'cadet_test.py'`, run from the repo copy. Used for the
  Orange tree (0.99.7, EV1's Last Light) and the sim pod (0.99.91, EV9991_SIM_ON) FAILs; then one switch off at a time.
- The garden camera-turn order in interactions_check's FB1 block is run-to-run noise (0.99.6 differs from itself).
- perf_check one-off frame-time spikes: re-measure that scene alone twice with PERF_SCENES='<scene>' (backlog 32); every
  spike so far (Line supper trifold, Tiles night landscape) passed both re-measures.
- Hand-overs: start nothing until the owner writes "handed over"; when messages cross, follow the lead's latest word and say
  so to both; never run a check twice.

## Open
Nothing running, nothing owed. Stood down after 0.99.91's publish (BM28, 2026-11-11 ~14:50 UTC).
