# Handover: events engineer 1 (EV1), the events base

Written 2026-10-21 ~03:50 UTC by EV1 (session_014ckxYgG3KA6eHksEMi6Eru) at about 55% memory, after F4. Lead 22's plan:
EV2 (session_017S7eVMgX34nSt8fxZ5kat9, `claude/events-base-2`) takes F0b, F5, F8 and then the ion storm update; a
fresh session taking the role reads this first, then `plans/events-base-brief.md`.

## Role, branch, people

- **Role:** step 4's shared base for ship-wide events (F0-F8) in section 18 (the traditions engineer's section, which
  this role holds for events). Brief: `plans/events-base-brief.md` (F0-F8 as turns, OR1's fixes, the user's answers).
- **Branch:** `claude/events-base` only (from claude/integration 0.64.5; 0.64.6 merged in; claude/events-plan merged,
  docs only). Never set the build number.
- **Lead:** lead 22, session_01BGQCZLK6gYTnqu6mwZ61jB (overnight mode: questions go to the lead, who takes the recommended
  answer). **Reviews:** PR2 (session_013ttt3gV3DaF9y4caBtFnh9) the turns, and it covers owner hooks now that OR1
  (session_01W7AHxrcgBM3rJNtCFKwp9W) is handing over; PR3 reviews storm/Line turns; ER2 reviews finished events.
- **Others:** EC1 (session_01QgShGXD6P24DDxTp8npN41, `claude/bigevents-check`) **owns `bigevents_check.py`**: never edit
  it, take its file (`git checkout origin/claude/bigevents-check -- bigevents_check.py`) and send EC1 notes. FR1
  (session_01FXFdUaCbBurQbdY9E58HKs, `claude/fridays`): Short Fridays and the Captain's address. EW1
  (session_01KkAhg7eVhPenBBVfLufPU1, `claude/events-lines`): the events' words, ready in `plans/events-ready/<event>/`.
  PB (session_01FWW2piuXkFYaRRzLXZiqYb): section 14's owner, reviews the F0b hook. EP2 (session_01GpiqZ9jCYbS9XTNPF8adHr):
  the Crossing the Line plan (`claude/event-plan-line`). EP3: the storm plan (`claude/event-plan-storm`, v1.2, answered).

## What's built (all behind `EVENTS_ON = false`: off = 0.64.6, cadet_test ALL IDENTICAL every turn)

Switch lines (section 18, just after `const EVENT_BANDS`): `EVENTS_ON`, and `EV_CAL_ON`, `EV_GUARD_ON`, `EV_NOTES_ON`,
`EV_DEVICE_ON`, `EV_REPLAY_ON` = EVENTS_ON (a check flips one line to try one piece). Data there too: `EV_CALENDAR`,
`EV_TABLE_EARLY`, `EV_LATE`, `EV_BEATS`. Functions are in the slot `// ---- slot: Traditions engineer` (end of 18).

| Piece | Commit | What |
| --- | --- | --- |
| F0a | 835ab24 | `EV_CALENDAR` (crossingLine 6, ionStorm 11, comet 16, diplomatic 26: day = the event's day 0); `eventDueDay` -> `evCalDue` when on; `EV_BEATS`' Friday row (held 15:30-17:00 from Day 5; FR1 reads it by id 'fridayAddress', never rename); `evBeatAt(startDay, [day, min])` is the ONE place an event beat's minute is worked out (phases, meetings, news, felt moments; a beat in a held hour waits for its end, `evHeldEnd`); gathering moments carry `k`, `from`, `places` (party `k: 340`). |
| F1a | 0313e52 | `eventDay(d)` (24k's cases skip it): the onset/escalation/resolution days, from the calendar's plan only. puzzle_check P1 skips those days. |
| F1b-c | 1030626 | `EV_BEATS` guard list (first promotion, all-clear, Pillar 5's held beats with "est." hours, night shifts held from 20:30); `evBeatsOn(d)`, `guardFree(d, from, to, kind)`; the summons `occReadyAt(d)` (Day 18 16:00 on), the Captain's table `occTableSlot(d)` (19:00-20:15 on night-shift weeks: user answer 2); occasion Mail bodies may be functions. |
| F2 | a2d9f40 | `simNote('eventPhase', { id, phase, day, t })` as each phase begins (s20 makes the cue `event.<id>.<phase>`; the 89 storm reaction lines can play). |
| F3a | 9ddea29, 35722f1 | `eventItems(a, b)` (meetings only; gatherings are already traditions) in the Schedule/Tracked (s19 devDay, devItemGoal hooks); `eventClosed(g, t)` hides closed places in Tracked (s15b); `EV_OPEN_FOR` opens the auditorium for the Friday address (user answer 3); a meeting keeps its toast while heads-ups are off. |
| F0c | 8b0c8dc | `SHIP.evFrom` (first day the calendar was on; saved once; new game 0), `evSkippedFor(from, log, cur)`, `EV_SKIPPED`, `evCalPlan()` (eventDay and evCalDue read it); readers `eventBandOf`, `eventJobDone`, `eventJobsCount` (play state: never the planner; job ids must stay \w-only). lines_check: event.* lengths (Mail 400; gathering mail/thanks, keepsake, plaque 200; status 60; rest 90). |
| timed Mail | (in 35722f1's batch) | `mail.<key>: { at: [day, min], from, subject, body }` beside the per-phase form; once a run (`e.mine['mail:<key>']`). EP2's Line plan (`mail.vanceLine`) and EP3's debrief use it. |
| F2b | 5189d08 | s20 socHear applies 'eventPhase' and new 'eventMoment' notes at once (cues at the minute, not the hour's end); `SOC_CUE_OF.eventMoment` -> `event.<id>.<moment>`; s18 sends eventMoment with each felt moment. |
| F3b | 1c86ab4 | `eventStatus(t)` on Home (writers' `event.<id>.status.<phase>`, else `def.status`), `eventRecord()` in Record (s19 hooks). |
| F4 | (this push) | `eventFinish(e, def, t, quiet, out)` split out of eventAdvance (for Dev mode's End and keep); a meeting open at a save plays again after the reload (`e.mine['open:<id>']`, counted once), else its gist; felt moments kept in `e.mine['felt:<id>']`. |

The user's answers (design-doc "Ship-wide events"): skip a passed event (decided once, saved); the 19:00 table; the
auditorium opens for the Day 12 address.

## Left for the next engineer (EV2's queue)

1. **F0b** (EV2 is building it): section 14 plans the cast into event meetings, in PB's shape (the brief's corrected F0b
   and my message to EV2 of 03:4x): the gatherings line, the 'meet' break during the shift, `eventCalledIn`, the
   calledIn note and cue, eventGatherings calendar-only when on, `SHIP.evFrom` in s14's evSig.
2. **F5** rank parts: a meeting's `ranks: [...]` (SHIP.works.rank: junior/officer/senior/specialist): below it, no panel,
   the gist by Mail; keep ranked-out meetings out of `eventItems` (OR1's note). Jobs by rank belong to section 17.
3. **F6:** with Dev mode's Stop 3 (the lead's call): `eventJump(phase)`, `eventEndKeep()` via `eventFinish`.
4. **F8:** section 20c's `homeCallable` (`ev.phase === 'onset'`, about line 40083) reads `eventMod('effect', 'commsDown', t)`
   when `EV_COMMS_ON`. Leave the story-moment gate (about line 39857, also `phase === 'onset'`) alone: it isn't calls.
   The brief said "two places"; only one is calls. Calls only (lead 21's answer), not Mail.
5. **The storm update S1-S10** (EP3's plan v1.2, the user's answers 02:30 UTC), with these carried in:
   - FR1 already added 'captains-address' to `SHIP_EVENTS.ionStorm.keep`: don't add it again.
   - Exempt the Captain AND Vance from the onset's doubleShift 16:00-16:50 on Day 12 (FR1's fridays_check notes an
     empty lectern until then).
   - The rec deck closes front -> all-clear: a routine `{ where: 'deck:7', rule: 'closed' }` (eventClosed already reads
     'deck:<n>'; EV_OPEN_FOR keeps the auditorium open for the address).
   - A slow player's promotion scene on storm days waits until after the all-clear (lead 22): a guard call in 24p
     (owner review).
   - `EV_DAY_DRESS`: the storm builds it, the Line reuses it; the final shape is ours (EP3's and EP2's plans describe it).
   - Move events_check's hard-coded storm day (10) to read `EV_CALENDAR` when the calendar is on (PR2 found 8 FAILs on
     with F0a, mostly that); PR2's quiet-watch Day 300 "7/9 reached" with the switch on: not looked into yet.
   - OR1: the visit's phases give eventDay 28, 29, 33 (resolution at +7): fix in the visit update.
   - EW1's files move in from `plans/events-ready/<event>/` and get baked in the turn that builds each event.
6. **PR2's nits still open:** a one-day event's Record row reads "Days 11-11" (use "Day 11"); the F3b comment's "one
   line on a phone" should say "about three lines" (60 characters); the s19 Home edit moved the "// 0.34.51: how many,
   then each" comment onto my eventStatus line (put it back on the Today-aboard line); a comment that event job ids
   stay \w-only. (I fold these in with F4 if they fit; check the F4 build-table row.)

## Gotchas

- **The container restarts** (three times on 2026-10-21 night): commit locally before long checks; run checks with a
  resumable runner (mine: a script appending "step exit tail" lines and skipping finished steps). player_check takes
  about 20 minutes a run; cadet_test about 8; check_fast about 4.
- Test setup in a fresh container: `pip install playwright`; three.js from npm (`npm pack three@0.128.0` in
  /tmp/cadet-work/three, then untar): cdnjs is blocked; acorn from npm (DEV_NOTES "quick check").
- A switched-on copy: `sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/'`. With it on, events_check FAILS on its
  hard-coded storm day (expected until the storm update), career_check fails only its known row-12 line.
- Name clashes: `evAt` is section 14's (mine is `evBeatAt`). Run `node names_check.js` after every edit.
- cadet_test sometimes prints "renderer noise: 1 level": documented (DEV_NOTES "Screenshot noise"), not a change.
- eventGatherings/eventOn read eventNow, which reads the live log: fine for play, not for the planner (F0b fixes it).

## How to test a turn

names_check -> your probe (a switched-on copy, `cadet_test.py`'s Game class: `exec(open('cadet_test.py').read().split('a, shots = run(')[0])`)
-> events_check, the area checks off and on -> cadet_test old (claude/integration) vs new -> `bash check_fast.sh` alone ->
build-table row -> commit, push -> lead 22 (PR2 the turn; owner hooks to PR2 while OR1 is away).
