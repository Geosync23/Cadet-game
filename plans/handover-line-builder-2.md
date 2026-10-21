# Handover: the Line builder 2 (EV7), the Crossing the Line update

Written 2026-10-21 by EV7 (session_01WeSNWT2a7Fs8HS3j9HWamK), before the project's account move (lead 24's ask).
Memory used: about a quarter. A fresh session taking the role reads this, then EV5's `plans/handover-line-builder.md`
(L1-L5, the switch, the gotchas), then the build-table rows "line L1" to "line L5f" (plans/build-table.md, the
"Crossing the Line update" table), then ER3's review (claude/event-plan-review-3, plans/event-line-build-review.md).

## Role, branch, people

- **Role:** Crossing the Line (Sunday Day 7), turns L1-L6 of `plans/event-line-plan.md` v2.2 (claude/event-plan-line).
  Section 18: its data block after the storm's, and the slot `// ---- slot: Line builder`. Small hooks elsewhere
  (section 14's evClosed, 4d's lineRibbons tap, 18's base: see "Shared things I touched"). **Never set the build lines.**
  Name each turn in a build-table row.
- **Branch:** `claude/line-update`. Merge `claude/storm-update` in as it moves (last: b991877, in e658e43).
- **Lead:** lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r (lead 23 handed over). Questions go to the lead, never the user.
- **Reviews:** PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i) every turn. ER3 (session_017jM4m1bcqPHbSesi2kSfLr) the hard
  build review (round 1: PASS WITH FIXES; round 2 to ask for). PB (session_01FWW2piuXkFYaRRzLXZiqYb) owns sections 10/13/14
  (closed the evClosed fix). EC1 (session_01QgShGXD6P24DDxTp8npN41) owns bigevents_check.py (take it as is:
  `git checkout origin/claude/bigevents-check -- bigevents_check.py`). EW2 (session_0138EzUAZjAJ3rUMiwyK3m3p) the words
  (claude/events-lines-2, plans/events-ready/crossingLine/content/...: take its files whole, then `python3 content_gen.py`).
  FD1 (session_01YJhagf6oyF6SeT5XGvrL5H) has food_check's "garden carry" (see Loose ends). EV6 owns claude/storm-update.

## What I built (all behind `EV_LINE_ON`, still `false`; off = cadet_test ALL IDENTICAL every turn)

| Turn | Commit | What |
| --- | --- | --- |
| merges | ebac8fb, e658e43 | claude/storm-update (seated lantern supper, S2, the stand-ins out); five code clashes kept from both sides |
| L5b | 24020ef | PB's evClosed fix (a `gather` closure checked through the whole stay); EW2's words; the dunking (14:55-15:15 mug pose); Brennan's offer in person (from 10:30, wherever she is); the goal pointer to Tomas while the mug's yours; Brennan's saved mug for you |
| L5c | 0aae259 | the Line supper seated (the user's answer): `stay`, `seated`, `pudding: true`; `lineStandTray` gone |
| L5d | 4306fd1 | PR6's fix 1: the oath's cast 25 min early (a meeting's `early`), the crowd's `lead` (lineLead); moments' flags set when the panel ends; the volunteer jobs held to 13:45 |
| L5e | b42b6d8 | ER3 round-1 fixes 2-7: supper 18:00-19:45 + Pell; 'everyone' in a day-dress `who` read as a floor; first-timers' own ceremony (`ownFor`); thanks at 15:00 (`joinAt`); Brennan's two bubbles 4 min apart; punch job's workDone counts |
| L5f | e3870c1 | lead 24: supper everyone at 1, 30-45 min sittings (59 come, at most 40 at once, 83 mean to go; widest 416 draw calls); EW2's c2ee4e4 words ("The Line oath") |

## Shared things I touched (optional fields: absent = as before)

- section 14: `evClosed` (PB's fix). section 18's base: `evMeetsOn` passes a meeting's `early`; `eventMeetPlan` uses
  `g.early || 5`; `eventPlan`'s `own` also from a gathering's `ownFor(p, d)`; `eventsPlayer` waits for a gathering's
  `joinAt`; EV_SHIPWIDE passes `seated`, `easy`, `whereFor`, `lead`, `ownFor`, `joinAt`; `evDressed` takes `stay`,
  `seated` and an `'everyone'` floor in `who`. 4d: lineRibbons' tap text from `event.crossingLine.tap.punch`.

## Loose ends (for the next session)

1. **day_check 7 FAILs on L5f (the next job).** eklund-leila (not at the Line supper) eats her ordinary dinner twice:
   queued 18:13, a placeless 'dinner' 18:13-18:36, queues again, then 18:51-19:19 at 3-lounge-34 holding a tray
   ("a tray outside the mess hall", "standing still with a tray"). It's the two-dinner shape ER3 noted for Vance (its
   nit 13; also on the base on Day 21: section 14's, PB), made visible because the bigger supper fills the mess's
   seats so her second sitting lands in the lounge. Options: ask PB about the double dinner in section 14 (the real
   fix), or keep the supper's peak lower (e.g. stays [30, 40]) and re-measure. Ask lead 24 which. L5e (stays 45-60,
   own pulls) passed day_check 7.
2. **ER3's fix 9** (round 2 part A on 835bcfc, plans/event-line-build-review.md on claude/event-plan-review-3 d1bf2eb):
   three first-timers still skip their own ceremony: Lemaire (night shift, a day off on Day 7, ownFor true) sits on
   3-bench-14 14:17-15:44; Reyes and Yoon (night shift) wake 14:22-14:29 and go to music and the gym 14:29-15:24. ER3's
   fix: an off-duty honouree's leisure block gives way to the ceremony, and a night worker awake before 14:30 comes
   first (17 of 22 then). Cause I found: `eventFree` (section 18) says a night worker isn't free before 15:00 the day
   after a night shift (`P.works && a < 900`) and while asleep; Lemaire's case is that rule. A Line-only exception in
   `evArrive` for `ownFor` people (free from their wake + a few minutes) would do it. Repro: ER3's plans/er3-probes/r2.js
   (`firstNot`) and r2b.js. ER3's part A otherwise verified fixes 1-4 and EC1's check gaps; part B (the full set) after
   the account move.
3. **The Brennan rota clash** (FD1, food_check "rota vs plans": brennan 14:30 3-galley-1 → the oath's lead-2): only on
   claude/food-waits' food_check, which lacks EV5's line (an event meeting during a galley stint is a break). When
   food-waits and line-update meet, keep both (FD1's fresh() and that line). Nothing to change in the game.
3. **food_check 7 "garden carry"** FAILs with the Line on: the check's leftover machine history (gardenCond(8) light .877
   vs 1), not the game. FD1 extends its `fresh()` rewind (claude/food-waits) to part 4k; PB reviews. Check after it that
   4k passes on 7 with the Line on and off. "garden, good" FAILs on every build (not the Line's).
4. **L6, the switch-on**: `const EV_LINE_ON = EVENTS_ON;` (EVENTS_ON itself is the storm's S10, EV6's). Then the full
   round with both on: social, interactions, player, devmode, clothes, join, bubble, fridays, lines, day 6/7/8, food 7,
   events, bigevents, deck, perf (the two Line scenes), then intro_check `--week` ALONE (Day 7 is in the arrival week).
   I started that round once and stopped it (two rounds at once timed pages out): social, inter, join, bubble passed.
5. The first-timers who still miss the ceremony are on duty (Tomas, Ueda on watch; Varga cooking; Madsen's bar at
   15:00) or on the night shift (Reyes, Yoon, Keane, Lemaire): by design.
6. Not built: a mug in your own hands at the dunking (the crowd's mug is cocoa-brown at 8 px).

## Gotchas

- **One browser lane per core or so.** 4 cores: check_fast (two lanes) plus one more lane is the most; two rounds at
  once gave Page.goto timeouts (not failures: rerun).
- The test page freezes `performance.now`/`Date.now`: time from Python around `g.ev`.
- jobsHour gives jobs to the crew **on the hour**: a `hold` ending mid-hour reaches them at the next hour.
- `whereIs`/planDay segments' `from` is the time AT the place; the walk comes before it. A crowd set to start at 14:30
  arrives 14:40+; use a `lead`.
- Probes: my scratch copies are gone with the container. ER3's probes are in plans/er3-probes/ on
  claude/event-plan-review-3 (common.py has the helpers); ER2's in plans/er2-probes/ on claude/event-plan-review-2.
  A Line-on copy: `sed -e 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/' -e 's/^const EV_LINE_ON = false;/const EV_LINE_ON = true;/'`;
  for bigevents_check `sed -e 's/^const EV_LINE_ON = false;/const EV_LINE_ON = EVENTS_ON;/'`.
- Fresh container: `pip install playwright`; three.js and acorn in /tmp/cadet-work (DEV_NOTES "Testing" and the
  check_fast line).

## Open questions for the user (none blocking)

- None new. The supper's size (lead 24's call) and the 13:45 hold (lead 24's call) are in design-doc.
