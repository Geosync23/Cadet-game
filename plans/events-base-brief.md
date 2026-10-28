# Events base brief: F0-F8 as build turns (Turn 0)

Events engineer EV1 (session_014ckxYgG3KA6eHksEMi6Eru), 2026-10-20. Revised for OR1's review (PASS WITH FIXES, 10 fixes,
claude/owner-review-1 `plans/owner-review-1.md` part 5). Branch `claude/events-base`, from
claude/integration 0.64.5 (7958332). Reports to lead 21. **Planning only: the game is unchanged by this page.**

It turns the events plan's shared base (claude/events-plan f6996d86, `plans/events-plan.html` section 5, v3.2) into
build turns, and folds in the user's newer decisions:

- **No all-hands in the auditorium for the ion storm** (already settled in the plan; nothing in the base adds one).
- **The weekly Captain's address on Fridays** (claude/patch-plan cdeb1ff, `plans/fridays-plan.md` rev 4): off work 15:30,
  the address in the rec deck auditorium 16:00-16:50, dinner 17:00, first on Friday Day 5. It's built by its own plan
  (switch `SHORT_FRIDAY`), not by this base.
- **An event on a Friday: both happen.** Day 12's address is the regular address with the storm at its heart.
- **F0 marks Friday 15:30-17:00 as taken**, every Friday from Day 5, whether or not `SHORT_FRIDAY` is built yet.

## How it's switched

- One master switch in section 18: `const EVENTS_ON = false;`. Each piece has its own line that follows it
  (`const EV_CAL_ON = EVENTS_ON;` and so on), so a check can switch on one piece alone, the way `REC_TRAD_ON` does.
- **Off = identical game.** Every new function is still defined when off (so names_check and the hooks see it) but
  returns what today's code returns. cadet_test must say ALL IDENTICAL against 0.64.5 (or the latest integration) with
  the switch off, on every turn.
- The base is switched on **together with the ion storm update** (the next piece, 9-11 turns), after the user's
  review: F0 moves the storm from Day 10 to Day 11, and that only makes sense with the storm's new hours.
- Everything F0 and F1 decide is **data made at load plus pure functions of the day and minute**: no `R()`, and the
  crew's planner never reads anything built while the game runs (DEV_NOTES "Rules that keep it working").
- New code goes in my slot (`// ---- slot: Traditions engineer`, end of section 18). Outside section 18, only
  one-line `typeof`-guarded hooks, each listed in DEV_NOTES' Hook register and sent to its owner (OR1 stands in for
  the unstaffed seats).

## The calendar the base serves (a new game; Day 0 is the arrival, Day 1 a Monday)

| Day | What | Base pieces |
| --- | --- | --- |
| Fri 5 | First Captain's address (Fridays plan), 16:00-16:50; she mentions Sunday's crossing | F0 (Friday hold) |
| Sat 6 | Vance's Mail at 18:00: "Tomorrow we cross the Line" (a free day otherwise) | F0 |
| Sun 7 | Crossing the Line: 14:30 horn, gold lights, short banner address (the Captain called in); plaza ceremony 14:30-15:15; Line supper 18:00-19:15 | F0 (call-in), F1 |
| 9-11 | Career beats: test Day 9; summons 11:00 and move 17:00 Day 10; team job 09:30 and ceremony 17:15 Day 11 | F1 (held) |
| Thu 11 | Storm warning; Calder's briefing 14:00 | F0, F1 |
| Fri 12 | The front 14:00 (banner); **the regular address 16:00-16:50 with the storm at its heart**; no storm phase may start 15:30-17:00 | F0 (Friday hold), F2 |
| Sat 13 | Escalation, the lantern supper | F2 |
| Sun 14 | The all-clear 10:00 (four of five called in), commendation, threads stop; party 19:00-21:00 | F0 (call-in), F2 |
| Mon 15 - Thu 18 | Pillar 5 held days (test 15, Senior 16, toast 17, training 18); the summons on Day 18 at an hour clear of the training | F1 |
| Tue 16 | Comet 21:30 | F0 |
| Fri 19 | Address (the after-storm one); your night shift from 21:00 (Pillar 5) | F0, F1 |
| Sat 20 | Captain's table, must end by 20:30 (night shift at 21:00) | F1 (question 2) |
| Fri 26 | Address (four weeks, and guests); Calder's question; the visit's warning Mail that evening | F0, F1 |
| Sat 27 - Tue 30 | The visit: greeting (Captain called in), dinner, farewell after the 08:30 briefing on Day 29, afterglow | F0, F1 |

## The turns

Each turn: small exact edits, a row in `plans/build-table.md` under "events base", my area's checks, then
`bash check_fast.sh` run alone, commit, push to `claude/events-base`, report to the lead. The build number is the build
master's. I merge claude/integration in at the start of each turn (0.64.6 and patch-a when they land).

### F0. The event calendar (2 turns: F0a, F0b). Switch `EV_CAL_ON`. Section 18 only.

**F0a: the calendar table and the due day.**
- `EV_CALENDAR`: a table made at load, one row per event: `{ id, day, kind: 'main' | 'short' }`. Crossing the Line
  Day 7 (fallback Day 6 17:00, kept as a comment), ion storm Day 11 (its day 0 = the warning), comet Day 16, visit
  Day 26. An event that isn't built yet (Crossing the Line, the comet) is just skipped.
- `eventDueDay()` reads `EV_CALENDAR` when `EV_CAL_ON`, in place of `earliest` + `spread` + the `need` search
  (today's code is kept for the off switch). **One main event at a time:** an event whose days overlap a running one
  waits; none do in this calendar, and F7 checks it.
- **Saves already past an event's day** when it's switched on: question 1 (recommended: skipped, never run late).
- Ship-wide gatherings (`EV_SHIPWIDE`) are still built at load from each event's `moments`. F0a lets a moment carry
  its own `name`, `ask`, `here`, `thanks`, `from`, places and hash key, so the lantern supper, the Line ceremony and
  supper, and the comet's two windows register the same way as the party (today it's hard-wired to the party's words
  and the bow lounge's seat types). The party's row must come out unchanged (same k 340, same words). Each moment
  gets an **explicit hash key** in its data (`k`), not 350 + the order it was pushed in. `EV_SHIPWIDE` feeds section
  14's planner (through `evTable` and `eventsOn`), so with the switch off events_check compares its JSON with
  0.64.5's: it must be byte-identical (OR1).
- **The Friday hold:** `evHeld(t)` is true from 15:30 to 17:00 on every Friday from Day 5. **One source:** the hold is
  `EV_BEATS`' Friday row (F1b); F0a adds that row to the table first and `evHeld` reads it, so there's never a second
  copy. An event's phase, meeting
  or gathering that would start in it waits until 17:00 (the Fridays plan's "a storm phase waits for the address").
  None of today's dates fall in it (the front is 14:00 on Day 12); F7 checks that none ever does. The address itself
  is the Fridays builder's tradition; for both to happen on Day 12, the storm's `pause` must list it in `keep` (noted
  for the storm update and the Fridays builder).

**F0b: called in on a day off.**
- `eventCalledIn(p, d)`: true when an event's meeting or gathering on day d names p and it's p's rota day off
  (`isWorkDay`). Pure, from `EV_CALENDAR`, the events' data and the rota only: never `eventNow`, `SHIP.event` or
  anything saved. Days 7 (the Captain), 14 (Marrow, Calder, Sato, Holt) and 27
  (the Captain).
- **Corrected (EC1's finding, PR3 confirmed):** nothing in section 14 plans an event meeting's cast today
  (`eventGatherings` has no caller), so F0b adds the call in section 14's `gatherings(p, d, F)`, in PB's shape (PB
  reviews): named crew planned in on a day off **and on shift** (a 'meet' break in the shift: Calder's briefing, Tomas
  at the Line), `dept:N` by a fixed order, a chance by its own hash key; planner-safe, from the calendar only.
- A ship note `simNote('calledIn', { id: event, who, day, at })` at the meeting's start, so lines can say so. Hook:
  section 20's `SOC_CUE_OF` gains `calledIn` (a new key in a registry, plus `who` for `@me`): **social engineer's
  section, owner review (OR1)**. The cues: `cue:calledIn@me` (I was called in), `cue:calledIn` (crew chatter about it).

Checks: events_check (whole, with `EV_SHIPWIDE` byte-identical off), day_check on Days 7 and 14 with the switch on,
cadet_test off (ALL IDENTICAL). **Day 11 with `EV_CAL_ON` alone** puts today's storm, with its old hours (the 09:15
briefing, the 06:00 warning jobs), onto the 09:30 team job and the 17:15 ceremony. That's expected until the storm
update gives it its new hours, so F0a checks Day 11 only on paper (the due day and the phases' minutes). day_check
Day 11, career_check and leave_check with the switch on come with the storm update; F0a runs career_check and
leave_check on as well, to note what they say. **At F0a I tell PB (the sim seat):** the storm's new day and the new
gatherings reach section 14's planner; and `eventFree` (section 14) is shared between the Fridays plan's part A and
the storm update, so neither changes it without the other.

Before F0b, I bring in patch-a (it edits 18's `tradJoinMinute` and `tradGoal`, 20's `socialChatter` and 22) and
patch-b's batch F (15 and 17), once they're in claude/integration.

### F1. `eventDay(d)` and the career-beat guard (2-3 turns: F1a, F1b, F1c if needed). Switch `EV_GUARD_ON`. Section 18, plus reads in 24k (already there).

**F1a: `eventDay(d)`.** Section 24k already asks `typeof eventDay === 'function' && eventDay(d)` (cases skip event
days) but nothing defines it. Defined here: true only on the days of the front, the escalation and the all-clear
(Days 12-14 for the storm), never the warning or the afterglow. **It comes only from `EV_CALENDAR` and the events'
data**, never `eventNow`, `SHIP.event` or anything saved (24k's incidents plan is saved per day, OR1). An event the
calendar skips (user question 1) is decided once at load, from the save's day, so it never changes during play. **When off it returns false**, which is what 24k sees
today, so the game is unchanged.

**F1b: the guard.** `EV_BEATS`, a table made at load: each beat with its day, hours and kind:
- today's beats: the test (Day 9), the summons 11:00 and the move 17:00 (Day 10), the team job 09:30 and the
  ceremony 17:15 (Day 11);
- Pillar 5's beats held now, with their hours: the Tier 3 test (Day 15, no summons), Senior Officer (Day 16), the
  toast (Day 17), the Shutdowns training and Calder assigning your night shift (Day 18), the night shifts from 21:00
  (Days 19-20), the Monday briefing (Day 22), Engine Specialist (Day 23), Calder's question (Day 26), the 08:30 senior
  briefing (Day 29);
- every Friday 15:30-17:00 from Day 5 (the address).

`guardFree(day, from, to, kind)` answers "can a Captain's scene (or any event beat) go here?". The rules: at most one
of the Captain's scenes a day, none on a test day, never across a night shift, never in a held hour. **The weekly
address doesn't count as one of the Captain's scenes** (it's for everyone, not a scene with you); no day in today's
calendar would clash either way.

**F1c: the occasions read it.** The commendation summons (`OCCASIONS.readyRoom`) takes the first free day and hour the
guard leaves (Day 18, about 16:00, clear of the training); the Captain's table on Day 20 ends by 20:30 (question 2).
Both are in section 18 (mine). The bridge invite stays as built.

Checks: events_check, career_check, leave_check (Days 9-11 unchanged), day_check on Days 18 and 20 with the switch
on, cadet_test off.

### F2. Phase notes (1 turn). Switch `EV_NOTES_ON`. Section 18 only.

`eventAdvance` sends `simNote('eventPhase', { id, phase, day, t })` as each phase begins (after a sleep or skip too,
once per phase, at the phase's own minute). Section 20 already turns that note into the cue `event.<id>.<phase>`
(`SOC_CUE_OF.eventPhase`), and section 22 already holds 89 storm reaction lines waiting for it, so nothing outside
section 18 changes. F2 also sends `simNote('moment', ...)` for felt-everywhere moments (the jolt, the horn), which
`SOC_HEARS` already lists.

Checks: events_check (a reaction line plays on the front, within a ship hour), lines_check, social_check, cadet_test off.

### F3. On your device (2 turns: F3a, F3b). Switch `EV_DEVICE_ON`. Section 18 plus hooks in 19 (device engineer: OR1).

**F3a: the Schedule and Tracked.**
- `eventItems(a, b)`: the event's meetings and gatherings between two ship minutes, shaped like
  `upcomingTraditions`' items (`{ id, kind, title, at, to, where, deck, room }`). A new function, so
  `upcomingTraditions` keeps its result as it is (a shared function's result goes to its owner first; this avoids
  that). One hook line in section 19 adds `eventItems` to the Schedule and the Tracked list.
- `eventClosed(deck, room)`: a place an event has closed (the bow lounge, the call booths, the rec deck during the
  storm), from `eventRoutines`. Tracked and "show on map" skip a closed place (hook in 19; and 15b if the goal
  pointer offers it: interactions engineer, OR1). **The Day 12 auditorium exception (user question 3) is in
  `eventClosed` from the start**, or Tracked would hide the address's room (OR1).

**F3b: the Ship status line and the Record.**
- `eventStatus(t)`: one plain line, about 60 characters at most, while an event runs ("Ion storm: the front has passed. Lights may flicker.") from
  the event's data (new `status: { <phase>: text }`, the writer's words). Hook: the device's home screen (19).
- `eventRecord()`: blocks for the Record app: each event you lived through, its result in words (never a score), and
  your commendation. Hook: Record's view (19), next to `worksRecordHead`.

Checks: device_check, interactions_check, events_check, phone-size screenshots of the Schedule, the status line and the
Record (at 390x844 and 360 px wide), cadet_test off.

### F4. Safe through skips and reloads (2 turns: F4a, F4b). Switch `EV_REPLAY_ON`. Section 18 (and 13's save, OR1).

**F4a: skips and jumps.** Every phase between two minutes runs once and in order after a sleep, a skip or a Dev mode
jump (today a jump backwards or past an event's end can drop phases); the threads, news, Mail and notes come out the
same as when played minute by minute. The ending is split out of `eventAdvance` into `eventFinish(t, quiet)` (F6
needs it too).

**F4b: reloads.** Saved with the event (in `ship.event`, a few bytes, within the save budget): the moments already
felt (so a reload doesn't replay the jolt: today's "reload replays the jolt" item) and an open meeting's id. A meeting
whose window is still open comes back after a reload (its panel is offered again when you're in the room); one
whose window closed sends its gist as today. **Moments are never replayed.**

Checks: events_check, player_check (saving), devmode_check, a reload mid-front and mid-briefing in F7's check,
cadet_test off.

### F5. Small parts by rank (1 turn). Switch `EV_RANK_ON`. Section 18, reading section 24's `SHIP.works.rank` (Works career: OR1).

An event's meeting may say who's in it by rank: `ranks: ['officer', 'senior']`. At your rank you're invited (a
notice, it's in your Schedule); below it, you get the gist by Mail as everyone else does ("the summary by Mail to
everyone else"). Jobs may carry a `rank` too (a junior carries filters; a senior is in the briefing). Only your part
changes: the crew's plans never read your rank, so they stay the same at every rank. The head writer writes the
rank versions of lines (`rank:` in the lines' conditions already exists).

Checks: events_check (one meeting at junior and at officer), career_check, cadet_test off.

### F6. Dev mode extras (under 1 turn). Switch: none needed (Dev mode only, `#dev`). Section 18, buttons in 25 (Dev mode engineer: OR1).

`eventJump(phase)`: jump the running event to a phase (through F4a, so every phase between runs once). `eventEndKeep()`:
end the event now and keep what happened (through `eventFinish`). Dev mode's Stop 3 (not built yet) does starting an
event, the threads view and "End and undo". Question for the lead (below): the two buttons now, or with Stop 3.

Checks: devmode_check (the real save untouched; Undo after a jump), events_check.

### F7. One events check driven by the data (2-3 turns: F7a, F7b, F7c). **F7a is built straight after F1** (OR1), so F2-F6 are built against it; F7b-c come late. New file; perf_check scenes (performance engineer: OR1).

A new `bigevents_check.py` (question for the lead: a new file, or more parts in events_check, which already takes
6-10 minutes). It reads `SHIP_EVENTS` and `EV_CALENDAR` from the page and, for each event that's built:
- **F7a, on paper:** every phase at its time; the calendar's days; one main event at a time; nothing starts in a
  Friday hold or a guarded hour; the casts on shift or marked called in; the same run twice is identical; switch off
  = no event at all.
- **F7b, live:** jumps across each phase (skipTo forward, a Dev mode jump), a reload mid-phase and mid-meeting, the
  phase notes reach a reaction line, the device's Schedule shows the meeting, closed places hidden.
- **F7c, crowds:** draw calls at every gathering with about 60 crew (budget 450), at phone size; perf_check gains the
  storm's scenes (the front on Deck 3, the lantern supper in the mess, the party in the bow lounge), agreed with the
  Fridays plan's part G (its auditorium and lift-lobby scenes), plus **Day 12's address during the storm's onset
  routines**, the worst case.

Checks: the new check itself, perf_check, deck_check, check_fast.

### F8. Comms down (1 turn). Switch `EV_COMMS_ON`. Hooks in 20c (social engineer: OR1).

Section 20c blocks calls home only when `eventNow(t).phase === 'onset'` (two places, around lines 39548 and 39774).
With the switch on, both read `eventMod('effect', 'commsDown', t)`, so calls are down for any event that says so, in
every phase that says so (the storm: the front and the escalation, not just the front). The booths' "closed" routine is
already the event's. Outside Mail is held while comms are down and arrives at the all-clear (section 15's Mail:
player engineer, OR1), if the lead agrees; else F8 is only the calls.

Checks: social_check, events_check (no call during the escalation; calls rush at the all-clear), cadet_test off.

## Order, size and who reviews

| Turn | Piece | Owners asked | Checks besides check_fast |
| --- | --- | --- | --- |
| 1 | F0a calendar, due day, gatherings at load, Friday hold | none (18) | events_check, day_check 7/11/14 (on), cadet_test (off) |
| 2 | F0b called in | social (OR1): `SOC_CUE_OF.calledIn` | events_check, social_check |
| 3 | F1a `eventDay` | none (24k already reads it) | events_check, puzzle_check |
| 4-5 | F1b guard, F1c occasions | none (18) | career_check, leave_check, day_check 18/20 |
| 6 | F7a the check on paper | none (a new file) | the check itself |
| 6 | F2 phase notes | none | lines_check, social_check |
| 7-8 | F3a, F3b device | device (OR1); interactions (OR1) | device_check, interactions_check, shots |
| 9-10 | F4a, F4b skips, reloads | sim/save (OR1) | player_check, devmode_check |
| 11 | F5 rank parts | Works career (OR1) | career_check |
| 11 | F6 Dev mode | Dev mode (OR1) | devmode_check |
| 12-14 | F7b-c the check, live and crowds | performance (OR1) for perf_check | perf_check, deck_check |
| 15 | F8 comms down | social (OR1); player (OR1) for Mail | social_check |

About 13-15 turns, within the plan's 12-15. Patch reviews by PR2. intro_check (over 2 hours) runs alone, in pieces
(`--evening`, `--week`, `--firsts`), at the end of F0 and at the end of the base.

## The content formats (to agree with the events writer EW1 now)

Nothing new for the writers' tools unless EW1 asks:
- **Meetings:** `content/meetings/<id>.meet`, as today (the briefing, the all-clear, the oath scene, the greeting).
- **Reactions:** `content/reactions/event.<id>.<phase>.lines` with `@reactions event.<id>.<phase>` (the cue F2 makes).
  Called in: `content/reactions/calledIn.lines`, `cue:calledIn@me` (the speaker was called in) and `cue:calledIn`.
- **The event's own words** (address banners, Mail, news, the status line, the debrief): a bank file per event,
  `content/banks/event-<id>.lines` (`@bank all`), one `== event.<id>.<what>.<phase>[.<band>]` section per text, read
  with section 18's `quizText` (as the rec deck's Mail is). A text of several lines is numbered (`.1`, `.2`, `.3`).
  Until a key is baked, the words written in `SHIP_EVENTS` today are used, so nothing changes.
- The four Friday addresses are the Fridays plan's (`captains-address.trad`, the writer and the traditions engineer's
  format); the base only needs Day 12's to exist as a tradition the storm keeps.

## Questions for the user (each with a recommendation)

**Answered (the user, 2026-10-21, via lead 21): the recommended option on all three** (in design-doc.md, "Ship-wide events"). 1: skipped, decided once on the first load with events on and kept with the save (OR1's fix: never "the save's day at each load"). 2: 19:00-20:15. 3: the auditorium opens for the address.

1. **A save that's already past an event's day when events are switched on** (for example a save on Day 20 that never
   saw Crossing the Line): **recommended: it's skipped** (the calendar is the calendar; Dev mode can still start it).
   Other option: it runs at the next day that fits.
2. **The Captain's table on Day 20 and your night shift at 21:00** (the plan left it as "either"): **recommended: on a
   night-shift week the table starts at 19:00 and ends by 20:15**, so you go. Other option: your seat moves to the next
   table (Day 48).
3. **Two earlier answers meet on Friday Day 12:** the rec deck closes from the storm's front (14:00) to the all-clear,
   and the Day 12 address is held as usual in the rec deck auditorium (16:00-16:50). **Recommended: the auditorium (and
   the way to it from the lift) opens just for the address, the rest of the rec deck stays closed**, and the Captain
   says so ("we've opened the auditorium for this"). Other options: that week's address on the ship's speakers (banner
   and Mail), or on the plaza.

## Questions for the lead (answered by lead 21, 23:39 UTC)

Answers: F6's buttons come with Dev mode's Stop 3; F7 is a new `bigevents_check.py`, kept out of check_fast; F8 does
calls home only. User questions 1-2 went to the user; question 3 is on EW1's addresses page (the same clash).

1. F6: add the two Dev mode buttons (jump to phase, End and keep) now in a small "Big events" tab, or leave them for
   Dev mode's Stop 3 and test the functions from events_check? Recommended: with Stop 3, so two seats don't build
   the same tab.
2. F7: a new `bigevents_check.py` (recommended: events_check is already 6-10 minutes), and keep it out of check_fast.
3. F8: also hold outside Mail while comms are down (section 15's Mail), or only the calls? Recommended: only the calls
   now (the smaller change); Mail later if the user wants it.

## Loose ends noted for later pieces (not this base)

- **The storm update** must keep the Friday address in `pause`'s `keep`, exempt the Captain from the onset's double
  shift for 16:00-16:50 on Day 12, and keep the front's banner short (the 16:00 address is the full one; three
  addresses in the storm at most, as the design doc says).
- **The Fridays builder:** the address on Day 12 runs during the storm's onset routines (the bow lounge and booths
  closed, a share of crew staying in). The rec deck closes from the front to the all-clear, so the auditorium's
  opening for the address on Day 12 (user question 3) is built with the storm update.
- `EV_MAILBOX`'s comment says 20; its cap is 40 (an old note): fixed in F0a's commit if it touches the line, else
  left (backlog).
