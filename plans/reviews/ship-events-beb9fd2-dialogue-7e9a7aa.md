# Re-review: claude/ship-events beb9fd2 (0.34.23) with claude/dialogue 7e9a7aa, reviewer 2

**Verdict: PASS** for both, and for combining them.
Trial merge (integration, then ship-events beb9fd2, then dialogue 7e9a7aa). Conflicts: only the two build labels.
- After `content_gen.py` on the merged tree, Sowing is baked; a second run says "no change"; `node --check` OK;
  lines_check PASS.
- events_check (7 days) on the merged, re-baked build: plans the same twice; sowing due on days 6, 97, 188 and 279;
  baked and its Mail filled. The only FAIL is hull-lights, which falls after the 7-day window.
- My first-review findings, each checked:
  - friends-of-host now uses `affinityPlan(host, p.id, d)`.
  - Lines that name their own speaker are filtered (tradText); the Mail uses {time}.
  - trad_parse gives a TradError (file:line) for: quarter week 14, year day 400, quarter day 0, arrival nth 0,
    week x, hold abc/0, and a hold beyond the where lines.
  - The eventsOn cache clears when introArrival() changes.
- Still the build master's step: re-run content_gen.py after merging dialogue (the block on the dialogue branch can
  be empty), and the build label.

## Addendum: e1a5d01 (0.34.24): PASS
- events_check now fails when a content/traditions/*.trad id isn't among the baked SHIP_TRADITIONS. This closes the
  "empty block hides Sowing" hole.
- `simNote('choice', { script, k, meeting, who, flavour, mem, flag })` in dialogueStep, inside section 18 and
  typeof-guarded. `D.m` is already relied on two lines above, and `who` is de-duplicated ids. No state change, no R(),
  nothing per frame.

## Addendum: 4294df1, 5a547e8 (0.34.25-0.34.26): PASS
- `trace` on a tradition: `traceAdd(id, day)` stores `{ id, day }` once, when you join. Loading keeps strings or
  `{ id: string, day: int }`. `traceOn` reads both shapes, and every other SHIP.traces use on every branch only compares
  strings (`includes`), which is safe with objects mixed in. dressShow hands `{ id, day }` to the decks branch's
  seedlingYours as `o`, as it expects.
- `tradDecor`: ties.decor -> a DECK_DRESS id, from 30 minutes before to 15 after; one more dressShow entry (the
  key-compare stops any rebuild per minute).
- The storm: `earliest: 10, spread: 1` gives day 10 for every new game. The diplomatic visit follows from it as before.
