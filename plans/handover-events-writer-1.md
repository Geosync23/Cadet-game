# Handover: events writer 1 (EW1)

**Role:** writes the words for the ship-wide events and the Captain's Friday addresses. Content only: never the game
file, never baked blocks. Reports to the lead (lead 22, session_01BGQCZLK6gYTnqu6mwZ61jB; lead 21 before it).
**Session:** EW1, session_01KkAhg7eVhPenBBVfLufPU1. **Branch:** `claude/events-lines` (push only there), from
claude/integration 0.64.5. Last commit: see `git log` (c37f321 at writing).

## What's on the branch (all reviewed and passed)
- **`content/addresses/`** (not read by content_gen; FR1 bakes them for Short Fridays):
  - `friday-d5|d12|d19|d26.address`: the four Captain's Friday addresses, 16-19 bubble lines each (PR2 PASS 407fd07).
  - `friday-weekly.address`: the pool for every Friday after Day 26 (PR3 PASS 307addc).
  - `captains-address.trad.draft` (needs its k:), `part-e.draft` (Zeke, Halloran and Friday breakfast lines with
    their new flag keys), `README.md` (the format, the conditions and who owns each).
- **`plans/events-ready/<event>/content/...`**: finished files in EV1's agreed formats, mirroring where each goes in
  `content/`. EV1 moves an event's files in and bakes in the turn that builds it (outside `content/` because
  content_gen reads every folder there). Events: ionStorm, crossingLine (story A "The one on watch", PR2 PASS
  dfd083a), comet, diplomatic, and firstLightCocoa (the Pale Shoals / Tavessa swap). Its README says what's where.
- **`content/events/*.draft`**: the first plain drafts, superseded by events-ready, kept for the record.
- **`content/facts.md`**: two new canon lines (section 1): "Out of the windows" (the Pale Shoals, Tavessa; the user's
  pick) and "The Veyli reach" (last visited two years ago on a quiet charting run; never tie an incident to it).
- **`plans/events-lines-addresses.md`** (the user's review page source for the addresses, answers recorded) and
  **`plans/events-lines-events.md`** (the summary of jobs 2-3).

## The user's decisions on my work
- Addresses: 16-19 lines spread over 16:00-16:48; on Day 12 the Captain "borrows" the closed rec deck for the hour;
  keep Day 5's "a quiet ship, I hope"; names the Pale Shoals and Tavessa.
- Crossing the Line: story A "The one on watch"; the ceremony moved to the bow lounge; q4-q6 the recommendations;
  q1 the crew's Line chatter starts Saturday 08:00 (my warning lines say "tomorrow", so they read fine all day).
- The lead's calls: Crossing the Line's cake cut to a pudding (the four-weeks cake is the cake moment); Day 26 keeps
  "Works has something for you"; Day 19 "keeps her on her toes"; a bridge week in the weekly nods; myrank: is read by
  FR1's address player from SHIP.works.rank.

## Formats agreed (EV1)
- Reactions: `content/reactions/event.<id>.<phase>.lines`, `@reactions event.<id>.<phase>`, lines under
  `? cue:event.<id>.<phase> ...`. Called in: `content/reactions/calledIn.lines`, `cue:calledIn@me` / `cue:calledIn`.
- Event texts: `content/banks/event-<id>.lines` (`@bank all`), `== event.<id>.<what>.<phase>[.<band>]`, numbered .1
  .2 for several lines. Mail "Subject | body". lines_check limits (EV1, events-base bb285a0): mail 400; gathering
  mail/thanks, keepsake, plaque 200; status 60; the rest 90. Placeholders `{me}` (not `{you}`), `{dark}`, `{band}`.
- Meetings: `.meet` as today; no `?` conditions inside, no `thread:` key, so versions are separate files
  (captainAllClear.smooth|bumpy|rough, calderStorm.officer) or a line the code inserts from a bank key.
- Address readers (EV1): eventBandOf, eventJobDone, eventJobsCount; commended = SHIP.commendations.length.

## Loose ends
- The Veyli are now human (the user, via lead 22): a culture that went further out centuries ago. LW1's lore plan
  (claude/veyli-lore 9fa7521) is with the user; about 14 "why it matters" lines wait for those answers. My lines
  don't describe the Veyli as non-human, but re-read the visit and Crossing lines against the lore once it's settled
  ("Proud, careful, and very good at noticing things"; "A Veyli does not watch another people's rite").
- myshift:night waits for Pillar 5's night shifts; {leavers}/{arrivals} for ROSTER_ROTATIONS wiring (FR1).
- The game's veyliGreeting summary says "her aide" (Veyli are they/them): the backlog has it; the ready file fixes it.

## Gotchas
- **No arc spoilers** (the main risk): Marrow (daughter, retiring, the Admiral), Holt (his bad day on a border
  patrol years ago; never link it to the reach or the Line), Tomas (beat 5 the exam, beat 7 staying), Calder's Day 26
  question, the four-weeks cake surprise.
- Bubbles 90 characters with a 20-24 letter name; tradition names up to about 25.
- Never bake on this branch (two seats regenerating the game's blocks clash). Test-bake in a scratch copy: copy the
  tracked files, copy plans/events-ready/*/content/ over content/, run content_gen.py then lines_check.py.
- check_fast needs acorn and three.js in /tmp/cadet-work and `pip install playwright` in a fresh container.
- Rotas that mattered: the Captain, Calder, Sato and Holt are off at weekends; Vance off Days 11, 17-18, 21; Brennan
  off Fri-Sat (Lukas Dlamini covers); Tomas works Sundays (off Mon-Tue); Zeke off Thu-Fri.

## How to test
`python3 lines_check.py` (PASS) and `python3 content_gen.py --check` (up to date) on the branch; the scratch-copy bake
above for the ready files; `bash check_fast.sh` before a push (OK in about 210 s).
