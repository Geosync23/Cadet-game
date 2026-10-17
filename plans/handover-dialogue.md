# Handover: dialogue engineer (Pillar 4, seat 2)

Written by session_01UmrVVpV7eBqEsa4sBucASP (the first dialogue engineer), while still working, so a fresh session can
take over at any time. Read CLAUDE.md, DEV_NOTES.md ("Lines (section 22)" and the 0.43.x rows), plans/pillar4-plan.md
(Part 2 and seat 2 in Part 6), plans/social-deep-plan.md (Parts 6 and 9) and **content/README.md** (the writers' guide:
it is the full spec of the file formats and the condition vocabulary) first.

## Role, branch, builds
- Branch `claude/dialogue`, builds **0.43.x** (last: **0.43.11**, e69936d), on ship integration 0.41.10.
- I own: section **`// 22. LINES`** in starship-cadet.html (between section 17's end and `// 18. SHIP EVENTS`), the
  generated blocks' markers (LINES, MEETINGS, TRADITIONS), **content_gen.py**, **lines_check.py**, **content/README.md**.
- Not mine: everything else under content/ (head writer 2, session_01HNrh3xCtczeZM5NVFrE6pa, branch claude/content,
  merges the writers); plans/trad_parse.py (traditions engineer, session_018WZccmSvEfz2LC7DCfxdii; frozen interface,
  I only call `read_all`).
- Report each push to the lead (now session_01KPJMYjXAPkNUcrQ8VRkhLE) and ask reviewer 2 (session_0142TQw4ke8caPSyAC93VT98)
  to look. Only the lead talks to the user.

## What's built (all reviewed and passed by reviewer 2 up to 0.43.10; 0.43.11 just pushed)
- 0.43.0 the writers' kit: `lineFor(who, kind, ctx)` (own > template > bank, most specific wins, recently-said penalty,
  seeded by person+hour with schedU 750, `told:`→memTold, `peek`), `linesOk`/`lineCond` (the frozen vocabulary),
  `linesFill` (voice tokens, placeholders, socialFill first, capitalises a filled word at a sentence start),
  `overheardFor(a, b, ctx)` (pure; not played yet), `linesMeetings(MEETING_SCRIPTS)` (section 18 calls it),
  `linesLegacy(kind)` (section 20's five old lists read back from content/banks/old.lines, pick-identical).
  Torres baked as the sample person (his chat card greets with his own lines).
- 0.43.1 GUESTS known. 0.43.2 the `.arc` grammar → `MOMENTS` / `MOMENT_THEMES` (social B's shapes).
- 0.43.3 `place:` aliases/underscores, `ctx.flags` (onboarding fetches Torres's walk lines by step), facts.md names.
- 0.43.4-0.43.6 the romance rule (the lead's final call): no romance words in any line with a player reference
  ({me}, {nick}, new hand, cadet, newcomer, you/your), every kind; couple talk only in overheard under
  `pair:couple`/`bond:couple`; about/rumour/smalltalk under the full ban; married/wedding fine; `content/allow.list`
  (head writer approves by line id). Also max 3 replies, poses sigh/laugh/listen/nod/gesture/play.
- 0.43.7 `cue:<key>@me` / `@dept` (social A's cue records carry who/dept). 0.43.8 `who:` / `with:`, crew ids in `pair:`.
- 0.43.9 `rep:` and `ship.*:` are "this band or better"; `deck:` = the scene's deck (ctx.deck, else deckDef.num).
- 0.43.10 `gift:` (ctx.how loved/liked/polite, or ctx.tag).
- 0.43.11 calls home: `content/home/<contact>.call` → `HOME_CONTACTS`, `HOME_MOMENTS['<c>:<n>']` (+ `via`),
  `HOME_SEND[c]` (`sets`/`memo` = what a choice sets), `HOME_CHAT[c]`; conditions `came:` (ctx.trad) and `friend:`
  (ctx.friend). Social B agreed the shapes (their successor builds B8; see plans/handover-social-stories.md).

## Hooks outside section 22 (the hook register)
- Section 20 (mine, approved by the lead): `const CHATTER_IDLE/CHAT_GREET/CHAT_NEAR/CHAT_LIFE/CHAT_DEPT = linesLegacy(...)`
  and the first statement of `chatGreet` (own lines via lineFor, peek when asked about another hour). Social A doesn't
  touch those lines; when they move chatLine to `lineFor` (socLine), the legacy reads can go.
- Section 18 (traditions engineer's): `if (typeof linesMeetings === 'function') linesMeetings(MEETING_SCRIPTS);`.

## Gotchas
- **After every merge, run `python3 content_gen.py`** (it needs plans/trad_parse.py from claude/ship-events) and then
  `--check`. On my branch alone the TRADITIONS block is empty and Sowing morning would vanish from a combined build.
- Generated blocks are never hand-edited or hand-merged: on a conflict, take either side and re-run the generator.
- `lineQ(name)` is a switch with one typeof per name: section 20's queries are consts (not on window).
- Entries' data fields must be in `LINE_META` or `linesOk` reads them as conditions (that's why sends bake `sets`/`memo`).
- A `?` condition lasts until the next `?` line or `==`; a bare `?` clears.
- cadet_test sometimes shows a "+N Energy" float (`.nf`, real-time timers) in g_nocrew: compare with `.nf` hidden in
  both builds (inject `<style>.nf{display:none!important}</style>`); then it's identical.
- device_check's "Needs: the bar pulses" failure is on 0.41.10 too (not mine).

## How to test
- `python3 content_gen.py --check` (byte-identical bake) and `python3 lines_check.py` (PASS).
- The writers' real content: `git archive origin/claude/content content | tar -x -C <scratch>`, copy content_gen.py,
  lines_check.py, starship-cadet.html and plans/trad_parse.py (from claude/ship-events) there, bake and check.
- cadet_test against the previous build (see DEV_NOTES "Testing"; `/tmp/cadet-work`, `CADET_CHROME=/opt/pw-browsers/chromium`).
- Quick logic checks: node scripts that slice section 22 out of the file (`// 22. LINES` to `// 18. SHIP EVENTS`) and
  run it with stub schedU/shipNow/ROSTER (examples were in my scratchpad: eq.js, cue.js, who.js, rep.js, home.js).
- Browser checks one at a time; social/deck/day/player/events/interactions/food/machine all passed on 0.43.0.

## Loose ends / next (wave 2, waiting for the lead's go-ahead)
- Play overheard conversations as alternating bubbles (section 8b's `bubbleSay`) under the voice budget (one on screen,
  none while a card or meeting is open), with the saved ring (`SHIP.lines = { ring, serious }`, `save.lines`, no repeat
  within 7 ship days) — needs a save hook in section 13 (sim engineer).
- One-speaker overheard lines for the call booths (head writer 2's ask): allow a conversation with only `A:` lines,
  e.g. `@overheard booths` with `? place:booths`.
- Reactions from `onSim` cues (sim engineer's bus: simNote/onSim/simNotes), once per person per kind per day; the
  galley's `lateMeal` note carries { who, meal, late, how, dish, deck }.
- lines_check's simulated voice-budget day in a browser (now only a report of the rules and the supply).
- mum.call needs two edits by the writers (drop "(?)", add a bare `?` before the anyone-can-say send lines).

## Open questions for the user (via the lead)
- None of mine outstanding.
