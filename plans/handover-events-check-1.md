# Handover: the big events check (EC1)

**Role:** EC1 writes and owns `bigevents_check.py`, the check for the ship-wide events (the events base brief's F7). It is **not part of check_fast**.
**Branch:** `claude/bigevents-check`, made from `claude/integration`. Bring integration in at the start of each turn.
**Reports to:** the lead (lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r). **Reviews go to:** PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i).
**Builders it follows:** EV1/EV2 (events base, F0-F3), EV5/EV7 (Crossing the Line, `claude/line-update`), EV6 (the ion storm, `claude/storm-update`).
**Never edit the game file.** If the check needs a hook in the game, ask the builder for it.

## How to run it
```
export CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=/tmp/cadet-work   # three.js + acorn installed there
python3 bigevents_check.py starship-cadet.html        # or any build: git show origin/<branch>:starship-cadet.html > X.html
```
Exit codes: 0 OK, 1 FAIL. It takes about 4-6 minutes. To run several builds side by side, give each one its own `CADET_WORK` (copy `/tmp/cadet-work` to a new folder; it's about 50 MB). The check writes its copies to `$CADET_WORK/test/bigev_*.html`.

## What it checks (parts)
The check turns switches on by text-replacing lines in a copy of the game: `const EVENTS_ON = false;`, `const EV_CAL_ON = EVENTS_ON;`, and `const EV_LINE_ON = false;` (set to `EVENTS_ON`). If the build already has `EVENTS_ON = true` (from the storm's S10), it makes its own switched-off copy for parts 1-2.
1. **Off:** the game must be unchanged. No eventDay, no beats moved by the hold, nothing passed over, the guard idle, the summons at 11:00, and the Captain's table at 19:30 for 90 minutes. Hash keys must be unique. The Device shows no events, there are no calledIn notes, and no event notes. With `EV_LINE_ON` in the build: the Day 7 galley menu has no "Line", there's no lineCeremony, and there's no `bow-lounge-line` key or place.
2. **The calendar alone** (EV_CAL_ON).
3. **Everything on.** This covers the calendar days, phases, the Friday hold, the career-beat guard (a meeting's or gathering's own beat is excused by id, or a captain beat within 15 minutes), the casts planned in the room, the crowd rules, rooms not clashing with traditions, the plan's clashes, a run twice being identical, the Device (`check_device`), calledIn (`check_callin`), and the notes (`check_notes`).
   - 3b. **The Line** (only while `EV_LINE_ON` is its own switch; `check_line`):
     - the oath cast on the lead spots, with Brennan on lead-2;
     - the front spots for first-timers only (`lineFirst`);
     - Saruth never at the ceremony;
     - Tomas at 2-watch-6 at 10:00, and Tomas and Ueda on watch every 5 minutes from 14:30 to 15:15 (a 2-wc* break is fine, never an ev- segment);
     - Tomas, Torres-Zeke and Pell on the Lap at 20:40;
     - the Line supper seated, with at least 40 who came (`LINE_SUPPER_MIN`), at once ≤ seats, and no standing spots;
     - commend false.
4. **Self-test:** clashes planted in a copy must each be caught.
5. **Late saves:** `evSkippedFor` and `evCalPlan`, real saves through localStorage with evFrom 0, 9 and 20, a reload keeping evFrom, and off with no key.
6. WAITING for F7b (live checks, when F4 lands) and F7c (crowds and draw calls).

## Crowd rules (as the user and leads have decided them)
- An **unseated** gathering FAILS when more than 60 mean to go (`CROWD`).
- **Seated** gatherings (lead 24): there's no cap on how many mean to go, because the sittings are staggered. The limits are: never more there at once than its seats, no standing (gather) spots, and the draw-call budget (F7c, not built yet).
- Every gathering: never more at once than its places. A gathering with `stay` (dropping in and out) is judged by its peak only.
- The lantern supper and the Line supper must both be `seated` (the user: no standing at meals). The "mess over 44 needs standing" rule was dropped. `MESS_SEATS` is kept only for reference.

## Gotchas
- Tradition ids carry `@day` ('party@19860'). Match on `split('@')[0]`, and use `isTrad` by id, never by the object itself.
- `SHIP.social.cues` are applied an hour after a calledIn note, so read cues at +65 minutes, not +5.
- With evFrom 0, the game catches up missed events when it loads, so a late save's expected log is every planned event ended by that day. Work it out from `evCalPlan`, never by hardcoding it.
- Don't assume the storm is the first or only event. Find rows by id.
- The `who` in an evDressed dress is a **by-person-id map**. In the Line build (c9fa161), `['everyone', .85]` matches nobody, so the Line supper used the Sunday table's own pull (55 meant to go). This was reported to lead 24 and PR6 for EV7. EV7 is widening the supper: about 83 mean to go, about 59 come, a peak of 40 at once for 48 seats.
- Planting a mutant: copy the build, make a one-string change, and run the check on the copy. The mutants used for the Line's gaps (turn 18):
  - supper emptied: evDressed's `who` returns 0 when `o.name`;
  - watch pulled off: remove `'dept:watch'` from the onset standEasy `not`;
  - not seated: remove `seated: true` from the Line supper's dress.
  - Turn 19 mutant (want over 60 while seated): `who` returns 0.9 when `o.name`. With `seated` it must pass, and without it it must fail.

## Loose ends
- Turns 14-19 are with PR6: 15-17 have been read and their runs are queued; 18 is ER3's Line gaps; 19 is the seated cap.
- PR6's note: add a comment line explaining the 15-minute captain-beat excuse in the guard.
- Still to build: F7b live checks (when EV1's F4 lands), F7c crowds and draw calls, and the jobs-done commendation.
- After the Line's L6 (`EV_LINE_ON` follows `EVENTS_ON`), part 3b goes away by itself and the Line is checked in part 3.

## Each turn
Add a row under "### The big events check (EC1 ...)" in `plans/build-table.md`, run `bash check_fast.sh` (never push when it FAILS), commit with the session trailer, push to `claude/bigevents-check`, then send to PR6 and report to the lead in plain words.
