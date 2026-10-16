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

- **No fail state.** A neglected ship gets shabby, uncomfortable and talked about. It is never lost. Losing would break the feeling of being just another crew member.
- **The player climbs but never commands.** They start on simple jobs (filters, lamps, carts), then move up to the engines and eventually sit in briefings with the Captain. Rank decides which jobs and which parts of an event reach the player.
- **A ship day lasts 30 real minutes.** One ship hour is 75 real seconds, and a 7-day ship week is about 3½ hours of play.
- **The ship doesn't run while the game is closed.** Time stops when you leave and resumes where you were.
- **Sleeping skips time.** When the player sleeps, time skips to morning. The player's own needs (hunger, rest, hygiene) work as described under "Crew simulation".
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

**Access and mood.** The lift reaches every deck from day one. Locking parts of the ship by tier or story comes later, with the story work; until then, sealed rooms and hatches show what's behind them with tap text. Each deck has its own lighting mood: warmer and dimmer on Deck 6, cooler on the bridge.


## Crew and rooms

All 75 crew have a rank and a bed, and where you sleep shows where you stand: senior crew in quarters on Deck 2, officers in single cabins and juniors in bunk rooms on Deck 4.

| Rank | Count | Lives in |
| --- | --- | --- |
| Captain | 1 | The Captain's quarters, Deck 2 |
| Executive Officer | 1 | Cabin, Deck 2 |
| Department Chief | 4 (Works, Watch, Survey, Infirmary) | Cabins, Deck 2 |
| Senior Officer | 6 | Cabins, Deck 2 |
| Officer | 16 | Single cabins, Deck 4 (24 built: 16 officers, 6 guest cabins, 2 spare) |
| Junior Officer | 47 | Bunks, Deck 4 (8 rooms × 6 = 48 berths, 1 empty) |

**Deck 2's senior quarters** have twelve crew bedrooms and three visitor rooms for VIPs such as the Envoy. Six of the twelve are the Captain, the XO and the four Chiefs. The other six are senior officers: a Second Officer, a Senior Helm Officer, a Ship's Counsellor, a Comms Chief, a Deputy Survey Chief and a Senior Watch Officer. Their names and personalities are still to be written.

**Guest cabins on Deck 4.** With six officers moved up to Deck 2, six of the officers' corridor's 24 cabins are guest cabins and two stay spare. Guests come and go: visiting specialists, passengers being carried somewhere, crew from other ships in transit, and people who arrive with events (a scientist for the nebula, a delegation's staff, survivors from a salvage job). The corridor always has a few new faces and new things to talk about, which feeds the social system and gossip. Guests aren't part of the 75 crew.

**Deck 4, the Quarters deck.** The junior wing sits aft of the lift: 6-berth bunk rooms, two shared washrooms, a laundry and a junior common room with stern windows. The officers' corridor runs forward of the lift toward the bow: single cabins, carpet, warm lamps and quiet after 23:00, ending in the music room at the bow, a soundproofed room with a door, so the corridor stays quiet. It has a stage round the bow windows with drums, guitars, amps and a mic, a grand piano, beanbags, a record cabinet and a rail of instruments to borrow; the Captain plays the piano late on Thursdays. Twelve cabins have hull windows; twelve are inner cabins. Sixteen hold officers, six are guest cabins and two are spare.

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
  - the Works Chief, your boss and the one who certifies you, still to be named and designed. They live on Deck 2 and work from a glass office on Deck 5.
- **About 65 generated crew,** with names, looks, jobs and personalities. Each comes from a template: role, home deck, shift, habits, a couple of personality traits, and a few life details for gossip.

Pell works on Deck 5 for now. When shifts move crew between decks, Pell will sleep in Bunk 2 and work on Deck 5.


## Deck 5: the working deck

Deck 5 is the ship's garage, not its home, and it was built first after Deck 4 so the Works bay can anchor the shared job list. Where Deck 4 is homey, Deck 5 is a workshop: steel plate and grating floors, gold-and-charcoal hazard striping at doorways and machines, pipe runs along the walls, bright cool work lights and very few windows. The plan is in `plans/deck5-plan.html`.

**Shape.** About 44 × 16 tiles, narrower than Decks 3 and 4. The lift lines up with Deck 4's, a little aft of midships, splitting the deck into a cargo end aft and a working end forward.

| Area | What's there | Opens at |
| --- | --- | --- |
| Shuttle bay (stern) | One small shuttle, the Tern, on its pad; the flat stern hull is the bay doors; a control booth with glass over the pad. Where you first arrive. | Start (bay floor) |
| Bay door gear | Giant gears and rams in the stern corner; the doors slide into a pocket here. Glass panel onto the pad. | Sealed, visible through glass |
| Cargo hold | Crates off the shuttles plus the big spares. Where supplies enter the ship; they leave on hover hand carts up the main lift. | Sealed until supplies start moving |
| Cart bay | Hover hand carts, docked and charging between runs. | Opens once supplies start moving |
| Haulway and lift lobby | The walkable route from the shuttle pad to the lift, opening straight into the Works bay. | Start |
| Works bay | Big job board (the shared job list's home), workbenches, tool wall, kit lockers, a window onto the shuttle pad, and the Works Chief's glass office overlooking the floor. | Start |
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

- **Mess hall and galley** along the port side. The mess hall is the biggest room on the ship: long tables and round ones, a drinks station, a tray return, a menu board and hull windows. The serving counter opens through to Chef Brennan's galley, with a grab-and-go shelf for anyone running late. A walk-in cold store sits behind the galley, stocked by hover cart.
- **The bow lounge** fills the whole bow on one floor, with curved windows sweeping from side to side and a curved bar stocked from the galley behind it. It's zoned so it never feels like one empty hall: a lively bar end and a quiet window end.
- **The infirmary** is just aft of the lift, with a ward, an exam room and Rina on duty.
- **The hydroponics garden** fills the stern: grow racks, raised beds, fruit trees, a pond with benches and a herb wall for the galley. Glass doors at the end of the promenade let you see green as soon as you step out of the lift.
- **Along the starboard side:** a gym, a small crew store, and call-home booths for recorded messages home.
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

- **The bridge** fills the bow. A curved viewscreen covers the bow wall. Facing it is the command ring: the Captain's chair with a seat either side, the helm and ops consoles in front, and a curved wooden rail behind. The ring is a sunken ring in the design; for now the build fakes the step with the rail, a painted step edge and a curved step strip, and a real sunken floor can come later. The rear stations (Watch, Survey, Comms and Works) stand along the aft walls. The bridge has its own dark carpet with the command ring inlaid.
- **The Captain's ready room** is aft of the bridge on the port side, opening from the bridge: a desk, a bookshelf, a port window and an aquarium with one slow fish called the Admiral.
- **The bridge washroom** mirrors it to starboard, so the watch doesn't have to ride the lift down.
- **The observation room**, on the far side of the lift, is also the conference room: a long table for ten, a wall screen and windows round the stern and both sides. Briefings happen here.
- **Service layer:** the relay room and a sub-floor crawl under the rear stations (tier 3, a shortcut up beside the Works station), and a utility closet. The ladder and trunks end here.


## Deck 2: Command & Science

52 × 22 tiles, on Deck 3's outline. The deck splits at the lift: the lift's stern door opens to the senior quarters and its bow door to science. The plan is in `plans/deck2-plan.html`.

- **The senior quarters**, aft of the lift: one carpeted corridor in a loop, with fifteen bedrooms opening off it, each with its own door. Twelve are for the senior crew and three for visitors.
  - **The Captain's quarters** fill the stern, with windows all along it: the biggest bedroom aboard, with a dining table where the Captain hosts the senior crew and the Envoy, a study and a sleeping alcove.
  - **Hull cabins with windows** for Commander Vance, the Works Chief, the Infirmary Chief, Dr. Sato, Chief Holt (next door to the Envoy), the visitors' suite and three of the senior officers.
  - **Envoy Saruth's guest cabin**, on a stern corner: a low table for Veyli tea rituals, cushions instead of chairs, and a knot of cord on the door handle meaning visitors by invitation.
  - **Inner cabins** inside the loop for the other three senior officers and a second visitors' cabin.
- **Science**, forward of the lift along a wide science corridor: the Watch office (glass onto the lobby, so the Watch sees who rides the lift), the chart room, the Survey lab, the sample lab, the comms room (where every recorded call home goes out), an observatory with bow windows, the specimen store and the probe bay.
- **Service layer:** the sensor and comms array, a sealed machine room in the nose seen through glass at the end of the science corridor (tier 3); the lab gas plant (tier 2); a cable crawl along the starboard hull (tier 3); a utility closet.


## The clockwork: systems, supplies and the job list

Every machine aboard has a condition that wears down with use and time, and wear turns into work on one shared job list that the whole crew draws from.

### The ship's systems

- **Systems:** air, water, power, heat, food, waste and laundry, hull, comms and sensors, and propulsion.
- **Condition:** each system has a score from 0 to 100 that wears down with use and time. Each is made of parts that can fail, such as filters, pumps, relays and seals.
- **Dependencies:**
  - Power feeds everything.
  - Water feeds the garden, and the garden feeds the galley.
  - Air needs scrubbers, and scrubbers need filters from the Deck 5 hold.
- **Ship health** is a blend of all the systems. It shows on a status board on the bridge and in the Works bay.

### Machines

Each machine is a real object in a room, with a condition from 100% to 0%, a wear rate and the effect it has on the ship when it falters. Wear depends on use: the galley oven wears fastest around mealtimes, the laundry washers on the morning after a busy shift, the lift whenever people ride it.

A machine's life runs through five states:

1. **Healthy.** Works normally.
2. **Worn.** Still works, but a sharp-eyed tech can spot it. Servicing now is cheap and quick.
3. **Faulty.** A fault is logged on the job list. The machine works badly: slower, noisier, less effective.
4. **Failing.** Effects spread to the crew and the ship. The job is marked urgent.
5. **Broken.** The machine stops. Repairs take longer and need more parts.

### Supplies

Supplies come aboard by shuttle into the Deck 5 cargo hold and are shelved in main storage: filters, spare parts, tools, linen and food stores. Food goes up to Deck 3's cold store on hover hand carts via the main lift. Repairs use parts and cooking uses food. Low stock adds restock work. An empty shelf blocks a repair until supplies arrive, unless you make the part in the machine shop, which is slower.

### The job list

One list for the whole ship, shown on the big job board in the Works bay and on your wrist comm. The ship adds jobs itself: faults, routine servicing, restocking, cleaning, cooking.

1. Wear generates jobs, which go onto the Works bay job board.
2. Crew on duty with the right department and skills claim them.
3. They fetch parts, using hover carts from the Deck 5 hold for supplies, walk to the fault and fix it.
4. The player gets the skilled or interesting jobs for their rank. Routine jobs get done by the crew if the player leaves them, but more slowly. Jobs nobody claims pile up and get worse.

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

**The galley's week** (decided 2026-10-16). The menu runs on a weekly cycle: a crew member's favourite on Wednesdays, a Friday treat with a pudding, and a Sunday dinner the crew vote for; the menu board in the mess shows the day's meals. Food in the cold store spoils when its chiller falters (faster the worse it is); the galley bins what's gone off and tells you by Mail. Some meals are busy: a rush after the 17:00 shift change, or an oven playing up, and a short queue forms. On a crew member's birthday the galley bakes a cake for after dinner. Nobody but the galley crew works in the galley, the grab shelf isn't cleared overnight, and there's no lunch.

On duty, crew claim jobs from the job list that match their department and skill, walk there and do the work. A Works tech fixes the scrubber; Chef Brennan cooks; Infirmary checks on whoever is run-down.

Off duty, each person picks what to do by scoring their options against their needs and traits: eat, sleep, wash, socialise, relax in a favourite spot, a hobby.

**Needs.** Hunger, energy, social and hygiene, from 0 to 100. Showers restore hygiene, which gives the washrooms a morning rush. Mood comes from needs, the state of the ship and the people around them.

**Skill.** Each crew member has a skill level in their department. Skilled crew work faster and cause fewer follow-up faults.

### Routines with variety

No crew member does exactly the same thing at the same time every day. Variety comes in layers:

1. **Rota.** A 7-day ship week with staggered days off, so a different crowd is at breakfast each day. Some crew move between day and night shifts every few weeks.
2. **The shape of each day.** Each day of the week runs a little differently. For example: drills one day, maintenance inspections another, and on the rest day a late breakfast, a busy gym and a film in the lounge.
3. **Time jitter.** Small daily offsets for everyone, such as waking 5–25 ship minutes early or late, or lingering at dinner. The offsets come from a seed per person per day, so they look random but replay the same way. That keeps saves and tests reliable.
4. **Habits.** Personal quirks: an early riser, someone who always takes the window seat, someone who skips breakfast, someone who calls home on rest days.
5. **Needs drive choices.** Hunger, tiredness and wanting company make crew choose between a few options instead of following a script.
6. **Interruptions.** Faults and events pull crew off their routine. This is how the ship simulation reaches daily life.

*Example:* on Monday Pell has breakfast at 07:40, then goes to the Works bay. On Thursday it's breakfast at 07:10, then drills. On a rest day Pell sleeps in, goes to the gym, then the garden, and gets called away to a scrubber fault one evening.

### Crew on other decks and performance

Only one deck is loaded at a time. Crew elsewhere are simulated "on paper": they move through their schedules as data and are drawn only when the player is on their deck. Arriving on a deck shows everyone where their schedule puts them. Only crew on the deck you are viewing walk tile by tile, so the full crew of 75 stays cheap on a phone. A busy deck shows about 15–25 people at once.

All 75 crew (about 60 on days, 15 on nights) are in the simulation: about 10 hand-written story characters and about 65 generated ones (see "The crew: 75 people").


## Social life

**Relationships with the player.** Every crew member has a relationship meter with five tiers: stranger, acquaintance, colleague, friend, close friend. It doesn't decay, or decays very slowly, to keep the game cozy.

Ways it grows, biggest first:

1. Working a job together.
2. Eating together.
3. Talking: once per person per day counts, so it can't be farmed.
4. Helping with something they mentioned.

What higher tiers unlock:

- They greet you.
- At social time, they come and find you.
- They share news about their life (family back home, a hobby) and about the ship.
- Friends cover a job, tip you off about spare parts, and put in a good word with the Works Chief toward promotion.

**Reputation.** Crew remember who keeps their corner of the ship running. Good work raises friendship and trust.

**Gossip is a hint system.** Crew news comes partly from the ship simulation: "The scrubbers on 4 have been rattling all week." "Brennan's furious, the cold store's warm again." The social system quietly tells the player what the ship needs. News is built from sentence templates filled in with what's actually happening; no AI writing is needed.

**Crew relationships with each other.** Each pair of crew has an affinity that drifts as they eat, work, bunk and spend time together. Friendships and small rivalries form on their own. They shape who sits together, who swaps shifts and who avoids whom, so the player can stumble into their dramas.

**Romance** is out for now.

### Ship traditions

*Decided 2026-10-16 (the answers pass; built in 0.34.0).* Alongside the big ship-wide events, the Wren has small, recurring traditions, "lots of little holiday-like things, almost like Stardew Valley". The crew who are free simply go, and talk about them; nothing stops daily life, and there are no menus or cutscenes.

- **Weekly:** running club (Monday evening, the gym), quiz night (Thursday, the bow lounge), Works Friday tea and tool cleaning (Deck 5) and the Friday music jam (Deck 4), film night and observatory night (Saturday: the junior common room, and Deck 2's observatory), and the Sunday swap meet on the promenade.
- **Every few weeks:** harvest morning in the garden (every other Saturday, fresh salad at dinner) and the hull-lights evening (every four weeks).
- **Birthdays:** each crew member's day; the galley bakes a cake and the mess gathers after dinner (20:15): their department, their bunkmates and plenty of others.
- **Once a year** (a ship year is 52 weeks): Founding Day (day 100: cake and a few words from the Captain) and the quiet watch (day 300: a quiet while at the windows for the people they miss).
- **Hearing about them:** a Mail the evening before (on the device's calendar later), and crew mention them when you talk to them ("Coming to the quiz tonight?").
- **Joining in:** be in the room while it's on. It gives a little social, and the organiser thanks you.


## The player: Works technician

You work the day shift as a Works maintenance tech, taking jobs from the same list as the rest of the crew and doing them with your own hands.

**Arriving by shuttle.** The game opens with your shuttle landing in the Deck 5 shuttle bay. You step off onto the pad, walk the haulway to the lift lobby, glimpse the Works bay that will be your workplace, and find your own way up to your bunk on Deck 4. The shuttle Tern is already in the bay with its ramp down, ready for it. Until the arrival is built, the game starts with you waking in Bunk 1. Still to decide: which milestone builds it, and who meets you off the shuttle.

**The job loop.** Every job follows the same physical steps:

1. **Notice.** A fault arrives on your wrist comm or the Works bay job board, someone flags you down, or you spot a worn machine on your rounds.
2. **Diagnose.** Open the panel and inspect it. You see which component is failing and what the fix needs.
3. **Fetch.** Get the part or tool from main storage or the Works bay, or make it in the machine shop. You can carry two items at a time.
4. **Repair.** Hold to work. Repairs take longer on broken machines and go faster as your skill grows.
5. **Done.** The machine recovers, the job closes, and the people it affected notice.

What makes it interesting:

- **Priorities.** Several jobs compete. The urgent scrubber, the oven Chef Brennan keeps asking about, or the routine service that prevents next week's breakdown?
- **Prevention.** Spotting wear early is cheap and quick. Waiting for faults costs more time, parts and goodwill.
- **Routes.** Walking matters, and the job spans decks: parts are on Deck 5, the scrubbers on Deck 4, the oven on Deck 3. Fetching the right parts in one trip saves real time on your shift.
- **Interruptions.** The ship keeps living around you. People stop you for help or argue in corridors.
- **Reputation.** Crew remember who keeps their corner of the ship running. Good work raises friendship and trust.

**No hard failure.** If you slack, other Works crew pick up jobs, but more slowly, and your supervisor notices. The ship never dies because of you, but it gets visibly worse.

**Off shift**, you are free: eat, wash, socialise, explore, sleep. Some crew will ask for small favours, like fixing a lamp in their cabin, which build friendships and earn goodwill. Sleeping skips time to morning.

**Your needs** (decided 2026-10-16). Food, energy, hygiene, fitness and social, from 0 to 100. A rested player stays up 16 to 18 ship hours before energy runs low (about 17 at average fitness). Getting into your bunk from 20:00 fades out and wakes you at 06:00, with no question asked; earlier, the bunk says it's too early. Needs give bonuses as well as penalties: at 75 or more a bonus, under 25 a penalty, in between nothing, and the effects multiply. Well rested: tasks go faster; fit: you walk a little faster and tire more slowly; well fed: you tire more slowly; clean: chatting does you more good; in good spirits: tasks go faster. Tired or out of shape: you walk slower; hungry: tasks go slower; unwashed: chatting does less good; lonely: you tire sooner. The device marks each need giving a bonus or a penalty, with a one-line reason. Faulty machines slow only the crew, not you. The exact numbers are in DEV_NOTES ("Player needs and the device").

**Thirty seconds of play.** Your wrist comm chirps: scrubber 2 on Deck 4 is at 60%. You head out of the junior wing, passing Rina and Pell arguing in the corridor. You open the scrubber panel; it needs a filter, so it's down the lift to storage on Deck 5. On the way back, Chef Brennan calls: the oven on Deck 3 is acting up again. Now, or after the scrubber? You choose, and the ship reacts.


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


## Ship-wide events (main missions)

Story arrives without stopping daily life, like a TNG episode where a phenomenon or entity changes life aboard for a while. Story sits on top of the simulation, so events grow out of a living ship rather than replacing it.

**An event is a layer on top of normal life.** For a few days it changes the ship's systems, the crew's routines and what the decks look like, and it adds its own jobs to the board.

**Structure:** onset, then escalation, then resolution, over 2–4 ship days. Every event resolves. How well it goes decides:

- ship health afterwards;
- relationship gains;
- commendations toward promotion;
- small permanent traces, such as a scorch mark, a plaque or a new pet.

**Pacing:** roughly one main event every 1–2 ship weeks (3½–7 real hours), with small incidents most days. Small incidents include crew moments the simulation can trigger: a friendship scene, an argument that needs smoothing over, a birthday gathering in the mess (see "Ship traditions").

**What the player sees depends on rank.** A junior carries filters during the storm. A senior is in the Captain's briefing about it.

**Event ideas:**

- **Ion storm** (the first to build, because it touches every system): power flickers and comms go down. The bridge runs double shifts and the mess goes quiet.
- **Diplomatic visit:** Envoy Saruth's delegation fills the visitor cabins. Formal dinners in the Captain's quarters stretch the galley.
- **Something in the garden:** a creature eats the crops, food quality drops, and the hunt involves half the ship.
- **Shipboard illness:** the infirmary fills and sick crew stay in their bunks. Fewer hands means more work for everyone.
- **Nebula drift:** the sensor array is overloaded, and strange dreams leave the crew sleepy and chatty.
- **The déjà vu day:** a time anomaly replays the same day. Seeded routines make this cheap to build.
- **Salvage:** a derelict is found. The shuttle Tern goes out and the cargo hold fills with odd finds.
- Other ship situations that put the systems under pressure: a power surge, a Veyli vessel needing aid, a sensor anomaly.

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

- **Camera:** orthographic isometric view that follows you. Walls between you and the camera drop to knee height, a straight run at a time; tall furniture fades a room at a time. Rotate in 90° steps; pinch or scroll to zoom.
- **Materials:** procedural textures (deck plating, carpet, wall panels, fabrics, wood, rugs, screens), soft shadows and warm lamps. Lighting shifts from cool white by day to amber at night.
- **Each deck has its own character.** Deck 4 is homey: carpet and warm lamps in the officers' corridor, plate floors and work lights in the junior wing. Deck 5 is a workshop: steel plate, grating, hazard striping, pipe runs and cool work lights. Deck 3 is the warm heart of the ship, with a planked promenade, the garden and the lounge. Deck 6 is warmer and dimmer, and the bridge is cooler.
- **Curved hull:** the deck keeps its tile grid for walking, but the outer hull follows the ship's curved shape, with rounded corners and an elliptical bow. Windows are openings in the curved hull, onto the stars. Inner glass walls let you see into sealed rooms and machine rooms.
- **Characters:** built from a one-line spec with skin tone, hair style and colour, height, build, accessories, department colour and badge. Walk animation with planted feet.
- **Controls:** tap to walk to a spot or object, press and hold to walk toward your finger, tap a person to talk. Walk into the lift car (or tap a lift door) and press the panel on its back wall to choose one of the six decks. Doors slide open for anyone nearby; sealed rooms give tap text.
- Crawlways get low ceilings and a crouch-walk.
- **UI to come:** wrist comm with the job list, machine inspection panel, a two-slot carry indicator, and watch tools (time speed, crew panel, systems panel).


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
   - the ship clock (30-minute days), calendar, rota and days off;
   - sleeping skips to morning;
   - the 75-crew roster as data;
   - crew moving through their schedules on decks the player isn't on;
   - crew drawn on the current deck walking their real schedule, with daily variety;
   - watch tools: time speed, crew panel, systems panel.
   - Test: watch a full ship day and check it feels alive.
2. **Ship systems and jobs:**
   - systems with condition and wear, and their dependencies;
   - consequences in stages: machine effects on crew needs and mood, and uniforms and the laundry;
   - the job board, parts and carts;
   - crew and player tending the ship, with the player's tools: wrist comm, inspect, two-slot carry, repair;
   - the ship health board on the bridge and in the Works bay.
3. **Social:**
   - relationship meters and talking;
   - crew seeking the player out;
   - gossip from the ship simulation and from crew lives;
   - crew relationships with each other, and crew remembering who helped;
   - the first story crew arcs.
4. **Events:** the event framework, then the ion storm, then more events.

**After that:** progression to tier 2 (certification, promotion to Officer and your own cabin, the Deck 5 machine rooms and connected-system faults); the spine's crawlways and pipe galleries, with the crouch-walk; and the shuttle arrival, if not built earlier.


## Open questions

**The game:**

- Who is the Works Chief? Name, personality and how they judge your work. They live on Deck 2 and work from the glass office on Deck 5. Needed before Pillar 2, because they run the job board and certify the player.
- Who meets you off the shuttle, and which milestone builds the arrival?
- Should the player ever work the night shift, for example as part of on-call duty?
- How does diagnosing a fault look on screen: a simple panel with labelled components, or something more hands-on? Prototype it in Pillar 2.
- Can the player be passed over for certification, or only delayed?
- Should the player customise or shape their character at the start?
- Which event comes after the ion storm?
- Does the diplomacy-and-story starship game become its own future project?

**The decks:**

- How often do Deck 4's guests change? Decide when the crew roster is built (Pillar 1).
- Deck 2's fifteenth bedroom is a second visitors' cabin for now. Keep it, or make it a senior lounge?
- Who keeps the engine watch on Deck 6: is there a watch on both shifts, and are they Works crew?
- Should one of Deck 6's power junctions open at tier 2 rather than tier 3?

**Answered:**

- The player starts in Bunk 1 with Tomas, and Pell and Rina are in Bunk 2 (answered since v3).
- A ship day lasts 30 real minutes (the old guess was 10, and a working shift needed more). This sets every wear rate.
- What triggers the first story events: ship-wide events are the main missions, about one every 1–2 ship weeks, starting with the ion storm (see "Ship-wide events").
- Decks 6 and 1 are reachable by lift from day one; locking by tier or story comes later.
- The bridge's sunken command ring is faked for now with a rail, a painted step edge and a curved step strip.
- The bridge washroom stays.
- Deck 2's six senior officers are confirmed (Second Officer, Senior Helm Officer, Ship's Counsellor, Comms Chief, Deputy Survey Chief, Senior Watch Officer), moved up from Deck 4's officers. The six cabins they leave on Deck 4 become guest cabins, so the deck stays lived-in (agreed 2026-10-15).
- Deck 4's guest cabins are the six nearest the lift: 4-01, 4-02, 4-03 and 4-04 (the first column, two with windows) and the inner pair 4-07 and 4-08, so guests don't walk the corridor and officers keep 10 of the 12 window cabins. The two spares are 4-23 and 4-24, the inner pair at the music-room end. Guest cabins never use bunks (built in 0.14.0).
