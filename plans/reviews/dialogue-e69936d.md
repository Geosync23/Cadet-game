# Review: claude/dialogue 47ba9e8 + e69936d (0.43.10-0.43.11: gift:, calls home), reviewer 2

**Verdict: PASS WITH FIXES** (two medium content risks in the call-file exemption).
Fine:
- HOME_CONTACTS, HOME_MOMENTS, HOME_SEND and HOME_CHAT are declared on no other branch.
- The head writer's mum.call (content 5a07b86, with the "(?)" marks removed) bakes byte-stable ("no change" on the
  second run) and passes lines_check clean.
- `gift:`, `came:` and `friend:` read only ctx, with no saved state.
- The new LINE_META keys (flavour, reply, sets, memo) are data, not conditions, as intended.

1. **MEDIUM:** the family exemption in .call files reaches further than "love you". "I'm still in love with you, you
   know." passes in a call from Sam. The user's rule is no romance with the player, ever, including people back
   home. Keep only the family phrases ("love you", "love you, pet") exempt in .call files, and keep "in love",
   "my love", "darling", "fallen for", "marry" etc. as errors there.
2. **MEDIUM:** contacts aren't limited to the user's fixed cast (Mum, Gran, Jo and Sam, by the user's ruling 2026-10-17).
   A `home:partner` contact named Alex, saying "Love you. I'm counting the days till you're home, my love.", passes. Make
   any home id outside mum, gran, jo and sam an error (a list kept by the head writer, from facts.md), and add "my love" to
   the banned list in every kind.
3. NOTE: Sam's relation to the player should be written down in facts.md (sibling? friend?), so "love you" from Sam
   reads as family or friendship and the writers have a canon to check against.
