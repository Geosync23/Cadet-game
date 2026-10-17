# Review: crowd-render 0.27.33 (73b8998), the shadow stand-ins built a slice a frame after a deck change

**Reviewer:** adversarial reviewer 2b (for performance engineer 3). **Verdict: PASS.** Two LOW notes for the watchdog.

## Read against 0.27.25's one-go build
- Which meshes become stand-ins: the old first pass set `castShadow = false` on each mesh as it took it, so a mesh
  reached twice, or a TALL own mesh met later, was skipped. The new `seen` set does the same, and own meshes are added
  to it at the same point in the order. So the set and the bucket order are the same, and the fill reads exactly the
  meshes the count read.
- Triangles: indexed geometry read through `getX` in index order is what `toNonIndexed` produced. The cell key is
  `floor(cx / 3 / CELL)` in the same order of operations, and the matrix is taken at listing time (build time), as before.
- The bounding sphere: box while counting, centre = box middle, radius = max distance while filling, which is what
  `computeBoundingSphere` does for a position attribute.
- During the job the originals cast as before 0.27.25; `tallSync` still swaps own meshes and the combined TALL mesh, so
  each tall piece casts exactly once. At the end it all switches in one frame. `unloadDeck` and a changed `deckRoot`
  drop a job.

## Tests
- cadet_test 0.27.32 (b3930f8) vs 0.27.33: **every shot 0 px**. The state differs only in GPU memory (geometries
  371 -> 416 at the end of the test), as the author says: off-screen originals uploaded by the shadow pass while the job runs.
- **Interrupted builds:** I visited all 6 decks (job running on frame 1: 0 stand-ins, all originals casting; settled
  after 120 frames), then made 30 random deck changes leaving 1 to 13 frames after arriving, then visited all 6 again.
  Each settled deck has the **same stand-in count, casters and shadowProxy marks** as the first visit (D3 82/133/441,
  D2 103/129/382, D5 62/90/286, D4 156/167/633, D1 32/43/146, D6 34/48/138), no job left over, no errors.

## LOW (for the phone-speed watchdog)
1. For the first frames on a deck (about 48 on Deck 3, 1.6 s at 30 fps) the shadow pass draws the originals, as
   before 0.27.25: on Deck 3, 629 meshes cast instead of 133 + 82 stand-ins. That's shorter and lighter than the old
   165-326 ms freeze, but perf_check's arrival frames will show it.
2. Those shadow-pass draws upload ~45 off-screen geometries that stay in GPU memory until the deck is left (371 -> 416
   in cadet_test). That's bounded per visit and not a leak (deck_check's memory over round trips is flat, per the author).
