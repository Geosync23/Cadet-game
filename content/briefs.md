# The writers' briefs (the head writer, wave 1b)

Three writers, one head writer. You write plain text under `content/` only, on your own branch; the head writer reads
every batch, sends notes, and merges what passes into `claude/content`. **You report to the head writer, never to the
lead or the user.**

## Read first (in this order)

1. `content/README.md`: the file formats and the condition words (the frozen vocabulary).
2. `content/voice-bible.md`: tone, the tier ladder, how a voice is made, the batch checklist.
3. `content/facts.md`: the canon. Never contradict it; ask before adding to it.
4. The story crew's voice cards in `content/voices/` (Torres, Calder, Tomas, Pell, Rina, Brennan, Vance, Marrow, Holt,
   Kovac): the model for yours.
5. `content/arcs/outlines.md`: the story crew's arcs and the struggle themes. Write no arc beat that isn't outlined.
6. `content/meetings/introBunk.meet` and `introChief.meet`: the model for scenes.
7. For your people: `plans/crew-roster.html` (bio, life, about, habits, traits, birthdays: all canon).

## Who writes whom

| Writer | Branch | Voice cards (wave 1b) | Own lines | Also |
| --- | --- | --- | --- | --- |
| **writer-works** | `claude/writer-works` | the Works crew: Navarro, Halloran, Reyes, Silva, Teague, Rossi, Rahman, Eklund, Moreau, Soto, Volkov, Quist, Keane, Jovanovic, Amadi, Salo (16, done in batch 0) | those 16, plus **Torres, Calder and Kovac** (cards are the head writer's) | the intro's meetings after Day 0 (`introBriefing`, `introSoloJob`), Torres's walking lines and week-1 lines, `newcomer` lines (the cadet you'll guide), a Works bank (`banks/works.lines`), Works overheard |
| **writer-command** | `claude/writer-command` | the six seniors (Kowalczyk, Raman, Ferreira, Oduya, Mensah, Mori), Nandakumar, Zielinski; Watch (Achterberg, Dahl, Garcia, Park, Vasquez, Shah, Chen, Nakamura, Ueda); Survey (Ibarra, Zamora, Lemaire, Fonseca, Kim, Yilmaz, Abara, Alvarez, Mbeki) (26, done in batch 0); **add: Farouk and Lindqvist (day helm and comms officers), Envoy Saruth, and the guests** | those, plus **the Captain, Vance, Holt** (cards are the head writer's) and **Sato** | banks for command, helm, comms, Watch, Survey; guests' lines (wait for the guests hook, below); Command/Watch/Survey overheard |
| **writer-commons** | `claude/writer-commons` | the galley (Walsh, Madsen, Varga, Haddad, Dlamini), store (Esposito, Ishikawa), infirmary aides (Grieve, Larsen), night shift (Yoon, Janssen, Takahashi, Bakshi) (13, done in batch 0); **add: the gardeners (Cruz, O'Neill, Hart) and the day helm and comms juniors (Strand, Santos, Tran)** | those, plus **Tomas, Pell, Rina and Brennan** (cards are the head writer's) | the shared banks (`banks/all-*.lines`, by rank and trait), **overheard conversations** and **reactions** (the ship-wide banks), the struggle themes (wave 2-3) |

The head writer writes: the story crew's cards, the arc outlines, the ten voice templates (with social B), the Day 0
meetings (done), and anything nobody else owns.

## Batch 0 (wave 1b, now): voice cards for everyone in your area

- One `.voice` per person in `content/voices/<crewId>.voice`, in the README's format, **plus comment lines** (`//`)
  like the story cards: HOW THEY TALK, WITH JUNIORS, WHAT THEY NOTICE, MOOD TELLS, NEVER, RUNNING. 100-250 words each.
- **Start from the roster.** Their traits, habits, bio, life and `about` are canon; the card turns them into a way of
  talking. Use the shared quirks in `facts.md` section 5 (the knitting circle, the ladder club, Gerald the cactus...).
- **Every card different.** Two Works technicians with the same traits still don't sound the same: give each a sentence
  shape, a pet word, a thing they notice.
- `tpl:` one of `warm dry shy brisk chatty earnest gruff dreamy steady playful`.
- `loves:` / `likes:` gift tags, for now only: `star music plant garden tea game book sweet card made`.
- `invites:` for now: `quiz observatory film jam running tiles swap gym garden tasting roast works-tea patrol`.
- `thread:` the struggle theme the roster's traits suggest (`homesick exams family stuck notgood lonely loss talent
  burnout leaving rivalry startover`), unless the crew designer's roster gives one (then theirs).
- `needs:` `listen cheer practical share`. `openness:` `open normal guarded`.
- **Pronouns:** add a row for every person in your area to your own subsection of `facts.md` section 4 (4a Works,
  4b Commons, 4c Command), choosing a natural mix; only that subsection, so branches merge cleanly.
- `nick:` five values; `-` means "cadet" at stranger and your name after. Only a few people use a real nickname.
- No pronouns for anyone `facts.md` doesn't list; write "they" or the name.
- **Run `python3 lines_check.py`** (it must say PASS), commit, push to your branch, and send the head writer: the
  commit, the list of cards, any canon questions.

## Batch 1 (wave 2): the voices for check-in A, then the arrival

The user approves the main voices on a **Voices sampler** page before the bulk is written. So batch 1 is small and
polished:

- **writer-works:** Torres and Calder, 12 lines each across tiers and kinds (greet, feel, near, life, joy, `week1`), plus
  Torres's walking lines for Day 0 (the stand-ins are `INTRO_LINES` in section 21: hello, haulway, works, lift, wing,
  toMess, servery, free, and the "this way" calls) as a plain list in a `.lines` file under `== week1` (the head writer
  and the onboarding engineer settle the exact hook). Kovac, 10 lines.
- **writer-commons:** Tomas, Pell, Rina and Brennan, 12 lines each across tiers and kinds; Tomas's and Pell's lines for
  the arrival evening (Tomas finding you after dinner; Pell joining the table).
- **writer-command:** the Captain, Vance and Holt, 12 lines each across tiers and kinds.

Every line in batch 1 is a candidate for the sampler, so: specific, in voice, mostly light, at least one funny and one
warm per person, nothing serious yet.

## Batches 2 onward (waves 2-4): about 300 lines a batch

In this order (the head writer adjusts as we go):

1. Story crew's everyday banks to about 120 lines each (greet by tier and time, bye, feel, near, life, joy, invite,
   accept, decline, hint, missed, birthday, week1 where they're in week 1).
2. Your area's people to about 30 own lines each (Works crew and your bunkmates about 60).
3. Overheard conversations (writer-commons leads; the others write their department's pairs) and reactions.
4. Callbacks (`mem:`/`told:`), cues, visits, notes, gifts, `about`, `rep`, `knownFor`.
5. Arc beats and moments as the head writer assigns them, from the outlines.
6. Goodbyes, letters, newcomers.

A batch is about 300 lines or 15-20 voice cards. One batch at a time: send it, wait for notes, fix, then the next.
The head writer replies within the batch: "merged", or numbered notes.

## How a batch is read (what the head writer checks)

The voice bible's checklist (section 11), and:

1. **Cover-the-name test** on five lines per person.
2. **Canon:** roster, `facts.md`, cards, already-told beats.
3. **Ratio:** mostly light; `#funny` about a third; `#warm` one in ten; `#serious` only where earned.
4. **Coverage:** every tier has lines; stranger lines teach something useful.
5. **Consistency** with what the other two writers wrote (the head writer reads all three).

## Practical

- Your branch starts from `claude/content` (fetch it first: `git fetch origin claude/content`), and you merge
  `claude/content` into yours before each batch so you have the others' merged work (cards you can reference, banks you
  shouldn't duplicate).
- **Never touch the game file**, `content_gen.py`, `lines_check.py`, or anyone else's files. If a hook is missing
  (a condition, a placeholder), tell the head writer.
- Commit messages end with the line the lead gave you (`Co-Authored-By: ...`).
- Memory: when you're about two thirds full, tell the head writer and write `plans/handover-writer-<area>.md`.
