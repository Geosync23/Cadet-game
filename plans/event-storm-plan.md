# The ion storm: the event plan (version 1.1: the storm update, Days 11-15)

Event planner EP3, 2026-10-21. Branch `claude/event-plan-storm`, from `claude/event-plan-line` (7040dc8; build 0.64.6). Reports to lead 22 (session_01BGQCZLK6gYTnqu6mwZ61jB). **Planning only: the game is unchanged.**

- **The review:** ER2, claude/event-plan-review-2 69629c7, `plans/event-storm-plan-review.md`: PASS WITH FIXES (5 fixes, 2 nits). How each was taken is at the end.
- **The full page:** `plans/event-storm-plan.html` (with the answer form, `data-doc="event-storm-plan"`).
- **Screenshots:** `plans/event-storm-plan-shots/` (390x844, a new game, the storm's days as they run today).
- **What it builds on:**
  - the events plan v3.2 (claude/events-plan, section 2: the storm's changes and the 13 update items; the user's answers);
  - EV1's events base (claude/events-base 18f0d9d: F0a, F1a-c, F2 and F3a built, switched off; F0b, F2b, F3b, F4, F5, F7, F8 still to come);
  - the Fridays build brief (claude/fridays): Day 12's address is the regular one, with the storm at its heart;
  - EW1's storm lines, ready (claude/events-lines, `plans/events-ready/ionStorm/`);
  - the Crossing the Line plan (this branch, 7040dc8) as the model, and ER2's review of it, so the numbers here are measured, not assumed.
- **Order:** the events base, then **this storm update** (the base is switched on with it), then Crossing the Line, the comet and the visit.

## In short
- **Thursday Day 11 to Monday Day 15.** The storm already runs in the game (built before most of it). This update moves it a day later, gives it its new hours, makes your help count, adds the lantern supper and a small story, and fixes the 13 items the events plan found.
- **Thursday 14:00:** Calder's briefing in the Works bay, after the tea. The storm jobs go up when it ends, and the one you pick is held for you.
- **Friday 14:00, the front:** the jolt, the lights dip, the Captain's short banner. The bow lounge, the call booths and the rec deck close; the bridge goes on double shifts; comms go down. **16:00:** the Captain's regular Friday address in the auditorium, opened just for it.
- **Saturday:** the worst of it: blackouts deck by deck, storm stew, the surge at 11:20. **18:00-19:30, the lantern supper** in the mess by lamp light, about 55-60 people.
- **The story (recommended: A, "Sixty by lamplight"):** Brennan is off on Friday and Saturday, so Lukas Dlamini, from your old bunk room, runs her galley alone through the worst of the storm, and the lantern supper is his. The surge takes out four of his six rings. Your one choice: fix the range yourself, carry his question to Brennan, or tell him two rings is plenty. Brennan comes to the supper as a diner, and what she says depends on your choice.
- **Sunday 10:00, the all-clear** in the observation room: the Captain, Calder, Sato and Holt come in on their day off (and say so), Vance is on duty. Your commendation letter comes here, and the storm's result is settled. The booths reopen to a queue, and **the party** fills the bow lounge 19:00-21:00.
- **Your help counts:** left alone, a new game's storm comes out **bumpy** (measured). Fitting the ballasts, carrying the batteries up and drawing up the booth rota make it **smooth**.
- **Monday:** the afterglow, Calder's debrief at 18:00, Lap of the Wren at 20:30 led by Tomas. The event ends at midnight, so Tuesday's comet stands alone.
- **About 10 build turns** (the plan said 9-11), behind the events base's switch, off until the user's review.

## The story
Each option has a beginning, a middle where your one choice matters, and a payoff. All three use crew already aboard and the real rota (measured in a new game with the base switched on), and none touches anyone's later story beats.

### Option A: "Sixty by lamplight" (recommended)
The ship's own facts: Brennan's days off are Friday and Saturday (`offDays [4, 5]`), and `content/facts.md` already says "Lukas Dlamini covers for Brennan Fri-Sat". So the storm's two worst days fall on Lukas's watch, and the lantern supper is his. He's a galley junior, eight months aboard, from Port Halloran, dry, few words, and he cares about one thing above all (his card): "Brennan's galley not slipping on his watch". He sleeps in Bunk 1 (berth 5), where you started. On track you've moved to the officers' corridor on Wednesday (Day 10); the promotion can be delayed, never failed, so a slower player is still his bunkmate. **His lines read the save** ("since you moved" only if you have; "bunkmate" if you haven't), never a rank or day assumed.

- **Beginning, Friday Day 12, 17:00-20:30, at the servery.** The front hit at 14:00. Lukas is on the galley line through dinner (measured: cooking 16:50-20:30, tea at 20:30). The moment opens when you're near him: at the servery (the queue 17:00-18:00 is the natural place) or in the galley, both open to you. He says a number, the way he does: *"Sixty."* Covers. Tomorrow. The lantern supper, by lamp light, on her day off. Three replies:
  - "I'll give you a hand tomorrow." (practical; sets `storm.lukas.promised` and holds the lantern job `stormLanterns` for you)
  - "She left you in charge for a reason." (cheer; *"She left me a list. Eleven of the twelve lines say don't panic."*)
  - "What's the worst that could happen?" (he just says the number again)

  If you don't meet him before he goes to his bunk (20:47), he sends a short Mail at about 20:50: *"Lantern supper tomorrow. If you've got hands, I've got onions."*
- **Middle, Saturday Day 13, the galley, 14:30-17:00.** At 11:20 the surge goes through the ship (a felt moment). When Lukas comes on at 14:30 (measured) the range is down to two rings of six: *"Surge took four rings. Works has a list. I'm near the bottom. Sixty bowls on two rings. Or I go and knock on her door."* Your one choice:
  - **"I'm Works. Let me look at it."** (any rank: you're a Works hand either way) A story job is held for you: reset the galley range (`stormRange`, one stop `{ deck: 3, machine: 'range', mins: 20, tag: 'reset' }`, which resolves to `3-range-1` at its panel `3-range-1-panel`, the only range on Deck 3). Done before 17:00, he has all six rings.
  - **"Ask her. I'll go."** You carry his question to Brennan, wherever her own plan has her (on Deck 4 that afternoon: her cabin 4-05 or a bench; measured). She won't come in (*"It's his night."*) and sends one line back: *"Tell him: one pot, low and slow, lid on. And tell him it's his galley tonight."*
  - **"Two rings is plenty. Stew's one pot."** He nearly laughs. His aunt was a pilot (his card) and cooked on two rings in a cockpit for twenty years. He makes her stew.

  If you're not there, nothing is lost: he manages on two rings, his way, and the supper goes on.
- **Payoff, Saturday 18:00-19:30, the lantern supper.** The mess by lamp light, about 55-60 people. Brennan comes as a diner: she's off, and her own day already has her at dinner in the mess 18:05-18:32 (measured); the supper's data gives her a pull of 1 so it stays so. She eats every bit and says one thing, by your choice:
  - you fixed the range: *"Six rings on a storm night. Somebody's been in my galley with a spanner."* A nod to you, then to Lukas: *"Good."*
  - you asked her: *"Low and slow. He listened. Nobody listens."*
  - his way: *"That's not my stew."* A pause. *"Make it again on Friday."*

  When the last bowl goes out, Lukas says a number (the covers), and that's all he says.
- **Sunday.** Brennan's back at 04:50. The crew retell it (an afterglow line: *"Lukas ran the lantern supper on two rings. Or six. Depends who you ask."*). A storm lantern stays on the galley pass from then on (a small trace, one prop on Deck 3).
- **If you skip all of it,** the supper still happens, Lukas still runs it, and Brennan still eats it (her "his way" line). You hear about it on Sunday.
- **No spoilers:**
  - Lukas talks only about tonight's supper and Brennan's galley. Nothing of his own worry theme (`notgood`: a mistake on an old ship, checking his work twice), nothing about the person he married (unnamed in facts.md) or his count of days.
  - Brennan's lines never touch her own story: no restaurant, fire, soup, blue sage, Hesper Dock, her book of favourite dishes or leaving, **and nothing that hints at handing the galley on** (no "he's ready", no "one day this'll be yours": her later beats keep that question). "His galley" is for tonight only.
  - Calder never says "well done" (her arc's payoff).
  - Nothing about the Veyli or the visit.
- **What it needs** (about one turn):
  - three moments (section 20c, like `moment:quiz`): Friday with Lukas, the Saturday galley choice, Brennan at the supper; each reads saved flags (`storm.lukas.promised|fixed|asked|own`), never the planner;
  - the range job `stormRange`: one stop `{ deck: 3, machine: 'range' }` (the kind on Deck 3, as the ballasts job writes `machine: 'lights'`; `eventStopOf` reads a kind or the middle part of an id, so `'3-range-1'` itself wouldn't resolve), held for you from the moment's reply, the way `calderStorm`'s `job:` works; the galley's own cooking isn't changed (the four dead rings are words);
  - the errand: a stop at Brennan found from her own plan, like the Line's mug for Tomas;
  - Brennan's pull of 1 at the supper (the event's data, not your choice: the planner never reads your reply);
  - the lantern trace on the galley pass (deck architect, 1 draw call);
  - the lantern job `stormLanterns` (built in S5);
  - Lukas's Mail; about 30-35 lines from EW1.

### Option B: "First in the queue" (not recommended)
Femi Rossi: a Works junior two months aboard (your department), from the Tevan belt, who calls his younger brother every week (the `calls-home` habit, measured) and works Friday to Sunday (off Monday and Tuesday).
- **Beginning, Friday 14:00:** comms go down with the front. At the Works tea he tells you his brother starts at the belt's flight school on Monday, and he promised to call on Sunday.
- **Middle, Saturday:** you choose: draw up the booth rota and put him first; ask Vance for one line on the bridge's storm channel (by the book: *"Storm traffic only"*); or help him write it, to go out the moment comms are back.
- **Payoff, Sunday:** the booths reopen to a queue of about 39 people (measured: 39 owed a call, 4 booths). With the rota he's first; otherwise he waits until mid-afternoon, in the middle of his shift (his real call at 14:57). On Monday he tells you what his brother said.
- **Weaker:** the payoff happens inside a booth, off screen, and lands in a Mail. Waiting for news from home is close to Rina's beats, already told.

### Option C: "What the storm is called" (not recommended)
Dr. Sato is off on Saturday and Sunday, but spends Saturday afternoon and evening in the observation room anyway (measured: 12:44-14:10 and 18:48-20:16), and in EW1's all-clear she says *"You don't sleep through the end of a storm."*
- **Beginning, Friday's address:** *"Dr. Sato says it's bigger than a moon. She's thrilled."* That evening she asks for a hand with the readings.
- **Middle, Saturday evening, the observation room:** you read the hull meter by the window while the storm's heart goes past in violet. She lets you name the storm for the log: three names.
- **Payoff, Sunday's all-clear:** Sato says the name in front of the room, and the crew use it afterwards.
- **Weaker:** quiet, one person. It clashes with the lantern supper (18:00-19:30), and naming things is Sato's own thread two days later, at Tuesday's comet (she "named three comets").

**Recommended: A.** It's true to the rota and to facts.md (Lukas covers for Brennan Friday and Saturday). It gives a guarded friend something he wants: to keep her galley from slipping on his watch. It puts your choice where your trade is (a Works officer, a dead range) or where your heart is (carry the question, or trust him). It pays off at the storm's big crowd moment, the lantern supper, in front of everyone, and it still works if you miss it.

## The days at a glance (a new game, Day 0 the arrival, Day 1 a Monday; you work Thursday, Friday and Monday)
| Day | What happens |
| --- | --- |
| Thu 11 | **Warning** from 06:00 (Calder's Mail). The team job 09:30-13:00 and the tea as built. **14:00 Calder's briefing**, Works bay; storm jobs go up at 14:12, your pick held. Nothing from the storm 17:00-18:30 (the officer ceremony, 17:15). Postcard night and the quiz as usual. |
| Fri 12 | **14:00 the front** (onset): jolt, lights, banner; the bow lounge, booths and rec deck close; double shifts on the bridge; comms down. 15:30 the short Friday. **16:00-16:50 the Captain's address** in the auditorium (opened for it). Story A begins at dinner. |
| Sat 13 | **06:00 escalation**: blackouts, storm stew, stay in. **11:20 the surge.** Story A's choice in the galley from 14:30. **18:00-19:30 the lantern supper** (mess). |
| Sun 14 | **10:00 the all-clear** (observation room; four of five called in): commendation, result settled, rec deck and booths reopen, the booth rush. The market, Winner Stays On, reading corner, Sunday table as usual. **19:00-21:00 the party** (bow lounge). Talent night moves a week; Lap moves to Monday. 22:00 afterglow. |
| Mon 15 | Afterglow. **18:00 Calder's debrief** (Mail). **20:30 Lap of the Wren**, led by Tomas. The event ends at midnight. |
| Thu 18 | The commendation summons (F1c), at an hour clear of Pillar 5's training. |

**The phases:** `warning [0, 360]`, `onset [1, 840]`, `escalation [2, 360]`, `resolution [3, 600]` (clears), `afterglow [3, 1320]` (clears), **`days: 5`** (was 6: the afterglow now ends Monday midnight, so the comet on Tuesday Day 16 stands alone, and the shorter afterglow the user asked for). `pause: ['onset', 'escalation']`, **`keep: ['birthday', 'captains-address']`** (Day 12's address happens). `eventDay` is true on Days 12-14 (measured on the base). `EV_CALENDAR`'s `ionStorm` row is already day 11 (measured: `eventDueDay` gives 11 with the base on, 10 with it off).

## Checked in the game (0.64.6 with the events base 18f0d9d switched on, a new game, 390x844)
- **Aboard:** 76 on Days 10-11 (74 crew, Envoy Saruth and one other guest who leaves after Day 11), 75 from Day 12 (74 crew and Saruth). 69 crew are on the day shift, 17 on nights (of 86 on the roster; 12 crew are away).
- **Who works (of 74 crew):** Day 11: 57 (off: Vance, Zeke). Day 12: 61 (off: Brennan, Zeke). Day 13: 45 (off: the Captain, Calder, Sato, Holt, Brennan, Rina, Raman). Day 14: 45 (off: the Captain, Calder, Sato, Holt, Rina, Raman; Brennan and Vance work). Day 15: 57 (off: Tomas). **You** work Days 11, 12 and 15 and are off Days 13-14.
- **The galley on Saturday:** Brennan and Esme Walsh off; Lukas Dlamini (head of the line 04:50-09:00 and 14:30-20:45), Ivo Madsen, Tariq Varga, Tamsin Haddad and Agnes Sorensen (one week aboard) on.
- **At each moment (crew aboard, by what they're doing):**
  - Thu 14:00 (briefing): 39 at work, 24 free, 11 asleep; 5 crew in the Works bay at 14:05.
  - Fri 14:00 (the front): 43 at work, 19 free, 12 asleep. Fri 16:00: 46 at work, 25 free (today the day shift works to 17:00; the Fridays plan stops it at 15:30).
  - Sat 11:20 (the surge): 28 at work, 35 free, 11 asleep. **Sat 18:30 (the supper's slot): 9 at work, 65 free, none asleep; 25 already in the mess for dinner.**
  - Sun 10:00 (the all-clear): 29 at work, 34 free, 11 asleep. Sun 19:30: 69 free, but 32 are on their way to the rec deck's talent night and only 17 are in the bow lounge (so moving talent night matters).
  - Mon 20:30: 69 free.
- **The all-clear's cast today:** at 10:00 on Day 14 nobody is planned in the observation room (the Captain is in the music room, Calder in the gym, Sato at a desk on Deck 2, Holt in his cabin): the base's known gap, fixed by F0b.
- **The Captain on Friday:** on the bridge's double shift 08:03-20:30 (measured), so she must step off it 16:00-16:50 for the address, **and so must Vance** (command is on double shifts too, and the address's cast is Marrow and Vance).
- **Traditions the storm pauses (measured):** Day 12: Works tea 18:45, the jam 19:45, tap night 20:00 (bow lounge). Day 13: long breakfast 08:00, garden hour 14:00, the Tiles ladder 15:00, cook-along 15:30, film night 20:00, observatory night 21:15. Not paused: Day 11's quiz 20:00 and postcard night 18:45 (the warning); Day 14 from 10:00: the market, Winner Stays On, the reading corner (16:00, bow lounge), the Sunday table (18:00), talent night (19:30, rec deck), Lap of the Wren (20:30). Day 15: running 19:15, book circle 20:15.
- **The result, left alone (a new game, skipped through Days 11-14):** blackout 117 minutes (Deck 1 07:10-07:56 and 13:13-13:33 on Saturday, Deck 6 09:06-09:57 on Sunday; **none on Deck 3**), spoiled 18, bridgeHungry 12, calls 7.8 hours. Bands: bumpy, bumpy, bumpy, rough, so the storm comes out **bumpy** (`eventBand` averages the four). The calls queue: 39 owed a call, 4 booths, 40 minutes each. (The events plan's 0.64.2 run had 405 blackout minutes and came out rough; today's ship is in better shape.)
- **Places:** the Works bay venue 21 (3 lead spots, 18 standing); the observation room 37 in the room (2 lead, 20 standing, 15 seats) plus 7 in the lobby; the mess 67 in the room (1 lead, 44 seats, 22 standing), then the promenade and plaza; the bow lounge 95 (1 lead, 60 standing, 34 seats), then the promenade and plaza; the auditorium 84 seats; 4 call booths.
- **Draw calls (390x844, budget 450):** the Works bay Thu 14:05: 190; the promenade Fri 14:05: 215; the mess Sat 18:40 (49 crew on the deck, 20 in the mess): 239; the observation room Sun 10:05: 101; the bow lounge Sun 19:40 (34 crew on the deck): 207; the promenade Mon 20:40: 227. EP2 notes the party measured up to 367 with 64 crew in the lounge.
- **Hash keys:** 340 the party (built), **352 the lantern supper (confirmed here)**, 353-354 the Line, 355 up the comet. The storm needs no other key: the Lap's Monday re-dress keeps 442.

## The days, minute by minute (Day 0 of the event = Thursday Day 11)
| When | What | Where | The piece |
| --- | --- | --- | --- |
| Thu 11, 06:00 | **Warning**: Calder's Mail (EW1: "Briefing at the job board, 14:00 today, after tea"); status line; Survey's news (Sato) | Mail, device | `mail.warning`, F2, F3b |
| 06:05 on | Crew react (EW1's warning lines; within about 5 ship minutes, F2b) | every deck | `event.ionStorm.warning` |
| 09:00 | News: Works tying things down | Works | `storm-prep` |
| 09:30-13:00 | The team job (career beat, held by F1) | Deck 5 | unchanged |
| 13:00-13:15 | Works tea | tea corner | unchanged |
| 13:45 | Device notice: the briefing at 14:00 | device | F3a |
| **14:00-14:12** | **Calder's briefing** (Calder, two Works hands on shift, you; the Officer's version once you're promoted); your reply holds a job | Works bay, job board | meeting `stormBriefing`, `calderStorm(.officer)` |
| 14:12 | **The storm jobs go up**: the lounge, ballasts, batteries, junctions (tier 3), **the booth rota (new)**; your pick held | job board | `jobs.warning` at 852 |
| 14:12 to Fri 14:00 | Prep jobs count toward the result if done before the front | Decks 1, 3, 4, 5 | S4 |
| 17:00-18:30 | Nothing from the storm (the officer ceremony 17:15, the Captain's scene) | | F1 |
| 18:45, 20:00 | Postcard night (booths), the quiz (bow lounge), as usual | Deck 3 | unchanged |
| **Fri 12, 14:00** | **The front** (onset): jolt, lights dip, flicker; the Captain's 3-line banner (fits a phone); Vance's Mail; bow lounge, booths, rec deck close; double shifts (command, helm); Watch patrols; stay in (40% of leisure); comms down | every deck | moment `front`, `address.onset`, routines |
| 14:05 on | Crew react | every deck | `event.ionStorm.onset` (89 lines in the game) |
| 15:00 | News: the bridge on double shifts | | `storm-bridge` |
| 15:30 | The short Friday: the day shift stops | | Fridays plan |
| **16:00-16:50** | **The Captain's address** (`friday-d12`: the storm at its heart); the auditorium and its way from the lift open 15:30-17:00 only; Marrow and Vance step off the double shift; stay-in doesn't apply | rec deck auditorium | Fridays plan, `keep`, S2, S3 |
| 17:00-20:30 | Dinner. **Story A begins at the servery** (Lukas on the line) | servery, galley | 20c moment |
| 18:45-21:15 | Works tea, jam, tap night paused | | `pause` |
| **Sat 13, 06:00** | **Escalation**: blackouts (none on Deck 3 in a new game), storm stew, stay in (50%), sleep and social needs | every deck | routines, needs, galley |
| 07:00, 11:00 | News: a deck went dark; storm stew again | | `storm-dark`, `storm-stew` |
| **11:20** | **The surge** (jolt, lights dip) | every deck | moment `surge` |
| 12:00 | The lantern supper's notice and Mail | Mail | gathering `lanternSupper` |
| 14:00 | The lantern job goes up (held for you if you promised Lukas) | Deck 5 storage to the mess | `stormLanterns` |
| 14:30-17:00 | **Story A's choice** (Lukas, the range) | galley | 20c moment, story job `stormRange` |
| 18:00 | Trays to the bridge (the galley's cart run) | Deck 3 to Deck 1 | `galley.trays` |
| **18:00-19:30** | **The lantern supper**: the mess dimmed to lamp light, lanterns on the long tables, storm stew; about 55-60; stay-in pauses 17:45-19:45; Brennan dines; **story A's payoff** | mess (spills to the promenade) | gathering k 352 |
| (all day) | Long breakfast, garden hour, Tiles ladder, cook-along, film night, observatory night paused | | `pause` |
| **Sun 14, 09:45** | Device notice: the all-clear at 10:00 | device | F3a |
| **10:00-10:12** | **The all-clear** (`captainAllClear.<band>`): the Captain, Calder, Sato, Holt called in, Vance on duty, you; the Captain's line to you; **the commendation letter**; **the result settled** (threads stop); her 3-line banner | observation room | meeting `allClear`, F0b |
| 10:00 | Rec deck and booths reopen; **the booth rush** 10:00-18:00 (by the rota, if drawn up) | booths | routine `rush` |
| 10:05 on | Crew react | | `event.ionStorm.resolution` |
| 10:30 | The bow lounge tidy job (moved from Monday: question 7) | bow lounge | `jobs.resolution` |
| 10:30-17:00 | Market, Winner Stays On, reading corner (16:00), as usual | Deck 3, rec deck | unchanged |
| 18:00-19:00 | The Sunday table, as usual | mess | unchanged |
| **19:00-21:00** | **The party** (EW1's words): about 50-60 | bow lounge | gathering k 340 |
| 19:30, 20:30 | Talent night moves to Day 21; Lap of the Wren moves to Monday | | S6 |
| 22:00 | **Afterglow**: the retelling by band | | `storm-told` |
| Mon 15, all day | Status line; the traces by band | | F3b, traces |
| **18:00** | **Calder's debrief** Mail, with your part | Mail | `debrief` at a fixed minute |
| **20:30-21:15** | **Lap of the Wren**, led by Tomas (off that day) | promenade | `EV_DAY_DRESS` (Day 15) |
| 24:00 | The event ends | | `days: 5` |

## What you can do
- **Thursday:** go to Calder's briefing and pick a job; take the storm jobs from the board (the lounge, the ballasts, the batteries, the booth rota; the junctions at tier 3).
- **Friday:** feel the front; go to the Captain's address; meet Lukas at dinner.
- **Saturday (your day off):** help Lukas (the range, the errand to Brennan, or a word); carry the lanterns up from storage (`stormLanterns`); go to the lantern supper.
- **Sunday:** the all-clear (your commendation, if earned); the booth queue; the party.
- **Monday:** read the debrief; walk the Lap with Tomas.
- **Miss any of it** and still be part of it: meetings send their gist by Mail; the supper and the party go on without you.
- **Commendation:** two storm jobs, or one and a storm meeting (the briefing or the all-clear), up to the all-clear (question 8). The range job and the lantern job count.

## Your help and the result
| Your help | What it changes | Thread | Left alone (measured) | Target with it |
| --- | --- | --- | --- | --- |
| Fit the shielded ballasts (Decks 3 and 4) before the front | blackouts are rarer and shorter ship-wide | blackout (good 60, bad 200) | 117 min, bumpy | 60 or under, smooth |
| Carry the battery packs to the bridge before the front | the bridge's urn and hot plate run on them, so the double shift eats on time | bridgeHungry (good 6, bad 14) | 12, bumpy | 6 or under, smooth |
| Draw up the booth rota (new job) | the rush runs in booked slots | calls (good 3, bad 6) | 7.8 h, rough (retuned to about 4.5, bumpy) | 3 or under, smooth |
| (none: the galley's own) | spoiled food | spoiled (good 10, bad 60) | 18, bumpy | stays bumpy |

Left alone: four bumpy (after the calls retune) = **bumpy**. With the three helps: three smooth, one bumpy = **smooth** (`eventBand` rounds the average; two smooth and two bumpy rounds to bumpy, so it takes all three). **Rough** only on a worn ship. The exact numbers are the owners' (blackout: systems, section 17; the fed bridge and spoiled: galley, 16; calls: traditions, 18); bigevents_check checks the three results.

## How the pieces work
- **The new hours (S1).** Phases as above; the briefing at `[0, 840]`, 12 minutes; the jobs at 852; the commendation and the result at the all-clear (`eventFinish`'s scoring split from the ending: F4a); the debrief at `[4, 1080]`; EW1's files moved into `content/` and baked.
- **The double shift and the address (S2).** The routine gets an exception: `{ who: 'dept:command', rule: 'doubleShift', except: [{ ids: ['marrow', 'vance'], day: 1, at: [960, 1010] }] }`, and `stayIn` doesn't apply in the Friday hold (15:30-17:00). Section 14 (the sim seat).
- **The rec deck (S3).** A routine `{ where: '7|*', rule: 'closed' }` in onset and escalation, with the auditorium and its way from the lift open 15:30-17:00 on Day 12 (`eventClosed` already carries the exception, F3a). Blackouts still skip the rec deck. The rec engineer reviews.
- **The first all-hands (S3).** Today it's set by the first event's first address (`recFirstAllHands`, section 18). Unhooked: question 5.
- **The lantern supper (S5).** A moment `{ id: 'lanternSupper', phase: 'escalation', at: [2, 1080], len: 90, k: 352, where: { venue: 'mess', deck: 3, room: /^Mess hall$/ }, gathering: true, who: .85, anim: 'talk' }` with `brennan` at 1, Lukas on the line (the galley line, never pulled), `stayIn` paused 17:45-19:45. **The lantern job** (ER2's fix 1): `jobs.escalation: [{ id: 'stormLanterns', title: 'Lantern supper: carry the lanterns up from storage', tier: 1, at: 840, bring: 'a crate of storm lanterns', stops: [{ deck: 5, room: /^Main storage$/, mins: 5, tag: 'pickup' }, { deck: 3, room: /^Mess hall$/, types: ['mess-seat'], mins: 15, tag: 'drop' }] }]`, posted at 14:00 Saturday, held for you if you promised Lukas, else open on the board (and the mess sign-up sheet); left for a galley hand at 17:00 if nobody takes it. The lanterns on the tables show from 18:00 whoever carried them (the look never waits for the job). The look: the mess's lights at emergency level and lanterns on the long tables (one instanced prop, `DECK_DRESS.lanternMess`, 1-2 draw calls), 18:00-19:30 only. The galley: storm stew for 60.
- **The all-clear day (S6).** The tidy job to 10:30 Sunday (question 7); talent night and the Lap moved by `EV_DAY_DRESS`.
- **`EV_DAY_DRESS`, one shape shared with the Line plan (ER2's fix 5; EP2's proposal, agreed; lead 22: one table serves both, EV1 owns the final shape).** Built here first (S6); the Line's L2 reuses it.
  - **Where:** section 18, a Map keyed `'<tradition id>@<ship day>'`, made at load from `EV_CALENDAR` and each event's own `dayDress` list. Never `eventNow`, `SHIP.event` or anything saved. An event the calendar skips (`EV_SKIPPED`) adds no rows. With `EVENTS_ON` off the Map is empty, so `eventsOn(d)` comes out byte-identical.
  - **An event's data:** `dayDress: [{ trad, day, drop: true } | { trad, day, set: {...} } | { trad, day, add: {...} }]`, where `day` is the event's own day, turned into a ship day through its calendar row.
    - `drop: true`: the tradition doesn't happen that day;
    - `set`: it happens with some fields replaced: `name`, `at`, `jitter: 0`, `who` (extra pulls such as `[['tomas', 1]]`, added to its own), `words` (a bank prefix) and `mail: false`;
    - `add`: a one-off copy on a day it doesn't normally fall, keeping the tradition's `k`.
  - **Who reads it:** `eventsOn(d)`, as it builds the day's list. A stop on a walk (the Line's `3-lap-6`) is a 20c moment, not dress.
  - **The storm's rows** (its day 0 = Day 11): `{ trad: 'lap-of-the-wren', day: 3, drop: true }`; `{ trad: 'lap-of-the-wren', day: 4, add: { at: [1230, 1275], who: [['tomas', 1]], words: 'event.ionStorm.trad.lap-of-the-wren' } }`; `{ trad: 'rec-talent-night', day: 3, drop: true }`; `{ trad: 'rec-talent-night', day: 10, add: {} }` (Day 21, its usual hours).
  - **The Line's rows** are EP2's (Day 7: `sunday-table` set, `lap-of-the-wren` set).
- **Determinism.** Everything the crew's planner reads comes from the calendar, the event's data and the rota. Your replies (the briefing, Lukas, the errand) only set saved flags and hold jobs; nothing in the planner reads them.

## The build turns (after the events base; switch: the base's `EVENTS_ON`, on with this update after the user's review)
Each turn: small exact edits; a build-table row under "Ion storm update"; the area's checks, then `bash check_fast.sh`; cadet_test with the switch off (ALL IDENTICAL); push, report. The build number is the build master's.

| Turn | What | Sections (owners) | Checks besides check_fast |
| --- | --- | --- | --- |
| S1 | The new hours: phases, `days: 5`, `keep: captains-address`, the briefing at 14:00 and jobs at 14:12 (your pick held), nothing 17:00-18:30 Thursday, the result and commendation at the all-clear, the debrief Monday 18:00; EW1's ionStorm files moved into `content/` and baked | 18 (traditions: EV1), 22 generated (writers) | events_check, bigevents_check on paper, lines_check, career_check, leave_check |
| S2 | The cast: the all-clear's four called in (F0b), `works:2` at the briefing on shift; Marrow and Vance off the double shift 16:00-16:50 Day 12; stay-in not in the Friday hold | 14 (sim), 18 | day_check Days 11-14, bigevents_check cast |
| S3 | The rec deck: closed front to all-clear, the auditorium open 15:30-17:00 Day 12; the first all-hands unhooked (question 5); talent night to Day 21 | 18, 4e/15r/8c (rec engineer) | events_check, join_check, day_check 12, devmode_check |
| S4 | Your help counts: the ballasts, batteries and booth rota effects; the calls retune; the booth rota job and its sheet | 17 (systems), 16 (galley), 18, 4d (the sheet) | machine_check, food_check 12-14, bigevents_check results |
| S5 | The lantern supper: k 352, the crowd, stay-in paused, Brennan's pull, storm stew for 60, the lamp-light look and lanterns, **the lantern job `stormLanterns`** | 18, 14, 16, 17 (the job), 8b/4d | food_check 13, day_check 13, bigevents_check crowds, perf_check scene **with about 60 in the mess and the lanterns at 390x844** (239 was measured with 20 in the room) |
| S6 | The all-clear day: the party's words, the tidy job, `EV_DAY_DRESS` (Lap to Monday with Tomas), talent night's move, the booth rush | 18, 16 (if the party gets food) | events_check, day_check 14-15, social_check |
| S7 | Story A: the three moments, the range job, the errand stop, Lukas's Mail, the lantern trace, ~30-35 lines | 20c (social), 18, 17 (the job), 4d (trace) | social_check, events_check, bigevents_check live (Lukas on the line Fri-Sat, Brennan at the supper) |
| S8 | Your device and the banner: the banner on phones (HUD), status lines, Schedule, Record, the Officer's briefing (F5) | page/11 (HUD), 19 (device), 18 | device_check, interactions_check, bubble_check, shots at 390 and 360 |
| S9 | Small things: old placeholder code, the framed menu prop, Deck 4's common room draw calls (454, budget 450) | 18, 4d, 8b (performance) | deck_check, perf_check |
| S10 | Switch on (`EVENTS_ON = true`) after the user's review; the full round; design-doc and DEV_NOTES | 18 | the full round (intro_check in pieces) |

**About 10 turns** (the plan said 9-11), then the adversarial build review, then the user's review.

**Needed first** (the events base): F0b (called in, and named people placed into an event's meetings), F2b, F3b, F4a-b, F5, F7a-c (bigevents_check), F8 (comms down for calls); the Fridays plan's `SHORT_FRIDAY` and `captains-address` (Day 12's address).

## The 13 update items (events plan v2/v3), where each goes
1. It lands on your promotion: moved to Days 11-15 (F0, F1; S1).
2. The 89 storm lines never play: phase notes (F2, F2b).
3. Nothing you do changes the result: S4.
4. The device misses meetings; Tracked offers closed places; no status line or Record: F3, S8.
5. Skips and reloads lose phases and meetings: F4.
6. Calls home blocked only on the front day: F8 (`commsDown` in onset and escalation).
7. No proper event day: F1a (`eventDay` Days 12-14, measured).
8. The rec deck tied into the storm: S3.
9. Your briefing choice never holds a job: S1 (jobs at 14:12, your pick held).
10. The banner covers the HUD on phones: S8 (HUD seat).
11. Small parts by rank: F5, S8.
12. The ready room and the Captain's table spaced out: F1c.
13. Small things (placeholder code, the framed menu prop, a reload replaying the jolt (F4b), too many traditions on the party evening (S6), Deck 4's draw calls): S9.

## Risks
1. **The base's gap:** today nobody is placed into an event's meeting (measured: the all-clear room is empty at 10:00). S2 is gated on F0b.
2. **Off must stay identical:** all of it behind the base's switch; cadet_test ALL IDENTICAL every turn.
3. **The double shift and stay-in meet the Friday address:** without S2's exceptions the Captain and Vance would miss their own address and 40% of the free crew would stay in.
4. **Stay-in vs the supper:** without the pause, half the free crew stay in their quarters (the supper would get about 30).
5. **The talent night pulls the party's crowd** (measured: 32 heading to the rec deck at 19:30); its move must land with the party.
6. **The result must move with help** (bigevents_check runs it three ways). The calls retune changes only the minutes a call takes in `stormCallBacklog` (section 18: about 25 minutes left alone, 15 with the rota), never `callOwed`, which section 14's rush rule shares.
7. **Words vs the sim:** the dead rings in story A are words; the galley's real cooking isn't touched.
8. **The rec deck's first all-hands** moves film night: whichever date is chosen, the rec engineer's check runs.
9. **Draw calls with 60 in the mess** plus the lanterns: perf_check's supper scene at phone size.
10. **Spoilers:** the guard rails above; EW1 and the head writer read the lines.

## Questions for the user (ids `storm-q1` to `storm-q8`, plus `storm-general`)
1. **The story.** Recommended: A, "Sixty by lamplight". Others: B, "First in the queue"; C, "What the storm is called".
2. **How much does your help count?** Recommended: each prep job moves its own part (ballasts the blackouts, batteries the fed bridge, the booth rota the calls); left alone bumpy, all three smooth. Others: the jobs add up into one score; help only softens the effects, and the result is luck.
3. **The lantern supper's light.** Recommended: the mess dimmed to emergency level with lanterns on the long tables, 18:00-19:30, on purpose (no blackout lands on Deck 3 in a new game). Others: wait for a real blackout on Deck 3 (rare); normal light, the lanterns only in words.
4. **Staying in vs the supper.** Recommended: the supper is where everyone stays in: off-duty crew are drawn to it (about 55-60, cap 60) and stay-in pauses 17:45-19:45. Other: stay-in holds (about 30).
5. **The rec deck's first all-hands, unhooked from the storm.** Recommended: the first Friday address (Day 5) counts as it, so film night moves to the auditorium from Saturday Day 6. Others: the first Monday of the next season; film night moves on Day 6 anyway and the season's all-hands waits.
6. **Who's at the all-clear?** Recommended: as today, the five (four called in) and you, in the observation room; everyone else gets the Captain's banner. Other: open to anyone nearby (up to 37 in the room).
7. **When is the bow lounge tidied?** Recommended: Sunday 10:30, just after the all-clear, so the room's back to normal for the reading corner and the party. Other: Monday 08:00 as today (the party has paper cups: the glassware's still packed).
8. **What counts toward your commendation?** Recommended: storm jobs and storm meetings up to the all-clear, including Saturday's range job (`stormRange`) and lantern job (`stormLanterns`, built in S5) (two jobs, or one and a meeting). Other: only the prep jobs posted at the briefing.

## Judgement calls (tell me if any is wrong)
- The storm is the regular Friday address's heart on Day 12; no all-hands of its own (the user's decision).
- The front's banner stays short (3 lines); the full words are at 16:00.
- The Captain's scene that weekend is the all-clear (Sunday); Thursday's scene is the officer ceremony.
- The party keeps its key (340) and the bow lounge; the Sunday table and reading corner run as usual that day.
- The lantern supper is the storm's Saturday dinner (no other dinner tradition that day).
- The story's range job is a real Works job (it counts); the four dead rings are words, not a machine fault.
- Saruth goes to the supper and the party like anyone off duty (no visit spoilers in either).

## A delayed promotion during the storm (ER2's fix 3; decided by lead 22)
The promotion can be delayed, never failed, so a slower player's summons, move or commissioning can fall on Days 12-14. F1's guard holds only the default days (Days 9-11). **Lead 22's decision:** a delayed career scene on storm days is held by the guard until after the all-clear. `guardFree` treats the storm's onset, escalation and resolution hours as held for career beats, so a delayed summons, move or ceremony waits until after the all-clear (Sunday from 10:12, or Monday), and never displaces the front, the Friday address, the lantern supper or the all-clear. Story A never assumes your rank or cabin (its lines read the save). EV1 builds it in F1b-c; bigevents_check holds a slow player's summons on Day 12 until after the all-clear.

## ER2's round 1 (69629c7), as taken
1. **The lantern job:** built in S5 as `stormLanterns` (Deck 5 storage to the mess's long tables, tier 1, posted Saturday 14:00, held for you if you promised Lukas). q8 now names it.
2. **"He's ready":** reworded to "tell him it's his galley tonight", with a new guard rail: nothing that hints at handing the galley on.
3. **Rank and cabin:** Lukas's lines read the save ("bunkmate" or "since you moved"); "I'm Works" works at any rank. A delayed career scene on storm days is held until after the all-clear (lead 22's decision, above).
4. **The range stop:** `{ deck: 3, machine: 'range' }`. Note: `'3-range-1'` as the machine wouldn't resolve: `eventStopOf` matches a kind, or the middle part of an id (`id.split('-')[1]`), so the kind is the way the ballasts job does it (`'lights'`); it lands on `3-range-1`'s panel `3-range-1-panel`.
5. **`EV_DAY_DRESS`:** EP2's shape (Map `trad@day`; `drop` / `set` / `add`), above, built here in S6; the Line's L2 reuses it; EV1 owns the final shape.
- **Nits:** S5's perf_check scene measures about 60 in the mess plus the lanterns at 390x844; story A begins "at the servery".
