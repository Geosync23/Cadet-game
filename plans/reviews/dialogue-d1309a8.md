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

## Addendum: e507613 (0.43.4): PASS WITH ONE FIX
- Player-facing kinds: the full ban holds. Overheard couples' "We should tell people we are in love." passes, as
  intended.
- **MEDIUM:** overheard lines *about the player* also pass: "I think I am in love with the new hand." is accepted
  (only "crush" happened to be caught). That is romance involving the player, which is never allowed. Fix: in overheard
  conversations, the romance words are allowed only when the line names no player reference (`{me}`, "the new hand",
  "the cadet", "new cadet", "you"), and ideally only under a `bond:couple` pair condition.
- LOW (false positives): "married" and "wedding" now stop ordinary family lines in moments ("My parents have been
  married forty years."), which the family and homesick themes will want. Consider keeping those two for overheard
  and you-directed checks only, or allow them when they don't sit next to you/me.

## Addendum: 09b8c33: BLOCK for writers on overheard, about, rumour and smalltalk until fixed
The relaxed kinds now let romance *about the player* through, because BANNED_AT_YOU only matches second-person
phrasings. All of these pass lines_check as overheard lines:
- "I think I am in love with the new hand."
- "Torres is sweet on the cadet, you know."
- "Rumour is {me} and Pell are dating."  ("dating" isn't on any list)

`rumour` and `about` are lines a crew member says *to you* on the chat card, so they are player-facing, not
background. Fix:
1. In every relaxed kind, any romance word plus a player reference is an error. Player references: `{me}`, `{nick}`,
   "the new hand", "the cadet", "new cadet", "the newcomer", "you", "your".
2. Put `rumour` and `about` back under the full ban (keep the relaxation for overheard, smalltalk between two crew,
   and bond:couple lines).
3. Add `\bdating\b`, `\bgoing out\b` and `\bseeing each other\b` to the couple-words list (so they're judged by the
   same rules).
The allow list by line id is a good way out.

## Addendum: 453c577 (0.43.5): PASS WITH ONE ONE-LINE FIX
Re-tested. These are now errors: "in love" without a couple pair; "in love with the new hand" and "sweet on the
cadet" even under pair:couple; "Torres is sweet on you" as a rumour. "My parents have been married forty years."
passes, as it should.
**Still open:** "dating" is on no list, so "Rumour is {me} and Pell are dating." passes both as an overheard line
(under pair:couple) and as a rumour said to you. Add `\bdating\b`, `\bgoing out\b` and `\bseeing each other\b` to the
couple words, so the player-reference rule catches them. Once that's in, writers can start on every kind.
