# The answers pass (overnight, 2026-10-16)

The user answered the team's 39 handover questions (the question board, https://claude.ai/artifact/KPFb1CUhz6vrXTaNBvs6sh; answers summarised below) and gave the lead sole authority to interpret them. This pass builds the answers that fit now, plus the user's new tweaks to time and needs. Bigger items go into the Pillar 3 plan. Read with `design-doc.md`, `TEAM.md`, your role's `plans/handover-<role>.md`, and `DEV_NOTES.md`.

Combined builds: **0.41.0, 0.41.1, ...** on `claude/ship-integration` (the lead). Helpers keep their branches and build ranges (next numbers below). Same rules as Pillar 2: your own sections only, shared changes minimal and inert, report each push to the lead, run the checks one at a time.

## The user's new tweaks (decided)

1. **Time.** 18 ship hours take 30 real minutes: `SHIP_RATE = 1080 / 1800` (0.6 ship minutes a second; a whole 24-hour day is 40 real minutes). Every check that assumes 0.8 must be updated. Owner: sim engineer (section 13), with every check owner updating their check.
2. **Long days.** A rested player can stay up **16 to 18 ship hours** before energy runs low (energy drains from 100 to the tired line in about 17 hours at average fitness). Owner: player engineer.
3. **Going to bed skips the night automatically.** Getting into your bunk (from 20:00) fades out and wakes you at 06:00, no dialog; tapping the bunk earlier in the day says it's too early to sleep. Crew catch up as now (`sleepUntil`). Owner: player engineer, with the sim engineer.
4. **Needs give bonuses as well as penalties.** High (75 and over) gives a bonus, low (under 25) a penalty, in between nothing. The lead's starting table, for the player engineer to tune and record in DEV_NOTES:

   | Need | High (≥ 75) | Low (< 25) |
   | --- | --- | --- |
   | Energy | tasks 15% faster (repairs, making parts, activities) | walk 80% (as now) |
   | Fitness | energy drains 15% slower; walk 105% | walk 80% (as now), energy drains 15% faster |
   | Hunger (fed) | energy drains 10% slower | tasks 15% slower |
   | Hygiene | chatting gives 50% more social | chatting gives half; crew may remark on it |
   | Social | tasks 10% faster (a good mood) | energy drains 10% faster |

   Effects stack by multiplying. The device shows a small up or down mark beside a need that is giving a bonus or a penalty, with a one-line reason.
5. **Machine trouble and the player** (unanswered): keep the current rule; faulty machines slow only the crew.

## Answers built tonight

| # | Answer | What it means here | Owner |
| --- | --- | --- | --- |
| 1 | Faults you meet: yes, balanced ("enough work, not overwhelming") | Tune Works crew so roughly 3 to 6 jobs a day are left for the player on day shift: crew take only urgent and big jobs straight away, small ones wait a few hours. machine_check reports "jobs left for the player". | Systems |
| 2 | Faults shown on the decks: yes | Visible signs on machines and rooms: flickering lights, drips, weak shower spray, wilting plants, warm-red glow on a failing panel. A "Ship health" board on the bridge (Deck 1) and in the Works bay (Deck 5) listing systems and their condition. | Systems (data, hook `machineLook(id)`), architects (boards), performance (effects) |
| 3 | Wear on machines: yes | Same hook: worn machines dim their screens, failing ones blink red. | as 2 |
| 4 | Tier locks: yes | Utility rooms by tier: closets Tier 1, plant rooms Tier 2, batteries and junctions Tier 3, through `hatchPassable`. The player is Tier 1 for now (a Works junior). | Deck 6 architect (tags), systems (rule) |
| 5 | Tap a machine: yes, and it should operate the machine if tied to a system | Tapping a machine shows a line about it and its condition, and where it has a use (a washer, an oven, a lift call panel, the lights, a fan), starts it: the machine runs, its use counts toward wear, the system responds. | Systems (rule), player (tap), architects (texts) |
| 6 | Supplies short: no story beat, but simulated, and the game must tell you | Shortages happen from the numbers (late delivery, high use). They arrive as messages in the device's **Mail** tab (a simple inbox now; the full device is Pillar 3). | Systems (events), player (Mail tab) |
| 7 | Food spoils when the chiller fails: yes | Cold-store meals spoil at a rate tied to the chiller's condition; spoiled food is binned and noted in Mail. | Galley, systems |
| 8 | Push the food cart yourself: yes | A player job: take the cart run from the job board. | Systems, player |
| 9 | Help in the galley: no | Nothing. | — |
| 10 | Menus: yes | A menu cycle with crew favourites, Friday treat, and a Sunday dinner the crew voted for (shown on the galley board). | Galley |
| 11 | More queues: yes | Queues form more often: busier serving windows, the odd slow oven, a rush after shift change. | Galley, sim |
| 12 | Grab shelf binned overnight: no | Nothing. | — |
| 13 | Lunch: no | Nothing. | — |
| 14 | Social from chatting and eating with company: yes | Talking to crew and eating at a table with others raise social. | Player |
| 15 | Shopping buys things: yes | The store sells snacks (a little hunger) and small comforts (a little social, kept in your locker). Credits are a simple balance on the device. | Player |
| 16 | Crew feelings on tap: yes | The tap toast adds a line like "Tomas looks tired". | Sim |
| 17 | Birthdays: yes | Each crew member has a birthday (about one a week); the galley bakes a cake, the mess gathers after dinner, Mail tells you. | Crew designer (dates), galley (cake), sim (gathering) |
| 18 | Habits change over time: yes | Small, slow changes: a junior takes up running, someone drops the bar. A few per month, logged. | Sim, crew designer |
| 19 | Store open every day: no | Nothing. | — |
| 20 | Gym slot or equipment: no ("more later") | Nothing now. | — |
| 21 | Window seats: yes | Architects mark seats by windows (`window: true`); the habit uses them. | All architects, sim |
| 22 | Ship health affects crew mood visibly: yes | Crew mood dips with poor ship health; shown in the tap line ("grumbling about the showers"). Pillar 3 builds on it. | Sim, systems |
| 23 | Crew carry more things: yes | Trays in the mess, toolboxes for Works crew on jobs, datapads for officers. | Performance, sim |
| 24 | Liven up Deck 1: yes | A shift handover at the command ring at 06:00 and 18:00, and the Captain's evening walk through the observation room. | Bridge architect (places), sim |
| 25 | Observatory night: yes | One evening a week, off-duty crew gather in the Deck 2 observatory. | Command architect (places), sim |
| 26 | Ready room, officers' quarters, meetings: yes, eventually | Progression: Pillar 3 plan. Tonight nothing changes in play. | Pillar 3 |
| 27 | Officers' names on door plates: yes, any officers | Every officer's door plate shows their name and rank, on Decks 2 and 4. | Command architect, Deck 6 architect |
| 28 | Visitors' cabin into a lounge: no (needed for ship-wide event visitors) | Nothing; noted for events. | — |
| 29 | Crouch through crawlways: yes | Crawlway tiles slow you to a crouch-walk with a crouch pose. | Player, performance, architects (tag tiles) |
| 30 | Cargo hatch to the shuttle bay: yes | Open it (passable for Works crew and the player). | Deck 6 architect |
| 31 | Lived-in touches in utility rooms: yes | A radio in the heating plant, a mug on a cabinet, signs, a calendar. | All architects |
| 32 | Names approved | Drop "provisional" everywhere. | Crew designer, lead (design doc) |
| 33 | Smooth hull stripes Decks 3–5: yes | `byFace` on Decks 3, 4, 5. | Bridge (3), Deck 6 architect (4, 5) |
| 34 | Real phone test: yes | Needs the user. A test checklist goes in the morning report. | Lead |
| 35 | Crowds over 70: yes (ship-wide events) | A third, coarse level of detail for distant crew; a `?crowd=120` demo. | Performance |
| 36 | Ship runs while closed: no | Nothing. | — |
| 37 | Device: its own large pass | Pillar 3. Tonight only the Mail tab and the bonus marks. | — |

## Who does what (next build numbers)

| Role | Session | Branch | Next builds |
| --- | --- | --- | --- |
| Sim engineer (standby) | session_01S5xTHRBpJ9kqytfrwKipUG | `claude/sim-engineer` | 0.26.8+ |
| Performance engineer (standby) | session_01TiBtENVFJV7RqEQ7YkxH1Z | `claude/crowd-render` | 0.27.7+ |
| Bridge architect (standby) | session_015BoZMMp5b4A4F51dMcZ3ax | `claude/deck1-scale` | 0.31.6+ |
| Crew designer (standby) | session_01JScnVG158eYAHYvKDz3jZG | `claude/deck-plans-1-2-6` | 0.16.6+ |
| Systems engineer (new) | see TEAM.md | `claude/ship-systems` | 0.33.16+ |
| Deck 6 architect (new) | see TEAM.md | `claude/deck-architect` | 0.30.11+ |
| Player engineer (new) | see TEAM.md | `claude/player-needs` | 0.28.9+ |
| Galley engineer (new) | see TEAM.md | `claude/galley-food` | 0.29.11+ |
| Command architect (new) | see TEAM.md | `claude/deck2-command` | 0.32.3+ |

## Shared formats (new)

- `SHIP_RATE = 1080 / 1800` (section 13).
- Places: optional `window: true` (a seat by a window); tiles: deck-level `crawl: ['i,j', ...]` (crouch tiles); utility rooms: `tier: 1 | 2 | 3` on each service hatch in `service`.
- `machineLook(id) -> { state: 'fine'|'worn'|'poor'|'failing', blink, dim, drip, flicker }` (section 17), read by deck dressing and effects. Inert when absent.
- `machineUse(id, who) -> { text, ran }` (section 17): what a tap on a machine does. Player section 15 calls it from the tap.
- `mailSend({ at, from, subject, body })` and `SHIP.mail` (section 15, saved through SAVE_EXTRA): the device's Mail tab. Any section may send.
- `crewMood(p, t) -> number` and `crewFeeling(p, t) -> string | null` (section 14): the tap line.
- `ROSTER[i].birthday`: a ship day of the year, 1–364 (52 weeks of 7 days, day 1 = the game's Day 1), spread so about one falls each week (section 9). `SHIP.habitLog`: the habit changes so far (section 14, saved).
- `needEffects(state) -> { walk, task, drain, socialGain, notes: [] }` (section 15): the bonus table, one place.
- Player credits: `SHIP.player.credits` (section 15).

## Order

1. Everyone starts on their table rows at once against these formats (stubs where another section isn't in yet).
2. The lead merges as pushes arrive (0.41.0, 0.41.1, ...), runs all checks, republishes the playable link.
3. End: the lead's report of design decisions, and the Pillar 3 plan pitch.
