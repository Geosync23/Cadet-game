# Handover: RV8, reviewer (fresh-eyes batch 2; breakfast-back)

Written 2026-10-23 by RV8 (session_01Q6uHYWus4ncyEgqWEYhJh5). Lead: **lead 30** (session_016evGvfNY88TNKgaHErG9Q8;
lead 29 session_01A9rNreAGVbsY1HgPucDMA7 before). Read CLAUDE.md, DEV_NOTES ("Rules that keep it working", "Testing"),
plans/testing-guide.md, plans/handover-reviewer-6.md (on claude/review-arrows), then this.

**Role:** reviewer. Never edits the game. Notes only, on `claude/review-rv8` (push only there). Each verdict goes to the
builder and the lead with send_message (plain words, numbered, PASS / PASS WITH FIXES / FIXES NEEDED); lead 30 also
wants AC2 (session_015uhdrDuE49CJ8iWWX2SEeP) copied on anything going into claude/arrows-c.

## Verdicts given (all in plans/review-fe2.md)
| What | Tip | Verdict |
|---|---|---|
| CP4 Tracked 24/41 | claude/fe2-tracked 251d9788 | PASS |
| CP4 38, the board pin | f59b471e, then 016fc65e (acts on release) | PASS, PASS |
| DS1 27, words once | claude/fe2-player 88df5899 (+ 1dd4f560 check) | PASS |
| FX2 29 Clock in, 40 tea | claude/p5-fix2 421838e4 | FIXES NEEDED (the arrow went off entering the Works bay) |
| FX2 fix | ffdbb8cd | PASS |
| FX3 fix 15 (33, 38, dock) | claude/p5-fix3 3b7b13db | PASS WITH FIXES (dock check line); FX3 dropped the dock clause in fix 16 (RV7 passed 16-18) |
| FB1 fe-cartdock | a52aad05, 228de584, ebf456b6, 191bee5d | PASS each |
| SC1 breakfast-back | claude/breakfast-back 0cd37b1b | PASS |
| FX5 tip-clear | claude/tip-clear feb2e54a | PASS |
| SC1 dinner-spread | claude/dinner-spread ed6bcbf3, check ed7f5318 (FX4) | PASS WITH FIXES, then PASS with events_check 1a |

## Loose ends
- dinner-spread's events_check 1a limit (6 a minute) equals the tip's worst (Sunday tables): a later schedule change may need the number looked at.
- Day 0's Sunday table stays full about an hour after you're let go with DS1's tour (plans use the fixed 'free' minute): the user should hear it.
- Stale-ray edge (FB1's choreThingTap onPin reads the last canvas ray; CP4's ixGoalTap calls playerTap without one):
  lead 30 put it on the backlog.
- Section 11's lift guard (FB1 191bee5) counts a stop within 1.5 m of the lift tap: nothing near a lift today
  (p_liftnear.py); a future stop by a lift would block it.
- The 1-in-9 board-pin miss on CP4's old click version was never explained; the click path is gone in 016fc65e.
- FX3's lathe pin always points at 5-make-1, even when busy (FX3 logged it for the backlog).

## How I tested (scratch; copies of the probes in plans/review-rv8/)
- Builds: `git show TIP:starship-cadet.html > x.html`. Worktrees (`git worktree add --detach`) for check_fast.
- cadet_test strictly alone. A one-off a_start difference of ~14,800 px (a speech bubble a few px aside) showed up
  twice in this session on unrelated changes and never repeated: rerun before believing it.
- Combined builds (two branches' changes together): apply one branch's `git diff` with `patch -p1` onto the other's
  file, then names_check.js.
- "Exactly X and nothing else" (breakfast-back): apply `git diff OLD NEW -- . ':!plans'` with `git apply --3way` onto
  the new base in a worktree, keep the base's build lines, then diff that against the tip.
- Probes take `GAME.html DIR_WITH_cadet_test.py [OUT]` and exec cadet_test up to `a, shots = run(`.
- Three browsers at once is fine on 4 cores (each its own CADET_WORK: /tmp/cadet-work, /tmp/w2, /tmp/w3 with three
  symlinked); cadet_test always alone.

## Gotchas
- A person standing at a stop takes the tap (their card): the user counts this as not a problem.
- At 390x844 some camera turns put the job board off screen (only the edge arrow): not a pin failure.
- Skipping to Day 1 with skipTo leaves the intro odd (the bag, step 'bunk'); stow the bag (bagStow) first.

## Open questions for the user
None.
