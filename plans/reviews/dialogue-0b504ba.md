# Review: dialogue 0.43.26 (0b504ba), the performance pass

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS WITH FIXES** (one MUST-FIX, two LOW).
Builds under test: 46e948b (0.43.25) and 0b504ba (0.43.26), each with claude/content's content/ baked in by its own
content_gen.py (6,659 lines, 432 conversations), since the dialogue branch alone has no conversations to pick from.

## Tests
- **lineFor, called directly:** 80 crew x 15 kinds x 5 days x 4 times (22,200 calls, 17,266 lines): **identical** in both
  builds (the top-score-only fill, lineQuick and the cue memo give the same picks). Overheard pairs called directly: identical.
- **Overheard conversations in play** (the real linesTick, Deck 3 day 8 from 12:20 and 18:30, Deck 2 day 9 20:00,
  3,000 frames each; the same both runs, so deterministic): 0.43.25 plays 8, 0.43.26 plays 7. They agree up to 18:42;
  at 19:09 0.43.25 plays `1oaa56m` and 0.43.26 plays nothing, and from then on the picks differ (20:04 `ql68kg` vs `yr5po3`).

## Findings
1. **MUST-FIX: section 20's chatter now cuts in on a scan, so overheard conversations are lost.** Logged at 19:09:
   the scan has 2 tries; frame 1 runs the reaction try (nothing); in frame 2 a chatter bubble ("Is it Friday? It feels
   like a Friday.", started one frame earlier: `CHATTER_AT` 33 ms old) is up, so `linesScan` sees `bubbles.list.length`
   and drops the scan; `OVH_MIN` is already this minute, so nothing is tried again. In 0.43.25 every try ran in the
   linesTick frame, before the chatter's turn, so the overheard conversation won and the chatter found the bubbles busy.
   So "same picks" holds for the functions but not in play: about 1 in 8 overheard conversations lost in this sample,
   and every later pick shifts. Fix ideas: section 20's chatter skips while `OVH_SCAN` is set (one condition on its
   line `if (CHAT || sleeping || ...)`, social A's section, so agree it with them), or keep the minute's chatter roll
   until the scan ends. Recheck: the 3 runs above give the same 8 conversations as 0.43.25.
2. **LOW: the cue memo can serve a stale answer, but only in a narrow case.** It is keyed on `shipNow()` and
   `SHIP.social.cues.length`. `shipNow()` is fractional (`SHIP.time.min += dt * SHIP_RATE`), so while the clock runs the
   memo lasts one frame, not "the minute" (the comments say minute). It lasts longer only while the clock stands still.
   The stale case: socialCue pushes then `filter(...).slice(-30)`, so once the list holds 30 cues a new cue leaves the
   length at 30. If that happens while the clock is stopped (or within one frame), `cue('gift.you')` keeps answering
   from before the gift. A new game or a loaded save at the same `shipNow` with the same length would be the same.
   Fix (one line): key on the array itself (`LINE_CUE.arr !== SHIP.social.cues`; socialCue makes a new array every
   time it adds one) plus `now`. Then the lead's case (a bond or flag changing mid-minute) can't go stale either:
   only cue is memoised; bonds, flags and the rest are asked fresh each time.
3. **LOW: the comments** "cue answers kept for the minute" (lineQ, LINE_FAST, the dev notes row) should say "while the
   ship clock stands still (in practice, a frame)".
