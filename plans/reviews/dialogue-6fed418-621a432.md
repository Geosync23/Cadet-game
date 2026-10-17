# Review: dialogue 0.43.22 (6fed418) and 0.43.23 (621a432)

Reviewer 2, 2026-10-17. **Verdict: PASS for both.**

## 0.43.23: JSON.parse([...].join(''))
- Same data and key order: VOICE and LINES evaluated in node are identical to 0.43.19's (and so to 0.43.20's).
- Full size: with 621a432's content_gen on claude/content 0a86991, the rebake equals content's own data (VOICE 752,166 characters, LINES 93,321). Re-running gives byte-identical output.
- The array form is flat, which settles my earlier Safari note. A trailing comma after the last piece is valid in an array.

## 0.43.22: lines_check checks trad: and came: values
- The regex finds all 12 SHIP_TRADITIONS ids in dialogue 621a432, in the released 0.60.2 and in ship-events f78dd03. The baked traditions are added on top.
- Content today: every trad: and came: value it uses passes (observatory-night, quiz, jam, running, market, film, harvest, today, any). lines_check PASSES with 0 errors.
- Negative test: changing `trad:quiz` to `quizz` and `came:any` to `anything` → FAIL with 4 errors, each naming the bad value and the allowed list.
- The allowed values match the game: section 22's lineCond treats `today` (trad:) and `any` (came:) the same way.

The save-size answer is accepted: save.lines is separate from social's SAVE_MAX, at about 10 KB worst case.
