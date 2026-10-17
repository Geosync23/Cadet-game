# Review: dialogue 0.43.27 (c084a1a), goodbyes, pair:best/mentor, {missed}

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS WITH FIXES** (one MUST-FIX here; 0.43.26's MUST-FIX, chatter
cutting in on the spread-out scan, is still open and applies to goodbyes too).

## Tests
- claude/content fd3db63 baked into c084a1a: content_gen 6,659 lines, 432 conversations; **lines_check PASS**
  (0 errors, 3 warnings), so {missed} and pair:best/mentor are known words. Without 0.43.27, content 0.48.50 fails
  lines_check (see content-5e2605e-fd3db63.md).
- Read: `{missed}` uses `bond('missed')`, so a speaker who misses nobody gets null and the line is skipped (same path
  as {friend}). Goodbye tries come first in the scan, for everyone "around" (not only the first OVH_NEAR), only for a
  leaver (`leavingSoon`) with someone within OVH_PAIR, and once per pair (`SHIP.lines.bye`, saved and loaded, reset on
  a new game). They still wait for OVH_GAP, the chatter gap, bubbles and the hush, as before.
- Not seen in play: on a fresh game no leaver has a best/mentor bond yet (days 34 to 244, all 12 leavers: none), and
  Teague and Hart (the named pair) are never within 2 tiles of each other on days 33 and 34, so I couldn't stage a
  goodbye on the deck. The DEV_NOTES row says how the engineer tested it.

## Findings
1. **MUST-FIX: `pair:mentor` matches either way, but the lines assume B is A's mentor.** linePair: mentor is true if
   A mentors B *or* B mentors A. goodbyes.lines (whose header says "B is their ... mentor"): "Anything I should know,
   out there?" / "Ask. Listen. Write it down." / "That's what you said on day one." and "Thank you. For all of it." /
   "You did the work. I just watched." When the one leaving (A) is the mentor, the mentor asks their mentee for advice
   and thanks them for teaching. Fix: make `pair:mentor` one way (B is A's mentor: `bondOf(a, 'mentor') === b`), add
   `pair:mentee` for the other way if writers want it, and fix the README and lines_check's PAIR_WORDS to match.
2. **LOW: the pair's goodbye is marked as said when it's picked, not when it's played.** If the conversation stops at
   its first line (one of them walks off, the hush, a deck change), that pair never gets another goodbye. Marking it
   in linesTalk when the last line is shown would let it try again.
3. **LOW: goodbye tries carry no `skip` (the heard ring) and no `noSerious`.** Today no goodbye is #serious, so it
   doesn't matter yet; if a writer adds a #serious goodbye it will skip the one-serious-a-day budget.
