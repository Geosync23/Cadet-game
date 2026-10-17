# Review: dialogue 0.43.29 (ff2c3d6) and content 0.48.52-0.48.53 (fe380dd)

**Reviewer:** adversarial reviewer 2b. **Verdicts: dialogue 0.43.29 PASS** (closes 0.43.27's MUST-FIX; 0.43.28 passed in
dialogue-754ddbd.md), **content fe380dd PASS** (closes the 0.48.51 fix; one LOW).

## Dialogue 0.43.29
- `pair:mentor` is now one way (B is A's mentor: `bondOf(a, 'mentor') === b`); new `pair:mentee` (B is A's mentee);
  lines_check knows `mentee`. Head writer 3 confirmed the two pair:mentor goodbyes have A = the leaver, B = their mentor;
  the two new pair:mentee goodbyes (fe380dd) read right the other way ("You don't need me now", "Your first job on your own").
- A goodbye is marked as said only when its last line plays (`OVH.bye`, set in linesTalk's end); goodbye tries now carry
  `skip` (the heard ring) and `noSerious`. Note: a goodbye cut short is in the ring already (linesHeard at the pick), so
  the retry picks another goodbye for that pair (there are 3 pair:friend ones), not the same one. That's fine.
- In play (content 92866aa baked): the same 8 overheard conversations at the same minutes as 0.43.25 and 0.43.28.
- With content fe380dd baked: content_gen 434 conversations, **lines_check PASS** (0 errors, 3 warnings).

## Content fe380dd (0.48.52 fixes, 0.48.53 two pair:mentee goodbyes)
- The voice cards (Kovac, Cruz, Keane, Larsen), the file comments, briefs.md, voice-bible.md and outlines.md now
  describe the lift club and quick breakfasts; Keane's "Leg day." -> "Steady."; Pell's line -> "Saved me pudding when I
  was late". Searching content/ for "take(s) the ladder", "ladder club", "skip(s/ped) breakfast", "for the exercise"
  leaves only Lemaire's comet joke, Rina asking *you*, and the rule lines themselves.
- **LOW:** facts.md Zeke Torres still says "Skips breakfast for ten more minutes with the coils." His lines were
  changed to "last in to breakfast", so the fact sheet should say that too. Also goodbyes.lines' header still lists
  B as "friend, best friend, mentor or partner" (add mentee).
- Needs dialogue 0.43.29 in the same candidate (pair:mentee); 0.43.28 or older fails lines_check on it.
