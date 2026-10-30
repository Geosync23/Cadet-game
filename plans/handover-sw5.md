# Handover: SW5 (ending writer B, the endgame pool)

**Role:** writer B for the ending, under lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). SW5 was session_01FFW8ZfuaUqiPPqqhruwZhX.
**Branch:** `claude/ending-words-b`, from `claude/staging-0.93.3`. Content only: the game file is untouched and not baked
(content_gen rejects the word `endgame` until EN2 adds it).
**Spec:** plans/ending-spec.html on claude/p5-specs (f2f9a705), section 9's endgame row.

## What I wrote (420 lines)

| File | What | Lines |
| --- | --- | --- |
| `content/ending/endgame/<id>.lines` (`@crew`) | the Captain, Calder, Vance, Zeke (10 each); 36 crew (6 each): Tomas, Pell, Rina, Brennan, Holt, Kovac, Halloran, Basil, Saruth, Sato, Nandakumar, Oduya, Mensah, Raman, Ferreira, Mori, Kowalczyk, Zielinski, Reyes, Navarro, Eklund, Amadi, Salo, Keane, Silva, Volkov, Quist, Rossi, Santos, Tran, Dlamini, Madsen, Cruz, O'Neill, Esposito, Grieve, Yoon, Dahl, Achterberg, Vasquez | 280 |
| `content/ending/endgame.lines` (`@bank all`) | anyone, by tier (acquaintance to close: greet, chat, bye, invite, note, visit, feel, near, life, rumour), and 20 remarks at traditions (`trad:`) | 80 |
| `content/ending/endgame-overheard.lines` (`@overheard endgame`) | 25 conversations about you staying (11 named pairs by `who:`/`with:`) | 60 |

Commits: cd97eb3d (batch 1a), c9431963 (batch 1b), 8d3c8829 (batch 2).

## Formats and choices

- **The gate:** every `?` line carries the bare word `endgame` (like `newhere`). EN2 adds it to content_gen's COND_KEYS
  (and so lines_check) and section 22's filter. If EN2 picks another word, it's one sed over `content/ending/`.
- **First-weeks lines (RV21's should):** lines that only hold just after the Line (the week's news, "last week",
  "Monday") carry `endgame:early` instead of `endgame`: 107 of the crew's 280, 42 of the bank's 80, 21 of the 25
  overheard. EN2's gate: `endgame:early` holds for about two weeks after you stay, then stops; plain `endgame` holds
  for good (about 220 lines carry on).
- **Why per-person files:** section 22 scores own lines 300 and bank lines 100 (`LINE_SRC`), so a bank line with `who:`
  would never beat a person's own line. content_gen merges a second `@crew` file into the same person.
- **Basil** is story-only (content/stories). The `@crew bramwell-basil` file makes a VOICE entry with only lines; the
  STORY_VOICE merge (section 20c) keeps `VOICE[k].lines`, and he has no other own lines, so nothing is lost.
- **Arc facts are gated** by beats: marrow.5 (her academy offer), calder.3 (Fenn), vance.5 (Gull), torres.4 (his
  dad) and torres.6 (the scarf), kovac.2 (the lift), holt.5 (tea with the Envoy).
- Kept clear of writer A's scenes: no quotes of the Captain's address, Zeke's ramp lines or the offer's words.
- The Admiral is only ever calm and silent. Saruth (they/them) uses no contractions. No "leave" or "permission" about
  the reach.

## How to check

Plain lines_check fails on this branch until EN2's word is in. The scratch way: copy `*.py`, the game, `content/`,
`plans/`, `tools/` to a scratch folder, `sed` `endgame:early` to `flag:end.early` and then `endgame` to `flag:end.stay` in `content/ending/`, then
`python3 content_gen.py <copy>` and `python3 lines_check.py <copy>`: PASS, 0 errors, no new warnings (69, the same as
the base). CS1's `near_dupes.py` on every file: zero EXACT, zero NEAR. names_check OK and check_fast QUICK CHECK OK
on the scratch-baked copy (261 s).

## Loose ends

- Bake for real once EN2's gate is merged, then lines_check and check_fast on the real build.
- If EN2's weights need fewer or more lines of one kind, the tier ladder in endgame.lines is the easiest place to trim.
