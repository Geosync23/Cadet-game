# Review: dialogue 0.43.21 (b8cf2d9): {home} {family} {hobby} {since} through socialFill

Reviewer 2, 2026-10-17. Tested on a trial combine: social 84e992e (0.36.64, on 0.60.2) + dialogue b8cf2d9, rebaked with content_gen.

**Verdict on the change itself: PASS.** It is one line, which adds the four names to `SOCIAL_FILL`.
- On the trial combine, every crew member gets all four filled on days 1, 30, 120 and 400, with no nulls. `{since}` grows: Marrow's "six years" on day 1 is "seven years" on day 400.
- lines_check PASSES. The game loads with no errors.
- Combine note: on dialogue's branch alone, section 20 answers null for these four. The lines that use them then drop quietly; nothing leaks or crashes. Ship it only with social 0.36.60 or later, as the commit says.
- Small (social's socDuration): the durations mix digits and words, "21 months" next to "eighteen months".

## HIGH, not caused by this commit and already in the released 0.60.2: the theme lines and the roster's `family`/`hobby` don't fit together

The writers' theme files (content/themes/*.arc, head 1) assume `{family}` comes with "my" ("my gran"). Social's socialFill says the opposite: "as written (writers say 'my {family}')". The roster's `family` is a description, not a "my" phrase: 0 of 87 values start with "my". The values were the same before 0.43.21, so this is not new, but here is what the released game says, rendered with `linesFill` in the browser:

- Oduya (loss theme): "It's the day we lost late wife, who I still talk about. Years ago now." and "To late wife, who I still talk about. Who laughed at everything."
- Hart (loss): "It's the day we lost parents, who run a repair shop." Present tense, so they are dead and running a shop at once. Every loss-theme person except Oduya has living family in their roster and in their about lines: yoon-elif and garcia-greta "aunt, who was a pilot", bakshi-sol "twin", eklund-leila "younger brother". So the loss theme kills a relative that the person's other lines treat as alive. That's a serious line that contradicts the rest of the game.
- Ferreira (family): "It's big family, who all talk at once. Not well. They've gone into hospital, back home."
- Halloran (family): "News came this morning. Mother, who writes every week's home."
- `{hobby}` assumes a noun ("painting"), but the roster gives phrases. Quist (talent): "Me, teaching reading mystery novels. Imagine." Ibarra: "Just a bit of doing crosswords in the bow lounge."
- `{home}` and `{since}` read fine.

Lines affected: family.arc 24 and 42, loss.arc 25, 42 and 49, and talent.arc 9, 11, 26 and 42.

Possible fixes, for the lead to assign: a short roster field for the themes (`kin: "my aunt"`, and a `lost:` only for people whose roster really has someone gone, like Oduya), or socialFill cutting at the comma and adding "my", which still leaves the loss contradiction. The loss theme needs `needs: lost` (or similar), so only people with a real loss get it. That is a story decision: who aboard has lost someone.
