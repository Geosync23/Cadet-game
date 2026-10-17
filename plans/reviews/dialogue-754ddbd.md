# Review: dialogue 0.43.28 (754ddbd), the fixes for 0.43.26

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS for 0.43.26's findings** (both fixed). **0.43.27's MUST-FIX
(pair:mentor either way, dialogue-c084a1a.md) is still open**: linePair is unchanged in 754ddbd.

- **The chatter must-fix:** `OVH_PER_FRAME = Infinity`, so the minute's tries run in its own frame again, before section
  20's chatter. The same in-play run as before (content 92866aa baked into both; Deck 3 day 8 from 12:20 and 18:30,
  Deck 2 day 9 20:00, 3,000 frames each): 0.43.25 and 0.43.28 play **the same 8 conversations at the same minutes**
  (tr7nu8, 1vkzvo3, 1xmqgi4, e0c8j6, 1oaa56m at 19:09 is back, ql68kg, 1j1354q, 176ulv4).
- **The cue memo:** keyed on the cue array itself (`LINE_CUE.arr !== SHIP.social.cues`) plus `now`; section 20 makes a
  new array on every new cue, so a cue added at the 30-cue cap is seen. The comments now say "while the clock stands still".
- lines_check PASS with content 92866aa.
