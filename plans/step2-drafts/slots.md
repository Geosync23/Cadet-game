# Draft: labelled per-seat append slots in the game file (not applied)

**What:** one empty, labelled block per seat at the end of its main section, where that seat adds new top-level code (SR2's option d; the split rehearsal found 260 of the 606 clashes left after the build number were two seats adding lines at the same spot, and 18 merges had nothing else). Section 20c's `// ---- end of 20c ----` did this before, "so social engineer A's merges never clash".

**How:** `python3 plans/step2-drafts/add_slots.py` (comment and blank lines only; it refuses if a heading moved, a slot exists, or a slot would land inside a statement, and it proves that removing the added lines gives back the original byte for byte). Tried on 0.64.2: 17 slots, 51 lines; names_check OK, content_gen --check "up to date", section.py still finds all 56 sections.

**Proved on a scratch git repository** (0.64.2 with the slots): the player and interactions seats each add a function in their slot, both merge with no clash. Without slots, the same two additions at the old spot (the end of section 15, just before 15b's heading) clash.

| Seat | Slot at the end of section | Just before |
|---|---|---|
| Deck architect | 4d | `// 4e.` |
| Rec engineer | 4e | `// 5. LIGHTING` |
| Sim engineer | 14 | `// 19. DEVICE` |
| Device engineer | 19 | `// 15. PLAYER NEEDS` |
| Player engineer | 15 | `// 15b.` |
| Interactions engineer | 15b | `// 15r.` |
| Galley engineer | 16 | `// 17. MACHINES` |
| Systems engineer | 17 | `// 22. LINES` |
| Dialogue engineer | 22 (after the generated blocks and the engine) | `// 18. SHIP EVENTS` |
| Traditions engineer | 18 | `// 20. SOCIAL` |
| Social engineer | 20c | `// 21. ARRIVAL` |
| Onboarding engineer | 21b | `// 23. TILES` |
| Games engineer | 23b | `// 24. WORK` |
| Puzzles seat | 24k | `// 24e TUNING` |
| Works career engineer | 24p | `// 6. CAMERA` |
| Performance engineer | 8b | `// 9. CREW DATA` |
| HUD seat | 11 | `// 12. MAIN LOOP` |

No slot for the crew designer (section 9's roster is written by `plans/crew-roster-gen.py`).

**Rules that go with it** (in the CLAUDE.md and DEV_NOTES drafts):
- New top-level code goes in your slot, just above its end line. Edits to existing code stay where the code is.
- A slot is a place in the load order: code there runs after everything above it. If new code must load earlier (something above reads it at load), ask the lead for a second slot at the right place rather than squeezing it into a neighbour's spot.
- A whole new feature (for example Dev mode, step 3) gets its own section heading and its own slot, placed by its plan page. A suggestion for Dev mode: a new `// 25. DEV MODE` section just before `// 12. MAIN LOOP` (after every system it moves: the clock, the career, the traditions), gated by one switch so the normal game is unchanged.
- The same seat on two branches can still clash in its own slot; that's the normal, small kind.

**Applying it (after the rec deck is published; the build master's job since it's the shared file):**
1. On the shared branch's tip: `python3 plans/step2-drafts/add_slots.py`.
2. Prove the game is unchanged: `cadet_test.py OLD NEW` ALL IDENTICAL (OLD = the tip before, NEW = with slots), `bash check_fast.sh` OK, and a screenshot of the opening on a phone and a desktop for the lead. (Comments change nothing the browser runs, but the file's size and every later line number move.)
3. No build number change (nothing in the game changed); a DEV_NOTES row "slots added, game identical".
4. Move `add_slots.py` to `tools/` (it stays useful for adding a seat's slot later) or delete it; update `plans/map.md` with the slot list.
