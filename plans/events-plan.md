# Ship-wide events plan: summary (version 2)

Events planner EP1, 2026-10-20. Branch `claude/events-plan`; build 0.64.2.

The full page is `plans/events-plan.html`, with screenshots in `plans/events-plan-shots/` and the run log in `plans/events-plan-run-log.json`. Version 2 takes in reviewer ER1's review (`claude/events-plan-review`, `plans/events-plan-review.md`) and lead 20's two asks: a parked list, and answer slots for each question. This is planning only; the game is unchanged.

## When the career ends
- **Day 26 (a Friday), "Calder's question"**, from the Pillar 5 plan v11:
  - Officer on Day 10
  - Senior Officer on Day 16
  - Engine Specialist on Day 23
- **These are the earliest possible days.** A busy player can't get there sooner.
- **Day 26 is a target, not yet proven.** Pillar 5 steps 5-6 need "not before" days (the Tier 3 test on Day 15 at the earliest, the Tier 4 test on Day 22) and a reputation pace a player can actually keep.
- **Slower players:**
  - A slow player becomes Officer on Day 29.
  - A player who skips work is let go on Day 20.
- **Built today:** only the first promotion.

## In scope (recommended dates)
1. **Ion storm** (main). Built and on. Keep Days 10-15, with a career-beat guard and the commendation at the all-clear.
2. **Comet viewing** (short). Drafted. Tuesday Day 16, 21:30, one day long. Sato works weekdays only.
3. **Diplomatic visit** (main). Built, kept off. Shortened to fit:
   - warning Friday Day 19
   - greeting Monday Day 22, after the Monday briefing
   - one dinner Tuesday Day 23
   - farewell Friday Day 26

**The game's own scheduling can't produce these dates** (its rules give the comet Day 22 and the visit Day 26 or 33), so the first framework piece, F0, sets the dates directly.

## Parked for later (kept on record, never deleted)
In design order. Each full breakdown is in `plans/pillar3-plan.md` at the line given.

| Event | Kind | Line |
| --- | --- | --- |
| Crew rotation day (its traditions already run, first on Days 34-40) | short | 396 |
| Something in the garden | main | 350 |
| Power surge | short | 393 |
| Shipboard illness | main | 358 |
| Founders' Day festival | short | 392 |
| Nebula drift | main | 365 |
| Late supply shuttle | short | 395 |
| Salvage | main | 373 |
| A Veyli vessel needs help | short | 394 |
| The déjà vu day | main | 381 |

`design-doc.md` marks them parked when it's next updated.

## Storm audit (13 items, reviewer-checked)
1. It lands on the first promotion. Moving it a day only moves the clash.
2. The 89 storm lines never play: no phase note is sent.
3. Nothing the player does changes the result. Left alone it is rough every time:
   - the calls thread is a fixed sum;
   - smooth blackouts are impossible even at full power;
   - spoiled meals count from the warning;
   - prep jobs feed no thread.
4. The device's Schedule misses the meetings, Tracked offers the closed booths, and there's no status line or Record entry.
5. Skips and reloads drop phases. A jump over the whole storm comes out "smooth", and a reload loses a meeting.
6. Calls home are blocked only on the front day, and for any event.
7. `eventDay(d)` is called but doesn't exist, so the puzzle and incident guards are dead.
8. The storm is what moves film night to the rec deck, and there are two film-night flags.
9. The briefing choice can never hold a job: the jobs go up before the briefing.
10. On phones, the banner covers the HUD.
11. Rank-aware parts aren't built.
12. Too many ready-room and Captain's-table scenes.
13. Small things: placeholder code, the framed menu prop, a jolt replayed after a reload, Day 13's tradition count, a blackout reading 454 draw calls.

## Shared base F0-F8
| Piece | What it does |
| --- | --- |
| F0 | The event calendar |
| F1 | `eventDay` and the career-beat guard |
| F2 | Phase notes |
| F3 | The device |
| F4 | Safe through skips and reloads |
| F5 | Small rank parts |
| F6 | Dev mode hooks |
| F7 | One data-driven check, plus perf scenes |
| F8 | Comms down |

## Size
About 31-40 build turns, plus the head writer's lines:

| Part | Turns |
| --- | --- |
| Shared base | 12-15 |
| Storm | 8-10 |
| Comet | 2-3 |
| Visit | 9-11 |

## Order
1. Step 2
2. Dev mode
3. Pillar 5 steps 5-6
4. F0-F8
5. Storm
6. Comet
7. Visit

Each event is built switched off, tested in Dev mode, then switched on.

## Questions for the user (answer slots on the page: ids ev-q1 to ev-q9, plus ev-general)
1. **Are the storm, the comet and the visit the right three?** Recommended: yes.
2. **What should happen where the storm meets the first promotion?** Recommended: (a) keep Days 10-15 with the hours kept apart. The other options are (b) one day later, or (c) the Senior week.
3. **When is the comet?** Recommended: Tuesday Day 16, rather than Sunday Day 21.
4. **Should the visit be shortened to Days 19-26?** Recommended: yes.
5. **Should events follow the calendar or the player's rank?** Recommended: the calendar, with small rank parts.
6. **What should helping in the storm change?** Recommended: prep jobs and help move the threads; left alone it comes out bumpy, and with good help smooth.
7. **What should the rec deck do in the storm?** Recommended: unhook its first all-hands from the storm and close the rec deck from the front to the all-clear.
8. **What about the repeated scenes?** Recommended: fold them. The commendation comes at the all-clear and is mentioned on Day 16, and the Day 17 toast counts as that month's Captain's table.
9. **Who is the junior you mentor on Day 26?** Recommended: a small arrival on Day 21 using the rotation traditions.
