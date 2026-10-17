# Review: crowd-render 0.27.32 (abe6d2b), loop() without iterators or closures

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS**, no findings.

## The three things the author asked me to check
- **Counter names:** in loop() the new counters are `k` (outer loops), `j` (inner loops) and `q` (STEAM). Apart from the
  loop headers, the only `k` is STEAM's own `const k` (inside its `q` loop), and the only `i` is DUST's and the posts'
  inner loops. No other line in the function reads `k`, `j` or `q`, so nothing outside a loop picks up a counter.
- **TALL:** the hide test is now a `j` loop that stops at the first hit (the same as `.some`); the rest of the body
  runs per tall piece as before, and `t` shadows the time inside it exactly as the old `for (const t of TALL)` did.
- **Doors' `near`:** `walk` is worked out only when `force` is undefined, `crewAt` is false and the door is passable or
  service, which are exactly the cases where the old `crewAt || (passable || svc) && walkers.some(...)` reached the
  `some`. It stops at the first active walker in range, so `near` is the same in every case. The leaves use `j`
  for forEach's `k` (0 = left, else right).
- Index loops see a length change mid-loop the same way `for...of` over an array does (e.g. a MOVERS tick).
- STEAM's scale (`.1 + k * .18`) and every other expression are unchanged.

## Tests
- cadet_test 0.27.31 vs 0.27.32: **ALL IDENTICAL** (run with a longer page-load timeout: this container was slow, 39 s
  to load the page).
