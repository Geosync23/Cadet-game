# Re-review: claude/arrival 330e538..11ceb84 (0.42.11-0.42.12: Torres's arrow comes back; the sim 0.26.23 merge; the evening walked in the real game)

Reviewer 1, 2026-10-17. **Verdict: PASS.** It fixes the first-load finding from my sim 94aa2d2 review, on this side.
- `introWanted` is now a function declaration that reads the storage key itself, so section 13 can call it at load (no temporal dead zone). Section 21 calls `introBegin()` at load when `ARRIVING`.
- **Proven in the browser** (`?debug`, fresh storage): the first launch opens on Day 0 17:40, Deck 5 [7, 8], intro on, with the manifest showing. Signing and playing on to `haulway`, then reloading, resumes at Day 0, `haulway`, with Torres on the deck. A save made by closing the page during the manifest also resumes at the manifest.
- intro_check OK, including part 8, the evening walked in the real game: draw-call peaks Deck 5 192, Deck 4 209, Deck 3 292 (budget 450). name_check OK on the file and against 330e538.
- The name after a reload is null on this branch alone. That's expected: section 15's saved name is on claude/player-needs (0.28.22+), not merged here.
- Still to come (as the branch says): a reload mid-walk inside intro_check itself. The browser run above covers one case by hand.
