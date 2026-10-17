# Review: claude/dialogue 0.43.1-0.43.3 (up to d1309a8), reviewer 2

**Verdict: PASS WITH FIXES** (one medium content risk, two low). Base: ship-integration 0.60.0.
Checked: the game diff; whether MOMENTS, MOMENT_THEMES and LINE_PLACES are declared on any other branch (no; GUESTS
is the existing roster const); every place alias against the real room names (all nine match: Mess hall, Junior common
room, Bow lounge, Call-home booths, Engine overlook, Tea corner, Works bay, Chart room, Music room). Then I baked
README's own .arc example: 2 moments, a second run gave "no change", and the warmer answer (`+`) is kept. Finally I
fed it bad .arc input: a bad flavour, a bad tone, beats out of order, bad mail, a misspelt when word and an unknown
token are all rejected with file:line; an unknown `who` is caught by lines_check.

1. **MEDIUM (romance with the player must never happen):** moments are one-to-one scenes with you, so this is where
   the rule matters most. The banned list catches "kiss", "darling" and "love you" in them lines, replies and warm
   answers, but **"I think I'm falling in love with you." passes both tools.** So would "in love", "fallen for you",
   "marry me" and "my heart". Add patterns like `\bin love\b`, `\bfall(ing|en)? for you\b`, `\bmarry\b` and
   `\bmy heart\b` (the reach of a word list is limited, so the head writer's read of every moment for this rule stays
   the real safeguard; please put that in the README).
2. **LOW:** four `*` replies are accepted by both tools, though the README says "up to three" (the meeting panel
   on a phone). Make it an error.
3. **LOW:** an unknown pose (`[dance]`) is accepted by both tools. The README lists sigh, laugh, listen, nod and
   gesture; check against that list, so the crowd or panel never gets a pose it can't play.
- Fine: `ctx.flags` only answers for keys it was given (other flag: words still read section 13); linesWho finds GUESTS
  for guest voice cards; the `place:` aliases and `_` for spaces; no hash keys outside 750-799; no R() or Math.random.

## Addendum: 8e38f76 (tools only): PASS
Re-tested with the same inputs: "falling in love with you" and "fallen for you" are errors, 4 replies is an error,
`[dance]` is an error. Note the trade-off: the wider list also stops innocent lines ("Brennan's in love with that new
oven", "my heart can't take it") and background couples' lines ("those two are in love"). That's the safe side, but
writers will hit it, so the README should say to reword, or have the head writer approve a specific line id.
