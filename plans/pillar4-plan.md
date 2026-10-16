# Pillar 4 plan: arriving, the voices aboard, deep social life and many more traditions

**DRAFT 2 (2026-10-16, the Pillar 4 planner, session_01KLFXcNJztCSVLXunD8Jt7R).** Draft 2 folds in the interfaces agreed with the social system designer (their draft 2, ab351f1). Not agreed. Nothing here is official until the user approves it; the lead interprets their answers and marks each decision **Agreed** or **Changed** with the date, as in `plans/pillar3-plan.md`. Built from the user's own notes and answers in `plans/pillar4-notes.md`. The deep social design is the **social system designer's** (session_01SMfS1WKqzQ93X6zyZ7NFpJ, `plans/social-deep-plan.md` on `claude/social-design`): this plan references and schedules it, and the two plans must agree on shapes and order (see "Working with the social system design").

Read with `design-doc.md` ("The player", "Social life", "Ship-wide events", "Milestones", "Open questions"), `plans/pillar3-plan.md` (the device, meetings with dialogue, chat cards, the news model), `TEAM.md`, `DEV_NOTES.md`, and the handover notes for social, events, device and the crew designer.

A plain-language version for the user is `plans/pillar4-plan.html`.

---

## The pitch (one page)

After Pillar 3 the Wren has a device, crew who know you, news that spreads, ship traditions and its first big event, the ion storm. But a new game still starts with you waking in a bunk with nobody to tell you anything, most crew say the same few template lines, and the traditions are a dozen weekly happenings. **Pillar 4 makes arriving on the Wren a story, gives every one of the 75 crew a voice, makes friendships go deep, and fills the calendar.** It is deliberately big ("full bore"): about 15 helpers in parallel.

1. **You arrive.** Every new game opens on a **Sunday evening** with your shuttle settling in the Deck 5 bay. **Emeka Halloran**, a Works systems officer one rank above you, meets you at the ramp and walks you through the ship, talking as he goes; you follow, always in control. He shows you the Works bay, rides the lift with you, leaves you at your bunk with your **personal device**, and takes you to **dinner in the mess**, where **Chief Calder** stops by the table. Then you're free; bed ends the night.
2. **Your first week, taught by people, not pop-ups.** Monday is a **shadow shift**: Halloran takes one real job with you from the board to the turn-in, then lets you lead the second while he follows. Through the week, the people aboard each teach you one thing: Tomas the washroom and the bunk, Brennan the mess, Rina your health check, Calder your first solo job, Pell a chat and the quiz, the Works team their Friday tea. An optional **"Settling in"** list on the device keeps track. On your first Saturday, Tomas takes you to **Sowing morning** in the garden, where you plant a seedling of your own that grows all game. Later new games can **skip** the arrival.
3. **A voice for everyone.** Every crew member gets a **voice card** (how they talk, what they care about, their running jokes) and a **bank of lines**: greetings, moods, work talk, what they say about the ship, life details, reactions to what really happens aboard (the storm, a harvest, the lamp you just fixed), and **conversations you overhear** as you pass two people talking. Ten main characters get **story arcs** over weeks: mostly light and funny, with **moments where you really get to know them**, sometimes their struggles, as you grow close. No romance. Writers write plain text files, not code: **a head writer and three writers**.
4. **Deep social life**, designed by the social system designer: crew remember what you did, crew friendships change on their own, small gifts, crew visiting your bunk, and the heartfelt moments that friendship opens up.
5. **Many more traditions.** From a dozen to about thirty: new weekly evenings (a Tiles league, Brennan's tasting table, Sunday roast), monthly days (talent night, the department cup, the crossover breakfast where day and night shifts meet), four ship seasons tied to the garden, a midyear and a year's end, and life moments (your first week, farewells, welcome teas). **Three tradition designers**, each tied into the garden, the galley and the events framework.

**How it's built:** 15 helpers in four waves, each owning its own part of the one game file, with two "collectors" (the head writer and the traditions engineer) so the lead reviews about nine branches, not fifteen. Three check-ins with the user. Combined builds **0.60.x**. Pillar 3 finishes first (0.41.9, check-in 1, the full-storm check-in 2); writers and tradition designers could start early, because they only write text.

---

## Where we start

- **The build at the start of Pillar 4:** Pillar 3 finished (0.41.9 and its check-ins). It has the device and all its apps (section 19), chat cards, relationships, affinity, news and chatter, favours, the first arcs for Tomas, Pell and Rina (section 20), meetings with dialogue (`MEETING_SCRIPTS`, `meetingsTick`, the device's `deviceDialogue`), the Captain's address, the ion storm, occasions (ready room, Captain's table, progress talks), appointments crew keep (section 14), the job loop with take and turn-in at the board and the goal arrow (sections 15b, 17), first tips (`tipShow`), twelve ship traditions in `SHIP_EVENTS` (section 18), the garden growing food for the galley (section 16), two days off a week (Saturday, Sunday).
- **What's missing for Pillar 4:** no arrival (the game starts Day 1, Monday 06:00 in Bunk 1); no way for a crew member to lead or follow you; lines are templates in section 20, about ten per kind and tier, the same voice for everyone; no overheard conversations (chatter is one person's line); no reactions to specific things you did; crew remember little beyond relationship points; traditions only repeat weekly or every few weeks, and there are no seasons.
- **Pacing reality** (from "18 ship hours take 30 real minutes"): a ship day is 40 real minutes, a week about 4⅔ hours, four weeks about 19 hours, a quarter (13 weeks) about 60 hours, a year about 240 hours. **So weekly traditions are what players live with; monthly ones are occasions; seasonal ones are rare treats; yearly ones are for the devoted.** The plan puts most new traditions at weekly and four-weekly rhythms, and most new writing where players spend their first 20 hours.

---

## Part 1: the arrival and the first week

### The shape

**Proposed:** a new game opens on **Day 0, Sunday, at 17:40**, so **Day 1 stays Monday** and nothing else in the calendar moves (birthdays on days 1–364, the ion storm on day 10, Founding Day on day 100). Day 0 is a real ship Sunday: the crew are on their Sunday schedules (the sim plans day 0 like any Sunday). The arrival is one long evening (about 2½ ship hours, about 4 real minutes of walking and 3 meetings), then the night, then the week.

**Never a cutscene.** You always walk yourself. The escort walks ahead and talks (speech bubbles, the same as chatter), stops and waits when you lag, and says "This way" with the goal arrow pointing at him if you wander. The conversations that matter are **meetings with dialogue** (Pillar 3's panel), which you can walk away from; their gist then arrives in Mail.

### Who meets you: Emeka Halloran

**The user's rule:** someone one notch above you in rank, in Works. You are a Junior Officer, so the escort is a Works **Officer**. The roster has four: Mateo Navarro (systems, nights), Alejandro Reyes (engines, nights), Zeke Torres (engines, days, off Saturday and Sunday) and **Emeka Halloran** (systems, days, off Thursday and Friday).

**Recommended: Emeka Halloran**, Works systems officer, cabin 4-13 on Deck 4.

- **He's on duty when it matters:** day shift, working Sunday, Monday and Tuesday; off Thursday and Friday. So he can meet a Sunday shuttle, train you Monday and Tuesday, and his days off on Thursday and Friday are exactly when the game "lets you loose".
- **His job is the job board:** "Keeps the Works bay's day running, and the job board tidy." The person who teaches you the board is the one who runs it.
- **His roster personality fits a first friend:** kind and loyal; "tells terrible jokes at breakfast"; "bakes on rest days, if Brennan allows it". Warm, a little silly, steady.
- **He lives on Deck 4,** so walking you to the junior wing is on his way home.
- Torres (curious, ambitious, knits scarves, off Sunday) is the alternative, but he's an engine officer whose world is Deck 6, and off on the arrival day.

**Halloran's voice (a starting card for the head writer):** talks in short, friendly bursts and fills silences with facts about the ship; a pun he's proud of about once a scene; calls you by name from the start; says "right then" when moving on; never talks down. Cares about: a tidy board, people not being left alone with a problem, his bread. Running joke: the coffee machine in the tea corner, which he maintains and which is always slightly wrong. **His arc (heartfelt, for friend and close friend):** he's never trained a new hand before and worries he's doing it wrong, because the last junior he looked out for, years ago on another ship, washed out of certification and left the service, and he's never been sure it wasn't his fault. You are, quietly, his second chance; when you pass your certification later, it's his moment as much as yours.

### Chief Ines Calder (her personality, an open question since v4)

The design doc has asked since v4 for Calder's personality and how she judges your work. **Proposed** (it builds on her roster card: exacting, fair, dry; "remembers every repair you got wrong, and every one you got right"; her first chief's battered toolbox):

- **How she talks:** few words, all of them exact. Numbers instead of adjectives ("That scrubber's at sixty-one. Not sixty. Sixty-one."). Never raises her voice; when she's annoyed she gets quieter. Her humour is so dry you notice it a beat later. Praise is rare and plain: "Good. Clean work." From her, that's a lot.
- **What she cares about:** the invisible ship. Her creed: "Nobody thanks the air. That's how you know it's working." She values prevention over heroics, honesty about a mistake over hiding it, and finishing what you start.
- **How she judges your work** (feeds the progress talks and certification later): she reads the Record, not your words; early catches and clean turn-ins count most; a job left half-done counts against you more than a slow one; she notices who you helped. She never compares you to anyone else out loud.
- **Running details:** the battered toolbox on her shelf she never uses and never lends; a mug with nothing written on it ("It's a mug."); she knows every machine's serial number and nobody's birthday.
- **Her arc (later, for colleague and up):** her first chief, the owner of the toolbox, is retiring on a station a long way off and has written to her; she hasn't answered, because she was hard on Calder, and Calder has become hard in the same way, and she isn't sure that was right. It surfaces slowly through progress talks, a late evening in the Works bay, and one day the toolbox on your bench.
- **At the arrival she sets the tone:** brief, not cold. She sits for exactly one minute.

**A quirk of the roster we turn into story:** Calder's days off are **Monday and Tuesday**. Rather than change the rota (which would ripple through schedules and checks), she says so at dinner: "I'm off tomorrow and Tuesday. Halloran has you. Wednesday, quarter to eight, my office." So your first solo job comes from her on **Wednesday**, not Tuesday. *(Question for the user: keep this, or move her days off?)*

### Day 0, Sunday: the arrival evening, step by step

Times are ship times. Each step has a **checkpoint** (where a reload resumes) and a **fallback** (what happens if you're not there).

| # | When | Where | What happens | Uses |
| --- | --- | --- | --- | --- |
| A1 | 17:40 | Deck 5 shuttle bay, the Tern's ramp | Fade in from black. You stand at the top of the ramp holding your **kit bag** (it fills one of your two carry slots). Halloran waits at the ramp's foot and waves. The only control tip of the whole intro: how to walk (tap or press-and-hold). | `PLAYER` carry, `tipShow` |
| A2 | 17:42 | Ramp foot | Halloran: a short hello as bubbles ("You must be the new hand. Emeka Halloran, Works. Welcome to the Wren."). He sets off; the goal arrow points at him. | bubbles (8b), `setGoal` |
| A3 | 17:44 | The haulway | He walks ahead, two or three lines about the ship as you go (the cargo hold, the Cart bay, "mind the carts, they don't mind you"). Waits if you're more than 4 tiles behind. | escort **lead** mode |
| A4 | 17:46 | The Works bay door | He stops at the door: the board, the tea corner, the Chief's glass office. "That's us. Tomorrow, ten to eight." A Works junior or two on their Sunday look up and wave. | lead mode, crew on Sunday plans |
| A5 | 17:48 | Lift lobby, Deck 5 | "Four, please." You press Deck 4 on the panel yourself (learning the lift by doing it). He rides with you. | lift (11), escort crosses decks |
| A6 | 17:50 | Deck 4, junior wing | Past the washrooms ("hot water till ten, then it's character-building"), the laundry, the common room. | lead mode |
| A7 | 17:53 | Bunk 1 | **Meeting: "Your bunk".** You put your bag in your locker (tap: the bag leaves your hands). Halloran hands you your **device**: your character raises it, it boots for the first time ("CSV Wren crew device. Assigned to: …"), and shows Home with a new **Settling in** list. Tomas may be there (Sunday evening); if so he says hello and is very pleased not to be the newest any more. | meeting, device first boot (19), the device pose (8b) |
| A8 | 18:05 | Deck 4 → Deck 3 | "Dinner. Mess is on Three." He leads again: lift, the promenade, the mess. | lead mode |
| A9 | 18:12 | The mess servery | You take a tray at the servery like everyone (the player engineer's tray). Halloran picks a table; Pell joins if he's in the mess. | galley (16), tray |
| A10 | about 18:30 | Your table | **Meeting: "The Chief stops by".** Calder comes over with her mug, sits for a minute, welcomes you in her way, tells you about Monday ("Halloran has you") and Wednesday. One reply choice ("Looking forward to it" / "What should I read up on?" / say nothing), nudging her a point or two; no wrong answer. | meeting with a choice, `relAdd` |
| A11 | 19:00 | The mess | Halloran: "You're free. Bunk's yours any time from eight. I'm on Four if you need me: 13, the one with the bread smell." The escort is released; he goes back to his own Sunday plan. | escort ends |
| A12 | 19:00–bed | Anywhere | Free evening. If you go to the junior common room or your bunk room, **Tomas** finds you (the "seek" chip) for your first chat card: teaches Chat and Ask about. | social seek (20) |
| A13 | from 20:00 | Bunk 1 | Getting into your bunk skips to **Monday 06:00** as usual. A one-off "Good morning" line from the device: your first shift today. | sleep (13) |

**Fallbacks.** If you walk off and don't come back, Halloran waits at the step's checkpoint for 20 ship minutes, then moves on to the next checkpoint and waits there (the arrow points at him). If you miss dinner entirely, Calder's meeting turns into Mail at 20:00 ("Missed you at dinner. Halloran has you tomorrow; ten to eight, the Works bay. — I. Calder"), and Brennan leaves a covered plate on the grab shelf. If you never collect your device, Halloran gives it to you at Monday's briefing. **Nothing can block the game.**

### Day 1 to Day 7: the first week, taught by people

Each beat is something a person does in their real day: it is scheduled in their plan for that day (as an appointment or gathering, so it is in the schedules, deterministic and testable), it teaches one thing, it ticks an item on the Settling-in list, and if you miss it, it either happens later or arrives as Mail. Existing job-loop tips are marked as seen when a person has taught that step; a player who skips the intro gets the tips instead.

| Day | Who | Where, when | What you learn | Settling-in item |
| --- | --- | --- | --- | --- |
| **Mon 1** | Tomas | Bunk 1, 06:00 | Wash and use the washroom before breakfast; "breakfast's till eight" | Washed and fed |
| | Halloran | Works bay, 07:50 (the Monday briefing; he runs it while Calder's off) | The board. A short meeting introduces the Works team on shift. | Meet the team |
| | Halloran | the whole morning | **The shadow shift:** one reserved, real Tier 1 job end to end. He takes it at the board with you, walks you to the machine, you inspect it (he explains the panel), fetch a part from storage, **make** a part in the machine shop, repair it (hold to work), and turn it in at the board. He talks you through each step; you do every step with your own hands. | Shadow a job |
| | the Works team | Tea corner, 10:30 | The tea break counts as work; Halloran's coffee; Pell's introductions | — |
| | Halloran | the afternoon | **You lead, he follows**: a second reserved job; the escort switches to **follow** mode and only speaks if you're stuck for a while ("Storage is down one deck, I think you'll find."). Your first job in your Record. | Lead a job |
| | Brennan | Mess, dinner | The dinner window, the grab shelf ("for emergencies, and Pell"), sitting with others for social | Eat with the crew |
| **Tue 2** | Halloran | Works bay, 08:00 | "Pick one." You take a job yourself; he works his own job nearby and checks in once at the tea break. | Take a job yourself |
| | Rina | Infirmary, 14:00 (already in your Appointments) | **New-crew health check**: your needs, energy and the Needs app, bonuses and penalties, in her dry way. Teaches Appointments and Calendar by being one. | Health check |
| | a crew member at the booths (Leila Eklund) | Call-home booths, evening | **Mail from home** arrives at 18:00; she shows you the booth and the queue | Call home |
| **Wed 3** | Calder | Her glass office, 07:45 | **Meeting: your first solo job.** She hands you a job by name, explains your Record and progress talks ("Any time. Book it."). | Meet the Chief properly |
| | Orla Ishikawa (storekeeper) | Crew store, after shift | Credits, the Wallet, the store, your locker | Buy something |
| | Pell | wherever you are, evening | Comes and finds you (the seek chip): a proper chat; **Meet up** and **Ask about**; invites you to Thursday's quiz | Make a friend |
| | (Mail) | 18:00 | The quiz's ship-tradition Mail: how traditions, Mail and the Calendar's reminders work | — |
| **Thu 4** | (Halloran off) | — | You're on your own at the board. Mail from Halloran at 07:00: "Don't break anything big." | — |
| | a Works junior (Zainab Kovac) | after shift | **Your first favour**: a small personal job, accepted and handed back in person | Do a favour |
| | Watch (bunk inspection) | Deck 4, Thursday's inspection | A light comic scene: Tomas panicking about the bunk; teaches laundry and tidiness | Laundry day |
| | Pell, the quiz crowd | Bow lounge, 20:00 | Quiz night | Join a tradition |
| **Fri 5** | Works team | Tea corner, Friday tea | **The new hand's mug**: the team gives you a mug with your name on it; it hangs on the tea corner rack from then on (a trace). | — |
| | Tomas | evening | Invites you to Saturday's **Sowing morning** and film night | — |
| **Sat 6** | Tomas (his invitation sent Friday through `socialInvite`, so it's a real appointment), the gardeners | Garden, 09:00 | **Days off** ("You're off. The board's open if you're bored; nobody expects you."). **Sowing morning** (a new seasonal tradition): you plant a seedling of your own in the garden; it grows through the game (a lasting trace). Film night in the evening. | A day off |
| **Sun 7** | Calder (Mail) | 18:00 | "One week. You'll do." A summary of what you did. The Sunday swap meet. The intro ends at midnight (or when you tick everything, or when you end it). | — |

**The Settling in list** (a small app on the device, section 19). About 14 items, all optional, each ticking itself when you've done the thing (by watching ship notes, see "Shared formats"), each naming who can teach it, with "Go there" to that person or place. Ticking them all earns a line in your Record and a short note from Calder. A button, **"I know my way around"**, ends the intro at any time: the scripted beats stop, the escort goes back to his day, the list stays as a checklist.

**Skip-intro.** Once a device has finished or ended one intro (a flag kept outside the save, so New game doesn't erase it), New game asks: **"Arrive by shuttle (Sunday evening)"** or **"Skip to Monday morning"**. Skipping starts Day 1 at 06:00 in Bunk 1 (today's start), with the device in hand, the same relationships and flags as after the arrival evening, the job-loop tips on, the reserved jobs not reserved, and the Settling-in list available.

**The shuttle.** The Tern is already in the bay with its ramp down; the arrival needs no flying. A fade in, a soft "settle" (the performance engineer's `shipFeel` with a tiny jolt), and the kit bag. Later, when the Tern flies (salvage), the arrival can show it landing.

### How the arrival uses the existing systems

- **Schedules (section 14):** the sim plans **day 0** like any Sunday. The escort's and teachers' intro beats are added to their plans through one hook, `introPlan(p, d)` (like `eventPlan`), so they're part of the real, seeded day; nobody is teleported. Calder's dinner stop is a short gathering at your table's place.
- **Walkers (section 10):** a new **lead / follow** mode for one named crew member, driven by `escortPlan(p, t)`: lead (walk to the next waypoint, wait when the player is more than 4 tiles behind, carry on when they catch up), follow (stay 2 tiles behind the player), wait (stand at a checkpoint). Crossing decks: the escort enters the lift with you and is placed at the lift on the new deck, as the ship already does for crew who change decks.
- **Meetings (section 18):** "Your bunk", "The Chief stops by", "Monday briefing", "Your first solo job" are `MEETING_SCRIPTS` written by the writers (content/meetings), played by `meetingsTick` when you're in the room. Walking away sends the gist to Mail.
- **Tips (sections 15b, 19):** only the first "how to walk" tip shows. The job-loop tips are marked seen as Halloran teaches each step; for skip-intro players they work as now.
- **The job loop (sections 15b, 17):** the systems engineer adds `jobReserve(kind, day, at)`: a real Tier 1 fault (a junior-wing lamp housing, a laundry washer) whose wear is set so it faults on cue on Monday morning, needs a stored part and a made part, and is held for you (the crew don't take it). The board, tracking, the arrow, Record and turn-in all work as for any job.
- **The device (section 19):** locked (the button says "No device yet") until A7; first-boot screen; the Settling-in app; Appointments already holds the Tuesday health check; Mail carries the fallbacks.
- **Social (section 20):** each step calls `relAdd(id, 'intro:<step>', pts)`; the seek chip delivers Tomas (Sunday) and Pell (Wednesday).
- **Saving:** `SHIP.intro` is saved; the escort's position is never saved, only the step: on load, the escort is placed at the current step's checkpoint and the step resumes (meetings restart from their first line; if their time has passed, their gist goes to Mail).

### How it's tested: `intro_check.py` (new, the onboarding engineer)

Runs the arrival and the first week with a scripted player, the way `player_check` drives the player:

1. **The happy path:** Day 0 17:40 to Day 8 06:00, following the escort; each step fires in order, at its place, at its time; the escort reaches every waypoint and never sticks (path check on each leg); he crosses decks with you; the device is locked before A7 and works after; each meeting plays with its whole cast present; the reserved jobs exist on Monday, are reachable, and complete end to end through the turn-in; the follow switch works; every teacher turns up in their plan; every Settling-in item ticks.
2. **The wanderer:** walks the other way at each step; the escort waits, moves to the next checkpoint, and the evening still ends in bed.
3. **The idler:** stands still from 17:40 to Day 8; every fallback Mail arrives, the game reaches Day 8 as a normal game, nothing errors.
4. **Save and reload** at every checkpoint and twice mid-walk: the same step resumes, the escort is at the checkpoint, and the rest of the run is identical to the run without reloads.
5. **Skip-intro:** the skipped state equals the state after the arrival evening (relationships, flags, device, location, time).
6. **Determinism:** runs twice; plans, lines and results identical.
7. **Draw calls:** under 450 at the shuttle bay, at the Works bay door, at dinner and at Sowing morning.
8. **No change elsewhere:** test URLs (`?nosave&debug`) start with the intro off, so `cadet_test` stays ALL IDENTICAL and every other check is unchanged.

---

## Part 2: dialogue at scale

### What gets written

| Kind | What it is | Roughly how much |
| --- | --- | --- |
| **Voice cards** | One per crew member (75) and per guest template: how they talk (sentence length, words they use, what they never say), what they care about, a running joke, how they are with juniors, their mood tells, and for story crew their arc's outline. 150–300 words each. Built from the roster's traits, bio and life lines, which are canon. | 75 + guests |
| **Line banks per person** | greet (by tier and time of day), bye, feel (by mood), work (their job), ship (what's near them, ship health), life (by tier), Ask about (home, work, hobby, news), favour (ask, thanks), invite, remark (missed appointment, you're grubby, you're late), seek (waving you over), birthday (theirs, yours), gift, visit. | Story crew about 200 lines each; Works crew and your bunkmates about 60; everyone else about 30 personal lines on top of the shared banks |
| **Shared banks** | Lines by department, rank and trait, so no one ever runs dry ("Works, junior, dry humour"). A person's own lines always win over the banks. | about 1,500 |
| **Overheard conversations** | Two (sometimes three) crew talking as you pass: 2–4 lines, by pair type (same department, bunkmates, friends, rivals, senior and junior) and topic (the ship's state, a tradition, an event, gossip, their lives). Shown as alternating bubbles, at most one conversation on screen. | about 150 |
| **Reactions** | Lines tied to real things that happened: your repair nearby ("That lamp's been blinking since Tuesday!"), a fault in their room, the storm's phases, a harvest, a tradition they went to, a birthday, a guest arriving, a commendation, you missing an appointment. | about 40 kinds × about 10 voices each |
| **Meetings** | The intro's meetings and new tradition and arc meetings, in the existing `MEETING_SCRIPTS` shape. | about 30 |
| **Story arcs** | Ten main characters, 5–8 beats each (see below); 20 lighter two- or three-beat threads for generated crew. | about 70 beats + 50 small ones |
| **Traditions' text** | Each tradition's Mail, tap lines, thanks and chatter (written by the tradition designers, checked by the head writer). | about 25 lines each |

In all **about 8,000–9,000 lines**. Every line is short (a bubble at most 90 characters, a chat line at most 140).

### The ten arcs (proposals for the head writer and the social designer)

Light most of the time; one or two beats in each are where you really get to know them. All are gated by friendship tier and told through chats, appointments, Mail, one small gathering and, at the deepest beat, a meeting. Tomas, Pell and Rina already have four-beat arcs (0.36.10); Pillar 4 deepens them.

1. **Emeka Halloran** (your escort): the mentor who's afraid of failing a junior again (above).
2. **Tomas Lind** (bunkmate, Watch): "a little lost"; homesick, quietly thinking about asking for a transfer home; with your friendship he finds his place (and becomes the one who meets the *next* new arrival on crew rotation day).
3. **Pell Okafor** (Works): the three unread messages from his mum, who wants him home to run the family repair shop; he's scared of disappointing her either way.
4. **Rina Deshi** (infirmary): wants to be a doctor, failed the qualifying exam once and won't say so; you end up quizzing her from her journals.
5. **Chief Calder:** the toolbox and the unanswered letter (above).
6. **Chef Auda Brennan:** an old friend has offered her a restaurant on Hesper Dock; she cooks the menu she'd serve there, one dish a week, at the tasting table.
7. **Commander Teo Vance:** the two messages from home he hasn't opened; the rowing leaderboard as the thing he can control.
8. **Captain Odile Marrow:** the portrait gallery and the late Thursday piano; what it is to be responsible for everyone and friends with no one; she asks a junior's view because nobody else tells her the truth.
9. **Chief Bram Holt:** his distrust of the Veyli, its roots in an old incident, and a slow, grudging thaw that runs alongside the diplomatic visit and Envoy Saruth.
10. **One generated crew member, to show anyone can matter:** Zainab Kovac (Works, meticulous, shy, "secretly afraid of the lift"): a small, funny, kind arc about the lift.

*(Arc structure, gating and how beats unlock belong to the social system designer; the stories belong to the head writer. Both sign off on each arc outline before it's written.)*

### The format writers fill (no engine code)

Writers and tradition designers write **plain text files** under a new folder `content/`. A generator, `content_gen.py` (owned by the dialogue engineer, in the style of `plans/crew-roster-gen.py`), turns them into generated blocks in the game file between markers (`// ---- BEGIN LINES` … `// ---- END LINES ----`, and the same for traditions and meetings). Nobody hand-edits a generated block; re-running the generator with no changes gives byte-identical output.

```
content/
  facts.md                 the canon sheet: who's from where, who's related, running jokes (the head writer keeps it)
  voices/<crewId>.voice    voice cards (the social designer's shape: talk, cares, jokes, words tokens, needs, openness, loves/likes, joy, thread, keepsake, avoid)
  themes/<theme>.arc       struggle themes for generated crew (3 beats each, with roster fill-ins like {home})
  gifts.list               gift tags
  lines/<crewId>.lines     each person's own lines
  banks/<dept|rank|trait>.lines   shared lines
  overheard/<topic>.lines  conversations
  reactions/<kind>.lines   reactions to ship notes
  meetings/<id>.meet       meeting scripts (the MEETING_SCRIPTS shape)
  arcs/<arcId>.arc         arc beats and their lines
  traditions/<id>.trad     tradition data and texts
```

A `.lines` file (sketch; the dialogue engineer settles the exact grammar in wave 1, and the condition words are agreed with the social designer):

```
@crew halloran-emeka

== greet
? tier=stranger
- Evening. You'll be the new hand.
? tier>=acquaintance time:morning
- {hi}, {me}. Coffee's terrible. I made it.   #funny
- Morning! Board's light today. Don't tell it I said so.

== react
? cue:repair.lamp.you
- That lamp's been blinking since Tuesday. {thanks}!   #warm

== feel
? mood:low
- Long one. I'll be fine after bread.

== arc halloran.4
? tier>=friend flag:certified.tier2
- I had a junior once. Didn't make it through. I used to think that was on me.   #serious
```

```
== overheard
? pair:works+works topic:board
A: Board's light today.
B: Then it'll be heavy tomorrow. It always is.
```

- **Sections** (`== kind`) name the line kind; **conditions** (`? ...`) use one fixed vocabulary: the social ones read section 20's queries (`tier`, `mem:`, `warmth:`, `aff:`, `bond:`, `mood:`, `beat:`, `news:`, `rep:`, `you:`, `cue:`, `flag:`, `week1:`; see the social designer's Part 6), the rest are the dialogue engine's (`time:`, `weekday:`, `place:`, `deck:`, `event:`, `trad:`, `dept:`, `trait:`, `act:`, `pair:`, `topic:`). **Placeholders** are filled from the simulation (`{me}`, `{nick}`, `{name}`, `{friend}`, `{best}`, `{rival}`, `{boss}`, `{thing}`, `{trad}`, `{machine}`, `{room}`, `{deck}`, `{dish}`, `{weekday}`, `{home}`); a line whose placeholder can't be filled is skipped. **Voice tokens** (`{hi}`, `{bye}`, `{yes}`, `{thanks}`, `{wow}`, `{sigh}`, `{nick}`) come from the speaker's voice card, so one shared line sounds like each person. **Tone tags:** `#light` by default, `#funny`, `#warm`, `#serious`.
- **Picking a line** (`lineFor`, the dialogue engine; as agreed with the social designer): the person's own lines, then their voice template's, then the shared bank; keep those whose conditions all hold; most specific wins (own above template above shared); minus points for lines said recently (the last 6 by this person, the last 12 ship-wide); a seeded pick by person and hour (`schedU`), so a second tap in the same hour says the same; `told:` callbacks are said once and marked through `memTold`. Overheard conversations and reactions also keep a small saved ring so none repeats to you within 7 ship days. Each line's id is a hash of its file, kind and text.
- **The baked shapes are the social designer's** (their Part 9: `VOICE`, `LINES[kind]` with condition fields, `MOMENTS` and themes in `MEETING_SCRIPTS`' `{ who, text, pose, to }` / `{ choice: [...] }` shape, choices gaining `flavour`, `mem`, `flag`, `favour`), so `dialogueShow` plays moments unchanged.
- **The voice budget** from Pillar 3 stays: one bubble or one overheard conversation on screen at a time, none while a dialogue panel is open, at most one `#serious` line a day, reactions at most once per person per kind per day.

### How lines are reviewed (voice and tone)

1. **Automatic: `lines_check.py`** (the dialogue engineer): every token and condition is valid; lengths; every crew member has a voice card and the minimum count per kind and tier; no unknown names (only roster names and guests); no duplicate lines; the banned list (romance and flirting words, swearing beyond the ship's mild "blast", real-world politics and brands); `#serious` lines only behind friend tier or an arc beat; a reading-ease score per file. Writers run it before every push.
2. **The head writer, every batch:** reads each batch against the voice card and `content/facts.md`: does it sound like *them*; is it mostly light; is a serious line earned; is it kind (humour is never cruelty); is it consistent with what other writers wrote. Sends notes back; merges what passes.
3. **The lead:** doesn't read every line. Reviews the head writer's merged branch once a wave (diff size, check results, a sampled page) and the onboarding scripts in full.
4. **The user:** at check-in A, a **Voices sampler** page (each main character's card and ten lines, plus Halloran's and Calder's arrival scenes) to approve the voices **before** the bulk is written; at check-ins B and C, the sampler grows.

**Tone rules (for the voice bible):** generally light, cozy and funny; warmth over wit; serious moments are earned by friendship and are about real, ordinary things (homesickness, a failed exam, a parent getting older, doubting yourself, a friendship cooling); nobody dies on screen; no romance or flirting with the player (the user's answer); no cruelty played for laughs; Holt's distrust is voiced and argued with, never a slur; everyone is competent at their job.

---

## Part 3: deep social life (with the social system designer)

### Working with the social system design

The **social system designer** owns the design of deep social life in `plans/social-deep-plan.md` (branch `claude/social-design`): what crew remember about you, how crew-to-crew friendships and rivalries live and change, gifts, crew visiting your bunk, the heartfelt moments friendship opens up, how arcs are structured and gated, and the numbers. This plan doesn't redesign any of that. It:

- **schedules** it into the waves below (foundations in wave 1, features in waves 2–3, tuning in wave 4);
- **staffs** it with two social engineers (A and B, split as the designer decides; proposed split: A memories, gifts, visits and reputation; B crew-to-crew life, arcs and moments);
- **agrees the interfaces** between onboarding, dialogue data and social state (below, proposed to the designer on 2026-10-16; to be confirmed in both plans before either is final).

### The interfaces (agreed with the designer, 2026-10-16; both plans say the same)

1. **Line conditions read social state only through section 20's pure queries:** `relTier`, `mem(id, key)` (keys `kind.arg` with prefix match: `mem:fav.lamp`, `mem:came.quiz`, `mem:intro.dinner`), `warmth`, `affBand` (rival at -40 or less, friend at 60 or more), `bondOf` (best, rival, mentor, mentee, drifting), `moodOf`, `beatOf(arcId)` (beats told; `arcBeat` already means "the next beat due"), `knowsNews`, `repBand`, `knownFor`, `cue` (a recent ship note still talked about), `flag`. **The vocabulary freezes at the end of wave 1.**
2. **One ship notes bus and one flag store,** both in section 13 (the sim engineer), early in the file so load order never bites: `simNote(kind, data)` / `onSim(kind, fn)`, `flag(key)` / `flagSet(key)` (saved in the main save). Kinds others send: `repair`, `favour`, `tradition`, `gift`, `apptKept`, `apptMissed`, `introStep`, `eventPhase`, `choice`, `jobAbandoned`, `harvest`, `lateMeal`, `job`, `need`. Social sends `tierUp`, `moment`, `bond`, `invite`. Each note also stays a "cue" for a day or two for line conditions. Social makes memories from them, the dialogue engine reactions, onboarding Settling-in ticks.
3. **Onboarding → social:** onboarding owns `SHIP.intro`, calls `relAdd(id, 'intro:<step>', pts)` (after the arrival evening: Halloran 10, Tomas 10, Pell 5, Calder 3, Brennan 3), sets flags (`met.calder`, `escort.halloran`, `mug`, `seedling`, and the week's gates `week1.d2` … `week1.done`), and sends `simNote('introStep', { step, who })`. Social turns those into core memories (`intro.arrival`, `intro.dinner`, `intro.shadowShift`) and a **mentor bond** from Halloran to you (extra week-1 lines, an evening check-in each day of week 1). Skip-intro sets the same end state and memories.
4. **Week-1 gating** (social's): chat cards always; favours from `week1.d2`; friends waving you over from `week1.d3`; invitations from `week1.d5`; moments and bunk visits after `week1.done`. The scripted first-weekend invitation goes through `socialInvite({ trad, day, from })`, so it's a real `invite` appointment.
5. **Chat card:** section 20 decides which kind of line matters most (its extended order: missed appointment, week 1, a moment ready, arc beat, feud, birthday, invitation, memory callback, news, cue, feeling, life, greeting) and asks `lineFor(p, kind, ctx)` for the words. Today's hard-coded lists move into `content/` unchanged first (same lines out, `cadet_test` identical).
6. **Overheard conversations are the dialogue engine's** (playing them as alternating bubbles under the voice budget), with pair conditions read through `affBand` and `bondOf`; news riding on one spreads to the second speaker through section 20's `newsAdd`.
7. **Social data writers fill** (voice cards, themes, moments, gifts, invitation lines) lives in `content/` and is baked by the same generator.

---

## Part 4: many more traditions

### How traditions grow

Traditions stay in the one events system (section 18, `SHIP_EVENTS`): when, time, where, who, what they do, hold, cake, decor, Mail, tap lines and thanks. Pillar 4 adds:

- **New rhythms** for `when`: weekly (exists), every two or four weeks (exists in part), **by quarter** (the ship's four seasons), **by day of the year**, and **personal** (counted from your arrival: your first week, your first four weeks).
- **Ties** as data, each handled by its owner: `galley` (a dish, a batch, a special meal: the galley engineer), `garden` (sow, tend, harvest: the galley engineer, who owns the garden), `decor` (props on the deck for the window: the deck architect, with the performance engineer's draw-call budget), `tally` (a simple vote or score kept for a week: the traditions engineer).
- **Tradition data as content:** tradition designers write `content/traditions/<id>.trad` files; `content_gen.py` bakes them into the `TRADITIONS` block, merged into `SHIP_EVENTS` at load. The traditions engineer reviews their data and builds anything that needs code.
- **Joining does more** (the events handover's open question): joining gives a little social as now, plus `simNote('tradition')` so crew there remember you came, and friendship points with the host and anyone you sat with (numbers from the social designer).

### The ship's year: four seasons

A ship in space has no seasons, but the garden does. **Proposed:** the Wren's year (364 days, 52 weeks) has four quarters of 13 weeks named for the garden's cycle: **Sowing** (days 1–91), **Greening** (92–182), **Harvest** (183–273) and **Lanterns** (274–364). The galley's garden can follow the same rhythm, and the Calendar shows the season.

### The new traditions (proposals for the three designers)

| Rhythm | Tradition | When, where | Tied to |
| --- | --- | --- | --- |
| Weekly | **Tiles league** | Tuesday 20:00, the junior common room; Rina defends her title | social (rivalries), Rina's arc |
| Weekly | **Brennan's tasting table** | Wednesday dinner, the mess; a small new dish, crew vote with a token; the winner joins the menu | galley menus, `tally`, Brennan's arc |
| Weekly | **Garden hour** | Wednesday 18:00, the garden; volunteers tend the beds | garden growth |
| Weekly | **Late piano** | Thursday 22:00, the music room; the Captain plays (her habit already), a few listeners | Captain's arc |
| Weekly | **Long breakfast** | Saturday, breakfast runs to 10:00 with pancakes | galley, days off |
| Weekly | **Sunday roast** | Sunday dinner, long tables in the mess | galley, seating by friendship |
| Weekly | **Letters evening** | Sunday 19:00, the call-home booths and a postbox for paper letters (Reyes writes on paper) | call home, Mail from home |
| Every 4 weeks | **Talent night** | Bow lounge stage; musicians and anyone brave | music, social |
| Every 4 weeks | **Department cup** | The gym: a rowing relay between departments; Vance keeps the board | gym, departments, Vance |
| Every 4 weeks | **The crossover breakfast** | 06:00 in the mess: the night shift's dinner is the day shift's breakfast; the one time they meet | schedules (night crew), affinity |
| Every 4 weeks | **Mending day** | Laundry and the junior common room: uniforms mended and swapped | uniforms and laundry |
| Every 4 weeks | **Rummage day** | The cargo hold: odd things from storage laid out | storage, salvage later |
| Every 4 weeks | **Open lab** | Deck 2's Survey lab and observatory: Sato shows samples | Survey, Deck 2 |
| Every 4 weeks | **Bridge hour** | Juniors visit the bridge for an hour; the Captain says hello | Deck 1, progression |
| Seasonal | **Sowing morning** | First Saturday of a quarter (day 6 is the first: your first weekend), the garden: everyone plants a seedling; yours grows all game | garden, the intro |
| Seasonal | **First-fruit supper** | Greening: the first crop from the new beds | garden, galley |
| Seasonal | **Harvest supper** | Harvest: a long-table supper from the garden | garden, galley |
| Seasonal | **Lantern walk** | Lanterns: paper lanterns along the promenade at dusk | decor (one instanced mesh) |
| Yearly | **Midtour** | Day 182: half the year; crew write a letter to themselves, read at year's end | Mail, memos |
| Yearly | **Year's end** | Day 364: the log is read in the bow lounge; the letters come back | the Captain, Mail |
| Life | **New hand's tea** | The first Friday after anyone joins (you first): the mug on the rack | the intro, crew rotation day |
| Life | **One week / four weeks aboard** | Calder's Mail; a cake from the Works team at four weeks | Record, galley |
| Life | **Farewell supper** | When crew leave (crew rotation day) | events, social |

With the existing twelve (running club, quiz, Works Friday tea, Friday jam, film night, observatory night, swap meet, harvest morning, hull-lights, birthdays, Founding Day, the quiet watch), that's **about 35**. The designers may cut, merge or add; the user picks from a **Traditions calendar** page at check-in A.

**Voice budget for traditions:** at most two traditions on the same evening, never on the same deck at the same time; Mail announcements bundled into one "This week aboard" Mail on Sunday plus the evening-before Mail for the ones you marked; birthdays never moved.

---

## Part 5: staffing, waves and check-ins

### The 15 seats

| # | Role | New or existing | Owns (only these) | Branch | Builds |
| --- | --- | --- | --- | --- | --- |
| 1 | **Onboarding engineer** | new | new section `// 21. ARRIVAL` (intro steps, `SHIP.intro`, `escortPlan`, `introPlan`, Settling-in items, skip-intro), `intro_check.py` | `claude/arrival` | 0.42.x |
| 2 | **Dialogue engineer** | new | new section `// 22. LINES` (`lineFor`, `overheardFor`, reactions, conditions, tokens), `content_gen.py`, `lines_check.py`, the generated blocks' markers | `claude/dialogue` | 0.43.x |
| 3 | **Social engineer A** (query API, memories, the kind order, week-1 gating, gifts, reputation, invitations, bunk visits) | existing social role (fresh session if over half full) | section `// 20. SOCIAL`, `social_check.py` | `claude/social` | 0.36.20+ |
| 4 | **Social engineer B** (voice cards and steps, crew-to-crew, the moments engine, story arcs) | new | a marked sub-block `// 20c. SOCIAL STORIES` inside section 20 | `claude/social-stories` | 0.39.x |
| 5 | **Traditions engineer** (events engineer 3) | new session, existing role | section `// 18. SHIP EVENTS`, the TRADITIONS block's loader, `events_check.py`; collects the tradition designers' files | `claude/ship-events` | 0.34.x |
| 6 | **Sim engineer** | existing | sections 13 (the `simNote` bus and the `flag` store), 14 (day 0, `introPlan`, `crewComeTo` for visits, the weekly affinity snapshot, tradition routines), 10 (lead/follow mode) | `claude/sim-engineer` | 0.26.x |
| 7 | **Device engineer** | existing | section 19 (device lock and first boot, the Settling-in app, skip-intro choice, season in Calendar, gifts in the locker view) | `claude/device` | 0.35.x |
| 8 | **Deck architect** (places and decor) | existing | `DECKS[n]` places and dressing (your seedling's pot, the mug rack, tradition decor, the postbox, the tasting board), kit | `claude/decks-p3` | 0.38.x |
| 9 | **Head writer** | new | `content/` (merges writers' branches), `content/facts.md`, the voice bible, the voice cards of the story crew, arc outlines; runs the generator and owns the baked LINES and MEETINGS blocks | `claude/content` | 0.48.x |
| 10 | **Writer: Works and the arrival** | new | `content/` files for Works crew (25), Halloran and Calder's lines, the intro's meetings | `claude/writer-works` | — |
| 11 | **Writer: command, Survey, Watch and guests** | new | the Captain, Vance, Holt, Sato, Nandakumar, senior officers, Watch, Survey, guests | `claude/writer-command` | — |
| 12 | **Writer: Commons and juniors** | new | Tomas, Pell, Rina, Brennan, galley, infirmary, store, night shift; overheard and reactions banks | `claude/writer-commons` | — |
| 13 | **Tradition designer: weekly** | new | `content/traditions/` weekly ones | `claude/trad-weekly` | — |
| 14 | **Tradition designer: every few weeks** | new | `content/traditions/` four-weekly ones, the "This week aboard" Mail | `claude/trad-monthly` | — |
| 15 | **Tradition designer: seasons, year and life moments** | new | `content/traditions/` seasonal, yearly, life; the seasons on the Calendar (data) | `claude/trad-seasons` | — |

**On call** (existing helpers, small rows, not counted in the 15, woken only for their row): systems engineer (`jobReserve`, 0.33.x), galley engineer (tasting table, roast, long breakfast, harvest supper, the four-week cake, the seedling in the garden's data, 0.29.x), performance engineer (two-person overheard bubbles, the device hand-over and bag props, draw calls at gatherings, the lantern instancing, 0.27.x), player engineer (the kit bag in your hands, device lock, gift tags on carried items, 0.28.x), interactions engineer (tips marked seen when taught, the locker drop, 0.37.x), crew designer (the generator fields social needs: `tpl`, `loves`, `likes`, `joy`, `thread`, `needs`, `openness`, `keepsake`, `home`, `family`, more `about` details; 0.16.x). **The social system designer** stays on as the keeper of the social design through wave 2, answering questions and reviewing the social engineers' work. **This planner** stays on through wave 1 to answer plan questions, then hands over.

**Combined builds:** **0.60.0, 0.60.1, …** on `claude/ship-integration` (the lead). (0.50.x was planned for Pillar 3 and not used; 0.60.x keeps Pillar 4 clearly apart.) Writers and tradition designers have no build numbers: their work reaches the game only through the head writer's (0.48.x) and the traditions engineer's (0.34.x) builds.

### Who merges what (keeping the lead's load down)

- **Writers → head writer:** writers push `content/` files only, to their own branches; the head writer reviews each batch, merges it into `claude/content`, runs `lines_check.py` and `content_gen.py`, and pushes a build. The lead never merges a writer's branch.
- **Tradition designers → traditions engineer:** the same, into `claude/ship-events`; text goes past the head writer for tone (light touch).
- **The lead merges about nine branches** (seats 1–9) into the combined build, in a fixed order each round: sim (13/14/10) → device (19) → social A (20) → social B (20c) → traditions (18) → dialogue (22) → arrival (21) → places (DECKS) → content (generated blocks last; on any conflict in a generated block, re-run the generator rather than merge by hand).

### Keeping the one file from colliding

- **Each new piece is its own section,** owned by one seat (21, 22, and the sub-block 20c) and placed so load order is safe (each is lazy, as section 20 is).
- **Generated blocks** (LINES, MEETINGS, TRADITIONS) sit between markers, are rewritten whole by the generator and never hand-merged.
- **Hooks into other sections are one-line, `typeof`-guarded calls** (as today), and the lead keeps a **hook register** in DEV_NOTES listing every such line and its owner.
- **Hash keys** for seeded randomness: each seat gets its own range (social, both engineers: 644–699; arrival 700–749; lines 750–799; the new traditions 434–499), listed in DEV_NOTES beside the existing ones.
- **The save:** `save.intro`, `save.lines`, and the social engineers' new parts, each read defensively; `SAVE_V` stays 2 unless the lead decides otherwise.

### Waves and order

**Wave 0 (now, while Pillar 3 finishes):** this plan and the social designer's plan, agreed with each other and then with the user. **If the user agrees, the head writer, the three writers and the three tradition designers can start as soon as the plan is approved,** because they write only text files and touch nothing Pillar 3 is finishing: voice cards, the voice bible, `facts.md`, tradition design cards.

**Wave 1: foundations (all "on paper", nothing visible changes).** About 12 active.
- Dialogue engineer: the `.lines` grammar, `content_gen.py`, `lines_check.py`, `lineFor` with the section-20 templates moved into content; the condition vocabulary agreed with the social designer and **frozen**.
- Sim engineer: the `simNote` bus; day 0 planned like a Sunday; `introPlan`; lead and follow modes for one walker.
- Onboarding engineer: `SHIP.intro`, the steps as data, checkpoints and fallbacks, `intro_check.py` running Day 0 on paper.
- Social engineers A and B: the designer's wave 1 (A1 the query API, A2 memories with decay, A3 the kind order calling `lineFor`, A4 week-1 gating; B1 voice cards and steps, B2 crew-to-crew).
- Traditions engineer: the new `when` rhythms, seasons, ties, the TRADITIONS block loader; `events_check` for a whole year on paper.
- Head writer and writers: the voice bible; voice cards for all 75; the story crew's samples; the intro meetings' first drafts.
- Tradition designers: design cards for every proposed tradition (who, what, where, ties, decor and galley asks).
- Tests: `cadet_test` ALL IDENTICAL on every build in this wave (intro off in tests).

**Wave 2: the arrival evening, voices in.** About 13 active.
- Onboarding + sim + device + performance + deck architect: Day 0 playable from the ramp to the bunk; device lock and first boot; the kit bag; the escort leading across decks; dinner with Calder.
- Dialogue engineer: overheard conversations and reactions running from content.
- Writers: first full banks for the story crew and the Works crew; overheard batch 1; reactions to the storm and repairs.
- Social A/B: the moments engine (B3, before check-in B if possible: you asked for these by name), gifts (A5), reputation by department (A6), invitations (A7).
- Traditions: the first six weekly traditions live.
- **Check-in A with the user:** play the arrival evening; the **Voices sampler** (approve the main voices before the bulk is written); the **Traditions calendar** (pick, cut, add).

**Wave 3: the first week, depth.** About 14 active (the peak).
- Onboarding: Days 1–7, the shadow shift with `jobReserve`, the follow switch, every teacher, the Settling-in list, Sowing morning and your seedling, the new hand's mug, fallbacks; skip-intro.
- Writers: all 75 people's banks; arcs beats 1–3 for the ten; overheard batch 2.
- Social A/B: bunk visits (A8), story arcs as the writers deliver them (B4), the tuning pass.
- Traditions: the rest of the weekly ones, the four-weekly ones.
- **Check-in B with the user:** a whole first week played; overheard conversations; reactions; crew who remember; the new weekly traditions.

**Wave 4: finish and tune.** Shrinking as seats finish.
- Arcs to their last beats; the seasonal, yearly and life traditions; the small arcs for generated crew; tuning numbers from the user's check-in B notes; the real-phone draw-call pass at the busiest moments (Sunday roast, talent night, the lantern walk).
- **Check-in C with the user:** Pillar 4 final; then a pull request to `main` with the user's OK.

**Tests every turn**, as in Pillars 2 and 3: `cadet_test.py`, `deck_check.py`, `day_check.py` (including day 0, a tradition night and Sowing morning), `player_check`, `food_check`, `machine_check`, `events_check` (a whole year of traditions on paper), `interactions_check`, `social_check`, `device_check`, and the new **`intro_check`** and **`lines_check`**. Check-runner sessions run them in parallel on `claude/integration-test`, as in Pillar 3.

### Risks

- **Draw calls on phones.** The escort plus a full mess at dinner; tradition decor; two-person bubbles; the lantern walk; Sunday roast with long tables. *Answer:* a budget per tradition (decor at most 6 draw calls, merged geometry or one instanced mesh, only on its deck during its window); bubbles stay the one shared bubble; `day_check` runs at each new tradition's busiest minute; 450 stays the ceiling; the performance engineer is on call for any spike.
- **The one-file merge load.** Fifteen helpers, one file. *Answer:* new sections per seat, generated blocks never hand-merged, one-line hooks in a register, a fixed merge order, and collectors so only about nine branches reach the lead.
- **The lead's review load.** *Answer:* the head writer reviews and merges all writing; the traditions engineer collects the tradition designers; the social designer reviews the social engineers; this planner reviews onboarding against the plan through wave 1; the lead reviews digests and the arrival in full.
- **Usage limits** (Pillar 3 hit the account's limit with about 13 sessions and lost 2½ hours). *Answer:* waves that peak at about 14 only in wave 3, writers paced in batches, the lead's repeating hourly check-in resuming stalled sessions, and the user's go-ahead before each wave.
- **Voices drift between writers.** *Answer:* the voice bible and voice cards come first; `facts.md` is canon; the head writer reads every batch; the user approves the main voices at check-in A before the bulk.
- **Too much talk.** Overheard conversations plus reactions plus chatter plus traditions could make the ship noisy. *Answer:* the voice budget (one on screen, no repeats within a week, at most one serious line a day, reactions once per person per kind per day), checked by `lines_check` on a simulated day.
- **The intro is brittle** (wandering, reloading, the lift, missing dinner). *Answer:* checkpoints, fallbacks by Mail, `intro_check`'s wanderer, idler and reload runs, and "I know my way around".
- **The intro feels like a tutorial.** *Answer:* people teach, not pop-ups; one control tip only; you can walk away from anything; the ship keeps living around you during it.
- **Serious moments land wrong.** *Answer:* earned by friendship, small and real, reviewed by the head writer, and the user sets the limit (question 8).
- **The save grows.** *Answer:* line memory as a small ring of ids, memories compact, the intro's state tiny; a size line in each checker.
- **Determinism.** *Answer:* every pick seeded per person per day; the intro is fixed; checkers run twice and compare.
- **Pillar 3 isn't finished.** *Answer:* no game code for Pillar 4 starts until the lead says Pillar 3 is done; only text work starts early, if the user agrees.
- **Helpers' memory.** *Answer:* the 70% handover rule; writers in particular hand over between batches, with the voice bible as their memory.

---

## Questions for the user

1. **The escort:** Emeka Halloran (Works systems officer: kind, terrible breakfast jokes, bakes, runs the job board, off Thursday and Friday)? The alternative is Zeke Torres (engine officer, off at weekends).
2. **Calder's days off** are Monday and Tuesday in the rota. Keep them, so Halloran trains you Monday and Tuesday and Calder gives your first solo job on Wednesday (recommended), or move her days off so she's there on Monday?
3. **Your name:** should you type a name on the shuttle (the crew use it), or stay "the new hand" with no name? And should you choose your look then (a design-doc open question)? Recommended: a name only, for now.
4. **Your first weekend:** Sowing morning in the garden (you plant a seedling that grows all game) and film night with Tomas: good?
5. **Writers:** a head writer and three writers (a fourth later for overheard and reactions only if needed)?
6. **Starting early:** may the writers and tradition designers start while Pillar 3 finishes? They only write text files, nothing in the game changes.
7. **Seasons:** four ship seasons named for the garden (Sowing, Greening, Harvest, Lanterns)?
8. **How serious is serious?** Proposed: homesickness, a failed exam, a parent getting older, self-doubt, a friend drifting; nobody dies on screen; no romance.
9. **The remaining ship-wide events** (comet viewing onward) are paused (your call, ~20:25). Keep them out of Pillar 4 and do them next?

The social system designer's own questions (crew couples in the background or none, whether grief is in, bunk visits, gifts from the machine shop, reputation that can dip, "what you know" counts) are in `plans/social-deep-plan.md`; the lead may want to put both lists to the user together.

---

## Appendix: shared formats (proposed; owners refine and tell the lead)

```js
// 13. SHIP TIME & SAVE (sim engineer): the ship notes bus, early in the file
simNote(kind, data)   onSim(kind, fn)   flag(key)   flagSet(key)      // flags saved in the main save
// kinds sent: repair {who, machine, kind, deck}, favour {who, from}, tradition {id, day, came, you}, gift {to, item}, apptKept / apptMissed {id, with},
//   introStep {step, who}, eventPhase {id, phase}, choice {script, k, who}, jobAbandoned {machine, dept}, harvest, lateMeal, job {id, step}, need {key, low}
// social sends: tierUp {id, tier}, moment {id, who, beat}, bond {a, b, kind}, invite {from, id}

// 14 / 10 (sim engineer)
// day 0 (Sunday) is planned like any Sunday; SHIP_START for a new arriving game: day 0, 17:40, the shuttle bay
introPlan(p, d) -> [ plan entries ] | null   // like eventPlan: the escort's and teachers' intro beats in their real day
// walkers: one named crew member can be driven by section 21's escortPlan(p, t)

// 21. ARRIVAL (onboarding engineer)
SHIP.intro = { on, step, day, done: { <stepId>: shipMin }, settle: { <itemId>: shipMin }, skipped, ended }   // save.intro
INTRO_STEPS = [ { id, day, at, until, who, where, mode: 'lead'|'follow'|'wait'|'meet'|'free', meeting, checkpoint, fallback: { mail, later } } ]
introOn() -> bool   introStep() -> step | null   introDone(id)   introEnd()   introSkip()
escortPlan(p, t) -> { mode: 'lead'|'follow'|'wait', to: placeId | tile } | null
SETTLE = [ { id, title, teacher, place, done: note => bool } ]   // ticks from simNote; the device's Settling-in app reads it
// the skip-intro flag lives outside the save: localStorage 'starship-cadet-arrived'

// 22. LINES (dialogue engineer)
lineFor(who, kind, ctx) -> { text, id, tone } | null    // who: crewId or guest id; kind: 'greet', 'react.repair.mine', 'arc.tomas.3', ...
overheardFor(a, b, ctx) -> [ { who, text } ] | null
SHIP.lines = { ring: [ overheard/reaction ids x 200 ], serious: day }     // save.lines (chat lines' recent-penalty is not saved)
LINE_CONDS (the frozen vocabulary)   LINE_TOKENS

// generated by content_gen.py from content/ (never hand-edited)
// ---- BEGIN LINES ----   LINES = { crew: { <id>: { <kind>: [ { t, c, tone, id } ] } }, bank: { ... }, pairs: [ ... ], reactions: { ... }, arcs: { ... } }
// ---- BEGIN MEETINGS ---- merged into MEETING_SCRIPTS at load
// ---- BEGIN TRADITIONS -- merged into SHIP_EVENTS at load

// 20 / 20c (social engineers; the social designer's plan, Part 6 and its appendix, is the authority)
relTier(id) relAdd(id, why, pts) mem(id, key) memAdd(id, key, data) memTold(id, key) warmth(id) affBand(a, b) bondOf(id, kind)
moodOf(p) beatOf(arcId) knowsNews(p, newsId) repBand(dept) knownFor() cue(kind) socialInvite({ trad, day, from })
// 13 (sim engineer): flag(key) flagSet(key) beside simNote

// 18. SHIP EVENTS (traditions engineer)
// SHIP_EVENTS.<id>.when gains: { every: 'week'|'2weeks'|'4weeks'|'quarter'|'year', weekday, week, quarterDay, dayOfYear, after: 'arrival', days }
// SHIP_EVENTS.<id>.ties = { galley: { dish, batch, meal }, garden: 'sow'|'tend'|'harvest', decor: id, tally: { kind, choices } }
season(d) -> 'sowing'|'greening'|'harvest'|'lanterns'

// 17. MACHINES & JOBS (systems engineer)
jobReserve(kind, day, at) -> jobId     // a real Tier 1 fault, due on cue, held for the player, needing a stored and a made part
```

A `.trad` file (sketch; the traditions engineer settles the grammar in wave 1):

```
@tradition tilesLeague
title: Tiles league
when: weekly tuesday 20:00
len: 90
where: 4-common tables
who: juniors 35%, rina always
anim: play
host: rina
ties: tally wins
mail: Tiles league tonight, 20:00, the junior common room. Rina is defending her title. Again.
thanks: Rina: "Next week. Bring your A game. Or any game."

== tap
- {host} is three games up and insufferable about it.   #funny
```
