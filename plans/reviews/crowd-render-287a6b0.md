# Review: crowd-render 0.27.27 (287a6b0), posing people on screen only

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS** (one LOW comment fix, optional). 0.27.26 (d45d019) passed
separately: crowd-render-d45d019.md.

## The lead's conditions, and how I tested each
1. **Posing never feeds back into the sim.** Read: `CrowdPerson.update` writes only the person's own smoothing state
   (`rot`, `g`, `k`, `moved`, `lookOff`, `fresh`), its own random stream (`this.rnd`, seeded per person) and its rig.
   The sim reads `p.pos`/`p.face`/`p.pose` (set by `set()`, every frame as before); bubbles and taps (`crowd.near`) use
   `p.pos`, not the rig; nothing outside section 8b reads the rig. Test: a copy with `CROWD_POSE_EVERY = 1` and an
   endless margin (everyone posed every frame, as before) against 0.27.27, Sunday dinner on Deck 3 (63 people), the
   player walking in four directions, a Rotate, zoom out and back; at 8 points I hashed `seed`, every DECK_CREW agent
   (place, spot, settled, talking, x/z to 5 places), every crowd person's position, pose and facing, the whole `SHIP`
   save state and the player: **all 8 hashes identical**.
2. **No stutter on screen, shadows included.** I hooked `renderer.render` to check, every frame, everyone whose body
   (5 heights and 4 sides of the head) or shadow (4 points along the sun's direction, `SUN_OFF`) lands on screen, and
   whether they were posed that frame. Same walk (1,540 frames, 56,100 on-screen checks): **0 missed** (body 0,
   shadow 0). Control: the same build with the margin set to 0 misses 2,889 bodies and 1,077 shadows, so the check
   works. The sun's shadows reach at most 0.67 x height sideways (about 1.3 m), well inside the 4 m margin.
3. **Whoever you're with is always posed:** agents with `talking > 0` or `esc` are kept (and they're beside you anyway).
4. **Every cadet_test difference is explained:** there are none. cadet_test 0.27.26 vs 0.27.27: **ALL IDENTICAL**.
   Screenshots from test 1 (throttled vs always) differ by 0 to 514 pixels: small head turns and looks, because the
   people who were off screen called their own random stream fewer times; no one is out of place (checked by eye).

## Finding
- **LOW (comment):** "posing (limbs only)" and "writes only their rig": the update also places the body
  (`rig.root.position`, rotation, lying down), so an off-screen person's whole body waits up to 9 frames, not just
  their limbs. Harmless (they're off screen, and the chunk's bounding sphere is rebuilt from the same roots each frame),
  but the comment should say so for the next reader.
