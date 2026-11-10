# Handover: build master BM27 (session_01GKuymjy5t3QwM8whGj2QFE), 0.99.8 and 0.99.9

For lead 51 (session_01GKuymjp49y3M5hgRLecobm, branch claude/lead-51) and the next build master (BM28). Read
plans/handover-bm26.md and plans/handover-bm25.md first (their tools in plans/build-master/bm25/, bm26/ still hold), then this.

## State
- Nothing of mine is running. Both builds are published; main = claude/integration = bfbcbdf (0.99.9, game
  583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16).
- 0.99.8: claude/staging-0998, FINAL GO 33c737b (game 13681748...59fd3), published as Playtest/Dev v4. Record:
  plans/round-0998.md (round 0998 found P, fixed in candidate 2; round 0998b OK).
- 0.99.9: claude/staging-0999, FINAL GO bfbcbdf (game 583d99ba...bd16), published as Playtest/Dev v5. Record:
  plans/round-0999.md (one find, Q: sound_check timing, check-side, backlog BM27-1).
- Local worktrees (/home/user/wt998, wt999, wtho; /tmp/bm27) are scratch and go with the container.

## Next (lead 51): 0.99.91, plans/patch-09991.md on claude/lead-51
Four pieces, each from main bfbcbdf, each merged only at its reviewer's exact PASS commit: A TP2 claude/p9991-tips
(TP9991_SD_ON, in re-review), B EV2 claude/p9991-flightsim (EV9991_SIM_ON), C TB7 claude/p9991-drills (TB9991_DRILL_ON),
D CR2 claude/p9991-results (CR9991_RESULTS_ON). OLD = 0.99.9 bfbcbdf. Steps: claude/staging-09991 from main bfbcbdf;
merge each PASS as lead 51 names it; all four switches on at the end (only the switch lines); setbuild.py 0.99.91;
DEV_NOTES paragraph + build-table row (+ design-doc if a decision); gates; GO the round (same six shares as
round-0998.md / round-0999.md; R1 and R4 are new sessions lead 51 hires near the GO). FINAL GO to the lead; never publish.

## How I ran it (what worked)
1. A worktree per candidate (`git worktree add /home/user/wtNNN -b claude/staging-NNN origin/main`): gates and R5 run
   on it, never switch branches under a running check.
2. Merge, then check the merged file before anything else: `python3 content_gen.py --check` (up to date), `node
   names_check.js` (OK), `python3 lines_check.py` (PASS, **0 errors**: lines over 90 characters fail it, and it is NOT in
   check_fast, so a fixer's "check_fast OK" doesn't cover it). Clashes so far were only plans/build-table.md and
   DEV_NOTES.md (keep both rows; take the branch's text with "on" wording) and the baked LINES block in the html when two
   commits touch the same .lines bank: resolve the .lines file by hand, then re-bake with content_gen. **If you take a
   branch's whole html with `git checkout --theirs`, re-apply the switch-on lines and the build number** and diff the
   html against your previous commit to see only the expected lines.
3. Switch on with one sed on the switch line; check with grep; commit alone. Then setbuild.py, DEV_NOTES, commit.
4. Gates (two browsers at most): check_fast, then the piece's own checks (player/arrows/events/fresh_walk as fits) and
   cadet_test vs the previous build (plans/build-master/bm25/cad.sh OLD NEW DIR). Lead 51 allowed sending the GO after
   check_fast + player and running the rest as R5's first items, with a stop-the-round promise if one fails.
5. GO message: branch + commit + full sha256 + OLD + "same share as round 0998" + anything new for that share. Record
   every share's final in plans/round-NNN.md as it comes; push the record often (see restarts below).
6. R5 as a **re-runnable script** (plans/build-master/bm27/r5-0999.sh): each check is skipped if its name is already in
   summary.md, so after a container restart you just run it again; to hand a check to a free runner, append
   `| name | handed to R1 |` to summary.md and the script skips it (no double runs).
7. Background runs: always `run_in_background` with `timeout` 7200000 (the default 30 minutes killed R5 once).

## Gotchas this time
- **Containers restart often** (four machines in round 0999, two in 0998b, mine three times). /home/user survived each
  time; /tmp sometimes did, sometimes /tmp/cadet-work was emptied (re-run the setup in plans/testing-guide.md section 2).
  Push the round record after every share's result.
- Messages cross: a fixer may quote an older lead instruction (TP1 in 0998b). Follow the lead's latest; ask if unsure.
- A runner may lose the exit code (R6 in 0999): the rule is exit 0 AND the OK line; ask for a rerun when free.
- sound_check can fail once on a timing line on either build (BM27-1): rerun alone twice, and on OLD, before NEW.
- perf_check: one-off frame-time spikes in the full run (backlog 32); re-measure each alone twice.
- cadet_test "ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)" counts as identical.
- fresh_walk's "long" (an arrow up over 3 ship hours) found P in 0998: keep "long [] needed" in the fresh_walk brief.

## Sessions (round 0999)
R1 session_01GKuymnpcUSBmpZYiDK67GH (lead 51 says a fresh R1 is needed: plans/handover-r1.md), R2
session_01GKuymmnJnzWMxP769P9Edd, R3 session_01GKuymo7sJwyufjkoEsCacB, R4 session_01GKuymmzABL4xHF9xBhM9fE (fresh R4
needed too: plans/handover-r4.md), R6 session_01GKuymjS1cBK12RvWv7L5ka.

## Open for the user (in lead 51's hands)
Backlog BM27-1 (sound_check timing race, check-side), TP1-1 (a shutdown booked into your night shift's clock-in, old),
TP1-4 was built in 0.99.8 (the Needs app's Social line).
