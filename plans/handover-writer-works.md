# Handover: Writer 2 (Works and the arrival; command, Survey, Watch and guests)

Written 2026-10-17 by the Writer 2 session, kept current after each batch. A fresh session taking this seat: read this
first, then the "Read first" list below. (Two older seat notes are folded into this one: the first Works writer's and the
first command writer's: `plans/handover-writer-command.md` still has the command writer's inventions list.)

## Role and chain of command

- **One seat, two old areas:** the Works crew, Torres, Calder, Kovac, the intro meetings, newcomers; and the Captain,
  Vance, Holt, Sato, Nandakumar, the senior officers, the day officers, Watch, Survey, guests and visitors.
- **Report only to the head writer** with `send_message` after each batch: the commit, who/what, canon questions,
  inventions to confirm. Never the user. Head writers change often (head writer 3 is `session_01FopKMT2ZKxuWcNDcmF7565`
  as of 05:10); if unsure who it is, ask the lead (`session_01KPJMYjXAPkNUcrQ8VRkhLE`).
- **Branch:** `claude/writer-works`, pushed only there. Merge `origin/claude/content` into it before every batch.
- **Only `content/` files for your people** (and this note). Never the game file, `content_gen.py`, `lines_check.py`,
  or writer-commons's files (Tomas, Pell, Rina, Brennan, galley, store, infirmary aides, night shift, gardeners, helm
  and comms juniors; `banks/all-*`, `overheard/circles|bunk|commons|...`, reactions, themes).
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. No model names anywhere else.

## Read first

`CLAUDE.md`; `content/README.md` (formats, the frozen condition words); `content/voice-bible.md` (tone, tiers, the
checklist, the no-romance read); `content/facts.md` (canon: pronouns in section 4, gated secrets in 10, approved
inventions in 11); `content/briefs.md`; `plans/pillar4-notes.md` (the user's words); the arc files you touch.

## What this seat built (all merged into claude/content unless noted)

| Batch | What |
| --- | --- |
| 1, 1b | The 16 Works crew and Kovac to ~30 own lines (greet by time/warmth, near, invite, accept, decline, missed, birthday, cue, hint, about); Torres's `flag:walk.job2.<step>` and `walk.job3.tea|turnin` bubbles (onboarding wired them in 0.42.19) |
| 2 | Seniors (Kowalczyk, Raman, Ferreira, Oduya, Mensah, Mori) and Watch (Achterberg, Dahl, Garcia, Park, Vasquez, Shah, Chen, Nakamura, Ueda) to ~30 |
| 3 | Day officers (Zielinski, Lindqvist, Farouk, Ibarra, Zamora), Survey (Lemaire, Fonseca, Kim, Yilmaz, Abara, Alvarez, Mbeki), Sato, Nandakumar to ~30 |
| 4 | Calder (116) and Kovac (106): seasons, rep/you, callbacks on arc memories, gifts, cues, visits, notes, bubbles |
| 5 | Vance, Marrow, Holt to ~110 the same way |
| 6 | 322 smalltalk/rumour bubbles for 46 people, at most one in five about work (the user's note: chatter felt all about work). Pushed ada7567; head writer 3 to merge |
| 7 | ~40 named overheard pairs (`who:`/`with:` plus `place:`/`deck:`) appended to `overheard/works|watch|survey|command.lines` (8c958d8) |
| 8 | Short voice cards and ~9 own lines each for the first 16 short-stay visitors (`content/voices/v-*.voice`, `content/lines/v-*.lines`: Jaramillo to Quinlan, arriving days 5-114). Last batch of this session |

## Rules that bit (the head writers' notes)

- **Rest days:** read `rota.offDays` in the game's `ROSTER`; **0 = Monday** (6 = Sunday). Calder's day-off lines use the
  planned Sat-Sun on purpose: leave them. `act:off` is a good rest-day condition too.
- **No-romance read** on every friend/close line, every hint, visit, note and moment: no "just us", no setting a scene for
  two ("Somewhere quiet", "Any window. I'll find you", "You can sit with me"), no "thinking about you", "I noticed (you)",
  "looking at the door", no word that can read as a pet name ("Sweet?"). Hints say a talk is coming ("Have you a minute
  later? I've something to say"), never where.
- **Notes are never signed** (the game adds the name).
- **Lengths:** card 90, bubble/overheard 60, moment 140; a placeholder counts as 9. Draft short.
- **No `habit:`** for people whose roster `habitShifts` has a drop-only entry (Mori, Zielinski, Dahl, Zamora, Chen,
  Ferreira, Fonseca, Vance): use `place:`, `deck:`, `act:`.
- **Gates:** Calder never says "well done" before beat 5, no exclamation marks, Fenn only from beat 3; Kovac's lift is
  "exercise" until beat 2, "Four, please" from beat 4; Torres's father from beat 4; Vance is Gull only from beat 5 (the
  poems are free), his father from beat 3/4; the Admiral is never explained; Marrow's daughter from beat 4, the academy
  post from beat 5; Holt's Rook and the bad day from beat 3, tea with the Envoy from beat 5; Holt's distrust is voiced and
  argued with, never a joke about the Veyli. Keane never says "afraid".
- Callbacks: `told:moment.<arc>.<choice mem>` for each arc reply's `mem:`; `told:fixed.` / `fav.` / `came.` / `bday`
  match by prefix. Gifts: `== gift` with `gift:loved|liked|polite` or a tag.
- Overheard: `? pair:any+any who:<A> with:<B>` and a `place:`/`deck:` when the talk belongs to a room. Aliases: mess,
  commons, lounge, booths, overlook, teacorner, worksbay, chartroom, musicroom; `junior_common_room`.

## What's next

1. Head writer 3's notes on batches 7 and 8 (batch 6 merged in 0.48.23 with the scarf bubble gated on `mem:moment.torres.scarf`).
2. **The other 15 visitors** (`GUESTS` in section 9 arriving from day 116: Tamura, Kalnins, Delacroix, Ferro, Upton,
   Ekwueme, Mercer, Kessler, Ellery, Rocha, Aalto, Gunn, Dunmore, Grimaldi, Abbas, Marsh) need cards and lines the same
   way: a short card (tpl, talk, hi/bye/yes/thanks/wow/sigh, likes, nick) and ~9 lines (greet stranger x2 + acquaintance,
   chat x2, near by habit/place, bye, smalltalk x2). Batch 8's files are the model. No pronouns (none in facts.md).
   Several share a role and bio (cartographers, retired captains, relief doctors): give each a different voice.
3. Newcomer reply sets: on hold until social's guide script format (Part 8b).
4. Goodbyes and letters for my people (later batches).

## How to test

```
S=<your scratchpad>; cp starship-cadet.html $S/game.html
python3 content_gen.py $S/game.html && python3 lines_check.py $S/game.html
```
It must say PASS (0 errors). Warnings in other writers' files aren't yours. A helper that prints a person's roster entry
(rest days with 0 = Monday, habits, habitShifts), card notes and current lines saves a lot of reading: parse `const ROSTER
= [` ... `];` from the game file as JSON after stripping the trailing comma.

## Open questions

None for the user.
