# Dev mode plan: summary (version 3, the lean Dev mode)

Dev mode planner DP1, 2026-10-20. Written after the user's answers (12:05) and their talk with lead 20.
- Branch `claude/devmode-plan`, based on `claude/integration` (0.64.2 + step 2).
- The full page is `plans/devmode-plan.html`.
- Version 2.1, with both reviews behind it, is in git (6c37f52).
- Planning only: the game is unchanged.

## What it is
- **Opening:** a ready Dev link (`#dev`). In Dev mode the place-and-clock card gets a gold outline and the word DEV, and tapping it opens the panel. Without the link, Dev mode doesn't exist in the game.
- **Saving:** Dev mode keeps its own save (the real save's names with "-dev" added).
  - The user answered "none" to q2. The lead's recommendation, kept here, is a separate save, because Mark, Undo and reloads need one. The user confirmed it after the talk.
  - Only three small things are stored: the save, one Mark and one Undo (about 120 KB each).
  - There's a space check before each write and a Clear button. A check proves the real save still writes and stays byte-identical.
  - No IndexedDB is needed now.

## Stops (about 9-10 turns)
- **Stop 1a, the patch kit (D1-D4):**
  - Clock: 30-minute frozen steps; workdays are **excused** (q5), through a Dev list read by `careerOff` plus one line in `careerTick`.
  - Needs kept as a normal day, plus Top up (q15), through a hook in section 15's skip step.
  - Take me to… (q14), refused during the arrival evening and inside meetings.
  - Mark / Back to mark (q14).
  - Undo my last Dev action (q11), Copy my real game, Clear.
  - The Day 2 recipe: play Day 0-1 once (or copy your real game), then Mark at Day 2 08:30. A notice appears when a skip passes a first-week meeting.
- **Stop 1b (D5):** traditions (q16 split).
  - A Dev list read by `eventsOn`; the traditions engineer reviews it first.
  - Plans are remade under the lift's fade (q7).
  - Refused on Day 0 and during a big event.
- **Stop 2, Set career (D6-D7)**, which replaces the replay:
  1. Pick a day from 0 to 30.
  2. A new Dev game starts the "Skip to Monday" way (`newGameStart(false)` + `introSkip()`, clearing `INTRO_BOOT`). Starting by shuttle would hold the clock at Day 0 17:30.
  3. The clock moves day by day with workdays excused. Each morning the career is set (both `W.tr` and `W.op`, then `promoPip()` after the rank) from a table of "what a steady player has by day N" (the ladder's days and the Pillar 5 dates: Officer 10, Senior 16, Engine Specialist 23, Calder's question 26).
  4. Set career doesn't depend on the first week's meetings (it works while the Day 2 meeting is broken): it marks the arrival week as attended (Day 1 briefing, Day 2 solo job, Settling-in, the shadow shift) before setting the career. The promotion beats are marked done, and friendships get a starting level (new question 1).
  5. You wake at 06:00 in your bed.
  - The result is marked **approximate**, and the panel's "What's set" list says what it gets wrong: thin friendships, an empty work log, no part in the storm, fresh tool wear.
  - devmode_check compares the table with `CAREER_LADDER`, and checks that Set career to Day 10 from a fresh Dev game gives a career, rank Officer and no missed-meeting Mail.
  - The Career tab (q8): the promotion test's needs with ticks; `ladderOpen` when only the day is missing (owner first); set rank marked approximate.
- **Stop 3, Big events (D8-D9):** start by day, next phase, threads with −/+, End and undo (End and keep after the events plan splits the ending out of `eventAdvance`).
- **D10:** fixes.

## Hooks (owners review first)
- **13:** `DEVMODE` read before `SAVE_KEY`; the freeze.
- **21:** `INTRO_KEY`, `introWanted`, the first-week beats' records.
- **20:** the excused list.
- **15:** needs kept.
- **18:** `eventsOn`; later, the ending split.
- **24 / 24p:** `SHIP.works` written in the shape `worksClean` keeps; `ladderOpen`.
- **page:** the card and the sheet.
- **New section 25.**

## The user's answers, now decided
| Question | Decided |
|---|---|
| q1 | the Dev link |
| q2 | own Dev save (confirmed by the user) |
| q3, q4 | parked |
| q5 | excused |
| q6 | no longer applies |
| q7 | fade |
| q8 | labelled |
| q9 | three stops |
| q10 | keep |
| q11 | Undo my last Dev action |
| q12, q13 | no longer apply |
| q14 | both |
| q15 | kept + Top up |
| q16 | split |

## New questions (dm-v3-q1..q3, plus dm-v3-general)
1. Friendships after Set career. **Recommended: a starting level with the people a steady player meets, marked approximate.**
2. Does Set career start a new Dev game or carry on? **Recommended: always new (Undo brings the old one back).**
3. Where do you wake? **Recommended: 06:00 in your bed; the beat shortcuts go on to the beat's time and place.**

## Parked: the steady-player replay
- **Status:** parked 2026-10-20 (the user's call). Its design is kept in full in v2.1 (6c37f52) and in section 7 of the page.
- **Design:** `DEV_PLAYER` with a line per career part; a fresh page, frozen, a fixed seed; first-week meetings attended in person; kept days in IndexedDB with a script fingerprint; 13-17 turns.
- **Measured** (from the Day 0 arrival, saving on, seed 1): Day 2 08:40 in 1.2-1.4 s, Day 10 in 6.3-7.3 s, Day 26 in 15.7-17.1 s, the same twice.
- **DJ1** (to be confirmed): Day 26 in ~43 s; Officer by Day 16.
- **Unpark** when approximate state isn't enough (friendships and stories, the checks).

## v3.1 (DR1's check: Set career works on a scratch copy)
- It starts with Skip to Monday, not the shuttle; first-week meetings are marked met before the skip passes them.
- `W.op` is written as well as `W.tr`; devmode_check plays Day N+1 and expects nothing re-opened.
- `INTRO_BOOT` is cleared in a new Dev save (a section 21 hook).
- The storm's briefing Mail is mentioned; the mug, seedling and Settling-in ticks are listed in "What's set".
- A one-line Dev seed is kept for byte comparisons.
- `promoPip()` is called after the rank.
- Hooks added: 20 social (`relAdd`) and 21 (`introSkip`, `INTRO_BOOT`).
