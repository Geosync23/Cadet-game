# Handover: the Line builder (EV5), the Crossing the Line update

Written 2026-10-21 by EV5 (session_012DBTAAiTTNJYugQL4YLScJ) at about 520k tokens. A fresh session taking the role reads
this, then `plans/event-line-plan.md` v2.2 (on claude/event-plan-line ee590ed; the user's answers are in it and in
design-doc.md "Crossing the Line's answers"), then `plans/handover-storm-builder-2.md` and
`plans/handover-events-engineer-1.md` / `-2.md` (how the events base works).

## Role, branch, people

- **Role:** Crossing the Line, turns L1-L6 of the plan, in section 18 (its data block right after the storm's, and the
  slot `// ---- slot: Line builder`), with small hooks elsewhere. **Never set the build lines** (the build master does).
  Name each turn in a build-table row ("Crossing the Line update" table, plans/build-table.md).
- **Branch:** `claude/line-update` (from claude/storm-update; merge it in as EV4 pushes; last merged 5f3fc3f).
- **Lead:** lead 23, session_01XXiKm9iPgm565SZ4n1knmU (overnight: questions to the lead only, never the user).
- **Reviews:** PR4 (session_014WyaZtasY32m5fnkBxuR9d) every turn, also as the 4d/8b stand-in owner. PB
  (session_01FWW2piuXkFYaRRzLXZiqYb) owns sections 10/13/14 (and reviews the 16 hook). EC1
  (session_01QgShGXD6P24DDxTp8npN41) owns bigevents_check.py: never edit it, take it as is
  (`git checkout origin/claude/bigevents-check -- bigevents_check.py`). ER2 (session_01S8pboNujAzZgMSWFK84CxD) does
  the adversarial build review before L6 (switch-on).

## The switch

`const EV_LINE_ON = false;` in section 18 by EV_STORM_ON. L6 makes it `EVENTS_ON` (after ER2's review and the user's).
Off: `SHIP_EVENTS.crossingLine` doesn't exist, so the calendar passes over its row: cadet_test ALL IDENTICAL each turn.
Test copies: `sed -e 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/' -e 's/^const EV_LINE_ON = false;/const EV_LINE_ON = true;/'`;
for bigevents_check (it flips EVENTS_ON itself) a copy with `const EV_LINE_ON = EVENTS_ON;`.

## What's built

| Turn | Commit | What |
| --- | --- | --- |
| L1 | b01eaf0, 5c3c003 (pushed) | The event's data; `lineFirst`, `lineFirstCrew` and the cast slot `first:2`; the oath meeting; EV_BEATS `lineCeremony`; EW1/EW2's files moved into content/ and baked; facts.md bullets. Two events in the calendar: `eventNow` sees later calendar events (`evLaterSpans`), `eventAdvance` catches up every due event, section 14's galley-rota stint takes a meeting break. events_check's `EV_BEFORE`. |
| L2 + L3 | 94254b4 (+ design-doc, food_check and events_check fixes after it) | The ceremony's venue `bow-lounge-line` (`lineVenue`, first-timers' front pool, lead spots via `evLeadWhere`), standing easy (`lineEasy`, eventPlan `meet`), the lounge closed to all but the ceremony (`gather: true`), the Line supper and Lap dressed (`evDressed` `where`, `lineStandTray`), `linePudding`, extra 12; the gold mood and the `horn` feel (8b), DECK_DRESS `lineRibbons`, `linePlaque`, `lineCertificate` (4d), the horn's notice. Shots: plans/line-shots/. |
| L4 + L5 | 239c697 (pushed with 18d's backlog row) | Story A: `lineMoment`, Saturday's Tomas moment (else his Mail 22:50), the mug at his post, the Lap moment at 3-lap-6 while you walk it (TJ_WALK), the supper guess and Brennan's saved mug. Your part: two jobs on Sunday 12:45 (`day: 1`, `hold: 855`: section 17's eventJobsHour/eventJob), the sign-up sheet, Brennan's secret as you take the punch, the Record line with no score sub. |

## Test results so far (switched on unless said)

- Off: cadet_test ALL IDENTICAL and check_fast OK after every turn (L1, L2+L3, L4+L5).
- L4+L5 on: events_check, social_check, device_check, interactions_check, devmode_check, player_check OK; intro_check --week OK.
- perf_check on: the Line's scenes fine; its one PROBLEM (geometry +2 on round trips) is on the storm tip already (backlog 18d).
- events_check OK off, storm-only and Line-on (L1); L2/L3 Line-on FAILed only "no Mail for" the Line supper and the
  gathering: fixed in the check (they send none on purpose).
- day_check Days 6, 7, 8 OK; deck_check (on) OK.
- food_check Day 7: the garden FAILs were already on the base (EV3's note); the rota-vs-plans FAIL (Brennan at the oath)
  fixed in the check (an event meeting tag is a break).
- bigevents_check (Line on): only EC1's storm-first expectations and the guard row (asked EC1 twice, with the cases).
- Draw calls 390x844: horn 258, oath 308 (57 on deck), supper 271, plaque 262, certificate 151.

## Loose ends

- **Crowd size:** about 43 + you at the oath (the plan's estimate 50-60; "45 or more is fine"). About 10 who'd come were
  already mid-way through Winner Stays On or a leisure block (section 14 doesn't cut a block for a gathering). Told the lead.
- **Not built:** the punch "dunking" pose (the gathering's anim stays 'talk': one anim per gathering); Brennan offering
  the jobs in person (they're on the board and the sheet); a goal pointer to Tomas for the mug; Brennan saving *you* a
  mug if you miss the ceremony (the writers' punch.saved line is about Tomas).
- **My words (for EW's check):** the resolution status line, the ceremony's ask and thanks, the punch bowl's and
  the mug notice's tap/toast text. Lines_check PASS.
- **L6:** switch on, the full round (intro_check in pieces, `--week` alone), DEV_NOTES, ER2's review first.

## Gotchas

- Anything the data block calls at load must be a function declaration with its tables inside it (`lineVenue`: a
  const table in the slot was in its dead zone).
- `var EV_LATER`-style memo of evCalPlan is wrong (a check flips `draft` at runtime): evLaterSpans calls evCalPlan each time.
- Background checks: give `timeout: 7200000` (the default 30 minutes killed a chained run in perf_check).
- `pkill -f <pattern>` can kill your own shell; kill by PID.
- One browser check at a time; separate copies for each run; never edit the main file while check_fast runs on it.

## Messages that came in after the note (for EV7), 12:23 UTC

- **L4+L5 are pushed** (239c697, shots 0032351): all checks above OK. Nothing is left only in EV5's container.
- **PB's fix, NOT applied:** section 14's `evClosed` with `gather` rules checks only the stay's first and last minute, so
  a stay spanning the whole 14:30-15:15 window (a lounge seat 14:00-15:30) sits through the ceremony. Check every
  10-minute slot from abs to to-1 (evAt is per slot), then send it to PB.
- **EV6's storm change clashes:** claude/storm-update 829f242c removes `evStandTray` (the user made the lantern supper
  seated sittings). `lineStandTray` extends it. Ask lead 23 whether "seated" covers the Line supper; if so drop
  lineStandTray and the Line supper's `@gather-mess` standing places, and use EV6's `seated` mark in eventPools.
- **EW2's words** (claude/events-lines-2 af19fbe, plans/events-ready/crossingLine/content/banks/event-crossingLine.lines):
  copy over content/banks/event-crossingLine.lines and bake, then read the new keys with evWord, keeping mine as
  fallbacks: status.resolution, gather.ceremony.ask (3) and .thanks, tap.punch, notice.mug (EW2: only with
  flag:line.promised).
- **EC1's bigevents_check 3f9a458** has the Line cases (part 3b) and passes on 9188428: take that file.
- **PB's L2 watch-list:** each standing-easy 'meet' finds a spot (count who got there); Works job claims during the break
  (none in two places).
- **Reviewer:** PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i), not PR4. Merge claude/fridays 11b2220 per FR3 when doing S10.
