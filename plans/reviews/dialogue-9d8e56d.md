# Review: dialogue 0.43.24 (9d8e56d): {kin} {lost} {hobbyNoun}, and lines_check guards

Reviewer 2, 2026-10-17. **Verdict: PASS WITH FIXES.** One check is missing, which I recommend adding before the writers switch over.

What holds:
- `linesFill`: for kin, lost and hobbyNoun it asks socialFill first, and when that answers null it uses the roster field. The token pattern now allows capitals. No `{Capital}` text exists in content, so nothing that read before stops working. lines_check catches a stray `{Kin}` ("unknown token").
- lines_check on claude/content 0a86991 → FAIL with 16 errors. That is every `{family}` and `{hobby}` theme line I reported (10), plus `needs: family|hobby` (7 beats; one beat is reported twice). This is the intended guard: **dialogue 0.43.24 can't combine on its own** until the head writer's .arc fix and crew designer 3's roster fields arrive. Combine all three together.
- Negative tests: "My {kin}" (with a capital) → error. `needs: hobbies` → error naming the allowed values. `{Kin}` → unknown token.

## MEDIUM: nothing checks that a token in a line matches its beat's `needs:`

Test: in loss.arc I changed `{family}` to `{lost}` and `needs: family` to `needs: kin`. lines_check reports no error on loss.

In the game, social's beat check (`d.needs.some(f => p[f] == null ...)`) then lets everyone with a `kin` into the loss beats. Their `{lost}` lines fill as null and drop, so the beat plays with lines missing. Worse, it is exactly the "loss theme for someone who lost nobody" the lead's plan rules out.

Suggested rule for arcs and themes: every roster token in a beat's lines (home, since, kin, lost, hobbyNoun) must be in that beat's `needs:`. It's a few lines in the beat loop.

Note for the head writer and crew designer: loss beat 1 has no `needs:`. If beats 2 and 3 become `needs: lost`, crew on the loss thread without `lost` would get beat 1's opening and then nothing. Either beat 1 gets `needs: lost` too, or only people with `lost` are put on the loss thread.
