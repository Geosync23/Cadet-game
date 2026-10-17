# Review: crowd-render 0.27.29 (870ee00), findPath as a heap search

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS**, no findings. (It also carries the 0.27.27 comment fix.)

## Equivalence, read against findPathScan
- The scan picks the lowest `dist + hx` (same arithmetic order in both), first in the open list on a tie. The open
  list keeps push order, a re-pushed node's entries share its current dist, and the first entry is never removed
  before the node closes, so the scan's choice is (f, the node's first push). The heap orders by (f, `seq` of first
  push) and decrease-key keeps `seq`. Same choice every step.
- Neighbours, diagonal corner checks and the four edge checks are in the same order; `free`/`edgeOpen` are memoised per
  call with the same edge keys as EDGES (`v,max i,j` / `h,i,max j`); off-grid, non-integer starts and goals go to the
  old function. The start equal to the goal gives [] in both; an unreachable goal gives null in both; the goal array
  object is still the last element. The avoid keys parse to on-grid tiles only (off-grid ones never matched anyway,
  since `free` fails there).
- The typed arrays are reallocated when W*D changes, and stamped per call. Nothing that `free`/`edgeOpen` call can call
  findPath again, so the shared arrays aren't re-entered.

## Tests
- path_check (870ee00's) on the branch: 6 decks x 3,000 random searches **all the same** (incl. no-path cases), a
  played Monday **1,131/1,131** real calls the same; 3.7x faster over the random set.
- On a trial merge with sim e1bb1e6 (0.26.37, crewMakeWay), decks-p3 (the trestle's tile block) and ship-events,
  with a **different random seed**: all decks the same, a played Monday **3,072/3,072**, and a Sunday evening on
  Deck 3 from 17:20 to about 19:20 (the trestle out and its tiles blocked) **616/616**.
- cadet_test 0.27.28 vs 0.27.29: **ALL IDENTICAL**.
