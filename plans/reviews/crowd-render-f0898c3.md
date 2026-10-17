# Review: crowd-render 0.27.31 (f0898c3), the main loop's wall cut without per-frame arrays

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS**, no findings.

- Posts: a plain max loop gives the same value as `Math.max(...touch)`, -Infinity when empty, NaN if any is NaN.
- HRUN_EDGES: `e.hrun` is set in exactly one place (line ~3274, in the deck build, right after `EDGES = new Map()`
  at ~2938 and the hull runs); nothing else assigns or deletes it. The loop can't run in the middle of a build, and a
  new deck makes a new Map, so the `of !== EDGES || n !== size` test lists the right edges for every deck.
- Void blocks: `dep()` takes the same four corners with the same expression, so it gives the same max.
- cadet_test 0.27.30 vs 0.27.31: **ALL IDENTICAL**.
