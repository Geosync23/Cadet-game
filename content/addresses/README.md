# The Captain's Friday addresses: draft format (EW1, for the events engineer EV1 to agree)

Not read by `content_gen.py` yet: nothing here changes the game. When SHORT_FRIDAY is built, EV1 (or the traditions
engineer) agrees or changes this shape, and content_gen learns to bake it.

- `friday-d5|d12|d19|d26.address`: one speech each. Header keys: `day:`, `from:`, `mail:` ("Subject | body", for anyone
  not there). Then `== lines`, written like a `.meet`: `who: text [pose] #tone`, `who > you: ...` for a line said to you.
- `? conditions` above lines applies to them until the next `?`; a bare `?` clears it. A line whose conditions fail, or
  whose placeholder can't be filled, is left out. `//` lines are notes.
- Conditions used, new ones marked *: `myrank:junior|officer|senior|specialist`* (playerRank()), `done:<jobId>`* (that
  event job was finished before the speech, by anyone), `done:<jobId>.you`* (by you), `band:smooth|bumpy|rough`* (the
  ion storm's result, as the debrief), `commended`* (your storm commendation), `myshift:night`* (your night shifts have
  started), `week1:true` (existing, in the .trad Mail).
- Placeholders: `{me}`; new: `{stormjobs}` (storm jobs closed by all crew), `{myjobs}` (jobs you've closed since Day 0),
  `{leavers}` (first names leaving this week, from the rota).
- Read when she speaks, never by the crew's planner (the plan's rule). Lines are 90 characters at most (bubbles).
- Timing: 16-19 lines a speech; spread them evenly over 16:00-16:48 (about one every 2.5-3 ship minutes).
- `captains-address.trad.draft`: the tradition's own words (Mail, ask, here, thanks, chatter); needs its `k:`.
- `part-e.draft`: the short-Fridays explaining lines for Zeke, Halloran and Friday breakfasts, with the file each goes
  into and its new flag key.
