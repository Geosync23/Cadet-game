# Pillar 3 plan: your device, the people aboard, and ship-wide events

**Agreed with the user on 2026-10-16** (their answers to the pitch, interpreted by the lead, who has the user's authority to interpret them). Each decision is marked **Agreed** or **Changed** with the date; "Changed" means the user's answer altered the proposal, and the text shows the agreed version. Every Pillar 3 session works from this file. If something here is wrong, tell the lead; don't work around it. Read with `design-doc.md` (above all "Vision & pillars", "The living ship", "Crew simulation", "Social life", "The player", "Works progression", "Ship-wide events" and "Open questions"), `plans/pillar2-plan.md`, `plans/answers-pass-plan.md`, `TEAM.md` and `DEV_NOTES.md`.

---

## The pitch (one page, as agreed)

After Pillar 2 the Wren works: the galley cooks, machines wear, the Works crew fix them and so can you. After tonight's answers pass it also has birthdays, observatory nights, crew who look tired when you tap them, and a simple Mail inbox. **Pillar 3 gives that ship a voice, a social life and its first stories.** It has three parts, built side by side:

1. **Your personal device becomes the game's main screen.** One device, many small apps: **Schedule, Appointments, Maps, Memos, Mail, Calendar, Needs and Jobs**, which you asked for, plus **Crew** (a contacts list), **Ship** (status and news), **Record** (your Works progress) and a small **Wallet**; **Music** comes later with sound. It's built in two layers (apps describe, a skin draws), and the real skin is built now: **an old-school screen**, with scan lines, a phosphor glow and chunky type, like looking at an actual device's display. The ship keeps running while it's open.
2. **The crew become people you know.** Each crew member has a relationship with you (stranger, acquaintance, colleague, friend, close friend) that grows by working, eating and talking together, and by doing them favours. Tapping someone opens a short chat, with no dialogue trees: they greet you by how well they know you, and tell you how they feel, what's going on aboard, or something about their life. Crew also like or dislike each other, so friendships and small rivalries grow on their own. Friends come and find you, invite you to things and put in a good word with the Chief.
3. **Ship-wide events begin, and they're ambient.** Your idea is the core of the design: *the key is they are ambient and everyone talks about them.* There are no cutscenes and no mission screens, and the game never stops. An event is a few days in which the ship's systems, the crew's routines and the decks change. News reaches you the way it reaches everyone: crew chatter first, then Mail, the job board, and finally the Captain's ship-wide address. You decide how much to get involved. How well it goes comes from what actually happened on the ship, not from a pass or fail. A few big **moments** (the storm front hitting, the delegation stepping off the shuttle) are announced ahead, happen in a real place at a real time with the crew gathered, and can be felt on every deck, so they never need the camera taken away from you. An event can also call a **meeting with dialogue** (a briefing, a summons, a greeting): if you're there, the people's lines play one by one in a panel, sometimes with a choice of reply, while the ship keeps running. It is never a full cutscene.

**The events, all kept, in order:** 1 the **ion storm** (touches every system), 2 a **diplomatic visit**, 3 **something in the garden**, 4 **shipboard illness**, 5 **nebula drift**, 6 **salvage**, 7 **the déjà vu day**, with six shorter events slotted between them (Founders' Day festival, power surge, a Veyli vessel needing help, the late supply shuttle, crew rotation day, comet viewing). Pillar 3 builds the event framework and the ion storm first, then works down the list. Nothing is dropped.

**Progression hooks:** your first time inside the Captain's ready room (summoned after a commendation), sitting in on a briefing at the conference table, tea in a friend's cabin, and an invitation to the Captain's table.

**How it's built:** three new helpers (device, social, and the events engineer you already have, who grows from traditions into ship-wide events), with the existing helpers doing small parts. Two check-ins with you: one after the device and social basics, one after the ion storm. Combined builds are **0.50.x**.

**What the user decided (2026-10-16):** yes to everything in "everything else"; the device's two layers, but with the real CRT-style skin built now and no Camera; ambient events, with meetings with dialogue added; and the full event list kept, in order. See "The user's decisions" at the end.

---

## Where we start (after tonight)

- **Pillars 3 and 4 meet here.** The design doc's milestones list Social as Pillar 3 and Events as Pillar 4. **Agreed (2026-10-16):** Pillar 3 builds the social basics and the *start* of events (the framework and the ion storm) together, because events are mostly people talking; the later events then follow as their own pillar.

- **The build** (0.41.x tonight, on `claude/ship-integration`): 75 crew on schedules (section 14), needs for crew and player (14, 15), the galley (16), machines, jobs and supplies (17), and section 18 `SHIP EVENTS`, small recurring traditions from the events engineer.
- **The device today** is a placeholder panel (section 15) with registered sections: `device.addSection(id, title, render)`. It has Now, Needs (with tonight's bonus and penalty marks) and Jobs, plus Mail (`mailSend`, `SHIP.mail`).
- **Crew feelings:** `crewMood(p, t)` and `crewFeeling(p, t)` give the tap line. Birthdays (`ROSTER[i].birthday`), habits that change (`SHIP.habitLog`), observatory night, the Deck 1 shift handover and the Captain's evening walk all exist or arrive tonight.
- **Tonight's interactions work** (the interactions engineer, section 15b, builds 0.37.x): the player can use everything the crew use (treadmill, rower, bar, music, garden, laundry, games and more); job-board pick-and-take; an on-screen goal arrow, `setGoal(target)` and `clearGoal()`; sit anywhere (tap a free seat); and squeezing past crew who are settled in a spot.
- **Not there yet:** no relationships, no conversation, no way to talk to crew beyond a toast, no guests, no events beyond traditions, no map, no appointments. The ready room and private bedrooms are locked. No sound at all (the game has no audio code).
- **Crowds:** the crowd draws all 75 cheaply; tonight adds a third, coarse level of detail and a `?crowd=120` demo (performance engineer).

---

## Part 1: the personal device

### What it is

**Agreed (2026-10-16):** the device is a small handheld (or wrist) computer every crew member carries. It holds your day, your messages, your notes and the ship's news. It's **the only menu in the game**: there are no other panels. It opens instantly and never stops time (no time controls, as you decided).

### Two layers, and the real skin now

**Changed (2026-10-16):** the device is built as two separate layers, as proposed, but the user doesn't want to wait for a later design: **the real skin is built now** (see "The device look" below). The layers stay, so the look can still be changed later without touching the apps.

1. **The apps (how it works).** Each app is a small piece of code that returns *plain content*: a title, lists of rows, a few buttons, a badge count. It never builds the screen itself. Example: the Jobs app says "three rows: *Scrubber 2, Deck 4, urgent*, with a Take button", and nothing about colours, fonts or layout.
2. **The skin (how it looks).** One piece of code turns that plain content into what you see. The first skin is the CRT screen described below; tonight's plain panel is retired. Any later skin replaces it with every app working unchanged.

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

### The device look: an old-school screen

**Agreed (2026-10-16):** the user's look. Opening the device should feel like looking at an actual device's display: an old CRT or phosphor screen set in a sturdy bezel.

- **Scan lines, interlaced:** one overlay on top of the screen, a repeating gradient of fine dark lines (about one dark line every 3 CSS pixels at roughly 20% darkness), with every other line very slightly brighter for the interlaced feel. Never drawn into the text itself, so letters stay sharp.
- **Phosphor glow:** text and lines carry a soft glow (a small text shadow in the phosphor colour, about 4 pixels at half strength). Bright items (alerts, the selected row) glow a little more.
- **Curvature and vignette:** the screen has rounded corners (about 18 pixels), an inner shadow and a gentle radial darkening toward the edges, which suggests a curved glass face. **No 3D transforms on text**, because they blur it on phones.
- **Flicker or roll (optional):** a very faint brightness flicker and a slow soft band rolling down the screen every few seconds. Both are off when the phone asks for reduced motion (`prefers-reduced-motion`), and there's a "Screen effects" switch in the device's settings.
- **Chunky, readable type:** a monospace system font (no download), at least 17 pixels for body text, uppercase headings with a little letter spacing, line height about 1.35. Body text keeps at least a 7 : 1 contrast with the screen background after the scan lines.
- **The bezel:** a dark frame with a small label ("CSV WREN · CREW PDA"), a power light that blinks for new mail, and the Back and Home buttons as physical-looking keys at the bottom.
- **Phones first:** crisp at phone size, every touch target at least 44 pixels, nothing smaller than 15 pixels anywhere.
- **Cheap to draw:** CSS and DOM only. No extra WebGL draw calls, no canvas, no blur filters over the game, no `backdrop-filter`. The only animation is the optional roll, done with a transform.

**Style tokens** (the device engineer proposes the final phosphor colour to the lead, with screenshots of each option):

| Token | Amber (option A) | Green (option B) | Wren cyan (option C) |
| --- | --- | --- | --- |
| `--crt-ink` (text) | `#ffb347` | `#5dff8a` | `#6ff0dc` |
| `--crt-dim` (secondary text) | `#b8803a` | `#3fae63` | `#46a99b` |
| `--crt-bg` (screen) | `#140c03` | `#041309` | `#03141a` |
| `--crt-hot` (alerts, selected) | `#fff1d6` | `#e6ffe9` | `#e8fffb` |
| `--crt-glow` | `rgba(255,170,60,.5)` | `rgba(80,255,130,.45)` | `rgba(95,227,208,.45)` |

Shared tokens: `--crt-scan: rgba(0,0,0,.2)` every `3px`; `--crt-radius: 18px`; `--crt-font: ui-monospace, "Cascadia Mono", Menlo, Consolas, monospace`; `--crt-size: 17px`; `--bezel: #1b1f24`. Option C matches the Wren's teal; option A is the most classic.

**The dialogue panel** (for meetings, Part 2) uses the same screen style: a strip across the bottom of the game, or the device itself if it's open.

### How it opens and works on a phone

- **Agreed (2026-10-16): opening.** A device button in a screen corner (where today's button is), and a swipe up from the bottom edge. It opens on a **home screen**: the time and day, your next item ("Shift starts 08:00", "Dinner with Pell, 18:30"), any active event in one line, then the grid of apps with badges.
- **Agreed (2026-10-16): phone (portrait).** It slides up as a sheet covering about two thirds of the screen, so the ship stays visible above it. Back goes to the home screen; tap the ship or swipe down to close.
- **Agreed (2026-10-16): the TriFold unfolded (wide).** It docks as a side panel on the left and can stay open while you walk. This suits the Maps and Jobs apps.
- **Touch first:** every tappable thing at least 44 pixels high, no hover, no tiny text.
- **Notifications:** a soft chirp (when we add sound) and a toast for urgent things (your job's machine broke, an appointment in 10 minutes, the Captain's address). Everything else is a quiet badge. **Agreed (2026-10-16):** a "Quiet off shift" setting that turns work notifications into badges after 17:00.
- **While it's open,** the game keeps running and you keep walking if you were. Tracking a job or favour, or tapping a map pin or a gathering note, points tonight's goal arrow at it (`setGoal`, section 15b). There is **one arrow in the game, never a second system.**

### The apps

Your eight first, then the extras. **Changed (2026-10-16):** all the proposed extras are agreed **except Camera**, which is dropped (and photos with it, everywhere).

| App | What it does | Built from |
| --- | --- | --- |
| **Schedule** | Today as a timeline: shift, meals, your appointments, gatherings, birthdays, event moments. A week view with the rota and your days off. A strip says where you're expected right now ("On shift: Works bay"). | Your rota (section 13/14), section 18 traditions, Appointments, events |
| **Appointments** | Make one: pick a person or a place (a crew member, the infirmary, the Works Chief's office, a meeting), a time and a spot. Crew answer from their real schedule: yes, "not then, how about 19:00?", or no. Accepted appointments go into their day and they turn up. Invitations from crew arrive here too. | New: section 19 (the form), section 14 (crew keep them) |
| **Maps** | Each deck as a clean plan drawn from its deck data: rooms named, you as a dot, locked rooms hatched. Search a room or a person; a person shows where they are now, if you know them well enough (see below). "Show on map" and "Go there" point the goal arrow (`setGoal`) at the room or person; on another deck the arrow leads to the lift first. | The deck text maps in `DECKS`, `whereIs` |
| **Memos** | Notes you write. Plain text, a title, the date. Pin one to the home screen. **Agreed (2026-10-16):** a "remember this" button on chats, Mail and job lines copies the line into a new memo. | New, saved |
| **Mail** | Tonight's inbox, grown: from the ship (shortages, spoilage), crew (invitations, thanks), departments (event notices), the Captain (addresses, in writing), and home (replies to your calls). Read and unread, delete, "remember this". | `mailSend`, `SHIP.mail` |
| **Calendar** | A month of ship life ahead: the weekday shapes (Monday briefing, Wednesday drill, Thursday inspection, Friday treat, Sunday vote dinner), the Captain's piano on Thursdays, observatory night, birthdays, traditions, holidays, and announced events once they're known. Tap a day to add it to Schedule or make an appointment that day. | Section 18, `ROSTER.birthday`, events |
| **Needs** | Your five needs as bars, each with its bonus or penalty mark and a one-line reason ("Fed: energy drains 10% slower"), from tonight's `needEffects`. A line suggests what would help and where. | Section 15 |
| **Jobs** | **Changed (2026-10-16): tracks only.** Your jobs and favours: list, details, parts needed, which step you're on, and a **Track** toggle. The tracked one drives the goal arrow and the pins in Maps. No taking or dropping from the device: see "Jobs: take and turn in at the board". Event jobs carry the event's tag. | Section 17, social favours, 15b |
| **Crew** | Your contacts: everyone you've met, with face, name, rank, department, relationship tier, birthday, and what you know about them (filled in as they tell you). Friends show where they usually are at this hour. Message a friend; make an appointment from here. | Section 20 social, `ROSTER` |
| **Ship** | Ship health and each system's condition (as on the Works bay board), what's happening ("Ion storm: day 3 of 4"), and **Ship news**: everything you've heard, newest first, each with who told you and when. | Section 17, events, the news model |
| **Record** | Your Works record: tier, jobs done, early catches, commendations, what the Chief thinks ("Calder: steady, a bit slow on filters"), and how close certification is. Where progression shows. | Section 17; certification comes later |
| **Wallet** (small) | Credits and what's in your locker (tonight's shop buys). Could live inside Needs instead. | Section 15 |
| **Music** (later) | The music room's record cabinet on your device: a few procedurally made tunes. The game has no sound yet, so this waits for a sound pass. | A future sound pass |

**Agreed (2026-10-16): knowing where people are.** Maps finds rooms always, and people only once they're at least an acquaintance (or are on duty somewhere public: the chef in the galley, Rina in the infirmary). This makes relationships useful and keeps the map from feeling like surveillance.

### Seeing yourself use the device

**Changed (2026-10-16):** the user's addition.

- **Opening it:** your character visibly raises a small handheld and looks at it: a `device` pose holding a small glowing prop, its screen tinted in the chosen phosphor colour. **Closing it:** they put it away.
- **Walking while it's open:** a walk-and-read pose (head down, the device held in front).
- **Framing on a phone:** the sheet covers about two thirds of the screen, so the camera **eases** (no cut) to keep you framed in the visible top part while it's open, and eases back on close. On the unfolded TriFold the side panel needs no change of framing.
- **Cheap:** the prop is part of the player's rig or the crowd's existing props, costing 0 or 1 extra draw call.
- **Owners:** the performance engineer (the pose and prop), the player engineer (when you're holding it), the device engineer (the framing hook). They meet at two events, `deviceOpen` and `deviceClose` (see "Shared formats").

### Jobs: take and turn in at the board

**Changed (2026-10-16): a new rule.** You always **take** a job and **turn it in** at the job board: the Works bay board now, with more boards later if needed.

1. **Take it at the board.** Walk up to the board and pick a job (tonight's pick-and-take). It goes into your Jobs app.
2. **Track it.** In the Jobs app, switch **Track** on (a newly taken job is tracked automatically). The goal arrow and the Maps pins show the way, **step by step**: the board → storage (parts) → the machine shop (if a part must be made) → the machine → back to the board.
3. **Do the work** at the machine and places, as now (inspect, fetch, repair).
4. **Turn it in at the board.** The machine is fixed as soon as you finish, but the job only **completes** (your credit, your Record, the commendation count) when you turn it in at a board. Until then it waits as "done, waiting to be turned in".

- **The device's Jobs app tracks only:** list, details, parts, the current step, the Track toggle. No taking or dropping from the device.
- **Crew jobs are unaffected:** the Works crew still finish jobs where they do them.
- **Favours** (the lead's interpretation, **Changed (2026-10-16)**): in the same spirit, face to face. You **accept** a favour in person, in the chat, and **turn it in to that person** (find them and tap them; the chat card offers "Done: here you go"). It's tracked in Jobs the same way, and the arrow leads to them at the end.
- **Owners:** the interactions engineer (accepting and turning in at the board, tracking → `setGoal`; section 15b owns the board and the pointer), the systems engineer (the "done, awaiting turn-in" job state), the device engineer (the Jobs view and Track).

### Light onboarding: first tips

**Changed (2026-10-16):** a first step. Pillar 4 does the full onboarding and tutorials.

- **Short tips, shown once each,** remembered in the save, in the device's CRT style (a small card near the bottom of the screen). **They never pause time** and close with a tap or on their own after a while.
- **The first set is the job loop:**
  1. first time near the job board: "Take jobs here, and turn them in here when they're done."
  2. first job taken: "Track it on your device; the marker shows the way."
  3. first arrival at the job's machine: "Tap the machine to inspect. You may need parts from storage or the machine shop."
  4. the job's work finished: "Head back to the board to turn it in."
  5. first time the device opens: what the apps are, in one line each.
- **A settings switch** turns tips off.
- **Owners:** the interactions engineer (when tips fire), the device engineer (how they look).

### Appointments in detail (the user's request)

- **Making one:** Appointments → New → who or what → when (the next three days; times in 15-minute steps) → where (a suggested place, or pick one from the map).
- **Crew answer from their real schedule.** If the slot falls in their free time and they like you enough for that kind of meeting, they accept. If not, they offer the nearest free slot. Strangers accept only work matters (meeting the Works Chief, an infirmary check-up); friends accept anything.
- **Crew keep them.** An accepted appointment goes into that person's day (`planDay` reads it), so they walk there and wait about 15 ship minutes.
- **Agreed (2026-10-16): no punishment if you miss one.** They mention it next time ("Waited for you at the gym yesterday"), and it doesn't count as time together. Nothing is lost.
- **Places with a purpose:**
  - **The infirmary:** a check-up with Rina or Dr. Nandakumar shows your needs in words and gives a small rest bonus.
  - **The Works Chief's office:** a progress talk. Calder tells you where you stand toward certification. This is how the Record app's comments are earned.
  - **A meeting:** with two or more people at a table (the mess, the lounge, the junior common room). The conference room only through a briefing (see Part 4).
- **Crew make appointments with you:** friends invite you ("Gym at 18:00?", "Pond bench after dinner?"). Officers summon you (Calder: "My office, 09:30"). Invitations arrive in Appointments and Mail; accept or decline.

### Saving

- **Agreed (2026-10-16):** everything the device owns goes into the save through `SAVE_EXTRA` as `SHIP.device = { memos, appts, readMail, pins, settings }`. The save goes up one version: `SAVE_V` is 2 at 0.41.2 (e806e7b), so the device makes it **3** (or the next free number, if another pass bumps it first), and still reads older saves with an empty device.
- **Appointments** are also saved in the crew side (section 14 reads `SHIP.device.appts`), so a crew member still turns up after a reload.

---

## Part 2: ship-wide events (the main missions)

### The core idea: ambient, and everyone talks about it

Traditional games tell a story by taking over: a cutscene, a mission marker, a fail screen. That breaks two of our pillars, "the ship runs itself" and "you are one of the crew". So **Agreed (2026-10-16): an event is never a mission you're given; it's something happening to the whole ship that you live through.** You learn about it like everyone else, talk about it like everyone else, and help as much as you choose to.

What that means in practice:

| A traditional story mission | A Wren ship-wide event |
| --- | --- |
| A quest giver hands you the mission | You hear about it: a rumour, then Mail, then the Captain's address |
| A marker shows where to go | The ship changes around you: flickering lights, a closed lounge, new jobs on the board |
| A cutscene plays and time stops | A *moment* happens at a real place and time; crew gather; at most a meeting plays its dialogue in a panel; the ship keeps running |
| You succeed or fail | The ship comes out of it smoothly, bumpily or roughly, from what actually happened |
| The story is the same for everyone | What you see depends on your rank, your friends and where you were |
| After the mission, the world resets | Small permanent traces stay: a scorch mark, a plaque, a pet, a gift on a shelf |

### How an event is put together

**Agreed (2026-10-16):** each event is one block of data (like a deck definition), so new events are mostly writing, not code.

```js
// section 18. SHIP EVENTS (the events engineer; ship-wide events join tonight's traditions)
SHIP_EVENTS.ionStorm = {
  title: 'Ion storm', days: 4, earliest: 8,           // ship days; the soonest day it can happen
  // at: [day, minute] with day counted from 0 (the warning's day); the prose calls these Days 1-4
  phases: [ { id: 'warning', at: [0, 9*60] }, { id: 'onset', at: [1, 14*60] },
            { id: 'peak', at: [2, 6*60] }, { id: 'clear', at: [3, 10*60] } ],
  // what each phase changes, read by the sections that own those things:
  systems:  { onset: { wear: { power: 2, comms: 3 }, effects: ['flicker'] }, ... },  // section 17
  routines: { onset: [ { who: 'dept:command', rule: 'doubleShift' }, { where: 'lounge', rule: 'closed' } ] }, // section 14
  galley:   { peak: { menu: 'stormStew', grab: 1.5 } },                              // section 16
  jobs:     { warning: [ { kind: 'secure', where: 'lounge', tier: 1 }, ... ] },      // section 17
  news:     [ { id: 'readings', from: 'Sato', phase: 'warning', seed: ['dept:survey'], lines: [...] }, ... ],
  moments:  [ { id: 'front', phase: 'onset', where: 'shipwide', feel: ['jolt', 'lightsDip'] } ],
  meetings: [ { id: 'stormBriefing', phase: 'warning', at: [0, 8*60+15], where: 'works-bay', script: 'calderStorm' },
              { id: 'allClear', phase: 'clear', at: [3, 10*60], where: 'observation', script: 'captainAllClear' } ],
  threads:  [ { id: 'power', label: 'Keep the lights on', score: 'minutesOfBlackout', good: 30, bad: 180 }, ... ],
  traces:   { good: ['stormRosterTeaCorner'], bumpy: ['relayScorch'], rough: ['relayScorch', 'tapedPanel'] },
}
eventNow() -> { id, phase, day } | null              // anyone may ask; inert when null
eventMod(kind, key) -> number | rule | null          // e.g. eventMod('wear', 'power') -> 2
```

Every other section asks `eventNow()` or `eventMod()` and changes its own behaviour. The events engineer never edits another section's code; the other owners add one small, inert check each.

**Agreed (2026-10-16): the shape of every event** (the design doc's onset, escalation and resolution over 2–4 days, with a warning added in front):

1. **Warning** (hours to a day ahead, when it makes sense): a few people notice something. Rumours start.
2. **Onset:** the event arrives. A moment marks it. Systems, routines and the decks change. Event jobs appear.
3. **Escalation:** things get harder: more faults, tighter food, tired crew, a second moment.
4. **Resolution:** it ends, always. An all-clear, a gathering, a debrief.
5. **Afterglow** (a day or two): crew talk about it, mood lifts or sags, traces appear, commendations are handed out.

### How news spreads

**Agreed (2026-10-16): a small news model** (section 20, social, used by events and also by everyday gossip).

- **A piece of news** is a fact with a source and a few spoken versions: `{ id, about, lines: ['Sato hasn't left the chart room since last night.', ...], weight }`.
- **It starts with a few people** (the event's `seed`: whoever would know first: Survey sees the readings, the galley knows about the extra dinner).
- **It spreads on paper, hour by hour,** like everything else in the simulation: people who know it pass it on to people they spend time with (meals, the same work room, the same bunk room). Friends pass it on more readily than strangers. This costs almost nothing: it's a check per crew member per ship hour, using the same "who is where" that schedules already give.
- **Crew who know it talk about it.** You hear news in five ways, in roughly this order for a big event:
  1. **Chatter:** walk near crew who know something and you sometimes overhear a line as a small speech bubble ("They say the storm's the size of a moon"). Cheap: a text sprite on one nearby person, at most one or two at a time.
  2. **The tap line and chats:** tap someone and their line may be the news; chatting gives the fuller version.
  3. **Mail:** department notices ("Works: all hands to secure loose fittings by 12:00"), and later the Captain's address in writing.
  4. **The boards:** the Works bay job board gets an event banner and event jobs; the mess menu board changes; the ship health boards show the strain.
  5. **The Captain's ship-wide address:** for big turns only (onset, all-clear). See "Moments".
- **What you know is recorded.** Each news item you hear goes into the Ship app's news feed with who told you. Nothing is gated on knowing, but (**agreed, 2026-10-16**) a crew member who tells you something first gives a small relationship nudge ("being in the loop" is social).
- **Gossip uses the same model every day,** not only during events: ship faults ("The scrubbers on 4 have been rattling all week", from section 17), crew lives (birthdays, habit changes from `SHIP.habitLog`, rivalries), guests arriving. This is the design doc's "gossip is a hint system".

### How you learn and choose to engage

- **You're never told to do anything,** except by your job. If you're on shift, your work is Works work, and an event adds event jobs to the board like any other. Taking them is your choice, as now.
- **Rank decides which parts reach you** (design doc). At Tier 1 you carry filters, secure fittings, swap lamps and run carts. You're in a briefing only when it's held where you work (Calder's storm briefing is in the Works bay) or someone takes you along (see Part 4). Later tiers get the relay work and a seat at the table.
- **Ways in for a Tier 1 junior:**
  - **Event jobs** on the board, tagged with the event, taken, done and turned in at the board exactly like any other job.
  - **Volunteering:** some events put a sign-up sheet on a board (in the mess or the Works bay): "Garden watch tonight, 21:00–23:00", "Help set up the plaza for the festival". Signing up is an appointment.
  - **Asks from crew** you know: Brennan needs a hand carrying stew to the bridge; Rina asks you to check on Tomas.
  - **Just being there:** turning up at a moment, keeping people company, checking on friends.
- **Not engaging is fine.** If you sleep through the storm, the crew handle it, more slowly, and you hear all about it the next day.

### How outcomes are scored, with no fail screens

**Agreed (2026-10-16):** each event has **3 to 5 threads**: the things the whole ship is trying to keep right. Each thread is measured from what actually happened in the simulation:

- *Ion storm:* minutes of blackout across the ship, food spoiled, call-home backlog when comms return, how tired the bridge crew got.
- *Diplomatic visit:* dinners served on time, guest cabins comfortable (machines healthy), crew who were rude to the guests (Holt's mood), the gift exchange.

Each thread lands in one of **three bands: smoothly, bumpily, roughly**. The event's overall result is the blend.

- **The whole crew's work counts,** not just yours. You affect the result as one good pair of hands, a bit more than one average crew member, because you pick the jobs that matter.
- **Your own part is counted separately** (the jobs you did, the people you helped, the moments you turned up to). It decides your **commendation** (toward promotion), relationship gains and whether you're mentioned in the debrief. A smooth event you sat out still gets you nothing personal; a rough event you worked hard in still gets you thanks.
- **Results show as story, never as a score:**
  - the Captain's all-clear address says how it went in words;
  - Mail brings a debrief from your department, and maybe a commendation letter;
  - crew talk about it for days ("Lights only went once on our deck, thanks to Works");
  - **traces** stay: the storm crew's signed duty roster pinned up in the tea corner (smooth), a scorch mark in the relay room (bumpy), a taped panel and a scorch mark (rough), a new pet in the garden, a Veyli gift in the lounge.
- **Rough is never failure.** Every event ends; the ship gets shabbier and moodier for a while and recovers, exactly like neglected machines today.

### Moments without stopping the simulation

The hard question: how do you stage a few unmissable beats without cutscenes? **Changed (2026-10-16): four kinds of moment.** The user agreed the three proposed and added a fourth: an event can trigger a meeting with dialogue, but never a full cutscene.

1. **Felt everywhere.** Some beats happen to the whole ship at once, so you can't miss them wherever you are: the storm front hits (a short camera shake, every light dips, then flickers), the drive kicks in after the salvage, the nebula fills every window with colour. These are cheap effects on the current deck only (the other decks are on paper anyway). Crew react where they stand: stop, look up, then carry on.
2. **The Captain's ship-wide address.** A banner across the top of the screen with the Captain's portrait and a few lines of text, shown on every deck at once, readable for about 20 seconds and kept in Mail afterwards. Crew on your deck stop and turn toward the nearest speaker grille for those seconds (a pose, no pathing change), then go on. **Time never stops.** Used at most two or three times per event, so it feels like an occasion.
3. **Gatherings at a real place and time.** Announced ahead (Calendar, Mail, the address, chatter): the delegation arrives at the shuttle bay at 10:00, the all-clear party in the bow lounge at 19:00, the hunt for the garden creature at 21:00. Crew who'd come put it into their day (section 14) and go. If you're there, you see it: the shuttle doors open, the guests walk down the ramp, the Captain greets them, everyone claps (a short scripted sequence that moves crew already there, never the camera). If you're not, you hear about it in chatter and get a Mail saying what happened.

4. **Meetings with dialogue.** A meeting is a gathering at a real place and time where people *talk to each other and to you*: a briefing, a summons, a delegation's greeting, a formal dinner. It's announced like any gathering (and a summons comes as an appointment). When you're there:
   - a **dialogue panel** plays the people's lines one by one, in the device's CRT style (a strip across the bottom of the screen, or inside the device if it's open). Each line shows the speaker's name and face; tap to go on, or let it advance on its own;
   - the speakers turn to each other and to you, with small talk poses (nod, gesture); nobody else is moved;
   - sometimes you get **two or three reply choices**. They nudge a relationship or an event thread a little ("Offer to take the bridge battery run" adds you to that job and pleases Calder). There's never a right or wrong answer and never a pass or fail;
   - **the ship keeps running**, the crew around keep living, the camera stays with you, and you can **walk away** at any time: the panel closes and the gist arrives in Mail ("Briefing notes: storm prep").
   - If you weren't there at all, the gist still comes by Mail (when it concerns you) and by chatter.
   - Meeting scripts are data, like events (see "Shared formats"). The events engineer owns the script format; the device engineer owns the panel's look.

- **Agreed (2026-10-16): no forced camera, ever.** At most, a gentle "Something's happening in the shuttle bay (Deck 5)" note on the device 15 minutes before a gathering, with "show on map" (which points the goal arrow, `setGoal`, at it).
- **Agreed (2026-10-16): moments repeat in conversation.** Whatever you saw or missed, the crew retell it in chatter for a day or two, with the details that happened (who was there, whether the lights went), because it's built from the simulation.

### Gatherings of more than 70 crew

- **Where:** the plaza and promenade (Deck 3), the mess hall, the bow lounge, the shuttle bay (Deck 5). These are the only places big enough.
- **How it's drawn:** the crowd's coarse third level of detail (tonight's work) for anyone more than about 12 tiles from the camera; normal crowd figures nearer; full rigs only for the story crew nearest you, as now.
- **How it's planned:** a gathering is a set of spots (a `gather` place group per venue, added by the architects), filled nearest first; if it overflows, people stand in the next room or the corridor, as in real life.
- **Budget:** the gathering must stay under the 450 draw-call budget with all 75 crew plus guests in one room, checked by `day_check` on a gathering day. **Agreed (2026-10-16):** the festival event (below) is the stress test and isn't built until the performance engineer signs it off on a real phone.

### Visitors in the guest cabins

- **Guests are like crew but temporary** (design doc): a short list `GUESTS` with the same spec as roster entries (looks, department colour or a civilian outfit, a role, a cabin, habits), plus `arrive` and `leave` days. They follow schedules from simple templates: "scientist" (lab and observatory), "delegate" (formal dinners, tours, their cabin), "passenger" (lounge, mess, garden), "survivor" (infirmary, then rest).
- **Where they sleep:**
  - Deck 2: Envoy Saruth's cabin (permanent), the visitors' suite, and the **second visitors' cabin, kept for event visitors** (your decision). A delegation leader or a visiting dignitary gets one of these.
  - Deck 4: the six guest cabins by the lift for everyone else (staff, specialists, passengers, survivors).
- **Agreed (2026-10-16): everyday guests too.** Between events, one or two guests now and then (a specialist for a week, a transfer waiting for their ship), so the corridor always has new faces and gossip, as the design doc says. About one arrival every ship week.
- **Guests eat, sleep and use rooms** like crew: the galley cooks for them, their cabins' machines wear, they show up in chatter and you can befriend them (a short-lived relationship).
- **Owners:** the crew designer writes guest templates and the event guests; the sim engineer schedules them; the architects make sure the guest cabins have places.

### The main events, in order

All kept (the user, 2026-10-16). Pillar 3 builds the framework and event 1 first, then works down the list. Each lasts 2–4 ship days. Tier 1 is what reaches you now; later tiers in brackets.

**1. Ion storm (the first, about day 8–10 of a new game).** Touches every system.
- *Day 1, warning:* Survey picks up readings. Dr. Sato lives in the chart room; chatter starts in Survey and spreads by dinner. **Meeting: Calder's storm briefing** in the Works bay at the start of shift (08:15): she and the Works crew go over the prep at the job board; lines from Calder and two techs, and one choice for you (offer to take the bridge battery run, or the lounge, or say nothing). Mail from Works: "Storm prep: secure fittings, top up filters, check battery packs." Event jobs: secure the lounge glassware and bar, swap two lamp ballasts for shielded ones, carry battery packs from Deck 5 to the bridge. [Tier 3: service the power junctions.]
- *Day 2, onset (14:00):* **Felt everywhere:** a jolt, every light dips, then flickering. **The Captain's address:** "We're in it. Expect flickers and no calls home for a while. Look after each other." Comms go down: the call-home booths close, outside Mail stops. The bridge runs double shifts; the lounge closes; the mess goes quiet as people stay in their quarters; Watch patrols the decks.
- *Day 3, escalation:* power wear doubled and comms tripled: relay faults pop up, one deck at a time goes to emergency lighting for up to an hour (a dim red-amber light mood on that deck), the chiller strains. Brennan cooks storm stew (one pot, quicker) and sends trays to the bridge (a cart job). Sleep is worse; crew are short-tempered in the tap lines.
- *Day 4, resolution (about 10:00):* **Meeting: the Captain's all-clear** in the observation room, with the senior crew and whoever is there (you, if you've been brought along or summoned); the Captain's words go out at the same moment as **the all-clear address** on every deck. Comms return, and everyone rushes the booths: a real queue at the call-home booths for an afternoon. That evening, a gathering in the bow lounge.
- *Threads:* minutes of blackout; food spoiled; how tired the bridge crew got; the call-home backlog.
- *Goes well:* short blackouts, no spoilage, a cheerful party, the storm crew's signed duty roster pinned up in the tea corner. *Goes badly:* long blackouts, binned food, a tired, grumpy ship for two days, a scorch mark and a taped panel in the relay room.

**2. Diplomatic visit.** Social, guests and the galley.
- *Warning (two days ahead):* Mail from Commander Vance: a Veyli delegation of four arrives on Day X. Chief Holt grumbles in chatter. Event jobs: get the visitors' suite and the second visitors' cabin ready (heaters up: the Veyli like it warm), fix the Captain's dining-room lamp, carry gift crates from the hold. The laundry spikes with dress uniforms.
- *Onset:* **meeting in the shuttle bay, 10:00 (the greeting):** a Veyli shuttle docks (or the Tern brings them), the delegation walks down the ramp and the crew line the bay. The dialogue panel plays the formal greeting between the Captain, Envoy Saruth and the delegation's leader; if you're near the front, a delegate may speak to you (a choice of courteous replies, which nudges the courtesy thread). The guests move into Deck 2.
- *Escalation:* formal dinners in the Captain's quarters (**a meeting** for those at the table: the dialogue panel carries the dinner's talk; Tier 1 juniors are there only if invited, see the Captain's table in Part 4) (an extra galley batch with Veyli dishes that need herbs from the garden, so the garden's condition matters); a tea ritual in the observatory; tours of the ship (guests walk through the decks with an officer). Holt and a delegate clash over something small: a tense line spreads as gossip. [Tier 3+: you're at the table.]
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
- *Trace:* a framed print of the nebula (from Survey's data) hung in the observatory.

**6. Salvage.** The shuttle flies, and the hold fills.
- *Warning:* Survey finds a derelict. Chatter about what it might be.
- *Onset:* **gathering in the shuttle bay control booth and lobby:** the bay doors open and the Tern flies out (the first time the shuttle moves: an animation of the bay doors and the shuttle leaving). [Later: you go aboard.]
- *Escalation:* the Tern comes back with crates: the cargo hold fills with odd finds that need sorting (cart jobs), one crate holds an old but excellent part, and perhaps survivors move into the guest cabins.
- *Resolution:* the finds are shared out; a "salvage auction" evening in the lounge with odd objects.
- *Threads:* crates sorted; the salvaged part fitted.
- *Trace:* a permanent improvement (the salvaged part makes one machine wear slower) and an odd object on a shelf somewhere. **Agreed (2026-10-16):** in later playthroughs, salvage can lead straight into "Something in the garden" (the creature came from the crates).

**7. The déjà vu day.** A time anomaly replays one day.
- *Warning:* none; that's the point. A faint shimmer at the windows at midnight.
- *Onset:* you wake to the same morning: the same breakfast, the same chatter lines, the same job list. Seeded routines make the replay exact.
- *Escalation:* only you (and maybe Envoy Saruth, who hints at it in a meeting) notice. Things you change in the replay (a fault you fix early, a friend you warn) change how the day goes.
- *Resolution:* Survey finds the cause; the day runs on normally.
- *Threads:* what you set right the second time. A favourite because it shows off the simulation.

### The shorter events, slotted between

All kept, and slotted between the main events from the start (Agreed, 2026-10-16):

- **Founders' Day festival** (a happy event, and the crowd test; built once the phone test says big crowds are OK): the plaza decorated, the galley's big feast, a talent night in the bow lounge, the whole crew together. Good for showing off crowds over 70.
- **Power surge:** a one-day event centred on Deck 6; a junction trips and two decks lose power for a while.
- **A Veyli vessel needs help:** their ship limps alongside; Works sends parts; one Veyli engineer comes aboard (a guest). A seed for later away jobs.
- **The late supply shuttle:** rationing, a bland menu, filters short, the machine shop busy. Fully from the numbers (tonight's shortage Mail grows into this).
- **Crew rotation day:** five crew leave on a transport and five new faces arrive; goodbyes in the lounge, new names in Crew.
- **Comet viewing:** one evening, the observatory and the bow lounge windows; a gentle gathering, no strain.

**Changed (2026-10-16): the full order.** The user asked to keep the whole list, so the order is explicit:

| Order | Event | Kind |
| --- | --- | --- |
| 1 | Ion storm | main (built first, for check-in 2) |
| — | Comet viewing | short |
| 2 | Diplomatic visit | main |
| — | Crew rotation day | short |
| 3 | Something in the garden | main |
| — | Power surge | short |
| 4 | Shipboard illness | main |
| — | Founders' Day festival | short (once the phone test says big crowds are OK) |
| 5 | Nebula drift | main |
| — | The late supply shuttle | short |
| 6 | Salvage | main (can lead into the garden creature in later playthroughs) |
| — | A Veyli vessel needs help | short |
| 7 | The déjà vu day | main |

The short events' exact slots are the events engineer's to tune; the main events' order is fixed. The storm comes about a week and a half into a new game, then one main event every 1–2 ship weeks, with a short event or small incidents (birthdays, traditions, arguments, guests) in between, as the design doc says. **Pillar 3 builds the framework and the ion storm first, then works down the list; nothing is dropped.**

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
| Crowd (8b) | Gatherings, the coarse level of detail, poses for "looking up", clapping and meeting talk (nod, gesture) |
| Decks (4d) | Event dressing as optional places and props (traps, sign-up sheets, decorations, traces) |

---

## Part 3: social life basics

Built on what exists: crew needs, feelings on tap, habits that change, birthdays and tonight's traditions.

### Relationships with you

- **Agreed (2026-10-16):** `SHIP.rel[crewId] = { pts, tier, met, lastTalk, known: [] }`. Five tiers, by points: stranger (0), acquaintance (10), colleague (30), friend (60), close friend (100). Points never drop, or drop very slowly after weeks apart (design doc: cozy).
- **How it grows** (biggest first, per the design doc): working a job together (both at the same machine, or a team job) **+6**; eating at the same table **+3**; a chat, once per person per day **+2**; a favour done **+8**; being told news first **+1**; keeping an appointment **+3**; a birthday wish on the day **+3**. Starting numbers, for the social engineer to tune.
- **What tiers unlock** (design doc): they greet you; they tell you about their life; they show on Maps; they come and find you in free time; they invite you; friends cover a job, tip you off about spare parts and put in a good word with Calder (it shows in the Record app).

### Conversations (tap a person)

**Agreed (2026-10-16): a short chat card, not a dialogue tree.**

- **The card:** their face, name, rank and tier; one line from them, picked in order of what matters: an event or news item they know → how they feel (`crewFeeling`) → something about the ship near them → a life detail (for acquaintances and up) → a greeting.
- **Three or four buttons:**
  - **Chat** (counts once a day: social up for both of you, relationship points);
  - **Ask about…** (news, their work, home: each fills in a line in Crew's "what you know");
  - **Help?** (if they have a favour to ask, it's offered; accepting adds it to Jobs, and you turn it in to them, in a chat, when it's done);
  - **Meet up** (opens Appointments with them already picked).
- **Lines are templates filled in from the simulation** ("The {machine} on {deck} has been {symptom} all week"), with about ten variations per kind and per tier, so it doesn't repeat quickly. No AI writing, as the design doc says.
- **Hygiene matters** (tonight's table): chatting while grubby gives half the social, and some crew remark on it.

### Crew relationships with each other

- **Agreed (2026-10-16):** an affinity number for every pair of crew (75 × 74 / 2 = 2,775 small numbers, cheap to store and save), starting from traits (same department, same bunk room, shared habits) with a little seeded variety.
- **It drifts on paper** once a ship hour from who spent time together (the same "who is where" the news model uses). Most pairs drift slowly toward friendly; a few pairs with clashing traits drift the other way.
- **What it changes:** who sits together in the mess and the lounge (section 14 seating), who swaps shifts (later), who avoids whom, and what they say about each other in chatter. Friends of your friends warm to you a little faster.
- **Small dramas:** when a pair crosses into rivalry or friendship, it becomes a news item ("Pell and Rina aren't speaking"), and sometimes a small incident: an argument in a corridor that you can smooth over (a chat with each), a reconciliation over dinner.

### Crew seeking you out, and favours

- **Friends come and find you** in their free time if you're on the same deck: they walk over, greet you, and a chat card is offered as a small prompt at the screen's edge (never a pop-up you must answer).
- **Favours** grow from their lives and the ship: "My cabin lamp flickers", "Could you bring a tray up to Tomas, he's ill", "I left my datapad in the gym". Each is accepted in person, tracked in Jobs like any job (the arrow points the way, then back to them), and turned in to that person face to face.
- **The parity rule:** favours and event jobs are done through the same paths as every other job and machine (`machineUse`, the job loop, tracking). Board jobs are taken and turned in at the board; favours are taken and turned in in person. Nothing gets a special finish of its own.

### Mood

- **Agreed (2026-10-16):** mood stays `crewMood(p, t)` (tonight), blended from needs, ship health, the event's threads, recent time with friends, and birthdays and traditions. It shows in tap lines, chat lines, posture (a slower walk when low) and who goes to the lounge.

### Story crew arcs (the first three)

- **Agreed (2026-10-16):** start with the three closest to you: **Tomas** (your bunkmate), **Pell** and **Rina**. Each gets four beats that open at acquaintance, colleague, friend and close friend: a small personal thread (homesickness and a call home that goes wrong, a hobby that becomes a little show at the music room, a worry about a family member) told through chats, an appointment or two, Mail and one small gathering. Arcs for the Captain, Vance, Calder, Brennan, Holt and Saruth come later.

---

## Part 4: progression hooks (the user's request)

These are moments of trust, not new rules; the full tier-2 promotion stays in the next pillar. **Agreed (2026-10-16):** each is opened by something you earned, and each is an appointment (a time window that unlocks the door).

| Hook | How you get there | What happens |
| --- | --- | --- |
| **The Captain's ready room** | Summoned after your first commendation (an event you did well in), or by Vance once you're friends | Your first time inside. A meeting: the Captain thanks you, asks about the ship from a junior's view (a reply choice or two), and the Admiral (the fish) is introduced. Mail afterwards. A permanent line in Record. Later visits when summoned. |
| **The conference table** | Calder takes you along to an event briefing in the observation room ("bring the filter numbers") when your Works record is good; by right from Tier 3 | A meeting at the table, with dialogue: the senior crew around it, the briefing screen showing the event, a few lines each. You hear the plan before the rest of the crew; your device gets the briefing as a memo. Crew around you take their seats and leave like any meeting. |
| **Officers' quarters** | An invitation from an officer friend on Deck 4 ("Tea in my cabin after shift?") or a senior friend on Deck 2 | The private cabin's door opens for the appointment's window. A chat in their cabin counts double. |
| **The Captain's table** | A monthly dinner in the Captain's quarters; the Captain invites one junior who stood out (an event, a commendation, many close friends) | The galley cooks a special dinner (an extra batch); the senior crew at the table; you seated at the end. A gathering with a guest list. A trace: a framed menu in your locker. |
| **Progress talks with the Chief** | An appointment in Calder's glass office, any time | Where she tells you how close certification is: a bridge into the next pillar's promotion. |

**Locked doors stay locked** except during an invitation or summons (the ready room, Deck 2 bedrooms, officers' cabins), through one rule in the hatch and door check (`doorOpenFor(room, who, t)`), owned by the sim engineer with the architects.

---

## Part 5: ideas carried in

From the lead and the helpers' handovers, not yet scheduled anywhere:

- **Gym equipment, "more later"** (the user): **Agreed (2026-10-16):** add a punch bag, a rowing pair and a stretching mat during Pillar 3 so the fitness-minded crew have more to choose from, with places and poses. Bridge architect (Deck 3) and performance engineer.
- **Ready room for the player** (bridge architect), **inside a bedroom / the Captain's table** (command architect): Part 4.
- **The second visitors' cabin** stays for event visitors: Part 2.
- **The observatory as a gathering place** (command architect): nebula drift and comet viewing.
- **Queues at a big event** (galley): formal dinners and the storm's call-home rush.
- **Supplies short as a story beat** (systems): the late supply shuttle event.
- **The cargo hatch** (now open) and the shuttle flying: salvage.
- **Crawlway crouch** (tonight): crawlways become event shortcuts (a Works junior who knows them gets to a blackout first).
- **Deck 6 crawlways' second inspection points** (Deck 6 architect): with the power-surge event.
- **Machines facing the camera** (command architect): a small tidy-up for whoever touches Deck 2 next.
- **Sound** (the lead): the game is silent. **Agreed (2026-10-16):** a small sound pass in Pillar 3 or right after (a device chirp, a soft ship hum per deck, the storm's crackle, the address chime), all made in code like the textures. This is where the Music app comes from.
- **Character creation** (open question): left for the user; the Crew app would make it more personal.

### The real-phone test

The user agreed to test on a real phone (answers pass, item 34), and the lead is giving them a checklist this morning on tonight's build. **Pillar 3 starts from those results** (they set the device's layout and the crowd budget). **Agreed (2026-10-16):** the same checklist runs again after the festival, on the TriFold folded and unfolded. Its points, for reference:

1. Load time from tapping the link to the first frame.
2. Smoothness on each deck by the lift and zoomed out (does it judder?).
3. The mess hall at dinner (the busiest normal moment), and the `?crowd=120` demo.
4. The lift ride: is the pause hidden by the fade on every deck?
5. Heat and battery after 20 minutes of play.
6. The device: opening, scrolling, tapping small things, typing a memo with the on-screen keyboard; is the CRT screen crisp and readable, and do the scan lines shimmer?
7. Folding and unfolding while playing (does the layout follow?).
8. Closing the browser and coming back: does it resume where you left off?

The lead turns the user's answers into fixes for the performance engineer and the device engineer.

---

## Workstreams and owners

| # | Workstream | Owner | Section of the game file | Builds |
| --- | --- | --- | --- | --- |
| C1 | The device: two layers, **the CRT skin** (with the three phosphor options for the lead), home screen, the shim for `addSection`, notifications, phone and wide layouts, the save part; moving Needs, Jobs and Mail onto it; the dialogue panel's and tips' look; `deviceOpen` / `deviceClose` and the camera framing hook; the Jobs app as a tracker (Track) | **Device engineer (new)** | new `// 19. DEVICE`, small hooks in 15 and 11 | 0.35.x |
| C2 | Device apps: Schedule, Calendar, Memos, Maps (drawn from deck data), Crew (with the social engineer), Ship, Record, Wallet | Device engineer | 19 | 0.35.x |
| C3 | Appointments and invitations: the app (C1) and crew keeping them in `planDay`; `doorOpenFor` | Device engineer (the app), **sim engineer** (crew side, doors) | 19, 14 | 0.35.x, 0.26.x |
| C4 | Social: relationships, chat cards and line templates, crew affinity, seating by friendship, crew seeking you out, favours, the first three arcs | **Social engineer (new)** | new `// 20. SOCIAL` | 0.36.x |
| C5 | The news model: items, spreading on paper, chatter bubbles, the Ship news feed; gossip from faults, habits, birthdays and guests | Social engineer, with the performance engineer (the bubble) | 20, 8b | 0.36.x |
| C6 | Ship-wide events: the event format, phases, `eventNow` and `eventMod`, threads and bands, traces, the Captain's address, moments, **meetings and their script format**; then the ion storm (with Calder's briefing and the Captain's all-clear), then down the event list | **Events engineer** (grows from tonight's traditions) | 18 | 0.34.x |
| C7 | Event hooks in each system: wear and jobs (systems), routines and gatherings (sim), menus and batches (galley), shake, flicker and sky moods, the coarse crowd at gatherings (performance) | Systems, sim, galley, performance engineers | 17, 14, 16, 8/8b, 5 | their ranges |
| C8 | Guests: templates, event guests, everyday visitors, guest schedules | **Crew designer** (data), sim engineer (schedules) | 9, 14 | 0.16.x, 0.26.x |
| C9 | Places for gatherings (`gather` groups), event dressing and traces, the ready room and Captain's dining room as visitable places, the extra gym kit | **Architects** (bridge: 1, 3; command: 2; Deck 6 architect: 4, 5, 6) | `DECKS[n]`, kit | 0.31.x, 0.32.x, 0.30.x |
| C11 | Seeing yourself use the device: the `device` and walk-and-read poses and the glowing prop (0–1 draw calls) | Performance engineer (pose, prop), player engineer (holding state) | 8/8b, 15 | 0.27.x, 0.28.x |
| C12 | Jobs at the board: accept and turn in at the board, step-by-step tracking into `setGoal`, favours turned in in person, the "done, awaiting turn-in" state | Interactions engineer (board, tracking), systems engineer (job state), social engineer (favour hand-in in the chat) | 15b, 17, 20 | 0.37.x, 0.33.x, 0.36.x |
| C13 | Light onboarding: the five job-loop tips, once each, saved, a switch to turn them off | Interactions engineer (triggers), device engineer (look) | 15b, 19 | 0.37.x, 0.35.x |
| C10 | Progression hooks: the summons, the briefing, invitations, the Captain's table | Events engineer (the occasions), social engineer (who's invited), sim engineer (doors) | 18, 20, 14 | as above |

**Who owns what at the seam with section 15:**

- `mailSend` / `SHIP.mail` and `needEffects` stay in section 15 as APIs (the player engineer).
- The device engineer (section 19) takes over the device's screens, including the Mail, Needs and Jobs views.
- Section 15b keeps `setGoal` / `clearGoal` (the interactions engineer); the device and social code only call it.

**Agreed (2026-10-16): hiring.** Two fresh sessions (device engineer, social engineer); the events engineer from tonight carries on into ship-wide events; the existing helpers (sim, systems, galley, performance, crew designer, the three architects) each take their rows. Any helper over about 500k of memory hands over to a fresh session before starting (the user's handover rule).

**Build numbers.** Combined builds on `claude/ship-integration` are **0.50.0, 0.50.1, ...** (the lead). Helper ranges continue from wherever tonight's answers pass ends for existing roles (for example sim 0.26.x, performance 0.27.x, player 0.28.x, galley 0.29.x, Deck 6 architect 0.30.x, bridge 0.31.x, command 0.32.x, systems 0.33.x, crew designer 0.16.x), the events engineer keeps 0.34.x, the interactions engineer has 0.37.x (taken tonight), and the two new roles get **0.35.x (device)** and **0.36.x (social)**.

## Shared formats

The owner of each may refine its details, but must tell the lead and keep the other sessions' side working.

```js
// 19. DEVICE (device engineer)
deviceApp({ id, title, icon, order, badge, view })   // view(ctx) -> VIEW (plain content)
deviceDo(action)  deviceNotify({ app, text, urgent })  DEVICE_SKIN
deviceOn('open' | 'close', fn)                      // events: deviceOpen / deviceClose; the player pose and the camera listen
deviceFrame(on)                                      // the camera eases the player into the visible top part (phone sheet)
tipShow(id, text)  SHIP.device.tipsSeen = { id: true }  SHIP.device.settings.tips   // shown once each; saved

// 15b. INTERACTIONS (interactions engineer)
SHIP.player.track = jobId | favourId | null          // the tracked one drives setGoal and the Maps pins
jobSteps(jobId) -> [ { at: 'board'|'storage'|'shop'|'machine'|'person', target } ], current step index
jobTurnIn(jobId)                                     // at a board: completes the job (credit, Record, commendations)

// 17. MACHINES & JOBS (systems engineer)
// job status gains 'awaitingTurnIn' (the player's jobs only; crew jobs complete where they're done)
device.addSection(id, title, render)                // kept as a shim
SHIP.device = { memos: [], appts: [], readMail: {}, pins: [], settings: {} }   // saved; SAVE_V 2 -> 3 (no photos)
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
meeting({ id, where, at, who, script })              // a gathering whose script plays in the dialogue panel when you're there
MEETING_SCRIPTS.<id> = { title, gist,                 // gist: the Mail you get if you walk away or weren't there
  lines: [ { who: 'Calder', text: 'Right, storm prep. Filters first.', pose: 'gesture' }, ...,
           { choice: [ { text: 'I\'ll take the bridge battery run.', rel: { Calder: 2 }, job: 'stormBatteries' },
                       { text: 'I can do the lounge.', job: 'stormLounge' },
                       { text: '(Say nothing)' } ] }, ... ] }
dialogueShow(scriptId) / dialogueClose()             // section 19 draws the panel; walking out of range closes it
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
   - Work starts from the results of this morning's real-phone test.
2. **Then:** C2 and C3 (apps, appointments), C11–C13 (seeing yourself use the device, jobs at the board, the first tips), C4's chat cards and seeking out, C5's chatter, C9 gathering places.
3. **Check-in 1 with the user:** the new device with all the apps in the CRT skin (and the phosphor colour chosen), relationships and chats, crew who come and find you, appointments that crew keep, chatter you overhear.
4. **Then:** C7 (event hooks in every system), meetings and the dialogue panel, and the ion storm end to end; C10's first hook (the ready room after a commendation).
5. **Check-in 2 with the user:** a full ion storm played through: warning, Calder's briefing, onset, the address, flickers and blackouts, storm jobs, the Captain's all-clear, the rush on the booths, the party, the debrief, the trace.
6. **After that, down the list** (see "The full order" in Part 2): the diplomatic visit (guests, the second visitors' cabin, the greeting and the formal dinners, the Captain's table), something in the garden, shipboard illness, nebula drift, salvage and the déjà vu day, with the short events between them; the festival once the phone numbers allow it. Each main event ends with a review by the user, as decks did.

**Tests every turn**, as in Pillar 2: `cadet_test.py`, `deck_check.py` on all six decks, `day_check.py`, and each new checker (`social_check`, `events_check`, a `device_check` that opens every app and checks it draws). Draw calls stay under about 450 everywhere, including at gatherings. Shared kit made at load never calls `R()`; all event randomness comes from the seed and the day, so a replayed day is identical (which is also what makes the déjà vu day cheap).

## Risks

- **Too much talk, too little ship.** If chatter, toasts, meetings and Mail all fire at once, the ship feels noisy. *Answer:* a single "voice budget": at most one bubble on screen, one toast at a time, no chatter bubbles while a dialogue panel is open, two meetings at most per event, and the address only at big turns.
- **The CRT look costs too much or reads badly on a phone.** *Answer:* CSS only, scan lines as one overlay that never touches the text, no blur filters, effects off with reduced motion or the settings switch, and the phone test checks it.
- **Draw calls at gatherings.** 75 crew plus guests in one room could break 450. *Answer:* the coarse level of detail, gatherings checked in `day_check`, the festival held back until the real-phone test passes.
- **The save grows.** Relationships, affinity, news and events all add to it. *Answer:* compact formats (affinity as small numbers, news knowledge as bit sets) and a size line in each checker. (No photos, now that Camera is dropped.)
- **Events feel like nothing happened** if the effects are too gentle, or like punishment if too harsh. *Answer:* tune the ion storm first on paper with `events_check` (blackout minutes, food spoiled, jobs left) and play it through before check-in 2.
- **Section owners collide.** The event layer touches every system. *Answer:* the events engineer only publishes `eventNow` and `eventMod`; each owner adds its own small, inert check (null means "no change"), as with `shipEffects`.
- **Determinism.** News spread, affinity drift and event timing must replay exactly. *Answer:* everything seeded per person per day, like time jitter; checkers run twice and compare.
- **Memory of the helpers.** Several sessions are near full. *Answer:* hand over before starting (the user's rule), fresh sessions for the big new jobs.
- **Too many sessions at once.** Running about 13 sessions in parallel hit the account's usage limit overnight and stopped everyone for hours. *Answer:* Pillar 3 runs **at most about 5–6 active helpers at a time**, staggered (the next starts as one finishes or goes idle), and the lead's repeating hourly check-in resumes any work that stalls.

## The user's decisions (2026-10-16)

The user answered the pitch; the lead interpreted the answers.

1. **Everything else we'd go with:** yes to all ten.
2. **The device:** **changed.** Keep the two layers, but build the real skin now: an old-school CRT screen (see "The device look"). All the extra apps **except Camera**: Schedule, Appointments, Maps, Memos, Mail, Calendar, Needs, Jobs, Crew, Ship, Record, Wallet (small; may live in Needs), and Music later with sound. Camera and photos are removed everywhere; traces that relied on photos are now in-world objects or Mail.
3. **Ambient events:** **agreed, with one change.** An event can trigger a **meeting with dialogue**, never a full cutscene: a fourth kind of moment, used in the ion storm (Calder's storm briefing, the Captain's all-clear) and the diplomatic visit (the greeting, the formal dinner).
4. **The event order:** **changed.** The user asked to keep the whole list, so the full order is explicit (Part 2, "The full order"): seven main events with six short ones between them. Pillar 3 builds the framework and the ion storm first, then works down the list; nothing is dropped.
5. **Seeing yourself use the device:** **changed** (added). Your character raises and looks at the glowing handheld when it opens, reads while walking, and puts it away on close; on a phone the camera eases to keep you in view above the sheet.
6. **Jobs at the board:** **changed** (a new rule). Take and turn in jobs at the job board; the device's Jobs app only tracks (with a Track toggle that drives the arrow and the map, step by step). Favours are accepted and turned in in person (the lead's interpretation).
7. **Light onboarding:** **changed** (added). Five short job-loop tips, once each, in the CRT style, never pausing time, with a switch to turn them off. Pillar 4 does the full onboarding and tutorials.

**Design-doc updates** (the lead, on the lead branch, from this agreed plan): "The player" (the device, its CRT look and its apps), "Social life" (numbers, chats, affinity, news), "Ship-wide events" (ambient rule, shape, threads and bands, the four kinds of moment including meetings with dialogue, guests, the full event list and order), "Works progression" (the hooks), "Milestones" (Pillar 3 as planned here, and a note that Pillar 4 expands onboarding and tutorials), "The player" job loop (take and turn in at the board), and move these answered questions out of "Open questions": the device; which event comes after the ion storm; the second visitors' cabin (already answered: kept for event visitors); how often Deck 4's guests change.

## Appendix: the full list of decisions

1. **Changed (2026-10-16):** the device's **two layers** (apps describe, a skin draws), with the real CRT skin built now; opening from a corner button or a swipe up, never pausing time.
2. **Changed (2026-10-16):** the **extra apps** Crew, Ship, Record and Wallet (Music once there's sound); **no Camera**.
3. **Agreed (2026-10-16):** **Maps shows people** only once you're acquaintances (or they're on public duty).
4. **Agreed (2026-10-16):** **missed appointments** cost nothing but a remark.
5. **Agreed (2026-10-16):** events are **ambient**: news by chatter, Mail, boards and the Captain's address; no markers or cutscenes; **no forced camera**.
6. **Agreed (2026-10-16):** outcomes in **three bands** (smoothly, bumpily, roughly) from 3–5 threads measured from the simulation; your own part counted separately for commendations; results told as story and traces.
7. **Changed (2026-10-16):** **four kinds of moment:** felt everywhere, the Captain's address, gatherings at a place and time, and meetings with dialogue (never a full cutscene).
8. **Changed (2026-10-16):** **the full event order**, all kept: ion storm, diplomatic visit, something in the garden, shipboard illness, nebula drift, salvage, the déjà vu day, with six short events between them; the festival after the phone test.
9. **Agreed (2026-10-16):** **everyday guests** about once a ship week, plus event guests; the second visitors' cabin for event visitors.
10. **Agreed (2026-10-16):** **relationship numbers** as above, chat cards with three or four buttons, crew affinity on paper, the first arcs for Tomas, Pell and Rina.
11. **Agreed (2026-10-16):** **progression hooks** as appointments that unlock a door for their time: ready room, conference table, officers' quarters, the Captain's table, progress talks.
12. **Agreed (2026-10-16):** **extra gym kit** now, and a **small sound pass** in or right after Pillar 3.
13. **Agreed (2026-10-16):** **hiring** a device engineer and a social engineer; the events engineer grows into ship-wide events; builds 0.50.x.
14. **Changed (2026-10-16):** **you see your character use the device** (pose, prop, walk-and-read, gentle camera framing on a phone).
15. **Changed (2026-10-16):** **jobs are taken and turned in at the board**; the Jobs app only tracks; favours are taken and turned in in person.
16. **Changed (2026-10-16):** **light onboarding**: five job-loop tips, once each, with a switch; full onboarding in Pillar 4.
