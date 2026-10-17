# Review: claude/ship-events 43e0bc8 (0.34.29-0.34.30, 24 baked traditions), reviewer 2

**Verdict: PASS WITH FIXES** (no blocker on this branch).
- Text: I baked the 24 traditions with dialogue's latest content_gen and lines_check (the romance, self-name and
  placeholder rules): PASS, 0 errors. Hash keys 434-482 are unique; drafts (`.trad-draft`) aren't loaded.
- events_check (the default run): every tradition loads and falls on its days; plans are the same twice; everyone
  reaches their places with no one stuck; draw calls 182-221. The only FAIL is
  `231 dayReport double: 3-store-1 esposito-yara/ishikawa-orla@14:30`. I ran dayReport(231) on ship-integration
  0.60.0 and got the same double, so it's **pre-existing** (the store till's 14:30 hand-over), not this branch. It
  only shows now because harvest supper's day gets checked. It belongs to the sim/store owner.

1. **MEDIUM (a promise the day doesn't keep):** one-week-aboard's Mail says "He [Zeke] and Pell will buy you a tea in
   the bow lounge at 15:30". On day 7 (Sunday) Pell is on shift (eventFree false), so only Torres goes ("went 1/2").
   Name only Torres, or time it after Pell's shift. Generally: Mail and texts shouldn't name anyone the `who` rules
   can't guarantee is free.
2. **MEDIUM (turnout at the meal traditions):** sunday-table drew 4 of 46 eligible on day 7 and 12 of 52 on day 364;
   harvest-supper "long tables and everything from the garden" drew 6 of 57. A harvest supper for the whole ship with
   6 people looks empty. Check whether section 14 honours `meal: dinner` yet (going IS dinner). If it doesn't, the
   ordinary dinner still competes. Either way, the lead should know before the user sees it.
3. **LOW, props:** 8 decor ids have no DECK_DRESS yet (cup-board, harvestTables, long-tables, mending-table,
   open-lab, rummage-crates, talent-stage, yearsEnd); that's the deck architect's queue. `mugRack` (new-hands-tea) is a
   wall-kit piece that's always on the wall, not a DECK_DRESS, so it will never resolve. Drop the tie. The deck
   architect's `tastingTable` prop exists, but tasting-table.trad doesn't ask for it (`ties: decor tastingTable`).
4. **LOW, Mail volume:** Tuesday evenings can bring three tradition Mails at 18:00 (Birthday, Open lab, Tiles night,
   seen on day 8), plus the existing duplicate "Storm prep" Mail on day 10 07:00. Worth a "This week aboard" digest,
   or a cap per evening.
