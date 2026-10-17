# Starship Cadet: Design Doc

Started as Design Doc v4 (Oct 14, 2026, @Geo Ma). Since then it has been a living document in the repo.

## How to use this document

- **This is the source of truth for what the game is.** The build (`starship-cadet.html`), the deck plans (`plans/`) and the dev notes (`DEV_NOTES.md`) follow it. The dev notes cover how the build works; this document covers what the game is and why.
- **When a design decision is made, update the relevant section here in the same commit** as the work that depends on it. Edit the section in place; don't append a changelog.
- **There are no version numbers any more.** Git history records every change, so the file keeps one name. The last PDF, v4, is kept in `archive/design-doc-v4.pdf` for reference.
- **Open questions live in one place,** the last section. When one is answered, move the answer into the section it belongs to and record it under "Answered".


## Vision & pillars

The CSV Wren is a little clockwork world: a properly simulated starship whose crew keeps it running day to day, whether you are watching or not. You arrive by shuttle as a new Works maintenance technician, and your work is part of what keeps the clockwork turning.

- **The ship runs itself.** Machines wear, supplies get used, crew follow shifts and do real work. The ship is never paused waiting for the player.
- **You are one of the crew.** The simulation treats you like everyone else: same job list, same needs, same schedule, a bunk in the junior wing like every other new hand.
- **Work is physical, not abstract.** You walk the ship, look, fetch, carry and repair. No mini-games standing in for the job.
- **Your work matters.** Fix the oven and breakfast is on time. Let the scrubber fail and the whole deck gets stuffy and short-tempered.
- **You grow by going deeper.** Progression means trust and access to the ship's more important systems, from galley ovens to the reactor.
- **Small, cozy, alive.** No combat, no fail screens. One ship you come to know like a home.


## The living ship

*Agreed with the user on 2026-10-15 (first written as the "Living Ship" addendum). It defines the crew-and-simulation phase, and where it changed earlier v4 text, the sections below have been updated to match.*

### The heart of the game

The CSV Wren is a living ship. Its systems have needs and wear down. Its 75 crew have needs, routines and relationships, and part of their routine is tending the ship. The player is one more pair of hands: just another crew member, never in command.

When the crew keep up, the ship hums. When they fall behind, or the player skips their jobs, it shows. It works like a city game, seen from the inside by one worker.

### Ground rules

- **Everything functional, everything simulated** (the project's ethos, agreed 2026-10-15). Every room and every function aboard is used, by the crew in their day-to-day and by the player. The gym is for working out, the booths are for calling home, the store is for shopping, the galley really cooks. Where full simulation isn't possible, get as close as we can, and never build a room that is only scenery.
- **No fail state.** A neglected ship gets shabby, uncomfortable and talked about. It is never lost. Losing would break the feeling of being just another crew member.
- **The player climbs but never commands.** They start on simple jobs (filters, lamps, carts), then move up to the engines and eventually sit in briefings with the Captain. Rank decides which jobs and which parts of an event reach the player.
- **18 ship hours take 30 real minutes** (agreed 2026-10-16). A whole 24-hour ship day lasts 40 real minutes, one ship hour is 100 real seconds, and a 7-day ship week is about 4⅔ hours of play.
- **The ship doesn't run while the game is closed.** Time stops when you leave and resumes where you were. Nothing catches up while you're away (confirmed 2026-10-16).
- **Sleeping skips time.** Getting into your bunk from 20:00 fades the screen out and wakes you at 06:00, with no question asked; earlier in the day the bunk tells you it's too early to sleep. The crew carry on through the night and catch up. The player's own needs (hunger, rest, hygiene) work as described under "Crew simulation".
- **All 75 crew are in the simulation:** about 60 on days and 15 on nights.


## What changed from v3

*Kept for history: this is what v4 changed from v3. Changes since v4 are in git history.*

V4 redesigns the ship around a daily loop across three decks and folds in everything agreed since v3 (dev notes of Oct 13–14). It stands on its own; the dev notes no longer override it.

- Six decks, not five, numbered from the top. The bridge gets its own small deck, and living is split into a Commons deck and a Quarters deck. Sleep on Deck 4, eat on Deck 3, work from Deck 5.
- Crew and rooms worked out. All 75 crew have a rank and a bed: senior suites on Deck 2, officer cabins and junior bunk rooms on Deck 4.
- Promotion means moving. Tier 2 brings Officer rank and your own cabin across the deck. The tier table now carries rank and room.
- You arrive by shuttle in the Deck 5 shuttle bay and find your own way up to your bunk.
- Deck 5 brief added: the ship's garage, built first so the Works bay can anchor the job list.
- Decks as data. The build now loads one deck at a time from a definition, with a ship-wide state that outlives it.
- The old living deck (build 0.3.x) is retired as a layout and kept as the style reference.
- Kept from v3: the clockwork, crew simulation, the job loop, the Works tiers and their gameplay, the art style, the named crew and the cozy tone.


## Setting & names

You serve in the Concord Survey Service, a peaceful exploration fleet, aboard the CSV Wren: a 75-person survey ship on a long tour of a frontier shared with the Veyli, a proud, ritual-minded people.

The Veyli and the frontier stay in the background for now. They are where story events will come from later, not the main thread of the game.

Uniforms follow the classic three-colour split: red for command, gold for operations, blue-green for sciences. Departments that share a colour are told apart by their badge.

| Department | Uniform | Badge | Role aboard |
| --- | --- | --- | --- |
| Command | Red | Silver diamond, gold inlay | Captain, Executive Officer, bridge officers |
| Works (engineering) | Gold | Silver diamond, copper inlay | Keeps every machine running. The player's department. |
| Watch (security) | Gold | Shield | Safety, patrols, docking, keeping the peace |
| Survey (science) | Blue-green | Circle | Sensors, labs, samples, charting |
| Infirmary (medical) | Blue-green | Cross | Crew health and rest |

Ranks: Junior Officer, Officer, Department Chief, Executive Officer, Captain. The player starts as a Junior Officer in Works and can rise to Officer and senior technician, but not beyond.


## The ship: six decks

The Wren has 6 decks, numbered TNG-style from the top, with a crew of 75. Its layout is a main attraction: a Works tech gets to know the hidden ship behind the walls that most of the crew never see.

Layout principles:

- **Every deck has its own shape.** The rounded hull is narrow at the top and bottom and widest in the middle: Decks 2 and 3 share the widest outline (Deck 2 is no bigger than Deck 3 below it), Deck 4 is nearly as wide, and Decks 1, 5 and 6 taper away. Each deck is recognisable at a glance.
- **Curved hull.** Walking stays on the tile grid; the outer hull follows true curves, with rounded corners and an elliptical bow.
- **Two layers to every deck.** The public ship is quarters, mess hall, labs and bridge. Behind it runs the service ship: crawlways, pipe galleries, access hatches and machine rooms.
- **Shortcuts for those who know.** Service routes cut across the ship, so learning them makes your rounds faster.
- **Places worth finding.** Quiet corners with a view, a spot where off-duty Works crew hide for tea, and odd things left in storage.

| Deck | Name | Public spaces | Service layer | Size (tiles) | Opens at |
| --- | --- | --- | --- | --- | --- |
| 1 | Bridge | Bridge (sunken command ring, curved viewscreen, rear stations), the Captain's ready room, observation room behind the bridge that serves as the conference room, bridge washroom | Bridge sub-floor relays: relay room, sub-floor crawl, utility closet | 22 × 12 (the smallest) | The lift reaches it from day one, but visits are rare, so each one feels like an occasion; relays at tier 3 |
| 2 | Command & Science | Senior quarters (12 crew bedrooms including the Captain's quarters, plus 3 visitor rooms, among them Envoy Saruth's guest cabin) on a looped senior corridor; Survey lab, sample lab, chart room, observatory, comms room, Watch office | Sensor and comms array, lab gas lines, specimen store, probe bay, cable crawl | 52 × 22 (Deck 3's outline) | Visitable; sensor array at tier 3 |
| 3 | Commons | Large mess hall and galley with a walk-in cold store, large one-floor bow lounge with sweeping curved windows and a bar, infirmary, hydroponics garden, gym, crew store, call-home booths, washrooms, all off a central promenade | Galley machinery, water recycler, garden irrigation | 52 × 22 (widest) | Start; recycler and irrigation at tier 2 |
| 4 | Quarters | Junior wing (8 bunk rooms, 2 washrooms, laundry, common room), officers' corridor (24 single cabins: 16 officers, 6 guest cabins, 2 spare; music room) | Air scrubbers, heating plant, utility and supply closets | 50 × 20 | Start; utility closet tier 1, scrubbers and heating tier 2 |
| 5 | Operations | Works bay, tea corner, main storage, machine shop, cargo hold, Cart bay, shuttle bay | Air plant, fan hall, manifold room, battery room, pipe galleries | 44 × 16 | Works complex at start; machine rooms tier 2; battery room tier 3 |
| 6 | Engineering | Engine room (walkable from day one), engine overlook, engine watch room | Reactor core, engine control, power junctions, the lowest crawlways | 36 × 12 | The lift reaches it from day one; engine control and junctions tier 3; reactor and engine repairs tier 4 |

The daily loop spans three decks: sleep on Deck 4, eat on Deck 3, work from Deck 5. The lift is part of the core from the first playable build.

**The spine.** A vertical core runs through all six decks with the main lift, a maintenance ladder and the main power and air trunks. The trunks and ladder can be seen behind glass beside the lift. Service crawlways branch off it on every deck. Crawlways have low ceilings, so you crouch-walk through them.

**The lift.** The lift car is a walkable room on every deck: 2 × 3 tiles, big enough for a hover cart, with one wide door on each side. You step in, press the deck panel on its back wall, and ride. Every deck is placed so the lift sits at the same spot, so the spine lines up from deck to deck.

**No freight lift.** Supplies leave the Deck 5 cargo hold on hover hand carts and ride the main lift to Deck 3's cold store and wherever else they're needed. The carts charge in Deck 5's Cart bay.

**Build order:** Deck 4, then Deck 5, then Deck 3, then Decks 6, 1 and 2. All six decks now have agreed plans (`plans/deckN-plan.html`). Decks 4, 5 and 3 are built and signed off. Decks 6, 1 and 2 are built as shells, rooms and furniture, without crew or machines (see DEV_NOTES and TEAM.md for their review status).

**Access and mood.** The lift reaches every deck from day one. Utility rooms lock by tier (agreed 2026-10-16): closets at Tier 1, plant rooms at Tier 2, batteries and power junctions at Tier 3. The player starts at Tier 1, a Works junior. Locking by story comes later, with the story work; until then, sealed rooms and hatches show what's behind them with tap text. Each deck has its own lighting mood: warmer and dimmer on Deck 6, cooler on the bridge.


## Crew and rooms

All 75 crew have a rank and a bed, and where you sleep shows where you stand: senior crew in quarters on Deck 2, officers in single cabins and juniors in bunk rooms on Deck 4.

| Rank | Count | Lives in |
| --- | --- | --- |
| Captain | 1 | The Captain's quarters, Deck 2 |
| Executive Officer | 1 | Cabin, Deck 2 |
| Department Chief | 4 (Works, Watch, Survey, Infirmary) | Cabins, Deck 2 |
| Senior Officer | 6 | Cabins, Deck 2 |
| Officer | 16 | Single cabins, Deck 4 (24 built: 16 officers, 6 guest cabins, 2 spare) |
| Junior Officer | 47, the player included | Bunks, Deck 4 (8 rooms × 6 = 48 berths, 1 empty). Bunk rooms 5 × 4 tiles with three bunk beds each (Deck 4 plan Sketch 3, approved 2026-10-15); the space comes from sealed service rooms, no guest cabins given up |

**Deck 2's senior quarters** have twelve crew bedrooms and three visitor rooms for VIPs such as the Envoy. Six of the twelve are the Captain, the XO and the four Chiefs. The other six are the senior officers: Second Officer Anja Kowalczyk, Senior Helm Officer Dev Raman, Comms Chief Lucia Ferreira, Ship's Counsellor Matthias Oduya, Senior Watch Officer Kofi Mensah and Deputy Survey Chief Hana Mori.

**Guest cabins on Deck 4.** With six officers moved up to Deck 2, six of the officers' corridor's 24 cabins are guest cabins and two stay spare. Guests come and go: visiting specialists, passengers being carried somewhere, crew from other ships in transit, and people who arrive with events (a scientist for the nebula, a delegation's staff, survivors from a salvage job). The corridor always has a few new faces and new things to talk about, which feeds the social system and gossip. Guests aren't part of the 75 crew.

**Deck 4, the Quarters deck.** The junior wing sits aft of the lift: 6-berth bunk rooms, two shared washrooms, a laundry and a junior common room with stern windows. The officers' corridor runs forward of the lift toward the bow: single cabins with each officer's name and rank on the door plate, carpet, warm lamps and quiet after 23:00, ending in the music room at the bow, a soundproofed room with a door, so the corridor stays quiet. It has a stage round the bow windows with drums, guitars, amps and a mic, a grand piano, beanbags, a record cabinet and a rail of instruments to borrow; the Captain plays the piano late on Thursdays. Twelve cabins have hull windows; twelve are inner cabins. Sixteen hold officers, six are guest cabins and two are spare.

**The night-shift room.** One junior bunk room houses the night shift, so it is dark and hushed at midday.

**Promotion means moving across the deck.** The player starts in a junior bunk room (Bunk 1, with Tomas; Pell and Rina are next door in Bunk 2). Promotion to Officer earns a cabin in the officers' corridor, and walking it for the first time with your own key is the moment of promotion.

### The crew: 75 people

- **About 10 story crew,** fully written, each with a story arc that opens up as the player gets closer to them:
  - Captain Odile Marrow
  - Commander Teo Vance, the Executive Officer
  - Dr. Imra Sato, Head of Survey
  - Chief Bram Holt, Head of Watch, who does not trust the Veyli and says so
  - Tomas Lind
  - Pell Okafor
  - Chef Auda Brennan, who runs the galley and mess hall
  - Rina Deshi, who works in the infirmary
  - Envoy Saruth (Veyli), who has the guest cabin on Deck 2
  - Chief Ines Calder, Head of Works: your boss and the one who certifies you. She lives on Deck 2 and works from the glass office on Deck 5.
  - Dr. Priya Nandakumar, Head of Infirmary.
- **About 65 generated crew,** with names, looks, jobs and personalities. Each comes from a template: role, home deck, shift, habits, a couple of personality traits, and a few life details for gossip.

Pell works on Deck 5 for now. When shifts move crew between decks, Pell will sleep in Bunk 2 and work on Deck 5.


## Deck 5: the working deck

Deck 5 is the ship's garage, not its home, and it was built first after Deck 4 so the Works bay can anchor the shared job list. Where Deck 4 is homey, Deck 5 is a workshop: steel plate and grating floors, gold-and-charcoal hazard striping at doorways and machines, pipe runs along the walls, bright cool work lights and very few windows. The plan is in `plans/deck5-plan.html`.

**Shape.** About 44 × 16 tiles, narrower than Decks 3 and 4. The lift lines up with Deck 4's, a little aft of midships, splitting the deck into a cargo end aft and a working end forward.

| Area | What's there | Opens at |
| --- | --- | --- |
| Shuttle bay (stern) | One small shuttle, the Tern, on its pad; the flat stern hull is the bay doors; a control booth with glass over the pad. Where you first arrive. | Start (bay floor) |
| Bay door gear | Giant gears and rams in the stern corner; the doors slide into a pocket here. Glass panel onto the pad. | Sealed, visible through glass |
| Cargo hold | Crates off the shuttles plus the big spares. Where supplies enter the ship; they leave on hover hand carts up the main lift. Its cargo hatch to the shuttle bay is open to Works crew and the player. | Open: supplies move by cart since Pillar 2 |
| Cart bay | Hover hand carts, docked and charging between runs. | Opens once supplies start moving |
| Haulway and lift lobby | The walkable route from the shuttle pad to the lift, opening straight into the Works bay. | Start |
| Works bay | Big job board (the shared job list's home), the Ship health board, workbenches, tool wall, kit lockers, a window onto the shuttle pad, and the Works Chief's glass office overlooking the floor. | Start |
| Tea corner | Behind the parts racks, where off-duty Works crew hide. One warm lamp. | Start |
| Main storage | Aisles of shelving sorted by system (lights, filters, plumbing, galley parts) and a check-out counter. A dusty back corner of things nobody remembers ordering. You carry two items, so aisle layout shapes routes. | Start |
| Machine shop | Lathe, parts fabricator, welding bench. When storage runs out of a part, make one: slower than fetching. | Tier 1 |
| Battery room | Rows of cells with glowing charge bars. | Tier 3 |
| Air plant (bow) | Oxygen cells in glass columns, scrubber stacks. | Tier 2 |
| Fan hall (bow) | The ship's lungs: one huge slow fan, ducted under the main corridor to the spine trunk. Visible through a window at the corridor's end from day one. | Tier 2 |
| Manifold room (bow) | A wall of colour-coded pipes and valves serving every deck; where tier 2 fault tracing starts. | Tier 2 |
| Pipe galleries | Narrow crawls along both hull sides, storage to the air plant and machine shop to the manifold. Later shortcuts, and part of tracing connected faults. | Tier 2 |

The first build of Deck 5 (step 6c) made the lift lobby, haulway, corridor, Works bay, tea corner, washroom, storage, machine shop and the shuttle bay floor, plus the glass onto the pad and into the fan hall. Everything else is sealed with tap text, as on Deck 4.


## Deck 3: the Commons

Everyone comes here to eat. A wide promenade runs stern to bow down the middle of the ship, with the lift standing in a plaza halfway along: the hydroponics garden at the stern end, the bow lounge at the bow end, and every room opening off it. 52 × 22 tiles, the widest outline (Deck 2 shares it). The plan is in `plans/deck3-plan.html`.

- **Mess hall and galley** along the port side. The mess hall is the biggest room on the ship: long tables and round ones, a drinks station, a tray return, a menu board (see "Food and cooking") and hull windows. The serving counter opens through to Chef Brennan's galley, with a grab-and-go shelf for anyone running late. A walk-in cold store sits behind the galley, stocked by hover cart.
- **The bow lounge** fills the whole bow on one floor, with curved windows sweeping from side to side and a curved bar stocked from the galley behind it. It's zoned so it never feels like one empty hall: a lively bar end and a quiet window end.
- **The infirmary** is just aft of the lift, with a ward, an exam room and Rina on duty.
- **The hydroponics garden** fills the stern: grow racks, raised beds, fruit trees, a pond with benches and a herb wall for the galley. Glass doors at the end of the promenade let you see green as soon as you step out of the lift.
- **Along the starboard side:** a gym (with a treadmill, added 2026-10-15; no extra kit or booked slots for now, more later), a small crew store, and call-home booths for recorded messages home.
- **Washrooms** off the plaza.
- **Service layer:** the galley plant, the water recycler (when it struggles, the showers on Deck 4 run weak) and the garden's irrigation room, all sealed.


## Deck 6: Engineering

The bottom of the ship: short, narrow and warm, with a hum you feel through your boots. 36 × 12 tiles, with a blunt bow and a flat stern for the drive. The plan is in `plans/deck6-plan.html`.

- **The engine room** fills the flat stern: three drive coils in a row, each taller than a person and glowing as they cycle, and the drive housing across the stern. You can walk it from day one; big repairs here are tier 4 team jobs, often timed with the bridge.
- **The engine overlook** is a gallery with a rail along its window onto the coils, with a door straight onto the coil floor. New crew always come down in their first week.
- **The engine watch room** sits at the end of the overlook with its own window onto the coils: two armchairs, a tea table, a kettle, a stack of old engine logs and a heater nobody needs.
- **Engine control** runs the reactor and the drive, with glass onto the lobby and the reactor. Tier 3.
- **The reactor** fills the bow in its shielded drum. Its shielded door opens off the lift lobby. Tier 4.
- **Service layer:** two power junctions by the spine, where the reactor's output splits for every deck above (tier 3; some jobs need a shutdown, so you pick a quiet hour and warn whoever loses power), and the lowest crawlways along both hulls from the engine room to the reactor (tier 3).
- No windows to space anywhere. The spine ends here.


## Deck 1: the Bridge

The smallest deck, at the very top of the hull. 22 × 12 tiles. Step out of the lift and the bridge doors are right ahead, with the observation room behind you, looking aft over the whole ship. The plan is in `plans/deck1-plan.html`.

- **The bridge** fills the bow. A curved viewscreen covers the bow wall. Facing it is the command ring: the Captain's chair with a seat either side, the helm and ops consoles in front, and a curved wooden rail behind. The ring is a sunken ring in the design; for now the build fakes the step with the rail, a painted step edge and a curved step strip, and a real sunken floor can come later. The rear stations (Watch, Survey, Comms and Works) stand along the aft walls. The bridge has its own dark carpet with the command ring inlaid, and a Ship health board. The bridge watch hands over at the command ring at 06:00 and 18:00.
- **The Captain's ready room** is aft of the bridge on the port side, opening from the bridge: a desk, a bookshelf, a port window and an aquarium with one slow fish called the Admiral.
- **The bridge washroom** mirrors it to starboard, so the watch doesn't have to ride the lift down.
- **The observation room**, on the far side of the lift, is also the conference room: a long table for ten, a wall screen and windows round the stern and both sides. Briefings happen here, and the Captain takes an evening walk through it. Visiting the ready room and the officers' quarters, and sitting in meetings, come with progression (planned for Pillar 3).
- **Service layer:** the relay room and a sub-floor crawl under the rear stations (tier 3, a shortcut up beside the Works station), and a utility closet. The ladder and trunks end here.


## Deck 2: Command & Science

52 × 22 tiles, on Deck 3's outline. The deck splits at the lift: the lift's stern door opens to the senior quarters and its bow door to science. The plan is in `plans/deck2-plan.html`.

- **The senior quarters**, aft of the lift: one carpeted corridor in a loop, with fifteen bedrooms opening off it, each with its own door; every officer's door plate shows their name and rank. Twelve are for the senior crew and three for visitors.
  - **The Captain's quarters** fill the stern, with windows all along it: the biggest bedroom aboard, with a dining table where the Captain hosts the senior crew and the Envoy, a study and a sleeping alcove.
  - **Hull cabins with windows** for Commander Vance, the Works Chief, the Infirmary Chief, Dr. Sato, Chief Holt (next door to the Envoy), the visitors' suite and three of the senior officers.
  - **Envoy Saruth's guest cabin**, on a stern corner: a low table for Veyli tea rituals, cushions instead of chairs, and a knot of cord on the door handle meaning visitors by invitation.
  - **Inner cabins** inside the loop for the other three senior officers and a second visitors' cabin. It stays a cabin rather than a lounge, because ship-wide events bring visitors (agreed 2026-10-16).
- **Science**, forward of the lift along a wide science corridor: the Watch office (glass onto the lobby, so the Watch sees who rides the lift), the chart room, the Survey lab, the sample lab, the comms room (where every recorded call home goes out), an observatory with bow windows (where off-duty crew gather for observatory night, one evening a week), the specimen store and the probe bay.
- **Service layer:** the sensor and comms array, a sealed machine room in the nose seen through glass at the end of the science corridor (tier 3); the lab gas plant (tier 2); a cable crawl along the starboard hull (tier 3); a utility closet.


## The clockwork: systems, supplies and the job list

Every machine aboard has a condition that wears down with use and time, and wear turns into work on one shared job list that the whole crew draws from.

### The ship's systems

- **Systems:** air, water, power, heat, food, waste and laundry, hull, comms and sensors, propulsion, and transport (the lift and doors, added 2026-10-15).
- **Condition:** each system has a score from 0 to 100 that wears down with use and time. Each is made of parts that can fail, such as filters, pumps, relays and seals.
- **Dependencies:**
  - Power feeds everything.
  - Water feeds the garden, and the garden feeds the galley. **The garden really grows food** (the user, 2026-10-16: "everything simulated, as far as we can"): gardeners on a rota tend the beds and racks, crops grow over ship days, harvests go into the cold store, and crew carry the produce to the galley, where the menus use it. A poor garden (low water, dim lights, no gardeners) means smaller harvests and the galley falls back on stores.
  - Air needs scrubbers, and scrubbers need filters from the Deck 5 hold.
- **Ship health** is a blend of all the systems. A Ship health board on the bridge (Deck 1) and in the Works bay (Deck 5) lists each system and its condition.

### Machines

Each machine is a real object in a room, with a condition from 100% to 0%, a wear rate and the effect it has on the ship when it falters. Wear depends on use: the galley oven wears fastest around mealtimes, the laundry washers on the morning after a busy shift, the lift whenever people ride it.

Wear is measured against an average day, so the ship's machines last the same whatever the crew's routines; busy days wear them faster and quiet days slower. Condition bands: healthy 75–100, worn 50–75, faulty 25–50, failing 10–25, broken under 10. A fresh ship starts every machine at 70–100. Ship health measures how well things work, so a well-kept ship reads close to 100 (agreed 2026-10-15).

A machine's life runs through five states:

1. **Healthy.** Works normally.
2. **Worn.** Still works, but a sharp-eyed tech can spot it. Servicing now is cheap and quick.
3. **Faulty.** A fault is logged on the job list. The machine works badly: slower, noisier, less effective.
4. **Failing.** Effects spread to the crew and the ship. The job is marked urgent.
5. **Broken.** The machine stops. Repairs take longer and need more parts.

**Faults you can see** (agreed 2026-10-16). One shared system draws a machine's condition on every deck: worn machines dim their screens, failing ones blink red or glow warm red, pipes drip, lights flicker, showers spray weakly and plants wilt. Each deck only adds touches of its own where it needs them.

**Tapping a machine** gives a line about it and its condition. Where the machine has a use (a washer, an oven, a lift call panel, the lights, a fan), tapping it also starts it: it runs, the use counts toward its wear, and its system responds. Faulty machines slow the crew who use them, never the player.

### Food and cooking

Food is simulated from store to plate (agreed 2026-10-15):

- **The galley really cooks.** Chef Brennan (and her galley hands, when on shift) wakes early and starts cooking before breakfast opens, so food is ready when the window starts; the same before dinner. You can see her at the ranges, ovens and prep island, even when she works alone.
- **Food flows:** stores from the Deck 5 hold, by hover cart and lift, to the cold store; from the cold store to the galley; cooked in batches; served at the servery; dishes back to the dish pit. The grab-and-go shelf is stocked from the same cooking, and its food isn't binned overnight. Food you push up yourself lands in the cold store when you unload the cart.
- **What runs out shows:** a late batch makes a queue, an empty shelf stays empty until restocked, low stores turn into restock jobs.
- **The galley's day:** Chef Brennan rises about 04:30 and cooks from 04:50 for breakfast at 06:00, and from 14:30 for dinner at 17:00; her deputy cooks on her days off. Early hands (05:30–13:30) bake for the grab shelf, serve, wash up and prep; late hands (13:00–21:15) prep, cook, serve and clean down. The staff eat at 08:00 and 16:30. The cooks cook to the numbers expected, but queues still form now and then: a busy serving window, the odd slow oven, a rush after shift change. A long queue means something has gone wrong, such as an empty cold store. The cold store holds under two days' food (built in 0.29.0).
- **Menus** (agreed 2026-10-16): a weekly menu cycle with a crew member's favourite on Wednesdays, a Friday treat with a pudding and a Sunday dinner the crew voted for. The menu board in the mess shows the day's meals. On a crew member's birthday (and on Founding Day) the galley bakes a cake for after dinner, and a harvest morning in the garden puts fresh salad on that evening's menu (see "Ship traditions").
- **Machines matter here too:** the ovens and ranges wear with use (see "Machines"). Cold-store meals spoil when the chiller falters, faster the worse its condition; spoiled food is binned and noted in Mail.
- **The player doesn't help in the galley** (agreed 2026-10-16), but can take the food cart run (see "The job list").

### Supplies

Supplies come aboard by shuttle into the Deck 5 cargo hold and are shelved in main storage: filters, spare parts, tools, linen and food stores. Food goes up to Deck 3's cold store on hover hand carts via the main lift. Repairs use parts and cooking uses food. Low stock adds restock work. An empty shelf blocks a repair until supplies arrive, unless you make the part in the machine shop, which is slower. Shortages come from the numbers (a late delivery, heavy use), not from a story beat, and the game tells you about them in the Mail tab on your device.

### The job list

One list for the whole ship, shown on the big job board in the Works bay and on your personal device. The ship adds jobs itself: faults, routine servicing, restocking, cleaning, cooking.

1. Wear generates jobs, which go onto the Works bay job board.
2. Crew on duty with the right department and skills claim them.
3. They fetch parts, using hover carts from the Deck 5 hold for supplies, walk to the fault and fix it.
4. The player gets the skilled or interesting jobs for their rank. Routine jobs get done by the crew if the player leaves them, but more slowly. Jobs nobody claims pile up and get worse.

**Enough work, not overwhelming** (agreed 2026-10-16). About 3 to 6 jobs a day are left for the player on day shift. The Works crew take urgent and big jobs straight away; small Tier 1 jobs left for the player are held until the end of your shift that day (at least 3 hours, so one found late carries into the next morning), at most 6 held at once (extras go to the crew as usual), and on day 1 a couple of chores are ready at 08:00 (changed 2026-10-16: at the real clock, 3 ship hours was only about 5 real minutes, so the crew swept the board before you got there). On your days off nothing is held for you; the crew take them, and the board stays open. The food cart run is a player job too: take it from the job board, and it waits an hour for you before the crew take it.

### Consequences

Consequences come in stages, and you can see them:

| Stage | Examples |
| --- | --- |
| Minor | A flickering lamp, a dripping pipe, a filter-due light |
| Noticeable | Weak showers on Deck 4, a warm stuffy deck, dim garden lights, an empty grab-and-go shelf |
| Serious | Alarms, a room sealed off, crew rerouting, crew mood dropping |

**Recovery is visible too.** Lights steady, plants perk up and the mess fills again.

Machines affect crew needs and mood, often on another deck:

| Machine | When it falters |
| --- | --- |
| Air scrubber | Air gets stuffy, energy and mood drop on that deck |
| Water recycler (Deck 3) | Showers run weak on Deck 4, hygiene and mood drop |
| Laundry washers | Crew go about in grubby uniforms, mood drops |
| Heating | Cold cabins, grumbling crew |
| Galley oven | Meals run late, hunger rises, Chef Brennan gets stressed |
| Lights | Rooms dim, people move slower and grumble |
| Doors and lift | Routes get longer, people run late for shifts |

Uniforms are objects that get grubby. You drop yours at the laundry and take a clean one from your locker.


## Crew simulation

Every crew member is a simulated agent with a job, a shift, a bed, needs and opinions of the others, and their day is decided by the same rules as yours.

**Shifts.** Two shifts: a busy day shift and a much quieter night shift. Most of the crew work days, so the ship has a real daily rhythm. Nights are dim and calm, with a skeleton crew keeping watch.

| Shift | Share of crew | On duty | Off duty | Asleep |
| --- | --- | --- | --- | --- |
| Day | About 80% | 08:00–17:00 | 17:00–23:00 | 23:00–07:00 |
| Night | About 20% | 21:00–06:00 | 14:00–21:00 | 06:00–14:00 |

During the night, only urgent jobs and essential systems get attention. Routine work waits for morning, which is when the job list is busiest.

**A day moves through three decks.** Crew wake on Deck 4, eat on Deck 3 and work wherever their department is, so the lift and the lobbies have rush hours.

**Meals.** Two meals a day, breakfast and dinner, each served over a window rather than at a set time. Breakfast runs 06:00 to 08:00, catching the night shift coming off at 06:00 and the day shift before 08:00. Dinner runs 17:00 to 20:30, catching the day shift coming off at 17:00 and the night shift before 21:00. The galley also keeps a grab-and-go shelf for anyone running late.

On duty, crew claim jobs from the job list that match their department and skill, walk there and do the work. A Works tech fixes the scrubber; Chef Brennan cooks; Infirmary checks on whoever is run-down.

Off duty, each person picks what to do by scoring their options against their needs and traits: eat, sleep, wash, socialise, relax in a favourite spot, a hobby.

**Needs.** Hunger, energy, social, hygiene and fitness, from 0 to 100. Fitness (agreed 2026-10-15) drops slowly and is restored at the gym. High needs give a small bonus and low ones a penalty (the table is under "The player"). Showers restore hygiene, which gives the washrooms a morning rush. Mood comes from needs, the state of the ship and the people around them: when ship health is poor, crew mood dips and they say so ("grumbling about the showers").

**Skill.** Each crew member has a skill level in their department. Skilled crew work faster and cause fewer follow-up faults.

### Every room in use

Crew use every room and every function in their daily life, not just beds, seats and workstations (agreed 2026-10-15):

- **Free time draws on the whole ship:** the gym (treadmill, weights), the call-home booths, shopping at the crew store, the garden, the lounge and bar, the music room, the observatory, the laundry, the common room.
- **Each activity looks like itself:** running on the treadmill, talking in a booth, browsing the store's shelves and paying at the counter, playing an instrument, watering the beds. Crew carry what they need: trays in the mess, toolboxes for Works crew on jobs, datapads for officers.
- **Needs and habits pick the activity** (see Needs below), so the gym is busy after shift and the booths on rest days.
- **A room with no use is a gap to fill,** in the simulation or in the furniture.
- **Small things too:** crew also use the toilets and basins, take tea breaks, shop at the crew store (browse, then pay at the till), wait by the lift, and stand in at stations their department doesn't fill every day. Needs (hunger, energy, hygiene, fitness, social) are worked out from each person's day, and steer the gym, calls home and resting (built in 0.26.1).
- **The crew store is staffed:** two juniors are the ship's storekeepers, on staggered day shifts, so there's someone at the till through the day and evening (agreed 2026-10-15). It isn't open every day: there's no third storekeeper or honour box (agreed 2026-10-16).

### Routines with variety

No crew member does exactly the same thing at the same time every day. Variety comes in layers:

1. **Rota.** A 7-day ship week with staggered days off, so a different crowd is at breakfast each day. Everyone has two days off a week, but on different schedules: a good number are off at the weekend, but not all, and the night shift keeps its own pattern (the user, 2026-10-17). Some crew move between day and night shifts every few weeks.
2. **The shape of each day.** Each day of the week runs a little differently. For example: drills one day, maintenance inspections another, and on the rest day a late breakfast, a busy gym and a film in the lounge.
3. **Time jitter.** Small daily offsets for everyone, such as waking 5–25 ship minutes early or late, or lingering at dinner. The offsets come from a seed per person per day, so they look random but replay the same way. That keeps saves and tests reliable.
4. **Habits.** Personal quirks: an early riser, someone who always takes a window seat (seats by windows are marked on every deck), someone who skips breakfast, someone who calls home on rest days. Habits change slowly over time, a few a month: a junior takes up running, someone stops going to the bar. The ship keeps a log of the changes.
5. **Needs drive choices.** Hunger, tiredness and wanting company make crew choose between a few options instead of following a script.
6. **Interruptions.** Faults and events pull crew off their routine. This is how the ship simulation reaches daily life.

*Example:* on Monday Pell has breakfast at 07:40, then goes to the Works bay. On Thursday it's breakfast at 07:10, then drills. On a rest day Pell sleeps in, goes to the gym, then the garden, and gets called away to a scrubber fault one evening.

### Crew on other decks and performance

Only one deck is loaded at a time. Crew elsewhere are simulated "on paper": they move through their schedules as data and are drawn only when the player is on their deck. Arriving on a deck shows everyone where their schedule puts them. Only crew on the deck you are viewing walk tile by tile, so the full crew of 75 stays cheap on a phone. A busy deck shows about 15–25 people at once.

All 75 crew (about 60 on days, 15 on nights) are in the simulation: about 10 hand-written story characters and about 65 generated ones (see "The crew: 75 people").


## Social life

**Relationships with the player.** Every crew member has a relationship meter with five tiers, reached by points: stranger (0), acquaintance (10), colleague (30), friend (60), close friend (100). It doesn't decay, or decays very slowly after weeks apart, to keep the game cozy.

Ways it grows (agreed 2026-10-16; starting numbers, tuned in play):

1. A favour done: +8.
2. Working a job together: +6.
3. Eating at the same table, keeping an appointment, or a birthday wish on the day: +3.
4. Chatting: +2, once per person per day, so it can't be farmed.
5. Being the first to tell you a piece of news: +1.

What higher tiers unlock:

- They greet you.
- They share news about their life (family back home, a hobby) and about the ship.
- They show on your device's Maps.
- At social time, they come and find you, and they invite you to things.
- Friends cover a job, tip you off about spare parts, and put in a good word with the Works Chief toward promotion (it shows in your Record).

**Chats, not dialogue trees** (agreed 2026-10-16). Tapping someone opens a short chat card: their face, name, rank and tier, and one line from them. The line is whatever matters most: news they know, then how they feel, then something about the ship near them, then a life detail (for acquaintances and up), then a greeting. The card has three or four buttons: **Chat** (social for both of you, once a day), **Ask about…** (news, their work, home; each answer fills in what you know about them), **Help?** (a favour, if they have one) and **Meet up** (an appointment). Lines are templates filled in from the simulation, with about ten variations per kind and tier. Chatting while grubby gives half the social.

**Favours and crew seeking you out.** Favours grow from crew lives and the ship: "My cabin lamp flickers", "Could you bring a tray up to Tomas, he's ill". Each is a personal job in your Jobs app, done the same way as every other job. Friends on your deck come and find you in their free time; a chat is offered as a small prompt at the screen's edge, never a pop-up you must answer.

**Reputation.** Crew remember who keeps their corner of the ship running. Good work raises friendship and trust.

**Gossip is a hint system.** Crew news comes partly from the ship simulation: "The scrubbers on 4 have been rattling all week." "Brennan's furious, the cold store's warm again." The social system quietly tells the player what the ship needs. News is built from sentence templates filled in with what's actually happening; no AI writing is needed.

**How news spreads** (agreed 2026-10-16). One news model serves everyday gossip and ship-wide events alike. A piece of news starts with the few people who'd know first, and spreads hour by hour to the people they spend time with: meals, the same work room, the same bunk room. Friends pass it on more readily than strangers. Crew who know something talk about it. You hear it as **chatter**, a line overheard as a small speech bubble when you walk past (one or two on screen at most), or in their tap line and chats. Everything you hear goes into the Ship app's news feed, with who told you and when. Nothing is locked behind knowing it.

**Crew relationships with each other** (agreed 2026-10-16). Each pair of crew has an affinity, starting from what they share (department, bunk room, habits) with a little seeded variety. It drifts once a ship hour from the time they spend together: most pairs slowly grow friendly, and a few with clashing traits drift the other way. It shapes who sits together in the mess and lounge, who swaps shifts and who avoids whom, and what they say about each other. Friends of your friends warm to you a little faster. When a pair becomes friends or rivals, it turns into news ("Pell and Rina aren't speaking"), and sometimes a small incident: an argument in a corridor you can smooth over, a reconciliation over dinner.

**Crew feelings on tap.** Tapping a crew member shows their role, how they feel ("Tomas looks tired"), any event they're part of, and a line of chat. Mood blends their needs, ship health, how a current event is going, recent time with friends, and birthdays and traditions; it shows in their lines, their walk and who goes to the lounge.

**The first story arcs** (agreed 2026-10-16) belong to the three crew closest to you: Tomas, Pell and Rina. Each has four beats that open at acquaintance, colleague, friend and close friend: a small personal thread told through chats, an appointment or two, Mail and one small gathering. Arcs for the Captain, Vance, Calder, Brennan, Holt and Saruth come later.

**Guests** (agreed 2026-10-16). Guests live like crew, but for a while: they eat, sleep, use rooms, turn up in chatter and can be befriended. Between events, an everyday guest (a specialist for a week, a transfer waiting for their ship) arrives about once a ship week, so Deck 4's corridor always has a new face. Events bring their own guests; a delegation leader or dignitary gets one of Deck 2's visitor rooms.

**Ship traditions** (agreed 2026-10-16; "ship traditions" is the official name, while the big ones are "ship-wide events"; built in 0.34.0). Alongside the big ship-wide events, the Wren has small, recurring traditions, "lots of little holiday-like things, almost like Stardew Valley". The crew who are free simply go, and talk about them; nothing stops daily life, and there are no menus or cutscenes. One events system runs them. They're announced in Mail the evening before, shown on the device's Calendar, and the Calendar reminds you before each one:

- **Weekly:** running club (Monday evening, the gym), quiz night (Thursday, the bow lounge), Works Friday tea and tool cleaning (Deck 5) and the Friday music jam (Deck 4), film night and observatory night (Saturday: the junior common room, and Deck 2's observatory), and the Sunday swap meet on the promenade.
- **Every few weeks:** harvest morning in the garden (every other Saturday, fresh salad at dinner) and the hull-lights evening (every four weeks).
- **Birthdays.** Every crew member has a birthday on a ship day of the year (1 to 364: 52 weeks of 7 days, day 1 being the game's Day 1), spread so about one falls each week. The galley bakes a cake and the mess gathers after dinner (20:15): their department, their bunkmates and plenty of others.
- **Once a year:** Founding Day (day 100: cake and a few words from the Captain) and the quiet watch (day 300: a quiet while at the windows for the people they miss). The bigger Founders' Day festival on the plaza is a short ship-wide event (see "Ship-wide events").
- **Hearing about them:** besides Mail and the Calendar, crew mention them when you talk to them ("Coming to the quiz tonight?").
- **Joining in:** be in the room while it's on. It gives a little social, and the organiser thanks you.
- More to come, in the same system.

Daily routines belong to the crew's ordinary day instead: the bridge watch hands over at the command ring at 06:00 and 18:00, and the Captain takes an evening walk through the observation room.

**Romance** is out for the player (the user, 2026-10-16). A few established crew couples live in the background, never involving you (the user, 2026-10-17).


## The player: Works technician

You work the day shift as a Works maintenance tech, with **two days off a week** like a Works junior (the user's choice, 2026-10-16): Saturday and Sunday, no shift and no jobs expected, though the board stays open if you want work. On shift you take jobs from the same list as the rest of the crew and do them with your own hands.

**Arriving by shuttle.** The game opens with your shuttle landing in the Deck 5 shuttle bay. You step off onto the pad, walk the haulway to the lift lobby, glimpse the Works bay that will be your workplace, and find your own way up to your bunk on Deck 4. The shuttle Tern is already in the bay with its ramp down, ready for it. Until the arrival is built, the game starts with you waking in Bunk 1.

**The arrival and first week (the user, 2026-10-16; built in Pillar 4).** You land on a **Sunday evening**, so Monday is your first shift. Waiting at the ramp is your **escort: a Works crew member one rank above you who becomes a future friend (the user, 2026-10-17): Zeke Torres**, a Works engine officer (Pell, the junior in Bunk 2, joins you at dinner; see plans/pillar4-plan.md), who walks you (you stay in control, following them) through the haulway, past the Works bay, up to your bunk, where they hand you your device, then to **dinner in the mess**, where **Chief Calder** stops by the table to welcome you. Your first full day is a **shadow shift**: your escort trains you on one real job end to end, and your **first solo job comes soon after, before Wednesday** (the user, 2026-10-17: rotas are aligned to make that work). Your character gets a **name you type on the shuttle** that the crew use (no choice of look for now). Your first weekend: **Sowing morning**, planting your own seedling, and **film night with Tomas**. Then you're let loose a little at a time over the first week, each new thing taught by someone aboard (an optional "Settling in" list on the device tracks it); your first weekend brings an invitation to a tradition. A skip-intro option is offered on later new games.

**The job loop.** Every job follows the same physical steps:

1. **Notice and take.** A fault shows on the Works bay job board, someone flags you down, or you spot a worn machine on your rounds. You always take jobs at the board (agreed 2026-10-16). The device's Jobs app only tracks them: the tracked job sets the on-screen arrow and the map pins, step by step (board, storage, machine shop, machine, back to the board). The pointer is a marker over the place when it's on screen, an arrow at the screen edge when it isn't, and "Take the lift to Deck N" when it's on another deck; Maps uses the same pointer.
2. **Diagnose.** Open the panel and inspect it. You see which component is failing and what the fix needs.
3. **Fetch.** Get the part or tool from main storage or the Works bay, or make it in the machine shop. You can carry two items at a time.
4. **Repair.** Hold to work. Repairs take longer on broken machines and go faster as your skill grows.
5. **Turn in.** The machine recovers and the people it affected notice, but the job only completes when you turn it in back at the board, which is when it counts toward credit, your Record and commendations (agreed 2026-10-16). Favours are the exception: you accept them in person in a chat and hand them back to that person.

What makes it interesting:

- **Priorities.** Several jobs compete. The urgent scrubber, the oven Chef Brennan keeps asking about, or the routine service that prevents next week's breakdown?
- **Prevention.** Spotting wear early is cheap and quick. Waiting for faults costs more time, parts and goodwill.
- **Routes.** Walking matters, and the job spans decks: parts are on Deck 5, the scrubbers on Deck 4, the oven on Deck 3. Fetching the right parts in one trip saves real time on your shift.
- **Interruptions.** The ship keeps living around you. People stop you for help or argue in corridors.
- **Reputation.** Crew remember who keeps their corner of the ship running. Good work raises friendship and trust.

**No hard failure.** If you slack, other Works crew pick up jobs, but more slowly, and your supervisor notices. The ship never dies because of you, but it gets visibly worse.

**Your needs and activities** (agreed 2026-10-15). You have the same needs as the crew, including fitness and social, and the same rooms to meet them: eat in the mess or grab from the shelf, shower, sleep in your bunk, work out at the gym (a treadmill and weights), call home from a booth, shop at the crew store. Needs drain with ship time and come back by doing things: a meal +55, the grab shelf +25, a shower +80, a workout +30, a call home +40, and 8 hours' sleep fills energy. Social rises when you talk to crew and when you eat at a table with others. A rested player can stay up 16 to 18 ship hours before energy runs low (about 17 at average fitness).

**Bathroom** (the user, 2026-10-16): a need like the others, filled by using a toilet in any washroom (yours on Deck 4, the public ones elsewhere). Crew already use them.

**You can see it working** (the user, 2026-10-16): anything that fills a need shows it as it happens (the need's mark rising, a small "+25 Food" style note), and anything that takes time (eating, showering, the toilet, a workout, a call home, a job step) shows a progress bar for how long is left, like the workout already does.

**Needs give bonuses as well as penalties** (agreed 2026-10-16). A need at 75 or over gives a bonus, one under 25 a penalty, and anything in between does nothing. Effects multiply when they stack, so low fitness and low energy together make you walk at 64%. Your device shows a small up or down mark beside a need that's giving a bonus or a penalty, with a one-line reason. Needs never punish you harder than this (no fail state). The starting numbers (tuned in play; the build's exact values are in DEV_NOTES):

| Need | High (75 and over) | Low (under 25) |
| --- | --- | --- |
| Energy | Tasks 15% faster (repairs, making parts, activities) | Walk at 80% |
| Fitness | Energy drains a little slower; walk at 105% | Walk at 80%; energy drains a little faster |
| Hunger (well fed) | Energy drains a little slower | Tasks 15% slower |
| Hygiene | Chatting gives 50% more social | Chatting gives half the social; crew may remark on it |
| Social | Tasks 10% faster (a good mood) | Energy drains a little faster |

**Anything the crew can use, you can use** (agreed 2026-10-16). Anything the crew use to meet a need or pass the time, you can use too, with the same pose: the gym, the bar, lounges and common rooms, reading seats, benches, the garden, the music room, the laundry, basins, the kettle, the observatories. Tap the thing to use it. Sit on any free seat or bench: resting slows your energy drain, and sitting near crew who are chatting gives a little social. You can squeeze past crew who are settled (working, seated, or standing at a station) with a polite word; crew on the move still block the way. In crawlways you crouch-walk. The store sells snacks (a little hunger) and small comforts (a little social, kept in your locker), paid from a simple balance of credits on your device.

**Your personal device** is the game's main screen (agreed 2026-10-15; designed 2026-10-16, built in Pillar 3). It's a small handheld computer every crew member carries, holding your day, your messages, your notes and the ship's news. It's the only menu in the game. It opens instantly from the Device button (the user's choice, 2026-10-16: the button only, no pull tab; it must never open by itself), and it never pauses time: the ship keeps running, and you keep walking, while it's open. Until it's built, the game uses a plain placeholder with the need marks, your credits and a simple Mail tab.

- **Two layers.** The apps describe what to show (plain lists, bars, text and buttons); one skin draws it. So the look can change later without touching the apps.
- **The look: an old-school screen.** Opening the device feels like looking at a real old display in a sturdy bezel: interlaced scan lines, a soft phosphor glow on the text, a curved, darkened edge and chunky monospace type. A faint flicker and a slow rolling band are optional, and off when the phone asks for reduced motion. The phosphor colour is the Wren's cyan (chosen by the user, 2026-10-16); amber and green stay as options in Settings. Meetings' dialogue uses the same screen style.
- **You see yourself use it** (agreed 2026-10-16). Opening the device, your character raises a small glowing handheld (tinted in the screen's colour) and looks at it; walking while it's open, they read as they go; closing it, they put it away. On a phone the camera eases gently to keep you in view above the device, and back when it closes.
- **First tips** (agreed 2026-10-16, a first step toward Pillar 4's onboarding). Short pop-ups in the device's style, each shown once and remembered in the save, never pausing time, with a switch to turn them off. They cover the job loop: the first time at the job board, your first job, arriving at the job's machine, finishing the work (turn it in at the board), and the first time you open the device.
- **On a phone** it slides up over about two thirds of the screen, so the ship stays visible. On the TriFold unfolded it docks as a side panel and can stay open while you walk. A home screen shows the time, your next item, any event in one line and the apps with badges. Urgent things (your job's machine broke, an appointment in 10 minutes, the Captain's address) show as a toast; everything else is a quiet badge, and a "Quiet off shift" setting turns work notices into badges after 17:00.
- **The apps:** Schedule (today as a timeline, a week view and where you're expected now), Appointments, Maps, Memos (your own notes, with a "remember this" button on chats, Mail and jobs), Mail (from the ship, crew, departments, the Captain and home), Calendar (a month of ship life ahead; it reminds you of ship traditions about 30 ship minutes before each one, with a morning "today aboard" line, a remind-me toggle per tradition and a setting to turn reminders off; during your shift they're quiet badges unless you marked that tradition), Needs, Jobs (including favours), Crew (your contacts and what you know about them), Ship (ship health, what's happening and the ship news you've heard), Record (your Works progress) and a small Wallet. Music comes later, with sound. There is no Camera, and no photos anywhere.
- **Appointments.** Pick a person or place, a time and a spot. Crew answer from their real schedule: yes, "not then, how about 19:00?", or no. Strangers accept only work matters; friends accept anything. Accepted appointments go into their day and they turn up and wait. Friends invite you and officers summon you the same way. Missing one costs only a remark next time ("Waited for you at the gym yesterday").
- **Maps** draws each deck as a clean plan from its deck data and finds rooms; "Go there" points the goal arrow, and there's only ever one arrow. It shows no people (the user's choice, 2026-10-16: no dots).
- **Roster** (the user's choice, 2026-10-16) is how you track crew: a list of the crew by department, people you know first. Tap a name and it tells you in words where they are now ("Deck 3, the gym", "on duty on the bridge"); someone asleep or washing reads "in their quarters" (privacy). "Go there" points the goal arrow at that room.

**Off shift**, you are free: eat, wash, socialise, explore, sleep, work out, call home, shop. Some crew will ask for small favours, like fixing a lamp in their cabin, which build friendships and earn goodwill. Getting into your bunk from 20:00 skips the night to 06:00.

**Thirty seconds of play.** Your device chirps: scrubber 2 on Deck 4 is at 60%. You head out of the junior wing, passing Rina and Pell arguing in the corridor. You open the scrubber panel; it needs a filter, so it's down the lift to storage on Deck 5. On the way back, Chef Brennan calls: the oven on Deck 3 is acting up again. Now, or after the scrubber? You choose, and the ship reacts.


## Works progression: deeper ship systems

You progress by earning clearance to work on deeper, more connected systems, and each tier changes how the job plays, not just how big the numbers are. Tier 2 is also your first promotion: Officer rank and your own cabin. Rank also decides which parts of a ship-wide event reach you.

| Tier | Title | Rank | Room | Systems you can work on | What's new in the gameplay | Parts of the ship opened |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Junior Technician | Junior Officer | Bunk, junior wing | Galley oven, lights, doors, washroom fixtures, laundry washers, cabin fixtures | One machine, one fault. Learn the loop: diagnose, fetch, repair, service | Works bay, storage, machine shop, utility closets |
| 2 | Technician | Officer (first promotion) | Own cabin, officers' corridor | Air scrubbers, water recycler, heating, air plant, fan | Connected systems. Ducts and pipes run between rooms and decks, so a fault can start upstream. Trace it from the manifold room and junctions | Air plant, fan hall, manifold room, pipe galleries, Deck 4 scrubbers and heating, Deck 3 recycler |
| 3 | Senior Technician | Officer | Own cabin | Power conduits, relays, batteries, sensor array | Planning around the crew. Some repairs need a shutdown. Pick a quiet hour, warn affected crew, and decide which systems get power during a fault | Battery room, power junctions, crawlspaces, bridge sub-floor |
| 4 | Engine Specialist | Officer | Own cabin | Reactor, drive coils, engine controls | Team jobs. Big repairs need several techs. You plan the job, call in crew and coordinate, often timed with the bridge | Deck 6: engine room repairs and the reactor |

How you earn a tier:

- **Experience.** Jobs completed in your current tier, weighted by quality and how early you caught faults.
- **Certification.** When you are ready, the Works Chief sets a supervised qualification job in the next tier. Pass it and your clearance goes up.
- **Trust.** Reliability matters: turning up for shifts, not leaving jobs half-done, keeping your corner of the ship running.

What each tier gives you:

- **Access.** Keycards to new rooms and systems. The ship literally opens up as you grow, and at tier 2 your key opens a cabin of your own.
- **Tools.** A diagnostic scanner, a pipe kit, a conduit tester, a calibration rig. Each one makes new kinds of faults readable.
- **Responsibility.** Night on-call duty, where emergencies can wake you. Later, a junior tech to mentor.
- **Skill.** Repairs get faster and cleaner in tiers you have mastered, so old jobs become quick wins while new ones stay challenging.

Why it stays interesting: each tier adds a new kind of thinking. Tier 1 is fixing things, tier 2 is tracing problems, tier 3 is planning around people, and tier 4 is leading a team.

**Moments of trust** (agreed 2026-10-16, built in Pillar 3). Before the first promotion, progression shows in invitations. Each is earned, and each is an appointment: the locked door opens for that appointment's window only, then locks again.

| Hook | How you get there | What happens |
| --- | --- | --- |
| The Captain's ready room | Summoned after your first commendation, or by Vance once you're friends | Your first time inside: a meeting where the Captain thanks you, asks about the ship from a junior's view, and introduces the Admiral. A line in your Record. Later visits when summoned. |
| The conference table | Calder takes you to an event briefing in the observation room when your Works record is good; by right from Tier 3 | A meeting at the table with the senior crew. You hear the plan before the rest of the crew, and the briefing lands on your device as a memo. |
| Officers' cabins | An invitation from an officer friend on Deck 4, or a senior friend on Deck 2 | Their cabin door opens for the visit. A chat there counts double. |
| The Captain's table | A monthly dinner in the Captain's quarters; the Captain invites one junior who stood out | The galley cooks a special dinner and you sit at the end of the table. A framed menu goes in your locker. |
| Progress talks with the Chief | An appointment in Calder's glass office, any time | She tells you how close certification is. This is how your Record earns her comments. |


## Ship-wide events (main missions)

Story arrives without stopping daily life, like a TNG episode where a phenomenon or entity changes life aboard for a while. Story sits on top of the simulation, so events grow out of a living ship rather than replacing it.

**An event is a layer on top of normal life.** For a few days it changes the ship's systems, the crew's routines and what the decks look like, and it adds its own jobs to the board.

**Events are ambient, and everyone talks about them** (agreed 2026-10-16). An event is never a mission you're given; it's something happening to the whole ship that you live through. News reaches you the way it reaches everyone: crew chatter first, then Mail, the boards (an event banner and event jobs on the job board, a changed menu, strain on the ship health boards), and at big turns the Captain's address. There are no mission markers and no cutscenes, and the camera is never taken away from you. At most, a gentle note on the device 15 minutes before a gathering, with "show on map". You choose how much to get involved: take event jobs, sign up on a volunteer sheet, help crew who ask, or just turn up. Sitting it out is fine; the crew handle it more slowly and you hear all about it.

**Shape** (agreed 2026-10-16), over 2–4 ship days. Every event resolves.

1. **Warning:** hours to a day ahead, a few people notice something and rumours start.
2. **Onset:** the event arrives with a moment; systems, routines and decks change; event jobs appear.
3. **Escalation:** more faults, tighter food, tired crew, perhaps a second moment.
4. **Resolution:** it ends, always: an all-clear, a gathering, a debrief.
5. **Afterglow:** for a day or two crew talk about it, mood lifts or sags, traces appear and commendations are handed out.

**How it goes** (agreed 2026-10-16). Each event has 3 to 5 threads, the things the whole ship is trying to keep right, each measured from what actually happened (for the ion storm: minutes of blackout, food spoiled, how tired the bridge crew got, the call-home backlog). Each thread lands in one of three bands: **smoothly, bumpily or roughly**, and the overall result is the blend. The whole crew's work counts; you count as one good pair of hands. Your own part (jobs done, people helped, moments you turned up to) is counted separately and decides your commendation toward promotion, your relationship gains and whether you're mentioned in the debrief. Results are told as story, never a score: the Captain's all-clear in words, a debrief in Mail, crew talking for days, and small permanent traces in the world, such as the storm crew's signed roster in the tea corner, a scorch mark, a plaque, a gift or a new pet. Rough is never failure: the ship gets shabbier and moodier for a while, then recovers.

**Four kinds of moment** (agreed 2026-10-16). Big beats happen without stopping the simulation:

1. **Felt everywhere:** beats that hit the whole ship at once, like the storm front's jolt and dipping lights or the nebula filling every window. Crew stop, look up and carry on.
2. **The Captain's address:** a banner on every deck with the Captain's portrait and a few lines, readable for about 20 seconds and kept in Mail. Crew on your deck turn toward the nearest speaker. Two or three per event at most.
3. **Gatherings:** announced ahead, at a real place and time (the delegation at the shuttle bay at 10:00, the all-clear party in the bow lounge). Crew who'd come put it in their day. If you're there you see it happen; if not, you hear about it in chatter and Mail.
4. **Meetings with dialogue:** a gathering where people talk to each other and to you: a briefing, a summons, a greeting, a formal dinner. When you're there, a panel in the device's screen style plays their lines one by one, with each speaker's name and face, and the speakers turn to each other with small gestures. Sometimes you get two or three replies to choose from; they nudge a relationship or a thread a little, and there's never a right answer, a pass or a fail. The ship keeps running, the camera stays with you, and you can walk away at any time; the gist then arrives in Mail. It is never a full cutscene.

Whatever you saw or missed, the crew retell it in chatter for a day or two, with the details that really happened.

**Commendations and occasions (the events engineer, build 0.34.11, from the Pillar 3 plan's Part 4):**

- **A commendation** comes when an event ends and you did two or more of its jobs, or one job and a meeting. It's a letter from the Captain, kept on your record.
- **The Captain's ready room:** your first commendation (or a close friendship with Commander Vance) gets you a summons at 11:00 on the next day the Captain is on shift. She thanks you, asks for a junior's view, and introduces the Admiral.
- **The Captain's table:** a dinner in her quarters every four weeks (days 20, 48, ...) at 19:30. You're invited the day before if you were commended in the last four weeks, or have three close friends. The galley cooks an extra batch, and you keep a framed menu if you go.
- **Progress talks** with Chief Calder are appointments you ask for. They take place in her office on any day she's on shift.
- Each is an appointment that opens its door for its window. If you miss one, a short Mail tells you; nothing is lost.

**Pacing:** roughly one main event every 1–2 ship weeks (about 4½–9½ real hours), with small incidents most days. Small incidents include crew moments the simulation can trigger: a friendship scene, an argument that needs smoothing over, a birthday cake in the mess.

**What the player sees depends on rank.** A junior carries filters during the storm. A senior is in the Captain's briefing about it.

**The events, in order** (agreed 2026-10-16: all kept, nothing dropped). Seven main events, with six shorter ones slotted between them. The main events' order is fixed; the short events' exact slots can be tuned. The ion storm comes about a week and a half into a new game. The full breakdown of each event is in `plans/pillar3-plan.md`.

| Order | Event | Kind | In short |
| --- | --- | --- | --- |
| 1 | Ion storm | Main, built first | Touches every system: power flickers and comms go down. Calder's storm briefing in the Works bay, the Captain's address, emergency lighting deck by deck, storm stew, the Captain's all-clear, a rush on the call-home booths and a party in the bow lounge. |
| — | Comet viewing | Short | One gentle evening at the observatory and the bow lounge windows. |
| 2 | Diplomatic visit | Main | A Veyli delegation fills Deck 2's visitor rooms (the second visitors' cabin is kept for this). A greeting in the shuttle bay, formal dinners in the Captain's quarters, a gift exchange. |
| — | Crew rotation day | Short | Five crew leave on a transport and five new faces arrive. |
| 3 | Something in the garden | Main | A creature eats the crops; traps from the machine shop and a volunteer garden watch. It becomes the ship's pet. |
| — | Power surge | Short | A junction on Deck 6 trips and two decks lose power for a while. |
| 4 | Shipboard illness | Main | The infirmary fills and sick crew stay in their bunks, so more jobs are left for you. |
| — | Founders' Day festival | Short | The whole crew together on the plaza: the big-crowd test, built only once the real-phone test says crowds over 70 are fine. |
| 5 | Nebula drift | Main | Every window fills with colour, the sensor array overloads, and strange dreams leave the crew sleepy and chatty. |
| — | The late supply shuttle | Short | Rationing, a bland menu and a busy machine shop, all from the numbers. |
| 6 | Salvage | Main | The Tern flies out to a derelict and the hold fills with odd finds. In later playthroughs it can lead into the garden creature. |
| — | A Veyli vessel needs help | Short | Works sends parts and a Veyli engineer comes aboard as a guest. |
| 7 | The déjà vu day | Main | A time anomaly replays one day, and what you change the second time counts. Seeded routines make it cheap to build. |

**Special missions.** Startable when you're ready, shown as an icon on the job list or ship map. Occasionally an away job by shuttle, like repairing another ship's systems.

**Character arcs.** The named story crew have personal threads that open up as friendships grow.

**The bridge.** Deck 1 is rarely visited, so story events are the natural reason to go: a briefing in the observation room, a repair timed with the bridge.


## Later: other jobs

Other jobs come after the Works game works. Version 1 is Works only.

**Other jobs and transfers.** Other departments come later as transfers, all drawing from the same job list, so each one is mostly new jobs and tools rather than new systems. Each would need its own progression ladder, like Works has.

| Job | Core activity | Ties into the sim through |
| --- | --- | --- |
| Galley / crew services | Cook from the stores, learn favourites, time meals to shift changes | Hunger, mood, food supplies |
| Infirmary aide | Notice who's run-down, treat them, send them to rest | Energy, health, mood |
| Survey lab assistant | Collect sensor readings, run samples through lab equipment | Sensors, story threads |


## Art, camera & controls

The look is locked: textured low-poly in a cozy isometric cutaway, with every texture drawn in code. The old living deck from builds 0.3.x is kept in the build as the style reference.

- **Camera:** orthographic isometric view that follows you. Walls between you and the camera drop to knee height, a straight run at a time; tall furniture fades a room at a time. Rotate in 90° steps; pinch or scroll to zoom. Zooming out stops before the edges of the drawn area show (the user, 2026-10-16: no visible culling), while still giving a good wide view. The user kept this limit (2026-10-16 ~22:30) rather than limiting further; when zoomed far out, small decor will be thinned out later so it stays quick on phones.
- **Materials:** procedural textures (deck plating, carpet, wall panels, fabrics, wood, rugs, screens), soft shadows and warm lamps. Lighting shifts from cool white by day to amber at night.
- **Each deck has its own character.** Deck 4 is homey: carpet and warm lamps in the officers' corridor, plate floors and work lights in the junior wing. Deck 5 is a workshop: steel plate, grating, hazard striping, pipe runs and cool work lights. Deck 3 is the warm heart of the ship, with a planked promenade, the garden and the lounge. Deck 6 is warmer and dimmer, and the bridge is cooler.
- **Curved hull:** the deck keeps its tile grid for walking, but the outer hull follows the ship's curved shape, with rounded corners and an elliptical bow. Every deck draws its hull in one smooth piece per facing, so the stripes run unbroken (Decks 3 to 5 joined the others on 2026-10-16). Windows are openings in the curved hull, onto the stars. Inner glass walls let you see into sealed rooms and machine rooms.
- **Characters:** built from a one-line spec with skin tone, hair style and colour, height, build, accessories, department colour and badge. Walk animation with planted feet.
- **Controls:** tap to walk to a spot or object, press and hold to walk toward your finger, tap a person to talk, tap a free seat to sit, tap a machine to look at it or use it. Walk into the lift car (or tap a lift door) and press the panel on its back wall to choose one of the six decks. Doors slide open for anyone nearby; sealed rooms give tap text.
- Crawlways get low ceilings, and their tiles slow you to a crouch-walk with a crouching pose.
- **UI:** the personal device (its old-school screen look and apps are under "The player"), the machine inspection panel and a two-slot carry indicator. No time controls (dropped, see Open questions).


## Technical plan: how decks work in the build

The game stays one HTML file using three.js r128 from cdnjs, built in chat on a phone (Galaxy TriFold), with no image assets. Ship, decks, machines, crew and jobs are all stored as data, so adding content never means rewriting code.

**One deck in memory at a time.** Only the deck you are on is built. Leaving a deck unloads it completely; built decks are never cached, because a single floor texture is 4096 × 2048.

**Ship state outlives decks.** A ship-wide state (`SHIP`) holds everything that must survive a deck change. A deck is rebuilt from its definition plus that state, so leaving a deck loses nothing. Today it holds unlocked doors per deck; systems, machines, supplies and wear join with the Living Ship (Pillar 2).

**Deck definitions.** Each deck is one block of data in `DECKS`: number, name, random seed, lift position, a text map of rooms, doors, hull shape, windows, sealed rooms and their tap text, and a dress function that furnishes it in a fixed order. The seed means a deck comes out the same every time. Deck plans are sketched as stand-alone HTML pages in `plans/`, in the same format, so a plan's data block drops straight into `DECKS[n]`.

**Shared kit vs. current deck.** Materials, textures, furniture builders and room templates are made once at load and shared by every deck. Everything a deck build creates belongs to that deck and is freed on unload.

**Room templates.** A room is furnished from its size and where its door is (bunk room, washroom, laundry, officer cabin so far), and the same template works whichever way the room faces. Templates also record the spots people use: beds, showers, basins, washers, desks.

**Ship frame.** Every deck is placed so its lift sits at the same world position, which keeps the spine lined up from deck to deck.

**Changing decks.** `goToDeck(n)` hides the crew, unloads, builds deck n, puts you by the lift and brings in the crew who are on that deck. Each crew member has a deck; only those on yours walk tile by tile. The lift's fade covers the rebuild.

Rules that keep it working on phones:

- Never let two surfaces share a plane: overlap solids, or keep faces at least 0.005 apart.
- Keep the canvas opaque, the camera depth range tight, and snap the camera to whole pixels.
- Avoid per-pixel noise on large surfaces; it shimmers on high-resolution screens.
- 1 unit equals 1 floor tile. Furniture blocks tiles; walls sit on the edges between rooms.
- Distant crew are drawn with less detail. For crowds over 70 (ship-wide events) a third, coarsest level of detail keeps them cheap.
- Decks with different lamp counts may compile extra shaders on first visit. If the lift's fade doesn't hide the pause, pad every deck to the same number of point lights.

**Testing.** `cadet_test.py` compares two builds headlessly (Playwright and SwiftShader) with a virtual clock, so runs are deterministic: deck data, paths, collisions, crew positions, taps and screenshots. `deck_check.py` visits every built deck and checks reachability, crew, draw calls and memory. Real-device checks on the TriFold are the final word.

**Working method.** This design doc, the latest build, the deck plans, the tests and the dev notes live in the git repo. Several sessions work in parallel under a lead session (see `TEAM.md`). Builds are edited in place, never rewritten whole. Turns stay short, each ending with a tested build. When a session gets long, the dev notes are updated as a handoff for a fresh one.


## Milestones

The current build and its history are in `DEV_NOTES.md`.

Done so far:

| Build | What it added |
| --- | --- |
| 0.1 | Art style test, one cabin |
| 0.2 | Character kit and walk animation |
| 0.3 | The living deck (now the style reference), press-and-hold walking |
| 0.3.2 | Step 1: kit carry-over, wall runs, v3 uniforms and badges |
| 0.3.3 | Step 2: room templates |
| 0.3.4 | Step 3: curved hull walls |
| 0.4.0 | Step 4: Deck 4 junior wing; officers' wing built and locked |
| 0.4.1 | Step 5: Deck 4 finishing touches |
| 0.4.2 – 0.5.0 | Step 6a: decks as data, unloading, ship frame, crew decks, ship state. Plays exactly as 0.4.1. Deck 5 planned (6b). |
| 0.5.1 – 0.6.1 | Step 6c: Deck 5 and the lift. The lift panel and ride, the Works complex dressed, the shuttle bay with the Tern, the walk-in lift car, the spine behind glass, the moving sky and real windows, the Deck 4 music room. Pell moved to Deck 5. |
| 0.6.2 – 0.7.0 | Step 6d: Deck 3, the Commons. Mess hall and galley, the bow lounge, the garden, infirmary, gym, crew store and call-home booths, the dressed promenade. Chef Brennan and Rina on Deck 3. |
| 0.7.x onward | Step 6e: Decks 6, 1 and 2 built (shell, rooms, dressing and furniture; no crew or machines), then integrated into one build. In review. |

**Next: the Living Ship.** Crew and simulation as one phase, built in four pillars. Each pillar ends with something playable and is reviewed before the next begins. It replaces the old step 7 (machines, supplies and the shared job list), which is now Pillar 2.

1. **Foundation:**
   - the ship clock (now 18 ship hours in 30 real minutes), calendar, rota and days off;
   - sleeping skips to morning;
   - the 75-crew roster as data;
   - crew moving through their schedules on decks the player isn't on;
   - crew drawn on the current deck walking their real schedule, with daily variety;
   - Test: watch a full ship day and check it feels alive.
2. **Ship systems and jobs** (agreed 2026-10-15; the breakdown is in `plans/pillar2-plan.md`):
   - every room in use by crew and player, and the utility rooms built inside;
   - player needs (hunger, energy, hygiene, fitness) and activities: working out, calling home, shopping;
   - food and cooking simulated, with the chef cooking ahead of each meal;
   - systems with condition and wear, and their dependencies;
   - consequences in stages: machine effects on crew needs and mood, and uniforms and the laundry;
   - the job board, parts and carts;
   - crew and player tending the ship, with the player's tools: the personal device, inspect, two-slot carry, repair;
   - the ship health board on the bridge and in the Works bay.
3. **Your device, the people aboard, and the first events** (agreed 2026-10-16; the breakdown is in `plans/pillar3-plan.md`). The social and events pillars meet here, because events are mostly people talking:
   - the personal device: two layers, the old-school screen skin and all its apps, appointments that crew keep;
   - relationships, chat cards, crew affinity, crew seeking you out, favours, and the first arcs for Tomas, Pell and Rina;
   - the news model: gossip and chatter from the ship simulation and from crew lives;
   - everyday guests;
   - the event framework (phases, threads and bands, traces, the Captain's address, gatherings and meetings with dialogue), then the ion storm end to end;
   - the progression hooks: the ready room, the conference table, officers' cabins, the Captain's table and progress talks;
   - extra gym kit, and a small sound pass in or right after this pillar.
   - Two check-ins with the user: one after the device and social basics, one after a full ion storm.
   - Combined builds are 0.50.x. Two new helpers join: the device engineer (builds 0.35.x) and the social engineer (0.36.x); the events engineer carries on.
4. **More events, onboarding and tutorials:** after the ion storm, the rest of the event list in order (see "Ship-wide events"), each reviewed by the user as decks were; the festival once the real-phone test allows it. Also full onboarding and tutorials, growing from Pillar 3's first tips.
   - **Pillar 4 scope (the user, 2026-10-16): a massive pass, "full bore".** The full arrival and first week (above); far more dialogue (a voice for every crew member, overheard conversations, reactions to what happens aboard, story arcs); a much deeper social system, where getting to know someone unlocks moments where you really get to know them, sometimes their struggles; many more traditions. Tone: mostly light, with serious and heartfelt moments as you grow close. Staffing: a Pillar 4 planner and a social system designer plan it together first; then engineers, a head writer with a few writers, and tradition designers (about 15 helpers).
   - **Pillar 4 decisions (the user, 2026-10-17):** a head writer and three writers (a fourth only if needed); writers and tradition designers may start early, but engineers and designers build every hook and format they need first; four ship seasons named for the garden (Sowing, Greening, Harvest, Lanterns); serious themes allowed (homesickness, a failed exam, a parent getting older, self-doubt, a friend drifting, gentle grief), nobody dies on screen; friends visit your bunk (friends only, evenings, easy to ignore), and once you're promoted and have your own room you can invite people over; gifts can be bought, picked or made in the machine shop; **reputation**, a full system, by department and ship-wide, which can dip when you leave a department's job unfinished; no "5 of 11 things" counts in the Crew app (too gamey); the remaining big events (comet viewing onward) wait for their own later phase.
   - **Crew come and go (the user, 2026-10-17):** not often, crew are transferred off and new crew arrive, including new cadets like you. Someone leaving says goodbye a day or two before (talking about your friendship) and again on the day. At some point you're assigned to guide a newcomer the way you were guided.
   - **Tiles (the user, 2026-10-17):** a simple playable tile game, designed by us later. A small tiles station with boards in the lounge; on tiles night, every lounge table has a board.
     **Direction (the user, 2026-10-17 ~02:50):** a two-player mix of checkers and block matching: quick and fun, visually appealing, original, balanced, tight, easy to get into, accessible, quick and different. Hired now (ahead of wave 3): the Tiles engineer designs it first on `plans/tiles-plan.html` for the user to approve before it's built.

**After that:** progression to tier 2 (certification, promotion to Officer and your own cabin, the Deck 5 machine rooms and connected-system faults) and the spine's crawlways and pipe galleries. (The shuttle arrival is now part of Pillar 4.)


## Open questions

**The game:**

- The Works Chief is Chief Ines Calder. Her personality and how she judges your work are still to be designed, before Pillar 2, because she runs the job board and certifies the player.
- Should the player ever work the night shift, for example as part of on-call duty?
- How does diagnosing a fault look on screen: a simple panel with labelled components, or something more hands-on? Prototype it in Pillar 2.
- Can the player be passed over for certification, or only delayed?
- Beyond the name you type on the shuttle, should the player ever choose their look? (No choice of look for now, the user, 2026-10-16.)
- Does the diplomacy-and-story starship game become its own future project?

**The decks:**

- Who keeps the engine watch on Deck 6: is there a watch on both shifts, and are they Works crew?

**Answered:**

- Who meets you off the shuttle, and which milestone builds the arrival: Zeke Torres, a Works engine officer, built in Pillar 4 (the user, 2026-10-16/17). See "The player".
- The device's phosphor colour is the Wren's cyan, with amber and green as options in Settings (the user, 2026-10-16).
- The personal device (agreed 2026-10-16): two layers (apps describe, a skin draws), an old-school screen look built now, never pausing time, and the apps Schedule, Appointments, Maps, Memos, Mail, Calendar, Needs, Jobs, Crew, Ship, Record and Wallet (Music later, with sound). No Camera. See "The player".
- The event after the ion storm is the diplomatic visit; all seven main events are kept in a fixed order with six short ones between them (agreed 2026-10-16). See "Ship-wide events".
- Events are ambient, with four kinds of moment including meetings with dialogue, never a full cutscene (agreed 2026-10-16). See "Ship-wide events".
- Deck 4's guests: an everyday guest arrives about once a ship week, plus guests who come with events (agreed 2026-10-16). See "Social life".
- Pillar 3 builds the device, the social basics and the start of events together (agreed 2026-10-16). See "Milestones".

- Needs give a bonus at 75 and over and a penalty under 25 (agreed 2026-10-16; replaces "fitness gains nothing" from 2026-10-15). See "The player".
- Your needs show on your personal device, the main interface; a placeholder until its design is done (agreed 2026-10-15).
- No time controls (time speed, crew and systems panels): dropped for now (agreed 2026-10-15).

- The player starts in Bunk 1 with Tomas, and Pell and Rina are in Bunk 2 (answered since v3).
- 18 ship hours take 30 real minutes, so a whole day is 40 (agreed 2026-10-16; first 30 minutes a day, before that a guess of 10). This sets every wear rate.
- What triggers the first story events: ship-wide events are the main missions, about one every 1–2 ship weeks, starting with the ion storm (see "Ship-wide events").
- Decks 6 and 1 are reachable by lift from day one. Utility rooms lock by tier (closets 1, plant rooms 2, batteries and power junctions 3, so Deck 6's junctions stay at tier 3); locking by story comes later (agreed 2026-10-16).
- The bridge's sunken command ring is faked for now with a rail, a painted step edge and a curved step strip.
- The bridge washroom stays.
- The game starts on Day 1, a Monday, at 06:00, with the player in Bunk 1 (agreed 2026-10-15).
- The player is one of the 75 crew: one of the 47 juniors, so 46 others plus you share the 48 berths, with one empty (agreed 2026-10-15).
- The junior bunk rooms get bigger so each fits three ordinary bunk beds (6 berths), rather than triple bunks or fewer juniors (agreed 2026-10-15). Deck 4 plan Sketch 3 approved the same day: rooms 5 × 4, the air scrubbers, junior stores, utility closet and heating plant shrink, no guest cabins given up, and no table in the bunk rooms.
- Saving is automatic, in the browser, per device; the game resumes where you left it (agreed 2026-10-15). Built in 0.15.1: the game saves every ship hour, on deck change and when it's hidden or closed; New game (tap twice) starts again.
- Night runs 21:00–06:00, with an hour of dusk and of dawn centred on those times, so the game opens at first light. The old Night/Day button is now a debug control (built in 0.15.1).
- Going to sleep: get into your own bunk from 20:00 and the night skips to 06:00, with no question asked (agreed 2026-10-16).
- Each weekday has a shape (provisional, from the schedule engine in 0.21.1): a Monday briefing, a Wednesday afternoon drill, a Thursday bunk inspection, later nights on Friday and Saturday, and a Sunday lie-in. Two meals a day, no lunch; the tea break counts as work.
- The Works Chief, the Infirmary Chief and the six senior officers were named by the crew designer (build 0.16.1): Works Chief Ines Calder, Infirmary Chief Priya Nandakumar, and the six senior officers named in "Crew and rooms". The user approved the names (2026-10-16).
- The player meets about 3 to 6 jobs a day; the crew leave small jobs for a while (agreed 2026-10-16, see "The job list").
- Deck 2's second visitors' cabin stays a cabin, not a senior lounge: ship-wide events bring visitors (2026-10-16).
- Answered no (2026-10-16), so not to be re-asked: the player helping in the galley, lunch, binning the grab shelf overnight, opening the store every day, extra gym kit or booked gym slots (more later), and the ship running while the game is closed. Unanswered, so kept as it is: faulty machines slow only the crew, not the player.
- Envoy Saruth is a guest, not one of the 75 crew.
- Deck 2's six senior officers are confirmed (Second Officer, Senior Helm Officer, Ship's Counsellor, Comms Chief, Deputy Survey Chief, Senior Watch Officer), moved up from Deck 4's officers. The six cabins they leave on Deck 4 become guest cabins, so the deck stays lived-in (agreed 2026-10-15).
- Deck 4's guest cabins are the six nearest the lift: 4-01, 4-02, 4-03 and 4-04 (the first column, two with windows) and the inner pair 4-07 and 4-08, so guests don't walk the corridor and officers keep 10 of the 12 window cabins. The two spares are 4-23 and 4-24, the inner pair at the music-room end. Guest cabins never use bunks (built in 0.14.0).
