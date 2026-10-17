# Review: ship events 0.34.49 (3d06bcb), the long-table seats as overflow

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.** Closes reviewer 2's open item 3.
Tested on a trial merge with decks 3e1f4f9 (0.38.23: 14 long-table seats, the trestle blocking its tiles).

## Tests
- events_check (28 days + the year) on the merge: **EVENTS CHECK OK**. lines_check/cadet_test as the author ran them.
- **Does the room fill first?** For every Sunday table, farewell supper and harvest supper in 400 days I built each
  long-table place's and mess seat's busy times from everyone's plans, then for each trestle sitter looked for a mess-hall
  seat or end chair free for their whole stay. **None found** (0 cases). Seats used (mess / end chairs / trestle):
  day 7 23/4/5, day 14 26/4/3, day 21 24/4/10, day 28 27/4/5, day 35 22/4/0, day 42 21/4/8, day 49 30/4/4,
  day 56 27/4/3, day 63 25/4/2, day 70 22/4/3. The end chairs are always used before the trestle.
- **Harvest supper day 231:** 32 / 4 / 10: all 14 long-table seats used; events_check walk: 46/46 reached, stuck 0.
- Farewell suppers (9 to 14 people) stay in the mess. The room patterns `^Mess hall$` and `^Promenade$` match the deck's
  room names (`M` "Mess hall", `=` "Promenade").

## Notes (no change needed)
- Because a seat must be free for the whole stay, someone can go out to the trestle while a mess seat frees up a few
  minutes later (day 21: 10 on the trestle). That's the rule as agreed; just noting it for the lead.
