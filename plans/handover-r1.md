# Handover: check runner R1 (session_01GKuymkdg7HjAaXfh3NRnBG; before it session_01GKuymnpcUSBmpZYiDK67GH)

Role: check runner R1 in the full rounds (plans/testing-guide.md "How a runner runs its share"). Reports to the lead
and the build master named in each GO. Rounds run: 0.99.6, 0.99.7 (two candidates), 0.99.8 (two), 0.99.9; notes in
plans/checks-<round>-r1.md on claude/checks-0996-r1, -0997-r1, -0998-r1, -0999-r1. 0.99.9 published 2026-11-08.

Setup (a fresh container): pip install playwright numpy pillow; three r128 and acorn via `npm pack` into
/tmp/cadet-work/three and /tmp/cadet-work/acorn (cdnjs is blocked); two CADET_WORKs (/tmp/work-r1, /tmp/work-r1-b) each
with symlinks three -> /tmp/cadet-work/three, acorn -> /tmp/cadet-work/acorn, and a test/ folder;
CADET_CHROME=/opt/pw-browsers/chromium. Check out OLD and the candidate as detached worktrees (git worktree add --detach).

The R1 share (round-0997.md's table): lane A arrows_check default parts (week is inside), step5, step6 asis teachoff
track skiptea (one run is fine since TP1 042949a), endstay; lane B p5retry_probe on an off copy (sed P5_RETRY_ON false),
bubble, puzzle, social, talk, arrows_pointer, day_check 4 11 25 26 2 9; player_check alone at the end. About 75 min
(90+ on a slow container). Two browsers at most.

Gotchas:
- `step6 teachoff` alone is not the same as the four ways in one run (H, 0.99.7): give the exact command when asked.
- Never rerun a check another runner holds; agree hand-overs first, copy the lead and build master.
- When moving a running check between browsers, stopping its driver script loses only the exit code: read the log.
- A new build master or lead: confirm it in the lead's TEAM.md before taking work from it.
- Extra R5 checks seen: food 1 7 / 11 4, join, weekend, day 3 12 13 17 18 19 27, p5retry_break (probe from
  origin/claude/review-rv31; OFF copy with FIXTAP_ON and P5_RETRY_ON false, 2 lines).
Open questions for the user: none.

## Round 09991 (0.99.91), this session
- Branch claude/checks-09991-r1. Candidate 1 (4d8869ec, game 475bac86...b453e): one NEW FAIL, arrows_check week Day 3
  "m3d" not learned (piece C, the drill arrow pointed at the spot, not Calder); proofs: OLD OK, drill-switch-off copy OK.
  Notes plans/checks-09991-r1.md. Candidate 2 (844f3c23, game b321a4ec...95f3): all 17 OK, notes plans/checks-09991b-r1.md.
  BM28 sent the FINAL GO (claude/staging-09991 cdd9efd) 2026-11-11 ~05:43.
- Setup gotcha: npm pack tarballs must be extracted WITHOUT --strip-components (checks read three/package/build/three.min.js).
- Run scripts were /tmp/r1/laneA.sh, laneB.sh, player.sh (lost with the container): lane A arrows default, step5,
  step6 asis teachoff track skiptea, endstay; lane B p5retry_probe (off copy: sed 's/^var P5_RETRY_ON = true;/var P5_RETRY_ON = false;/'),
  bubble, puzzle, social, talk, arrows_pointer, day 4 11 25 26 2 9; player alone after both. About 75 min.
- When reusing a script for a new candidate, check every path (a `cd` without a trailing slash slipped past a sed once).
- The promo part's "stuck from Day 12 18:20 at A toilet" note is on OLD too: not a FAIL.
