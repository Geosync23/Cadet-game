# Handover: build master BM26 (session_01GKuymkyzjd6auLTCEZK5CN), 0.99.7's round

For lead 50 (session_01GKuymmoEriV3ugms2s3hsn, branch claude/lead-50) and the next build master (BM27). Read
plans/handover-bm25.md first (its tools in plans/build-master/bm25/ still hold), then this.

## State
- 0.99.7 is done and gated, NOT published (the user: fold it into a small 0.99.8). claude/staging-0997 at 1baafc1 = the
  FINAL GO (game sha256 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9, build 0.99.7); later commits
  (3d5a8f4, this note) are docs only. Round record, every find A-O with cause and fix, every share's result:
  plans/round-0997.md, "Round record". DEV_NOTES' 0.99.7 paragraph and the build-table row "0.99.7 candidate 2" updated.
- Nothing of mine is running. A local scratch branch bm26-cand2 and worktrees under /tmp/bm24 only (not pushed; lost
  with the container, nothing needed).

## Next (lead 50's plan, plans/patch-0998.md on claude/lead-50)
0.99.8 = 0.99.7 + TP1 913ba6c (TP998_ARROW_ON, TP998_BOOTH_ON), after SC1's PASS:
1. claude/staging-0998 from staging-0997 **1baafc1**.
2. Merge 913ba6c. **Staging's content/banks/tp997.lines must win** (CL1's K shortenings, 4bd36a1 + c72cff9; TP1's
   branch has the long lines). After the merge: `python3 content_gen.py --check` must say "up to date"; if not, re-bake
   (content_gen) and check `lines_check.py` PASS (0 errors) and `node names_check.js` OK.
3. Switch both on (only the two switch lines change), build turn 0.99.8 (setbuild.py; the HUD, DEV_NOTES row,
   design-doc: one call home a day, a second booth use gives nothing).
4. Gates: check_fast, player, arrows default + week, cadet vs 0.99.7's 1b17203d (only the arrow/booth differences).
5. GO round 0998 to R1-R4, R6 (same six shares as round-0997.md; check files at the GO commit).

## Gotchas found this round
- **Run on the merged candidate, not on each fixer's branch.** Fixers ran checks on their own branches with stale copies
  of other seats' check files (EV1's events/machine "FAILs"); always use staging's check files.
- **A fixer's "OK" isn't on the mix.** devmode_check failed on the CR1+EV1 merge though each was fine alone; and CR1
  changed its fix twice (2e034d2, then 93eb0e4). Gate the exact merged file before every GO.
- **Kill whole chains.** `pkill -f` on one run lets a waiting script start the next (twice a stray check_fast or
  ev1only run started). Check `pgrep -c chrome` is 0 before new gates; two browsers at most.
- **Don't switch branches in the repo while a check runs on its working tree**: use `git worktree add` for every gate
  (plans/build-master/bm26/r5.sh does this for R5).
- Someone else may push docs to staging (BM25 did after handing over): fetch and rebase before pushing.
- p926_check, career_check s5, disc_check #25 and weekend_check now read the calendar's own times; the 0.99.7 calendar
  moved several things (Spice supper 19:15, Lightdisc's Day 2 pair 21:30, Saturday run parked, the first Saturday's
  garden hour out). A FAIL at a fixed time is usually the check, but prove it (OLD run + a switch-off bisect).
- interactions_check's garden camera turns vary run to run even on 0.99.6 (noise, R6).
- fresh_walk's record doesn't log bubbles or intro flags: a "scene missing" there needs a trace (SC1 did it for O).

## Tools (plans/build-master/bm26/)
- r5.sh: R5's share on a worktree of a given commit (edit the commit and paths), two lanes, then cadet alone.
- crew_probe.py BUILD...: crew on a deck at a given time (edit the skipTo) — used to place perf's garden 33 -> 29.
- BM25's switchon.py (--off PIECE) makes one-piece-off copies for bisects; keepboth2.py resolves table clashes.

## Open for the user (in lead 50's hands)
M: a steady Senior can be a point short of Trusted on Day 19 (career_check loosened by 5 xp); F: Lightdisc's Day 2
pair at 21:30; L: the Saturday run parked; backlog TP1-1 (a shutdown booked into your night shift's clock-in, old).
