# Review: content 0.48.51 (92866aa), the writing follows the game (the lift club; no skipped breakfasts)

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS WITH FIXES.** One fix, in the writers' sources only: nothing the
game shows. Two LOW.

## Tests
- Baked into dialogue 0.43.28 (754ddbd) with its own content_gen: 6,659 lines, 432 conversations; **lines_check PASS**
  (0 errors, 3 warnings). `banks/missing.lines` ({missed}) is unchanged since fd3db63, so it still needs dialogue
  0.43.27+ (0.43.28 now); with 0.60.3's dialogue (0.43.23) lines_check fails (content-5e2605e-fd3db63.md).
- **"Ladder" in the baked game text** (92866aa's html): what the player can see is the Spine ladder's own tap texts
  ("maintenance ladder"), Zeke's new "The ladder's behind the glass. Maintenance only. Thirty-one rungs.", "one ladder"
  in a bunk tap, and "gladder". **No line says anyone takes the ladder.** Kovac's arc beat 1 still has `mem: ladder`,
  an internal key that is never shown.
- **Skipped meals** (content lines, any meal, "skip/skipped/no breakfast/not eaten/forgot to eat"): what's left is
  Lemaire's comet joke ("Why did the comet skip breakfast?"), Rina asking *you* if you skipped breakfast, Brennan's
  "You've not eaten" to you, "Who's not eaten?", Zeke's "Never skip tea", and the late-meal reaction "Skipped
  dinners are not [fine]". None says a crew member skips a meal, except the LOW below.
- I read all 41 changed lines: they keep the voices (Kovac's "Lovely lift", the rail).

## Findings
1. **FIX (writers' sources, not shown in the game): the voice cards still say they take the ladder and skip breakfast.**
   `voices/kovac-zainab.voice` jokes: "\"I'll take the ladder. Exercise.\""; `cruz-tove.voice`: jokes "takes the ladder
   \"for the exercise\"", the MOOD TELLS ("Nervous = the ladder") and RUNNING lines; `keane-davi.voice` header ("he takes
   the ladder \"for the exercise\"", "Ladder's good for the legs!"); `larsen-hamid.voice`: "skips breakfast while telling
   everyone not to" (jokes, RUNNING, WHAT HE NOTICES). The game doesn't use `jokes`; I checked that voiceCard never
   reads it. But these cards are what writers write new lines from (and the Voices sampler shows them), so the
   next batch would bring the ladder back. Also the comments in kovac-zainab.lines, keane-davi.lines and circles.lines
   ("the ladder is only ever 'exercise'"), santos-zofia.lines ("skips breakfast"), briefs.md ("the ladder club") and
   voice-bible.md section 9 ("anyone who avoids the lift 'takes the ladder'") still say the old rule.
2. **LOW:** keane-davi.lines 48 "Lift? Course. Lovely lift. I'll just hold this rail. Leg day." The "Leg day" was the
   ladder joke; without the ladder it doesn't follow.
3. **LOW:** pell.lines 160 "{friend}'s all right. Fed me when I forgot to eat. Twice. In one day." It's a crew member
   missing meals, in the spirit of what was changed.
