# Handover: the career engineer

**Role:** leave, missed shifts, the summons ladder, being let go (the game's only fail state), and being sick.
Reports to the lead (lead 8, session_01FutyR6xiAmZv29oS4TWKdS, from 2026-10-17 ~20:00; before that session_01KPJMYjXAPkNUcrQ8VRkhLE). First session: session_01862tURG1qXAVGj2sdUrVCw.
**Branch:** `claude/leave` (from 0.60.4 d449914). **Builds:** 0.61.0-0.61.16. Reviewer: 1d (session_01AxGXvu4gwTfNVGRKeYbBPw).
**Writers:** head writer 4 (session_01MWyyMaXv6D7yKtDNy9VbCA; career, sickness) and head writer 5 (session_011KTwL5FVSdmWNAkbkZsrgj; the clock), on `claude/content`. Reviewers: 1d, then 1e.

## What's built (all in DEV_NOTES "Leave, missed shifts and being let go" and the 0.61.x rows)
- The career section sits in section 20, after `movedOff`: `CAREER`, `careerTick` (each ship minute from `tickShip`, and
  after a skip via `SIM_ADVANCE`), leave (`careerBook`, `careerCanBook`, `careerOff`), misses (`careerMissed`), the
  ladder (`careerLadder`, `careerDue`, `careerHeld`), the goodbye (`careerLetGo`, `careerGoTick`, `careerSendOff`,
  `careerCard`), warnings (`careerTip`), worried friends (`careerSeek`, `careerSeekLine`).
- Being sick (`SICK`, `sick*`) right after it.
- The time clock (0.61.13-0.61.16): `WALL_KIT.timeClock` (Works bay north wall past the tool wall), place `5-timeclock-1`, `careerClock`, `careerClockTap`, `careerRemark`; section 14's `shiftWithBreaks` gives the Works crew on Deck 5 a clock stop at the start and just after the end of the shift; `careerAtWork` (asked by `shiftTick`) is "clocked in" after the first week.
- Reputation you can see (0.61.15): `careerJobIn` on `simNote('job', { step: 'turnin' })`: the chip (`needFloat`) and a small gain for jobs with no machine.
- Hooks outside it (all small, marked 0.61.x): `playerShiftOn` (section 14), `tickShip` (13), section 14's farewell
  segment in `gatherings`, `occasionAdd` passes an occasion's `with`, `seekShow`/`socialSeekAsks`/the chip's click
  (20), `chatLine` (20), the Schedule app (19), `needEffects`, the crawl crouch, `bunkLie`, `offerSleep`, the sleep
  handler (15, 13).
- The rules (the user's): the Chief's talk after 3 workday shifts missed in a row OR work under 15; the Captain at
  work under 12, only after the Chief's talk has been held; let go after 3 workdays at the bottom (under 5), counted
  only after the Captain's reprimand has been held. Lateness alone never reaches the Chief.

## Shared formats
- Save: `ship.career` (see the comment above `CAREER` and at `SICK`), about 200 bytes, read by `careerClean`.
- Words: `content/banks/career.lines`, `content/banks/sick.lines`, `content/career/*.lines`, meetings `careerChief`,
  `careerCaptain`, `careerLetGo`, `careerSendoff`, `sickExam1-3`, `sickExamCover`. Texts read as data with
  `careerText(kind, k)` ("subject | body" for Mail, "title | body" for cards). `lines_check.py` allows 140 characters
  for `career` kinds.

## Loose ends (parked by the lead)
- On a Sunday last day Torres and Pell are on shift, so their plans keep them at work during the send-off (a
  section 14 change to let send-off crew step away).
- Head writer 4's extra kinds aren't used: `career.missed`, `career.up`, `career.leave.booked`, `career.onleave`,
  `career.back`.
- The Record (device) doesn't list sick days; the Schedule says "Sick, seen by Rina".

## Gotchas
- `SHIP.career.gs` (the game seed) is random per game: tests must pin it (leave_check does) or switch sickness off.
- `careerTick` walks every day it has passed (`e`, `z`), so a long skip counts each missed workday.
- In tests, section 20 scores `shiftStart` only in `socialHour`: call `repNote('shiftStart', ...)` on paper.
- Don't put a `//` comment in a one-line JS string you `ev()`, or in the middle of a line you build by string replacement: it swallows the rest of the line (it happened twice).
- cadet_test hides the floating chips (`#needFx`), so screenshots never show the reputation chip.
- The clock stops change the Works crew's plans: run day_check (shift minutes) whenever you touch them.

## How to test
`CADET_CHROME=/opt/pw-browsers/chromium python3 leave_check.py starship-cadet.html` (about a minute), plus player_check,
social_check, day_check, device_check and cadet_test against the build before.
