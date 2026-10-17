# Handover: dialogue engineer (Pillar 4, seat 2)

Written by session_01UmrVVpV7eBqEsa4sBucASP (the first dialogue engineer); kept current by session_01S26bs4oMahyGJkuVaCKQGT
(dialogue engineer 2, from 0.43.12), so a fresh session can take over at any time. Read CLAUDE.md, DEV_NOTES.md ("Lines (section 22)" and the 0.43.x rows), plans/pillar4-plan.md
(Part 2 and seat 2 in Part 6), plans/social-deep-plan.md (Parts 6 and 9) and **content/README.md** (the writers' guide:
it is the full spec of the file formats and the condition vocabulary) first.

## Role, branch, builds
- Branch `claude/dialogue`, builds **0.43.x** (last: **0.43.26**, 0b504ba). Reviewer 2 passed up to 0.43.24; 0.43.25, 0.43.26 and Tiles 0.46.6 await review (reviewer 2's session went inactive ~08:20; asked the lead who reviews now). Also (lead-assigned, Tiles seat vacant) Tiles 0.46.6 = 99609d3 on claude/tiles (crewHold for the opponent), with reviewer 2. 0.43.23: the JSON.parse strings are an array joined with join(''), not a + chain (Safari). Since 0.43.17
  (7c888e4) the branch carries claude/ship-integration 0.60.1 (merged, the lead's call), so onSim, cue() and social are here.
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

- 0.43.12 overheard played: `linesTick` (from section 20's socialTick) -> alternating bubbles under the voice budget;
  the saved ring `SHIP.lines = { ring: [[id, day]], serious }` in save.lines via SAVE_EXTRA (no sim-engineer hook needed).
- 0.43.13 one-speaker conversations (only `A:`), booth callers talk only to home.
- 0.43.14 reviewer 2's fixes (calls home: family warmth only; contacts mum/gran/jo/sam; "my love"; `linesNew` on New game;
  cheaper pair scan: OVH_NEAR 6, OVH_TRIES 8, overheardFor fills only its top group). 0.43.15 act:call = callhome;
  one-speaker lines need place:/act:.
- 0.43.16 reactions (`linesReact`, onSim('*'), SHIP.lines.reacted). 0.43.17 the merge; New game resets through
  onSim('newGame'). 0.43.18 trait:/you: take `_`, values checked. 0.43.19 `lines_check.py --day` (the voice budget in a browser).
- 0.43.20 VOICE and LINES bake as `JSON.parse('...')` (perf item 4; one literal per entry joined with +; performance
  engineer 2, session_01XAkY9U3mmstHQT2yAMTocA, measures it). 0.43.21 {home} {family} {hobby} {since} through socialFill
  (needs social A's 0.36.60 in the same build; build master 2 is session_01F8ph7FKqViF3heRn94YgBr). 0.43.22 lines_check
  checks trad:/came: ids. save.lines is separate from social_check's 30 KB social budget (about 10 KB worst case).

## Hooks outside section 22 (the hook register)
- Section 20 (mine, approved by the lead): `const CHATTER_IDLE/CHAT_GREET/CHAT_NEAR/CHAT_LIFE/CHAT_DEPT = linesLegacy(...)`
  and the first statement of `chatGreet` (own lines via lineFor, peek when asked about another hour). Social A doesn't
  touch those lines; when they move chatLine to `lineFor` (socLine), the legacy reads can go.
- Section 20 (0.43.12): `if (typeof linesTick === 'function') linesTick();` after `chatTick();` in socialTick; section 22
  sets section 20's `CHATTER_AT` while a conversation plays. (0.43.14's section 13 hook went in the 0.43.17 merge: section 22 listens to onSim('newGame').)
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
- Wave 2 is done (overheard, the ring, booth lines, reactions, the --day check).
- 0.43.24 {kin} {lost} {hobbyNoun}: crew designer 3's (session_01TDCn9auvCBML52hyjWGY6x) line-ready roster fields;
  socialFill first, else the roster; lines_check errors on {family}/{hobby} in arcs/themes. Head writer 3 switches the
  family/loss/talent themes, then takes the new lines_check. Social A hasn't said whether socialFill will answer them.
- 0.43.25: a theme beat's roster words must be in its needs: ({lost} in arcs too). 0.43.24/25 make lines_check fail on the
  writers' content until head writer 3 switches the family/loss/talent themes: they ship together.
- 0.43.26 perf: the minute's overheard/reaction tries one a frame (OVH_SCAN, OVH_PER_FRAME 1), lineQuick (cheap
  conditions first), LINE_CUE memo, lineFor fills only its top group. Benchmarks (scratch scripts): every crew x kind x 4 times
  gives identical lines before/after. Performance engineer 2 (session_01XAkY9U3mmstHQT2yAMTocA) may send phone numbers.
- In flight (asked 07:5x UTC): head writer 3 (session_01FopKMT2ZKxuWcNDcmF7565) and social B2
  (session_014A3w2gK8FBNWs66YC3LfME): what the arcs' last beats need from section 22 (head writer 3: nothing; Tiles: nothing more). Social B2 hasn't
  answered yet.
- (done: overheard played, the ring, booth one-speaker lines.) Test script for overheard in a browser: see
  DEV_NOTES 0.43.12 (stand the player by a group on Deck 3 at dinner, step, log `bubbles.list` and `OVH`).

## Open questions for the user (via the lead)
- None of mine outstanding.
