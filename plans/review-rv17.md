# RV17 review: FX22's appointments (0.92.6 item 9)

Reviewer RV17 (session_01CBbf1dZKv1LCrACof9HgyP), hired by lead 36. Notes only, branch `claude/review-rv17`.
Builder FX22 (session_013hfW44u1PvirfEXtYYtwVF), `claude/p926-fx22`.

## What was reviewed
- Final sha (lead 36): **eaaa6446**. First pass on **582a3544** (game sha256 1389038c...), then **eaaa6446** (game ce0f6595...; FX17 173f21ed merged,
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
| appt_check (all parts) | eaaa6446 | APPT CHECK OK (171 ok; both planted faults fail their part) |
| check_fast | eaaa6446 | QUICK CHECK OK |
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

## Re-review of the fix sha 6b03bea7 (game sha256 84819518...cbe1)
FX22's fixes for 2-6 and 7 (a), (c). Diff read: every change is behind P926_APPT.
| Check | Result |
|---|---|
| cadet_test off vs 0.92.5 | first run: only a_start differed (14812 px), the known timing-sensitive first shot (backlog FX17-2), on a busy machine; run again alone: ALL IDENTICAL (1-level noise) |
| check_fast | QUICK CHECK OK |
| appt_check (all parts, now with lines for 2-5) | APPT CHECK OK (183 ok; both planted faults fail their part) |
| events_check (28 days), switch on | EVENTS CHECK OK |
| 2: my reload probe | joined, saved, reloaded: a tap on Sato reopens the scene; read through: kept, one Record row |
| 3: heads-up probe (Brennan 14:30, on shift, Accept tapped on screen) | the strip comes at 14:15 on shift, and with heads-ups switched off too |
| 4: booking matrix again | every single host now covers the slot; the only new miss is Cruz's garden from Day 33 (its one Saturday no longer passes; the invite comes later), fine |
| 6: night round at phone size | the seven stop lines only; no chatter bubble beside them |
Left (lead's question): a reload in the middle of the night round still ends as missed. Not a must-fix: a missed
round isn't counted as kept, so Mensah can invite you again; nothing is lost.

## Final verdict: PASS at 6b03bea7.

## Re-review of FX22b's bae25ae7 (game sha256 ad896a8d...d6df; lead 36: this replaces 6b03bea7)
Diff 6b03bea7..bae25ae7 read; all new lines behind P926_APPT; the tradJoinTap line returns false as before with it off.
| Check | Result |
|---|---|
| cadet_test off vs 0.92.5 | under load only a_start (known FX17-2 flip); alone: ALL IDENTICAL |
| check_fast | QUICK CHECK OK |
| appt_check all parts incl. `fixes` | APPT CHECK OK (210 ok; planted faults caught) |
| events_check, switch on | EVENTS CHECK OK |
| my reload probe: scope (Sato) | joined, saved, reloaded: a tap reopens the scene; kept; one Record row |
| my reload probe: Brennan's book | **FAIL**: after the reload a tap on Brennan does nothing; at the end apptOver keeps it, but the scene (and your dish choice) never comes |
| my reload probe: night round | **FAIL**: after a reload Mensah waits at the bench again, but a tap does nothing (stop 1 walked, `ri: 1` saved), so the round can't resume and ends missed |

**Finding R1 (new).** The rejoin needs the one-off from the tap. `tradJoinTap` gets it from `eventOf(a.p)` (only when
the host is planned there: Sato, the teachers, Cruz) or from `TJ_NOW.lead`, and tradJoinMinute drops a joined tradition
from TJ_NOW. Hosts at work for it (`only: []`: Brennan, the five shadow hosts, Mensah) have neither after you've joined,
so `apptRejoin` is never reached. Suggest: when `e` is null and P926_APPT, look for today's appointment one-off on now
whose open booking's host is `a.p.id` (`eventsOn(d).find(x => x.ev.appt && (apptBooking(x, d) || {}).host === a.p.id)`)
and use it. Re-test: reload mid-Brennan and mid-round, tap the host, the scene / round goes on.

Verdict on bae25ae7: **FIXES NEEDED (one small)**: R1. Everything else passes.
Note (BM17, 13:18 UTC): 6b03bea7 (passed 11:24) is already on staging-0.92.6 (merge 2f0c29de, P926_APPT off); bae25ae7
held locally; BM17 merges the next sha I pass on top.

## Re-review of dd4d8797 (game sha256 23ad7d70...f008): R1 fixed
Diff bae25ae7..dd4d8797: `apptHostEvent` (slot) and one guarded `||` in tradJoinTap (off: unchanged).
| Check | Result |
|---|---|
| cadet_test off vs 0.92.5, alone | ALL IDENTICAL |
| check_fast | QUICK CHECK OK |
| appt_check all parts (new Brennan and round reload lines) | APPT CHECK OK (223 ok; planted faults caught) |
| events_check, switch on | EVENTS CHECK OK |
| my reload probe: Brennan | mid-scene, save, reload, tap Brennan: the scene opens again; read through: kept, one Record row |
| my reload probe: night round | stop 1, reload, Mensah back at the bench, tap: the round goes on from stop 2; reload again after 5 stops: kept at its end |

## Final verdict: PASS at dd4d8797 (replaces the earlier PASS at 6b03bea7).

## Other reviews for lead 36 (2026-10-25 afternoon)
- **FX17 Day 7 Line fix** claude/p926-fx17 3e8c78a6 (+ check-only eba4d365; game 10f654de...): **PASS**. cadet_test vs
  9d758ada ALL IDENTICAL; bigevents, p926 (new 7 line), events, day_check 7 OK; mech_check m17 OK on 9d758ada and
  3e8c78a6 with eba4d365. Goers Days 1-112 old vs new: only rec-wso Day 7, 11 -> 8 (Marrow, Cruz, Walsh: the Line cast).
- **FX22b join_check** claude/p926-fx22b-join 3d011393 (test only, game 88f4cc8d = 9d758ada): **PASS**. JOIN CHECK OK
  with all switches on (the scope booked, a tap on Sato, the scene to its end, kept) and with P926_APPT off; the old
  check on the same game FAILs "appt-*: not on in 400 days" (the check, not the game).

## 0.93.0 sound reviews for lead 37 (2026-10-25 evening)
Base 0.92.6 = claude/integration 5898c190 (game 10f654de...).

### FX20 activity sounds: PASS at claude/sound-act 7e63f194 (game 84290839...; 0.93.0-a.5)
- Code: section 27's activity slot; Math.random only (`rand`/`pick` inside SND); nothing runs without an AudioContext
  (S.frame returns at once), so checks stay silent; hooks (actBegin/actEnd, clockPunch, tapCrew, deviceAddress, wsFinish)
  are one line, try-wrapped, read-only; activity sounds are the player's own ACT only (crew never go through actBegin).
  Room ambience (galley sizzle/chop, laundry washer) only while you're in that room, read-only (machineLook, DECK_CREW).
- 81aa8a35: cadet vs 0.92.6 ALL IDENTICAL, sound_check, check_fast, day 1, interactions, events OK; player_check's 3
  reserved-job FAILs identical on 0.92.6 (old). Planted: shower loop removed -> sound_check FAILs.
- Scope (lead 37): ~18 approved sounds were missing; 9aa5098a added them, dryer/airlock/shuttle bay on audio-todo.
  9aa5098a: cadet ALL IDENTICAL, sound_check, check_fast OK (FX20: interactions OK).
- The user's ask (blanket follow-up after getting straight up): 7e63f194 cancels follow-ups on any begin/end; cadet
  ALL IDENTICAL, sound_check OK (new case).

### FX22b music + Music app: PASS at claude/sound-music a4ac9e31 (game 6b5f15c9...; 0.93.0-m.2)
- Code: v7 module in the music slot (Math.random + per-track seeded tunes); prefs only in starship-cadet-sound
  (SND.prefs.music; savePrefs skips under nosave); clock read-only (day, min, clocked in); made on the first running frame.
- cadet vs 0.92.6 ALL IDENTICAL, sound_check OK (core + music), check_fast OK, day 1 OK.
- Played at phone size with ?sound: evening plays Evening star (Ship schedule: music for the evening); Choose a track ->
  Quiet stars on repeat; Next -> Nebula; Ship schedule back; Low; Off; the game save has no music data. Music tile next
  to Hobbies (text glyph), grouped track list readable, no sideways scroll. Day 0 quiet is covered by sound_check (my
  test page opens on Day 1). Not measured by me: levels under the hum (SD1's Sound Lab numbers; no levels check exists).

### RV16 arrows_check promo fix: PASS at claude/fix-promo-arrow 32374ef3 (test only; for 0.93.1)
Game byte-identical to staging-0.93.0 4f1e52bf (97f21893...). New check: promo OK, printing "the test job led by the board
arrow naming it (shift:job:9, Day 9 09:15), not promo:test"; the old check on the same game FAILs "never led with
promo:test". The new condition still needs the label to name the Tier 2 test job AND the job to be takeable (guideTakeable),
so 08:01-09:00 (label up, job not yet on the board) doesn't count; the other three beats unchanged.
