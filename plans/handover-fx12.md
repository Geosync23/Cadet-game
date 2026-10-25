# Handover: FX12 (fixes for 0.92.3, 0.92.4 and 0.92.5), 2026-10-24

Role: a builder under the lead (lead 32, then 33, now lead 34: session_019RdVfeRPRiJpHGjKujZZJA). Reviewer RV12
(session_013JmdoWWEDQde8y1bwrMGnY). Build masters BM15 (0.92.3), BM16 (0.92.4, 0.92.5: session_01MB7n4yvCAeGyWN4WZCAGPh).
Never set build numbers. Each job: its own branch, a row in plans/build-table.md, design-doc in the same commit.

## Branches
| Branch | Base | What | State |
|---|---|---|---|
| claude/p923-fx12 | integration 364c80cb | 0.92.3 items 19 (tray kept, TRAY_TRAVELS) and 27 (Pick-your-own tray) | RV12 PASS da1825d2, in 0.92.3 |
| claude/p924-fx12 | integration 3866c8f3 | 0.92.4 item A: the user's tray rules (TRAY_TRAVELS off, trayKeep, trayGo) | RV12 PASS ceee5664, in 0.92.4 |
| claude/p925-fx12 | integration 3866c8f3 | 0.92.5 items 4 (late piano), 9 (birthdays an hour apart), 10 (birthdays redone) | pushed, with RV12 (see below) |

## 0.92.5 (claude/p925-fx12): what's built
- **4 Late piano** (content/traditions/late-piano.trad): Tuesday and Thursday (not Wed+Thu), 21:40-22:25, everyone 10%,
  new tradition field `to-bed: yes` (plans/trad_parse.py, plans/trad-format.md; section 18 tradLoad, evArrive, eventPlan):
  someone whose bedtime is inside it still comes for 20+ minutes and leaves 20 minutes before bed. Lead 34 said "Thursdays
  only"; I kept two evenings because the .trad records the user's earlier answer "two evenings" (tell the lead if asked).
  21:40, not 21:30: section 14 holds a tradition's places from 5 minutes before, and a one-off show in the music room to
  21:30 (events_check's pell-show) lost its seats at 21:30.
- **9 Birthdays an hour apart**: section 18 `evBdaySlot` + `evBdayBusy` + `EV_BDAY` (by evBudget). eventsOn now stores the
  day's list (EV_DAYS) before the birthday picks its time, because shiftBlocks -> galleyDay -> eventsOn(d) recursed
  (Maximum call stack). Only weekly traditions are ever dropped; a time near a meal / prio 2+ / rarer-than-weekly one is
  taken last. events_check's "2-3 traditions a weekday" now counts the birthday (Tuesday birthdays keep only the spice supper).
- **10 Birthdays redone**: ZW1's words cherry-picked (f869f540, 62f89173 from claude/p925-zw1; the rest of that branch is
  items 5 and 8, not mine). Places 3-bday-head + 3-bday-1..8 (Deck 3 data by the long-table heads). The birthday row's
  where/hold/whereFor/ties.decor. DECK_DRESS.birthdayTable (chair, cake, candles, tap item tag bdayCake). bdayFrame (from
  eventsTick): bubbles round the ring, lineFor with ctx.keep (no repeats) and ctx.other = the person object (an id string
  is printed raw by linesFill). Cake tap via PLAYER_TAPS, SLICE / sliceHeld / sliceTick; 8b's PROP_KIT.slice + HOLDS.slice;
  section 15's hold line; section 16 hides the servery cake while bdayTableOut().
- Checks: events_check part 13 (every line fails on 3866c8f3). Screenshots in the scratchpad were for the report only.

## Open (for whoever picks this up)
- **arrows_check week FAILS on p925-fx12**: Day 9, "m6 not learned", stuck at "! Burst pipe, Deck 4" from 10:36. It passes
  on 3866c8f3 and FAILS on 3866c8f3 + only the late-piano change (variant B) and on the build without the new Deck 3
  places (variant A): any change to the crew's plans around Day 9 seems to break the follower at the burst pipe. Not
  found why (Day 9 is a Tuesday and a birthday; the pipe is in the morning). FX3 owns the burst pipe; arrows_check is AC3's.
  Suggest: replay Day 9 10:30-10:45 on both builds and see who/what blocks the pipe's tap or the m6 step.
- Item 13 (the first ship-wide event sooner) is held: lead 34 asked the user (options in my message: move the Line to Day
  3 evening/Day 4 with re-dated words; build the comet; or a teaser).
- Backlog FX12-1: crew reach gatherings 15-20 ship minutes after their plan (walk time vs the planner's commute).

## How to test
- Fresh container: `pip install playwright numpy pillow`; three r128 + acorn in /tmp/cadet-work (testing guide 2);
  `CADET_CHROME=/opt/pw-browsers/chromium`. Run at most two browser checks at once: under load, page loads time out
  (device_check, day_check) and intro_check runs past an hour.
- events_check part 13 alone: split events_check.py at "# 13. 0.92.5" (top-level `with` blocks).
- `python3 content_gen.py starship-cadet.html` after any .trad / .lines change (check_fast's "words baked").

## Gotchas
- The shell's safety check refuses `rm -f $VAR/...`; use new file names or `"${VAR:?}"`.
- Don't replace a test block by slicing "from my part to the end of the with-block": I cut FX8's block once (RV12 caught it).
  Diff the check against the base before pushing.
