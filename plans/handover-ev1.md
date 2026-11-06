# Handover: EV1 (0.99.7 playtest patch: new events and the first week's shape)

Role: EV1, builder for lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Reviewer RV33 (session_01GKuymoAK9gACR31MRd1CMX).
Branch `claude/p997-events`, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8). The user's notes 8, 34,
36 and 46 (their words: plans/patch-0997.md on claude/lead-49). CL1 (session_01GKuymjnwwEESL9W6V7kQFK,
claude/p997-calendar) owns the calendar rules; we agreed times directly (below).

## What I built (all switched off; off = cadet_test ALL IDENTICAL against 0.99.6)

| Switch | Note | What it does |
|---|---|---|
| `EV997_LIGHT_ON` | 8, 34 | **The Last Light**, a short ship-wide event (calendar row Day 3, before the Line). Wed Day 3 18:00 Vance's Mail; Thu Day 4 chatter from 07:00; 14:00 the Captain's address; 14:00-14:30 Dr. Sato's gathering at the bow glass (`lastLightGlass`, k 369, tap Sato to join, the day shift standing easy, the bow lounge theirs 13:40-14:40), her talk and the crowd's in bubbles (`lightSay`). Phases warning/passing/afterglow (never onset: eventDay(4) stays false). |
| `EV997_SAT_ON` | 36 | **The first Saturday (Day 6):** Line day-0 dress rows: garden hour dropped that day; added Paddle club 14:00-15:00 (rec deck, Holt, a small pull), Window sketching 09:45 (Deck 2), the big jigsaw 10:35-11:40 (Deck 1), Every song 17:15 (Deck 4). Day 7 untouched. |
| `EV997_READ_ON` | 46 | **Reading corner reads The Lighthouse at Coriel:** Day 7 Esme hands it round (her wrap line); Days 21, 35, 49, 63 four parts in bubbles (content/meetings/readStory1-4.meet), your question card when joined (flags read.s<N>.<k>), your answer recalled next part (readStory<N>.recall.meet). Four regulars pulled on those days. |

Where: data block for the Last Light just before the EV_SHIPWIDE loop (section 18); everything else in the slot
`// ---- slot: Events 0.99.7` after 'Visit dinner'; one-line hooks in readSay, p926Frame and tradJoinable. Words:
content/banks/event-lastLight.lines, ev997-saturday.lines, reading-corner.lines (read.story.*), join.lines
(join.lastLightGlass.*). DEV_NOTES "The first week's shape and the reading corner's book"; design-doc (events
calendar, weekend traditions, reading corner, open questions with my defaults).

## Agreed with CL1
Day 6: harvest and sowing untouched; the paddle moved to 14:00-15:00 (garden hour's freed hour; at 07:00 only Holt came once merged). CL1 adds the Last Light as a
fixed item (13:50-14:40, a guard) and a lead arrow 13:45-14:15 to the bow lounge, let through on shift.

## Check edits (check-side, for their owners to see)
- bigevents_check: `LIGHT` list: a late save passes over the Last Light with the Line (only when the switch is on).
- events_check: the Sowing decor test looks only at its planted decor; a New game on Day 4 may have the Last Light running.

## Loose ends
- Backlog EV1-1: a tap to join stands the person up for the rest of it (lead gave it to TB6). My reading talk works round it.
- lines_check warns on the book's names (Ada, Quill): fictional, expected. "The Last Light" is a new name for facts.md (head writer).
- The regulars don't always come (rota, other plans); their lines are read by whoever's there.

## How to test
Copy with the switches on: `sed -e 's/^const EV997_READ_ON = false;/const EV997_READ_ON = true;/' -e 's/^const EV997_SAT_ON = false;/const EV997_SAT_ON = true;/' -e 's/^const EV997_LIGHT_ON = false; /const EV997_LIGHT_ON = true; /'`.
Then bigevents_check, events_check, day_check 1-14, stories_check 36, fridays, weekend, join; probes in plans/ev1-probes/.

---

# The earlier EV1 notes (kept as they were)

# Handover: EV1, events engineer (the Diplomatic visit switched on)

For a fresh session taking over the events seat. Written 2026-10-28 by EV1 (for lead 43, then lead 44).

## Role, branch, builds
- Events engineer: section 18 (ship-wide events), its slots, and the event checks (events_check.py; bigevents_check.py is EC1's).
- Branch `claude/visit-on`, from `claude/staging-pad` e158dcf (0.95.0 plus the controller waves, PAD_ON off). Final commit a1917dd (game last changed in 8c91437). RV25: PASS. BM20 is merging it into the controller switch-on round. Build-table row: `0.95.0-vis.1`.

## What I built (the user, 2026-10-28: "Turn it on")
- **The visit runs in a real game, Days 16-19.** It had `draft: true` since 0.93.2, so the calendar passed it over even with `EV_SWAP_ON` on. The event-swap block (section 18, `if (EV_SWAP_ON) {`) now does `if (EVENTS_ON) delete V.draft`. Without the storm update or the swap it stays a draft.
- **Times on Friday Day 19:** the gift exchange is at 09:00 and the farewell at 09:30 (they were 08:20 and 09:00, when the Captain and Saruth were still at breakfast). The Veyli leave at 10:00 (GUEST_AT, section 14).
- **Farewell places:** the farewell uses `places: [{ deck: 5, pool: '@gather-shuttle-bay' }]`, because the bay has no seats (before, it had 0 places).
- **`eventGuestDays`:** if the event isn't running, logged or due, it falls back to `evCalPlan()`. Plans made early then show the Veyli aboard Wednesday 10:00 to Friday 10:00. Taavek's days, for the Veyli vessel, now show on paper from Day 1 the same way.
- **xp (lead 43, option b):** in the swap block, `onSim('job')` adds `SHIP.works.tier - 1` when you turn in a `j.event === 'diplomatic'` job, so the visit's jobs earn your tier's worth. A steady Senior is Trusted by Day 19 again (60).
- **Words:**
  - The greeting's gist says "until Friday".
  - Teshavi is they/them ("the Speaker's aide", "they have rarely been made so welcome").
  - One formal dinner: content/reactions/guests.lines, the debrief, and the thread label "The dinner on time".
- **Kept as designed (lead 43):** the greeting day, Day 17, pauses that day's evening traditions (`pause: ['onset']`).

## Checks changed
- **events_check:**
  - The visit runs as the build has it. If it is still a draft, the check is skipped, or failed when the swap is on.
  - The storm's paper run stops at its own end.
  - The live storm may be followed by the visit.
  - On Day 16, eventOn shows the visit's warning.
  - Rec-deck days paused by an event are allowed for.
  - An event guest's own `ev-<event>-...` steps aren't counted as traditions.
- **bigevents_check (EC1's file, reviewed by RV25):**
  - Someone with no rota (Saruth, a guest) is never "off" or called in.
  - A guest arriving off the shuttle (`tag: 'arrive'`) counts as at the greeting.

## Loose ends
- **Backlog after 0.96.0 (RV25 note 1):** the xp listener's comment says section 24 pays first, but it's registered earlier and runs first. The xp total is the same, but the reputation toast could show twice.
- **Possible follow-ups (lead 44 has them for the user):**
  - A seated formal dinner. Today Day 18's dinner is only the galley's 10 extra meals, and nobody sits in the Captain's quarters.
  - A nod to the visit in the Veyli vessel's words (Days 27-30). Today they neither assume nor deny it.
- **Old failures, also on e158dcf:**
  - career_check: "busy: Relied on before Day 5".
  - events_check: "not reached farouk-olu>3-lounge-28 16:00" (reading corner, Day 7).

## Gotchas
- Four checks at once on a 4-core container makes pages time out on load (Page.goto 30000 ms). Run at most 2 or 3 at once, each in its own CADET_WORK.
- `pgrep -f` / `pkill -f` patterns match your own shell's command line: don't wait on a pattern that's in your own command.
- Run cadet_test from a scratch folder: it writes screenshots into the current folder.
- Don't commit while check_fast runs: a push at its end takes the new commit too.

## How to test the visit
- `bigevents_check`
- `events_check`
- `fridays_check`
- `day_check` Days 16, 17, 18, 19 and 22
- `career_check` (s5)
- `arrows_check` and `arrows_check step6`
- `cadet_test` against the base (Day 1 identical)
- `check_fast`

## Open questions for the user
None of mine.

## Second job: the visit's pointers (claude/visit-pointer, 0.96.0; RV25 PASS at 6db1cdd)
- Greeting (Wed 10:00) and gift exchange (Fri 09:00): the Schedule's heads-up 15 minutes before with Go there (the storm meetings' pattern). The gift exchange gained `notify` (shown only with heads-ups off).
- Farewell (Fri 09:30): tap to join, host Envoy Saruth (TRAD_JOIN.farewell; the moment's `host` so the planner brings them; `tradJoinable` admits `when.ship === 'diplomatic'`). Words `join.farewell.tip/notice` in content/banks/join.lines, because shortName("Envoy Saruth") is "Envoy".
- Real-play probes I used: scratchpad look2.py / look3.py (not in the repo). Note cadet_test's Game hides `#devHu`: read `DEV.hu` / `HU_Q` instead. Heads-ups wait behind queued tips (`devHuBusy`).
