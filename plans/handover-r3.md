# Handover: R3 (check runner), session_01GKuymo7sJwyufjkoEsCacB

## Role
Check runner for the full rounds. Share R3 (unchanged since 0.99.5): controller_check (every part but reach, in four
groups), sound_check, promo_sight_check, arrows_d_check, arrows_f_check, ending_check, devmode_check (all parts),
dev_arrow_check. Report to the build master and the lead; a NEW FAIL at once.

## Rounds run (notes on each branch)
| Round | Build | Notes | Result |
|---|---|---|---|
| 0996 | 0.99.6 | claude/checks-0996-r3: plans/checks-0996-r3.md | OK (one sound "long" flake under load) |
| 0997 | 0.99.7 c1 | claude/checks-0997-r3: plans/checks-0997-r3.md | 4 NEW FAILs (devmode, arrows_d, controller ending, tiles), all fixed |
| 0997b | 0.99.7 c2 | claude/checks-0997-r3: plans/checks-0997b-r3.md | OK |
| 0998 / 0998b | 0.99.8 | claude/checks-0998-r3: plans/checks-0998-r3.md, checks-0998b-r3.md (+ 3 extra runs for BM27) | OK |
| 0999 | 0.99.9 | claude/checks-0999-r3: plans/checks-0999-r3.md | OK (sound timing race, backlog BM27-1; R2 ran the proof) |
| 09991 | 0.99.91 c1 | claude/checks-09991-r3: plans/checks-09991-r3.md | 1 NEW FAIL (arrows_d drill, TB7, fixed) |
| 09991b | 0.99.91 c2 | claude/checks-09991-r3: plans/checks-09991b-r3.md | OK (one controller tiles one-off, not repeated) |

## Setup (fresh container)
- pip install playwright numpy pillow; three r128 and acorn 8.12.1 by `npm pack` into /tmp/cadet-work/{three,acorn}
  (cdnjs is blocked); CADET_CHROME=/opt/pw-browsers/chromium.
- Two work folders, each with its own test/ and links to three and acorn: /tmp/work-r3 and /tmp/work-r3b.
- Candidate and OLD as git worktrees (`git worktree add -f --detach /tmp/cand <commit>`, same for /tmp/old); check the
  sha256 of starship-cadet.html in both against the GO before anything.
- Scripts kept in plans/r3-scripts/ (copy to /tmp/r3scripts): run.sh (one check, 90 min timeout, a line in
  LOGS/summary.txt) and round2.sh LOGS (sound_check alone first, then lane A controller G3+G2 and lane B devmode,
  dev_arrow, promo_sight, arrows_d, arrows_f, ending, controller G4+G1). About 85 min in all.

## Gotchas
- sound_check alone (backlog BM24-1, BM27-1): its "long", "live" and "hide while resuming" parts are timing-sensitive
  and fail once in a while; run it again alone (and on OLD) before calling it.
- controller_check finds cadet_test.py by its own file name: a check file from another branch must be saved as
  controller_check.py in a copy of the candidate's folder, not under another name.
- Container restarts kill running checks but keep /tmp; re-run the lost ones from the start.
- Killing a lane's bash wrapper lets its current check finish but stops the rest: rebuild the lane with a fresh script.
- One controller tiles line and one devmode "real" line have each failed once and passed on re-run.
- Build masters and leads change often: check a new one on the lead's TEAM.md before routing results.

## Open
Nothing. Idle after 0.99.91 was published (2026-11-11 ~14:49 UTC).
