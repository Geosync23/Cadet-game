# Re-review: claude/social-stories fa2f20d..192e9c8 (0.39.1-0.39.2: review fixes, bonds, introductions, the weekly snapshot; social A 0.36.41 merged)

Reviewer 1, 2026-10-17. Social B's own changes (`git diff d4538df 192e9c8`): sub-block 20c, plus the two hook lines in section 20 that are in its register. Everything else is social A's merged work, already reviewed. name_check OK against fa2f20d and on a merge with crew 0.16.13. The WIP commits after 192e9c8 (0.39.3, moments) aren't reviewed yet.

**Verdict: PASS WITH FIXES:** one decision for the lead (the save size), nothing broken.

## My 0.39.0 points: fixed (checked)
- `relGain` scales only when openness is written (`card.opennessSet`), never on a guess.
- An unknown `about` topic goes under Home.
- `voiceOf` reads `VOICE` / `VOICE_TEMPLATES` inside a try (a `const` not yet declared counts as none) and rebuilds its cards when they change.
- Bond kinds are social A's frozen list. Thread spellings follow the crew designer (`notgood`, `startover`, `arc:<id>`).

## 1. DECISION for the lead (should fix): the social save is 27.8 kB once the reserve is in (budget 20 kB)
- social_check on a merge of 192e9c8 with crew 0.16.13 (86 crew): `Save: social part 27801 bytes (limit 20000)`, `FAIL the save is too big`. Without the reserve it's about 21 kB (social B's own run).
- Most of the growth is the weekly snapshot `SHIP.social.affWeek`: two full copies of the pair table, on top of the live one, in base64. With 86 crew that's 3,655 pairs, about 4.9 kB per copy, so the three copies come to about 15 kB, and the table grows with the square of the crew.
- Options, cheapest first:
  - (a) Keep only the pairs a seating plan can use (friends and rivals, |affinity| ≥ 40, as `i,j,v` triples). The rest plan as `affStart` already does.
  - (b) Store each snapshot as the difference from the live table, sparse.
  - (c) Raise the budget. localStorage has room; the cost is only the size of each `saveGame` (on hide and on sleep, not per frame).
- `socLoad`'s crew-change path doesn't carry `affWeek` across by id: a snapshot of the wrong length is ignored, so seating falls back to the starting affinity for up to two weeks after the reserve first lands. Harmless, but worth one line in the notes.

## Low notes
- On Day 0 the week number is negative (`Math.floor(-1 / 7)` = -1), and `affWeeks`' `/^(\d+):/` doesn't read "-1:...". So the Day 0 snapshot is never found, and a fresh 5 kB copy is re-encoded at every ship hour of the arrival evening. Allow a minus sign in the regex, or skip Day 0.
- `affPlanWeek` reads the snapshot taken at the start of the week before. A day planned more than a week ahead (before that snapshot exists) gets the starting affinity, and is planned differently once the snapshot is taken. Only a concern if some app shows plans that far ahead.

## Checked, fine
- `storyHour` (bonds, best friends, drifting, mentors) runs once a ship hour, over 3,655 pairs at most, with the mentor search once a day. It's deterministic: ties broken by id, keys 672-699 (`introDo` 681).
- Bond changes go on the bus (`simNote('bond')`). `socBondOf` gives `undefined` for kinds that are section 20's own.
- With the reserve: 10 best friends, 9 mentors, 9 friends and 2 rivals after 14 days; save and load the same; the reserve case passes.
