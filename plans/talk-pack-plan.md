# The "Talk a while" pack: plan and data shape

**TW1 (head writer of the pack), for lead 20 and the engineer who wires it** after Dev mode and the playtest patch.
Content only: nothing here touches `starship-cadet.html`, and `content_gen.py` doesn't read `.talk` files yet, so the
game and `content_gen.py --check` are unchanged until the engineer bakes them.

## The user's rules (from the roadmap, 2026-10-20)

1. **No repeats.** Once a talk fires, it's done for that save.
2. **A shared pool** any character can draw from (talks that don't fit someone carry a condition so the engine skips
   them), **plus each named character's own** few.
3. **Shorter talks are fine, but keep the question:** their question to you, your three replies (listen = curious,
   share = about you, cheer = light), their answer to each.
4. **Run-out order:** the character's own talks first, then the pool; when both are used up, light small talk with no
   question, and now and then "We've talked about everything, haven't we?".

## What's in the pack

| File | What | Talks | Lines |
| --- | --- | --- | --- |
| `content/talkpack/pool-<topic>.talk` (10 files) | the shared pool, 10 talks on each of the ten topics | 100 | 900 |
| `content/talkpack/<crewId>.talk` (15 files) | each named character's own talks | (see below) | |
| `content/talkpack/smalltalk.talk` | small talk with no question, and the "talked about everything" lines | | |

A **line** here is one card line, one button text or one answer (a talk is about nine).

## The file format (`.talk`)

New extension on purpose: `content_gen.py` walks `content/` and bakes every `.lines` file, so `.talk` keeps the pack out
of the game until the engineer adds a reader. It follows the `.lines` and `.arc` grammar wherever it can.

```
@talks pool                       <- whose talks: "pool", a crew id ("calder"), or "smalltalk"
topic: hobby                      <- pool files: the topic for every talk in the file (a talk may override it)
// comments as usual

== one-hour                       <- a talk, by its slug
when: tier>=acquaintance !who:pell   <- optional: conditions, the frozen vocabulary (README "Conditions") + 2 new words
them: I've been {hobby} again. It's the one hour my head goes quiet.     <- the opener
them: Nobody needs anything from me.   #funny                            <- 0-2 "more" lines
ask: Have you got a thing yet? Something you do just because?            <- the question (exactly one)
listen: How did you get started?                                         <- your three replies: button texts,
  them: Someone showed me, years back. Now I can't put it down.   #warm   <- each with their answer, indented
share: Still looking. I might try a few.
  them: Try a few. One will stick.
cheer: Sleep. I'm very good at sleep.
  them: Underrated hobby. You'll go far.   #funny
```

- **Every talk** has 1-3 `them:` lines, one `ask:`, and all three replies (`listen`, `share`, `cheer`) each with one
  indented answer. The order on the card is: the `them:` lines (the first is the opener; the rest play as "more" lines
  every few seconds), the ask, the three buttons, the chosen answer.
- **Tone tags** `#funny`, `#warm`, `#serious` as in `.lines`. `#serious` is only ever behind `tier>=friend` (one line in
  the whole pool).
- **Lengths:** `them:`, `ask:` and answers are card lines, 90 characters at most (a placeholder counts 9). **Replies are
  button texts, 44 at most**, with no voice tokens and no placeholders.
- **Placeholders** as in `.lines` (`{hobby}`, `{home}`, `{friend}`, `{boss}`, `{trad}`, `{dish}`, `{me}`, `{nick}`).
  **If any placeholder in a talk can't be filled, skip the whole talk** (not just the line: a talk with a hole in it
  makes no sense). Voice tokens (`{hi}` etc.) work but the pool hardly uses them: these are said in full sentences.

### Talk ids (what "fired" saves)

- Pool: `pool.<topic>.<slug>` (`pool.hobby.one-hour`). Own: `<crewId>.<slug>` (`calder.serials`).
- **Written by hand, not hashed:** rewording a line keeps its id, so a save's "fired" list stays right after an edit.
  A slug is never reused for a different talk (the "parked, never deleted" rule: a cut talk's id stays retired).
- Saved per save as a set of fired ids. The pool is fired **per save, not per person**: once you've had
  `pool.hobby.one-hour` with anyone, nobody offers it again (otherwise the same story comes from three mouths, which
  reads as a repeat). Own talks are only ever said by their owner.

## Conditions

`when:` uses the frozen condition vocabulary from `content/README.md` ("Conditions"), read for **the speaker** (dept,
rank, trait, who) and **you with them** (tier, mem, flag, beat, rep). What the pack uses:

| Condition | Used for | Already in the engine? |
| --- | --- | --- |
| `tier>=acquaintance`, `tier>=colleague`, `tier>=friend` | the tier ladder (no tier = any tier, strangers too) | yes |
| `!who:<id>\|<id>` | **skip people a talk is about** (Brennan doesn't say "Brennan pretends not to see") or who it doesn't fit | yes |
| `rank:junior`, `!rank:captain` | talks about bunks or "my boss" | yes |
| `!newhere` | "my first month..." needs someone who's been aboard a while | yes |
| `beat:<arc>.<n>`, `flag:<key>`, `rep:` | own talks that follow an arc beat or your Works record | yes |
| **`aboard>=<days>`** (new) | days since you arrived (Day 0 = 0): "You've got good at this" waits two weeks | **no: please add** |
| **`tpl:<template>`** (new, proposed, not yet used) | the speaker's voice template (`gruff`, `shy`...), to skip a talk for a whole voice | **no: optional** |

**Guests** (Saruth, visiting guests) don't draw the pool: the pool is the crew's life (bunks, shifts, the mess). Saruth
has own talks only, then small talk. If that runs out too fast, a `fit:guest` tag can open chosen pool talks later.

**The career month:** the pool never mentions a promotion, an event (the ion storm, Founding Day) or an arc beat that
may not have happened. Talks that lean on your progress use `aboard>=`, `rep:`, `flag:` or `beat:` (all checkable).

## Picking a talk (the run-out order)

When you tap Talk a while with someone:

1. **Their own talks** (`<crewId>.talk`) that pass `when:` and haven't fired, in file order (they're written as a
   rough sequence: the first is the get-to-know-you one).
2. Else **the pool**: talks that pass `when:` and haven't fired. Prefer a topic you haven't talked about with this
   person lately, then pick at random (seeded, so a replay is the same). The pool is 100 talks, so with one talk a day
   per person and ~75 crew it runs out after about 100 talks in a save: a busy player meets the end in a few weeks of
   play, a normal one rarely.
3. Else **small talk**: three or four lines from `smalltalk.talk` `== small` over the 15 minutes, no question, no
   buttons (the friendship and social still count; the +2 from a reply doesn't). About one time in four, the first
   line is one from `== done` ("We've talked about everything, haven't we?"), and never twice running with the same
   person.

Own talks that fail `when:` today (a tier too low) wait: the pool fills in, and the own talk comes when it's ready,
ahead of the pool again. The existing `talk.*` lines in `content/banks/talk.lines` (start, sit, filler, end, stop, the
go lines, the buttons) stay as they are and wrap every talk: start, then the talk, then filler if there's time left,
then end.

## For the engineer

- **Reader:** a `parse_talk_file` in `content_gen.py` beside `parse_lines_file`, baked to something like
  `TALKS = { pool: [{ id, topic, when, lines: [text...], ask, replies: { listen: { text, ans }, share: ..., cheer: ... },
  tone }], own: { calder: [...] }, small: [...], done: [...] }` with `when` as a `linesOk` condition object. Ids as above.
- **lines_check:** the same rules as `.lines` (lengths, banned words, British spelling, names, `#serious` earned), plus
  the shape (1-3 `them:`, one `ask:`, three replies each with an answer, replies 44 characters and no tokens), unique
  ids across the pack, and the two new condition words. TW1 checked the pack with a scratch script that does exactly
  that (all clean); it's in the handover note if you want it.
- **The +2 for the matching reply** works as today (`needs:` on the voice card). Answers are written so any reply is
  welcome.
- **Save:** the set of fired ids. Small talk doesn't fire.
