# Handover: HUD + player needs, seat U2 (playtest update 2)

**Role:** HUD and player-needs engineer for playtest update 2 (overnight 2026-10-19). Took over U's remaining items when U retired (U's note: `plans/handover-hud.md`, read it too).
**Branch:** `claude/hud-pt2`, series 0.73.x. Base: U's `claude/hud-pt1` 93194ef (0.72.5), U's final 0335523 (0.72.6) merged in.
**Builds:** 0.73.0 (items 4, 5, 23, item 1's HUD half), 0.73.1 (U's 0.72.6 merged; round-guide fixes), 0.73.2 (item 12 a). Head 0f34cfb at hand-off time. Reviewer R6 (session_01CPyuA1o5jgxwQtv7huZTNg); build master BM7 (session_01QbuzvT3TwzMwSWRmakzX8Z); lead 17 (session_016bN7x175WBwBL7S9xc2Lpb).

## What I own and built (DEV_NOTES rows 0.73.0-0.73.2 have the detail)
- **Item 4, toilet → "−3 Hygiene".** Section 15: an activity's `cost` is summed in `A.o.cost` (in the needs update) and `actEnd` floats it with `needFloat('−N Need', k, -v)`; `stripRise`/`stripTick` keep drops apart from rises and print "−N". Applies to every `cost` (a workout shows "−6 Energy").
- **Item 5, energy and the alarm clock.** `NEED_DRAIN.energy[0]` 4.4 → 4.8. Section 13 (bunk/sleep): `#sleepAsk` rebuilt as the Alarm card (− / Wake at hh:mm / +, energy line, warning, Set alarm, Not yet). `offerSleep` → `alarmOpen()` at night (the unwell-by-day nap still sleeps at once via `sleepGo(null)`). `ALARM_STEP` 30, `ALARM_FROM` 04:00, `ALARM_TO` 12:00, `ALARM_SOON` 30; `alarmChoices`, `alarmEnergy(m)` (needsDrain on your needs, restored), `alarmLate(m)` (DAY_SHIFT[0] if playerShiftOn that morning and m >= it), `sleepGo(m)`. `SHIP.player.alarm` (minute of day) is initialised and saved in section 15 next to `stripFold` (SHIP.player doesn't exist yet in section 13); New game resets it in `playerNew`. Texts: W2's `alarm.*` via `careerText`, stand-ins until baked.
- **Item 23, work wears leisure down.** Section 15 `workLeisure(mins, fx, except)` from the needs update; `WORK_LEISURE` 4.2/h on top of the 0.8 base (5/h, 40 a shift; lead 16 and 17 agreed) while `workingNow()` (clocked in and not out, to 18:00, or a WORK_ACTS activity). "−5 Leisure" note every `WORK_LS_NOTE`. One constant for the user to retune.
- **Item 1, HUD half.** Section 15b `roundGuide()` (called from `ixTips`, once a second) reads `roundTrainStep()` (24a, E1 → now E6 session_018cZuXpb4XdFs47zXoPcF8B). 'take': board arrow `RG_GOAL` (takes over straight after Torres's talk, never over another goal later); each step change: tip `rg:<step>:<n>` from W2's `tip.round.<step>` ({machine}), the previous round tip removed; all round tips gone after turn-in. `ixJobStep`: a claimed 'rounds' job's arrow label "Look at <machine>" (`machineLabel(m).split(',')[0]`, E1's naming). Inert without roundTrainStep (not on this branch).
- **Item 12 (a).** Section 19 `devDay` adds, while `introOn()`, the INTRO_WEEK beats in `DEV_BEATS` (d1-briefing, d2-solo, d2-booths, d3-store) as kind 'beat'; `devItemGoal` gives the room arrow; `devHeadsTick` lets 'beat' through with heads-ups off (like appointments). Torres's training is a section 20 occasion, already listed by `devOccasions`.

## Merge note for whoever combines with claude/mech-rounds
One conflict in section 15's `teachTick` tip line: keep both, `let tx = text; if (typeof text === 'function') { try { tx = text(); } catch (e) { tx = null; } }` then `if (tipShow(id, tx && bedText(tx))) { POP.tip = POP.card = now; return id; }`. Plus the build lines.

## Tests (all green on 0.73.1/0.73.2)
- player_check: paper week now Monday-Friday on shift (with the work drain), a hobby + "something fun" (+15) every evening; energy at bedtime averages 18-30, never under 15; leisure only checked never 0 (it gets to ~3 by Friday's shift); long days 14.5-17 h; sitting reads NEED_DRAIN; the alarm card (06:00 default, steps, 04:00-12:00, energy 60/85/100 from a 02:00 bedtime at 10, the late warning, saved 450, old/junk → 360).
- interactions_check: new parts for the round guide (stubbed roundTrainStep) and the arrival beats.
- day_check (prints "Energy at the end of the day"): crew lowest at 23:59 and you awake 06:00-24:00, both above 0. Days 0-8 OK.
- intro_check --evening OK; cadet_test ALL IDENTICAL vs 0.72.5 and 0.72.6.

## Gotchas
- player_check takes 20-40 min when other browsers are running; give it a long timeout (the 900/2400 s runs got killed).
- Don't `pkill -f player_check.py` from a shell whose own command line contains that name: it kills itself. Anchor: `pkill -f '^python3 /home/user/Cadet-game/...'`.
- `flagSet('intro.device')` is needed in tests for heads-ups (the device is locked before Torres hands it over).

## Open questions for the user
- Energy and leisure tuning (4.8/h energy; 40 leisure a shift): you're a little tired the last hour or two before bed, and leisure runs low by Friday on a normal week. Retune via `NEED_DRAIN.energy` and `WORK_LEISURE`.
- The alarm card replaces the old "just sleep" bunk tap at night (the 0.28.9 no-dialog rule): OK?
