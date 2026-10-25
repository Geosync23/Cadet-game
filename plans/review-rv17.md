# RV17 review: FX22's appointments (0.92.6 item 9)

Reviewer RV17 (session_01CBbf1dZKv1LCrACof9HgyP), hired by lead 36. Notes only, branch `claude/review-rv17`.
Builder FX22 (session_013hfW44u1PvirfEXtYYtwVF), `claude/p926-fx22`.

## What was reviewed
- First pass on **582a3544** (game sha256 1389038c...), then **eaaa6446** (game ce0f6595...; FX17 173f21ed merged,
  `apptScene(b, now, e)` -> `cardWhere(e)`). staging's promo-sight.lines not merged yet when this was written.
- Diff read against FX17's base 4eab8c9f: the switch line, the Record and Appointments app hooks, `evOneOffDefs` (`only`,
  `appt`, `toBed`), the `eventJoin` and `eventsTick` hooks, `tradJoinable`, the LINES and APPT_WORDS blocks, and the
  whole "Appointments builder" slot.

## Rules
- Nothing at load calls `R()`. Invitations use `schedU(idHash(host), ...)` (a hash, not the random stream). All the
  slot's setup (TRAD_JOIN entries, the feast spots, the garden sign) is inside `if (P926_APPT)`.
- Colours: the sign's two boxes go through `dressBox` -> `dressMat` -> `col()`.
- Coplanar: the board's back is 0.008 in front of the stake's face. The stake's bottom face sits at floor level but faces
  down (hidden, culled), like other dressing.
- Draw calls: two meshes on Deck 3 once the bed is planted (184 calls in the garden at phone size).
- Save: `save.ship.apptx` only with the switch; capped (30 bookings, 10 offers, 40 told, 12 days per kind:host).
  Worst case about 16 KB. player_check --long on the switched-on copy (both switches): largest 127.6 KB on Day 188,
  SAVE BUDGET OK, so even the worst case stays far under 250 KB. One-offs are saved through the existing last-20 list.

## Checks
| Check | Build | Result |
|---|---|---|
| cadet_test vs 0.92.5 (staging-0.92.5 39f7741d, game fddc0ef6) | 582a3544 off | ALL IDENTICAL |
| cadet_test vs 0.92.5 | eaaa6446 off | ALL IDENTICAL |
| check_fast | 582a3544 | QUICK CHECK OK |
| appt_check (all parts incl. off and planted) | 582a3544 | APPT CHECK OK (171 ok; both planted faults fail their part) |
| appt_check | eaaa6446 | see the end of this page |
| check_fast | eaaa6446 | see the end of this page |
| events_check (28 days) | 582a3544, both switches on | EVENTS CHECK OK |
| lines_check | 582a3544 on | PASS (0 errors, 66 old warnings) |
| day_check Day 5 and Day 19 with 7 appointments planted on each (shadow, Brennan, teach me, scope, feast, night round, garden) | 582a3544 on | DAY CHECK OK, both |
| player_check --long | 582a3544, both on | SAVE BUDGET OK (127.6 KB max) |
| My booking matrix: every kind x host from Days 3, 9, 16, 23, 33, 47 | 582a3544 on | every host books when the schedule allows; the only misses are the storm week and Cruz's busy Saturdays (fine) |

## Played at phone size (390 x 844), real taps
Scope (Sato), An hour with the Watch (Holt), Teach me (Rina), Brennan's book, Show and tell (Zeke's cabin), Midnight
feast (Bunk 1), A bed of your own (Cruz), the night round (Mensah, all 7 decks), the real talk at a plain appointment
(Alejandro Reyes). Real screen taps on Holt, Brennan, Tomas and Mensah opened the scene; the Accept button and the
"What for?" row work as taps. Hosts show up, scene lines are in order and filled, kept goes in the Record, the Mail comes
the evening before (or that day for tonight's). Night round: the seven stop lines once each, on the right decks, then the
scene. Screenshots: /tmp/rv17/shots (not in the repo).

## Findings (priority "next")
1. **Doorway (fixed in eaaa6446).** On 582a3544, tapping the host from the doorway and walking in closed the card at the
   next ship minute and counted the appointment as kept with most lines unread (Teach me, Brennan, feast). eaaa6446
   passes the one-off to `cardWhere(e)`: retested, the card stays open all the way in for all three.
2. **Save and reload in the middle of a scene loses the appointment.** Scope: tapped Sato, card open, saved, reloaded:
   the card is gone, `SHIP.events.joined` already has `appt-scope@4`, so tapping Sato again does nothing
   (`tradJoinTap` false), and at the end the booking turns to missed (`gone: 1`) although you were there.
   Suggest: let a tap rejoin an appointment whose booking isn't done (skip the joined test for `e.ev.appt` while
   `apptBooking(e, d)` is open), or keep the booking at its end when you joined it.
3. **No heads-up for appointments during your shift.** Booked one-offs are `kind: 'tradition'` in the Schedule, so
   `devHeadsTick` (section 19, the "on shift: a quiet badge" line) only adds a calendar badge for Brennan's book (14:30)
   and the shadow hours inside your shift (Nandakumar 09:30, Holt 10:00, Mori 14:00). Also, with heads-ups switched off
   in Settings, things you're booked for still remind you (`x.kind === 'appt'`), but these are skipped as traditions.
   The design says your appointments always remind you. Suggest: in `devHeadsTick`, treat a `tkind` starting `appt-` as
   an appointment (always a strip, even on shift or with heads-ups off), like the beam's exception.
4. **The host can leave before the booked time is up.** `apptBookIt` checks the host is planned there at all, not for
   the whole slot. Seen: Sato on Day 48 planned 18:57-19:15 for a 19:00-19:30 scope turn (then washing); Cruz on Day 41
   10:00-10:14 for the 10:00-10:30 planting; Zeke on Day 34 washing at 19:50 in a 19:15-19:55 lesson. Arrive at 19:20
   and she's gone. Suggest: require the host's segment to cover from to to-10, else try the next slot.
5. **Record repeats.** `apptRecord` lists each kept booking: the garden's "Grew your own bed of lettuce in the garden."
   shows right after the planting (weeks before any lettuce) and once more per visit; a weekly scope or lesson repeats the
   same line. Suggest: one row per kind and host (latest day), and the garden's line only at the harvest.
6. **Two bubbles from Mensah at once.** On Deck 5 his stop line and his ordinary chatter ("Rina won at Tiles night, of
   course.") were up together. Suggest: hush his chatter while the round runs.
7. **Small, optional.** (a) `b.waits` is saved, so after a reload between 22:25 and 22:30 Mensah doesn't wait at the
   bench again; (b) a reload mid-round ends the round and the booking turns to missed (your notes say "a reload ends it",
   fine, but with 4 stops done it could still count); (c) the Accept/Decline buttons carry an index into `X.offers`, which
   `apptHour` filters each hour, so a screen left open across the hour could answer a different offer; (d) the Record
   hook moved the "section 18's ship-wide events" comment onto the new line, and `apptScene`'s line has two comments.

## Verdict
**FIXES NEEDED (small).** Everything works and every check is green; the switch-off build is pixel-identical to 0.92.5.
Before switch-on: 2 and 3 (a player can lose an appointment or miss it), and ideally 4-6. 7 is optional.
