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

## Writer 4 (session_01AB5f3VLMh8huiLWbEnqa8U): batches 1-12, reviewed by head writer 3

Head writer 2 went inactive before Writer 4 started. **Head writer 3 is session_01FopKMT2ZKxuWcNDcmF7565**: send it
each batch hash. Batches 1-16 merged (to 0.48.34); Calder (872395c) and Brennan (020b55a) pushed, awaiting review. **Writer 4 stood down
after batch 18 (2026-10-17, ~65% memory).** A fresh writer starts from this note.

| Batch | What | Files |
| --- | --- | --- |
| 1 | one-sided booth calls home (101, speaker A only, `place:booths`) | `overheard/booths.lines` (head writer added `!who:torres-zeke\|vance\|calder\|marrow\|holt` to the generic ones: keep it on new ones) |
| 2 | everyday non-work chatter for the Commons 19 (~15 smalltalk + 2 rumour each) | their own `lines/` |
| 3 | Deck 4 juniors: 154 bubbles, 36 convos | `banks/juniors.lines` (`@bank rank:junior`), `overheard/deck4.lines` |
| 4 | Tiles talk (`tiles.start/dock/miss/win/lose`), 30 Deck 3 named pairs | `banks/tiles.lines`, own files (Rina, Pell, Tomas + 7), `overheard/pairs.lines` |
| 5 | 16 visitors Tamura to Marsh: card + 12 lines | `voices/v-*.voice`, `lines/v-*.lines` |
| 6 | Zeke Torres's ordinary weeks (50) + 10 intro callbacks | `lines/torres-zeke.lines` |
| 7, 11, 12 | goodbyes (`leaving:you`), packing (`feel` `leaving:soon`), letters, for the Commons 19, 25 Works/Watch, 20 Survey/officers/seniors | own files |
| 8 | the mess at dinner: 40 convos, 20 crowd bubbles | `overheard/dinner.lines`, `banks/mess.lines` |
| 9, 10 | reactions: Commons repairs, favours, gifts, harvest, late meals; Works repairs; Brennan's and Pell's `cue:repair.you` | `reactions/repairs-commons.lines`, `reactions/repairs-works.lines` + appends |
| 13-18 | story-crew everyday passes (~50 lines + 8 callbacks each, `!week1:true`, arc gates kept): Holt, Vance, Marrow, Kovac, Calder, Brennan | their own `lines/` under "// Writer 4, batch N" |

Gotchas found: "love you" and "thinking about you" are on the romance list even in family calls or as jokes; no poems,
dedications or "thought of you" to the player (letters say "thought of the Wren"); "apple" is banned (brand); words
like "Gardening", "Retirement", "Power" at a sentence start warn as names; `trait:` can't reach "dry humour" (space);
goodbye lines also go into the engine's "Sorry I missed you at the shuttle" Mail; `place:crew_store`,
`place:infirmary`, `place:gym`, `place:laundry`, `place:port_washroom|starboard_washroom`, `place:bunk_1..8` match
room names; head writer 3's style note: don't end many lines on "Lovely".
Head writer 3's later edits, for the next writer: a line that pre-empts a beat's reveal waits for that beat
(Marrow's daughter's short letters now need beat:marrow.4); a callback must not assume when its memory happened
("on your first week" dropped); mentor warmth points outward ("The bay's better for it"), never private ("I say it to
myself"); keep age and year counts vague unless canon ("thirty years").

Still open after Writer 4: done by Writer 5 (below), except the dry-humour Tiles variant (waits on `_` in `trait:`).

## Writer 5 (session_01HW7UxnuNvRXoEjn8tK4sQq): batches 1-7, reviewed by head writer 3

Reports to **head writer 3** (session_01FopKMT2ZKxuWcNDcmF7565). All merged or being merged by head writer 3 (to
0.48.41). Last head on `claude/writer-commons`: 4721c26 + this note. After batch 9 (2026-10-17 ~08:25) the planned
list is done. Onboarding seat 1 (session_01KaHzfqSqF8B4bkNFrH1tsx) is inactive: its successor wires batch 9 from
`plans/handover-onboarding.md` and the key list above.

| Batch | What | Files | Hash |
| --- | --- | --- | --- |
| 1-3 | everyday passes, ~55 lines + 8-9 callbacks each, `!week1:true`, arc gates kept | `lines/tomas`, `pell`, `rina` | 3b96127, 0282f69, e1100b1 (+707f1f1) |
| 4-5 | goodbyes (`leaving:you`), packing (`feel leaving:soon`), letters for all ten story crew | the ten story crew's `lines/` | 91ded9b, 41424a7, 838136b, acf14ef; six in e81ea03 |
| 6 | seasons and traditions gaps for the ten (exact trad ids) + `trad:today` | the ten | cd488f8, 78d55a4, 7335bee, be0bd77 |
| 7 | 39 overheard conversations, off duty in work places | `overheard/deck2`, `deck5`, `deck6.lines` | 4721c26 |
| 8 | 17 crew-to-crew goodbyes for rotation days (A is `leaving:soon`; pair:friend/best/mentor/couple + 8 named leavers) | `overheard/goodbyes.lines` | 4a3879d |
| 10 | missing a friend who moved on (`bond:missed`, `{missed}`), for social B2 | `banks/missed.lines` | 177d478 |
| 9 | week 1 for onboarding's hook: `beat.<beatId>.<n>` bubbles (tomas d1-wash, d5-invite, d6-sowing; brennan d1-dinner; eklund-leila d2-booths; ishikawa-orla d3-store; torres-zeke d3-pick; pell d4-quiz), Mail `mail.d4-mail` (Torres), `mail.d7-calder` + `mail.settled` (Calder), `mail.d5-mug` (Halloran) as one line "Subject \| body", unsigned; `meetings/introHealth.meet` (Rina, Tue 14:00) | those files' `== week1` | b4a86bf |

Head writer 3's edits and rulings this seat: story crew never leave, so their goodbyes only play if that ever changes
(kept anyway, harmless); **the scarf exists only after Torres's beat 1**: any scarf line needs `mem:moment.torres.scarf`;
`trad:observatory` never fired (the id is `observatory-night`; head writer fixed 11 lines; `came.observatory` is fine
as a prefix); Tomas's jam invite trimmed to 90; on a `tomas.lines` merge conflict, keep claude/content's copy (but check
it still holds your unmerged sections: `git checkout --theirs` once wiped my batch 4 Tomas lines); week 1 (0.48.47):
hot water runs out at ten **at night** (a dawn line can't say it), and the player is Works, not engines (Pell's quiz
line now "We need a sensible one").

Tradition ids and times (the game's TRADITIONS): running Mon 19:15, quiz Thu 20:00, works-tea Fri 18:45, jam Fri
19:45, film Sat 20:00, observatory-night Sat 21:15, market = the Sunday swap meet 10:30, harvest = harvest morning
(every other Saturday 09:30), hull-lights every 28 days 21:00, founding day 100, quiet-watch day 300 21:30; seasons
sowing, greening, harvest, lanterns. Rest days (rota.offDays, 0 = Mon): Tomas Fri-Sat, Pell Tue-Wed, Rina Sun-Mon,
Brennan Fri-Sat, Torres Sat-Sun, Calder Mon-Tue, Vance Tue-Wed, Marrow Mon-Tue, Holt Thu-Fri, Kovac Tue-Wed.
Room names for `place:` (lowercase, `_` for spaces): senior_corridor, observatory, chartroom, watch_office,
teacorner, worksbay, main_storage, shuttle_bay, cart_bay, machine_shop, overlook, engine_watch_room.
Habit: run a PASS-gated check script before every commit (an edit after the last check once pushed a 92-char line).

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

- Batch 10 (177d478): 15 "missing them" lines in `banks/missed.lines` (`bond:missed`, `{missed}`, name only, no
  pronouns). They PASS only with dialogue 0.43.27's lines_check/content_gen; head writer 3 merges once claude/content
  has them.
- **Stood down** 2026-10-17 ~08:20 (all batches merged to 0.48.47). Head writer 3 messages this session when
  DE2's `bond:missed`/`{missed}` lands or the newcomer format exists. Candidates: newcomer lines (wait on onboarding's wave 4), more overheard
  for other quiet places (the cart bay, machine shop, Deck 1 observation room), about/invite for the 19.
- Theme fill-in `{since}` still not live (lines using it are skipped).
- Favour jobs `pellPractice`, `brennanSage` depend on others.
- Dry-humour Tiles variant waits on `_` in `trait:`.

## How to test

```
S=<scratchpad>; cp starship-cadet.html $S/game.html
python3 content_gen.py $S/game.html && python3 content_gen.py $S/game.html --check && python3 lines_check.py $S/game.html   # must say PASS
```
