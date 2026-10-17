# Writing for the Wren: the writers' guide

Everything the crew say lives here, in plain text files. You never touch the game file: the head writer runs
`content_gen.py`, which bakes these files into the game, and `lines_check.py`, which checks them. **Run
`python3 lines_check.py` before every push.** It must say PASS.

Read this with the voice bible and `content/facts.md` (the head writer's), and the voice card of whoever you're writing.

## The folders

| Folder | What goes in it | One file per |
| --- | --- | --- |
| `voices/<crewId>.voice` | voice cards: how someone talks | person |
| `templates/<name>.voice` and `.lines` | the ten voice templates generated crew start from (`warm`, `dry`, `shy`, ...) | template |
| `lines/<crewId>.lines` | a person's own lines | person |
| `banks/<name>.lines` | shared lines anyone can say (by department, rank, trait, or everyone) | bank |
| `overheard/<topic>.lines` | two or three crew talking as you pass | topic |
| `reactions/<cue>.lines` | lines about something that really happened (a repair, a tradition, the storm) | kind of happening |
| `meetings/<id>.meet` | meeting scripts with replies to choose | meeting |
| `traditions/<id>.trad` | a tradition's data and words: fields in the traditions engineer's grammar (`plans/trad-format.md`), texts in `== mail`, `== ask`, `== here`, `== thanks`, `== chatter` sections | tradition |
| `themes/`, `arcs/`, `gifts.list` | coming in wave 2 with social engineer B | |

Crew ids are the roster's (`tomas`, `pell`, `rina`, `torres-zeke`, `calder`, ...): see `plans/crew-roster.html`.
`banks/old.lines` holds the lines the game had before the kit. Leave it alone; it's kept exactly as it was.

## A .lines file

```
@crew torres-zeke
// a comment: anything after // at the start of a line is ignored

== greet
? tier=stranger
- {hi}. You'll be the new hand.
? tier>=acquaintance time:morning
- {hi}, {nick}. Coil three's sulking. Don't take it personally.   #funny
- Morning! Board's light today. Don't tell it I said so.

== feel
? mood:low
- Long one. Coil three sulked all shift.
```

- **The first line** says whose lines these are:
  - `@crew <id>`: this person's own lines.
  - `@bank all`, `@bank dept:works`, `@bank rank:junior`, `@bank trait:shy`: shared lines; the conditions after
    `@bank` apply to every line in the file.
  - `@template <name>`: lines for a voice template.
  - `@reactions <cue>`: reactions to one kind of happening (the lines go in the `cue` kind).
  - `@overheard <topic>`: conversations (below).
- **`== kind`** starts the lines of one kind (the list is below).
- **`? conditions`** sets when the lines under it can be said, until the next `?` or `==`. A bare `?` clears them.
  All the conditions on a line must hold.
- **`- text`** is one line. End it with a tone tag if it isn't light: `#funny`, `#warm`, `#serious`.

### Which line gets said

When someone talks, the game gathers every line of that kind they *could* say: their own, their template's, then the
shared banks. It keeps the ones whose conditions all hold, and the **most specific wins**: a person's own line beats a
template's, which beats a shared one, and a line with more conditions beats one with fewer. Lines said recently lose
out, so people don't repeat themselves. Within the same hour a person says the same line if you tap them again.

So: write plenty of plain lines with few conditions (they're the everyday ones), and a few special ones with sharp
conditions (they jump the queue when their moment comes).

## Line kinds

`greet` (hello, by how well they know you), `bye`, `chat` (after Chat), `near` (about where they are or what they're
doing), `feel` (how they feel), `life` (a detail of their life), `joy` (the light thing they love), `callback` (a
memory of something you did), `cue` (a reaction to something that happened), `invite`, `accept`, `decline`, `visit`
(at your bunk), `note` (left on your bunk), `gift` (thanks for a gift), `about` (about a crewmate they're close to),
`rep` (your standing with their department), `knownFor`, `week1` (your first week), `smalltalk` (chatter between crew,
a bubble), `rumour` (how they open with news), `hint` (a moment is ready: "Got a minute? Properly, I mean."),
`missed` (you missed an appointment), `birthday`, `story.<arc>` (an arc beat), `goodbye` (someone leaving the Wren),
`letter` (Mail from crew who've moved on), `newcomer` (the newcomer you guide asking you things), `host` (guests at
your cabin, later).

## Conditions (the frozen vocabulary)

These are the only condition words. `lines_check.py` rejects anything else. Put `!` in front of any of them for
"not" (`!flag:met.calder`). Where a value can be one of several, separate them with `|` (`act:breakfast|dinner`).

**About you and them** (the social side):

| Condition | Holds when | Examples |
| --- | --- | --- |
| `tier=`, `tier>=`, `tier<=`, `tier>`, `tier<` | how well they know you: `stranger`, `acquaintance`, `colleague`, `friend`, `close` (or 0-4) | `tier>=friend` |
| `mem:<what>` | they remember you doing it (starts-with match) | `mem:fav.lamp`, `mem:came.quiz`, `mem:intro.dinner` |
| `told:<what>` | they remember it and haven't mentioned it yet; said once, then marked told | `told:fixed.oven` |
| `warmth:` | `warm` (you've been around lately) or `cold` (not for a while) | `warmth:cold` |
| `aff:` | how they get on with the other crew member in the scene: `rival`, `neutral`, `friend`; or with a named one: `aff:<crewId>:<band>` | `aff:rival`, `aff:saruth:rival` |
| `bond:` | they have a crewmate who is their `best`, `rival`, `mentor`, `mentee`, `drifting`, `couple`, `friend` | `bond:best` |
| `mood:` | `low`, `ok`, `high` | `mood:low` |
| `beat:<arc>.<n>` | at least n beats of that story arc have been told | `beat:tomas.3` |
| `beat=<arc>.<n>` | exactly n beats told (a line that belongs between two beats) | `beat=tomas.2` |
| `news:<id>` | they know that piece of news | `news:storm` |
| `rep:` | your standing with their department: `new`, `known`, `well`, `theirs` | `rep:well` |
| `ship.work:`, `ship.kindness:`, `ship.spirit:` | the ship's view of you: `low`, `ok`, `high` | `ship.kindness:high` |
| `you:<tag>` | you're known for it | `you:reliable` |
| `cue:<what>` | it happened in the last day or two (`.you` on the end: and you did it) | `cue:repair.oven`, `cue:repair.oven.you` |
| `flag:<key>` | a story flag is set | `flag:met.calder`, `flag:mug` |
| `week1:` | `true` during your first week (from the arrival evening until the week is done) | `week1:true` |
| `leaving:` | `soon`: the speaker is transferring off within 10 days; `you`: this is a goodbye | `leaving:soon` |
| `newhere` | the speaker arrived within the last 7 days (a bare word, no value) | `newhere` |
| `moved:<id>` | that crew member has left the Wren | `moved:okoro` |
| `guide:` | `true` while you're guiding a newcomer | `guide:true` |

**About the moment** (the dialogue engine):

| Condition | Holds when | Values |
| --- | --- | --- |
| `time:` | the time of day | `morning` (6-12), `afternoon` (12-17), `evening` (17-22), `night` (22-6) |
| `weekday:` | the day | `mon` `tue` `wed` `thu` `fri` `sat` `sun` |
| `season:` | the ship's season | `sowing` `greening` `harvest` `lanterns` |
| `place:` | where they are: a room's name or a place type (`calm`: somewhere people sit and talk) | `place:mess`, `place:calm` |
| `deck:` | the deck | `deck:3` |
| `event:<id>[.<phase>]` | a ship-wide event is on | `event:ionStorm`, `event:ionStorm.onset` |
| `trad:` | a tradition (`today`: any tradition today) | `trad:quiz`, `trad:today` |
| `dept:` `rank:` `trait:` `habit:` | the speaker's department, rank, trait or habit | `dept:galley`, `rank:junior`, `trait:shy`, `habit:gardener` |
| `act:` | what they're doing | `work`, `breakfast`, `dinner`, `meal` (either), `gym`, `wash`, `leisure`, `off`, `free` (either) |
| `birthday:` | `me` (the speaker's) or `you` (yours) | `birthday:me` |
| `pair:` `topic:` | overheard only (below) | |

**Not conditions:** `w:2` makes a line twice as likely as its neighbours; `odds:0.3` lets it come up only 30% of
the hours it could.

## Placeholders and voice tokens

**Placeholders** are filled in by the game. If one can't be filled (nobody is their best friend yet), the line is
skipped, so it's safe to use them.

`{me}` your name, `{name}` the speaker's name, `{first}` their first name, `{nick}` what they call you,
`{friend}` `{best}` `{rival}` `{partner}` `{mentor}` `{mentee}` a crewmate with that bond, `{boss}` their chief,
`{other}` the other crew member in the scene, `{thing}` what the line's memory is about (`mem:fav.lamp` gives "the lamp"), `{trad}` the tradition,
`{machine}`, `{room}`, `{deck}`, `{dish}`, `{weekday}`, and from their roster entry `{home}`, `{family}`, `{hobby}`,
`{since}`.

**Voice tokens** come from the speaker's voice card, so one shared line sounds like each person:
`{hi}` `{bye}` `{yes}` `{thanks}` `{wow}` `{sigh}` `{nick}`.

```
- {hi}, {nick}. Busy day?
```

is "Cadet. Busy day?" from Holt and "Oi oi, spanner. Busy day?" from Pell.

## A voice card (.voice)

```
@voice torres-zeke
tpl: earnest
talk: Quick and warm; talks about the drive coils as if they were moody pets.
cares: the drive coils | knitting scarves | being ready for more responsibility
jokes: coil three sulks | he knits a scarf for anyone who stands still long enough
hi: Hey | Hello there | Oh, hi
bye: Mind the coils | Off you go, then
yes: Course | Happy to
thanks: Cheers | You're a star
wow: Look at that
sigh: Well, there it is
nick: - | - | {me} | spanner | spanner
needs: listen
openness: open
loves: knitting | music
likes: tea | engines
invites: observatory
joy: knitting scarves
thread: ready
keepsake: a half-knitted scarf in Works orange
avoid: his father (until his arc opens)
```

- Lists are separated by ` | `.
- `nick` has five values, one per tier (stranger, acquaintance, colleague, friend, close); `-` means "use your name".
- Voice tokens should work anywhere in a day: `hi` is "Hey", not "Morning".
- `talk`, `cares`, `jokes` and `avoid` are for writers; the game doesn't show them. `needs`, `openness`, `loves`,
  `likes`, `invites`, `joy`, `thread` and `keepsake` are read by the social side (see the social plan, Part 9).

## Overheard conversations

```
@overheard board
== overheard
? pair:works+works
A: Board's light today.
B: Then it'll be heavy tomorrow. It always is.

? pair:friend
A: You coming to quiz night?
B: Only if you stop shouting the answers.   #funny
A: No promises.
```

- `A:`, `B:` (and `C:`) are the speakers; a blank line or `---` ends a conversation. Two to four lines.
- `pair:x+y`: speaker A is x and B is y, each a department, a rank or `any` (`pair:junior+chief`, `pair:galley+any`);
  or one word for how they relate: `same` (department), `bunk` (share a bunk room), `friend`, `rival`, `senior`
  (A outranks B).
- The conditions are read for speaker A; `{other}` is the other one. The topic is the file's name.

## Reactions

```
@reactions repair.lamp
? cue:repair.lamp.you tier>=acquaintance
- That lamp's been blinking since Tuesday. {thanks}!   #warm
?
- Someone fixed the lamp at last.
```

## Traditions (.trad)

The fields (`when:`, `where:`, `who:`, `ties:`, ...) follow the traditions engineer's grammar in `plans/trad-format.md`;
content_gen.py checks them with `plans/trad_parse.py`. The words go in sections, as `- text   #tone` lines:
`== mail`, `== ask`, `== here`, `== thanks`, `== chatter`. lines_check checks those texts like any other line.

## Meetings (.meet)

```
@meeting calderFirstDay
title: Monday briefing
from: Chief Ines Calder
gist: Calder's first briefing: the board, the tool wall, and who to ask.
== lines
calder: Gather round. Coffee can wait two minutes.   [gesture]
calder > you: {me}, welcome to Works. Questions?
? choice
* Where do I start?   rel:calder+1
  calder: The board. Always the board.   [nod]
* (Say nothing)
  calder: Fine. You'll find me.
calder: Right. Off you go.
```

`who: text [pose]`; `who > to: text` for a line said to someone; `? choice` then `* reply` lines, each with its answer
indented under it. A choice can carry `rel:calder+2,tech2+1`, `job:<id>`, `flavour:listen`, `mem:<key>`, `flag:<key>`,
`favour:<id>`. Cast names are roster ids, `you`, or the meeting's stand-ins (`tech1`, `tech2`).

## The rules lines_check enforces

- **Length:** a chat card line 90 characters at most; a bubble (`smalltalk`, `rumour`, overheard) 60 (90 is an error);
  arc beats, moments, notes and meeting lines 140. A placeholder counts as about 9 characters.
- **No romance or flirting** with anyone, **no swearing** beyond "blast", **no real-world brands or politics**, and
  nothing the game doesn't have (no photos, cameras, phones, weapons).
- **`#serious` lines are earned:** only behind `tier>=friend`, a `beat:`, `mem:moment...` or `leaving:soon`.
- **Names:** only roster crew and guests. A name it doesn't know is a warning.
- **British spelling** (colour, favourite, mum, biscuit).
- **Easy to read:** short words, short sentences. A file under 60 on the reading-ease score is a warning.
- **Habits:** a `habit:` condition in someone's own file must be a habit they have.
- The baked blocks must be up to date (the head writer re-runs `content_gen.py`).

## Tone (from the plan; the voice bible has more)

Generally light, cozy and funny; warmth over wit. Serious moments are earned by friendship and are about ordinary
things (homesickness, a failed exam, a parent getting older). Gentle grief is allowed; nobody dies on screen. No
cruelty played for laughs. Holt's distrust of the Veyli is voiced and argued with, never a slur. Everyone is good at
their job. Never contradict the roster: bio, life lines, habits and birthdays are canon.

## For the engineers

- `python3 content_gen.py [GAME.html] [--check]` bakes; a second run with no changes gives byte-identical output.
  `--check` exits 1 when the game file is out of date.
- Baked shapes (the social plan's Part 9): `VOICE[id] = { tpl, talk, cares, jokes, words, needs, openness, loves,
  likes, invites, joy, thread, keepsake, avoid, lines: { kind: [...] } }`, `VOICE_TEMPLATES[name] = { words, lines }`,
  `LINES[kind] = [{ text, id, tone, w, odds, ...conditions, not: { ... } }]` (a condition's value is a string, `'a|b'`
  for either, an array when all must hold; `tier: [lo, hi]`), `CONVOS = [{ id, topic, pair, ..., lines: [{ who, text }] }]`,
  `MEETINGS_BAKED[id]` in `MEETING_SCRIPTS`' shape, `TRADITIONS[id] = { field: 'text', ..., text: { section: [...] } }`.
- A line's id is a short hash of its file, kind and text: rewording a line gives it a new id.
- Section 22 (`lineFor`, `overheardFor`, `linesOk`, `linesFill`) is the engine; see DEV_NOTES, "Lines (section 22)".
