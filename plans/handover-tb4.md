# Handover: TB4, ship traditions builder (0.99.5 playtest patch, lead 47)

**Role:** TR1's item 3 (plans/review-tr1-traditions.md on claude/p995-tr1): the eight 0.92.6 traditions had a host, a
crowd and a Mail promise but nothing to tap. **Branch:** claude/p995-trad926, from claude/staging-0994 596712bc (docs on
8976965e; game a01d1a4c...bc4a). **Switch:** `TRAD926_JOIN_ON` (off; `?trad926` previews). Reviewer RV30; BM22 merges,
alongside TB3's claude/p995-traditions (the Traditions slot's other fixes).

## What was built (section 18, Traditions slot)
All in **TB4's own block**, right after `t932Frame()` and before "// Brennan's dishes", plus two one-line hooks:
- `t932Join`: one new line after the tasting-table line: with the switch on, the eight go to `t926Join`.
- `tradWalkEnd`: `tradWords(W.e, 'done', {}) || W.done || ...` (Garden walk's own end words; the lap is unchanged).

The block (with the switch on):
- `TRAD_JOIN` entries for tool-night (Kovac, talk), route-night (Raman, sit:talk), card-night (Oduya, sit:fold),
  garden-walk (Tove Cruz, act walk), window-sketch (Luca) and window-sketch-2 (Lumi) (sit:read), open-house (Ferreira,
  talk), spoon-band (Femi Rossi, sit:play), worst-joke (Holt, sit:talk); `tjActs()`; each added to `T932_IDS` (so the
  0.93.2 talk in bubbles and the host's close line, `t932Say`, run for them too).
- `t926Join(e, a, notice, lead)`: the host's card (script id `t932.join`, as the 0.93.2 ones, so join_check's card
  handling covers it): the writer's `t932.<id>.join` if present, else our stand-in; the Mail's promise as one question
  with three answers and the host's reply; on the card's end, the activity (`tradJoin` with `T932_GO`). Tool night picks
  three tools of the day and the one in your hand by `quizH` (never `R()`); a right or wrong reply.
- `t926Walk` / `t926GardenPath`: Garden walk is the lap's walk (`TJ_WALK`, `tradWalkFrame`, `tradWhere`'s escort roles)
  on up to 8 of its own garden places in a ring round their middle. No ring or no host: you stand with them to the end.

## Stand-in words for a writer (all in `T926_CARD`; the writer's keys win when baked)
Keys: `t932.<id>.join` (greeting), `t926.<id>.ask`, `t926.<id>.pick.1`-`.3`, `t926.<id>.answer.1`-`.3`; Tool night:
`t926.tool-night.right` / `.wrong` (with `{tool}`; the tool names are in `T926_CARD['tool-night'].tools`); Garden walk's end:
`t926.garden-walk.done`. Close lines: `t932.<id>.close` (else "Same time next time."). Window sketching's two share words.
Words notes seen in the probe (not mine to change, existing `here` lines): Kovac says "Eyes shut. No peeking. Kovac can
tell." herself (the host names herself in the third person); the same can happen with other `here` lines that name the host.

## Tests (all on a switched-on copy unless said)
- cadet_test vs 8976965e with the switch off: **ALL IDENTICAL**.
- join_check: **JOIN CHECK OK**, all nine join (marker, arrow, tip, tap, activity or the walk).
- events_check 35: **EVENTS CHECK OK**. bigevents_check: **BIGEVENTS CHECK OK**.
- day_check on Days 29, 38, 48, 53, 63, 64, 73, 81, 104 (each one's day): **all nine DAY CHECK OK**.
- `plans/tb4-probes/t926_probe.py BUILD.html [id ...]` (switches a copy on itself): per tradition on its day: the
  leader, marker and arrow from its start minute, the tap's card (lines and the question), the activity, bubbles, a
  **real save and reload mid-way** (joined kept, no marker, no second join), the end (no activity, no marker, no arrow),
  no page errors. All nine OK; Garden walk's marker was off camera at the start (the arrow and tip were there).
  Garden walk, followed to its end: the walk goes bed to bed and ends at 10:05 with its own words.
- check_fast on the real build: **QUICK CHECK OK** (335 s).

## Loose ends, gotchas
- After a reload you're still joined (the credit is kept) but your seat or the walk isn't resumed: the same as every
  joinable tradition (ACT and TJ_WALK aren't saved).
- Card night and the spoon band (junior common room) are often full: you then stand beside the host with its pose
  (tradJoin's "every spot taken"). TB3's fix for TR1 item 5 (two traditions on one deck) is in `tradJoinMinute`.
- Garden walk: you start wherever you are; Tove waits (escort `lead`) until you're near, so the first turn can take a
  few ship minutes if you tapped from across the garden.
- The switch lives in TB4's block (not section 13) to keep clear of other seats; BM22 / the lead can move it.

## Open questions for the user
- None of mine; the words are stand-ins for a writer (above).

## Words (SW4, after the build)
SW4 wrote the real words: claude/p995-trad926-words ef310be (content/banks/trad-0926.lines, baked; lines_check's PLACEHOLDERS gained 'tool'), fast-forwarded into this branch. Checked: words baked, names_check OK, lines_check PASS, check_fast OK, the probe shows the writer's lines on Tool night's and Garden walk's cards. Backlog TB4-1: Open house's own Mail says "Deck 2".
