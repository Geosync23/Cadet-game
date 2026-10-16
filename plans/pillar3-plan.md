# Pillar 3 plan: your device, the people aboard, and the first ship-wide events

**Draft, 2026-10-16, for the user's approval.** Written by the Pillar 3 planner for the lead. Nothing in it is agreed yet: every decision is marked **Proposal** and waits for the user's yes, no or change. Read with `design-doc.md` (above all "Vision & pillars", "The living ship", "Crew simulation", "Social life", "The player", "Works progression", "Ship-wide events" and "Open questions"), `plans/pillar2-plan.md`, `plans/answers-pass-plan.md`, `TEAM.md` and `DEV_NOTES.md`.

---

## The pitch (one page)

After Pillar 2 the Wren works: the galley cooks, machines wear, the Works crew fix them and so can you. After tonight's answers pass it also has birthdays, observatory nights, crew who look tired when you tap them, and a simple Mail inbox. **Pillar 3 gives that ship a voice, a social life and its first stories.** It has three parts, built side by side:

1. **Your personal device becomes the game's main screen.** One device, many small apps: **Schedule, Appointments, Maps, Memos, Mail, Calendar, Needs and Jobs**, which you asked for, plus **Crew** (a contacts list), **Ship** (status and news) and **Camera** (a photo log). It's built in two layers, so your visual design can be dropped in later without touching how anything works. The ship keeps running while it's open.
2. **The crew become people you know.** Each crew member has a relationship with you (stranger, acquaintance, colleague, friend, close friend) that grows by working, eating and talking together, and by doing them favours. Tapping someone opens a short chat, with no dialogue trees: they greet you by how well they know you, and tell you how they feel, what's going on aboard, or something about their life. Crew also like or dislike each other, so friendships and small rivalries grow on their own. Friends come and find you, invite you to things and put in a good word with the Chief.
3. **Ship-wide events begin, and they're ambient.** Your idea is the core of the design: *the key is they are ambient and everyone talks about them.* There are no cutscenes and no mission screens, and the game never stops. An event is a few days in which the ship's systems, the crew's routines and the decks change. News reaches you the way it reaches everyone: crew chatter first, then Mail, the job board, and finally the Captain's ship-wide address. You decide how much to get involved. How well it goes comes from what actually happened on the ship, not from a pass or fail. A few big **moments** (the storm front hitting, the delegation stepping off the shuttle) are announced ahead, happen in a real place at a real time with the crew gathered, and can be felt on every deck, so they never need the camera taken away from you.

**First events:** the **ion storm** (touches every system), then a **diplomatic visit** (guests, formal dinners, the second visitors' cabin in use) and **something in the garden** (a creature eats the crops, and ends up as the ship's pet). Three more are fleshed out (illness, nebula drift, salvage), plus seven shorter ideas, including a festival with the whole crew on the plaza, which is where the crowds over 70 come in.

**Progression hooks:** your first time inside the Captain's ready room (summoned after a commendation), sitting in on a briefing at the conference table, tea in a friend's cabin, and an invitation to the Captain's table.

**How it's built:** three new helpers (device, social, and the events engineer you already have, who grows from traditions into ship-wide events), with the existing helpers doing small parts. Two check-ins with you: one after the device and social basics, one after the ion storm. Combined builds are **0.50.x**.

**What we need from you:** a yes, no or change on each **Proposal** below; above all the device's two-layer approach, the "no fail screens, outcomes in three bands" rule for events, and the event order. The device's look stays yours to design whenever you're ready.

---

## Where we start (after tonight)

- **Pillars 3 and 4 meet here.** The design doc's milestones list Social as Pillar 3 and Events as Pillar 4. **Proposal:** Pillar 3 builds the social basics and the *start* of events (the framework and the ion storm) together, because events are mostly people talking; the later events then follow as their own pillar.

- **The build** (0.41.x tonight, on `claude/ship-integration`): 75 crew on schedules (section 14), needs for crew and player (14, 15), the galley (16), machines, jobs and supplies (17), and section 18 `SHIP EVENTS`, small recurring traditions from the events engineer.
- **The device today** is a placeholder panel (section 15) with registered sections: `device.addSection(id, title, render)`. It has Now, Needs (with tonight's bonus and penalty marks) and Jobs, plus Mail (`mailSend`, `SHIP.mail`).
- **Crew feelings:** `crewMood(p, t)` and `crewFeeling(p, t)` give the tap line. Birthdays (`ROSTER[i].birthday`), habits that change (`SHIP.habitLog`), observatory night, the Deck 1 shift handover and the Captain's evening walk all exist or arrive tonight.
- **Not there yet:** no relationships, no conversation, no way to talk to crew beyond a toast, no guests, no events beyond traditions, no map, no appointments. The ready room and private bedrooms are locked. No sound at all (the game has no audio code).
- **Crowds:** the crowd draws all 75 cheaply; tonight adds a third, coarse level of detail and a `?crowd=120` demo (performance engineer).

---

## Part 1: the personal device

### What it is

**Proposal:** the device is a small handheld (or wrist) computer every crew member carries. It holds your day, your messages, your notes and the ship's news. It's **the only menu in the game**: there are no other panels. It opens instantly and never stops time (no time controls, as you decided).

### Two layers, so your design can drop in

**Proposal:** the device is built as two separate layers.

1. **The apps (how it works).** Each app is a small piece of code that returns *plain content*: a title, lists of rows, a few buttons, a badge count. It never builds the screen itself. Example: the Jobs app says "three rows: *Scrubber 2, Deck 4, urgent*, with a Take button", and nothing about colours, fonts or layout.
2. **The skin (how it looks).** One piece of code turns that plain content into what you see. Tonight's plain panel becomes the first skin. When your design is ready, a new skin replaces it, and every app keeps working unchanged.

This is the same idea as the current `addSection`, taken one step further: apps describe, the skin draws. The skin can also choose layout per screen size.

```js
// section 19. DEVICE (new, the device engineer)
deviceApp({ id: 'jobs', title: 'Jobs', icon: 'wrench', order: 80,
            badge: () => n,                      // a number or null
            view: (ctx) => VIEW })               // plain content, see below
// VIEW: { title, blocks: [ { kind: 'list', rows: [{ text, sub, mark, action }] },
//                          { kind: 'bars', items: [{ label, value, mark, note }] },
//                          { kind: 'text', text }, { kind: 'buttons', items: [{ label, action }] },
//                          { kind: 'map', deck }, { kind: 'form', fields: [...] } ] }
// action: { app, do, arg }: the skin calls deviceDo(action) when it's tapped; the app handles it.
DEVICE_SKIN = { open(), close(), draw(appId, VIEW), notify(note) }   // the only code that touches the DOM
deviceNotify({ app, text, urgent })            // the chirp: a badge, and a toast if urgent
```

`device.addSection` stays as a shim for anything that still uses it, so nothing breaks during the move.

### How it opens and works on a phone

- **Proposal: opening.** A device button in a screen corner (where today's button is), and a swipe up from the bottom edge. It opens on a **home screen**: the time and day, your next item ("Shift starts 08:00", "Dinner with Pell, 18:30"), any active event in one line, then the grid of apps with badges.
- **Proposal: phone (portrait).** It slides up as a sheet covering about two thirds of the screen, so the ship stays visible above it. Back goes to the home screen; tap the ship or swipe down to close.
- **Proposal: the TriFold unfolded (wide).** It docks as a side panel on the left and can stay open while you walk. This suits the Maps and Jobs apps.
- **Touch first:** every tappable thing at least 44 pixels high, no hover, no tiny text.
- **Notifications:** a soft chirp (when we add sound) and a toast for urgent things (your job's machine broke, an appointment in 10 minutes, the Captain's address). Everything else is a quiet badge. **Proposal:** a "Quiet off shift" setting that turns work notifications into badges after 17:00.
- **While it's open,** the game keeps running and you keep walking if you were. Tapping a map pin or a job can set your walk target (see Maps).

### The apps

Your eight first, then the proposed extras.

| App | What it does | Built from |
| --- | --- | --- |
| **Schedule** | Today as a timeline: shift, meals, your appointments, gatherings, birthdays, event moments. A week view with the rota and your days off. A strip says where you're expected right now ("On shift: Works bay"). | Your rota (section 13/14), section 18 traditions, Appointments, events |
| **Appointments** | Make one: pick a person or a place (a crew member, the infirmary, the Works Chief's office, a meeting), a time and a spot. Crew answer from their real schedule: yes, "not then, how about 19:00?", or no. Accepted appointments go into their day and they turn up. Invitations from crew arrive here too. | New: section 19 (the form), section 14 (crew keep them) |
| **Maps** | Each deck as a clean plan drawn from its deck data: rooms named, you as a dot, locked rooms hatched. Search a room or a person; a person shows where they are now, if you know them well enough (see below). Tap a spot to walk there; on another deck, it walks you to the lift. | The deck text maps in `DECKS`, `whereIs` |
| **Memos** | Notes you write. Plain text, a title, the date. Pin one to the home screen. **Proposal:** a "remember this" button on chats, Mail and job lines copies the line into a new memo. | New, saved |
| **Mail** | Tonight's inbox, grown: from the ship (shortages, spoilage), crew (invitations, thanks), departments (event notices), the Captain (addresses, in writing), and home (replies to your calls). Read and unread, delete, "remember this". | `mailSend`, `SHIP.mail` |
| **Calendar** | A month of ship life ahead: the weekday shapes (Monday briefing, Wednesday drill, Thursday inspection, Friday treat, Sunday vote dinner), the Captain's piano on Thursdays, observatory night, birthdays, traditions, holidays, and announced events once they're known. Tap a day to add it to Schedule or make an appointment that day. | Section 18, `ROSTER.birthday`, events |
| **Needs** | Your five needs as bars, each with its bonus or penalty mark and a one-line reason ("Fed: energy drains 10% slower"), from tonight's `needEffects`. A line suggests what would help and where. | Section 15 |
| **Jobs** | The job list for your tier: take, drop, see parts needed, where it is (with "show on map"). Event jobs carry the event's tag. Favours crew asked of you sit in their own list. | Section 17, social favours |
| **Crew** (proposed) | Your contacts: everyone you've met, with face, name, rank, department, relationship tier, birthday, and what you know about them (filled in as they tell you). Friends show where they usually are at this hour. Message a friend; make an appointment from here. | Section 20 social, `ROSTER` |
| **Ship** (proposed) | Ship health and each system's condition (as on the Works bay board), what's happening ("Ion storm: day 2 of about 3"), and **Ship news**: everything you've heard, newest first, each with who told you and when. | Section 17, events, the news model |
| **Camera** (proposed) | Take a photo of what's on screen; the photo log keeps them with date, deck and who's in shot. Events and moments add a suggested caption. A small way to keep memories of the ship. | Renderer snapshot (see saving) |
| **Record** (proposed) | Your Works record: tier, jobs done, early catches, commendations, what the Chief thinks ("Calder: steady, a bit slow on filters"), and how close certification is. Where progression shows. | Section 17; certification comes later |
| **Wallet** (proposed, small) | Credits and what's in your locker (tonight's shop buys). Could live inside Needs instead. | Section 15 |
| **Music** (proposed, later) | The music room's record cabinet on your device: a few procedurally made tunes. The game has no sound yet, so this waits for a sound pass. | A future sound pass |

**Proposal: knowing where people are.** Maps finds rooms always, and people only once they're at least an acquaintance (or are on duty somewhere public: the chef in the galley, Rina in the infirmary). This makes relationships useful and keeps the map from feeling like surveillance.

### Appointments in detail (the user's request)

- **Making one:** Appointments → New → who or what → when (the next three days; times in 15-minute steps) → where (a suggested place, or pick one from the map).
- **Crew answer from their real schedule.** If the slot falls in their free time and they like you enough for that kind of meeting, they accept. If not, they offer the nearest free slot. Strangers accept only work matters (meeting the Works Chief, an infirmary check-up); friends accept anything.
- **Crew keep them.** An accepted appointment goes into that person's day (`planDay` reads it), so they walk there and wait about 15 ship minutes.
- **Proposal: no punishment if you miss one.** They mention it next time ("Waited for you at the gym yesterday"), and it doesn't count as time together. Nothing is lost.
- **Places with a purpose:**
  - **The infirmary:** a check-up with Rina or Dr. Nandakumar shows your needs in words and gives a small rest bonus.
  - **The Works Chief's office:** a progress talk. Calder tells you where you stand toward certification. This is how the Record app's comments are earned.
  - **A meeting:** with two or more people at a table (the mess, the lounge, the junior common room). The conference room only through a briefing (see Part 4).
- **Crew make appointments with you:** friends invite you ("Gym at 18:00?", "Pond bench after dinner?"). Officers summon you (Calder: "My office, 09:30"). Invitations arrive in Appointments and Mail; accept or decline.

### Saving

- **Proposal:** everything the device owns goes into the save through `SAVE_EXTRA` as `SHIP.device = { memos, appts, readMail, pins, settings, photos }`. The save goes to `v: 3` and still reads `v: 2` saves (empty device).
- **Photos** are small (320 pixels wide, compressed, about 20 KB each) and kept in the browser's larger storage (IndexedDB), not the main save, with a cap of 30. When full, the oldest unpinned one goes. If the browser refuses storage, the camera says so and nothing else breaks.
- **Appointments** are also saved in the crew side (section 14 reads `SHIP.device.appts`), so a crew member still turns up after a reload.

---

## Part 2: ship-wide events (the main missions)

### The core idea: ambient, and everyone talks about it

Traditional games tell a story by taking over: a cutscene, a mission marker, a fail screen. That breaks two of our pillars, "the ship runs itself" and "you are one of the crew". So **Proposal: an event is never a mission you're given; it's something happening to the whole ship that you live through.** You learn about it like everyone else, talk about it like everyone else, and help as much as you choose to.

What that means in practice:

| A traditional story mission | A Wren ship-wide event |
| --- | --- |
| A quest giver hands you the mission | You hear about it: a rumour, then Mail, then the Captain's address |
| A marker shows where to go | The ship changes around you: flickering lights, a closed lounge, new jobs on the board |
| A cutscene plays and time stops | A *moment* happens at a real place and time; crew gather; the ship keeps running |
| You succeed or fail | The ship comes out of it smoothly, bumpily or roughly, from what actually happened |
| The story is the same for everyone | What you see depends on your rank, your friends and where you were |
| After the mission, the world resets | Small permanent traces stay: a scorch mark, a plaque, a pet, a photo |

### How an event is put together

**Proposal:** each event is one block of data (like a deck definition), so new events are mostly writing, not code.

```js
// section 18. SHIP EVENTS (the events engineer; ship-wide events join tonight's traditions)
SHIP_EVENTS.ionStorm = {
  title: 'Ion storm', days: 3, earliest: 8,           // ship days; the soonest day it can happen
  phases: [ { id: 'warning', at: [0, 9*60] }, { id: 'onset', at: [1, 14*60] },
            { id: 'peak', at: [2, 6*60] }, { id: 'clear', at: [3, 10*60] } ],
  // what each phase changes, read by the sections that own those things:
  systems:  { onset: { wear: { power: 2, comms: 3 }, effects: ['flicker'] }, ... },  // section 17
  routines: { onset: [ { who: 'dept:command', rule: 'doubleShift' }, { where: 'lounge', rule: 'closed' } ] }, // section 14
  galley:   { peak: { menu: 'stormStew', grab: 1.5 } },                              // section 16
  jobs:     { warning: [ { kind: 'secure', where: 'lounge', tier: 1 }, ... ] },      // section 17
  news:     [ { id: 'readings', from: 'Sato', phase: 'warning', seed: ['dept:survey'], lines: [...] }, ... ],
  moments:  [ { id: 'front', phase: 'onset', where: 'shipwide', feel: ['jolt', 'lightsDip'] } ],
  threads:  [ { id: 'power', label: 'Keep the lights on', score: 'minutesOfBlackout', good: 30, bad: 180 }, ... ],
  traces:   { good: ['stormPhotoTeaCorner'], bumpy: ['relayScorch'], rough: ['relayScorch', 'tapedPanel'] },
}
eventNow() -> { id, phase, day } | null              // anyone may ask; inert when null
eventMod(kind, key) -> number | rule | null          // e.g. eventMod('wear', 'power') -> 2
```

Every other section asks `eventNow()` or `eventMod()` and changes its own behaviour. The events engineer never edits another section's code; the other owners add one small, inert check each.

**Proposal: the shape of every event** (the design doc's onset, escalation and resolution over 2–4 days, with a warning added in front):

1. **Warning** (hours to a day ahead, when it makes sense): a few people notice something. Rumours start.
2. **Onset:** the event arrives. A moment marks it. Systems, routines and the decks change. Event jobs appear.
3. **Escalation:** things get harder: more faults, tighter food, tired crew, a second moment.
4. **Resolution:** it ends, always. An all-clear, a gathering, a debrief.
5. **Afterglow** (a day or two): crew talk about it, mood lifts or sags, traces appear, commendations are handed out.

### How news spreads

**Proposal: a small news model** (section 20, social, used by events and also by everyday gossip).

- **A piece of news** is a fact with a source and a few spoken versions: `{ id, about, lines: ['Sato hasn't left the chart room since last night.', ...], weight }`.
- **It starts with a few people** (the event's `seed`: whoever would know first: Survey sees the readings, the galley knows about the extra dinner).
- **It spreads on paper, hour by hour,** like everything else in the simulation: people who know it pass it on to people they spend time with (meals, the same work room, the same bunk room). Friends pass it on more readily than strangers. This costs almost nothing: it's a check per crew member per ship hour, using the same "who is where" that schedules already give.
- **Crew who know it talk about it.** You hear news in five ways, in roughly this order for a big event:
  1. **Chatter:** walk near crew who know something and you sometimes overhear a line as a small speech bubble ("They say the storm's the size of a moon"). Cheap: a text sprite on one nearby person, at most one or two at a time.
  2. **The tap line and chats:** tap someone and their line may be the news; chatting gives the fuller version.
  3. **Mail:** department notices ("Works: all hands to secure loose fittings by 12:00"), and later the Captain's address in writing.
  4. **The boards:** the Works bay job board gets an event banner and event jobs; the mess menu board changes; the ship health boards show the strain.
  5. **The Captain's ship-wide address:** for big turns only (onset, all-clear). See "Moments".
- **What you know is recorded.** Each news item you hear goes into the Ship app's news feed with who told you. Nothing is gated on knowing, but **Proposal:** a crew member who tells you something first gives a small relationship nudge ("being in the loop" is social).
- **Gossip uses the same model every day,** not only during events: ship faults ("The scrubbers on 4 have been rattling all week", from section 17), crew lives (birthdays, habit changes from `SHIP.habitLog`, rivalries), guests arriving. This is the design doc's "gossip is a hint system".

### How you learn and choose to engage

- **You're never told to do anything,** except by your job. If you're on shift, your work is Works work, and an event adds event jobs to the board like any other. Taking them is your choice, as now.
- **Rank decides which parts reach you** (design doc). At Tier 1 you carry filters, secure fittings, swap lamps and run carts. You see the briefing only if someone takes you along (see Part 4). Later tiers get the relay work and a seat at the table.
- **Ways in for a Tier 1 junior:**
  - **Event jobs** on the board, tagged with the event.
  - **Volunteering:** some events put a sign-up sheet on a board (in the mess or the Works bay): "Garden watch tonight, 21:00–23:00", "Help set up the plaza for the festival". Signing up is an appointment.
  - **Asks from crew** you know: Brennan needs a hand carrying stew to the bridge; Rina asks you to check on Tomas.
  - **Just being there:** turning up at a moment, keeping people company, checking on friends.
- **Not engaging is fine.** If you sleep through the storm, the crew handle it, more slowly, and you hear all about it the next day.

### How outcomes are scored, with no fail screens

**Proposal:** each event has **3 to 5 threads**: the things the whole ship is trying to keep right. Each thread is measured from what actually happened in the simulation:

- *Ion storm:* minutes of blackout across the ship, food spoiled, call-home backlog when comms return, how tired the bridge crew got.
- *Diplomatic visit:* dinners served on time, guest cabins comfortable (machines healthy), crew who were rude to the guests (Holt's mood), the gift exchange.

Each thread lands in one of **three bands: smoothly, bumpily, roughly**. The event's overall result is the blend.

- **The whole crew's work counts,** not just yours. You affect the result as one good pair of hands, a bit more than one average crew member, because you pick the jobs that matter.
- **Your own part is counted separately** (the jobs you did, the people you helped, the moments you turned up to). It decides your **commendation** (toward promotion), relationship gains and whether you're mentioned in the debrief. A smooth event you sat out still gets you nothing personal; a rough event you worked hard in still gets you thanks.
- **Results show as story, never as a score:**
  - the Captain's all-clear address says how it went in words;
  - Mail brings a debrief from your department, and maybe a commendation letter;
  - crew talk about it for days ("Lights only went once on our deck, thanks to Works");
  - **traces** stay: a photo of the storm crew pinned in the tea corner (smooth), a scorch mark in the relay room (bumpy), a taped panel and a scorch mark (rough), a new pet in the garden, a Veyli gift in the lounge.
- **Rough is never failure.** Every event ends; the ship gets shabbier and moodier for a while and recovers, exactly like neglected machines today.

### Moments without stopping the simulation

The hard question: how do you stage a few unmissable beats without cutscenes? **Proposal: three kinds of moment.**

1. **Felt everywhere.** Some beats happen to the whole ship at once, so you can't miss them wherever you are: the storm front hits (a short camera shake, every light dips, then flickers), the drive kicks in after the salvage, the nebula fills every window with colour. These are cheap effects on the current deck only (the other decks are on paper anyway). Crew react where they stand: stop, look up, then carry on.
2. **The Captain's ship-wide address.** A banner across the top of the screen with the Captain's portrait and a few lines of text, shown on every deck at once, readable for about 20 seconds and kept in Mail afterwards. Crew on your deck stop and turn toward the nearest speaker grille for those seconds (a pose, no pathing change), then go on. **Time never stops.** Used at most two or three times per event, so it feels like an occasion.
3. **Gatherings at a real place and time.** Announced ahead (Calendar, Mail, the address, chatter): the delegation arrives at the shuttle bay at 10:00, the all-clear party in the bow lounge at 19:00, the hunt for the garden creature at 21:00. Crew who'd come put it into their day (section 14) and go. If you're there, you see it: the shuttle doors open, the guests walk down the ramp, the Captain greets them, everyone claps (a short scripted sequence that moves crew already there, never the camera). If you're not, you hear about it, get a Mail with a photo, and the Camera app has a "missed" note.

- **Proposal: no forced camera, ever.** At most, a gentle "Something's happening in the shuttle bay (Deck 5)" note on the device 15 minutes before a gathering, with "show on map".
- **Proposal: moments repeat in conversation.** Whatever you saw or missed, the crew retell it in chatter for a day or two, with the details that happened (who was there, whether the lights went), because it's built from the simulation.

### Gatherings of more than 70 crew

- **Where:** the plaza and promenade (Deck 3), the mess hall, the bow lounge, the shuttle bay (Deck 5). These are the only places big enough.
- **How it's drawn:** the crowd's coarse third level of detail (tonight's work) for anyone more than about 12 tiles from the camera; normal crowd figures nearer; full rigs only for the story crew nearest you, as now.
- **How it's planned:** a gathering is a set of spots (a `gather` place group per venue, added by the architects), filled nearest first; if it overflows, people stand in the next room or the corridor, as in real life.
- **Budget:** the gathering must stay under the 450 draw-call budget with all 75 crew plus guests in one room, checked by `day_check` on a gathering day. **Proposal:** the festival event (below) is the stress test and isn't built until the performance engineer signs it off on a real phone.

### Visitors in the guest cabins

- **Guests are like crew but temporary** (design doc): a short list `GUESTS` with the same spec as roster entries (looks, department colour or a civilian outfit, a role, a cabin, habits), plus `arrive` and `leave` days. They follow schedules from simple templates: "scientist" (lab and observatory), "delegate" (formal dinners, tours, their cabin), "passenger" (lounge, mess, garden), "survivor" (infirmary, then rest).
- **Where they sleep:**
  - Deck 2: Envoy Saruth's cabin (permanent), the visitors' suite, and the **second visitors' cabin, kept for event visitors** (your decision). A delegation leader or a visiting dignitary gets one of these.
  - Deck 4: the six guest cabins by the lift for everyone else (staff, specialists, passengers, survivors).
- **Proposal: everyday guests too.** Between events, one or two guests now and then (a specialist for a week, a transfer waiting for their ship), so the corridor always has new faces and gossip, as the design doc says. About one arrival every ship week.
- **Guests eat, sleep and use rooms** like crew: the galley cooks for them, their cabins' machines wear, they show up in chatter and you can befriend them (a short-lived relationship).
- **Owners:** the crew designer writes guest templates and the event guests; the sim engineer schedules them; the architects make sure the guest cabins have places.

### Six events, fleshed out

Each lasts 2–4 ship days. Tier 1 is what reaches you now; later tiers in brackets.

**1. Ion storm (the first, about day 8–10 of a new game).** Touches every system.
- *Warning (the day before):* Survey picks up readings. Dr. Sato lives in the chart room; chatter starts in Survey and spreads by dinner. Mail from Works: "Storm prep: secure fittings, top up filters, check battery packs." Event jobs: secure the lounge glassware and bar, swap two lamp ballasts for shielded ones, carry battery packs from Deck 5 to the bridge. [Tier 3: service the power junctions.]
- *Onset (day 1, 14:00):* **Felt everywhere:** a jolt, every light dips, then flickering. **The Captain's address:** "We're in it. Expect flickers and no calls home for a while. Look after each other." Comms go down: the call-home booths close, outside Mail stops. The bridge runs double shifts; the lounge closes; the mess goes quiet as people stay in their quarters; Watch patrols the decks.
- *Escalation (day 2):* power wear doubled and comms tripled: relay faults pop up, one deck at a time goes to emergency lighting for up to an hour (a dim red-amber light mood on that deck), the chiller strains. Brennan cooks storm stew (one pot, quicker) and sends trays to the bridge (a cart job). Sleep is worse; crew are short-tempered in the tap lines.
- *Resolution (day 3, about 10:00):* **the all-clear address.** Comms return, and everyone rushes the booths: a real queue at the call-home booths for an afternoon. That evening, a gathering in the bow lounge.
- *Threads:* minutes of blackout; food spoiled; how tired the bridge crew got; the call-home backlog.
- *Goes well:* short blackouts, no spoilage, a cheerful party, a photo of the storm crew in the tea corner. *Goes badly:* long blackouts, binned food, a tired, grumpy ship for two days, a scorch mark and a taped panel in the relay room.

**2. Diplomatic visit.** Social, guests and the galley.
- *Warning (two days ahead):* Mail from Commander Vance: a Veyli delegation of four arrives on Day X. Chief Holt grumbles in chatter. Event jobs: get the visitors' suite and the second visitors' cabin ready (heaters up: the Veyli like it warm), fix the Captain's dining-room lamp, carry gift crates from the hold. The laundry spikes with dress uniforms.
- *Onset:* **gathering in the shuttle bay, 10:00:** a Veyli shuttle docks (or the Tern brings them), the delegation walks down the ramp, Envoy Saruth and the Captain greet them, the crew line the bay. The guests move into Deck 2.
- *Escalation:* formal dinners in the Captain's quarters (an extra galley batch with Veyli dishes that need herbs from the garden, so the garden's condition matters); a tea ritual in the observatory; tours of the ship (guests walk through the decks with an officer). Holt and a delegate clash over something small: a tense line spreads as gossip. [Tier 3+: you're at the table.]
- *Resolution:* the gift exchange in the observation room; the delegation leaves from the shuttle bay.
- *Threads:* dinners on time; guest cabins comfortable; the garden's herbs; crew courtesy (crew mood, Holt above all).
- *Goes well:* a Veyli cord sculpture is given to the ship and hangs in the bow lounge; Saruth warms to you if you helped. *Goes badly:* a stiff farewell, Holt's line becomes a running joke, no gift.

**3. Something in the garden.** Food, a hunt, and a new pet.
- *Warning:* nibbled leaves; a herb rack stripped; small tracks in the garden's soil; things moved in storage. Crew blame each other in chatter.
- *Onset:* the herb wall is bare one morning. Brennan is furious (Mail); the menu loses its herby dishes; food quality drops (meals restore a little less).
- *Escalation:* sightings on other decks ("Something ran under the bunks in Bunk 6!"). Event jobs: make traps in the machine shop (a real fabrication job), set them where it's been seen, check them each morning; **volunteer garden watch** at night.
- *Resolution:* a **gathering** when it's caught: a small, harmless creature (perhaps a stowaway from the last supply crates), the garden crowd around it, someone names it.
- *Threads:* crop loss; how long the menu stays bland; how many traps were set and checked.
- *Goes well (any outcome, really):* the creature becomes **the ship's pet**, lives in the garden, wanders the Commons and shows up in chatter for the rest of the game. How well it went decides how soon the garden recovers.

**4. Shipboard illness ("the Wren cough").** Fewer hands, more work.
- *Warning:* a few people coughing in the mess; Rina mentions it.
- *Onset:* the infirmary fills. Sick crew stay in their bunks (a schedule rule: bunk all day, a nurse visits). One bunk room is quarantined (a closed door with a sign).
- *Escalation:* about a fifth of the crew are off; the Works crew are short, so more jobs are left for you; soup goes to the bunk rooms by cart. **You can catch it** if your hygiene is low: energy drains faster and rest helps; no worse than that.
- *Resolution:* the last patients leave the infirmary; Rina and Dr. Nandakumar are exhausted (bring them tea: a favour).
- *Threads:* jobs left undone; how many caught it; how long the infirmary stayed full.

**5. Nebula drift.** Beautiful, sleepy and chatty.
- *Warning:* a visiting scientist arrives (guest cabin on Deck 4) and the observatory is booked.
- *Onset:* **felt everywhere:** every window fills with nebula colour (the sky mood changes on every deck). The sensor array overloads [Tier 3: array jobs; Tier 1: carry coolant].
- *Escalation:* strange dreams: crew sleep worse (energy refills slower) but are chatty (social restores faster, more people in the lounge late); dream gossip ("I dreamt the Admiral could talk"). The observatory is full every night.
- *Resolution:* the ship drifts out; the scientist gives a talk in the observation room (a gathering).
- *Threads:* survey data gathered (array condition); how tired the crew got.
- *Trace:* a framed nebula photo in the observatory.

**6. Salvage.** The shuttle flies, and the hold fills.
- *Warning:* Survey finds a derelict. Chatter about what it might be.
- *Onset:* **gathering in the shuttle bay control booth and lobby:** the bay doors open and the Tern flies out (the first time the shuttle moves: an animation of the bay doors and the shuttle leaving). [Later: you go aboard.]
- *Escalation:* the Tern comes back with crates: the cargo hold fills with odd finds that need sorting (cart jobs), one crate holds an old but excellent part, and perhaps survivors move into the guest cabins.
- *Resolution:* the finds are shared out; a "salvage auction" evening in the lounge with odd objects.
- *Threads:* crates sorted; the salvaged part fitted.
- *Trace:* a permanent improvement (the salvaged part makes one machine wear slower) and an odd object on a shelf somewhere. **Proposal:** salvage can lead straight into "Something in the garden" (the creature came from the crates).

### More event ideas

- **Founders' Day festival** (a happy event, and the crowd test): the plaza decorated, the galley's big feast, a talent night in the bow lounge, the whole crew together. Good for showing off crowds over 70.
- **Power surge:** a one-day event centred on Deck 6; a junction trips and two decks lose power for a while.
- **A Veyli vessel needs help:** their ship limps alongside; Works sends parts; one Veyli engineer comes aboard (a guest). A seed for later away jobs.
- **The déjà vu day:** a time anomaly replays one day. Seeded routines make the replay exact; only you (and maybe Saruth) notice. A favourite for later, because it shows off the simulation.
- **The late supply shuttle:** rationing, a bland menu, filters short, the machine shop busy. Fully from the numbers (tonight's shortage Mail grows into this).
- **Crew rotation day:** five crew leave on a transport and five new faces arrive; goodbyes in the lounge, new names in Crew.
- **Comet viewing:** one evening, the observatory and the bow lounge windows; a gentle gathering, no strain.

**Proposal: event order.** Ion storm first (agreed), then the diplomatic visit, then something in the garden (salvage can lead into it later). The storm comes about a week and a half into a new game, then one main event every 1–2 ship weeks, with small incidents (birthdays, traditions, arguments, guests) on most days, as the design doc says.

### How events tie into what's already built

| Built system | During an event |
| --- | --- |
| Machines and wear (17) | `eventMod('wear', system)` multiplies wear; visible fault looks (`machineLook`) do the rest |
| Jobs (17) | Events add jobs with an `event` tag and tier; Works crew take them as usual |
| Schedules (14) | Event rules: double shifts, closed rooms, sick in bunk, gatherings, appointments |
| Galley (16) | Menu changes, extra batches for guests and dinners, trays by cart, spoilage when the chiller strains |
| Needs and mood (14, 15) | Small multipliers (worse sleep, chattier crew); mood follows threads ("grumbling about the dark") |
| Mail (15) | Notices, addresses, debriefs, commendations |
| Traditions (18) | Pause or change during an event (no observatory night in a storm); a party after |
| Crowd (8b) | Gatherings, the coarse level of detail, poses for "looking up" and clapping |
| Decks (4d) | Event dressing as optional places and props (traps, sign-up sheets, decorations, traces) |

---

## Part 3: social life basics

Built on what exists: crew needs, feelings on tap, habits that change, birthdays and tonight's traditions.

### Relationships with you

- **Proposal:** `SHIP.rel[crewId] = { pts, tier, met, lastTalk, known: [] }`. Five tiers, by points: stranger (0), acquaintance (10), colleague (30), friend (60), close friend (100). Points never drop, or drop very slowly after weeks apart (design doc: cozy).
- **How it grows** (biggest first, per the design doc): working a job together (both at the same machine, or a team job) **+6**; eating at the same table **+3**; a chat, once per person per day **+2**; a favour done **+8**; being told news first **+1**; keeping an appointment **+3**; a birthday wish on the day **+3**. Starting numbers, for the social engineer to tune.
- **What tiers unlock** (design doc): they greet you; they tell you about their life; they show on Maps; they come and find you in free time; they invite you; friends cover a job, tip you off about spare parts and put in a good word with Calder (it shows in the Record app).

### Conversations (tap a person)

**Proposal: a short chat card, not a dialogue tree.**

- **The card:** their face, name, rank and tier; one line from them, picked in order of what matters: an event or news item they know → how they feel (`crewFeeling`) → something about the ship near them → a life detail (for acquaintances and up) → a greeting.
- **Three or four buttons:**
  - **Chat** (counts once a day: social up for both of you, relationship points);
  - **Ask about…** (news, their work, home: each fills in a line in Crew's "what you know");
  - **Help?** (if they have a favour to ask, it's offered; accepting adds it to Jobs);
  - **Meet up** (opens Appointments with them already picked).
- **Lines are templates filled in from the simulation** ("The {machine} on {deck} has been {symptom} all week"), with about ten variations per kind and per tier, so it doesn't repeat quickly. No AI writing, as the design doc says.
- **Hygiene matters** (tonight's table): chatting while grubby gives half the social, and some crew remark on it.

### Crew relationships with each other

- **Proposal:** an affinity number for every pair of crew (75 × 74 / 2 = 2,775 small numbers, cheap to store and save), starting from traits (same department, same bunk room, shared habits) with a little seeded variety.
- **It drifts on paper** once a ship hour from who spent time together (the same "who is where" the news model uses). Most pairs drift slowly toward friendly; a few pairs with clashing traits drift the other way.
- **What it changes:** who sits together in the mess and the lounge (section 14 seating), who swaps shifts (later), who avoids whom, and what they say about each other in chatter. Friends of your friends warm to you a little faster.
- **Small dramas:** when a pair crosses into rivalry or friendship, it becomes a news item ("Pell and Rina aren't speaking"), and sometimes a small incident: an argument in a corridor that you can smooth over (a chat with each), a reconciliation over dinner.

### Crew seeking you out, and favours

- **Friends come and find you** in their free time if you're on the same deck: they walk over, greet you, and a chat card is offered as a small prompt at the screen's edge (never a pop-up you must answer).
- **Favours** grow from their lives and the ship: "My cabin lamp flickers", "Could you bring a tray up to Tomas, he's ill", "I left my datapad in the gym". Each is a personal job in Jobs, completed physically like any other job.

### Mood

- **Proposal:** mood stays `crewMood(p, t)` (tonight), blended from needs, ship health, the event's threads, recent time with friends, and birthdays and traditions. It shows in tap lines, chat lines, posture (a slower walk when low) and who goes to the lounge.

### Story crew arcs (the first three)

- **Proposal:** start with the three closest to you: **Tomas** (your bunkmate), **Pell** and **Rina**. Each gets four beats that open at acquaintance, colleague, friend and close friend: a small personal thread (homesickness and a call home that goes wrong, a hobby that becomes a little show at the music room, a worry about a family member) told through chats, an appointment or two, Mail and one small gathering. Arcs for the Captain, Vance, Calder, Brennan, Holt and Saruth come later.

---

## Part 4: progression hooks (the user's request)

These are moments of trust, not new rules; the full tier-2 promotion stays in the next pillar. **Proposal:** each is opened by something you earned, and each is an appointment (a time window that unlocks the door).

| Hook | How you get there | What happens |
| --- | --- | --- |
| **The Captain's ready room** | Summoned after your first commendation (an event you did well in), or by Vance once you're friends | Your first time inside. The Captain thanks you, asks about the ship from a junior's view, and the Admiral (the fish) is introduced. Mail afterwards. A permanent line in Record. Later visits when summoned. |
| **The conference table** | Calder takes you along to an event briefing in the observation room ("bring the filter numbers") when your Works record is good; by right from Tier 3 | A short meeting at the table: the senior crew around it, the briefing screen showing the event, a few lines each. You hear the plan before the rest of the crew; your device gets the briefing as a memo. Crew around you take their seats and leave like any meeting. |
| **Officers' quarters** | An invitation from an officer friend on Deck 4 ("Tea in my cabin after shift?") or a senior friend on Deck 2 | The private cabin's door opens for the appointment's window. A chat in their cabin counts double. |
| **The Captain's table** | A monthly dinner in the Captain's quarters; the Captain invites one junior who stood out (an event, a commendation, many close friends) | The galley cooks a special dinner (an extra batch); the senior crew at the table; you seated at the end. A gathering with a guest list. A trace: a framed menu in your locker. |
| **Progress talks with the Chief** | An appointment in Calder's glass office, any time | Where she tells you how close certification is: a bridge into the next pillar's promotion. |

**Locked doors stay locked** except during an invitation or summons (the ready room, Deck 2 bedrooms, officers' cabins), through one rule in the hatch and door check (`doorOpenFor(room, who, t)`), owned by the sim engineer with the architects.

---

## Part 5: ideas carried in

From the lead and the helpers' handovers, not yet scheduled anywhere:

- **Gym equipment, "more later"** (the user): **Proposal:** add a punch bag, a rowing pair and a stretching mat during Pillar 3 so the fitness-minded crew have more to choose from, with places and poses. Bridge architect (Deck 3) and performance engineer.
- **Ready room for the player** (bridge architect), **inside a bedroom / the Captain's table** (command architect): Part 4.
- **The second visitors' cabin** stays for event visitors: Part 2.
- **The observatory as a gathering place** (command architect): nebula drift and comet viewing.
- **Queues at a big event** (galley): formal dinners and the storm's call-home rush.
- **Supplies short as a story beat** (systems): the late supply shuttle event.
- **The cargo hatch** (now open) and the shuttle flying: salvage.
- **Crawlway crouch** (tonight): crawlways become event shortcuts (a Works junior who knows them gets to a blackout first).
- **Deck 6 crawlways' second inspection points** (Deck 6 architect): with the power-surge event.
- **Machines facing the camera** (command architect): a small tidy-up for whoever touches Deck 2 next.
- **Sound** (the lead): the game is silent. **Proposal:** a small sound pass in Pillar 3 or right after (a device chirp, a soft ship hum per deck, the storm's crackle, the address chime), all made in code like the textures. This is where the Music app comes from.
- **Character creation** (open question): left for the user; the Crew app and photos would make it more personal.

### The real-phone test

The user agreed to test on a real phone (answers pass, item 34). **Proposal: the checklist**, run on the TriFold folded and unfolded, at the start of Pillar 3 and again after the festival:

1. Load time from tapping the link to the first frame.
2. Smoothness on each deck by the lift and zoomed out (does it judder?).
3. The mess hall at dinner (the busiest normal moment), and the `?crowd=120` demo.
4. The lift ride: is the pause hidden by the fade on every deck?
5. Heat and battery after 20 minutes of play.
6. The device: opening, scrolling, tapping small things, typing a memo with the on-screen keyboard.
7. Folding and unfolding while playing (does the layout follow?).
8. Closing the browser and coming back: does it resume where you left off?

The lead turns the user's answers into fixes for the performance engineer and the device engineer.

---

## Workstreams and owners

| # | Workstream | Owner | Section of the game file | Builds |
| --- | --- | --- | --- | --- |
| C1 | The device: two layers, home screen, the shim for `addSection`, notifications, phone and wide layouts, the save part; moving Needs, Jobs and Mail onto it | **Device engineer (new)** | new `// 19. DEVICE`, small hooks in 15 and 11 | 0.35.x |
| C2 | Device apps: Schedule, Calendar, Memos, Maps (drawn from deck data), Ship, Record, Wallet, Camera | Device engineer | 19 | 0.35.x |
| C3 | Appointments and invitations: the app (C1) and crew keeping them in `planDay`; `doorOpenFor` | Device engineer (the app), **sim engineer** (crew side, doors) | 19, 14 | 0.35.x, 0.26.x |
| C4 | Social: relationships, chat cards and line templates, crew affinity, seating by friendship, crew seeking you out, favours, the first three arcs | **Social engineer (new)** | new `// 20. SOCIAL` | 0.36.x |
| C5 | The news model: items, spreading on paper, chatter bubbles, the Ship news feed; gossip from faults, habits, birthdays and guests | Social engineer, with the performance engineer (the bubble) | 20, 8b | 0.36.x |
| C6 | Ship-wide events: the event format, phases, `eventNow` and `eventMod`, threads and bands, traces, the Captain's address, moments; then the ion storm | **Events engineer** (grows from tonight's traditions) | 18 | 0.34.x |
| C7 | Event hooks in each system: wear and jobs (systems), routines and gatherings (sim), menus and batches (galley), shake, flicker and sky moods, the coarse crowd at gatherings (performance) | Systems, sim, galley, performance engineers | 17, 14, 16, 8/8b, 5 | their ranges |
| C8 | Guests: templates, event guests, everyday visitors, guest schedules | **Crew designer** (data), sim engineer (schedules) | 9, 14 | 0.16.x, 0.26.x |
| C9 | Places for gatherings (`gather` groups), event dressing and traces, the ready room and Captain's dining room as visitable places, the extra gym kit | **Architects** (bridge: 1, 3; command: 2; Deck 6 architect: 4, 5, 6) | `DECKS[n]`, kit | 0.31.x, 0.32.x, 0.30.x |
| C10 | Progression hooks: the summons, the briefing, invitations, the Captain's table | Events engineer (the occasions), social engineer (who's invited), sim engineer (doors) | 18, 20, 14 | as above |

**Proposal: hiring.** Two fresh sessions (device engineer, social engineer); the events engineer from tonight carries on into ship-wide events; the existing helpers (sim, systems, galley, performance, crew designer, the three architects) each take their rows. Any helper over about 500k of memory hands over to a fresh session before starting (the user's handover rule).

**Build numbers.** Combined builds on `claude/ship-integration` are **0.50.0, 0.50.1, ...** (the lead). Helper ranges continue from wherever tonight's answers pass ends for existing roles (for example sim 0.26.x, performance 0.27.x, player 0.28.x, galley 0.29.x, Deck 6 architect 0.30.x, bridge 0.31.x, command 0.32.x, systems 0.33.x, crew designer 0.16.x), the events engineer keeps 0.34.x, and the two new roles get **0.35.x (device)** and **0.36.x (social)**.

## Shared formats

The owner of each may refine its details, but must tell the lead and keep the other sessions' side working.

```js
// 19. DEVICE (device engineer)
deviceApp({ id, title, icon, order, badge, view })   // view(ctx) -> VIEW (plain content)
deviceDo(action)  deviceNotify({ app, text, urgent })  DEVICE_SKIN
device.addSection(id, title, render)                // kept as a shim
SHIP.device = { memos: [], appts: [], readMail: {}, pins: [], settings: {}, photos: [] }   // saved, v 3
// appointment: { id, with: [crewId|'guest:id'|'place:id'], at: shipMin, len: 30, where: placeId,
//                kind: 'social'|'work'|'checkup'|'meeting'|'summons'|'invite', status: 'asked'|'yes'|'no'|'kept'|'missed', by }

// 20. SOCIAL (social engineer)
SHIP.rel[crewId] = { pts, tier, met, lastTalk, known: [] }     // saved
relAdd(crewId, why, pts)  relTier(crewId) -> 0..4
SHIP.aff: Int8Array(2775) (pair index i<j)                     // saved compactly
affinity(a, b) -> -100..100
NEWS: [{ id, about, lines, weight, seed, born, event }]  SHIP.knows[newsId] = Set of crew (saved compactly)
playerHeard(newsId, from)  chatLine(p, t) -> { text, news? }   favourOf(p) -> job | null

// 18. SHIP EVENTS (events engineer)
SHIP_EVENTS.<id> = { title, days, earliest, phases, systems, routines, galley, jobs, news, moments, threads, traces }
SHIP.event = { id, startDay, phase, threads: {}, mine: {} } | null;  SHIP.eventLog: [...]   // saved
eventNow() -> { id, phase, day } | null
eventMod(kind, key) -> number | rule | null          // every reader treats null as "no change"
captainAddress({ lines, at })                        // the banner on every deck, copied to Mail
gathering({ id, where, at, len, who })               // section 14 fills it from 'gather' places

// 14. SCHEDULES (sim engineer): planDay reads appointments, event routines and gatherings
doorOpenFor(room, who, t) -> bool                    // invitations and summons

// 9. CREW DATA (crew designer)
GUESTS: [{ id, name, spec, role, cabin, arrive, leave, template }]

// Places (architects): optional gather: '<venue>' on a place; optional event: '<id>' for event dressing
```

## Order

1. **First (in parallel):**
   - C1 (device engineer: the two layers and moving today's sections over, with no change to play);
   - C4's data (social engineer: relationships, affinity and the news model on paper, with a `social_check.py` in the style of `day_check`);
   - C6's format (events engineer: the event format and phases on paper, an `events_check.py` that runs a storm for 4 days with nothing drawn);
   - C8 (crew designer: guest templates).
   - The real-phone test with the user, so the device and crowd work start from real numbers.
2. **Then:** C2 and C3 (apps, appointments), C4's chat cards and seeking out, C5's chatter, C9 gathering places.
3. **Check-in 1 with the user:** the new device with all the apps (in the plain skin), relationships and chats, crew who come and find you, appointments that crew keep, chatter you overhear. If the user's device design is ready by then, the device engineer builds the new skin next.
4. **Then:** C7 (event hooks in every system) and the ion storm end to end; C10's first hook (the ready room after a commendation).
5. **Check-in 2 with the user:** a full ion storm played through: warning, onset, the address, flickers and blackouts, storm jobs, the all-clear rush on the booths, the party, the debrief, the trace.
6. **After that, in this order unless the user changes it:** the diplomatic visit (guests, the second visitors' cabin, formal dinners, the Captain's table), something in the garden, then the festival as the crowd test once the phone numbers allow it.

**Tests every turn**, as in Pillar 2: `cadet_test.py`, `deck_check.py` on all six decks, `day_check.py`, and each new checker (`social_check`, `events_check`, a `device_check` that opens every app and checks it draws). Draw calls stay under about 450 everywhere, including at gatherings. Shared kit made at load never calls `R()`; all event randomness comes from the seed and the day, so a replayed day is identical (which is also what makes the déjà vu day cheap).

## Risks

- **Too much talk, too little ship.** If chatter, toasts and Mail all fire at once, the ship feels noisy. *Answer:* a single "voice budget": at most one bubble on screen, one toast at a time, and the address only at big turns.
- **The device design arrives late.** *Answer:* the two layers mean every app works in the plain skin; your design only replaces the skin.
- **Draw calls at gatherings.** 75 crew plus guests in one room could break 450. *Answer:* the coarse level of detail, gatherings checked in `day_check`, the festival held back until the real-phone test passes.
- **The save grows.** Relationships, affinity, news, events and photos all add to it. *Answer:* compact formats (affinity as small numbers, news knowledge as bit sets), photos in the browser's separate storage, a size line in each checker.
- **Events feel like nothing happened** if the effects are too gentle, or like punishment if too harsh. *Answer:* tune the ion storm first on paper with `events_check` (blackout minutes, food spoiled, jobs left) and play it through before check-in 2.
- **Section owners collide.** The event layer touches every system. *Answer:* the events engineer only publishes `eventNow` and `eventMod`; each owner adds its own small, inert check (null means "no change"), as with `shipEffects`.
- **Determinism.** News spread, affinity drift and event timing must replay exactly. *Answer:* everything seeded per person per day, like time jitter; checkers run twice and compare.
- **Memory of the helpers.** Several sessions are near full. *Answer:* hand over before starting (the user's rule), fresh sessions for the big new jobs.

## Decisions for the user

1. The device's **two layers** (apps describe, a skin draws), opening from a corner button or a swipe up, never pausing time.
2. The **extra apps:** Crew, Ship, Camera, Record (and Wallet; Music once there's sound).
3. **Maps shows people** only once you're acquaintances (or they're on public duty).
4. **Missed appointments** cost nothing but a remark.
5. Events are **ambient**: news by chatter, Mail, boards and the Captain's address; no markers or cutscenes; **no forced camera**.
6. Outcomes in **three bands** (smoothly, bumpily, roughly) from 3–5 threads measured from the simulation; your own part counted separately for commendations; results told as story and traces.
7. **Three kinds of moment:** felt everywhere, the Captain's address, gatherings at a place and time.
8. **Event order:** ion storm, diplomatic visit, something in the garden; festival as the crowd test after the real-phone test.
9. **Everyday guests** about once a ship week, plus event guests; the second visitors' cabin for event visitors.
10. **Relationship numbers** as above, chat cards with three or four buttons, crew affinity on paper, the first arcs for Tomas, Pell and Rina.
11. **Progression hooks** as appointments that unlock a door for their time: ready room, conference table, officers' quarters, the Captain's table, progress talks.
12. **Extra gym kit** now, and a **small sound pass** in or right after Pillar 3.
13. **Hiring** a device engineer and a social engineer; the events engineer grows into ship-wide events; builds 0.50.x.

**Design-doc updates when agreed** (the lead, on the lead branch): "The player" (the device and its apps), "Social life" (numbers, chats, affinity, news), "Ship-wide events" (ambient rule, shape, threads and bands, moments, guests, the six events and order), "Works progression" (the hooks), "Milestones" (Pillar 3 as planned here), and move these answered questions out of "Open questions": the device; which event comes after the ion storm; the second visitors' cabin (already answered: kept for event visitors); how often Deck 4's guests change.
