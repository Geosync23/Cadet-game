# Crew stories: build notes (game-side changes, for when they're built)

Kept by CS1 (the crew stories lead). **Nothing here goes into the game file now** (the user's rule: writing first,
built after the playtest). The stories are in `content/arcs/` (outlines in `content/arcs/outlines.md`, "Crew stories";
decisions in design-doc.md, Social life, "Crew stories"). Each item says who owns the part of the game it touches.

## 1. Roster text that the stories contradict (section 9, the crew designer's; proposed wording)

| Person | Field | Now | Proposed | Why |
| --- | --- | --- | --- | --- |
| halloran-emeka | about, tier 3, home | "Someone in the family has been unwell, and the news comes slowly." | "Tells one of his late dad's jokes every breakfast, from a numbered book in his pocket." | the user's no-illness rule; his story (the jokes were his late dad's) |
| teague-theo | about, tier 3, work | "Reads the transfer lists every week." | "Moved stations eight times before he was fourteen, and draws everyone in his first week." | no transfer lists in his story (Tomas's and Zeke's have them); his reason |
| teague-theo | about, tier 4, secret | "Isn't sure whether to stay on the Wren, and changes their mind daily." | "Likes the Wren more than any station he's lived on, which is exactly why he's going." | his papers are signed: he leaves on Day 21 |
| kowalczyk | about, tier 1, home | "Grew up on Marra Station, where her father kept a beacon." | "Grew up on Marra Station, where her father still keeps the beacon." | the beacon is switched off during her story |
| all six new story people | `thread` | teague-theo `leaving`, bramwell-basil `homesick`, halloran-emeka `family`, salo-saad `notgood`, raman `leaving`, kowalczyk `lonely` | `arc:teague`, `arc:bramwell`, `arc:halloran`, `arc:salo`, `arc:raman`, `arc:kowalczyk` | so nobody plays both a theme and a story |

Zeke's father: no roster text mentions him. content/facts.md is fixed (well, retiring; no memory loss).

## 2. Small new code pieces (section 20c, social stories; and section 22, lines)

1. **Per-line conditions in .arc files.** The writers marked them `// IF <conditions>: <speaker>: <text>` (Pell 7,
   Zeke 6, Theo 5, Halloran 5, Calder 5 and more). The dialogue engineer adds a real per-line condition to the arc
   grammar, then the comments become lines.
2. **Day gates:** a `day:` condition (from / until / exact), from the `// DAY:` comments.
3. **The crescendo hook:** when you're at the named gathering and the story is ready, its crescendo beat plays there,
   with the people already there (no crew re-planned). Reads the `// CRESCENDO rides on:` comments. A Calendar entry and
   a Mail the evening before a ready crescendo.
4. **The quiet-ending rule:** when a crescendo's window passes unplayed, its `// QUIET ENDING` beat becomes the next one.
   At most one crescendo a day.
5. **New favours** (social's `STORY_FAVOURS`): `theoCloud` (carry a page to Calder's glass office), `basilPlant` (a
   plant to the garden and back, two days), `emekaJokes` (three short stops: Yoon, Lemaire, Yilmaz; sets
   `flag:halloran.jokes.done` when done: a new favour shape, three stops), `ramanPin` (a stop at the machine shop bench).
6. **Theo's goodbye:** his crescendo (teague 5) is his goodbye; skip his ordinary goodbye moment once it's told.

## 3. Things the stories wait for (other owners)

| Story | Waits for | Owner |
| --- | --- | --- |
| Calder 5 | Calder's question, Day 26 (Pillar 5 career meeting): the crescendo plays just before her question | Pillar 5 |
| Zeke 6 | Engine Specialist (Pillar 5): one IF line "if you were made Engine Specialist today" | Pillar 5 |
| Kowalczyk 2-4 | your night shift, now Mon-Wed Days 22-24, 21:00-06:00 (comet/visit plan); the crescendo on the bridge at 05:50 on Day 24 | Pillar 5; the bridge (Deck 1) |
| Salo 4 | the ion storm (built): a crisis moment on Deck 6 on Saturday Day 13; Calder's comm line | storm owner (only to agree) |
| Raman 5 | comet viewing, Day 16 (EP2's plan): the observatory's back window 22:10-22:40; Bakshi on the night helm then (rota check) | events (EP2) |
| Kovac 4 | the Deck 5 lift lobby before the Friday address (15:35-15:45): a scene at the doors, no lift code | lift / Fridays owner (only to agree) |
| Theo 5 | the Day 21 send-off in the shuttle bay (built) | rotation (built) |
| Basil 1-4 | his arrival off the Tern (built), Name on the beam Day 22 (built), his new hand's tea Day 25 (built); his voice card (SW2) | rotation (built) |

## 4. Content outside the story files (done, or to note)

- `content/lines/kovac-zainab.lines`: the joy line changed from a scarf to the spanner grip and re-gated on
  `mem:moment.kovac.grip` (SW1, claude/stories-sw1 564472fd). The callback under `? told:moment.kovac.tellclub` no longer fires (the club is together at
  the doors in the new crescendo); harmless, left in place.
- `content/facts.md`: the new canon rows (CS1, done).
