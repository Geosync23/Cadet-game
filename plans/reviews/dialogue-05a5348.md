# Review: claude/dialogue 05a5348 (0.43.0 WIP: the writers' kit), reviewer 2

**Verdict: BLOCK for combining with claude/ship-events** (finding 1, shared with that review). On its own the branch
is PASS WITH FIXES.
Base: origin/claude/ship-integration (0.41.10). Checked: the diff, content_gen.py re-run (byte-identical: yes;
`--check` up to date), lines_check (PASS), the moved section 20 lists against the old ones (greet, near for every act,
life, dept and smalltalk all identical, run in node), and a trial merge with ship-events.

## 1. BLOCK: TRADITIONS baked twice, in different shapes (see plans/reviews/ship-events-45189b9.md, finding 1)
- The merged file declares `const TRADITIONS` twice (section 22's `{}` and section 18's `[...]`): SyntaxError, so the
  game doesn't load. Git merges it with no conflict.
- content_gen.py calls `trad_parse.parse_field`, `.finish` and `.check_all`, which the traditions engineer's
  trad_parse.py doesn't have: on the merged tree it crashes with AttributeError. Without trad_parse it bakes raw
  strings in an object keyed by id, with `{ text, id }` entries, but section 18's loader wants an array with `{ t, tone }`.
- content_gen rejects a .trad whose first lines are `#` comments (sowing.trad has two; trad-format.md allows them).
- lines_check checks `trad.*` text against the lines placeholders: it rejects `{season}` (sowing's thanks line fails,
  proven by adding sowing.trad to this branch) and lets through `{me}`, `{room}`, `{friend}`, which section 18's
  tradFill drops.
- Fix: as in the ship-events review. The likeliest shape: content_gen uses `trad_parse.bake_traditions`, section 22
  loses its TRADITIONS block, the marker text is agreed so the output is byte-identical, and lines_check gets a
  tradition placeholder set.

## 2. LOW-MEDIUM: "Talk more" runs lineFor as a side-effecting look-ahead
Section 20 line ~14896: `chatLine(p, shipNow() + 60 * k)` for k = 1..6, looking for a different line. Since this
branch, chatGreet calls `lineFor(p, 'greet', { t })` with no `peek`. So each look-ahead (a) pushes future-hour entries
into LINE_RECENT, which then shift the recently-said penalties, and (b) calls `memTold` for any `told:` line it
*considers*, even when the loop throws that line away (it's the same text as the one showing). That `told:` line is
then lost for good. Torres has no `told:` greet lines today, so this hasn't happened yet, but writers will add some.
Fix: pass `peek: true` from chatGreet (or from chatLine when t is in the future), and record a line only when it is
shown.

## 3. LOW
- `habit:` conditions read `p.habits`, but section 18 uses `habitsOn(p, d)` (habits change over time: Brennan
  becomes a gardener). A line gated on `habit:gardener` and a gardener tradition disagree about the same person.
- `lineQ` builds one object with 22 `typeof` checks inside one try. If any one of those names is a `const` still in its
  temporal dead zone when lineQ runs (a call during load, before sections 18/20/21 have run), the whole object throws,
  and every query returns undefined, not just that one. Today nothing calls lineQ at load (linesLegacy doesn't), so
  this is a note for whoever adds a load-time call.
- The commit says "checks running": chatGreet now gives Torres his own greetings, so a cadet_test shot that taps
  Torres would change. Please post the cadet_test result before the build master combines this.

Checked and fine: hash keys 750, 751, 760-769, 770-797 (all in 750-799); no R(), Math.random or Date; placeholders
are filled or the line is skipped (no raw `{x}` reaches the screen through lineFor or overheardFor); the
`{nick}` -> `{me}` second pass; the query signatures match social-deep-plan Part 11; section 20's edits are the
agreed move of its lists plus chatGreet (please list that line in the hook register); no romance with the player and
no serious lines in the sample content.
