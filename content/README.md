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
| `traditions/<id>.trad` | a tradition's data and words, in the traditions engineer's format (`plans/trad-format.md`) | tradition |
| `arcs/<arcId>.arc` | a story crew member's arc: their moments, beat by beat (from the head writer's outlines) | arc |
| `themes/<theme>.arc` | a struggle theme for generated crew, three beats with roster fill-ins | theme |
| `home/<contact>.call` | calls home: your people back home, their arc, what you can tell them, everyday calls | contact |
| `gifts.list` | coming with social engineer A | |

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
| `bond:` | they have a crewmate who is their `best`, `friends`, `rivals`, `mentor`, `mentee`, `drifting`, `couple` (`friend`, `rival`, `partner` work too) | `bond:best` |
| `mood:` | `low`, `ok`, `high` | `mood:low` |
| `beat:<arc>.<n>` | at least n beats of that story arc have been told | `beat:tomas.3` |
| `beat=<arc>.<n>` | exactly n beats told (a line that belongs between two beats) | `beat=tomas.2` |
| `news:<id>` | they know that piece of news | `news:storm` |
| `rep:` | your standing with their department is at least this: `new` < `known` < `well` < `theirs` (`!rep:well`: below well) | `rep:well` |
| `ship.work:`, `ship.kindness:`, `ship.spirit:` | the ship's view of you is at least this: `low` < `ok` < `high` | `ship.kindness:high` |
| `you:<tag>` | you're known for it (`_` for a space): `reliable`, `kind`, `chatty`, `quiz_regular`, `gym_rat`, `always_at_the_garden`, `the_one_who_fixes_ovens`, `good_with_newcomers`, `night_owl` | `you:night_owl` |
| `cue:<what>` | it happened in the last day or two (`.you` on the end: and you did it; `@me`: and it was about the speaker, e.g. their gift or favour; `@dept`: a repair in the speaker's department) | `cue:repair.oven`, `cue:repair.oven.you`, `cue:gift.you@me`, `cue:repair.you@dept` |
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
| `place:` | where they are: a room's name with `_` for spaces (`place:junior_common_room`), a short alias (`mess`, `commons`, `lounge`, `booths`, `overlook`, `teacorner`, `worksbay`, `chartroom`, `musicroom`), or a place type (`calm`: somewhere people sit and talk) | `place:mess`, `place:calm` |
| `deck:` | the deck where it happens (where you are) | `deck:3` |
| `event:<id>[.<phase>]` | a ship-wide event is on | `event:ionStorm`, `event:ionStorm.onset` |
| `trad:` | a tradition, by its id in the game (`observatory-night`, not `observatory`; lines_check knows them), or `today`: any tradition today | `trad:quiz`, `trad:today` |
| `dept:` `rank:` `trait:` `habit:` | the speaker's department, rank, trait (one of the roster's, `_` for a space) or habit | `dept:galley`, `rank:junior`, `trait:dry_humour`, `habit:gardener` |
| `act:` | what they're doing | `work`, `breakfast`, `dinner`, `meal` (either), `gym`, `wash`, `leisure`, `off`, `free` (either), `call` (on a call home) |
| `birthday:` | `me` (the speaker's) or `you` (yours) | `birthday:me` |
| `came:` | calls home: you went to a tradition lately (`any`, or its id); the call passes it, and `{trad}` fills from it | `came:any` |
| `friend:` | calls home: you have a friend aboard (`any`); `{friend}` fills from it | `friend:any` |
| `gift:` | thanking for a gift: how it landed (`loved`, `liked`, `polite`) or its tag | `gift:loved`, `gift:sweet` |
| `who:` | the speaker is one of these crew (overheard: speaker A) | `who:torres-zeke\|dahl-mira\|kovac-zainab` |
| `with:` | the other crew member in the scene is one of these (overheard: speaker B) | `with:kovac-zainab` |
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
- **One speaker** (0.43.13): a conversation with only `A:` lines is one person talking with nobody else in it, such as
  someone on a call home (`@overheard booths` with `? place:booths`), one to four lines. It plays when that person has
  no conversation with someone close by; people on a call home only ever say these. No `pair:`, `with:` or `{other}`
  in it, and it needs a `place:` or an `act:` (`act:call` for a call home), so it isn't said just anywhere (lines_check
  says so).
- `pair:x+y`: speaker A is x and B is y, each a department, a rank, a crew id or `any` (`pair:junior+chief`,
  `pair:galley+any`, `pair:dlamini-lukas+silva-bea`); for a group (the knitting circle) use `who:` and `with:` with ids
  separated by `|`;
  or one word for how they relate: `same` (department), `bunk` (share a bunk room), `friend`, `rival`, `senior`
  (A outranks B), `couple` (one of the established crew couples).
- The conditions are read for speaker A; `{other}` is the other one. The topic is the file's name.
- In the game (0.43.12): two crew standing or sitting together near you talk now and then, one bubble every 3 seconds
  or so, A and B taking turns. `act:`, `place:` and `deck:` are where speaker A is and what they're doing. Once you've
  heard a conversation it isn't played again for 7 ship days, and only one `#serious` conversation plays a day, so
  a place you visit often needs plenty of them. Give a conversation that only makes sense somewhere its `place:` (a
  plants talk without `place:garden` can turn up in the mess).

## Reactions

```
@reactions repair.lamp
? cue:repair.lamp.you tier>=acquaintance
- That lamp's been blinking since Tuesday. {thanks}!   #warm
?
- Someone fixed the lamp at last.
```

In the game (0.43.16): soon after something happens (a repair, a gift, a tradition, a storm's phase...), and now and
then while it's still talked about (a day or two), someone near you says one of these as a bubble. Each person reacts
to a kind (the file's `@reactions` kind) once a day at most, and you won't hear the same line again for 7 ship days,
so give each cue several lines and spread them over who'd notice (`dept:`, `who:`).

## Traditions (.trad)

A `.trad` file follows the traditions engineer's format, `plans/trad-format.md` (comments start with `//`). content_gen.py bakes it with their `plans/trad_parse.py`
into `const TRADITIONS = [ ... ]`. The words go in `== mail`, `== ask`, `== here`, `== thanks` and `== chatter`;
besides the usual placeholders they can use `{host}`, `{names}`, `{season}` and `{time}`. lines_check checks the words
(chatter, ask and here 90 characters, mail and thanks 200) but not the fields: content_gen.py does.

## Moments: story arcs and themes (.arc)

A moment is a short scene with someone you've got to know: a few lines, one or two choices, a reply. Story crew have
arcs (`content/arcs/<arcId>.arc`, written from `content/arcs/outlines.md`); generated crew share struggle themes
(`content/themes/<theme>.arc`). Social engineer B's engine decides when a moment is ready and plays it.

```
@arc torres
who: torres-zeke

== beat 1
tone: light
where: calm
when: !week1:true
hint: Don't look. It's a surprise.
mem: scarf
them: Don't look. It's a surprise. It's orange.   [laugh]
them: Every new hand should have something that's theirs.
? choice
* It's lovely. Honestly.   flavour:cheer mem:lovely
  them: Liar. Thank you.
* Who taught you?   flavour:listen
  them: Kovac. She despairs of me.
  + them: Kovac. Sit down, I'll show you the dropped stitch. Every single one.

== beat 3
tone: heartfelt
when: rep:known beat:torres.2
mail: 240 | Thanks | Thanks for tonight. Zeke
them: Was I any good, as your trainer?   [sigh]
? choice
* Ask Calder what she meant.   flavour:practical flag:torres.askCalder
  them: Maybe I will.
```

- **The header:** `@arc <arcId>` and `who: <crewId>` (the arc ids are the outline's: `torres`, `calder`, `tomas`, ...),
  or `@theme <name>` for a theme: `homesick`, `exams`, `family`, `stuck`, `notgood`, `lonely`, `loss`, `talent`,
  `burnout`, `leaving`, `rivalry`, `startover`.
- **`== beat <n>`**, in rising order (a gap is fine while beats are still being written). Its **fields** come first, one per line; only `tone:` is needed:

| Field | What it says |
| --- | --- |
| `tone:` | `light`, `heartfelt`, `serious` or `resolution`. It sets the default gate (light: colleague, met 3+ days; heartfelt and serious: friend, 7+ days, 2+ days since their last moment; resolution: close friend, 3+ days after the last heartfelt one) |
| `tier:` `metDays:` `gapDays:` | only where a beat differs from its tone's gate (`tier: close` for the Captain's arc; `metDays: 10`) |
| `when:` | extra conditions, in the same words as `?` lines: `when: rep:known flag:torres.askCalder beat:torres.2` |
| `where:` | `calm` (the default: off duty somewhere to sit, or visiting you), `visit` (your bunk), `appt` (an appointment), or a room name, only if their own free time takes them there |
| `duty: true` | it may open while they're on shift (light beats at work places only) |
| `crisis: true` | it may open during a ship-wide event's onset |
| `hint:` | their tap line while the moment is ready ("Got a minute? Properly, I mean.") |
| `mem:` | the memory word for the beat (stored as `moment.<arc>.<word>`) |
| `flag:` | a story flag set when the beat is told (`flag: torres.applied`) |
| `keepsake:` | what they give you to keep (resolution beats) |
| `learn:` | one line for the Crew app's "What you know" (their story) |
| `mail:` | a Mail from them afterwards: `<minutes later> \| <subject> \| <body>` |
| `needs:` | themes only: the roster details a beat uses (`needs: home, family`); people without them skip it |

- **The script** follows: `them: text [pose]` (`them` is the arc's person; a crew id or `you` also work;
  `them > you: ...` for a line said to you). Poses: `sigh`, `laugh`, `listen`, `nod`, `gesture`.
- **Choices:** `? choice`, then up to three `* reply` lines. Each can carry `flavour:` (`listen`, `cheer`, `practical`,
  `share`), `mem:<word>`, `flag:<key>` (set when chosen) and `favour:<job>` (a practical reply that starts a favour).
  Indent the answer under it (`  them: ...`), and if you like a warmer answer for the person this flavour suits,
  `  + them: ...` below it. There's never a wrong reply.
- **Placeholders and voice tokens** work as in lines (`{me}`, `{hi}`, `{home}`...). Lines are 140 characters at most;
  the hint 90; a Mail body 400.
- Beats 1-4 of Tomas, Pell and Rina are already in the game; their files start at `== beat 5`.

## Calls home (.call)

Your people back home (Mum, Gran, Jo and Sam) live in `content/home/<contact>.call`. A call file is an arc file with
three differences:

- **The header:** `@arc home.<contact>`, `who: home:<contact>`, `name: Mum` (what you call them), and `pron: they`
  where it applies.
- **Beats** take every arc field plus `via: reply` (an ordinary call) or `via: live` (it waits for a clear line, Letters
  evening). Chain them with `when: beat:home.mum.2` or `when: flag:home.mum.called`.
- **After the beats**, two sections:
  - `== send`: things you can tell them on a call. `? conditions`, then `- text   flavour:share` (optionally `flag:<key>`
    or `mem:<word>`, set when you choose it) with their reaction indented under it (`  them: text [pose]`). Conditions
    last until the next `?`, so put a bare `?` before lines anyone can say. `came:any` and `friend:any` (with `{trad}`
    and `{friend}`) are for "I went to quiz night" and "I've made a friend".
  - `== chat`: whole everyday calls for days with no beat, separated by `--`. An optional `when: <conditions>` first,
    the lines, and `? send` where your choice of news goes.

Family warmth ("I love you", "love to you") is fine in call files, and only that: any other romance word ("in love",
"my love", "my heart"...) is an error there as everywhere; the head writer reads them for tone. The contacts are `mum`,
`gran`, `jo` and `sam` (a file for anyone else is an error). Jo, Sam and the contacts' names count as known names.

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
- **No romance or flirting** with the player (the checker catches the obvious words in every line said to you; crew
  couples may talk in overheard conversations between a couple (`pair:couple`) and in lines with a `bond:couple`
  condition, but never in a line that mentions the player in any way: `{me}`, `{nick}`, "the new hand", "cadet",
  "newcomer", "you", "your". `about`, `rumour` and `smalltalk` are said to the player, so the full rule applies there). A false alarm ("Brennan's in love with that new oven"):
  reword it, or the head writer adds the line's id (shown in the error) to `content/allow.list`, one id a line, `#` for
  a note; the head writer also reads every
  moment and arc beat for the no-romance-with-the-player rule, which no word list can fully catch), **no swearing** beyond "blast", **no real-world brands or politics**, and
  nothing the game doesn't have (no photos, cameras, phones, weapons).
- **`#serious` lines are earned:** only behind `tier>=friend`, a `beat:`, `mem:moment...` or `leaving:soon`.
- **Names:** only roster crew, guests and canon names (every capitalised word in `content/facts.md` counts). A name it
  doesn't know is a warning.
- **British spelling** (colour, favourite, mum, biscuit).
- **Moments and meetings:** at most three replies in a choice; poses only `sigh`, `laugh`, `listen`, `nod`, `gesture`, `play`.
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
  for either, an array when all must hold; `tier: [lo, hi]`), `CONVOS = [{ id, topic, pair, ..., lines: [{ who, text }] }]`, `MOMENTS['<crewId>:<n>'] = { who, thread: 'arc:<arcId>', beat, tone, where, when, tier, metDays, gapDays, duty, crisis, hint, mem, flag, keepsake, learn, after: { mail }, lines }` and `MOMENT_THEMES[theme] = [{ beat, ..., needs, lines }]` (social B's shapes; `when` is a condition object for `linesOk`),
  `MEETINGS_BAKED[id]` in `MEETING_SCRIPTS`' shape, `TRADITIONS = [ ... ]`, one tradition a line, as `plans/trad_parse.py` reads it
  (the traditions engineer's shape, `plans/trad-format.md`).
- A line's id is a short hash of its file, kind and text: rewording a line gives it a new id.
- Lines gated on a flag nobody sets (Torres's walk, `? flag:walk.hello`) are fetched with `lineFor(who, kind, { flags: { 'walk.hello': true } })`: `ctx.flags` answers `flag:` for its keys.
- Section 22 (`lineFor`, `overheardFor`, `linesOk`, `linesFill`) is the engine; see DEV_NOTES, "Lines (section 22)".
