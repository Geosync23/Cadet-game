# Handover: RV4 (reviewer, playtest patch 1)

**Role:** reviewer for lead 26 (session_015mHBLCf5jpnzBkFY1iBTqv). Session session_01GpAWYxQbS4y8rcB5LWDVE7.
**Branch:** claude/review-play1b (review notes only; no game changes). Base reviewed against: claude/integration
32b699a6 (0.64.14, game sha256 94f32868...881e9).

## What I did

Reviewed four branches of playtest patch 1 (0.64.15); full notes in `plans/review-play1b.md`.

| Branch | Note | Builder | Tip | Verdict |
| --- | --- | --- | --- | --- |
| G claude/patch-play1-g | 13, more jobs | JB1 | 3ffb604f (511101405 docs only) | PASS |
| H claude/patch-play1-h | 15, open ladder rooms | LR1 | d0f96def | PASS |
| I claude/patch-play1-i | 19, toilet queue | TQ1 | 0c05e856 (1d2344eb docs only) | PASS, follow-up backlog TQ1-1 |
| K claude/patch-play1-k | 21, repeating lines | DL1 | d38d4cdc | PASS, balance note |

All verdicts sent to the lead, BM13 and each builder.

## Loose ends (for the user or the next patch)

- TQ1-1 (backlog): crew can stand in a toilet line while the light is off (planned slots reached late by the live
  crew; later arrivals get earlier slots). Same timing as before the patch, now visible. Idea: the front of the line
  takes any free toilet nobody is heading for (runtime only).
- K: a talk that runs out of lines wraps up with full social (30) in about 8 ship minutes instead of 15: social fills
  about twice as fast per minute. For the balancing pass. Nit: a new small-talk line mentions "the stairs".
- G: extra jobs give no reputation and the ship's upkeep tops out about Day 11 (both in design-doc open questions);
  the same chore can come up twice in an afternoon (backlog JB1-1). career_check's known FAIL (backlog 12) no longer
  shows with G merged.
- tiles_check times out clicking "Quick game" when other checks share the CPU; passes when run alone.

## Gotchas and how I tested

- Probe scripts (not committed) lived in the scratch folder /tmp/rv4/scripts: toilet repro, live toilet watch,
  ladder drive and close-ups, job board drive, crew plan dump/compare, talk pause timing. Each reuses cadet_test.py's
  `Game` class (`exec(open('cadet_test.py').read().split("a, shots = run(")[0])`).
- Run a branch's own copy of a check when the branch changes that check (I first ran the old interactions_check on I).
- Never `pkill -f` or `pgrep -f` with a pattern that also appears in your own shell command: it matches itself.
- Give each parallel check its own CADET_WORK; keep to about three browsers at once on 4 cores.
