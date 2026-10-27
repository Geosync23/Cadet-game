# Handover: N6 (the player + sim engineer for Pillar 5 Step 6, S6-1 the night shift)

- **Role:** S6-1, the night shift (M22, section 28a, switch `P5_NIGHT`), for lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j;
  send_message, priority "next"). Reviewer RV23 (session_01GKuymoDm1XbC5G8TvaCNLr). Build master BM19
  (session_01GKuymncYhRTKs8t4byNfdj). W6 (session_01GKuymmTEpqHLycbYTJwRQn) owns section 28's shared helpers, 24u and
  the switch lines: ask W6 before touching those. My session: session_01GKuymnDA25R2a5yZGYpaBS.
- **Branch:** `claude/p5s6-nights` from `claude/staging-p5s6` 64e296df (0.94.0 live + Step 6's first turn, all off).
  Build-table rows `0.94.0-n6.N`. The two build-number lines are never touched.
- **Spec:** `plans/p5-step6-spec.html` on claude/p5-specs (version 2; the user's answers all "recommended"), piece S6-1
  and every row naming it. Overnight mode: no questions to the user, the spec's recommended answers.

## Turns (six; the nights get their own round before switch-on)
1. **Hours, the clock, Navarro's leave, the state (done).** 28a: `P5N`, `P5N_LATE`, `p5nClean`, `p5nState`,
   `p5nLive`, `p5nOf`, `playerNightOn(d)`, `p5nNoDay(d)`, `p5nNight(d)`, `p5nOnLeave`, `p5nClockNight`, `p5nClock`,
   `p5nIn`, `p5nClockScreen`, `p5nClockTick` (WORK_TICKS), `P5N_WAKE`, `p5nItems`. Section 15: `yourShift(d)`,
   `yourDayEnd(d)`. Hooks (all `P5_NIGHT &&`, off identical): 14's `isWorkDay` (Navarro's leave), 19's `devDay`
   (the Schedule's rows), 20's `careerOff` (no day shift on Days 23-25), `careerClock` (the night's punch first;
   `yourDayEnd` for Day 22's 12:30), `clockScreen` (the night's screen), `careerTick`'s auto clock-out, 15b's
   `guideShiftOver` and the clock arrows (`yourDayEnd`).
2. **Sleeping by day, the knock, the kept plate (done).** 28a: `P5N_KNOCK`, `p5nDayBed`, `p5nSoon`, `p5nKnockAt`,
   `p5nKnock`, `p5nBed`, `p5nPlate`. Hooks: 13's offerSleep (`p5nBed` first), alarmLate (the night first), sleepGo
   (a day sleep isn't kept as your alarm; the knock wakes you); 15's bunkLie (lying down sleeps you after a night),
   needGoal (no bunk arrow on or just before a night; the bunk by day after one), the t:late tip, the tray tap (the plate).
3. Calder's night.on (Day 22 09:15) and night.off (Day 25 06:00); notices 20:30, arrows from 20:45 (level 1), ring
   lines, Tracked rows, Mail as the record; night 1's start at 22:40 with P5_PROMO4 off.
4. Held jobs' night windows (17's jobReserve), the night incident (24f), the night's ordinary jobs; 21b's clothes day;
   Navarro's call home.
5. Saves (03:00 loads into the same night), late saves, check parts: player_check night, clothes, saves, food, career,
   leave, day_check 22-25.
6. Controller presets (Day 22 22:40, Day 23 21:00), a pad-played night 2, the words (night.lines, baked), the round.

## Shared formats
- `SHIP.works.ns` = `{ skip?: true, [d]: { in, out, jobs: [ids], inc: [ids], late, miss?: true } }` (ship minutes).
  Restored after 24 core's worksClean (which drops unknown keys) by 28a at load, as 24u does for `pu`.
- `yourShift(d)` -> `{ day: [from, to] | null, night: [from, to] | null }`, minutes from day d's midnight.
- `playerNightOn(d)`: the night starting on day d is yours. `p5nNoDay(d)`: no day shift (the morning after a night).
- simNote `p5night` { step: 'missed' | 'knock' | 'plate', day }.

## Gotchas
- `P5_NIGHTS` / `P5_LEAVE` are consts after sections 13-24: read only at run time. My readers go through `p5nOf` /
  `p5nOnLeave` (try/catch). A probe (an on copy, a fresh load) found no call of isWorkDay or playerShiftOn before
  section 28 runs.
- SHIP.career.ci / .co stay the day's punch: a night's in/out are in ns, so careerTick's day logic never sees them.
- Day 22 is a Monday; Days 23-26 Tuesday-Friday.

## How to test
- Off: `cadet_test.py` vs 64e296df ALL IDENTICAL; `bash check_fast.sh`.
- On: a copy with `const P5_STEP6 = P5_STEP5 && true;` (or `?p5s6`).
