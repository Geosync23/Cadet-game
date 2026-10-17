# Review: galley 0.29.34 (7282327), food held warm for a meal tradition; galleyJoin peek

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.** It fixes the Sunday-table wait. One FYI for the combine.

## Tests
- cadet_test 0.29.33 vs 0.29.34: **ALL IDENTICAL**.
- **With and without, on the same trial merge** (galley + claude/sim-engineer e1bb1e6 (sim to 0.26.37) +
  claude/ship-events; build-label conflicts only, `node --check` OK), food_check (7282327's):
  - 0.29.33: day 7 `hart-ravi 18:16 waited 6 minutes`, and with it "carts: the cold store ran short", "spoilage...",
    "busy: day 7 waits dinner 6" (4 FAILs);
  - 0.29.34: **day 7 waited 0, longest 0 min**; those 4 FAILs are gone. Day 7 cooked 140, wasted 4, spoiled 0, cold store
    low 174, so holding 40 more warm doesn't waste food.
- **feastCap** read: the servery's cap is raised by 40 only on a day/meal with a tradition tie (`galleyTies(d)[meal]`),
  still capped by who's coming (`countFrom(...) + wait + slack`), so ordinary meals cook as before.
- **peek** read: with sim engineer 3's line (`lineJoin` pushes, `lineLeave(id)` splices; no `gaveUp`, so no log), a
  peek joins, reads the back spot and leaves in the same call, so the line is as it was. Someone already in the line
  (`had`) is not taken out. `galleyLine()` now also needs `servLine`, which comes with the other four.

## FYI for the build master
On that merge, food_check also fails `galleyJoin / galleyTurn: [1, False, False, True, False, True]` (the player isn't
at the front at the estimated turn). It fails **the same with 0.29.33**, so it's not this build. It comes from the
newer sim (e1bb1e6, 0.26.35-0.26.37: the engineer's own merge with bfcd864 passed): the live line has someone ahead
whom the jump in time didn't serve. It's for the galley or sim engineer to settle whether the check or the turn
estimate should change, before sim 0.26.35+ and galley are combined.
