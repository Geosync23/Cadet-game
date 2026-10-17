# The `.trad` format: ship traditions as plain text

Owner: the traditions engineer (seat 5, `claude/ship-events`). For the three tradition designers (who write the files) and the dialogue engineer (whose `content_gen.py` bakes them into the game). First written at build 0.34.20.

**How it flows:** a designer writes `content/traditions/<id>.trad` → the dialogue engineer's `content_gen.py` bakes every content file; for a `.trad` file it reads the frame (the `@tradition` header, `//` comments, `==` sections, `?` conditions and `- ` lines, exactly as in `.lines` files: `content/README.md`) and hands each `key: value` field to `parse_field()` in `plans/trad_parse.py` (this page's grammar, the traditions engineer's) → the result lands in the game's `TRADITIONS` block (section 22's generated blocks) → at load, section 18's loader turns each one into a ship tradition (`SHIP_TRADITIONS`), exactly like the twelve hand-written ones. No code needed for a normal tradition. A tradition with the same id as an existing one replaces it.

**Check before you push:** `python3 plans/trad_parse.py` (checks every `.trad` file and prints them, or the first error with file and line), then `python3 content_gen.py --check` and `python3 lines_check.py` when they're in your branch. Then tell the traditions engineer, who merges your files, runs `events_check.py` (a whole ship year on paper) and builds anything that needs code.

## A whole example

```
@tradition sowing
// lines starting with // are notes, ignored. The @tradition line comes first.
k: 434
title: Sowing morning
when: quarter week 1 saturday
at: 11:45-12:40
min: 20
prio: 1
where: 3 pool garden
hold: none
who: gardener 90%, garden-lover 75%, everyone 30%
anim: water
from: brennan
ties: garden sow

== mail
- A new season starts in the garden: Sowing morning tomorrow, 11:45, after the harvest. Everyone plants a seedling.

== ask
- Sowing morning today. Bring clean hands.
- I'm planting basil this time. Don't tell Brennan, she'll want it.   #funny

== here
- Two seeds a pot. One for luck.

== thanks
- You press a seedling into its pot and write your name on the tag. {season} has begun.

== chatter
- Whose seedling is that, already leaning towards the lamps?   #funny
```

One tradition per file, the file named after its id.

## The keys

| Key | Required | What it says | Examples |
| --- | --- | --- | --- |
| `@tradition <id>` | yes | starts a tradition; the id is lower-case letters, digits and dashes, never changed once it's in the game | `@tradition tiles-night` |
| `k:` | yes | its hash key, **given by the traditions engineer** (434-499, each once). Ask for one; never reuse one | `k: 435` |
| `title:` | yes | the name players see (Mail subject, Calendar) | `title: Tiles night` |
| `when:` | yes | the rhythm (below) | `when: weekly tuesday` |
| `at:` | yes | start and end, ship time | `at: 20:00-21:30` |
| `where:` | yes, one or more | where people go, best first (below) | `where: 3 room Bow lounge: lounge-seat` |
| `who:` | yes | who goes, as chances, first match wins (below) | `who: rina always, juniors 35%, everyone 10%` |
| `min:` | no | the shortest stay worth going for, ship minutes (default 20) | `min: 25` |
| `prio:` | no | if a person has two traditions that overlap, the higher prio wins (default 0; birthdays are 2, Founding Day 3) | `prio: 1` |
| `jitter:` | no | each person leaves up to this many minutes before the end | `jitter: 15` |
| `early:` | no | the honoree(s) come this many minutes early | `early: 5` |
| `hold:` | no | which `where` lines (1 = the first) are kept free for those going during the window: default the first; `none` for big, casual ones (so dinner goes on around it) | `hold: none`, `hold: 1,2` |
| `anim:` | no | what they do there: `talk`, `drink`, `play`, `water`, `wash`, `read`, or rules like `who:` | `anim: play`, `anim: musician play, everyone talk` |
| `host:` | no | a crew id: the host is seated first, always goes if free, and fills `{host}` | `host: rina` |
| `from:` | no | who signs the Mail: a crew id (their name is used) or plain text | `from: brennan`, `from: The crew store` |
| `cake:` | no | `yes`: the galley bakes a cake that day | `cake: yes` |
| `decor:` | no | props on the deck while it's on (an id the traditions engineer or deck architect builds) | `decor: stalls` |
| `ties:` | no, one per kind | what it asks of other parts of the ship (below) | `ties: garden harvest` |
| `invite:` | no | crew may invite you (social reads it) | `invite: host=rina odds=40% line="Tiles tonight. I need a victim."` |

Crew ids are the roster's (`brennan`, `calder`, `torres-zeke`, `rina`, `tomas`, `pell`...: see `plans/crew-roster.html`).

## `when:` the rhythms

| Write | Means |
| --- | --- |
| `weekly tuesday` | every Tuesday |
| `every 2 weeks tuesday` / `every 2 weeks tuesday week 2` | every other Tuesday (week 1 = days 1-7, the default; week 2 = days 8-14) |
| `every 4 weeks saturday week 3` | the Saturday of every fourth week, starting with week 3 (days 20, 48, 76...) |
| `quarter week 1 saturday` | the first Saturday of each season (days 6, 97, 188, 279) |
| `quarter day 1` | the first day of each season |
| `year day 182` | one day a year (the year is 364 days, Day 1 a Monday) |
| `year week 52 sunday` | the last Sunday of the year |
| `arrival +7` | seven days after you came aboard (you arrive on day 0, a Sunday evening) |
| `arrival friday` / `arrival friday 4` | the first (or fourth) Friday after you came aboard |
| `birthday` | each crew member's birthday (birthdays are never moved) |

Add any of these after the rhythm: `season greening` (or `season harvest,lanterns`), `from day 30`, `until day 200`. Example: `when: weekly wednesday season greening`.

**The seasons:** Sowing (days 1-91), Greening (92-182), Harvest (183-273), Lanterns (274-364), then again.

## `where:` places

- `3 pool garden`: a deck and one of the shared pools the schedules know (`gym`, `music`, `garden`, `garden-tend`, `mess-seat`, `lounge-seat`, `bench`, `common-room`...).
- `3 room Bow lounge: lounge-seat, bench`: the shared places of those types in the room with that name. Extra words after the types: `free` (nobody's work station), `officers` (officers and up only), `ids <regexp>` (only those place ids).
- Places the deck architect tags for your tradition (`event: '<id>'`) are always used first.

## `who:` and `anim:` rules

A comma-separated list of `<who> <chance>`; the first that fits a person decides. Chances are `90%`, `always` or `never`; anyone matching nothing doesn't go. Only people who are free for the whole window go (awake, off shift, not about to sleep), so a 100% still misses the people on duty.

`<who>` is one word, or several joined with `+` (all must fit, e.g. `works+juniors 60%`):

- `everyone`, `host`, `honoree`, `juniors`, `officers`, `friends-of-host`;
- a crew id (`rina`), a department (`works`, `galley`, `garden`, `survey`, `watch`, `infirmary`, `command`, `helm`, `comms`, `store`, `civilian`), or a habit (`gardener`, `musician`, `runner`, `stargazer`, `bar-regular`, `shopper`...: the roster's HABITS);
- to be exact: `id:<x>`, `dept:<x>`, `habit:<x>`, `rank:<x>`.

`events_check.py` fails on any word it can't resolve.

## `ties:` asking other parts of the ship

Each is read by its owner with `tradTies(kind, day)`; ask the traditions engineer before relying on one.

| Write | Read by | Means |
| --- | --- | --- |
| `ties: galley dish=<dishId> meal=dinner batch=10` | the galley engineer | a dish or a special meal that day |
| `ties: garden sow` / `tend` / `harvest` | the galley engineer (the garden) | the garden's part |
| `ties: decor <id>` | the deck architect | props on its deck for the window (at most 6 draw calls) |
| `ties: tally <kind> choices=a\|b\|c` | the traditions engineer | a simple vote or score kept for a week |

## Texts

Texts go in sections, one variant per line starting with `- ` (a line may have `? conditions` above it, as in `.lines` files, for the dialogue engine; the tradition's own Mail and tap lines use the plain ones):

| Section | When it's used | Notes |
| --- | --- | --- |
| `== mail` | the Mail at 18:00 the evening before ("Ship tradition: <title>, <day> <time>") | one is enough |
| `== ask` | a crew member's tap line earlier that day, when they're going | 2-4 variants; picked per person and day |
| `== here` | the tap line while they're there | 2-4 variants |
| `== thanks` | the toast when you join (five minutes in the room) | 1-2 |
| `== chatter` | lines crew may say about it (the dialogue engine) | a few |

- **Tone tags** at the end of a line: `#funny`, `#warm`, `#serious` (default light). A bubble is at most 90 characters, a Mail at most about 200.
- **Placeholders:** `{trad}` (its title), `{host}` (the host's first name), `{names}` and `{first}` (a birthday's people), `{season}`, `{weekday}`, `{time}`. A line whose placeholder can't be filled is skipped.
- The head writer checks the texts for tone.

## The baked shape (for content_gen.py)

`TRADITIONS = { <id>: { ... } }`, one object per tradition, fields as `parse_field()` builds them and `finish()` orders them: `id, k, name, when, at, min, prio, jitter, early, where, hold, who, anim, host, from, cake, decor, ties, invite, text`. `at` in minutes from midnight; `when` as section 18's objects (`{ every: 'quarter', week, weekday }`, weekdays 0 = Monday); room names as anchored regexp source (`"^Bow lounge$"`); `hold` 0-based; `who` as `[[cond, chance], ...]`; `anim` a string or `[[cond, act or null], ...]`; texts as `text: { <section>: [ line entries ] }` (content_gen.py's `{ text, id, tone?, ...conditions }`). In content_gen.py's `parse_tradition`: call `trad_parse.parse_field(tr, key, value, where)` for each field line, and `tr = trad_parse.finish(tr, id, path)` at the end; `trad_parse.check_all(list)` across all traditions (ids and `k` once each). Until that block is in the build, section 18 has a stand-in, `TRAD_STANDIN`, made by `python3 plans/trad_parse.py --standin`.
