# Handover: writer-commons (Writer 3, Commons and juniors, Pillar 4)

**Role:** writer for the Commons and juniors. Reports ONLY to **head writer 2** (session_01HNrh3xCtczeZM5NVFrE6pa) with
`send_message` after each batch; never the lead or the user. The head writer reviews, merges into `claude/content`
and sets the next batch. Project lead (for reference only): session_01KPJMYjXAPkNUcrQ8VRkhLE.
Writer 3 was session_01AS3Tzju3TuFbM9XAEYdvPX (took the seat from session_01DfadYjSP8skcVF72f6JxBw, handed over
2026-10-17 at about two thirds memory, after batch 10).

**Writer 4** is session_01AB5f3VLMh8huiLWbEnqa8U (hired ~05:06). Head writer 2 went inactive before Writer 4 started,
so Writer 4 reports batch hashes to the lead until a new head writer is named.

**Branch:** `claude/writer-commons` (push only there). Merge `claude/content` into it before every push. Writers have
no build numbers. Commit messages end with the Co-Authored-By line the lead gave; no model names anywhere else.

## Read first

CLAUDE.md; `content/README.md` (formats, conditions, "Calls home (.call)"); `content/voice-bible.md` (tone, tiers,
the checklist, section 12); `content/facts.md` (4b our pronouns, 4d home contacts, 5 shared quirks, 9-11 canon);
`content/briefs.md`; `content/arcs/outlines.md`.

## What I own (content/ files only; never the game file, content_gen.py, lines_check.py or Writer 2's files)

| Area | Files |
| --- | --- |
| Story crew lines (cards are the head writer's) | `lines/tomas, pell, rina, brennan .lines` (~130-140 each) |
| Story arcs | `arcs/tomas.arc` (5-7), `pell.arc` (5-8), `rina.arc` (5-7), `brennan.arc` (1-5) |
| My 19: cards + own lines | galley (walsh-esme, madsen-ivo, varga-tariq, haddad-tamsin, dlamini-lukas), store (esposito-yara, ishikawa-orla), infirmary (grieve-thea, larsen-hamid), night shift (yoon-elif, janssen-hugo, takahashi-wen, bakshi-sol), garden (cruz-tove, oneill-imani, hart-ravi), helm/comms juniors (strand-erik, santos-zofia, tran-chloe) |
| Shared banks | `overheard/` (incl. my `newlyweds.lines`, `circles.lines`), `reactions/` |
| Themes | `themes/*.arc` (all twelve) |
| Call home | `home/gran.call`, `jo.call`, `sam.call` (`mum.call` is the head writer's model) |

## Done this seat (batches 1-9 MERGED by head writer 2, last 0.48.19; batch 10 pushed, awaiting review)

1. Story four: callbacks (`told:` on moment.<arc>.<word>, came.<trad>, fav.*, gift.*, fixed.<kind>, bday, grubby,
   heard.moment.<friend>; Pell's `told:moment.pell.timed beat:pell.7`), visits, notes.
2. Overheard: newlyweds (Silva/Soto/Jovanovic count up, Lukas counts down) and 30 "circles" convos by `who:`/`with:`.
3. Story four toward 120: seasons, places, act:off rest days, smalltalk, rumour, cues, about, invites.
4. Smalltalk + rumour bubbles for my 19.
5. Callbacks for my 19.
6. rep / knownFor as greet lines (`rep:well`, `rep:theirs`; `you:reliable|kind|chatty`).
7. Call-home contacts Gran, Jo, Sam (6 beats, send, chat each).
8. Gift thanks (`== gift`, `gift:loved|liked|polite` or the loved tag) for the four and my 19.
9. Crew asking after your people (greet lines gated on home flags) for the four and the bunkmates.
10. `banks/everyday.lines` (`@bank all`): 60 non-work smalltalk/rumour bubbles (food, days off, letters, seasons,
    traditions, vents, hot water, Gerald), gated by act:/time:/season:/trad:/place:; lines naming Rina use `!who:rina`.

## Writer 4 (pushed, awaiting review)

1. Batch 1 (38b79e4): `overheard/booths.lines`, 101 one-sided calls home (303 lines). `? place:booths`, speaker A only
   (A-only convos bake and play; no new format needed). Sections: anyone, seasons/ship days, story crew, the circles,
   the Commons people (`who:`).
2. Batch 2 (2a9353d): everyday non-work chatter for the Commons 19 (289 lines, ~15 smalltalk + 2 rumour each),
   appended to each file under "// Writer 4, batch 2".

Gotchas found: "love you" is banned even in family calls in overheard banks (use "love to all", "big hug");
"apple" is banned (brand): use pear; "Geralds" and sentence-start words like "Gardening" warn as names.

## Formats and hooks that bite

- A bank line that names a crew member ("Not against Rina") needs `!who:<id>` so that person never says it.

- Card words no end punctuation. Lengths: card lines 90, bubbles 60, moments/calls 140, choices 90, hints 90.
- `rep:` means "this band or better" (`!rep:known` = new only; `rep:new` warns).
- `you:` matches knownFor() tags exactly and can't hold spaces: only `reliable`, `kind`, `chatty` work until the
  dialogue engineer accepts `_` (asked by the head writer).
- `gift:` (how or tag) only in `== gift`; the game appends " On my birthday, too." itself.
- Notes: the game appends the sender's name, so don't sign them. Visits only happen at tier friend+.
- Callback kind fires only when some memory is untold; only `told:` marks memories told.
- Rest days: read the game ROSTER's `rota.offDays` (0 = Monday), or use `act:off`. Story four: Tomas Fri-Sat, Pell
  Tue-Wed, Rina Sun-Mon, Brennan Fri-Sat.
- `place:` aliases: mess, commons, lounge, booths, overlook, teacorner, worksbay, chartroom, musicroom; garden is
  `place:hydroponics_garden`.
- `.call` files: `? ` conditions last until the next `?`; put a bare `?` before open send choices. `pron: they`.
- Ladder club: keep the lift fear as "exercise" unless gated `beat:kovac.2`.

## No-romance read (the head writer's rules of thumb, from their rewords)

Nobody in or on your bed; no "with me" at night; no "likes you"; no jealousy even as a joke; no dedications you
missed; no "nervous to ask / glad I asked"; no "best part of my day, this"; no looking for you in the stars; no
"hear me breathing". Sam is plainly an old friend. Hints never set a scene for two.

## Loose ends / next

- Batch 10 awaiting notes. After it the seat is handed over: head writer 2 asks the lead to retire it and hire
  fresh when needed. A fresh writer starts from this note.
- Booth overheard: done (batch 1). More could go to the generated crew's families via `{family}` once the roster has it.
- Theme fill-in `{since}` still not live (lines using it are skipped).
- Favour jobs `pellPractice`, `brennanSage` depend on others.
- Candidates: goodbyes and letters for my people, newcomer lines, more about/invite for my 19.

## How to test

```
S=<scratchpad>; cp starship-cadet.html $S/game.html
python3 content_gen.py $S/game.html && python3 lines_check.py $S/game.html   # must say PASS
```
