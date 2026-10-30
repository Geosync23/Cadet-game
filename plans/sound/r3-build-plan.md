# The sound update (Round 3 + the mess hall): build plan

SD2 for lead 43, 2026-10-28. Branch `claude/sound-r3` from `claude/staging-pad` e158dcff. One build, behind a new switch in section 27: `const SND_R3_ON = false;` (off: the game and its sound exactly as now; cadet_test ALL IDENTICAL, sound_check unchanged). Stays out of section 26 (controller) and section 18's visit lines (EV1).

## The approach: watch, don't hook

Section 27 already reads the game once a second (`S.actTick`) and every frame (`S.onFrame`) without changing anything. Almost every Round 3 moment can be read the same way: who's in which room, a tradition's rooms (`tradOn(id).rooms`), `eventNow()`, `dosiOut()`, a machine's `running`, `SHIP.works.rank`, `DIALOGUE.id`, the time clock's screen. So nearly all the work is inside section 27, and only five moments need a one-line `sndFx(...)` hook in another owner's section (turn 4).

## Turns

| Turn | What | Where | Estimate |
| --- | --- | --- | --- |
| 1 | **Event music.** 8 tradition tracks (Name on the beam, Cup day, Farewell supper, The goodbye, Harvest table, Lantern walk, Crossing the Line, Veyli welcome) and the farewell song B, as `SPACE` event tracks like the comet's (from the Round 3 samples, grown to full length, levels measured against the hum). The music slot's event pick: the comet, then a picked tradition while you're in one of its rooms (`tradOn(id).rooms`), then the ship-wide events by `eventNow()` (the Line's ceremony and supper, the visit's arrival and formal dinner, the visit's farewell song, the ending's goodbye and end page). A track you chose in the Music app still wins. sound_check part `r3music`. | section 27 only | about 2.5 h |
| 2 | **The mess hall.** The background (the galley and the clatter) plus the warm low hum of talk, every layer following the number of people in the mess hall (`DECK_CREW` in its room, plus you), silent when it's empty, only while you're in the mess, fading as you leave. sound_check part `r3mess` (empty: silent; few and full: the layers' rates; leaving: fades). | section 27 only | about 1.5 h |
| 3 | **The feature sounds a watcher can see:** the badge rack A (`dosiOut()` taken and back), the reactor door A (its door in the door watcher), inside the reactor room A (room watcher), a coil off and on A (the coil's `running`), winding A and the lathe B (the activity's step words, in the activity slot), promotions A (rank changes; the badge ceremony's scene), Calder's question B (its scene), Stay or Go B (the answer as it's saved), the Tern landing B (the vessel's arrival while you're in the shuttle bay), a booked shutdown A, the clock's early-out question B (its Cancel on the screen). sound_check part `r3fx`. | section 27 only | about 2.5 h |
| 4 | **The five that need a hook** (one line each, behind `SND_R3_ON`, the owners to review): the knock on your door B (28a's wake knock), the team "Next step" call A and the team done B (28d), the calibration lock A (24x), the bronze bar C (the vessel slot's tap test), clock Undo A (section 15's `clockUndo`). sound_check `r3hooks`. | 28a, 28d, 24x, 18 vessel slot (not the visit lines), 15 | about 1.5 h |

Not built (the user's picks): Basil, the Saves app, the Works tabs, the shop menu: no sound. The HQ offer A is the Mail bell, which already plays. Still to ask the user: the room B door, the test fit.

Total about 8 builder hours, plus the full round at the switch-on.

## Memory

SD2 is at about 50% now. Turn 1 fits. Before turn 2 SD2 will be near 60%, so the plan is: SD2 builds turn 1, writes `plans/handover-sd2.md`, and a fresh sound session takes turns 2 to 4 from it.
