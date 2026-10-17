# Review: crowd-render 0.27.30 (975e0e5), kept bodies and fewer per-frame allocations

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS**, no findings.

## The kept bodies (CROWD_KEPT)
- **Is a packed body a pure function of the spec?** Read: makeCharacter (to its end) touches no ship state, no R(),
  no time or screen size; `col()` is a pure colour conversion. Tested: on 7 deck visits across days 1, 2, 200 and 300
  (Decks 2, 3, 4; 19 to 61 people each, the kept list holding 7 to 36 looks), I rebuilt every person's rig from their
  spec and packed it afresh: all 5 arrays (P, N, C, B, I) at both detail levels **match what they carry**, kept or not.
- Sharing: a hit deletes the entry, so only one live person holds a kept {geo, jparts}; two with the same look just
  means the second packs its own. With 0.27.28's identity compare, someone leaving and coming back to the same slot
  carries the same pack objects, and the buffer at that slot already holds exactly that body (same slot, same `b0`).
  So skipping the rewrite there is right.
- The memory is bounded: 40 entries of typed arrays, no GPU buffers.

## The allocations
- parsePose's split maps, propKeyOf memo (it reads only ACTS[act] and base, both constant), the hold and cart keys
  made once, `pk && hk ? pk + ' ' + hk : pk || hk` (= the old filter/join), the same k[] insertion order in
  animateActivity, and index loops over the slots in the same order.

## Tests
- cadet_test 0.27.29 vs 0.27.30: **ALL IDENTICAL** (my run; no noise this time).
- The Sunday-dinner walk (walks, Rotate, zoom, the crowd hidden): **0 differing pixels in 8 shots**, same 8 sim/save hashes.
