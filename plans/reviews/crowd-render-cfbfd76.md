# Review: performance 0.27.25 (crowd-render cfbfd76): shadow stand-ins

Reviewer 2, 2026-10-17. Diff against a0c3624. **Verdict: PASS.**

The lead asked about three cases; I checked each in the browser, the old build against the new:
- **The Shadows button** (it switches `renderer.shadowMap.enabled` and marks materials for update): off, on, no errors. Three skips its shadow pass when shadows are off, so the wrapper only sets visibility flags.
- **Resize** (900x760 → 390x844 → back): no errors. Resizing changes neither `renderer.shadowMap` nor its `render`, so the wrapper stays.
- **Deck changes** (5, 3, 4): no errors. unloadDeck clears `SHADOW_PROXY`, and the stand-ins are children of `deckRoot`, so they go with the deck: 156 on Deck 4, all parented there. deckRoot is never moved, so stand-ins in world space are correct.
- **cadet_test old against new:** every shot has 0 differing pixels. The only difference is the renderer's geometry count, 416 → 371, which is the point.

Things that hide or move at runtime, checked one by one:
- Carts out on a run: `noMergeAll(cart)`, so they're skipped.
- Tall rooms fading: their own copies stop casting and the cell stand-in casts for them. That matches before, when the faded copies were still drawn and cast.
- Hull decor and wall runs dropping in the cutaway: `vis`/`follow` via shownChain.
- Event decor (dressShow): added after the build and `castShadow = false` anyway.
- The Tern's roof and ramp (decks 0.38.18): noMerge, so they're skipped.
- Anything that moves would already have broken `mergeMeshes`, so it's already noMerge.

Low, for the record:
- **Losing the graphics context** (`WEBGL_lose_context`, then restore): no errors in either build, but the picture is wrong after a restore in both (old build: 92k of 684k pixels differ from before the loss). The game has no restore handling today, so this is not new. The stand-ins free their CPU copy after upload (`onUpload → array = null`), so they could never be uploaded again. If anyone adds restore handling (phones lose the context when backgrounded), it must call `shadowStandIns()` again.
