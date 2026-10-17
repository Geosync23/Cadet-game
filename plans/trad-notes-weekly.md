# Weekly traditions: design notes (seat 15, `claude/trad-weekly`)

The tradition designer for weekly traditions. Files: `content/traditions/<id>.trad` (grammar: `plans/trad-format.md`). Hash keys 435-454 are this seat's; 435-441 used, 442-454 free. All seven pass `plans/trad_parse.py`, and `lines_check.py` passes once `content_gen.py` has baked them (the bake itself is the traditions engineer's: this seat never touches the game file). `events_check.py` on a scratch copy with the bake: **EVENTS CHECK OK** over 28 days plus days 100 and 300.

## The week, with the twelve existing traditions

Two at most an evening, never two on one deck at once (the voice budget). Birthdays (20:15, the mess) can land on any evening and are never moved: that's the engine's rarer-wins rule, not something the weekly files can avoid.

| Day | Morning | Evening (deck) | Count |
| --- | --- | --- | --- |
| Mon | | **Garden hour** 17:30-18:30 (3), running club 19:15-20:00 (3) | 2 |
| Tue | | **Tiles night** 20:00-21:30 (3) | 1 |
| Wed | | **Brennan's tasting table** 18:15-19:15 (3); hull-lights every 4th Wednesday 21:00 (3) | 1-2 |
| Thu | | quiz 20:00-21:30 (3), **Late piano** 21:45-22:30 (4) | 2 |
| Fri | | Works tea (5), music jam (4) | 2 (unchanged) |
| Sat | **Long breakfast** 08:00-09:30 (3); harvest morning 09:30 every other week | film (4), observatory (2) | 2 (unchanged) |
| Sun | swap meet 10:30 | **Sunday long table** 18:00-19:00 (3), **Letters evening** 19:15-20:15 (3) | 2 |

**Tuesday is the only evening with room** for an every-few-weeks tradition (after Tiles, or off Deck 3). Wednesdays are full one week in four (hull-lights, day 24, 52...).

## Cut, merged, moved, added (with reasons)

- **Garden hour moved** from Wednesday 18:00 to **Monday 17:30**: on Wednesday it would sit on Deck 3 at the same time as the tasting table, and it would make three on hull-lights Wednesdays. Monday also starts the week with the beds tended.
- **"Sunday roast" renamed Sunday long table**: Sunday dinner is already the dish the crew voted for (section 17's `galleyMenu`), which isn't always a roast. The tradition is the long tables and sitting with friends, not the dish.
- **Tasting table and Wednesday's favourite kept together**: the favourite stays the main; the tasting table is two small extra plates at the servery end.
- **Long breakfast** ends its gathering at 09:30 so it never overlaps the fortnightly harvest morning on Deck 3; the galley keeps serving until 10:00.
- **Late piano** moved from 22:00 to 21:45 (just after the quiz ends) so listeners aren't too close to bed; it's on Deck 4, so it never shares a deck with the quiz.
- **Nothing cut, nothing added**: seven weekly traditions fill the week to the voice budget; another weekly one would push an evening to three.

## What each asks of others

### The sim engineer
- **A `meal` field** (still to be added to the grammar by the traditions engineer; written as a `// meal: ...` comment in each file until then): `meal: dinner` (tasting table, Sunday long table) and `meal: breakfast` (long breakfast) mean going **is** that person's meal, so they don't eat twice or skip the tradition for their usual dinner. `events_check.py` shows why: Sunday long table has 41-50 people meaning to go, but only 4-10 end up there, because their ordinary dinner in the same mess takes the slot. Same for the tasting table (8-13 of 27-30).
- **Seating by friendship** at the Sunday long table: friends (`affinityPlan`) sit next to each other on the long tables (`ties: galley seating=friends`). Pure, from the weekly snapshot, never live state.
- Long breakfast: people who are off on Saturday may sleep in and have breakfast 08:00-10:00 instead of the usual window.

### The galley engineer
- **Long breakfast** (`ties: galley meal=breakfast dish=pancakes until=10:00`): on Saturdays, pancakes (today Saturday is Brennan's spiced beans; Tuesday's breakfast is already pancakes and fruit, so maybe swap those two days) and the breakfast window stays open until 10:00 (`FOOD.close.breakfast` 600 on Saturdays).
- **Tasting table** (`ties: galley meal=dinner extra=tasting batch=20`): two small dishes, about 20 tastes, cooked with Wednesday dinner, mostly from garden produce. The two this week come from the tally's list in order (two a week, so the list of eight lasts four weeks, then repeats).
- **Sunday long table** (`ties: galley meal=dinner seating=friends side=tasting`): Wednesday's winner as a side with Sunday's voted dish; the menu note might read "voted for by the crew, 23 votes, with Wednesday's winner: herb flatbread".

### The garden (the galley engineer)
- **Garden hour** (`ties: garden tend`): a small boost to the garden's condition for the week, by how many came (numbers yours).

### The traditions engineer
- **Tally `tasting`** with `choices=herb-flatbread|pickled-beans|...` (dashes for spaces; show them with spaces): each week two choices, the crew who went each pick one (seeded), the winner is read on Sunday by the galley. A token you drop yourself counts as one more vote.
- **Tally `tiles-night`**: the night's results, kept for a week, for news and chatter ("Rina won again"). The game and the crew's games on paper are the Tiles engineer's (session_01DG3in6CvFFta6NrLpoVCJV); this tally is only where the results live, if that suits them. Please pass the question on.
- **The `meal` field** above, for the grammar and the loader.
- **Birthday versus Tiles night:** on day 100 the voice budget dropped Tiles night for Founding Day (right). Birthdays on Tuesdays happened alongside it (day 9); if the rule ever drops Tiles night for a birthday, Rina's streak skips a week, which is fine.

### The deck architect (decor at most 6 draw calls, only on its deck, only during its window)
- **`tiles-boards`** (Tiles night, Deck 3 bow lounge, Tuesday 20:00-21:30): a board on every lounge table, one instanced mesh, at most 3 draw calls (Part 5). The always-there Tiles station is separate dressing.
- **`long-tables`** (Sunday long table, Deck 3 mess, Sunday 18:00-19:00): a table runner and a few jugs along the joined tables; at most 2 draw calls (one instanced runner, one instanced jug). The tables themselves don't move.
- **`postbox`** (Letters evening, Deck 3 call-home booths, Sunday 19:15-20:15): the postbox is permanent dressing already in the deck architect's brief; during the window, a small stack of envelopes and a lamp on the waiting-room table (1-2 draw calls).
- **Event tags, if you like:** the piano bench (`4-music-1`) as `event: 'late-piano'` so the Captain always gets it; the servery end of the mess for the tasting table.

## Each tradition in a line

| Id (k) | When, where | Who, host | Ties |
| --- | --- | --- | --- |
| `tiles-night` (435) | Tue 20:00-21:30, Bow lounge lounge seats | Rina always, lounge regulars, bar regulars, juniors; host Rina; invite 40% | decor `tiles-boards`, tally `tiles-night` |
| `tasting-table` (436) | Wed 18:15-19:15, Mess hall, hold none | Brennan always, galley crew, lingerers, everyone 35%; invite 25% | galley extra=tasting, tally `tasting` |
| `garden-hour` (437) | Mon 17:30-18:30, garden-tend then garden | Tove Cruz always, gardeners, garden-lovers; invite 25% | garden tend |
| `late-piano` (438) | Thu 21:45-22:30, music room | the Captain always (plays), music listeners, musicians, night owls; invite 10% | none |
| `long-breakfast` (439) | Sat 08:00-09:30, Mess hall, hold none | late sleepers, lingerers, juniors, everyone 40% | galley breakfast, pancakes, until 10:00 |
| `sunday-table` (440) | Sun 18:00-19:00, Mess hall, hold none | Brennan always, lingerers, everyone 60% | galley seating=friends side=tasting, decor `long-tables` |
| `letters-evening` (441) | Sun 19:15-20:15, call-home booths then the bow lounge | Alejandro Reyes always (host), calls-home 75%, quiet-corner 30% | decor `postbox` |

## Tone

Generally light and cozy; `#funny` where a line jokes, `#warm` for the quiet ones (late piano, letters). No `#serious` lines: `lines_check.py` keeps serious lines for earned moments. Speakers never name themselves (the loader skips such lines for that person), so lines naming Rina, Brennan or Reyes are said by others.

## Open questions (for the traditions engineer, to pass on)
1. The `meal` field: its name and shape, and who adds it to `trad_parse.py`.
2. The Tiles night tally: does the Tiles engineer want results there, or kept in section 23?
3. Long breakfast pancakes: swap Tuesday's and Saturday's breakfasts, or pancakes on both?
