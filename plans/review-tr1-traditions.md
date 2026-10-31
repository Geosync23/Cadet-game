# TR1: ship traditions review (starts and triggers)

Reviewer TR1 (session_014zyJYMx26ZwoJgqt2dLUYL), for lead 47, patch 0.99.5. Review only: nothing in the game changed.
Base: claude/staging-0994 8976965e (0.99.4 candidate), game sha256 a01d1a4c...bc4a (checked).
Branch: claude/p995-tr1 (this page and plans/tr1-probes/).

The user's ask (note 19): "Spice shelf supper doesn't do anything. Doesn't trigger. No one to click on. Hire a reviewer
whose sole task it is to analyze ship traditions. Especially their starts and triggers." Also notes 8, 10 and 16.

## In plain words

- **Spice shelf supper** really has nobody to tap. It never got a "Tap to join" entry, so there is no star over
  anyone, no arrow and no tip; you only "join" by standing in the mess for 5 minutes, and Brennan's guessing game starts
  about 23 minutes late (she is still cooking) and her guess card opens at 18:53 only if you're still there.
- **The same gap is in about 25 other traditions.** Each has a named host but no Tap to join, so you can walk in, tap the
  host and get only their ordinary chat. The user's own rule (quoted in the comet's code, 0.93.2-c.2) is "every
  gathering: a host you tap, a fitting pose, words only they say". Worst are the ones where something is meant to happen
  for you: your new hand's tea (Day 5), Four weeks aboard (Day 26), Six weeks aboard (Day 42, Zeke's tea, while One week
  aboard has it), Twelve weeks aboard, Open door (Calder's weekly tea), and the 0.92.6 new ones (Tool night, Route night,
  Card night, Garden walk, Window sketching, the spoon band, Worst joke night, Open house).
- **When two traditions with Tap to join run at once on one deck, only the first gets its star and arrow**, even if you
  are standing in the other one's room (Playlist duel, Day 57, while Book circle runs on the same deck).
- **Note 8** (Name on the beam): the place you stand to paint was never moved when your name moved (0.92.3); you stand
  about 1.4 m west of your name, and two watchers stand right under it.
- **Note 10** (Tea and biscuits): the tea corner is 5 tiles; its standing tea spot is the doorway tile, filled almost all
  of 13:00-13:50, so you can't get out. Two seats are used; the third person stands at the door.
- **Note 16** (health check): Rina's whole scene was written and is in the game, but nothing ever opens it.
- Everything starts on its day and time, and the Mail the evening before is sent for every one (events_check, 35 days
  plus the year's special days: EVENTS CHECK OK on the base).

## How it was checked

1. **On paper:** `events_check.py` on the base for 35 days (plus Days 36-364 samples): every tradition due on exactly its
   days, people planned to its places, Mail the evening before once each, decor on the deck, the voice budget. Result:
   **EVENTS CHECK OK**. Notes only (nobody went: lineCeremony Day 7, vesselChain/vesselArrival Day 28,
   crossingBackCeremony Day 35, rec-float-hour Day 24; these are ship-wide events whose people go by meeting, and the
   real-game sweep shows people there).
2. **In the real game** (`plans/tr1-probes/sweep.py`, read with `sweep_read.py`): for every tradition and ship-wide
   gathering, its first showing (Days 1-35; Days 36-364 for the later ones), a fresh game, you placed in its biggest room
   on its deck 6 minutes before the start. At +12 minutes: how many are there for it and at its places, the join offer
   (`TJ_NOW`: who leads, the star over them, the arrow and tip), then a tap on the leader (else the host, else anyone
   there): did it join, what you're doing, any card; then a jump to 5 minutes before the end and on to 8 minutes after:
   still there, still joined. 104 traditions and gatherings. Raw lines: plans/tr1-probes/results/.
3. **Focused probes:** `spice_probe.py` (Days 2, 9, 16, and a copy with a join added), `tea_probe.py` (note 10, Day 3),
   `beam_probe.py` (note 8, Day 1, phone size), `inventory.py` (who hosts, who goes, joinable or not, Days 1-365).

Limits: one showing each; a skip to near the end (the ship's clock jumps, so your own activity ends there); the sweep
counts speech bubbles only roughly in its first half (a few speakers aren't named). Two browsers at most.

## The findings, worst first

Ranks: **BROKEN** (doesn't trigger, nobody to tap, or the promised moment never comes), **WRONG** (people stand
wrong, trap you, overlap, against the design), **ROUGH** (looks or reads off). Lines are on the base 8976965e;
`python3 tools/section.py --where LINE` names the section. Section 18 (ship events and traditions) is the
traditions engineer's; 4d (places) the deck architect's; 14 (schedules) the sim engineer's; 21 (arrival) onboarding's.

### How Tap to join works (so the fixes make sense)

A tradition can be joined by a tap only if it has an entry in `TRAD_JOIN` (section 18, line 45877; more are added
later with `Object.assign(TRAD_JOIN, ...)` at 46966, 47808, 47830, 48539 and single ones at 46649, 48351, 48485).
`tradJoinable(e)` (45909) is false without one. Then, once a ship minute, `tradJoinMinute` (45927) picks the tradition
on now on your deck and its leader (`TJ_NOW`): that gives the star over the leader (`tradJoinFrame`), the arrow
(`setGoal`) and the tip "Tap X to ...". A tap on anyone (`tapCrew` -> `tradJoinTap` 45989 -> `tradJoin` 46000) joins you
and starts your activity. Without an entry the only way in is `eventsPlayer` (45796): stand in its room for 5 ship
minutes and you are joined with one toast (its "thanks" line), nothing else. The 0.93.2 ones (`T932_IDS`, `t932Join`
48560) show the host's own line on a card first, then the activity: the shape that works best in the sweep.

### 1. Spice shelf supper (note 19): BROKEN

- Tuesday 18:15-19:15, the mess; 23-32 go (they eat dinner there). No `TRAD_JOIN` entry, so no star, arrow or tip at
  any minute; a tap on Brennan at 18:40 gives her ordinary chat (Days 2, 9, 16 in the game).
- You are joined silently after 5 minutes in the mess (18:21: one toast "Brennan sets out supper...").
- Brennan's scene (`spiceFrame` 48430, FX17, 0.92.6 item 15) runs on fixed minutes (`SPICE_AT` 48424: open 18:32,
  card 18:53, end 19:02), 17 minutes after the start. She's held at the shelf (`crewHold`, `3-spice-host` 48463) only
  from 18:29, walks out of the galley, and speaks only once settled (~18:38): her opening, the first jar and the first
  guess all appear in the same frame. Your guess card (`spiceCard` 48453) opens at 18:53 only if you were auto-joined
  and are still on Deck 3. From 18:15 to 18:38 nothing visible happens.
- Tried in a copy (`results/spice-with-join-day9.txt`): one `TRAD_JOIN` entry gives the star and "Tap Chef Brennan to
  guess the spices", and the tap joins and seats you. But then Brennan leaves the shelf (spot empty from 18:42) and her
  last two jars and the reveal never come. The fix must keep her held through the tap.
- Fix: (a) `TRAD_JOIN['spice-shelf-supper']` with host brennan, pose `sit:talk`, verb "guess the spices"; being a meal,
  the tap seats you at a free mess seat with your dinner (its `meal: dinner`). (b) Hold Brennan at the shelf from the
  start (18:15) and time her lines from when she arrives, a few minutes apart, all done by about 18:45. (c) Your guess
  card on the tap once the jars are named (else after the last one), not at a fixed 18:53, and still offered after a
  reload (`SPICE.joined` isn't saved). (d) Words: jar lines picked by position, not at random by day ("Last dish..."
  came first); capitalise `{spice}` at the start of a line ("black pepper in the sauce"); a guess never names its own
  speaker ("That's Dr. Sato's", said by Sato). (e) Design doc lines 499 and 516: Spice shelf supper becomes tap to join.

### 2. Your own milestones, and Open door: BROKEN

Each is about you, has a host, and gives you nothing to tap and no moment:
- **New hand's tea** (your first Friday, Day 5, 18:40, Works; Calder): it replaces the Works Friday tea that day, and
  Works tea has Tap to join (Calder, "wipe tools over tea") but the new hand's tea has none. You stand there; 4 bubbles.
- **Four weeks aboard** (Day 26, 18:40, the cake; Calder): no tap, no card.
- **Six weeks aboard** (Day 42, 17:15, the bow lounge, Zeke's tea): no tap, no card. One week aboard (Day 7) has both
  (`TRAD_JOIN['one-week-aboard']` 48351 and Zeke's `week1.zeke` card): the six-week one was never given them.
- **Twelve weeks aboard** (Day 84, 17:30, the mess, Calder's toast): no tap, no moment.
- **Open door** (every Wednesday 16:40-17:50, the Works tea corner, Calder): no tap; in the game only 1 person there at
  +12; on paper 3 of the 15 who mean to go fit (the corner's 3 places, the same as note 10). The design calls it
  "end-of-shift tea with the Chief"; you get nothing from her.
- Fix: a `TRAD_JOIN` entry each with the host (Calder; Zeke for six weeks) and a card of their own words, the way One
  week aboard does it (`week1Card`), or the 0.93.2 shape (`T932_IDS` + `t932.<id>.join` line). Open door also needs
  room: hold it in the Works bay by the tea corner (stand places), not only the corner's 3 places.

### 3. The 0.92.6 new traditions (`P926_NEW`, line 9720): BROKEN

Tool night, Route night, Card night, Garden walk, Window sketching (and its second showing), the spoon band, Worst joke
night and Open house each have a host and a promise in their Mail ("name each tool with your eyes shut", "a pin for
everyone: where will we be in seven days?", "we make cards for the birthdays"), and none has Tap to join, a card or an
activity. People come (4-28 at their places), the host talks a little (3-4 bubbles), a tap gives the host's chat.
The 0.93.2 new ones (scone morning, coffee trials, jar day, five-minute skills, whodunnit club, windowsill herbs,
sounds from home, row for the board, playlist duel, beginners' guitar, seed packet day, midnight toast) all work: star,
arrow, the host's line on a card, then the activity. Fix: give the 0.92.6 eight the same shape (a `TRAD_JOIN` entry
each, added to `T932_IDS`, and a `t932.<id>.join` line from the writers); Garden walk as a walk (`act: 'walk'`, like the
lap). Six weeks and twelve weeks are also in this set (see 2).

### 4. Off the Tern: WRONG (against the design)

Design doc line 519: "it's in your Schedule with Mail the evening before, and you can tap to join". There is no
`TRAD_JOIN` entry: no star, no tap (Day 21 17:35, 8 at its places). Fix: an entry with the Works hand's greeter (Zeke)
or Raman as host, pose talk.

### 5. A second tradition on the same deck hides the first one's star: WRONG

`tradJoinMinute` (45927) takes the first joinable tradition on your deck with a leader and stops (`break`), even if
you're standing in another one's room. On paper, Days 1-120 (`followups.py`): every Saturday afternoon on Deck 3
(Cook-along or Jar day 15:30 hides the Tiles ladder; the coffee trials hide Cook-along), Book circle hides Playlist
duel (Days 57, 85, 113, Deck 4), the tasting table hides Whodunnit club (Day 66). In the game (Day 57): standing in
the music room, no star and no arrow for Playlist duel; the arrow, if any, points to the other room. A tap on someone
there still joins (it goes by what that person is doing). Fix: in `tradJoinMinute`, prefer the tradition whose rooms
hold you (`e.rooms.has(here)`), then the nearest; or keep one `TJ_NOW` per tradition on the deck.

### 6. Name on the beam (note 8): WRONG

- In 0.92.3 (item 23) your painted name moved from `BEAM.yours` (along 3.6) to `BEAM.slots[0]` (along 4.98, section
  4d, lines 7726-7736; `nameYours` 8368), but the place you paint from, `5-beam-1` (xy [13.6, .75], line 7755), stayed
  where the old name was. In the game (Day 1, phone size): your name's centre is at x -7.02 (from -7.62 to -6.42); you
  stand at x -8.40, about 1.4 m west of the centre and 0.8 m past the name's west end.
- The watchers `5-beam-2` (x -7.50) and `5-beam-3` (x -6.50) stand right under the name, so their bubbles and the
  star cover it when it goes up (screens at 390x844: `plans/tr1-probes/results/beam_*.png`).
- Fix (section 4d, deck architect; owner review): move `5-beam-1` under slot 0 (xy about [14.98, .75], tile [14, 0];
  check that tile is free) and turn the watchers' faces to the new spot (worked out from 13.6 at line 7757). Slide
  `5-beam-2..5` off the name's span (x -7.6 to -6.4): east of about -6.2 or west of -7.8, or a row further back.
  `beamFloorTap` and `padBeamOn` read `5-beam-1`'s spot and follow by themselves. Later hands (`nameNew`, slots 1-3,
  Basil on Day 22) paint at the same `5-beam-1`; check theirs too.

### 7. Hosts who don't come: ROUGH (sometimes WRONG)

On paper the host isn't among those going on some showings: Gym club Day 8 (Rina is gardening; in the game Saruth
leads it and the tip says "Tap Saruth to join Gym club"), Sunrise stretch Days 8, 12 and 15 (Rina), Pick-your-own
(Tove, every week; Luca leads), Bread day, Cook-along and Jar day twice each and the tasting table four times (their
hosts are on duty in the galley, which `tradJoinMinute`'s "host on duty nearby" rule covers: the game showed Brennan
leading). Winner stays on (Pell) on 4 Sundays. Fix:
the planner sends the host when they're free (a host is "always" in `who`); if they're on duty, the "host nearby" rule.

### 8. Rough edges in the join itself: ROUGH

- The join toast says "About 46 minutes; walk away to stop" for a 30-minute Sunrise stretch joined 13 minutes in
  (section 15's toast uses `taskMins(TJ_MINS)`, not the tradition's end). Say "until 07:00" instead.
- Two toasts on joining (the join notice, then the activity's start toast with the same words), 1 minute apart.
- The star isn't on screen on some (garden hour, book circle, open lab, the bow lounge ones): it was off camera, not
  missing; the arrow points the way. Fine.
- Still there after the end: Midnight toast (4 at 23:38), Founding Day, Worst joke night: within the 25-minute linger.

### 9. The rec deck's hosted ones: ROUGH

Dawn swim (Rina), Wall night (Tomas), Paddle club (Holt), Float hour (Oduya), Slow stretch (Nandakumar), the regatta
(Holt), Sim night (Raman), Winner stays on and the Lightdisc Cup (Pell): each has a host and no Tap to join. You join
by being there 5 minutes; the activity is the rec deck's own (the pool, the wall, the kayaks, the court). Two newer
rec ones do it right (`rec-lamplight-paddle`, `rec-ring-the-bell`: `TRAD_JOIN` entries in the 0.93.2 block at 48539, and
`t932Join` starts the rec activity for an entry with `rec:`, 48566). Fix (lower priority): the same for these nine. Also: Talent night (the Friday one, Dahl) has no act
card while the rec deck's Talent night has one; Tap night (bar, no host) and Midtour (Oduya's letter to yourself)
promise something that isn't there.

### 10. Tea and biscuits, 13:00 (note 10): WRONG (traps you)

- The Works tea corner (Deck 5 room `t`) has 5 floor tiles: [21,0], [21,1], [22,1], [23,1], [23,2]. Its three places
  (section 4d, lines 4727-4729): `5-tea-1` seat at [23,0], `5-tea-2` seat at [21,0], and `5-tea-3`, a standing place
  on [21,1], which is the doorway tile (the way in from the Works bay at [20,1]).
- The 13:00 tea (section 14, line 10841: `take('leisure', [[5, 'lounge-seat']], 15 min, wait 8)`, 4 staggered
  slots): in the game (Day 3, you in the corner 12:52-13:55) people do sit on the two seats (Calder, Silva, Quist), but
  someone stands on the doorway tile almost the whole hour (Asha, Halloran, Volkov, Salo in turn), and everyone going
  to either seat walks through it. That's "they just walk up to it" and "you can't get round them". A tap-to-walk
  squeezes past settled crew (`squeezePath`), never walking ones; walking with the stick or keys doesn't squeeze.
- Fix: keep the doorway clear: leave `5-tea-3` out of the 13:00 tea (two at a time, the rest wait in the bay or go back
  to work), or move the standing place to [23,2]. `5-tea-3` is also the promotion cake's and CQ's spot (lines 63597,
  64679, 67554): moving it moves those; their owners review. Open door (see 2) uses the same 3 places.

### 11. The new-crew health check (note 16): BROKEN

- Rina's whole scene was written and is in the game (`MEETINGS_BAKED.introHealth`, line 43207: "You're my two
  o'clock. Sit. Arm out. Don't touch anything blue..."), but nothing opens it: the Day 2 beat `d2-health` (section 21,
  line 55004) has no `meeting:` and `INTRO_MEETINGS` (54978) has no `introHealth` entry (compare `d2-solo` and
  `introSoloJob`). Keeping the appointment (within 2.2 tiles of its place, or a tap on Rina: `apptTapKeep` 10271,
  `tapCrew` 71260) gives a toast "Kept: Rina is seeing you now" and her ordinary chat.
- Fix (the user: "make it like a ship tradition: tap the doctor and a moment starts"): add `introHealth` to
  `INTRO_MEETINGS` (cast ['rina']) and `meeting: 'introHealth'` to `d2-health`; when a tap keeps a check-up with Rina,
  open the card at once; and a star over Rina while it's due (from 13:58), like the traditions' marker. Title stays
  "New-crew health check" (note 11). Onboarding's seat (OB2).

### What works (checked in the game)

Every tradition starts on its day and time (paper, 35 days and the year's special days; the game agrees on every one
visited). The Mail the evening before goes once for each (events_check). Every tradition on Days 1-120 is on the
Calendar at its right time (`calendar.py`). With Tap to join, all 45 or so do the right thing: the star over the leader
from the first minute, "Tap X to ..." with the arrow, a tap joins and starts the activity (a machine, a bed, a seat, the
walk), cards where they belong (quiz, the swap meet, One week aboard, the tasting table, First Light, the 0.93.2 hosts'
lines), and everyone leaves within the linger after the end. The comet's four gatherings and the Veyli farewell,
parts chain and engine lights work the same way.

## Every tradition, one line each

Day, time, where: the showing visited. "There at +12": people there for it on the deck 12 minutes in (and at its own
places). "Join offered": the leader `TJ_NOW` named (no = no Tap to join). "What you got": your activity and any card.

| Tradition | Day, time | Where | There at +12 (at its places) | Join offered (leader) | Tap on leader/host | What you got | Status | Note |
|---|---|---|---|---|---|---|---|---|
| card-night | D73 19:30-20:30 | Deck 4 room j | 12 (12) | no | oduya: nothing | - | BROKEN | 0.92.6 new: no tap, nothing to make (see 3) |
| four-weeks-aboard | D26 18:40-19:30 | Deck 5 room w | 9 (9) | no | calder: nothing | - | BROKEN | your four weeks, the cake: no tap, no moment (see 2) |
| garden-walk | D63 09:15-10:00 | Deck 3 room G | 4 (3) | no | cruz-tove: nothing | - | BROKEN | 0.92.6 new: no tap; a walk with no Tap to join walk (see 3) |
| new-hands-tea | D5 18:40-19:30 | Deck 5 room w | 9 (9) | no | calder: nothing | - | BROKEN | your own welcome tea, Calder hosts: no tap, no moment; replaces Works tea, which has one (see 2) |
| open-door | D3 16:40-17:50 | Deck 5 room t | 1 (1) | no | calder: nothing | - | BROKEN | Calder's weekly tea: no tap, 1 there at +12 (paper: 3 of 15 fit), the 5-tile tea corner (see 2, 10) |
| open-house | D53 17:15-18:15 | Deck 2 room = | 10 (10) | no | ferreira: nothing | - | BROKEN | 0.92.6 new: no tap (see 3) |
| route-night | D38 19:30-20:20 | Deck 2 room K | 7 (7) | no | raman: nothing | - | BROKEN | 0.92.6 new: "a pin for everyone" not built; no tap (see 3) |
| six-weeks-aboard | D42 17:15-17:55 | Deck 3 room L | 5 (5) | no | torres-zeke: nothing | - | BROKEN | Zeke's tea for your six weeks: no tap, no card (One week aboard has both) (see 2) |
| spice-shelf-supper | D2 18:15-19:15 | Deck 3 room M | 28 (28) | no | brennan: nothing | - | BROKEN | no Tap to join; Brennan out ~23 min late; card only at 18:53 (see 1) |
| spoon-band | D64 17:45-18:30 | Deck 4 room j | 12 (12) | no | rossi-femi: nothing | - | BROKEN | 0.92.6 new: no tap (see 3) |
| tool-night | D29 17:45-18:30 | Deck 5 room w | 4 (4) | no | kovac-zainab: nothing | - | BROKEN | 0.92.6 new: the eyes-shut tool game is not built; no tap (see 3) |
| twelve-weeks-aboard | D84 17:30-17:55 | Deck 3 room M | 16 (16) | no | calder: nothing | - | BROKEN | Calder's toast for your twelve weeks: no tap, no moment (see 2) |
| window-sketch | D48 11:45-12:30 | Deck 2 room = | 5 (4) | no | alvarez-luca: nothing | - | BROKEN | 0.92.6 new: no tap (see 3) |
| window-sketch-2 | D104 11:45-12:30 | Deck 2 room = | 7 (6) | no | achebe-lumi: nothing | - | BROKEN | 0.92.6 new: no tap (see 3) |
| worst-joke | D81 17:15-18:00 | Deck 3 room L | 28 (27) | no | holt: nothing | - | BROKEN | 0.92.6 new: no tap (see 3) |
| cook-along | D6 15:30-16:30 | Deck 3 room K | 5 (5) | dlamini-lukas | dlamini-lukas: joined | tj | WRONG | some Saturdays its star hidden by the coffee trials (see 5) |
| name-on-the-beam | D1 17:05-17:40 | Deck 5 room w | 7 (7) | torres-zeke | torres-zeke: joined | - | WRONG | note 8: you paint 1.4 m from your name; watchers under it |
| off-the-tern | D21 17:35-17:55 | Deck 5 room S | 8 (8) | no | zamora-quinn: nothing | - | WRONG | design says "you can tap to join"; no Tap to join (see 4) |
| playlist-duel | D57 21:15-22:00 | Deck 4 room n | 6 (5) | no | oneill-imani: joined | t932.join | WRONG | its star and arrow hidden by Book circle on the same deck (see 5) |
| tiles-ladder | D6 15:00-16:30 | Deck 3 room L | 6 (6) | farouk-olu | farouk-olu: joined | tiles.ladder | WRONG | Saturdays: star hidden from 15:30 by Cook-along / Jar day (see 5) |
| whodunnit-club | D38 19:30-20:30 | Deck 3 room L | 8 (7) | achterberg-lars | achterberg-lars: joined | t932.join | WRONG | its star hidden by the tasting table from 20:00 (Day 66 on) (see 5) |
| midtour | D182 20:00-21:00 | Deck 3 room L | 29 (27) | no | oduya: nothing | - | ROUGH | Oduya: "write a letter to yourself" not offered; no tap |
| rec-cup | D28 11:30-16:30 | Deck 7 room = | 1 (1) | no | farouk-olu: nothing | - | ROUGH | Pell's bracket; no host tap |
| rec-dawn-swim | D2 06:15-06:45 | Deck 7 room P | 2 (2) | no | rina: nothing | - | ROUGH | host Rina, no tap (rec deck: use the pool) |
| rec-float-hour | D3 21:30-22:15 | Deck 7 room F | 2 (2) | no | oduya: nothing | - | ROUGH | host Oduya, no tap |
| rec-paddle-club | D3 18:30-19:30 | Deck 7 room K | 5 (5) | no | holt: nothing | - | ROUGH | host Holt, no tap |
| rec-regatta | D21 09:30-11:00 | Deck 7 room = | 10 (10) | no | holt: nothing | - | ROUGH | host Holt, no tap |
| rec-sim-night | D25 19:30-20:30 | Deck 7 room S | 7 (7) | no | raman: nothing | - | ROUGH | host Raman, no tap |
| rec-slow-stretch | D7 08:00-08:45 | Deck 7 room F | 5 (5) | no | nandakumar: nothing | - | ROUGH | host Nandakumar, no tap |
| rec-wall-night | D2 18:30-19:45 | Deck 7 room K | 4 (4) | no | tomas: nothing | - | ROUGH | host Tomas, no tap (use the wall) |
| rec-wso | D7 11:30-16:30 | Deck 7 room = | 2 (1) | no | halloran-emeka: nothing | - | ROUGH | Pell's board; no host tap (5-6 at it by 13:30) |
| running | D8 19:15-20:00 | Deck 3 room F | 6 (5) | saruth | saruth: joined | gym | ROUGH | Day 8 Rina (host) not there; Saruth leads (see 7) |
| sunrise-stretch | D5 06:30-07:00 | Deck 3 room G | 5 (5) | rina | rina: joined | tj | ROUGH | host not going some days (8, 12, 15) on paper; "About 46 minutes" toast for a 30-minute stretch (see 8) |
| talent-night | D152 20:15-21:45 | Deck 3 room L | 17 (15) | no | dahl-mira: nothing | - | ROUGH | Dahl hosts; no tap, no act card (the rec one has one) |
| tap-night | D5 20:00-22:00 | Deck 3 room L | 14 (9) | no | zielinski-oona: nothing | - | ROUGH | no host; the drink of the week not offered |
| beginners-guitar | D23 21:40-22:25 | Deck 4 room n | 6 (4) | larsen-hamid | larsen-hamid: joined | t932.join | OK |  |
| big-jigsaw | D21 13:00-15:30 | Deck 1 room O | 6 (6) | raman | raman: joined | tj | OK |  |
| birthday | D4 18:00-18:55 | Deck 3 room L | 34 (28) | no | sato: nothing | - | OK (turn up) | tap the cake (not a person) |
| book-circle | D15 20:15-21:30 | Deck 4 room + | 9 (9) | oduya | oduya: joined | tj | OK |  |
| bread-day | D7 07:00-07:50 | Deck 3 room K | 4 (4) | brennan | brennan: joined | tj | OK |  |
| captains-address | D5 16:00-16:50 | Deck 7 room A | 50 (50) | no | marrow: nothing | - | OK (turn up) | the address |
| coffee-trials | D27 15:00-16:00 | Deck 3 room L | 6 (6) | volkov-maeve | volkov-maeve: joined | t932.join | OK |  |
| cometCaptain | D22 21:30-22:40 | Deck 1 room O | 5 (4) | no | marrow: joined | - | OK | Officers and up only (you were a Cadet): by design |
| cometLounge | D22 21:30-22:40 | Deck 3 room L | 32 (30) | sato | sato: joined | tj | OK |  |
| cometScope | D22 21:30-22:40 | Deck 2 room J | 7 (6) | mori | mori: joined | ixStars | OK |  |
| cometStern | D22 21:30-22:40 | Deck 4 room j | 8 (8) | tomas | tomas: joined | tj | OK |  |
| crossingBackCeremony | D35 14:30-15:15 | Deck 3 room L | 28 (19) | no | holt: nothing | crossingBackOath | OK (turn up) | ceremony card |
| department-cup | D22 20:15-21:15 | Deck 3 room F | 11 (11) | vance | vance: joined | gym | OK |  |
| every-song | D69 17:15-18:05 | Deck 4 room n | 8 (4) | torres-zeke | torres-zeke: joined | tj | OK |  |
| farewell | D19 09:30-10:00 | Deck 5 room S | 14 (14) | saruth | saruth: joined | tj | OK |  |
| farewell-supper | D20 18:00-19:20 | Deck 3 room M | 13 (13) | no | kowalczyk: nothing | - | OK (turn up) | a meal |
| film | D6 20:00-22:00 | Deck 4 room j | 0 (0) | no | - | - | OK (turn up) | turn up |
| first-fruits | D134 18:15-19:05 | Deck 3 room M | 14 (14) | no | cruz-tove: nothing | - | OK (turn up) | a meal |
| first-light | D1 20:00-20:45 | Deck 3 room L | 18 (15) | raman | raman: joined | tj, firstLightCocoa.today | OK |  |
| five-minute-skills | D8 18:15-18:45 | Deck 3 room L | 19 (10) | nakamura-bilal | nakamura-bilal: joined | t932.join | OK |  |
| founding | D100 19:30-21:30 | Deck 3 room L | 44 (29) | no | marrow: nothing | - | OK (turn up) | turn up |
| garden-hour | D6 14:00-15:00 | Deck 3 room G | 5 (4) | cruz-tove | cruz-tove: joined | ixGarden | OK |  |
| garden-picnic | D20 13:00-13:50 | Deck 3 room G | 10 (10) | cruz-tove | cruz-tove: joined | tj | OK |  |
| gerald-clinic | D14 14:30-15:15 | Deck 3 room G | 2 (1) | cruz-tove | cruz-tove: joined | tj | OK |  |
| harvest | D6 09:30-11:30 | Deck 3 room G | 4 (3) | cruz-tove | cruz-tove: joined | ixGarden | OK |  |
| harvest-supper | D231 18:00-19:30 | Deck 3 room M | 16 (16) | no | cruz-tove: nothing | - | OK (turn up) | a meal |
| hull-lights | D24 21:00-22:00 | Deck 3 room L | 25 (19) | no | vance: nothing | - | OK (turn up) | turn up |
| jam | D5 19:45-21:15 | Deck 4 room n | 6 (4) | larsen-hamid | larsen-hamid: joined | tj | OK |  |
| jar-day | D20 15:30-16:30 | Deck 3 room K | 2 (2) | varga-tariq | varga-tariq: joined | t932.join | OK |  |
| knit-and-natter | D2 20:00-21:30 | Deck 4 room j | 8 (8) | torres-zeke | torres-zeke: joined | tj | OK |  |
| lantern-walk | D316 20:30-21:20 | Deck 3 room L | 29 (24) | holt | holt: joined | - | OK |  |
| lanternSupper | D13 18:00-19:45 | Deck 3 room M | 1 (1) | no | janssen-hugo: nothing | - | OK (turn up) | a meal, the storm |
| lap-of-the-wren | D7 20:30-21:15 | Deck 3 room = | 16 (15) | tomas | tomas: joined | - | OK |  |
| late-piano | D2 21:40-22:25 | Deck 4 room n | 6 (3) | no | marrow: nothing | - | OK (turn up) | listen |
| lineCeremony | D7 14:30-15:15 | Deck 3 room L | 37 (21) | no | calder: nothing | crossingCeremony | OK (turn up) | ceremony card |
| long-breakfast | D6 08:00-09:30 | Deck 3 room M | 5 (5) | no | brennan: nothing | - | OK (turn up) | a meal |
| market | D7 10:30-12:30 | Deck 3 room = | 9 (8) | ishikawa-orla | ishikawa-orla: joined | tj, swap.meet | OK |  |
| midnight-toast | D26 23:00-23:30 | Deck 3 room M | 4 (4) | garcia-greta | garcia-greta: joined | t932.join | OK | 4 still there 8 min after (within the 25-minute linger) |
| name-on-the-beam-new | D22 17:05-17:40 | Deck 5 room w | 8 (8) | no | torres-zeke: nothing | - | OK (turn up) | Basil's name: you watch |
| night-owls-cocoa | D27 22:30-23:30 | Deck 3 room L | 6 (6) | mensah | mensah: joined | tj | OK |  |
| observatory-night | D6 21:15-22:35 | Deck 2 room = | 6 (4) | sato | sato: joined | ixStars | OK |  |
| one-week-aboard | D7 17:15-17:55 | Deck 3 room L | 4 (1) | torres-zeke | torres-zeke: joined | tj, week1.zeke | OK |  |
| open-lab | D9 17:30-18:30 | Deck 2 room = | 14 (12) | sato | sato: joined | tj | OK |  |
| party | D14 19:00-21:00 | Deck 3 room L | 16 (5) | no | nandakumar: nothing | - | OK (turn up) | the storm's party |
| pick-your-own | D3 06:15-06:55 | Deck 3 room G | 3 (3) | alvarez-luca | alvarez-luca: joined | ixGarden | OK |  |
| postcard-night | D11 18:45-19:45 | Deck 3 room = | 9 (9) | eklund-leila | eklund-leila: joined | tj | OK |  |
| quiet-watch | D300 21:30-22:15 | Deck 1 room O | 7 (0) | no | dahl-mira: nothing | - | OK (turn up) | turn up |
| quiz | D4 20:00-21:30 | Deck 3 room L | 23 (16) | tomas | tomas: joined | tj, moment:quiz | OK |  |
| reading-corner | D7 16:00-17:00 | Deck 3 room L | 3 (3) | walsh-esme | walsh-esme: joined | tj | OK |  |
| rec-chiefs-talk | D8 19:00-19:45 | Deck 7 room A | 33 (27) | no | raman: nothing | talk.sato.ask | OK (turn up) | spoken talk; question card after |
| rec-talent-night | D21 19:30-21:30 | Deck 7 room A | 24 (22) | no | ferreira: nothing | rec.talent.you | OK (turn up) | act-or-watch card |
| rec-wren-talk | D25 19:00-19:40 | Deck 7 room A | 3 (3) | no | oduya: nothing | talk.tomas.ask | OK (turn up) | spoken talk; question card after |
| row-for-the-board | D51 19:00-19:45 | Deck 3 room F | 5 (5) | lindqvist-isak | lindqvist-isak: joined | t932.join | OK |  |
| saturday-run | D6 07:00-07:40 | Deck 3 room = | 4 (4) | nandakumar | nandakumar: joined | - | OK |  |
| scone-morning | D70 09:30-10:15 | Deck 5 room t | 3 (3) | halloran-emeka | halloran-emeka: joined | t932.join | OK |  |
| seed-packet-day | D27 16:30-17:15 | Deck 3 room G | 4 (4) | hart-ravi | hart-ravi: joined | t932.join | OK |  |
| sounds-from-home | D46 20:00-20:45 | Deck 4 room n | 6 (4) | vasquez-uma | vasquez-uma: joined | t932.join | OK |  |
| sowing | D6 11:45-12:40 | Deck 3 room G | 13 (11) | cruz-tove | cruz-tove: joined | ixGarden | OK |  |
| storm-stories | D13 21:00-21:45 | Deck 4 room j | 9 (9) | oduya | oduya: joined | tj | OK |  |
| sunday-story | D28 21:15-21:55 | Deck 4 room j | 8 (7) | holt | holt: joined | tj | OK |  |
| sunday-table | D7 18:00-19:45 | Deck 3 room M | 9 (9) | no | brennan: nothing | - | OK (turn up) | a meal |
| tasting-table | D3 20:00-20:45 | Deck 3 room M | 13 (13) | brennan | brennan: joined | tasting.table | OK |  |
| tiles-night | D2 20:00-21:30 | Deck 3 room L | 13 (11) | rina | rina: joined | tj | OK |  |
| vesselArrival | D28 09:20-09:50 | Deck 5 room S | 20 (20) | no | pell: nothing | - | OK (turn up) | the Veyli ship arrives |
| vesselChain | D28 13:00-14:00 | Deck 5 room S | 29 (26) | torres-zeke | torres-zeke: joined | tj, vesselRamp.bench | OK |  |
| vesselLights | D29 17:30-18:00 | Deck 3 room L | 33 (30) | saruth | saruth: joined | tj | OK |  |
| windowsill-herbs | D36 17:30-18:00 | Deck 3 room G | 8 (8) | janssen-hugo | janssen-hugo: joined | t932.join | OK |  |
| works-tea | D19 18:45-19:30 | Deck 5 room w | 9 (9) | calder | calder: joined | tj | OK |  |
| years-end | D364 20:00-21:15 | Deck 3 room L | 39 (31) | no | marrow: nothing | - | OK (turn up) | turn up |

Not visited in the game (switched on by a flag later in the game, none on in a new game): bridge-hour (bridge.invited),
rec-all-hands (rec.allHands), rec-lamplight-paddle and rec-ring-the-bell (rec.on), tasting-table-late, crew-welcome-tea,
storm rotations. On paper they are due on their days (events_check "Flagged traditions").

## Suggested order for the traditions builder

1. Spice shelf supper (1), with Brennan kept at the shelf after the tap.
2. One fix for many: a `TRAD_JOIN` entry, with the host's own line on a card (`T932_IDS` + `t932.<id>.join`), for the
   milestones and Open door (2), the 0.92.6 eight (3) and Off the Tern (4). The writers (SW seat) give one join line
   each; until then `t932Join` falls back to the plain join (48570), so the tap works on day one.
3. The hidden star (5): a few lines in `tradJoinMinute`.
4. Notes 8 and 10 (4d places, with the deck architect's review), note 16 (onboarding).
5. Later: the rec deck's nine (9), hosts who don't come (7), the toasts (8).
Each behind a switch, off = identical (cadet_test), and events_check, p926_check 15, the comet and Veyli parts of
bigevents_check, day_check on a Tuesday, a Saturday and Day 5 afterwards.

## Open questions for the user

1. Meals with a host (Spice shelf supper, the farewell, first-fruit and harvest suppers, the Sunday table): should all of
   them get a host to tap (the meal then served at your seat), or only Spice shelf supper, where something happens?
2. The rec deck's nine hosted ones (Dawn swim, Wall night and the rest): tap the host to join, like the comet's, or
   leave them as "just use the pool / wall / kayak"?
3. The tea corner at 13:00: two at a time (the third waits in the bay), or move the standing place to the far corner?

## Your answers and comments

(Write here, or answer on the lead's page.)
