# Handover: Writer for command, Survey, Watch and guests (seat 13)

Written 2026-10-17 by the first writer-command session, at about 55% memory, at the head writer's request. A fresh
session taking over this seat: read this first, then the "Read first" list below.

## Role and chain of command

- **Seat 13, Pillar 4:** the writer for command (the Captain, Vance, the senior officers), Survey, Watch and the guests.
- **Report only to the head writer** (session `session_016i7YYgZd6puKxfBSkLggRF`) with `send_message`, after each
  batch: commit, what's in it, canon questions, inventions to confirm. Never the user, never the lead.
- The head writer sets batches (about 300 lines), reads every batch against the voice bible and the cards, and is the
  only one who merges writers' work into `claude/content`.
- **Branch:** `claude/writer-command`, pushed only there. Merge `origin/claude/content` into it before every batch.
- **Never touch** the game file, `content_gen.py`, `lines_check.py`, or other writers' files.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (the lead's line). Never put
  model names anywhere else.

## Read first

1. `CLAUDE.md`, then `content/briefs.md` (who writes whom, the batch order).
2. `content/README.md` (the file formats, the frozen condition words, the .arc grammar).
3. `content/voice-bible.md` (tone, tiers, the checklist in section 11; the no-romance read).
4. `content/facts.md` (canon). Section 4c is mine (pronouns for my area and the guests). Section 11 holds the head
   writer's record of approved inventions, mine included.
5. `content/arcs/outlines.md` (the arcs and social B's shape notes at the top).
6. The roster: `plans/crew-roster.html` or `ROSTER` / `ROSTER_GUESTS` / `GUESTS` in section 9 of the game file
   (bio, life, about, habits, habitShifts, traits, birthdays: all canon).

## What I own (my people)

- **Story crew, lines and arcs only** (cards are the head writer's): Captain Marrow, Commander Vance, Chief Holt.
- **Cards and lines:** Dr. Sato (story crew in the design doc, but the head writer handed her card to me), Dr.
  Nandakumar; the senior officers Kowalczyk, Raman, Ferreira, Oduya, Mensah, Mori; officers Zielinski, Lindqvist,
  Farouk, Achterberg, Dahl, Ibarra, Zamora; Watch ratings Garcia, Park, Vasquez, Shah, Chen, Nakamura, Ueda; Survey
  assistants Lemaire, Fonseca, Kim, Yilmaz, Abara, Alvarez, Mbeki.
- **Guests:** Envoy Saruth, and the event guests Teshavi, Kesrin, Moleth, Ithra (diplomatic visit), Lindgren (nebula),
  Taavek (Veyli vessel), Quill and Petrie (salvage). The 16 short-stay visitors (`v-...` ids) have no cards; they use
  `banks/guests.lines`.
- **Banks and overheard:** `banks/guests.lines`; overheard `command`, `watch`, `survey`.
- **Not mine:** Janssen, Takahashi, Yoon, Bakshi, Strand, Santos, Tran (writer-commons); the Works crew, Torres,
  Calder, Kovac (writer-works); Tomas, Pell, Rina, Brennan (writer-commons).

## What I wrote (all merged by the head writer, up to build 0.48.6)

| Batch | Files | What |
| --- | --- | --- |
| 0 | `content/voices/*.voice` (26) | cards for my non-story people, from the roster; notes in `//` lines above the fields |
| 1 | `content/lines/marrow.lines`, `vance.lines`, `holt.lines` | 12 lines each for the Voices sampler (the user approved all ten voices) |
| — | `voices/sato.voice`, `lindqvist-isak.voice`, `farouk-olu.voice`; `facts.md` 4c | three more cards; pronouns |
| 2 | `content/lines/<id>.lines` (29) | about 10 everyday lines each (greet by tier, feel, near, life, joy) |
| 3a | marrow, vance, holt `.lines` | grown to 61 lines each (greet by time, bye, chat, invite, accept, decline, missed, birthday, hint, near, smalltalk, rumour) |
| 3b | `voices/` + `lines/` for Saruth and the 8 event guests; `banks/guests.lines` | guest cards and lines |
| 3c | `content/overheard/command.lines`, `watch.lines`, `survey.lines` (15 conversations) | **held** in `content/held/` by the lead until the dialogue engineer's 0.43.5 passes review; nothing lost |
| arcs | `content/arcs/marrow.arc`, `vance.arc`, `holt.arc` | beats 1-5 each, from the outlines |

Head writer's change after merge: Holt's "Mensah asked if I'd been stood up" became "Mensah asked if I was lost. I am
never lost. Hm." ("stood up" reads as dating language). Watch for words like that.

## My inventions (all approved; in facts.md section 11)

- Pronouns (4c): he: Raman, Oduya, Mensah, Achterberg, Ibarra, Nakamura, Lemaire, Fonseca, Kim, Alvarez, Mbeki,
  Lindqvist. she: Mori, Ferreira, Kowalczyk, Zielinski, Dahl, Garcia, Park, Vasquez, Chen, Ueda, Yilmaz, Abara,
  Lindgren, Quill. they: Zamora, Shah, Farouk, Petrie, and the Veyli guests (like Saruth).
- Threads (themes) on every card; paired rivalries: Lemaire and Yilmaz (the worst breakfast joke), Nakamura and
  Garcia (herb planters).
- Vance: "Regulation two, section four" (no saluting, a nod), regulation six (shoes off in cabins), nine (rest),
  eleven section two (port leave); you're ninth on the good-records list; the six-person academy boat; breakfast at
  06:05; Tomas fourth on the treadmill board; his father's messages "waiting since Sowing"; 22 years since the academy;
  Gull's "Oh treadmill, thou belt of endless toil" (eleven beats in line two).
- Marrow: Captain Varga started the portrait gallery; her little book of juniors' answers (you're on page forty).
- Holt: Mensah's airlock joke ("too many seals"); the knot "under, over, through, and back"; he counts the Envoy's knots.
- Ferreira: the Veyli have many words for "quiet". Vasquez: new last Sowing, her mum feeds her fish. Ueda: a paper
  letter from Valo takes six weeks. Sato's tea: smoked leaf, dried kelp, a pinch of pepper. Nandakumar's chillies:
  the same seeds her mother grew.
- Saruth: "Do not bow. Most of you do it wrong."; why humans knock twice; Holt's plain distrust is "a kind of honesty
  I respect"; the cord tied loose means "you are expected".
- The salvage: nobody died; the derelict's crew were all rescued. Quill cooked for 22; Petrie navigated for 11 years.
  (Head writer approved; the lead is confirming with the events engineer. If the events engineer says otherwise,
  revisit `quill.voice`, `quill.lines`, `petrie.lines`.)

## Open hooks (waiting on others)

1. **`favour:holt.invite`** (Holt arc beat 4): the practical reply carries it, but the scene plays the favour in place
   (Saruth hands you the invitation in front of Holt; he goes in; a Mail afterwards). Social B may want it split into
   a favour that starts in the scene and completes later; if so, beat 4 needs re-cutting.
2. **Ready-room mem keys:** `MEETING_SCRIPTS.readyRoomFirst`'s three replies carry no `mem:` keys, so Marrow beat 1
   says "you gave me an answer" without quoting it. The head writer is asking social A. If keys arrive (for example
   `mem:readyroom.lights`, `.filters`, `.month`), add one line per answer to beat 1 or as `callback` lines.
3. **Visitors without cards:** the 16 `v-...` guests share `banks/guests.lines`. Ask the head writer whether they want
   cards (they're short stays with generic bios).
4. **Sato's thread** is the theme `notgood` (her tier-4 secret). If the head writer outlines an `arc:sato`, switch the
   card's `thread:` and write `content/arcs/sato.arc`.
5. **Invites vocabulary:** I moved `music` to `jam` and `dinner` to quiz, swap or tasting; the head writer said dinner
   and music may come back once social B confirms the list.
6. **lines_check:** the `habitShifts` KeyError (a shift with only "drop") was reported to the dialogue engineer. Until
   it's fixed, don't put `habit:` lines in the files of people with drop-only shifts: Mori, Zielinski, Dahl, Zamora,
   Chen, Ferreira, Fonseca, Vance (I used deck:/time:/act: instead). The known-words list (Valo, Coriel, Gerald,
   Admiral, Gull, Rook...) was also passed on; those warnings are harmless.

## How to test

- `python3 lines_check.py` must say PASS. The game file's baked blocks go stale as soon as content changes (and writers
  never re-bake the real file), so check against a scratch copy:
  ```
  SP=<your scratchpad>; cp starship-cadet.html $SP/game.html
  python3 content_gen.py $SP/game.html && python3 lines_check.py $SP/game.html
  ```
- Errors in other writers' files that arrive through `claude/content` aren't yours; mention them, don't fix them.
- Name warnings ("isn't a crew member") for canon places and words are fine.

## A guide for my successor (what worked)

- **Start from the roster every time.** Bio, life, about (by tier), habits and habitShifts: they're canon, and they
  hand you the jokes. Use the shared quirks in facts.md section 5 lightly (one mention per person, not every line).
- **Stranger lines teach:** name, department, where to find them, one useful thing.
- **Ratio:** about a third `#funny`, one in ten `#warm`, no `#serious` in everyday banks (seriousness lives in moments).
- **Lengths bite:** card 90, bubble 60, moment 140, hint 90, and `learn:` counts as a moment line (140). A placeholder
  counts as 9. Draft short.
- **habit:** conditions only for habits the person has (roster `habits` plus habitShifts `add`).
- **Gated canon:** check facts.md section 10 before mentioning arc secrets (Marrow's daughter and retiring, Vance's
  messages and that he's Gull, Holt's bad day and Rook).
- **Holt and the Veyli:** his distrust is his, about one day; never a word against the Veyli as a people; others push
  back. Saruth is formal, no contractions, and the joke arrives a sentence late.
- **The no-romance read:** no dating language at all, even as a joke ("stood up", "date", "crush"...).
- **Voice tokens** (`{hi}`, `{nick}`...) read from the speaker's card; check they work at the start of a line for
  every card in a bank.

## What's next (the briefs' order)

Callbacks (`mem:` / `told:`), cues and reactions for my people, visits, notes, gifts, `about`, `rep`, `knownFor`;
the remaining people to about 30 own lines each (they have about 10); goodbyes and letters later. Wait for the head
writer's next brief.
