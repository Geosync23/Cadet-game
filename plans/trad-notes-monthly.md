# Traditions every few weeks: design notes (seat 16)

The tradition designer for the two-weekly and four-weekly traditions (`claude/trad-monthly`), reporting to the traditions engineer. Files: `content/traditions/<id>.trad` (eight traditions) and `content/traditions/this-week-aboard.mail` (the Sunday Mail). Hash keys used: 455-462 (of 455-474). Started from 0.60.0.

**The user's answers at check-in A (collected by the traditions engineer, claude/ship-events a597a37):** crossover supper, mending day and rummage day are **cut** (their sections below are kept for the record, marked cut; keys 457-459 stay unused, never reused). Talent night is now **once a year, day 152** (a Friday in Greening, in place of that night's jam). Bridge hour stays every four weeks but only once a story beat has invited you (`flag: bridge.invited`, the head writer's). Decor ids are the deck architect's camelCase ones: `cupBoard`, `talentStage`, `openLab`.

## The four-week cycle at a glance

Every four-weekly tradition takes one week of the cycle (week 1 = days 1-7, 29-35...), so no two land in the same week on the same weekday, and each week has something. The existing ones are in brackets.

| Cycle week | Mon evening | Tue evening | Wed | Sat / Sun daytime |
| --- | --- | --- | --- | --- |
| 1 (days 1-7) | Book circle (every 2 weeks, from day 15) | | | [Sat: harvest morning] |
| 2 (days 8-14) | | **Open lab** 17:30, Deck 2 (day 9) | | |
| 3 (days 15-21) | Book circle | | | [Sat: harvest morning] |
| 4 (days 22-28) | **Department cup** 20:15, gym (day 22) | **Bridge hour** 17:15, Deck 1 (day 23), once you're invited | [hull-lights 21:00] | |

**The voice budget** (at most two traditions from 17:00, never two at once on one deck; section 18's `evBudget`):

- **Monday:** running club (Deck 3 gym, 19:15-20:00), then from 20:15 book circle (Deck 4, weeks 1 and 3) or the cup (Deck 3 gym, after running ends, week 4). Week 2 Mondays are free now.
- **Tuesday:** Tiles night (weekly, Deck 3, 20:00) plus open lab (Deck 2, 17:30, week 2) or bridge hour (Deck 1, 17:15, week 4, once invited). Two at most, on different decks.
- **Not mine, but noticed:** the existing hull-lights evening (every four weeks, Wednesday of week 4, Deck 3, 21:00) will clash with the weekly designer's Wednesday plans (tasting table and garden hour, both Deck 3). Because hull-lights is the rarer one, one of the weekly ones is dropped every fourth Wednesday. Worth telling the weekly designer.

## Each tradition

### Talent night (455): now yearly, day 152 (the user)
Every 4 weeks, Monday of week 2, 20:15-21:45, the bow lounge. Musicians play, the bar's regulars have a drink, everyone else talks and claps. **Host: Mira Dahl** (a Watch officer and musician, off on Mondays). Not Rina or Tomas: they already host weekly ones.
- **Asks the deck architect:** decor `talent-stage`: a low riser at the lounge's bow end, a mic stand, a string of bulbs. That's 3 draw calls, Deck 3 only, during the window.
- **Asks the sim:** nothing new (`play` for musicians already exists).
- **Social:** an invitation from Mira (35%).

### Department cup (456), kept as planned
Every 4 weeks, Monday of week 4, 20:15-21:15, the gym (straight after running club). A rowing relay. **Host: Commander Vance**, who tops the rowing leaderboard and keeps the board. There are five teams so that each has enough people: Works, Watch, Survey, **Bridge** (command, helm, comms) and **Commons** (galley, garden, store, infirmary).
- **Asks the traditions engineer:** `ties: tally cup choices=works|watch|survey|bridge|commons`. A winner kept for the week, so it can be news ("Watch won the cup"). The simplest rule: the team with the most people going wins, ties going to the earlier team, seeded by day. Chatter could read it later.
- **Asks the deck architect:** decor `cup-board`: a chalk scoreboard on a stand and the cup (a mug on a plinth). That's 2 draw calls, in the Deck 3 gym.
- **Asks the sim:** nothing new. The gym's own poses (rower, treadmill) are right, so there's no `anim`.

### Crossover supper (457): CUT by the user. Was: the plan's crossover breakfast, turned round; a meal tradition
Every 4 weeks, Tuesday of week 3, 18:30-19:30, at the mess's long table (the birthday seats, `3-mess-1` to `16`), then any mess seat. The day shift's dinner is the night shift's breakfast, so there's dinner and pancakes on one table.
- **Why changed:** at 06:00 nobody could go. The night shift eats at 06:05 and goes to bed, the early day shift sleeps until about 06:50, and a tradition doesn't wake anyone. events_check failed with "nobody went" on days 17, 45 and 73, even at 06:15. At 18:30 the night shift is up (from about 14:00; on at 21:00) and the day shift is off, so 8-11 people go with no sim changes. It's still the one time the two shifts properly meet. The id is `crossover-supper`.
- **No host:** Chef Brennan cooks it and signs the Mail, but she's in the galley at that hour (she would never be free to host). With no host there's no invitation either, since events_check needs an invite to have a host. If social would like hostless invites (anyone going asks you), I'll add one.
- **The `meal` field:** `ties: galley meal=dinner dish=crossover-pancakes`. Since 0.34.30 it also carries `meal: dinner`, the real field (going to it IS that meal; the night shift's breakfast).
- **Asks the sim:** for those going, eat at the tradition's seat instead of the servery (the `meal` field): their dinner, or the night shift's first meal of the day. Few of the night shift go today (1-2 of the 6-8 who'd like to), probably because their own meal and sleep times come first. The meal field should fix that. `who:` now uses the `night-shift` word (0.34.30).
- **Asks the galley:** the dish `crossover-pancakes` (pancakes and syrup next to the day's dinner; the menu note could read "Crossover supper: pancakes for the night shift"), a batch for about 25. Tuesday's dinner is from the cycle, so it's an extra pot, not a replacement.

### Mending day (458): CUT by the user
Every 4 weeks, Sunday of week 1, 14:00-16:00, the junior common room, with the laundry as overflow. Uniforms mended, buttons sewn, spares swapped. **Host: Zeke Torres**: the roster says he knits scarves, and in 0.60.0's roster he is off at the weekend. Day 7 (your first Sunday) is the first one, so your escort can invite you (40%). **If the crew designer moves Torres's days off to Thu-Fri, as Part 1 says, he'll be on shift on Sundays**: then move this to his day off, or swap the host for another Works junior who's off on Sundays.
- **Asks the deck architect:** decor `mending-table`: a folding table with folded uniforms and a sewing basket. That's 2 draw calls, Deck 4, junior common room. `hold: none`, so the common room carries on as usual around it.
- **Later (not needed now):** a mended uniform as a small item for the player engineer, and laundry ties.

### Rummage day (459): CUT by the user
Every 4 weeks, Sunday of week 4, 14:00-15:45, the cargo hold (Deck 5). Main storage opens old crates of odd, unclaimed things. **Why changed:** it overlapped the weekly Sunday swap meet, so it's now an afternoon on another deck, and the chatter says leftovers go on to the next swap meet. That makes the two feel linked rather than the same. There's no host; it's signed "Main storage".
- **Asks the deck architect (needed):** the cargo hold has only 2 usable places (storage). Please add **standing places tagged `event: 'rummage-day'`** among the crates (8-12), plus decor `rummage-crates`: open crates (one instanced mesh) and a trestle table. That's 2-3 draw calls, Deck 5. Until then, the fallback is the haulway's gathering spots (`5 room Haulway: event`, the farewell crowd places).
- **Later:** a found item as a keepsake (player engineer), or salvage in a later phase.

### Open lab (460), kept as planned
Every 4 weeks, Tuesday of week 2, 17:30-18:30, Deck 2. **Host: Dr. Sato** (off on Tuesdays in 0.60.0, so free all day), with the Survey team.
- **Asks the deck architect (wanted):** standing places tagged `event: 'open-lab'` at the Survey lab's benches and island (6-8), so it happens in the lab itself. The lab's places are all work stations, so they can't be borrowed. Decor `open-lab`: sample trays and a small "Open lab" sign. That's 2 draw calls, Deck 2. Until then: the chart room, the science corridor's benches and the observatory.
- Juniors and seniors alike; stargazers like it. (Saturday's observatory night is the Deck 2 evening for stargazers; this is the Tuesday one.)

### Bridge hour (461): every 4 weeks, once invited (`flag: bridge.invited`)
Every 4 weeks, Tuesday of week 4, 17:15-18:00, Deck 1. Juniors visit the bridge; **the Captain** (off on Tuesdays) comes up to say hello. `who:` is the Captain and juniors only.
- **Asks the deck architect (wanted):** standing places tagged `event: 'bridge-hour'` along the bridge's rail or behind the stations (8-10). Until then: the bridge lobby's event spots, then the observation room. No decor.
- **Later (progression):** a first bridge hour could be a Record line or a memory for the Captain (`simNote('tradition')` already says you came).
- **Check:** the bridge lobby's `event` places may belong to the ready-room visits. If events_check finds a clash, drop that `where` line.

### Book circle (462), added: the only two-weekly one
Every 2 weeks, Monday of week 1 (days 15, 29, 43...; `from day 8`, so not in your arrival week), 20:15-21:30, the junior common room. Bring a page and read it aloud, or just listen; cocoa. **Host: Matthias Oduya** (an infirmary senior who signs the birthday and quiet-watch Mail; off Tue-Wed). **Why added:** Monday evenings had only running club, every other Monday of my cycle already had something, and a quiet, cozy evening gives the "generally light" range a soft note between the lively ones. It needs nothing from anyone (`anim: read` exists).

### Not changed: the existing ones in my rhythm
Harvest morning (every 2 weeks) and the hull-lights evening (every 4 weeks) stay as they are in section 18. Rewriting them as `.trad` files would give them new hash keys (from my block), which changes who goes on those days and breaks regressions, all for no gain. If you want their texts in `content/` (for chatter), I can write `.trad` versions on your word.

## This week aboard (the Sunday Mail)

`content/traditions/this-week-aboard.mail` has the words and the rules. In short:
- **Sunday 18:00, signed by Matthias Oduya**, from day 7 (day 0 has the intro's welcome instead). The usual evening-before Mail for Monday still goes.
- **It lists the rarer things in full:** every tradition that isn't weekly, every birthday, and any weekly one the voice budget drops ("No quiz this Thursday: something rarer is on"). The weekly ones get one line ("Plus the usual weekly ones…"), except in your first digest (day 7), which lists them all so you learn the week's shape.
- **A season line** on the Sunday before a new season starts (days 91, 182, 273, 364).
- **A quiet week** has its own short form.
- **Picking:** one variant per section, seeded by the week, so the same week always reads the same.
- **What it needs from the traditions engineer:** a way in. That could be a small baked block, or reading the `.mail` file in `content_gen.py`, or copying it by hand. There's also a place name for each tradition (the first `where` line's room name, or a pool name from the table in the file), and the `eventsOn` list for days d+1 to d+7. It also needs the device engineer's Mail to show a list (one line per item). Nothing in the game reads the file yet; `trad_parse.py` and `content_gen.py` ignore it (they read only `*.trad`).

## Checks
- `python3 plans/trad_parse.py`: 9 traditions OK.
- `python3 lines_check.py`: the texts pass (lengths, tones, placeholders, reading ease 87-92). It fails only because the game file's baked block is out of date, and I may not touch the game file. Run against a scratch copy baked with `content_gen.py`, both checks pass.
- `events_check.py` on that baked scratch copy: see the report to the traditions engineer.
