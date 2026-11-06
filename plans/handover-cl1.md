# Handover: CL1, traditions calendar, arrows and the Captain's address (0.99.7 playtest patch)

Role: build the user's 0.99.7 notes 14, 15, 16, 20, 23, 26, 27, 30, 31 and 47 (plans/patch-0997.md on claude/lead-49).
Lead: lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Reviewer: RV33 (session_01GKuymoAK9gACR31MRd1CMX).
EV1 (session_01GKuymkhvqRE7N1Rj4VMtWD, claude/p997-events) owns what's on the first Thursday and Saturday; CL1 owns the
calendar rules. They agree directly, copying the lead.

## Branch and builds
- Branch claude/p997-calendar, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8).
- One switch: `CAL997_ON` (section 13, next to TRAD995_ON): `URL_FLAGS.has('cal997')`, so off by default; `?cal997` or
  `#cal997` previews it. Off = 0.99.6 exactly (cadet_test ALL IDENTICAL). The build master switches it on with
  `true ||` as for TRAD995_ON. The build-number lines are untouched.
- Build-table row "p997-calendar A".

## What it does (all behind CAL997_ON)
Code: slot 'Calendar builder' (section 18, after 'Vessel sky'), plus small hooks:
- 13 `tickShip`: the clock runs at `CL997_RATE` (0.6) while set.
- 14 `recHostEarly` asks `cl997HostEarly` (an early ship tradition's host wakes for it); `schedFrame`'s bed: that host to
  bed in time the night before; `eventFree`: before 10:00 you count as up only after bedtime + 6:50 (the plans' own
  sleep floor).
- 16 `galleyBirthdays`: crew cake only on a party day (yours always).
- 18 `eventsOn`: birthday only on `cl997Party(d)`; late piano never on a day after it was due; `cl997Clash` drops a
  tradition overlapping your fixed items (into EV_DROPPED). `evBdaySlot`: window `EV_BDAY_997` (19:00-20:00 starts,
  nearest 19:00), and Day 4's quiz never gives way. `upcomingTraditions`: a room for traditions whose places span rooms
  (`cl997Room`), so heads-ups have an arrow. `weekMail`: the birthday line's real time. `eventsTick`: `cl997RateFrame`
  (each frame, before 18f's tick) and `cl997LeadMinute` (each minute).
- 18f `friAddressTick`: the bubble's length divides by the slower rate.
- 19 `devDay`: Day 3's 'The crew store' beat item not listed.
- At load (slot): Saturday run taken out of SHIP_TRADITIONS; Pick-your-own's who doubled; the jam's who 0 for Marrow on
  a night next to late piano; the swap meet's Mail signed Oona Zielinski.
Words: content/banks/calendar-997.lines (cal.lead.<id>, cal.address.title, cal.address.call), stand-ins for the writers.

Per note: see the build-table row and design-doc.md (Traditions: weekly list, birthdays, joining in, not too much at once;
the Saturday run's cut record; the Captain's address paragraph).

## Party days (note 47), the first year
4, 22, 41, 62, 77, 94, 123, 147, 169, 188, 211, 226, 241, 256, 276, 293, 307, 331, 354 (19; were about 80). Never on a
Friday (a Day 19 party at 19:00 dropped the Works tea, so the first Works tea would have been Day 33).

## Gotchas
- Only `var` and function declarations in the slot: eventsOn and the planner can run before the slot does at load.
  INTRO_WEEK (section 21) is made later, so the two beats' times are copied as numbers in `cl997Beats()`; the probe
  below checks they still match.
- `calClash` already exists (section 19's Calendar): my names all start cl997 / CL997.
- events_check.py knows the party rule (a birthday is due only on a party day with the switch on).

## How to test
- Switched-on copy: `sed "s/const CAL997_ON = URL_FLAGS.has('cal997');/const CAL997_ON = true || URL_FLAGS.has('cal997');/"`.
- Probes in the session's scratchpad were: the calendar Days 0-35 (eventsOn per day, dropped), the arrows (Day 3 06:02-06:22,
  Day 6 09:20, Day 5 15:25-16:10 with the rate), goers per early tradition. Kept as plans/cl1-probes/ (see there).

## Open questions for the user
- 27: the slower clock in the auditorium is the default; the other way is shorter speeches (about 13 lines; writers).
- 15: taken as the Day 3 store visit on the Schedule and the swap meet's Mail signature (the lead's call); nothing else
  shows the store as a tradition.

## Loose ends
- Backlog CL1-1 (This week aboard's 20:15), CL1-2 (crew at the piano late), CL1-3 (early goers who never get up).
