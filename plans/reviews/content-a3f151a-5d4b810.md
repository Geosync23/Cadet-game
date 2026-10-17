# Review: content a3f151a..5d4b810 (0.48.43 to 0.48.47) for 0.60.4: content/ only

Reviewer 2, 2026-10-17, as build master 2 asked. **Verdict: PASS WITH FIXES.** One fix, to Tomas's week-1 beats.

What's in it: the theme switch to {kin}/{lost}/{hobbyNoun}, 17 goodbye conversations for rotation days, week-1 beat bubbles and Mails (Brennan, Calder, Leila Eklund, Halloran, Orla Ishikawa, Pell, Tomas, Torres), Rina's introHealth, voice cards losing `thread:`, and content/traditions/ dropped.

Checked:
- lines_check (the copy is identical to dialogue 46e948b): PASS, 0 errors, the same 3 warnings as before.
- The theme fix with roster d53cf40 (0.16.15):
  - every family-thread crew member has a `kin` ("my mum" … "my big sister"), and no kin lacks the "my";
  - every loss-thread crew member has a `lost`, and it is never the living relative in their `family`/`kin` (Hart: lost "my grandad", kin "my dad"), so the contradiction I reported is gone;
  - every talent-thread crew member has a `hobbyNoun`, every homesick one a `home`, every stuck one a `since`.
- Romance: none. Brennan's "love" is his established voice (17 lines before this range). The goodbyes are crew to crew, with no player in them.
- Week 1: nothing serious, no names that aren't aboard. Times match the game: breakfast to 08:00, quiz Thursday, film and sowing Saturday. Torres off Thu/Fri matches the roster ([3,4]) and his work deck 6 (the engine) matches.

## Fix (MEDIUM, week 1, first impressions): Tomas isn't off on Friday and Saturday
tomas.lines (batch 9) says "Tomas is off Fri-Sat, so d5 and d6 are his own time". That comes from content/facts.md ("Fri, Sat"). But the roster in the released 0.60.2 and in crew designer 3's d53cf40 has `offDays: [0, 1]`, which is **Monday and Tuesday** (`weekday` 0 = Monday, `isWorkDay`). So on Saturday 11:45 Tomas is on day shift at the Deck 2 watch station while his garden beat says "Day off. Nobody's working." Either move the beats or the speaker, or the crew designer gives Tomas Fri/Sat, if week 1 needs him then.

## Wider (for the head writer): facts.md's days-off column is stale
facts.md's days-off column matches the released roster for only **22 of 74** crew. Examples: Marrow "Mon, Tue" in facts, Sat/Sun in the game; Janssen "Sat, Sun", Mon/Tue in the game. It matches claude/content's own older game file (Tomas [4,5]), so the rotas were reshuffled since. Any line naming a day off can be wrong. Regenerate the column from the roster before the next batch.

Low:
- Rina's introHealth lists "Hunger, energy, hygiene, social, fitness". The Needs app says **Food** and also has **Bathroom**. Use the app's words.
- hobbyNoun "collecting" (Juarez, talent thread) gives "Me, teaching collecting. Imagine." and "I do a bit of collecting". "Collecting mission patches" would read better, or "patch collecting".

Combine: as build master 2 says, it needs dialogue 46e948b, social 0811adc and roster d53cf40 in the same candidate.

## Addendum: 5d4b810..5e2605e (0.48.48): PASS
- facts.md's days off now match roster caedef2 (0.16.19) for **all 74** crew (none differ). Tomas is Mon/Tue.
- Rina says "Food, energy, hygiene, social, fitness, bathroom", the app's six.
- Tomas's d6 line: "Your day off. My lunch break. Holt said ten minutes." Note for **onboarding**: the game has **no lunch** (two meals; no 'lunch' act is ever planned). On Saturday 11:45 Tomas's plan has him on watch on Deck 2, so the beat only works if the onboarding hook brings him to the garden (an appointment or crewHold). Check that it does. Also, Holt is off on Saturdays ([5,6]); "said ten minutes" still reads fine as said earlier.
