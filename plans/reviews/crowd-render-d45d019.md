# Review: crowd-render 0.27.26 (d45d019), freezeStill

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS** (one LOW note). 0.27.27 (crowd posing on screen only) is not pushed yet; reviewed separately when it lands.

## What it does
After each deck build, `freezeStill()` turns `matrixAutoUpdate` off for everything under staticRoot, TALL and WALL_DECOR,
except noMerge parts (and everything under them), SPINS targets, STEAM puffs and the groups that hold any of those.

## How I tried to break it
- **A moved-while-frozen detector.** On a trial merge onto claude/cand-0603 (d0d217b, 0.60.3 WIP, the newest game code),
  on every deck (1 to 6): after the build, took every object with `matrixAutoUpdate` off (minus the shadow stand-ins),
  then ran a whole ship day of crew (every 6 ship minutes `updateDeckCrew` plus 2 real frames, so MOVERS, SPINS, PULSES,
  the garden view and the galley views all ran) and cycled the Walls button every 4 hours. At the end I compared each
  frozen object's matrix with the one its position, rotation and scale would give. **Moved: 0 on every deck**
  (frozen: Deck 1 141, Deck 2 553, Deck 3 638, Deck 4 1,028, Deck 5 447, Deck 6 179).
- **Code read** for things that move after the build: curved walls, hull runs, doors and void blocks (scaled by the
  cutaway) all hang off deckRoot, not the frozen roots. The decor (dressShow), the galley's cake, food, plates and
  grab-and-go rolls, and the tray are added after the build, so they keep updating. The garden view and the tray read
  `matrixWorld`, which is still kept up to date (see the LOW note). The punch bag, gym seats and rotors are noMerge.
- cadet_test 0.27.25 vs 0.27.26: **ALL IDENTICAL**. deck_check: OK on the branch build and on the trial merge.

## Findings
- **LOW (the comment and the dev notes row say a bit more than happens).** In r128, `updateMatrixWorld` passes
  `force = true` down from any parent whose matrix was recomputed, and the scene and deckRoot still update themselves
  every frame. So every frozen object still gets its world matrix multiplied every frame; what freezeStill saves is the
  `compose` (position, rotation, scale into a matrix). That fits the small gain the row measured (0.35 to 0.33 ms).
  Turning the cascade off as well (deckRoot and the scene not recomputing themselves) would need every hand-set matrix
  (the shadow stand-ins) to set `matrixWorldNeedsUpdate`. Only worth it if a phone profile shows matrix work matters;
  the row already says the crowd's skeletons are the real cost. No change needed for this build.
