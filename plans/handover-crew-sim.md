# Handover: crew sim + social engineer X (session_01SNaWA6X5E9i2ZKfMnPTHJf), 2026-10-19

## Role, branch, builds
- Seat X, the crew sim (sections 14 schedules, 10 crew on the deck) and the social side (section 20). Branch `claude/crew-pt1`, build series **0.71.x**.
- Report to the lead (lead 17, session_016bN7x175WBwBL7S9xc2Lpb; was lead 16); hashes to the build master BM7 (session_01QbuzvT3TwzMwSWRmakzX8Z) and the reviewer R4 (session_01UGQxniXCxT5TLEE4tgRLfJ). Lines through the head writer W2 (session_01866TWKzGRgZmFcxiYRi4db).
- Builds (rows in DEV_NOTES' build table, after 0.55.x):
  - 0.71.0 crew walk up to start a conversation (`socialSeek` → `CrewAgent.seekStep`, kind 'seek'); mess-hall stuck fix (`crewWayOn`). Passed review.
  - 0.71.1 day shift 09:00-17:00 crew side (`SHIFTS.day`), breakfast 06:00-09:00, the Works 13:00 tea (`WORKS_TEA`, `worksTeaOn`), workaholics by 17:15, `NEWS_MAX` drops the least first, walk-up guards (`seekPrivate`, `seekBusy`). Passed review.
  - 0.71.2 (Step 3) the promotion's crew side: `playerBed()` reads `SHIP.works.home`; `crewScene`/`crewGather`/`worksGather`/`boxCarry`; `promoTick`; `ceremonySeat` (appointment `places`, saved); team-job talk (`teamJobOf`). Passed review (R3).
  - 0.71.3 (playtest 2, items 21, 22, 2, 8, 16, 13, 14): see its row. Last commit on the branch; announce state below.

## Playtest 2 (plans/brief-playtest2.md on claude/lead-pillar1): what's left
- **Done in 0.71.3:** 21+22 (wake 05:15-06:15, breakfast spread; bar staff keep the old wake), 2 (Calder seated at the arrival dinner), 8 (load/unload segs hold 'carry'), 16 (rower handle), 13 (beam: tap it or the floor within 2.5 tiles of 5-beam-1), 14 (everyone there welcomes you in turn, `BEAM_CHEERS`).
- **To redo: 21+22 per the user's detail (~05:20, via lead 16), arrived after 0.71.3 was built:** "Crew wake up staggered starts at 6 and increases. Must be earlier and varied. And not all members go straight to breakfast. But they must give themselves time to eat and get to work by 9 too." So: day-shift wake spread about 05:30-07:15, seeded per person (0.71.3 has 05:15-06:15 in `schedFrame`: `345 + 60·U(10) - 30`; widen it, keeping the bar staff's +45 and the 6-hour sleep floor `P.bed + 410`); after waking many do something first (wash/shower, dress, a short exercise or read, a coffee) before breakfast, others go straight (section 14's `morning(k, by)`: a gap filled by `wash` / `leisureUntil` before `meal('breakfast', ...)`; 0.71.3 spreads the breakfast start `by - 30 - 100·U(k+4)`); every day-shift member finishes breakfast and reaches work by 09:00 — add that to day_check (nobody late to their shift, nobody skips breakfast unless 'skips-breakfast'). Night shift and days off keep their own rules.
- **W2's names for 13-15:** 'beam.congrats' now also has an all-crew bank (anyone near the beam can welcome you; 0.71.3 already reads it). The queue texts for 15+20 are `queue.booth` / `queue.shower` ({nth}), `queue.next`, `queue.go`; the fresh seat also owns showing them (U is handing over).
- **Not started: 15 + 20, the call-booth and shower queues** (X builds the queue; U, the HUD seat session_01FcMPTX7mMTHkyr4pxDfNcS, shows "You're 2nd in line"). Agree the data shape with U first. Pointers:
  - Crew already queue for showers on paper: section 14's `showerQueue` (a wait of `SHOWER_Q`+ minutes becomes a 'shower-queue' stop, tag 'showerq', at a `shower-queue` place if the deck architect made them, else standing inside the washroom door). The booths (`callhome` places on Deck 3) have no queue: `take('callhome', ..., { wait: 20 })` just waits where they are.
  - The player's side: the servery line is the model to copy (`LINE`, `lineJoin`/`lineLeave`/`lineSpot`, section 10 + section 15's `queueHeld`). A small live queue per booth row / washroom: crew whose whereIs is a wait for that place type stand at the queue spots in order; the player joining gets a place; expose e.g. `queueOf(kind) -> { ids: [...], you: index | -1 }` for U's message.
  - Check with day_check (nobody stuck, places not double-booked) and perf (draw calls in the washroom).

## Announce state at handover
- 0.71.3's checks: day_check OK, food_check OK, events_check OK (after the bar-staff fix), join_check OK (after keeping the leader's "tap the beam" as T designed), intro_check: running on the build before the join fix (`intro_check.py` updated: the Chief is now expected AT your table when the dinner chat begins). cadet_test: Deck 4's morning crew differ (the wake/breakfast move); a copy with that reverted is ALL IDENTICAL. deck_check: only "Deck 4 memory changes between round trips" (geometries 373 ↔ 389, back to 373 each other trip, at 06:02 Day 1): not a leak — more crew are up then and story crew near you get a full rig, freed when they leave; with the wake change reverted it's steady. Explain it, or change the check's time.
- If intro_check isn't reported yet: run `CADET_CHROME=/opt/pw-browsers/chromium python3 intro_check.py starship-cadet.html` (long: an hour or more on a busy machine) and send the result.

## Gotchas
- `pgrep -f <name>` in a wait loop matches the loop's own shell: wait on a log line instead.
- Run browser checks one or two at a time; more and they fail with "game failed to start".
- `SHIP.works.home` defaults to 'bunk' (C2): `playerBed()` accepts only a Deck 4 bed id.
- Stage directions (`crewScene`) are live only; escortPlanOf asks section 21's escortPlan and C2's worksEscort first.
- Appointments' `places` is the only new saved field of the seat (social_check 14b round-trips it).

## Open questions for the user
- None outstanding from this seat.
