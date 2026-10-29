# Backlog before 1.0: the user's answers (final list)

From the user's answers on the "Backlog before 1.0" page (https://claude.ai/artifact/FVcaELmHkiq2hHCQp6defE, saved 2026-10-29 from 01:38 UTC; 44 answers, one for every A and B item). BT1, read straight from the page's store. The triage itself is `plans/backlog-triage.html` (0.96.0, fe11cd66). The user: through 1.0 only; the C (after 1.0) and D (already fixed) groups are left alone. **No action on the game yet.**

On the page, "Agree" means do it in the version shown. **"Close it" (stored as "D") means drop the item: don't do it.**

## Open question for the user first

Two items the user closed (dropped) here are the two long-standing check failures that the user asked, an hour earlier, to have fixed in 0.98 (plans/roadmap-1.0.md):

- **12**: a very busy player reaches "Relied on" on Day 4 (career_check).
- **FX24-2**: Farouk misses the Day 7 reading corner because the planner gives no walking time inside a deck (events_check).

The two answers conflict. Ask the user which one stands before 0.98 starts. If they are dropped, the two failures stay on the known-old list. The two 0.98 walk-time items below (FX12-1, TQ1-1) were grouped "with FX24-2"; they can be done on their own, but the planner's walking time is the same estimate, so a fix for them may cure FX24-2 too.

## 0.98 (game speed on phones)

| Item | What | User's note |
|---|---|---|
| FX12-1 | Crew reach evening gatherings 15 to 20 ship minutes after their plan, because the walk takes longer than the planner allows. | |
| TQ1-1 | Crew stand in the toilet queue while the toilet is empty, because they set off much too early (the walk estimate is too long here). | |
| SD3-2 | The sound update works out which music to play four times a second; it could remember the answer instead. | |
| (12, FX24-2) | The two check failures: see the open question above. | closed by the user on the page |

## 0.99 (balance)

| Item | What | User's note |
|---|---|---|
| 22 | Galley cookers break down every few days; two at once make dinner queues of about half an hour. | "Just explain with a message (small bottom screen type)": leave how often they break as it is, and tell the player with a small toast why dinner is late. |

## 1.0 (the last playtest patch)

| Item | What | User's note |
|---|---|---|
| FX17-1 | The talent night card ("do an act?") closes by itself within a ship minute, before you can choose. | |
| N6-1 | A saved game whose career ended (let go) won't start when loaded. | |
| PB1-1 | Tapping the birthday cake sits you at the table instead of giving you a slice. | |
| TM-1 | A "Tonight?" invitation Mail can show a line of program code instead of words. | |
| DV1-3 | A repair whose part is out of stock and can't be made: the arrow just says "Look over the machine". | |
| DV1-1 | A cart delivery got stuck on "Pick up a hover cart for 1 crate" (Deck 3) for 45+ ship minutes; look first whether it still happens. | |
| DV1-2 | A team job got stuck on "brace the housing"; probably fixed with MA6-1, so confirm with one run, then close. | |
| 15 | Envoy Saruth can't be talked to with "Talk a while", so Saruth's four written talks are never heard. | |
| CP5-1 | Pop-up messages aren't read out by screen readers for touch and mouse players. | |
| 30 | The arrow keeps saying "Clock in" for up to a ship minute after you've clocked in. | |
| 31 | Stopping tracking by hand doesn't bring your job's arrow back. | |
| JB1-1 | The same extra job can come up on the board twice in one day. | |
| FX3-1 | While a head-scratcher waits for your decision, the arrow says "Repair the machine" and nothing points to Fault notes. | |
| FX3-2 | The "make a part" arrow always points at the first lathe, even when it's taken and the second is free. | |
| FX10-1 | "Job taken" says "parts first, from main storage" even when the part has to be made in the machine shop. | |
| FX8-1 | A swimmer or climber leaving jumps up to about five tiles in one frame. | |
| FX21-1 | Crew make chatter bubbles in the middle of a conversation card or meeting. | |
| RV18-C1 | At the comet viewing, the bedtime arrow can hide the arrow to Saruth's knot. | |
| RV18-C2 | At the comet viewing, a speaker on their own can repeat their line. | |
| RV18-D1 | In the "every door needs a tap" setting, the door hint says "A private room" at public doors too. | |
| EV1-1 | During the visit a reputation pop-up may show twice (unconfirmed: watch for it, fix if seen). | |
| SD3-1 | A room's door chime forgets it has rung after a reload, and a crew member opening the door counts as you. | |
| V-1 | A seated formal dinner on the visit's Thursday (today it's an ordinary galley meal). | "Formal dinner dont worry about dev mode": build the dinner; no Dev mode jump for it needed. |
| V-2 | The Veyli vessel's words mention the visit two weeks before. | |
| RV23-2 | The follower's arrow showed "Clock in: shift at 09:00" from 16:03 the day before (Day 32), and "air plant, Deck 5" hung on Day 31. | |
| RV23-3 | The heads-up "Put Taavek's sketch on your shelf is starting" reads like an event, not a to-do. | |

## Dropped by the user ("Close it")

| Item | What |
|---|---|
| 12 | Busy player "Relied on" by Day 4 (career_check): **conflicts with the 0.98 plan, see above** |
| FX24-2 | Farouk misses the Day 7 reading corner (events_check): **conflicts with the 0.98 plan, see above** |
| 28 | A slow door on Deck 3's corridor holds walkers up for several minutes |
| BAL-1 | A late Specialist's Calder question still says "Four weeks aboard" |
| BAL-2 | No fallback for a player who never reaches the top tier (no badge, move, question or ending) |
| EV1-2 | A Senior gets few random head-scratchers on Days 16 to 22 |
| 1 | The device app tiles' two lost style rules (icon size, label wrapping) |
| 5 | The Tracked panel fills a 320-pixel phone screen |
| 6 | The tip card sits over the needs strip and Tracked on phones |
| CP5-2 | The left-hand one-handed controller layout has no zoom |
| LD1-1 | The Deck 5 lift brake takes taps meant for the ladder |
| DM1-4 | Dev mode: Set career Day 16 tells a Senior "Tier 3 test tomorrow" |
| DM1-5 | Dev mode: an Engine Specialist is told about lift roof training on Days 27 to 29 |
| DM2-1 | Dev mode: after "End and keep", the event's routines run to its calendar end |

Counts: 30 to do (0.98: 3, 0.99: 1, 1.0: 26), 14 dropped (2 of them waiting on the open question). The backlog's C and D groups were not answered and stay as they are.
