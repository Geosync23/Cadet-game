# Re-review: claude/arrival 11ceb84..7abf466 (0.42.13-0.42.15: the first launch from section 21's first frame; Torres's lines wait for their time; dinner seats)

Reviewer 1, 2026-10-17. Section 21 only (plus intro_check). name_check against 11ceb84: OK. **Verdict: PASS.**
- One first-launch design, agreed with sim 0.26.25: section 21's first frame calls `newGameStart(true)` when there's no save, it isn't a test URL and this device has never arrived (`INTRO_BOOT`). Combined with sim f9a4843 (and crew, social A, social B, systems), intro_check is OK, parts 8 and 9 included: a first launch arrives on Day 0, and its save reloads at its step.
- `introSeat` gives you, Torres and Calder dinner seats; Torres is led to his. In the real-game walk Torres led for 199 looks, and draw calls peak at 292 (Deck 3).
- The name after a reload is still null: part 9 notes it, waiting on player engineer 3's section 15 save. As agreed, make it a FAIL once that's combined.
