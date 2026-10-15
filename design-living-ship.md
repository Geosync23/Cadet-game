# Starship Cadet: The Living Ship

Design addendum to design doc v4, agreed with the user on 2026-10-15. Where this file and v4 differ, this file wins. It defines the next big phase: crew and simulation, built as one.

## The heart of the game

The CSV Wren is a living ship. Its systems have needs and wear down. Its 75 crew have needs, routines and relationships, and part of their routine is tending the ship. The player is one more pair of hands: just another crew member, never in command.

When the crew keep up, the ship hums. When they fall behind, or the player skips their jobs, it shows. It works like a city game, seen from the inside by one worker.

## Ground rules

- **No fail state.** A neglected ship gets shabby, uncomfortable and talked about. It is never lost. Losing would break the feeling of being just another crew member.
- **The player climbs but never commands.** They start on simple jobs (filters, lamps, carts), then move up to the engines and eventually sit in briefings with the Captain. Rank decides which jobs and which parts of an event reach the player.
- **A ship day lasts 30 real minutes.** One ship hour is 75 real seconds, and a 7-day ship week is about 3½ hours of play.
- **The ship doesn't run while the game is closed.** Time stops when you leave and resumes where you were.
- **Sleeping skips time.** When the player sleeps, time skips to morning. The player's own needs (hunger, rest, hygiene) stay as in v4.
- **All 75 crew are in the simulation:** about 60 on days and 15 on nights.

## 1. Crew routines with variety

No crew member does exactly the same thing at the same time every day. Variety comes in layers:

1. **Rota.** A 7-day ship week with staggered days off, so a different crowd is at breakfast each day. Some crew move between day and night shifts every few weeks.
2. **The shape of each day.** Each day of the week runs a little differently. For example: drills one day, maintenance inspections another, and on the rest day a late breakfast, a busy gym and a film in the lounge.
3. **Time jitter.** Small daily offsets for everyone, such as waking 5–25 ship minutes early or late, or lingering at dinner. The offsets come from a seed per person per day, so they look random but replay the same way. That keeps saves and tests reliable.
4. **Habits.** Personal quirks: an early riser, someone who always takes the window seat, someone who skips breakfast, someone who calls home on rest days.
5. **Needs drive choices.** Hunger, tiredness and wanting company make crew choose between a few options instead of following a script.
6. **Interruptions.** Faults and events pull crew off their routine. This is how the ship simulation reaches daily life.

*Example:* on Monday Pell has breakfast at 07:40, then goes to the Works bay. On Thursday it's breakfast at 07:10, then drills. On a rest day Pell sleeps in, goes to the gym, then the garden, and gets called away to a scrubber fault one evening.

**Crew on other decks.** Only one deck is loaded at a time. Crew elsewhere are simulated "on paper": they move through their schedules as data and are drawn only when the player is on their deck. Arriving on a deck shows everyone where their schedule puts them.

## 2. The ship's systems

- **Systems:** air, water, power, heat, food, waste and laundry, hull, comms and sensors, and propulsion.
- **Condition:** each system has a score from 0 to 100 that wears down with use and time. Each is made of parts that can fail, such as filters, pumps, relays and seals.
- **Dependencies:**
  - Power feeds everything.
  - Water feeds the garden, and the garden feeds the galley.
  - Air needs scrubbers, and scrubbers need filters from the Deck 5 hold.
- **Ship health** is a blend of all the systems. It shows on a status board on the bridge and in the Works bay.

**Consequences come in stages, and you can see them:**

| Stage | Examples |
| --- | --- |
| Minor | A flickering lamp, a dripping pipe, a filter-due light |
| Noticeable | Weak showers on Deck 4, a warm stuffy deck, dim garden lights, an empty grab-and-go shelf |
| Serious | Alarms, a room sealed off, crew rerouting, crew mood dropping |

**Recovery is visible too.** Lights steady, plants perk up and the mess fills again.

**Jobs.**
1. Wear generates jobs, which go onto the Works bay job board.
2. Crew with the right skills claim them.
3. They fetch parts, using hover carts from the Deck 5 hold for supplies, walk to the fault and fix it.
4. The player gets the skilled or interesting jobs for their rank. Routine jobs get done by the crew if the player leaves them, but more slowly.

## 3. Social systems

**Relationships with the player.** Every crew member has a relationship meter with five tiers: stranger, acquaintance, colleague, friend, close friend. It doesn't decay, or decays very slowly, to keep the game cozy.

Ways it grows, biggest first:
1. Working a job together.
2. Eating together.
3. Talking: once per person per day counts, so it can't be farmed.
4. Helping with something they mentioned.

**What higher tiers unlock:**
- They greet you.
- At social time, they come and find you.
- They share news about their life (family back home, a hobby) and about the ship.
- Friends cover a job, tip you off about spare parts, and put in a good word with the Works Chief toward promotion.

**Gossip is a hint system.** Crew news comes partly from the ship simulation: "The scrubbers on 4 have been rattling all week." "Brennan's furious, the cold store's warm again." The social system quietly tells the player what the ship needs. News is built from sentence templates filled in with what's actually happening; no AI writing is needed.

**Crew relationships with each other.** Crew form friendships and rivalries among themselves. These shape who sits together, who swaps shifts and who avoids whom, so the player can stumble into their dramas.

**Romance** is out for now.

## 4. Ship-wide events (main missions)

Story arrives without stopping daily life, like a TNG episode where a phenomenon or entity changes life aboard for a while.

**An event is a layer on top of normal life.** For a few days it changes the ship's systems, the crew's routines and what the decks look like, and it adds its own jobs to the board.

**Structure:** onset, then escalation, then resolution, over 2–4 ship days. Every event resolves. How well it goes decides:
- ship health afterwards;
- relationship gains;
- commendations toward promotion;
- small permanent traces, such as a scorch mark, a plaque or a new pet.

**Pacing:** roughly one main event every 1–2 ship weeks (3½–7 real hours), with small incidents most days.

**What the player sees depends on rank.** A junior carries filters during the storm. A senior is in the Captain's briefing about it.

**Event ideas:**
- **Ion storm** (the first to build, because it touches every system): power flickers and comms go down. The bridge runs double shifts and the mess goes quiet.
- **Diplomatic visit:** Envoy Saruth's delegation fills the visitor cabins. Formal dinners in the Captain's quarters stretch the galley.
- **Something in the garden:** a creature eats the crops, food quality drops, and the hunt involves half the ship.
- **Shipboard illness:** the infirmary fills and sick crew stay in their bunks. Fewer hands means more work for everyone.
- **Nebula drift:** the sensor array is overloaded, and strange dreams leave the crew sleepy and chatty.
- **The déjà vu day:** a time anomaly replays the same day. Seeded routines make this cheap to build.
- **Salvage:** a derelict is found. The shuttle Tern goes out and the cargo hold fills with odd finds.

## The crew: 75 people

- **About 10 story crew,** fully written, each with a story arc that opens up as the player gets closer to them:
  - Captain Odile Marrow
  - Commander Teo Vance
  - Dr. Imra Sato
  - Chief Bram Holt
  - Tomas Lind
  - Pell Okafor
  - Chef Auda Brennan
  - Rina Deshi
  - Envoy Saruth
  - the Works Chief (still to be named and designed)
- **About 65 generated crew.** Each comes from a template: role, home deck, shift, habits, a couple of personality traits, and a few life details for gossip.

## How the phase is built

The phase has four pillars. Each pillar ends with something playable and is reviewed before the next begins.

1. **Foundation:**
   - the ship clock (30-minute days), calendar, rota and days off;
   - sleeping skips to morning;
   - the 75-crew roster as data;
   - crew moving through their schedules on decks the player isn't on;
   - crew drawn on the current deck walking their real schedule, with daily variety.
2. **Ship systems and jobs:**
   - systems with condition and wear, and their dependencies;
   - consequences in stages;
   - the job board, parts and carts;
   - crew and player tending the ship;
   - the ship health board on the bridge and in the Works bay.
3. **Social:**
   - relationship meters and talking;
   - crew seeking the player out;
   - gossip from the ship simulation and from crew lives;
   - crew relationships with each other;
   - the first story crew arcs.
4. **Events:** the event framework, then the ion storm, then more events.

## Still open

- Who is the Works Chief? Needed before Pillar 2, because they run the job board and certify the player.
- Should the player ever work the night shift?
- How does diagnosing a fault look on screen? Prototype it in Pillar 2.
- Does the player shape their character at the start?
- Which event comes after the ion storm?
