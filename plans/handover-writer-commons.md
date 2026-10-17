# Handover: writer-commons (seat 14, Pillar 4)

**Role:** Writer for the Commons and juniors. Reports ONLY to the head writer (session_016i7YYgZd6puKxfBSkLggRF) with
`send_message` after each batch, never to the lead or the user. The head writer reviews, merges into `claude/content`,
and sets the next batch. Retiring session: session_01DfadYjSP8skcVF72f6JxBw (handed over at about 65-70% memory,
2026-10-17).

**Branch:** `claude/writer-commons` (push only there). Writers have no build numbers; work reaches the game through the
head writer's 0.48.x builds. Last commit at handover: see `git log -1 origin/claude/writer-commons` (batch 6b, aae127f,
plus this note).

## Read first

CLAUDE.md; `content/README.md` (formats, the frozen condition words); `content/voice-bible.md` (tone, tiers, the
checklist, section 12's batch notes); `content/facts.md` (canon: section 4b is our pronoun table, section 5 the shared
quirks, sections 9-11 the story so far and approved inventions); `content/briefs.md`; `content/arcs/outlines.md`.

## What I own (content/ files only; never the game file, content_gen.py or lines_check.py)

| Area | Files |
| --- | --- |
| Story crew lines (cards are the head writer's) | `lines/tomas, pell, rina, brennan .lines` (about 58-62 each) |
| Story arcs | `arcs/tomas.arc` (beats 5-7), `pell.arc` (5-8), `rina.arc` (5-7), `brennan.arc` (1-5) |
| My 19 people: cards + own lines | `voices/` and `lines/` for walsh-esme, madsen-ivo, varga-tariq, haddad-tamsin, dlamini-lukas (galley); esposito-yara, ishikawa-orla (store); grieve-thea, larsen-hamid (infirmary); yoon-elif, janssen-hugo, takahashi-wen, bakshi-sol (night shift); cruz-tove, oneill-imani, hart-ravi (garden); strand-erik, santos-zofia, tran-chloe (helm and comms juniors). Bunkmates Lukas, Zofia, Chloe about 55-60 lines; the other 16 about 29-30 |
| Shared banks | `overheard/` (mess, bunk, home, quirks, night, commons, bunkpairs, garden, galley: 72 conversations, plus other writers' files), `reactions/` (storm, repairs, traditions, guests, favours, gifts, latemeal) |
| Struggle themes | `themes/*.arc`, all twelve (3 beats each) |
| facts.md | section 4b only (my pronoun rows) |

Writer-works and writer-command have handed over; at handover I was the only writer on.

## Shared formats and hooks (the things that bite)

- **Card words carry no end punctuation** (`hi: Hi`, not `Hi!`): the line supplies it.
- **Lengths:** card lines 90, bubbles (overheard, smalltalk, rumour) 60, moment lines 140, hints 90.
- **place:** matches a place type or a one-word room name only (no spaces in a condition value): `place:infirmary`,
  `place:galley`, `place:calm`. Mess hall / junior common room aliases were asked of the dialogue engineer.
- **week1 lines:** `week1:true weekday:X`; avoid Sunday (day 0 and day 7 are both Sundays). Day 0 only:
  `week1:true weekday:sun time:evening !flag:week1.d2`.
- **Cues** (social's keys): `repair.<machine kind>` (MACHINE_KINDS), `tradition.<id>` (SHIP_TRADITIONS),
  `event.ionStorm.<phase>`, `event.diplomatic.<phase>`, `favour.lamp|fetch|job` (always `.you`), `gift.<tag>`,
  `harvest`, `lateMeal`. Dialogue 0.43.7 adds `@me` (about the speaker: `cue:gift.you@me`) and `@dept`.
  A file `@reactions <prefix>` adds that prefix as a base cue to every line.
- **Theme fill-ins (agreed shapes):** `{home}` a place ("Lisk", used as "on {home}"), `{family}` with the possessive
  ("my gran", then "they"), `{hobby}` an -ing activity, `{since}` a duration. Every beat using one lists it in `needs:`.
  The roster doesn't have these fields yet (the lead is finding an owner), so those beats don't play yet.
- **Arc gates I used:** Tomas exam from `beat:tomas.5`; Pell's mum's shop from tier friend, the practical from
  `beat:pell.5`; Rina's gran from `beat:rina.1`, the exam drawer from `beat:rina.5`, "a hard year" from `beat:rina.7`;
  Brennan's blue sage from `beat:brennan.2`, Port Halloran and the fire from `beat:brennan.3`. Brennan is off Fri and
  Sat (Lukas covers).
- **No-romance read** (the lead's standing rule): every friend- or close-tier line, every moment. Watch for "our day",
  "a bit of me with you", "I was thinking about you", "it's yours" (songs), "I'd be lost without them", poems. Never
  tease about bodies ("you're thin").

## How to test

`content_gen.py` refuses to bake into the real game file for writers (the head writer bakes), so bake into a scratch
copy:

```
S=<your scratchpad>; cp starship-cadet.html $S/game.html
python3 content_gen.py $S/game.html && python3 lines_check.py $S/game.html
```

If the head writer's branch is behind the dialogue engineer's (new conditions like `@me`), check against
`claude/dialogue`'s tools: copy its `content_gen.py`, `lines_check.py` and `starship-cadet.html` into a scratch folder
with `plans/trad_parse.py` and a `content` symlink to ours, then run them there. Must say PASS (0 errors).

**Known lines_check bug (reported):** a `habit:` condition in a person's own file crashes the habit check
(`KeyError: 'add'`) if their roster entry has a `habitShifts` item with only `drop`. Avoid `habit:` for those people
(Hamid Larsen hit it) until the dialogue engineer fixes it.

## Loose ends

1. **Newlyweds' day counts** in overheard: needs a speaker-identity condition (asked for `who:` or a `life:married`
   tag). Until then the counts live in Lukas's own lines.
2. **Pell beat 7 callback:** "if you helped him practise, he says so" can't be done inside an arc; write a
   `mem:moment.pell.timed` callback line in pell.lines later.
3. **Favour jobs** `pellPractice` and `brennanSage` (practical replies in the arcs) need the lead to have them built.
4. **Theme fill-ins** wait on the roster fields (above).
5. `reactions/repairs.lines` and `favours.lines` wait on `simNote('repair')` / `simNote('favour')` being posted
   (the head writer asked the lead).

## Next (as the head writer last set it)

The batches the head writer listed are done: reactions rework (favours by `@me`, gifts, lateMeal), overheard batch 2
and `about` lines, and my 19 to about 30 (bunkmates about 55-60). Report batch 6b and ask the head writer for the next
batch. Likely candidates: callbacks (`mem:`/`told:`), visits and notes at your bunk, `rep`, `knownFor`, `rumour` and
`smalltalk` for my people, goodbyes and letters, and the story crew towards about 120 each.

## Open questions for the head writer (none for the user)

- Who owns `{home}`, `{family}`, `{hobby}`, `{since}` now the crew designer has retired.
- A speaker-identity condition for overheard (the newlyweds).
- Whether `lateMeal` means what I guessed (a meal after the window, a kept plate).
