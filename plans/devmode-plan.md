# Dev mode plan: summary (version 1)

Dev mode planner DP1, 2026-10-20. Branch `claude/devmode-plan`, based on `claude/integration` (0.64.2 + step 2). The full page is `plans/devmode-plan.html`. Planning only: the game is unchanged.

## What it is
- **A hidden testing panel**, opened with `#dev` in the game's link. Without it, Dev mode doesn't exist in the game: no chip, no panel, no code running. Proof each turn: cadet_test ALL IDENTICAL.
- **Its own save:** the two storage names (`starship-cadet-save`, `starship-cadet-arrived`) get "-dev" added in Dev mode. The real save is never touched, and devmode_check proves it byte for byte.
- **It doesn't use `nosave`**, because that also switches off the arrival and the clothes.
- **Always labelled:** a gold DEV chip under the clock. Anything set by hand is marked in the Dev save.
- **The panel:** a bottom sheet at phone size (on the right in landscape), with five tabs: **Clock, Career, Traditions, Jump, Events**. Sketches are on the page.

## The five functions (the user's asks)
1. **Clock.** Moves time forward: +1 h, +3 h, to 17:00, to 21:40, next morning, +1 day, +7 days, or to a chosen time.
   - Two ways: "Skip (like sleeping)" is `skipTo`, where a skipped workday is a missed shift; "Play it steady" has the steady player work the hours.
   - It runs in 30-minute steps, a day at a time, with a progress bar.
   - Whatever's mid-flight is settled first (a conversation ends with its gist in Mail, an activity stops, a game closes). It refuses during a lift ride or sleep.
2. **Career.** Shows and sets your xp, band, trainings, tools, ship reputation and rank.
   - "Start promotion now" sets the real Tier 2 test for today (24p's test day), and "Next step" moves the clock to each beat, up to the ceremony.
   - Setting the rank directly is offered but marked approximate.
   - Later ranks appear when Steps 5-6 add them.
3. **Traditions.** Lists all 60, with search.
   - Start one in 20 minutes, at its usual time, or tomorrow, with its Mail if wanted.
   - It works through a Dev list read by one line in `eventsOn`; today's and later plans are then made again, as `eventOneOff` already does.
   - Handled cases: honorees (birthdays, rotations), flag-gated traditions, fixed hours, and refused during a storm.
4. **Jump to a day** (0-30, with milestone shortcuts). A new game in the Dev save; the steady player is replayed up to that day; then you're loaded in through the normal "open a save" path at 06:00, in your bed.
5. **Events** (events plan F6).
   - Start any ship-wide event, even the switched-off visit (in Dev mode only).
   - Start at a phase: the earlier phases pass as if slept through.
   - Threads live, with − and +, the bands and your part.
   - "End now" goes through the event's own ending (score, traces, log, debrief, commendation).
   - Phase jumps are only reliable after the events plan's F4; until then the panel says so.

## The day jump: recommended (a) replay + kept days
| | (a) replay | (b) shipped snapshots | (c) synthetic |
|---|---|---|---|
| Exact | yes (the game's own code; the same twice) | only for the build it was made with | no |
| Speed | ~8 s to Day 10, ~19 s to Day 26 | instant | instant |
| Upkeep | one steady-player script | rebuilt every build; ~118 KB a day, so +70% on the 5.1 MB file | rules kept by hand |

**Kept days:** the replay keeps a few days' saves (0, 5, 10, 15, 20, 25 and the last, ~0.8 MB) in the Dev save, stamped with the build. That makes repeat jumps instant, and they're thrown away when the build changes.

**Measured** on the shared branch (headless Chromium, 4 cores, 30-minute steps, page load not counted):

| Run | To Day 10 | To Day 26 |
|---|---|---|
| 30-minute steps | 7.5-8.1 s | 18.9-20.5 s |
| 10-minute steps | | 37.5 s |
| 60-minute steps | | 13.9 s |
| CPU slowed 4× (phone stand-in) | 40.4 s | 101.9 s |

- The same replay twice gave identical save fingerprints.
- The save on Day 26 is 118 KB.
- A plain 10-day skip takes 3.0 s.

**The finding that sizes the work:** my quick steady player was still a Junior Technician on Day 26.
- It never answered the incident call that "Making it safe" (m6) needs, so the Tier 2 test never opened.
- Its xp also depended on the step size (170, 234 and 292 at 60, 30 and 10 minutes).
- The checks each have only a part of a player: career_check's uses stand-in trainings, arc_check's does friendships, events_check goes to traditions.
- So **Dev mode needs one shared steady player, `DEV_PLAYER`**: a line per part of the game, each added by that part's owner. devmode_check proves the milestones (Officer on Day 10 today).

**Honest about believability:**
- Exact: the career, machines, jobs, galley, Mail, events, traditions and news.
- Exact for the steady player's choices: friendships.
- Approximate (marked): your needs, clothes, what you carry and where you stand.

## Turns (about 8-10) and stops
| Turn | Work |
|---|---|
| D1 | The switch, the Dev save, the chip and panel shell, section 25 and its slot |
| D2 | Clock |
| D3 | Career |
| D4 | Traditions |
| D5 | The steady player's table and its first lines |
| D6 | Each career part's line |
| D7 | Jump, kept days, phone speed |
| D8 | Events (F6) |
| D9-D10 | Fixes |

- **Stop 1** after D4, **Stop 2** after D7, **Stop 3** after D8. Each stop is a published Dev build with phone-size screenshots.
- **Every turn:** cadet_test ALL IDENTICAL, the area's checks, check_fast, and the new devmode_check.py (the real save untouched; nothing without `#dev`; jumps repeatable; tradition and event runs).

**Hooks in other sections** (one or two lines each, owner-reviewed; no shared function changes):
- 13 (`DEV`, `SAVE_KEY`)
- 21 (`INTRO_KEY`, and `introWanted`'s own copy of the string)
- 18 (`eventsOn` reads the Dev list)
- 24p (set today as the test day)
- each career part's steady-player line
- the page's CSS

## Questions for the user (answer slots dm-q1 to dm-q10, plus dm-general)
1. How is it opened? **Recommended: `#dev` in the link.**
2. How does it save? **Recommended: its own save** (not "no saving").
3. How does the day jump work? **Recommended: (a) replay + kept days.**
4. Which players can you jump as? **Recommended: steady now; busy and lazy later.**
5. What happens to your shift when the clock moves over a workday? **Recommended: two buttons, "Play it steady" and "Skip" (missed, as in the game).**
6. Does a jump include the arrival evening? **Recommended: yes.**
7. A tradition started today: how does it look? **Recommended: today, with the deck refreshing under the lift's fade.**
8. Set the rank directly? **Recommended: yes, marked approximate.**
9. How often to review? **Recommended: three stops.**
10. Keep Dev mode in published builds? **Recommended: yes, hidden behind `#dev`.**
