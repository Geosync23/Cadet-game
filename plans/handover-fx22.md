# Handover: FX22, appointments (0.92.6 item 9)

Role: builder for patch 0.92.6 item 9, "Need more interesting appointments" (the user's answers on page CTLouY4DK2gFuWBF8YwS3L: yes to the cheap fix and nine appointments, no to the spare helm chair; "Appointments work almost exactly the same as ship traditions but are usually one on one or very small group").
Lead: lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi). Reviewer: RV14 (session_01RwUYVcYt2PP7B7g3ogduFZ). Words: SW2 (session_01E4qPjPEbEsohiaqRLm3Nyb), checker CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v). Build master BM17 (session_01WxdNuUeTUoneMvqKiF6GQL). FX17 (session_01YKeSjUhEnJRbmjyHz2aa6u) owns the 0.92.6 traditions changes.

## Branch and builds
- `claude/p926-fx22`, from 53c11f8 (frozen 0.92.5), with FX17's claude/p926-fx17 d1097923 merged (lead 36: build on top of FX17, merge each later tip) and SW2's claude/p926-appt-words f5e86e8b merged.
- T1 6765153d (bake, switch, cheap fix), T2 c684a606 (engine + Brennan, scope, teach me, shadow), T3 5448b119 (show and tell, rehearse, feast, garden bed), T4 f9712154 (night round), T5 (appt_check, docs): see git log.
- Switch: `const P926_APPT = URL_FLAGS.has('appt')` (section 13, next to FX17's P926_TRADS). Off = the game as before (cadet_test vs 53c11f8 ALL IDENTICAL every turn). Preview with `?appt`.

## What I own
- content_gen.py: `parse_appt` (content/appointments/*.appt -> the `APPT_WORDS` block, markers after FRI_ADDRESSES) and `meet_line` (the .meet reader's line parser split out; its output unchanged).
- The slot "Appointments builder" (section 18, after the Line builder's slot): all the code. One-line hooks elsewhere, each guarded by P926_APPT: eventsTick (apptFrame), eventJoin (apptJoin), tradJoinable (an appointment one-off), evOneOffDefs (`only`, `appt`, `toBed`; absent = as before), the Appointments app (apptActX, apptViewX), the Record (apptRecord).
- Shapes: SHIP.apptx (saved as save.ship.apptx, only with the switch) = { book: [{ id, kind, key, host, guests, day, from, to, done, gone, aid?, mail, mailAt, mailed, waits?, shown? }], offers: [{ kind, host, day, from, to, made, status, said }], kept: { 'kind:host': [days] }, told: [booking ids], declined: { 'kind:host': day }, offerDay, garden?: { stage, due } }.

## How it works (short)
- APPT_RULES per kind: hosts, tier, once (true / 'week' / 'host'), path ('appt' = overlay), where, onShift(host, d), anyDeck, times(p, d), key, guests, toBed, days, today.
- Booking = a one-off tradition (eventOneOff, a later day) with `only` the host (or nobody when the host is at work for it, or the bunkmates); verified after booking (the host planned there), else undone (apptUnbook) and the next candidate tried (apptTry over apptSlots).
- Overlay ones (show and tell: a locked cabin; rehearse: tonight) are device appointments (apptAdd) with `appt` on them; the scene when kept and the host is near (apptOverlayFrame).
- Join: tap the host (TRAD_JOIN 'appt-<kind>') -> eventJoin -> apptScene (the scene as a meeting script; `where` = the room you're in) -> its end -> apptKeep.
- Night round: crewScene 'wait' then 'follow' for Mensah; stop lines per deck (apptRoundFrame).
- Cheap fix: apptTalkFrame on kept plain appointments.

## Loose ends / asked
- SW2 asked to reword midnight-feast's ask line "Quarter past ten" (the feast is at 22:00). Merge their fix and re-bake when it comes.
- FX17 told: dialogueShow with no `where` is closed by meetingsTick at the next ship minute (their week1Card / swapCard / spiceCard).
- Brennan's Wednesday dish: words only (lead 36), no menu change.

## Gotchas
- performance.now is not the checks' clock: pace in ship minutes.
- A one-off can't be today (eventOneOff); a tradition the host goes to at that hour wins over the appointment, so apptSlots skips those hours; ship-wide events pause one-offs (the storm, Days 11-16), so apptSlots skips paused hours.
- DECKS[n].lift is a tile inside the car; step out to a lobby tile in tests.

## How to test
- `python3 appt_check.py starship-cadet.html` (switch on in a copy; off copy for "nothing happens"); cadet_test vs 53c11f8 (off); names_check; content_gen --check; lines_check.
