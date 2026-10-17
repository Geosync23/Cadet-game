# Review: dialogue 0.43.20 (ac88e0b): VOICE and LINES baked as JSON.parse strings

Reviewer 2, 2026-10-17. Checked against the last tip I passed, e1594b9.

**Verdict: PASS.**

What I checked:
- **Only the bake changed.** The html differs from e1594b9 only in the build line, GAME_BUILD and the VOICE/LINES block.
- **Same data, same order.** I evaluated the old and new VOICE and LINES in node and compared them with JSON.stringify, which also catches key order. They are identical: VOICE 2,095 characters, LINES 9,221. The old blocks held nothing that JSON can't carry (no functions, undefined or regexes).
- **Full content size.** Trial merge of ac88e0b onto claude/content 0a86991. The only conflicts are the build numbers. After a rebake, VOICE (752,166 characters, 7,696 pieces) and LINES (93,321 characters) are identical to content's own bake.
  - Re-running content_gen gives byte-identical output.
  - lines_check: PASS (0 errors, 3 warnings, the same ones content already has).
  - The merged game loads in Chromium with no errors: 115 voice cards, 15 kinds of line.
- **Escaping.** I round-tripped awkward text through `lists_parsed` and `cards_parsed`: `'`, `\`, `"`, line breaks, `</script>`, U+2028/2029, tabs and control characters, emoji, `${x}`, a literal `A`, and a trailing backslash. Everything comes back exact, and no `</script` reaches the html. Empty lists, an empty `lines`, and cards without `lines` all come out as valid JSON.
- **The speed claim holds.** I loaded only the VOICE and LINES blocks on fresh pages, 6 runs each, with the CPU slowed 6× to stand in for a phone. The old bake took a median of 343 ms; the new one takes 238 ms.

Low, untested risk: Safari. At full content, VOICE is one `'..' + '..' + ...` chain of about 7,700 literals. Chromium and node are fine with that. I can't test Safari's engine here. Very long `+` chains have hit stack limits in some engines. If the lead wants to remove that risk for free, `JSON.parse(['..', '..', ...].join(''))` is flat, keeps one entry per line, and costs the same. Not a blocker.
