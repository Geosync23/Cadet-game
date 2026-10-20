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
| `content/talkpack/<crewId>.talk` (15 files) | each named character's own talks, 4 each | 60 | 540 |
| `content/talkpack/smalltalk.talk` | `== small` (22, no question), `== done` (6 "talked about everything"), and Saruth's no-contraction `small.saruth` (6) and `done.saruth` (2) | | 36 |
| **Total** | | **160** | **1,476** |

A **line** here is one card line, one button text or one answer (a talk is nine: 2 `them:`, the ask, 3 replies, 3
answers). Pool tiers: 29 talks at any tier (strangers too), 39 from acquaintance, 20 from colleague, 12 from friend.

### Who has their own talks, and why (15)

| Crew | Why |
| --- | --- |
| Torres, Calder, Tomas, Pell, Rina, Brennan, Vance, Marrow, Holt, Kovac | the ten story crew (the voices the user approved, with arcs); every one's talks keep clear of beats not yet told |
| Envoy Saruth | the guest who lives aboard: doesn't draw the pool (it's crew life), so needs their own; no-contractions voice |
| Kofi Mensah | Holt's deputy and the night Watch; a strong, warm voice the player meets on rounds |
| Dr. Nandakumar | Rina's chief and the infirmary; "drink some water"; the player sees her from Day 2 |
| Dr. Sato | Head of Survey, a distinct voice (the tea, the comets); a named "story crew" in the design doc |
| Emeka Halloran | the Works officer the player works beside daily (the mug, the joke at breakfast) |

Each set is four talks on four different topics, laddered: one at any tier or acquaintance, one acquaintance or
colleague, one colleague, one friend. Arc-gated: `rina.gran` waits for `beat:rina.4`, `holt.saruth` for `beat:holt.2`;
`halloran-emeka.mug-rack` for `flag:mug` (after the Day 5 mug); `torres-zeke.scarf-rows` for `mem:moment.torres.scarf` (after his beat 1). The file comments name what each must never say.

## The file format (`.talk`)

New extension on purpose: `content_gen.py` walks `content/` and bakes every `.lines` file, so `.talk` keeps the pack out
of the game until the engineer adds a reader. It follows the `.lines` and `.arc` grammar wherever it can.

```
@talks pool                       <- whose talks: "pool", a crew id ("calder"), or "smalltalk"
topic: hobby                      <- pool files: the topic for every talk in the file (frozen: see ids)
// comments as usual

== one-hour                       <- a talk, by its slug
when: tier>=acquaintance !who:pell   <- optional: conditions, the frozen vocabulary (README "Conditions") + 1 new word (thread:)
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
- **Tone tags** `#funny`, `#warm`, `#serious` as in `.lines`, on `them:` and `ask:` lines (one ask carries `#funny`). `#serious` is only ever behind `tier>=friend` (one line in
  the whole pool).
- **Lengths:** `them:`, `ask:` and answers are card lines, 90 characters at most (a placeholder counts 9). **Replies are
  button texts, 44 at most**, with no voice tokens and no placeholders.
- **Placeholders** as in `.lines` (`{hobby}`, `{hobbyNoun}`, `{home}`, `{friend}`, `{boss}`, `{trad}`, `{dish}`, `{me}`, `{nick}`).
  `{hobby}` is the roster's verb phrase ("knitting scarves": only after "I've been" / "gave up"); `{hobbyNoun}` the noun
  ("knitting"). `{trad}` is the next tradition the speaker could go to (skip rec-deck ones while `REC_DECK` is off), and
  needs a capital when it starts a line (`pool.tradition.coming`).
  **If any placeholder in a talk can't be filled, skip the whole talk** (not just the line: a talk with a hole in it
  makes no sense). Voice tokens (`{hi}` etc.) work but the pool hardly uses them: these are said in full sentences.

### Talk ids (what "fired" saves)

- Pool: `pool.<topic>.<slug>` (`pool.hobby.one-hour`). Own: `<crewId>.<slug>` (`calder.serials`).
- **The topic in an id is the file's `topic:` header, frozen:** a talk never overrides it and never moves file (slugs
  repeat across topics: `portraits` is in hobby and ship, so the topic must stay in the id).
- **Written by hand, not hashed:** rewording a line keeps its id, so a save's "fired" list stays right after an edit.
  A slug is never reused for a different talk (the "parked, never deleted" rule: a cut talk's id stays retired).
- Saved per save as `{ id: [day, crewId] }` (when and with whom it fired), not a bare set: "a topic you haven't talked
  about with this person lately" reads it, and it helps debugging. Small talk keeps one `lastDone[crewId]`.
- The pool is fired **per save, not per person** (**the user's decision, 2026-10-20:** keep strict once-per-save, no
  repeats; more pool talks will be written when the game grows past Day 30): once you've had
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
| `!moved:<id>` | talks naming crew who leave mid-year (Teague day 35, Lindqvist, Santos, Grieve, Haddad...) | yes |
| `!dept:` | "I'd like to see the bridge" (not helm, command); "{boss} said nice work" (not Works: Calder never says it) | yes |
| **`thread:<theme>` / `!thread:<theme>`** (new) | the speaker's roster `thread` (the struggle theme): pool talks that would tell a theme's story early skip people on it (`talent`, `homesick`, `notgood`, `leaving`, `family`) | **no: please add** (lines_check too) |

**Guests** (`rank:guest`: Saruth, visiting guests) don't draw the pool: the pool is the crew's life (bunks, shifts, the mess). Saruth
has own talks only, then small talk from `== small.saruth` / `== done.saruth` (no contractions; any Veyli guest too). If that runs out too fast, a `fit:guest` tag can open chosen pool talks later.

**The career month:** the pool never mentions a promotion, an event (the ion storm, Founding Day) or an arc beat that
may not have happened. Talks that lean on your progress use `rep:`, `flag:`, `mem:` or `beat:` (all checkable). (`aboard>=` and `tpl:` were
proposed and dropped: nothing needs them now.)

## Picking a talk (the run-out order)

When you tap Talk a while with someone:

1. **Their own talks** (`<crewId>.talk`) that pass `when:` and haven't fired, in file order (they're written as a
   rough sequence: the first is the get-to-know-you one).
2. Else **the pool**: talks that pass `when:` and haven't fired. Prefer a topic you haven't talked about with this
   person lately, then pick at random, seeded by ship day + speaker id (a reload picks the same talk; nothing at load calls `R()`). The pool is 100 talks, so with one talk a day
   per person and ~75 crew it runs out after about 100 talks in a save: a busy player meets the end in a few weeks of
   play, a normal one rarely.
3. Else **small talk**: three or four lines from `smalltalk.talk` `== small` over the 15 minutes, no question, no
   buttons (the friendship and social still count; the +2 from a reply doesn't). About one time in four, the first
   line is one from `== done` ("We've talked about everything, haven't we?"), and never twice running with the same
   person.

Own talks that fail `when:` today (a tier too low) wait: the pool fills in, and the own talk comes when it's ready,
ahead of the pool again. **The old topic lines** (`talk.<topic>.open/more/ask/reply/ans` in `content/banks/talk.lines`)
are replaced by the pack and the pack reuses some word for word: when the pack is switched on, **park them** (marked cut,
kept on record, keys retired: the cut rule), don't delete them. The other `talk.*` lines in `content/banks/talk.lines` (start, sit, filler, end, stop, the
go lines, the buttons) stay as they are and wrap every talk: start, then the talk, then filler if there's time left,
then end.

## For the engineer

- **Reader:** a `parse_talk_file` in `content_gen.py` beside `parse_lines_file`, baked to something like
  `TALKS = { pool: [{ id, topic, when, lines: [text...], ask, replies: { listen: { text, ans }, share: ..., cheer: ... },
  tone }], own: { calder: [...] }, small: [...], done: [...] }` with `when` as a `linesOk` condition object. Ids as above.
- **lines_check:** the same rules as `.lines` (lengths, banned words, British spelling, names, `#serious` earned), plus
  the shape (1-3 `them:`, one `ask:`, three replies each with an answer, replies 44 characters and no tokens), unique
  ids across the pack, and the new condition word `thread:`. TW1 checked the pack with a scratch script that does exactly
  that (all clean); the notes below list what it checked.
- **The +2 for the matching reply** works as today (`needs:` on the voice card; the game's `talkNeed` gives `practical`
  cards their +2 on **listen**, so the listen answer is the warm one for Calder, Holt, Vance, Nandakumar and Halloran).
  Answers are written so any reply is welcome.
- **Save:** `{ id: [day, crewId] }` for fired talks, `lastDone[crewId]` for small talk. Small talk doesn't fire.

## Notes for the engineer and the next writer

- **A talk's pool is "fired per save":** with ~100 pool talks, the friend-tier ones (12) arrive late in a save, by
  design. If the playtest shows the pool running dry too soon, the next writer adds more (ids never reused).
- **Placeholders that may not fill:** `{friend}` (crew topic, 4 talks), `{boss}` (`pool.work.well-done`, skipped for
  the Captain), `{trad}` (`pool.tradition.coming`), `{dish}`, `{hobby}`, `{home}`. Skip the whole talk if one won't fill.
- **`!who:`** is used a lot: a pool talk that mentions a named crew member skips that person (and the people a shared
  quirk belongs to, e.g. the four lost-property keepers). Keep doing this when adding talks.
- **Smalltalk** is said by anyone, guests included, so it's neutral; it's the only part of the pack that repeats.
- **Checked:** every file passes a scratch checker with lines_check's own lists (lengths, banned words, US spellings,
  one "!" a line, the talk shape, unique ids, known condition words). `content_gen.py --check` is unchanged and
  `lines_check.py` passes, because neither reads `.talk` yet.

## TR1's review (plans/talk-pack-review.md on claude/talk-pack-review): what was taken

All 7 blockers fixed (Torres's scarf gated after his beat 1; Holt's locker test replaced with `holt.doors` and his
Envoy talk kept at the door, no tea; the Captain's `one-question` and `admiral` replaced with `the-step` and
`quiz-third`; the lift club no longer named in the pool; the `{hobby}` sentences rewritten). Slugs changed before
anything shipped (`holt.nearest-locker`, `marrow.one-question`, `marrow.admiral` are retired, never reused).
Should-fix S1-S38 taken, with these differences:
- **S7:** `!moved:` added; Vance's leaderboard drops the three names.
- **S16:** `flag:mug` for the mug rack, `rep:known` for `pool.work.proud`; `aboard>=` dropped.
- **S35:** Brennan's bread and Mensah's night round no longer invite you; Nandakumar's "sit with me sometime" went too.
- **S38:** all the listed food swaps except Vance's (kept, as suggested).
Nits taken: N1-N8, N10-N18, N20-N30 (N9: the new-faces ask now works in any month; N16 removed). **Not taken:** N19
(night-shift crew and "evening" talks): no shift condition exists; low risk, left for the engineer.
**New canon for `facts.md` 11** (the head writer logs it when the pack goes in): Saruth's knock count; Mensah's good
night to the decks; Calder's slogan mug in the machine shop; Halloran's cup on Calder's desk at one; Sato's "two
comets count"; Kovac's 42 beans; Vance's seven salutes; the lighthouse song's disputed line; Holt's airlock-secrets
joke (Mensah's). Outside the pack: `traditions/new-hands-tea.trad`'s comment says Calder hangs your mug, facts 11 says
Halloran gives it (a backlog row for the head writer).

## The old topic lines: parked (2026-10-20)

TR1's call, through lead 20: the old `talk.<topic>.*` lines in `content/banks/talk.lines` are **parked**, as a marking
only: a comment in that file says they're unused while `TALK_PACK_ON` is on and kept for the switch-off path. Keys and
lines unchanged, never deleted; recorded in `design-doc.md` ("Talking").
