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
3. **Calder's word, notices, arrows, rings (done).** 28a: `P5N_WORD`, `P5N_SEEK`, `p5nScript`, `p5nTold`,
   `p5nWordTick`, `p5nEscort` (hooked into 24 core's worksEscort, after p5Escort), `p5nGuide`. Meetings
   content/meetings/night.on.meet, night.off.meet; words content/works/night.lines (stand-ins, baked). Each night: the
   notice (20:30; night 1 22:40; with P5_PROMO4 and W7's 24u `pu4Fetches(now)` true, none of ours: her fetch from the comet says it; see turn 6), a level 1 arrow and
   forced ring to the clock, then the engine room, the clock at 06:00, the plate, your bunk (ring on "Set alarm").
   Day 22 12:30: clock out, then sleep. Holding a job while the clock waits: an hourly notice. With P5_M21, 28b may
   define `m21Door(t)` -> { deck, tile } for Calder to wait at. Flags p5n.* (saved).
4. **The night's work, the night incident, the clothes day (done).** 28a: `P5N_INC`, `p5nBoardWin`, `p5nIncPlan`,
   `p5nIncTick`, the `job` turn-in listener (ns[d].jobs), `p5nClothes`. Hooks: 17's boardTopUp (your night's hours),
   leaveEnd (a job found in your night's hours is held for you in them), jobReserve (`o.night`: held to 06:00); 24f's
   incPost (held for you while clocked in for a night); 21b's clothesYesterday, the status line and the morning tip
   (`clothesLateAt`: four hours after your wake after a night). Navarro's call home: his rota's `calls-home` habit
   already gives his off nights calls; no planner change (left as is, noted for review).
5. **The checks (done).** player_check's `night_part` (end of every run; `--night` alone; its own on copy) and
   controller_check part `nights` (in ALL_PARTS): both OK on 06b6a15. Night 1 with P5_PROMO4 agreed with W7: 24u's
   22:40 fetch from the comet (W7's `pu4Fetches(now)`, true while she fetches and walks you down) silences our night-1
   notice; our clock and engine-room arrows lead her walk; the knock silent with P5_PROMO4. night.on/off open from 6 m (RV23's should). On-copy runs of day_check
   24/25, food, leave, clothes: see the build table's last N6 row.
6. **Turn 6 (done, 992a4b0):** W7's `pu4Fetches(now)` silences only our night-1 notice (our arrows lead her walk; no
   auto clock-in). Check fixes for the nights on: leave_check's full-shift part (Days 29-31), mech_check m19's next-day
   part (Days 18-19) and its reset clears SHIP.career. On a Step 6 copy: day_check 22-25, food, clothes, leave,
   mech m19, player_check, controller nights all OK. Controller presets: none in section 25 (S6-3's seat, W7 adds Step
   6's Dev rows at the end); controller_check's `nights` part sets its own Day 22 and Day 23 states instead.
   Words are stand-ins, baked.
- **Left for S6-1:** RV23's must (Calder's walk to you on Day 22): take W7's escort fix (claude/escort-follow-fix
  cffe8187) once it's in staging, then RV23 re-runs plans/rv23-shots/n6_play.py. Then the nights' own full round.

## Shared formats
- `SHIP.works.ns` = `{ skip?: true, [d]: { in, out, jobs: [ids], inc: [ids], late, miss?: true } }` (ship minutes).
  Restored after 24 core's worksClean (which drops unknown keys) by 28a at load, as 24u does for `pu`.
- `yourShift(d)` -> `{ day: [from, to] | null, night: [from, to] | null }`, minutes from day d's midnight.
- `playerNightOn(d)`: the night starting on day d is yours. `p5nNoDay(d)`: no day shift (the morning after a night).
- simNote `p5night` { step: 'missed' | 'knock' | 'plate', day }.

## State (2026-10-27 ~14:00 UTC)
- **Merged:** BM19 merged 992a4b0 into claude/staging-p5s6 7bc997eb (with W7's escort fix and promo4); this branch
  has 7bc997eb merged in (game identical to it). RV23's must is cleared there.
- Lead is now lead 42 (session_01GKuymjnCHnpwDqB94PVwmV, branch claude/lead-42), after lead 41.
- Latest: claude/p5s6-nights 3bf30e6 (staging-p5s6 a2ef6416 merged). RV23: PASS (13:40 UTC), its one must (Calder's walk
  on Day 22) cleared once W7's escort fix cffe8187 is in: RV23's scratch merge saw her walk 20.8 m -> 5.4 m and night.on
  play. Lead 42 (13:58 UTC): merge staging only if this branch needs cffe8187 (BM19 merges the nights himself); no separate nights round (the Step 6 full round after switch-on covers it); stay idle for round fixes; N6-1 waits for the playtest-patches stage. MA6 reviewed
  the mech_check m19 edits: OK.
- MA6 (28d, night 3) reads playerNightOn(24); its Watch hour avoids night 3's incident (02:30-03:30 Day 25). MA6's
  28b defines m21Door() for Calder's wait after the briefing.
- Backlog N6-1: an ended career's save doesn't load (section 20, not Step 6's).
- 16:00 UTC: lead 42 offered PZ6's arrows_check step6 + m24 pick pointer job; I was at ~54% memory, so it went to AS1
  (session_01GKuymmdgtDvbd8P7URXd4z). I stay idle for S6-1 round fixes and answer AS1's questions on the nights.
- Branch: claude/p5s6-nights 6034515 has staging-p5s6 40f3bdac merged (game identical to it).

## Gotchas
- `P5_NIGHTS` / `P5_LEAVE` are consts after sections 13-24: read only at run time. My readers go through `p5nOf` /
  `p5nOnLeave` (try/catch). A probe (an on copy, a fresh load) found no call of isWorkDay or playerShiftOn before
  section 28 runs.
- SHIP.career.ci / .co stay the day's punch: a night's in/out are in ns, so careerTick's day logic never sees them.
- Day 22 is a Monday; Days 23-26 Tuesday-Friday.

## How to test
- Off: `cadet_test.py` vs 64e296df ALL IDENTICAL; `bash check_fast.sh`.
- On: a copy with `const P5_STEP6 = P5_STEP5 && true;` (or `?p5s6`).
