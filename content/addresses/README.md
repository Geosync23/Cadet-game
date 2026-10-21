# The Captain's Friday addresses: draft format (EW1, for the events engineer EV1 to agree)

Not read by `content_gen.py` yet: nothing here changes the game. When SHORT_FRIDAY is built, EV1 (or the traditions
engineer) agrees or changes this shape, and content_gen learns to bake it.

- `friday-d5|d12|d19|d26.address`: one speech each. Header keys: `day:`, `from:`, `mail:` ("Subject | body", for anyone
  not there). Then `== lines`, written like a `.meet`: `who: text [pose] #tone`, `who > you: ...` for a line said to you.
- `? conditions` above lines applies to them until the next `?`; a bare `?` clears it. A line whose conditions fail, or
  whose placeholder can't be filled, is left out. `//` lines are notes.
- Conditions and placeholders, and who has agreed them (2026-10-20):
  - Agreed with EV1, whose section 18 readers are pushed (claude/events-base bb285a0): `band:smooth|bumpy|rough` =
    eventBandOf(id) ('smooth'|'bumpy'|'rough' or null); `done:<jobId>` and `done:<jobId>.you` = eventJobDone(jobId,
    you, t); `commended` = !!SHIP.commendations.length; `{stormjobs}` = eventJobsCount('ionStorm'), `{myjobs}` =
    eventJobsCount(id, true). The lines put the counts after a colon ("Storm jobs closed in four days: 12."), so a count of 1
    reads right; a count of 0 drops the line (FR1's address player).
  - Still to agree: `myrank:junior|officer|senior|specialist` (your rank, SHIP.works.rank; `rank:` is the speaker's, so
    it needs a small condition in section 22's engine, the dialogue engineer's, or FR1's player reading it) and
    `myshift:night` (your night shifts: Pillar 5, not built yet); `{leavers}` (this week's leavers' first names,
    from ROSTER_ROTATIONS); the `.address` file itself and its bake (the Fridays builder, the dialogue engineer and the
    lead); `week1:true` in the .trad Mail is existing.
  - The event drafts' calledin is now EV1's `cue:calledIn@me` / `cue:calledIn` (plans/events-ready); the drafts'
    other headers (@gathering, @tradition-day, == reactions.*) are superseded there by EV1's bank keys.
- Read when she speaks, never by the crew's planner (the plan's rule). Lines are 90 characters at most (bubbles).
- Timing: 16-19 lines a speech; spread them evenly over 16:00-16:48 (about one every 2.5-3 ship minutes).
- `captains-address.trad.draft`: the tradition's own words (Mail, ask, here, thanks, chatter); needs its `k:`.
- `part-e.draft`: the short-Fridays explaining lines for Zeke, Halloran and Friday breakfasts, with the file each goes
  into and its new flag key.
