# Handover: FX11 (the weekend traditions, after FX14; 0.92.5 item 16) → FX9

**Role:** builder under lead 34 (session_019RdVfeRPRiJpHGjKujZZJA). Reviewer RV13 (session_016ioWtxM6NJRV4Ck3ADwozc),
build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), words SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ), voice CS1
(session_01QcPAXHjQZ2HfZKMCTbaW9v), FX12 (session_01DfkfrfvdT2bW2Q1Y7b2AA5, the late-piano toBed rule and the birthday
hour). Read FX14's note first (plans/handover-fx14.md): how traditions, joins, places and the switch work.

## State (2026-10-24 ~22:40 UTC, FX11 at ~60% memory)

Branch **claude/p925-weekend** (from integration ba836359 = 0.92.4). On top of FX14's T1+T2 (9e840769):
- **53bf6de1 T3 Bread day + T4 The big jigsaw + the tj-acts fix + weekend_check.py** (build-table row "p925-weekend T3+T4").
- a commit: `evTagId` knows the 'cook' anim (else Bread day's kneaders, tag `ev-bread-day-cook`, don't count as at it);
  weekend_check: every weekend id has a join and each tap-join its activity; each tap-join ends by itself with its gain.
- merge of SW1's words (claude/weekend-words-sw1 cd1b6637 = 374a4765 + the bread/jigsaw join keys), re-baked (1d805955).
- Checks on the tip: see the last push's message to RV13/lead (check_fast, cadet_test switch-off vs 9e840769 ALL
  IDENTICAL on 53bf6de1; weekend_check). **Still to run with the switch on (a copy):** events_check, food_check
  (`1 7` style: a Sunday), day_check 7, deck_check. Not run yet by me.
- RV13 reviews T1-T4 together. T1+T2 was FIXES NEEDED only for the tj-acts bug, which this branch fixes.
- **SW1 is waiting for the sha** with bread-day.trad / big-jigsaw.trad on origin to write their words (mail kept from
  the pitch). Send SW1 the tip's sha; merge their next push and re-bake.

## What I built (all behind WEEKEND_ON; off = identical)

- **Bread day** `content/traditions/bread-day.trad` (k 467, Sun 07:00-07:50, `wake: 15`, host Brennan, anim cook,
  `where: 3 pool @bread-day`, `ties: decor breadDay`). Places `3-bread-1..6` (type event, round the galley's prep
  island: W 36,5 / 36,6, S 37,7 / 38,7, E 39,6, N 38,4), pushed in the Traditions engineer slot. DECK_DRESS `breadDay`
  (flour overlapping the island's steel top at .925, dough, four tins). Join `TRAD_JOIN['bread-day']`. If you joined:
  `SHIP.weekend.loaf = day` (saved as `save.weekend` only with the switch on; reset on new game) → `weekendDecor(now)`
  (added to eventsDress's list) draws `loafCard` (basket, loaf, "<name>'s loaf" card on the long table at M 8.7,4.0)
  06:30-10:00 the next day. Crew 4-6 a Sunday (Day 14's morning traditions all give way on that date: existing).
- **The big jigsaw** `big-jigsaw.trad` (k 468, Sun 13:00-15:30, host Vance, anim read, `where: 1 room Observation
  room: common-room`, `ties: decor bigJigsaw`): the puzzle (canvas texture, still picture) on the conference table,
  lid propped, dish of pieces; crew in the table's own seats; nothing new on Deck 1. TRAD_JOIN's new optional `mins`
  (tradJoin reads it: a turn of 20 minutes). onSim('tradition') with `x.you` → `hobbyCount('puzzle')`. Crew 6-10;
  2 on Winner Stays On / Cup Sundays (the rec deck takes the afternoon).
- **tj-acts fix** (FX14's T1+T2 too): section 18's loop that makes `PLAYER_ACTS['tj:<id>']` is now `tjActs()`, called
  where it was and again at the end of the weekend block (the weekend joins are added after the loop ran).
- **weekend_check.py** (new; switch on in a copy, ~6 min): each tradition on its day, none with the switch off, joins
  and their activities, each tap-join ends with its gain, Bread day's spots/decor/join/Monday loaf, the jigsaw's
  table/turn/hobby. Fails on 9e840769 (the joins line). Add it to the testing guide's round when the weekend goes on.

## Left for you (lead 34's list)

1. **Cook-along into the galley** (not behind the switch; separate small commit; the user: "Cook along tradition
   should be in the kitchen"). Today `cook-along.trad` (k 449, Sat 15:30-16:30, Lukas Dlamini) uses mess-seats + the
   6 standing spots `3-cookalong-1..6` at the pass (section 4, ~line 7681). Move its places into the galley: the six
   `3-bread-*` spots fit, but they're only pushed with WEEKEND_ON. Either push galley spots for cook-along always
   (`3-cookalong-*` moved, ids kept) or make the bread spots unconditional with an event tag both use. Keep time,
   host, words (adjust join.cook-along.notice/tip "at the galley pass" with SW1). Kitchen crew working dinner prep at
   15:30-16:30 need room (food_check). Check line failing on 0.92.4: participants in the galley (room K), not the mess.
2. **Attendance** (lead's ask): Night owls' cocoa (22:30) and the Sunday story (22:15) get 1-4; aim 5-8. Use FX12's
   shared toBed rule (crew whose bedtime falls in the window still come for at least 20 min): I asked FX12 where it
   will live; no answer yet. And/or raise odds. Every song: a couple of standing spots in the music room (it's capped
   at the room's 6 places; events_check says 11 wanting).
3. **RV13's host question:** on Day 6 the leaders were haddad-tamsin for every-song (host torres-zeke) and soto-marta for
   the picnic (host cruz-tove, "always"). Find whether the hosts are elsewhere (another event, shift) or missing.
4. **The Sunday story's chapters**: SW1's `content/banks/sunday-story.lines` has `story.sunday.1-.4`; wire Holt to read
   chapter ((week - 1) % 4) + 1 line by line (like the Friday address, `friAddressTick`, or a meeting).
5. **T5** decor on the days, head counts, perf numbers (rec deck and Deck 3 Sunday morning). **T6** the birthday hour with
   FX12 (no birthday within an hour of any tradition), design-doc (the eight weekend traditions, Mend-it morning
   parked as cut), DEV_NOTES, full checks.

## Gotchas

- Traditions are cached per day: after a change the planner reads, clear `SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear()`.
- A new crew anim on a tradition must be in `evTagId`'s strip list, or crew at it don't count as there.
- Joins added after section 18's load loop need `tjActs()` again.
- Test with the switch on: `sed "s/^const WEEKEND_ON = URL_FLAGS.has('weekend')/const WEEKEND_ON = true/"` into a copy.
- Never run more than two browser checks at once here (events/join checks time out loading).
- `pkill -f <check>` from a Bash call kills that call's own shell too (its command line matches): kill by pid.

## Open questions for the user

None new. The jigsaw's week-by-week fill (saved) is the large version; ask before building it.
