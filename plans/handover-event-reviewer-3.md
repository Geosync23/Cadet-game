# Handover: event reviewer 3 (ER3), the adversarial reviewer for ship-wide event builds

Written 2026-10-21 by ER3 (session_017jM4m1bcqPHbSesi2kSfLr), at about 150k memory, at lead 24's request (the account move).
A fresh reviewer reads `plans/handover-event-reviewer-2.md` first (the method), then this.

## Role, branch, people
- **Role:** the hard, adversarial review of each event build before its switch-on. The verdict is PASS, PASS WITH FIXES
  (numbered, each with an exact repro) or FAIL. Fixes go to the builder, a short summary to the lead.
- **Branch:** `claude/event-plan-review-3` (from claude/event-plan-review-2). Push only here. Never push to game branches,
  main or integration.
- **Lead:** lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r (report only there).
- **Builder:** EV7, session_01WeSNWT2a7Fs8HS3j9HWamK (the Line, claude/line-update).
- **Others:** EC1 owns bigevents_check (never edit it, ask); PR6 is the turn reviewer; FD1 (session_01YJhagf6oyF6SeT5XGvrL5H)
  owns the food_check fix.

## What I reviewed
| File | Subject | Verdict |
| --- | --- | --- |
| `plans/event-line-build-review.md` | Crossing the Line build, claude/line-update b4efc66 (L1-L5c) | PASS WITH FIXES, round 1 (23b8e03, 2dffd69) |

**Round 1 in one line:** off identical; the story plays.
- Must fix:
  - 1: a reload mid-panel loses the moment, because `lineMoment` sets `story:*` as the panel opens;
  - 2: the supper is one sitting of 44, and Pell's not at it;
  - 3: six off-duty first-timers skip the ceremony.
- Small: 4-7.
- Check gaps: 8. Plants P2 (the supper emptied) and P3 (Tomas off watch) pass bigevents_check; P4 (an off leak in
  linePudding) passes cadet_test.

## Where I stopped: round 2 part A done (claude/line-update 835bcfc); part B after the account move
- **Part A, verified:**
  - fix 1 (reloads re-offer the moments);
  - fix 2 (59 at the supper, at most 39 at once, Pell's guess plays);
  - fix 3 mostly (14 of 22 first-timers, the crowd 46 plus you);
  - PR6's Captain (at the glass from 14:30);
  - the jobs held to 13:45;
  - fix 8: plants Q2 and Q3 now FAIL bigevents_check 7c7d4eb.
- **Open:** fix 9 (sent to EV7). Lemaire (a day off) and Reyes and Yoon (night workers awake by 14:29) still skip their own
  ceremony.
- **Part B, to do after the move (lead 24's call), on the then tip:**
  - cadet_test off against the storm tip (the merge base, still b991877 at 835bcfc);
  - check_fast;
  - events_check, day_check 6/7/8 and food_check 7 (on);
  - fix 9's repro (`r2.js`: `firstNot`);
  - P4 (the off menu leak: did EC1 add the off-part reads?);
  - a quick look at fixes 4-6 (the thanks at 15:00, Brennan's two lines spaced, the punch counted when the work is done)
    and nits 8-10, 12 (EW2 c2ee4e4).
  - Then the final verdict and a summary to lead 24.

## How to test (what worked)
- **Setup:**
  - three.js: `npm pack three@0.128.0` into /tmp/cadet-work/three;
  - acorn 8.12.1 into $CADET_WORK/acorn for names_check;
  - `pip install playwright`.
- **Copies:**
  - on: the two-line sed (EVENTS_ON and EV_LINE_ON);
  - bigevents: `const EV_LINE_ON = EVENTS_ON;` and EVENTS_ON left false (it flips it itself).
- **Probes:** `plans/er3-probes/` (README there). `common.py` has `near_walk` (a real `playerGo` walk up to someone),
  `walk`, `run(g, ship_minutes, until_js)`, `__dlg(pick)`, and a toast log.
- **Speed:** 1 ship minute = 50 frames (SHIP_RATE 0.6 ship min a real second).
- **Paper first:** `planDay`/`whereIs` for everyone is fast and found fixes 2 and 3. Then walk the moments.
- **Runs:** one browser check at a time, each in its own CADET_WORK. A full set takes about 70 minutes: bigevents ~20,
  events ~10, day_check ~5 each, food_check 1 day ~5, check_fast ~5 alone, cadet_test ~10.

## Gotchas
- The game's `toast` is only swapped by assigning inside `__sc` (`toast = ...`); `window.toast` doesn't reach it.
- With TURN_IN on, `finishJob` isn't "done": `turnInJob` is.
- `nearestOpen` wants world coordinates; `placeSpot` needs the deck loaded.
- A `whereIs` on a person id that doesn't exist crashes in `wsoWhere`. Ulla's id is `v-jaramillo-ulla`.
- The servery tap from a script didn't queue me. Standing at the line spot (33,4) puts you within Brennan's 8 m.
- A real save-and-reload with `?debug` started a new game for me. Use ER2's simulated reload: DIALOGUE null, the
  `moment:` scripts deleted, `e.mine` kept.
- `food_check BUILD 11 4` FAILs on dinner waits, carts or the chiller come from the check (FD1's fix, claude/food-waits 0f808c3),
  not the build.

## Open questions for the user
None from me. Everything is with EV7 and EC1.
