# Review: claude/ship-events 45189b9 (0.34.19-0.34.20), reviewer 2

**Verdict: BLOCK for combining with claude/dialogue** (finding 1). On its own the branch is PASS WITH FIXES.
Base: origin/claude/ship-integration (0.41.10). Checked: the diff, trad_parse.py with bad input, the bake against the
block (byte-identical: yes), events_check (run with 7 days: everything passes except hull-lights, which falls on a later
day than my short run; the year on paper, seasons, sowing loaded and filled all pass), and a trial merge of
integration + ship-events + dialogue.

## 1. BLOCK: the two branches bake TRADITIONS two different ways, and merging them breaks the game
- Trial merge (integration, then ship-events, then dialogue): the only conflicts are the two build labels. Git then
  silently keeps **two** `const TRADITIONS` declarations: dialogue's in section 22 (`const TRADITIONS = {}`, an object)
  and this branch's in section 18 (`const TRADITIONS = [ ... ]`, an array). `node --check` on the merged script:
  `SyntaxError: Identifier 'TRADITIONS' has already been declared`. The whole game script fails, so the page is blank.
- Even with one block, the shapes don't match. content_gen.py writes an object keyed by id, with fields as raw strings
  (`"k": "434"`, `"when": "quarter week 1 saturday"`, `"title"` rather than `name`) and text entries as
  `{ text, id, ...conds }`. tradLoad wants an array of parsed fields and `{ t, tone }`. So `for (const t of TRADITIONS)`
  throws "not iterable" at load, and `x.t` is undefined.
- content_gen.py on the merged tree: (a) rejects sowing.trad because of its two `#` comment lines at the top
  ("the first line must be an @header"), although plans/trad-format.md allows comments; (b) with those removed, it
  crashes with `AttributeError: module 'trad_parse' has no attribute 'parse_field'`. It calls `parse_field`, `finish`
  and `check_all`; trad_parse.py only has `parse_trad` and `bake_traditions`.
- lines_check.py fails sowing.trad: `unknown token {season}`. It checks tradition texts against the *lines*
  placeholders (me, friend, room...), not section 18's (trad, host, names, first, season, weekday, time). So it rejects
  good tradition text and lets through `{me}` / `{room}`, which tradFill can't fill, so those lines are silently dropped.
- The fix (one owner decides, through the lead): one block, one marker, one shape. The simplest is for content_gen to
  write the TRADITIONS block with `trad_parse.bake_traditions('content/traditions')` (array, `{t, tone}`), drop
  section 22's own TRADITIONS block, accept leading `#` comments, and have lines_check use section 18's placeholder set
  for `trad.*` kinds. Also agree on the marker line: content_gen's `splice` rewrites the BEGIN line with its own text,
  so the block then no longer matches trad_parse's output byte for byte. If `?` conditions stay allowed in .trad text,
  the loader must honour them: today it would ignore them and show a gated line to everyone.

## 2. HIGH (determinism): `friends-of-host` reads live affinity inside planning
`tradIs` -> `affinity(host, p.id) >= 40`. `affinity` reads `SHIP.aff`, which changes during play and is saved.
`who()` runs in `eventPlan` -> section 14's day plan. A day planned before an affinity change (or before a reload)
and planned again after it comes out different. That breaks "plans are pure", and it's why `affinityPlan` exists.
Path: any .trad with `who: friends-of-host 80%`; chat with the host on day d-1 to raise affinity over 40; reload;
day d's plan changes. Fix: use `affinityPlan(host, p.id, d)`. (No baked tradition uses it yet, but the format
advertises it.)

## 3. MEDIUM (content): Brennan can say "Don't tell Brennan"
sowing.trad `ask`: "I'm planting basil this time. Don't tell Brennan, she'll want it." Any person going can say ask
lines, Brennan included. On day 97 (Saturday, her day off) her pick is that line (schedU(seed+7919, 97, 434)*2 -> 1),
and her chance to go is 0.298, under the 30% for everyone. Fix: a per-line `not` speaker rule, or reword it.
(Also, the Mail hard-codes "11:45" rather than `{time}`; it drifts if `at:` changes.)

## 4. MEDIUM: the parser accepts rhythms that never happen, and crashes on some bad input
- Accepted silently, never due: `quarter week 14 saturday`, `year day 400`, `quarter day 0`, `arrival friday 0`
  (nth 0). events_check doesn't fail a baked tradition that has zero days in the year: it is just left out of `sims`.
  Fix: range-check week (1-13 per quarter, 1-52 per year), day (1-91 / 1-364) and nth >= 1, and make events_check fail
  any baked tradition with no due day in 0-364.
- Python traceback instead of a TradError: `hold: abc` and `when: every 2 weeks saturday week x` (ValueError).
  `hold: 0` gives `[-1]`, which silently holds nothing.

## 5. LOW
- `EV_DAYS` caches `eventsOn(d)`, and the `after: 'arrival'` rhythms read `introArrival()` inside it. When section 21
  sets or changes the arrival day (skip to Monday, a new game started over a running one), the cache must be cleared,
  or the "one week aboard" style traditions stay on the old days for up to 30 days. Note it for the onboarding seat's
  hook.
- The build label: when this branch merges into integration, 0.34.20 replaces 0.41.10 with no conflict. The lead sets
  0.60.x anyway; just watch for it.
- `tradIs` stops at the first word that fails (`every`), so events_check's "every word resolves" pass misses a typo
  after a word that fails for everyone (e.g. `rank:captain+gardnr`). Resolve every word once in tradLoad instead.

Checked and fine: evDue against an independent calculation (the branch's own check plus mine on the edge cases: day 0,
negative weeks, quarter and year before Day 1); hash keys 434 and 534-599 collide with nothing; no R(), Math.random or
Date in the new code; shared kit untouched; room regexps from Python's re.escape are valid in JS; Mail, ask, here and
thanks reach the screen with no raw `{x}` (a line that can't be filled is skipped; thanks has a fallback).
