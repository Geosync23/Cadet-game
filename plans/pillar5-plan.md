# Pillar 5 plan: the Works career, and ship-wide events

**DRAFT (2026-10-17, the Pillar 5 planner, branch `claude/pillar5-plan`).** Built on the user's direction of 2026-10-17 (two parts, each standing on its own: **expanded core gameplay** and **ship-wide events**) and on the suggested answers in `plans/pillar5-notes.md`, which the user hasn't answered yet. Where this plan depends on an answer, it says so; the planner updates it when the answers come. **Nothing is built until the user approves this plan.**

Read with `design-doc.md` ("The clockwork", "The player", "Works progression", "Ship-wide events", "Open questions"), `plans/pillar3-plan.md` (Part 2, the events and their framework), `plans/pillar4-plan.md` (Part 6: seats, waves, the collision rules this plan reuses), `TEAM.md`, `DEV_NOTES.md` ("Machines and wear", "Player needs and the device", "Ship events", "Hook register") and the handover notes for systems, player, events, galley and device.

A plain-language version for the user is `plans/pillar5-plan.html`.

---

## The pitch (one page)

After Pillars 2-4 the Wren runs itself, the crew have voices, you arrive by shuttle and the calendar is full. But your **job** is still the same on day 40 as on day 2: the crew catch nearly every fault before you, the inspect step tells you the answer, and nothing lets you grow past Tier 1. And only one big **ship-wide event**, the ion storm, is switched on; the diplomatic visit and the comet viewing wait on a shelf.

**Pillar 5 makes your work a career, and gives the ship its big stories.** Two halves, each standing on its own:

1. **The Works career (core gameplay).**
   - **Real faults reach you.** About half your 3-6 daily jobs are machines actually misbehaving, with a cause to find.
   - **Diagnosing is play.** Inspecting opens a small panel of the machine's parts with readings; you work out which part is failing from the readings and what you saw on the deck. A wrong guess costs time (you fetch the wrong part), never a fail.
   - **You get better.** Repairs on a kind of machine get quicker as you practise, told in words in your Record ("Ovens: you know these well"), no points.
   - **Tools:** the **diagnostic scanner** (spot wear on your rounds, so prevention is a real choice), and with Tier 2 the **pipe kit**.
   - **Your first promotion.** Experience, Calder's progress talks, a **supervised certification job**, a promotion moment, Officer rank, a new badge, and **your own cabin** (Spare 4-23, on the officers' corridor), which Pillar 4's "Come over" visits then use. Never passed over, only delayed.
   - **Tier 2 work:** faults with a symptom in one place and a cause in another (weak showers on Deck 4, the recycler on Deck 3), traced from the manifold room through the pipe galleries; the Deck 5 machine rooms and the spine's crawlways open with your Tier 2 key.
   - **The week's small duties made real:** the Wednesday drill and the Thursday bunk inspection.
   - **Night on-call** (opt-in, from Tier 2), and a few off-shift things that grow from the job: **tinkering** in the machine shop, **furnishing your cabin**, **logging stars** for Survey.
2. **Ship-wide events.** Each event is **one self-contained piece**: its own block of data, its own switch, its own test, playable on its own and reviewed by the user like a deck.
   - **Switched on:** the **comet viewing** (one gentle evening) and the **diplomatic visit** (built in Pillar 3).
   - **Built new, from systems already in the game:** the **power surge** (short), **the late supply shuttle** (short), **something in the garden** (the ship gets a pet), **shipboard illness**.
   - **Then, if the pillar has room:** **nebula drift** and **salvage**; and, if the user wants it, a new main event, **the Fleet inspection**.
   - **Small incidents** about once a week between the big events: a burst pipe, the lift stuck with someone in it, a galley alarm.
   - **Later pillars:** the Founding Day festival (waits for the real-phone crowd test), a Veyli vessel needs help, the déjà vu day.

**How it's built alongside Pillar 4:** the career lives in the parts of the game Pillar 4 barely touches (section 17 machines and jobs, section 15 the player, a new section 24), so it starts as soon as the user approves. The events start **after Pillar 4's wave 3**, when Pillar 4 is mostly writing. About **4 helpers** for the career, **2 more** for events; Pillar 5 never adds more than about 6 active sessions on top of Pillar 4. Four check-ins with the user.

---

## Where we start

- **The build:** combined **0.60.0** ("the writers' kit", Pillar 4 wave 1a). Pillar 4 is in wave 1b/2: about 15 helpers in one game file.
- **What the career has today** (section 17, the systems engineer; section 15, the player engineer; DEV_NOTES "Machines and wear"):
  - ~36 machine kinds in `MACHINE_KINDS` with `system`, `life`, `use`, `tier` and **one** `part` each; condition, five states, wear against an average day; visible faults on the decks (`machineLook`, `deckLook`); the ship health board.
  - The job list: service, repair, overhaul, restock; Works crew claim by `CREW_TIER`; easy jobs wait `CREW_LEAVE` (180 minutes) for you. **The crew are too good** (systems handover): nothing gets past worn, so you rarely meet a real fault.
  - Your job loop: take at the board, fetch (two-slot carry), make a part in the shop, inspect (`INSPECT_MINS` 3, which simply tells you what's wrong), repair, turn in. `jobReserve` (0.33.36) holds jobs for Pillar 4's first week.
  - **`PLAYER_TIER = 1` is a constant** in section 17, read by sections 15b, 17 and 19. Doors lock by tier (closets 1, plant rooms 2, batteries and junctions 3).
  - Occasions: progress talks with Calder (appointments in her office), commendations at an event's end, the ready room, the Captain's table.
  - The Wednesday drill (15:00, off-duty crew muster by the lift) and Thursday inspection (juniors tidy their bunks) are in the crew's day shapes (section 14); **you take no part**.
- **What the events have today** (section 18; handover-events.md): the framework (`SHIP_EVENTS`, phases, systems/routines/galley/jobs/news/moments/meetings/threads/traces, `eventNow`, `eventMod`, `MEETING_SCRIPTS`, the Captain's address, felt-everywhere moments, commendations). **The ion storm is on.** **The diplomatic visit is built with `draft: true`** (two galley threads, `dinnersLate` and `noHerbs`, agreed and waiting). **The comet viewing** is on paper in `plans/comet-viewing-draft.js`. Nothing else is built.
- **What Pillar 4 is changing that we must fit around:** varied days off for everyone; crew coming and going (the aboard set, transfers, rotation Sundays); a **reputation** system (by department and ship-wide Work, Kindness, Spirit); `lineFor` and baked lines; ~30 traditions with a voice budget; the arrival and the first week (which reserves Tier 1 jobs for you on Days 1-2); your own cabin's "Come over" visits as a hook.
- **Pacing reality:** a ship day is 40 real minutes, a week about 4⅔ hours. The first promotion at about 2-3 ship weeks is about 10-14 real hours of play; the event list at one main event every 1-2 weeks lasts about 14 ship weeks (about 65 hours).

---

## Part 1: the Works career (core gameplay)

Each piece below is a self-contained step, numbered **C1-C10** for the seats and waves. Every number (shares, minutes, counts) is a starting point, tuned in play.

### C1. Real faults reach you (systems engineer, section 17)

*The problem:* crew claim every job of your tier after `CREW_LEAVE` and catch wear early, so you mostly do routine servicing.
- **Keep the 3-6 jobs a day** (agreed 2026-10-16), but aim for **about half of them real faults** (faulty or failing machines), half servicing and runs.
- Levers, all in section 17: crew **rounds find worn machines later** (the `found` delay of service jobs), crew **leave Tier 1 faults longer** for you on your shift days (a separate `CREW_LEAVE_FAULT`, say 4 hours), and **fewer Works crew free** for Tier 1 work while bigger jobs are open.
- **Off days and nights unchanged:** on your days off and at night the crew take everything as now, so the ship never suffers for your rest.
- **Pillar 4's first week** keeps its reserved jobs (`jobReserve`); C1 never touches a reserved job. `intro_check` must still pass.
- *Test:* `machine_check` measures, over 14 days with a stand-in player who takes the top job each hour: jobs left for you per shift day (3-6), the share that are faults (40-60%), ship health with the real crew and no player still 85 or more.

### C2. Diagnosing is play (systems: the data; player engineer: the panel)

*The design's open question ("how does diagnosing look?") answered by the suggested default (notes Q3).*
- **Machines get parts.** Each kind lists 3-5 parts (`parts: ['filter', 'pump', 'seal', 'relay']`), each with a reading and the symptom it causes (a pump: low flow, a drip; a relay: flicker; a filter: stuffy air). A fault picks its failing part **from the machine's id and the fault's hour** (hashed, never `R()`), so it's the same on every replay.
- **Inspecting opens a panel** in the device's screen style (a view described by section 15 and drawn by section 19's skin): the machine's name and state, and each part with a reading (`Flow 42% · low`, `Seal ok`, `Relay chatter`). Usually one reading is clearly off; sometimes two are, and the symptom you saw on the deck tells them apart.
- **You choose the part to fetch** (the job's fetch step then names it). Pick wrong and the repair tells you ("Fitted a new seal. Still low flow: it's the pump.") and you go back for the right part. That's the only cost. **No mini-games**: reading and deciding, then the physical fetch-and-fix as now.
- **Crew don't do this:** they always "know" the part, as now.
- **The scanner (C4)** reads the panel from a distance and earlier.
- *Test:* `player_check`: inspect shows the panel; the right pick finishes; a wrong pick costs a fetch and then finishes; the failing part is the same on two runs; every kind has parts.

### C3. You get better with practice (progression engineer, section 24)

- **Skill per machine kind:** each repair, service or overhaul you finish counts for its kind. Repair minutes shrink with practice: 100% for the first, about 80% after 5, 65% after 15 (a floor). Tier 2 kinds start fresh.
- **Shown in words only** (the user: "what you know" counts are too gamey): the Record says "Ovens: you know these well", "Scrubbers: still learning". Crew notice too: a reaction line (Pillar 4's `lineFor`, kind `reaction`) the first time you fix a kind quickly.
- Stacks with the needs' bonuses (energy, social) as section 15 already multiplies task speed.
- *Test:* `career_check`: minutes fall with practice and stop at the floor; the Record's words change at the thresholds; saved and restored.

### C4. Tools (progression: owning them; systems: what they read; player: using them)

- **The diagnostic scanner** (Tier 1, handed over by Calder at your first progress talk, or after your fifth job): tap it on the device while near a machine to see its condition and a hint of the coming fault, from across the room. It turns your rounds into **prevention**: a worn machine spotted early is a short service, not a repair later (the design's "Prevention" point). Jobs you found yourself are marked "found by you" and count a little more toward experience.
- **The pipe kit** (Tier 2, given at promotion): needed for Tier 2 water and air jobs, and lets you read the manifold board (C6).
- The conduit tester and the calibration rig wait for Tiers 3-4.
- Tools live in a **Tools** line on the device and in your locker; they don't take a carry slot.
- *Test:* `career_check` and `player_check`: you get the scanner at the right moment; scanning a worn machine posts a service job "found by you"; Tier 2 jobs need the pipe kit.

### C5. Your first promotion (progression engineer, with on-call rows)

- **Experience** (no number on screen): jobs finished in your tier, weighted by how bad it was (a service 1, a repair 2, a failing repair 3, an overhaul 4), how early you caught it (found by you +1) and doing it right (no wrong part +½).
- **Trust:** reliability: turning up for shifts, not dropping jobs half done, the drill (C7). **It reads Pillar 4's Work reputation** (social A's ship-wide Work axis) instead of keeping a second score, so the ship has one idea of how reliable you are. *(Agree with social A; if Work reputation isn't in yet, a stand-in counts shifts and dropped jobs.)*
- **Progress talks** (already built as occasions) gain Calder's words about how close you are: "not yet", "getting there", "I'll set your certification next week". About 2-3 ship weeks of steady work.
- **The certification job:** Calder sets it by Mail and at the board. A real Tier 2 job (the water recycler or a Deck 4 air scrubber goes faulty on the day; held for you like Pillar 4's `jobReserve`), with Calder (or Zeke Torres on her days off) **following you** (Pillar 4's lead-and-follow walker mode, the follower side) and saying a line at each step. Do it and you pass. Do it badly (wrong parts twice, or walk away) and she tells you what to work on and sets another in a week: **never passed over, only delayed** (notes Q5).
- **The promotion moment:** at the board the next morning, Calder hands you the Officer's badge in front of the Works crew (a short meeting with dialogue, `MEETING_SCRIPTS`); the Captain's congratulations by Mail; the news spreads (`simNote('promoted')`, chatter); your uniform's badge changes; Record, Roster and Crew show the new rank.
- **Your own cabin:** **Spare 4-23** on Deck 4's officers' corridor (the officers keep their 10 window cabins; 4-24 stays a spare). Your bed moves (`playerBed()` reads the career), your locker moves, the cabin door opens for you (the tier-lock check reads the career), and Tomas says goodbye to you as a bunkmate (a Pillar 4 moment kind, if social B has one). Pillar 4's **"Come over"** visits start working.
- **What changes in play:** Tier 2 jobs on the board are yours to take (`PLAYER_TIER` becomes `playerTier()`), the plant rooms open, the pipe kit, on-call (C8).
- *Test:* `career_check` end to end on paper (experience, the talk's words, the certification set, a failed then passed run, the promotion, the bed and doors), a live certification run, determinism twice, save round-trip, and a save from before Pillar 5 loads as Tier 1.

### C6. Tier 2 work: tracing connected faults (systems + deck architect 2)

- **Connected systems** (the design's Tier 2 row): water and air machines are joined by pipes and ducts in a small graph (`links: { 'recycler-1': ['manifold-3', 'showers-4a'] }`). A fault can **start upstream**: the symptom shows on Deck 4 (weak showers), the cause is a valve in the manifold room or the recycler on Deck 3.
- **The manifold room board** (Deck 5) and the **pipe galleries** show flow along each line (with the pipe kit): you follow the low reading back to its cause. The job card says where the symptom is; finding the cause is yours.
- **Places:** the Deck 5 machine rooms (air plant, fan hall, manifold room), the pipe galleries and the spine's crawlways (Deck 4's ladder hatch `h,20,14` is already tier 2) get real machines with panel places, so crew and you can walk to them. This also fixes the systems handover's stand-ins (the fan, the door gear, the washers).
- **Tiers 3-4** (shutdown planning, team jobs on the engines) wait for a later pillar (notes Q6).
- *Test:* `machine_check`: every Tier 2 machine has a panel place; a traced fault's symptom and cause are on different machines; fixing the cause clears the symptom; crew claim Tier 2 jobs only by `CREW_TIER`. `deck_check`: the new rooms reachable, draw calls under 450.

### C7. The week's duties: the drill and the inspection (progression; sim on call)

- **The Wednesday drill** (15:00, already in the crew's week): you get a device toast at 14:50; **muster at your station** (the Works bay for Works crew) for 15 minutes. Turn up and it counts toward trust; miss it and Calder says something the next day. Nothing worse.
- **The Thursday inspection:** the duty officer walks the junior wing at 06:30 (after promotion, the officers' corridor). Your bunk and uniform are checked: a grubby uniform (the laundry already exists) or an untidy locker gets a gentle remark, a tidy one a nod and a little trust. Tidy your berth by tapping it in the morning (a short activity, section 15).
- *Test:* `career_check` and `day_check` on a Wednesday and a Thursday: everyone still reaches their places; you at the muster count; the remark and the nod.

### C8. Night on-call (progression; player on call)

- **From Tier 2, opt-in** in the device's Settings ("Put me on the on-call rota"): about one night a week (seeded, never the night before your day off or a tradition you marked).
- On an on-call night, if a machine **breaks or goes failing** after 21:00 (or a small incident happens, Part 2), your device **wakes you** (the sleep skip stops at that minute), you fix it, go back to bed, and get a lie-in (shift starts 08:00).
- Off by default; never wakes you more than once a night.
- *Test:* `career_check`: the rota is seeded and the same twice; a break wakes you; nothing wakes you when off-call.

### C9. Off-shift things that grow from the job (player engineer, section 15)

- **Tinkering** in the machine shop on your own time: make small things (a lamp, a mug rack, a toy for the ship's pet later), which become Pillar 4's machine-shop gifts or decor for your cabin. Reuses the "make a part" activity.
- **Furnishing your cabin** (after promotion): a few spots in 4-23 take a thing you bought at the store or made in the shop (a rug, a plant, a lamp, a shelf of keepsakes). Drawn from the existing kit, at most 4 extra draw calls.
- **Logging stars** at the observatory telescope (Deck 2) for Survey: a short activity; Survey crew warm to you a little; a line in the Record after ten.
- *Test:* `player_check`: each activity starts, poses, finishes and saves; `deck_check` with a furnished cabin.

### C10. The device's work apps (progression registers its own; device on call)

- **Work log** (in Jobs): what you fixed, when, found by you or not, and who noticed (the last 30).
- **Record:** the certification in words (from C5), skills in words (C3), the tools you have (C4).
- **Settings:** the on-call switch (C8).
- The progression engineer registers these through `deviceApp` from section 24 (section 20 already does this), so section 19 needs no change. The device engineer is asked only if a view needs something the skin can't draw yet (the diagnosis panel's readings, maybe).

---

## Part 2: ship-wide events

### What "standing on its own" means (notes Q15)

- **One event, one block.** Each event is a self-contained entry in `SHIP_EVENTS` inside its own marked sub-block of section 18 (`// 18e. EVENT: powerSurge`), with its own meeting scripts, guests, news and traces, and its own hash key. Removing the sub-block removes the event and nothing else breaks.
- **One switch each.** `draft: true` keeps it off. A **"try this event"** switch for review builds (a URL like `?event=powerSurge&day=12`) starts any event on any day from a fresh game, so the user can review each one alone.
- **No event depends on another having happened.** The agreed order stays for a new game (`EVENT_ORDER`), but each event checks only the ship as it is (salvage → garden creature is a later-playthrough option, not a dependency).
- **One test each:** `events_check.py --event <id>` runs that event alone, on paper twice (identical) and live at its busiest moment; the full run does all of them.
- **One review each:** like a deck, each event is played and signed off by the user (in pairs if the user prefers).

### Framework additions (events engineer A, section 18, first)

- The "try this event" switch, `--event` in `events_check`, the sub-block markers.
- **Recurrence** (notes Q18): after the list is done, events come back in variations, rarer (a storm about every 6 weeks, a visit every 8), seeded by day; `EVENT_ORDER` gains a second, repeating round.
- **Small incidents** (notes Q17): a lighter shape, `kind: 'incident'`, an hour or two on one deck, no warning or threads, one moment and one job. About one a week, never on an event day or a tradition evening (the voice budget). They're on-call jobs at night (C8). The incident table and its timing are the events engineer's; the machine side is section 17's.
- **The conference table** (Pillar 3's occasion, waiting for a senior briefing) gets its first use (the surge's or the illness's briefing).
- **Each event's Tier 2 part** (notes Q19): a job or meeting only a Tier 2 player gets, read from `playerTier()`.

### The events (each self-contained; in the agreed order)

Each card: what happens · what it touches (and whose section) · its Tier 2 part · draw-call notes · its test. Lines are written by the events engineers in the event's block, as in Pillar 3, and read for tone by Pillar 4's head writer (or a writer freed up in Pillar 4's wave 4, the user's call: open question 4).

**E1. Comet viewing** (short; switch on). Drafted and tested on paper at 0.34.18 (`plans/comet-viewing-draft.js`): Sato's Mail, the comet at the bow lounge windows and the observatory at 21:00, traditions give way, chatter the next day. *Touches:* 18 only; the sky (`skyComet`, the performance engineer, uniforms only, no new draw calls). *Tier 2 part:* none (a gentle evening for everyone). *Test:* events_check's COMET block; day_check at 21:15.

**E2. Diplomatic visit** (main; switch on). Built at 0.34.16-0.34.18 with `draft: true`. Left: the galley's `dinnersLate` and `noHerbs` threads and the `herbs` key (agreed, waiting for the go), then lift the draft. *Touches:* 16 (galley rows), 18. *Tier 2 part:* keep the guest cabins warm on a heating line (C6's graph). *Test:* events_check, food_check, day_check 1 and 27, deck_check, player_check, cadet_test.

**E3. Power surge** (short, one day; new). A Deck 6 junction trips; two decks drop to emergency lighting for up to an hour; the lift runs slow; the engine crew and Works rush. *Touches:* 17 (a junction fault, `eventMod('wear', 'power')`), 18, the decks' emergency light mood (exists from the storm). *Tier 2 part:* the conference-table briefing and resetting the breakers in the battery room's anteroom. *Draw calls:* none new. *Test:* blackout minutes measured; the two decks' lights; crew reroute.

**E4. The late supply shuttle** (short, 2-3 days; new). Wednesday's delivery doesn't come: filters run short (`NO_MAKE` parts wait), the machine shop gets busy, the menu goes bland (rationing). Fully from the numbers (the shortage Mail grows into it). *Touches:* 17 (`DELIVERY` skipped, stock), 16 (a bland menu key, galley row), 18. *Tier 2 part:* rig a filter bypass on a scrubber line. *Test:* machine_check's stock never below 0; food_check through it.

**E5. Something in the garden** (main, 3-4 days; new). Nibbled leaves, then the herb wall bare; Brennan furious; traps made in the machine shop (a real make job), set where it's seen, checked each morning; a volunteer garden watch at night; caught at a gathering, named, and **the ship's pet** lives in the garden and wanders the Commons for the rest of the game. *Touches:* 16 (garden crop loss, a herbless menu), 17 (trap make jobs), 18, the pet as one small walker (performance engineer: one rig, Deck 3 only, about 3 draw calls), trap props (deck architect 2: one instanced mesh). *Tier 2 part:* the irrigation room's pump was nibbled (a traced fault). *Test:* the garden's yield recovers; the pet saved; draw calls on Deck 3 at dinner with the pet.

**E6. Shipboard illness ("the Wren cough")** (main, 3-4 days; new). The infirmary fills; sick crew stay in their bunks (a schedule rule: bunk all day, a nurse visits); a bunk room quarantined; about a fifth of the crew off, so more jobs are left for you; soup by cart; **you can catch it** if your hygiene is low (energy drains faster; rest helps). *Touches:* 14 (the sick rule, sim engineer), 15 (the player's cough, player engineer), 16 (soup by cart), 17 (fewer free crew, from the plans), 18; Pillar 4's aboard set and beds. *Tier 2 part:* keep the air plant clean (a scrubber series). *Draw calls:* fewer crew walking. *Test:* day_check on the peak day (nobody stuck, the sick in their beds), jobs left for you rise, everyone recovers.

**E7. The Fleet inspection** (main, 2 days; new, **only if the user wants it**, notes Q17). A Fleet inspector arrives by the Tern (a guest), the ship spends a day fixing and cleaning (event jobs: every worn machine is a job), the inspector tours with Vance (a walker with a lead), asks crew questions (a meeting at the board with Calder and you), and a report by Mail. *Threads:* machines worn on the day; ship health; crew courtesy. *Tier 2 part:* you walk the inspector through the manifold room. *Test:* the tour's route; the report's bands.

**E8. Nebula drift** (main, 3 days; if room). Every window fills with colour (sky mood on every deck, uniforms only), the sensor array overloads [Tier 1: carry coolant], strange dreams (energy refills slower, social faster), the observatory full each night; a visiting scientist's talk. *Touches:* 18, the sky (performance), 14/15 needs multipliers (`eventMod('need', …)`, exists), a guest (crew designer). *Test:* day_check at the talk; energy and social on paper.

**E9. Salvage** (main, 3 days; if room). The Tern flies out (the first time the shuttle moves: the bay doors open and it leaves), comes back with crates, cart jobs to sort them, one crate holds an excellent part (one machine wears slower for good), an auction evening in the lounge. *Touches:* 17 (crates in the hold, the part), 18, the shuttle animation (deck architect 2 + performance: the Tern as one group that moves). *Test:* the Tern leaves and returns; crates sorted; the wear change saved.

**Small incidents** (with the framework; about one a week). I1 **burst pipe** (a corridor on Deck 4 wet, crew reroute, a water job), I2 **the lift sticks** (a crew member stuck for 20 minutes, an urgent transport job, chatter), I3 **the galley alarm** (a scorched pan, the mess clears for 10 minutes, Brennan embarrassed). Each one is a self-contained block too.

**Later pillars:** the **Founding Day festival** (the whole crew on the plaza: waits for the real-phone crowd test), **a Veyli vessel needs help**, **the déjà vu day** (replaying a whole day is the riskiest thing on the list: the save, the clock and every seeded system must replay exactly). **Crew rotation day** is Pillar 4's rotation Sundays, not a separate event (notes Q16).

---

## Part 3: not colliding with Pillar 4

### Which parts of the game each touches

| Section | Pillar 4 (who, when) | Pillar 5 (who, when) | How they stay apart |
| --- | --- | --- | --- |
| 17 machines & jobs | on call only (`jobReserve`, notes) | **systems engineer, step 1 on** (C1, C2 data, C6, incidents' machine side) | Pillar 4 needs only `jobReserve` and `simNote('job')`, both stay as they are; `intro_check` runs on every section 17 push |
| 15 player | on call (kit bag, device lock, gift tags) | **player engineer, step 1 on** (C2 panel, C4 use, C7 tidy, C9, the cough) | one owner for both; Pillar 4's rows first |
| 15b interactions | on call | on call (tap targets for the new places) | small rows |
| **24 WORKS CAREER (new)** | — | **progression engineer, step 1 on** | a new lazy section, its own owner; hooks one-line, typeof-guarded, in the register |
| 19 device | **busy waves 2-3** (Settling in, New game, seasons, reputation) | registers its views from section 24 (`deviceApp`); device on call only for skin additions, **after Pillar 4's wave 3** | no Pillar 5 edits in section 19 before then |
| 13/14/10 sim | **busy all of Pillar 4** (aboard set, escort, routines) | on call: `playerBed()` reads the career, the sick-in-bunk rule (E6), event routines | two or three one-line rows, after Pillar 4's wave 3 |
| 16 galley | on call (tasting table, roast, suppers) | on call (E2 threads, bland menu, soup, herbless menu) | rows, in turn |
| 18 events | **traditions engineer, busy to wave 4** (`.trad` loader, ~30 traditions) | **events engineers, step 2** (after Pillar 4's wave 3) | Pillar 5 adds only marked sub-blocks `18e` at the end of section 18; the traditions engineer reviews the framework edits; the voice budget includes events |
| 20/20c social | busy all of Pillar 4 | reads: Work reputation for trust, `relAdd`, `lineFor` kinds; asks social B for a "new cabin" goodbye moment | reads only; any new social row through the lead |
| 22 lines / content | busy (writers) | event and career lines read for tone by the head writer | events' text lives in their blocks; career reactions as `content/` lines if the dialogue engineer agrees |
| DECKS[n] | deck architect, Deck 3 mostly (garden, lounge, mess, promenade), Deck 4 Bunk 1, Deck 5 tea corner | **deck architect 2**: Deck 5 machine rooms, manifold room, pipe galleries, Deck 4 spine and Spare 4-23, Deck 6 junctions, event props | different rooms; Pillar 5 places in a marked `// P5 places` block per deck |
| 8/8b crowd, sky | performance, on call | on call: the comet and nebula skies, the pet, the Tern moving, the inspector | rows |
| 9 roster | crew designer, wave 1a | on call: event guests (the inspector, the scientist) | the generator only |

### Rules (reusing Pillar 4's)

- New code in **new sections** (24, and `18e` sub-blocks), lazy at load, owned by one seat.
- **`PLAYER_TIER` → `playerTier()`**, done once, early and inert: section 17 declares `function playerTier() { return typeof careerTier === 'function' ? careerTier() : 1 }` and keeps `const PLAYER_TIER = 1` as a fallback name for one release; sections 15b, 17 and 19's readers switch to `playerTier()` in one combined build with `cadet_test` ALL IDENTICAL.
- **Hash keys** (checked free by the build master, 2026-10-17): the career 850-899 (section 24; no `k + 100` jitter there). New ship-wide events 950-979 and small incidents 980-999, because every section 18 entry also uses `k + 100` for its end jitter (so 1050-1099 is theirs too). Not 352-399: their jitter would land in the traditions' 434-499. 930 is already used in the game.
- **The save:** `save.career` (tier, experience, skills by kind, tools, on-call, the work log ring, certification state), small and read defensively; `SAVE_V` stays 2.
- **Merge order:** Pillar 5 branches go **after** Pillar 4's in each round: … content → systems (17) → career (24) → player (15) → deck architect 2 → events A/B (18e).
- **Simple notes on the bus:** `simNote('promoted')`, `simNote('certify', { step })`, `simNote('diagnose', { right })`, `simNote('incident', { id })`, so Pillar 4's lines and reputation can react without new hooks.

---

## Part 4: staffing, waves and check-ins

### The seats

| # | Seat | New or existing | Branch | Builds | Owns (only these) | Steps |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Systems engineer | existing role, **fresh session** (the last systems engineer retired; section 17 is held by the sim engineer meanwhile, who hands it back) | `claude/ship-systems` | 0.33.38+ | section 17; `machine_check.py` | 1, 2, 3 |
| P2 | Progression engineer | **new** | `claude/works-career` | 0.44.x | new section `// 24. WORKS CAREER`; `career_check.py` | 1, 2, 3 |
| P3 | Player engineer | existing | `claude/player-needs` | 0.28.23+ | section 15 (Pillar 5 rows); `player_check.py` | 1, 2, 3 |
| P4 | Deck architect 2 | **new** (the Pillar 4 architect is busy on Deck 3) | `claude/decks-p5` | 0.47.x | `DECKS[n]` places and dressing in Pillar 5's rooms (Part 3), in `// P5 places` blocks; kit added at the end of 4b | 2, 3, 4 |
| P5 | Events engineer A | **new** (or the Pillar 3 events engineer's standby session, if it has memory left) | `claude/shipwide-a` | 0.49.x | the framework additions in section 18 (agreed with the traditions engineer); sub-blocks `18e` for E1, E2, E3, E4, E7 and the incidents | 3, 4 |
| P6 | Events engineer B | **new** | `claude/shipwide-b` | 0.45.x | sub-blocks `18e` for E5, E6, E8, E9 | 3, 4 |

**On call** (existing helpers, small rows): device (section 19 skin additions, after Pillar 4's wave 3), sim (`playerBed()` from the career, the cabin door, the drill muster place for you, the sick rule, event routines), galley (E2's threads, menus, soup), performance (skies, the pet, the Tern, gathering draw calls), crew designer (event guests), social A (Work reputation as trust; reactions), dialogue/head writer (tone). **This planner** stays on through step 1 to answer plan questions, then hands over (`plans/handover-pillar5-planner.md`).

**At most 4 Pillar 5 sessions in step 1, 6 at the peak (step 3)**, when Pillar 4 is in wave 4 with fewer active seats.

### The briefs (ready to paste)

**Every brief starts with this paragraph:** "You are the <seat> for Starship Cadet's Pillar 5. Read CLAUDE.md, then DEV_NOTES.md, plans/pillar5-plan.md (your seat in Part 4 and the parts it names), plans/pillar5-notes.md (the user's answers), plans/pillar4-plan.md Part 6 (the rules for sharing the one game file with Pillar 4, which is building at the same time), TEAM.md, and your predecessor's handover note if your role had one. Push only to <branch>. Touch only what your seat owns; anything else goes through its owner via the lead. Each turn: small exact-string edits (never rewrite the game file), bump the build in the HUD, add a DEV_NOTES row, run the tests (one browser check at a time; always `intro_check` too when you touch jobs, the player or the clock), commit, push, and report to the lead (session_01PJtmxWgAPLebXSZKP6ZRpG) with send_message. Hooks into other sections are one-line, typeof-guarded, and listed in DEV_NOTES' hook register. Hand over at about 70% memory with plans/handover-<role>.md. Commit messages end with the Co-Authored-By line; never put model names anywhere else."

1. **Systems engineer** (0.33.38+, `claude/ship-systems`; a fresh session: read `plans/handover-systems.md`, then agree the hand-back of section 17 with the sim engineer, session_01R6RBwwBM9aorpsqDCrztDU, who holds it during Pillar 4). Section 17. Step 1: `playerTier()` (inert, Part 3's rule); parts per machine kind with readings and symptoms, and the failing part hashed from the machine and hour (C2's data, `machineParts(id)`, `faultPart(jobId)`, `fitPart(jobId, part)` → right or wrong); real faults for you (C1: `CREW_LEAVE_FAULT`, the `found` delay, crew busier on bigger jobs) with `machine_check` measuring jobs and fault share per shift day; `scanMachine(id)` for the scanner (C4); "found by you" jobs. Step 2: Tier 2 kinds and the pipe/duct graph (C6, `links`), traced faults (symptom on one machine, cause upstream), certification jobs held for you (`jobReserve`-style, slot 'certify'), real machines for the stand-ins once deck architect 2 adds panel places. Step 3: the machine side of incidents and events (E3 junction, E4 delivery, E5 traps and pump, E9 the salvaged part). Never change a reserved job's behaviour; run `intro_check` on every push.

2. **Progression engineer** (0.44.x, `claude/works-career`, new). A new lazy section `// 24. WORKS CAREER` (after section 21) and `career_check.py`. Step 1: on paper first: `SHIP.career` and `save.career`; `careerTier()`; experience from `simNote('job')` (weights in C5); skill by kind and `careerSpeed(kind)` (C3) for section 15's repair minutes; tools (`careerHas('scanner')`) and the scanner's hand-over; the drill and the inspection for you (C7, with the sim engineer's muster place); the work log; the device views (Record words, work log, Tools, Settings) registered with `deviceApp` from section 24. Step 2: trust (reads social A's Work reputation, else a stand-in); Calder's progress-talk words; the certification job (set, followed by Calder or Torres, passed or delayed); the promotion meeting (`MEETING_SCRIPTS` entry, agreed with the traditions engineer), the Captain's Mail, `simNote('promoted')`; the cabin move (asks the sim engineer for `playerBed()` and the door); on-call (C8). `career_check`: end to end on paper, live certification, determinism twice, save round-trip, old saves load as Tier 1.

3. **Player engineer** (0.28.23+, `claude/player-needs`). Section 15. Step 1: the diagnosis panel (C2: a view in the device's screen style when you inspect; pick a part; the job's fetch names it; the wrong-part message; `simNote('diagnose')`); repair minutes × `careerSpeed(kind)`; using the scanner (C4); tidying your berth (C7). Step 2: on-call waking (the sleep skip stops; the lie-in); tinkering (C9, reusing "make a part"); furnishing spots in your cabin; logging stars. Step 3: catching the cough (E6). Keep `player_check` current.

4. **Deck architect 2** (0.47.x, `claude/decks-p5`, new). Read the Pillar 4 deck architect's handover and DEV_NOTES "How decks work" first. Places and dressing only in Pillar 5's rooms, in a `// P5 places` block per deck: step 2: the Deck 5 machine rooms (air plant, fan hall, manifold room with its flow board), the pipe galleries and the spine's crawlways with real machines and panel places (C6); panel places for the stand-ins (lift, washers, fan, door gear, reactor, coils); Spare 4-23 dressed as your cabin with 3-4 furnishing spots; the Works muster spot for the drill. Step 3-4: event props, each within its budget (at most 6 draw calls, only on its deck, only in its window): traps (E5), crates in the hold (E9), the inspector's clipboard stand (E7), quarantine sign (E6). `deck_check` on every push; Decks without changes pixel-identical.

5. **Events engineer A** (0.49.x, `claude/shipwide-a`, new; hired after Pillar 4's wave 3). Read `plans/handover-events.md` and DEV_NOTES "Ship events" first; agree every framework edit in section 18 with the traditions engineer. The framework additions (the `18e` markers, the "try this event" switch, `events_check --event`, recurrence, the incident shape, the conference table's first use, Tier 2 parts); then E1 comet (paste from `plans/comet-viewing-draft.js`), E2 the diplomatic visit (the galley's threads, then lift the draft), E3 power surge, E4 the late supply shuttle, the small incidents, and E7 the Fleet inspection if the user wants it.

6. **Events engineer B** (0.45.x, `claude/shipwide-b`, new; hired with A, once A's framework is in). E5 something in the garden (with the ship's pet), E6 shipboard illness, then E8 nebula drift and E9 salvage if the pillar has room. Same rules as A; your sub-blocks only.

### Steps and order (tied to Pillar 4's progress)

**Step 0: approval (now).** The user answers `plans/pillar5-notes.md` and approves this plan. No code before that.

**Step 1: the work day (starts when the user approves; runs alongside Pillar 4's waves 2-3).** Seats P1, P2, P3 (3 sessions). C1, C2, C3, C4, C7, C10's first views.
- **Gate 1a (the lead):** a combined build where all of it is **inert** (`playerTier()` returns 1, the career on paper): `cadet_test` ALL IDENTICAL, every check passes including `intro_check`.
- **Check-in P5-A with the user:** play a work day: real faults, the diagnosis panel, the scanner, practice making repairs quicker, the drill and the inspection.

**Step 2: the first promotion (after check-in P5-A; the cabin move waits for Pillar 4's wave 3 to finish the aboard set, because both touch beds).** Seats P1, P2, P3, P4 (4 sessions); sim on call. C5, C6, C8, C9.
- **Check-in P5-B with the user:** play from a save near certification: the certification job, the promotion, your own cabin, a traced Tier 2 fault, a night on call.

**Step 3: the first events (after Pillar 4's wave 3 and its check-in B, when Pillar 4 is mostly writing).** Seats P1, P5, then P6; P2-P4 finishing. The framework additions, E1 comet, E2 diplomatic, E3 power surge, the small incidents.
- **Check-in P5-C with the user:** try each event alone with the switch, and a new game from the storm to the visit.

**Step 4: the big events.** P5 and P6, P1 and P4 on rows. E4 late supply, E5 garden (and the pet), E6 illness; E7 inspection if wanted; then E8 nebula and E9 salvage if there's room.
- **Check-in P5-D with the user:** each event played (in pairs); the full new-game run order; then a pull request to `main` with the user's OK.

**Tests every turn** (as in Pillars 2-4): `cadet_test.py`, `deck_check.py`, `day_check.py` (plus a Wednesday drill, a Thursday inspection, and each event's busiest day), `player_check`, `food_check`, `machine_check`, `events_check` (now with `--event`), `interactions_check`, `social_check`, `device_check`, `intro_check`, `lines_check`, and the new **`career_check.py`**. Check-runner sessions run them in parallel on `claude/integration-test`.

### Test changes

- **New `career_check.py`** (P2): experience, skill, tools, the drill and inspection, certification (pass, delay, pass), promotion, cabin and doors, on-call, the work log, saving, determinism twice, an old save.
- **`machine_check`** (P1): jobs left for you per shift day and the fault share; every kind has parts; the failing part is the same twice; right and wrong fits; the Tier 2 graph and traced faults; panel places for every machine; incidents' machine side; stock never below 0 through the late shuttle.
- **`player_check`** (P3): the panel, the wrong-part trip, quicker repairs, the scanner, tidying, waking on call, tinkering, cabin spots, star logging, the cough.
- **`events_check`** (P5/P6): `--event <id>` alone from a fresh game on any day, twice identical, live at its busiest moment; the switch; recurrence; incidents never on event days or tradition evenings.
- **`day_check`**: the drill and inspection days; each event's peak (the illness's sick in their beds, the comet at 21:15, the inspection's tour); draw calls under 450.
- **`deck_check`**: the new rooms and places reachable; your furnished cabin; event props on and off.
- **`intro_check`** (Pillar 4's) on every push that touches jobs, the player or the clock.

---

## Risks

- **Phone draw calls (450 ceiling).** New rooms on Deck 5 (machine rooms, galleries), a furnished cabin, event props, the pet, crowds at the comet and the inspection's tour. *Answer:* the props budget (at most 6 draw calls, one deck, only in its window); the cabin's spots at most 4; the pet one rig; skies as uniform changes only (no new meshes); `deck_check` and `day_check` at each new room and each event's busiest minute; the performance engineer on call.
- **Determinism.** Diagnosis, real faults, incidents, on-call nights and recurrence all choose things. *Answer:* every choice hashed from ids and the day or hour (never `R()`), checked by running twice; the career has no randomness at all.
- **The one-file merge load** (Pillar 4's ~15 helpers plus Pillar 5's). *Answer:* new section 24 and `18e` sub-blocks; one-line hooks in the register; Pillar 5 merged after Pillar 4 each round; at most 4 Pillar 5 sessions until Pillar 4's wave 3 is done; events wait until Pillar 4 is mostly writing.
- **Breaking Pillar 4's first week.** C1 changes how jobs reach you; the week reserves jobs on Days 1-2. *Answer:* reserved jobs are untouched; `intro_check` on every push to sections 15 and 17.
- **`PLAYER_TIER` is read in four sections.** *Answer:* `playerTier()` done once, early, inert, with `cadet_test` identical.
- **Two ideas of reliability** (the career's trust and Pillar 4's Work reputation). *Answer:* the career reads the reputation; one score.
- **Beds and the aboard set.** Your move to 4-23 touches beds while Pillar 4's crew coming and going changes them too. *Answer:* the cabin move waits for Pillar 4's wave 3; 4-23 is a spare no crew or guest uses (check with the crew designer's reserve pool).
- **Too gamey.** Experience, skill and trust could turn into numbers on screen. *Answer:* words only, everywhere (the user's rule from Pillar 4).
- **Diagnosis feels like a quiz.** *Answer:* usually one reading is clearly off; wrong guesses cost only a walk; the scanner makes it easier; tuned at check-in P5-A.
- **Too much happening.** Traditions (~30), events, incidents, on-call. *Answer:* incidents never on event days or tradition evenings; the events' voice budget joins the traditions'; on-call opt-in and at most once a night.
- **Usage limits.** *Answer:* small staffing (3-6), the lead's hourly check-in, and the user's go-ahead before each step.
- **Helpers' memory.** *Answer:* the 70% handover rule; each event is small enough for one session to finish.

---

## Open questions (for the user, with the plan's defaults)

The 20 questions in `plans/pillar5-notes.md` (the plan assumes their suggested answers), plus:

1. **Your own cabin:** Spare 4-23 on the officers' corridor (no window), or should a window cabin open up (an officer moves)? *Default:* 4-23.
2. **Who follows you on the certification job:** Calder herself (Torres on her days off)? *Default:* yes.
3. **The Fleet inspection** as a new main event (E7): yes or no? *Default:* yes, after the illness.
4. **Who writes the events' lines:** the events engineers (as in Pillar 3), with the head writer checking tone, or a Pillar 4 writer moved over in wave 4? *Default:* the events engineers, tone-checked by the head writer.
5. **Reviewing events:** one at a time like decks, or in pairs? *Default:* in pairs, with the "try this event" switch.

---

## Appendix: shared formats (proposed; owners refine and tell the lead)

```js
// section 17 (systems): parts and faults
MACHINE_KINDS.recycler.parts = [
  { id: 'pump',   read: 'Flow',     bad: 'low flow',     sign: 'weak showers' },
  { id: 'filter', read: 'Clarity',  bad: 'cloudy',       sign: 'a smell at the basins' },
  { id: 'uv',     read: 'UV lamp',  bad: 'dim',          sign: null },
  { id: 'seal',   read: 'Pressure', bad: 'dropping',     sign: 'a drip' } ];
machineParts(id) -> [{ id, read, value, bad }]   // the panel's readings now
faultPart(jobId) -> partId                        // hashed from the machine and the hour (key 850)
fitPart(jobId, partId) -> { right, msg }          // a wrong part: msg names the symptom still there
scanMachine(id) -> { cond, state, hint }          // the scanner
MACHINE_LINKS = { 'recycler-3': ['manifold-5a'], 'manifold-5a': ['showers-4a', 'showers-4b'] }  // Tier 2 graph
playerTier() -> 1 | 2                             // careerTier() when section 24 is there

// section 24 (career)
SHIP.career = { tier: 1, xp: 0, skill: { oven: 7 }, tools: ['scanner'], onCall: false,
                cert: { state: 'none'|'set'|'passed'|'delayed', day, job }, log: [ /* last 30 */ ] }
careerTier(), careerSpeed(kind) -> 0.65..1, careerHas(tool), careerWords() -> Record lines
simNote('promoted', { tier }), simNote('certify', { step }), simNote('diagnose', { right, kind })

// section 18e (events): an incident
SHIP_EVENTS.burstPipe = { kind: 'incident', k: 980, when: { every: [5, 9] }, deck: 4, mins: 90,
  moment: { feel: ['hiss'] }, jobs: [{ kind: 'repair', machine: 'pipe-4c', urgent: true }],
  routines: [{ where: '4-corridor-s', rule: 'closed' }], news: [ ... ], draft: true }
```
