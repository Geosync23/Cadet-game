# Light review: poses (claude/poses f9c6faa + 257b3ea, 0.27.36-0.27.37) and speech bubbles (claude/dialogue 33b1366, 0.43.30)

Reviewer 1d, 2026-10-17. Light reviews for perf engineer 3's poses and the dialogue engineer's bubbles. As the lead asked, I checked that the sim and timing are unchanged and the draw calls are steady.

## Verdict: PASS (both)

### Poses and table trays (on 0.60.4 d449914)
**The code:**
- Rig angles only: hands on the lap when seated, three work styles per person, and a weight shift for standing jobs.
- `tableTrays`: two instanced meshes (tray, then plate and mug) on Deck 3's mess tables, rebuilt every 15th frame only when the seated diners change.
- It only *reads* `DECK_CREW[].meal/spot`. No `R()`, no `simNote`, no plans, no `SHIP` writes. The meshes are made at first use, not at load.

| Check | Result |
| --- | --- |
| cadet_test 0.60.4 vs 257b3ea | Deck data, paths, collisions, crew and taps all the same. Every shot 0 px except `e_night`: 697 px, all in the top-left HUD panel box (24,0)-(96,41) (perf 3: a crew pose seen behind the panel). |
| day_check day 1 on 257b3ea | DAY CHECK OK. Every deck's crew count, worst-stuck person and time, and draw-call peak (Deck 3 268, Deck 4 249, ...) match the same check on 0.61.x (on 0.60.4), so the sim is unchanged. |

**Low:** day_check's hourly frames didn't catch the trays' +2 calls (the Deck 3 peak is the same 268), so the +2 is unconfirmed here. It's well inside 450 either way. perf_check's mess scenes are the place to confirm it.

### Speech bubbles (on dialogue 0.43.29 9cb6f7b)
**The code:**
- CSS and DOM only: a card, a tail, a name tag in the department's colour, a pop.
- The bubble is measured once instead of every frame.
- Two bubbles that would cover each other move apart.
- Speakers are looked up by reading `DECK_CREW`. No sim or game state.

| Check | Result |
| --- | --- |
| cadet_test 9cb6f7b vs 33b1366 | Paths, crew and taps the same. Only `b_wander10s` (14k px) and `i_tap1` (25k px) differ, both inside the bubble's box. The new style shows correctly (Orla Ishikawa's name tag, the tail). |

**Lows:**
- Only exactly two visible bubbles are kept apart. Three at once can still overlap (rare).
- Each bubble's width is measured once, so a phone rotated while a bubble is up keeps the old width for that bubble's life (a few seconds).
