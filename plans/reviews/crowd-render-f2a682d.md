# Review: crowd-render 0.27.28 (f2a682d), crowd chunks reuse their buffers and upload only what changed

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS**, no findings.

## Tests
- cadet_test 0.27.27 vs 0.27.28: **ALL IDENTICAL**.
- **Picture and sim:** the Sunday-dinner walk (Deck 3, 63 people; four walks, a Rotate, zoom out and back in, so the
  detail level changes and chunks rebuild, plus the crowd hidden for 50 frames). 0.27.27 and 0.27.28 give
  **0 differing pixels in all 8 shots** and the same 8 sim/save hashes.
- **What reaches the GPU, checked directly.** I wrapped `gl.bufferData`/`bufferSubData` to keep a copy of every GPU
  buffer, then after drawn frames compared each chunk's position, colour, skin-index and index arrays (up to `nv`/`ni`)
  with what the GPU holds, whenever three says the upload is done (`updateRange.count === -1`). Dinner from 17:50, 40
  steps of 37 to 116 skipped frames (several rebuilds between draws), zoom changes, the crowd hidden for 120 frames
  four times: **244 arrays checked, 0 mismatches**. Control: the same build with the range taken from this rebuild
  only (no pv/pi, the author's first try) gives **120 mismatches**, so the check catches the bug pv/pi fixes.
- **r128 order, read in the source:** `projectObject` calls `objects.update` (vertex uploads, once a frame) before
  `renderObject` calls `object.onBeforeRender` (which resets pv/pi) and then `renderBufferDirect` (index upload in
  `bindingStates.setup`). WebGLShadowMap calls `_objects.update` and `renderBufferDirect` but never `onBeforeRender`,
  so a shadow-pass upload leaves pv/pi low: a bigger upload next time, never a lost one. `WebGLAttributes.updateBuffer`
  uploads just `updateRange` and sets its count back to -1.
- Read: packs are compared by identity, and nothing edits a pack in place. The device's phosphor recolour deletes the
  cached prop packs and marks the chunks dirty, so the next rebuild sees new objects. The buffers only grow (by half
  again); `setDrawRange(0, ni)` keeps old tails from being drawn. The skin weights are written once on creation, and
  `crowd.stats` reads `c.nv`/`c.ni`.
