# Review: galley 0.29.33 (2bfd042, on 40166d6), tasting by turnout and an early cake

**Reviewer:** adversarial reviewer 2b (taking this one from reviewer 1, who keeps 40166d6 itself). **Verdict: PASS.**

## Tests
- cadet_test 0.29.32 (40166d6) vs 0.29.33: **ALL IDENTICAL**.
- food_check (2bfd042's): **FOOD CHECK OK** on the branch. On a trial merge with claude/ship-events (the rotations,
  so the welcome tea exists; only the build-label conflict, `node --check` OK) also **OK**, and its new check finds
  the tea: day 40 "New hand's tea", cake out at 18:40 (not out a minute before, out a minute after), servery text
  "A New hand's tea cake on the end of the counter."
  (Started at day 35 instead, food_check fails "spoilage: no Mail" and "garden, good" on 2bfd042 alone too, so that's
  the check's starting day, not this change.)
- **Tasting by turnout** on the merge, Wednesdays days 3 to 66: voters 19 to 26, tastes always twice that (38 to 52,
  never under 20). Day 10's dinner leaves 170 meals in the cold store and the tasting is cleared by 19:50, so the
  bigger batch doesn't starve dinner.
- Read: the cake block now runs every minute from dinner opening to 19:30 (it used to run only at fixed minutes);
  inside it, the Mail, the bake and "gone" are still keyed to their exact minutes, so only `out` moves. An early cake
  needs a gathering whose `where` names Deck 3's mess and that starts between dinner opening and 19:30; the Mail
  then says "out on the servery from 18:40, and everyone's in the mess at 18:40".

No findings.
