# Pillar 5 line keys (head writer, seat W)

Every key is a kind in a `.lines` file (or a meeting id), read the usual way: `lineFor(who, kind, ctx)` for a crew
member, the text helper for words nobody says, `MEETING_SCRIPTS[id]` for meetings. Placeholders the engineer fills are
listed per key. If a key doesn't fit your code, tell the writer and it's renamed here; don't rename on your side.

Files: `content/works/works.lines` (texts: the Works app, Record, ladder names, skill and band words, mails, notes),
`content/works/next.lines` (What's next), `content/works/faults.lines` (the fault tables' words), `content/works/cases.lines`
(head-scratcher texts and the Chief's notes), meetings `content/meetings/train.<id>.<teacher>.meet`, and the teachers'
step lines in `content/lines/<teacher>.lines` (kind `work`).

## Training moments (seat C, 24.2)

| What | Key | Notes |
| --- | --- | --- |
| The meeting at the place | meeting `train.<id>.<teacherId>` | e.g. `train.m7.calder`, `train.m7.torres-zeke`. Pick by the teacher who actually teaches (the `by` list's first on shift). Small openings use the same id (one or two lines) |
| The ask (toast + Mail) | `works.ask.<id>` | text, "Subject \| body"; Mail unsigned (the game adds the sender) |
| Teacher's words while they lead (you watch) | kind `work` in the teacher's own lines, `? flag:train.<id>.lead.<step>` | every line under a flag plays in order, like Zeke's walk lines; `<step>` = the stop's step or tag: `take`, `look`, `fetch`, `make`, `hold`, `choose`, `turn`, `carry`, `wait`, `done`, `turnin` |
| Teacher's words while you lead | `? flag:train.<id>.follow.<step>` | same steps |
| Trained | `works.trained` | text: "Trained: {mech}, with {name}." `{mech}` from `works.mech.<id>`, `{name}` the teacher's name |

## The Works app, the Record, words (seat C, 24.3-24.5)

| Key | Text | Placeholders |
| --- | --- | --- |
| `works.app.title`, `works.tab.training`, `works.tab.log`, `works.tab.tools` | app and tab names | |
| `works.mech.<id>` | each ladder row's name (m1 m4 m3d m5 m3i m7 p3 m6 m2 t2; `job` for Day 1's job loop) | |
| `works.training.none` | Training tab with nothing yet | |
| `works.training.next` | the heading before What's next | |
| `works.log.row` | one log line | `{job}` `{weekday}` `{n}` (day number) |
| `works.log.found`, `works.log.first`, `works.log.clever`, `works.log.noticed` | flags on a row | `{name}` (who noticed) |
| `works.log.none` | an empty log | |
| `works.tool.<id>` | a tool's name (clipboard, scanner, pipekit, logger, tester, calrig) | |
| `works.tool.<id>.about` | one line about it | |
| `works.toolwear.new`, `.good`, `.worn`, `.tired` | wear in words (0-.25, -.5, -.75, more) | |
| `works.tools.none` | no tools yet | |
| `works.locker` | the locker's tap line | `{tools}` (names joined) |
| `works.skill.new`, `works.skill.hang`, `works.skill.know` | skillWord: "new to you", "getting the hang of these", "you know these well" | |
| `works.skill.row` | "Ovens: you know these well." | `{machine}` (plural, capitalised by the game), `{skill}` |
| `works.band.new` ... `works.band.relied`, `works.band.newofficer` | the reputation words | |
| `works.title.t1` ... `works.title.t4`, `works.rank.junior` ... `works.rank.specialist` | rank and tier titles | |
| `works.record` | the Record's line | `{title}` `{rank}` `{band}` `{next}` |

**What's next** (`content/works/next.lines`, 24.4 worksNext): `next.<id>` (the next unopened row: what's coming, and who
teaches it), `next.wait.<id>` (opened but not trained yet: go and meet them), `next.band.<band>` (no row ahead: keep at it),
`next.t2` (ready for the test job). One line each; the game picks one at random per day if there are several.

## The scanner (seat H, 24g) and the parts (seat S, 17)

| Key | Text | Placeholders |
| --- | --- | --- |
| `scan.title` | "Scanner · {machine}" | `{machine}` |
| `scan.job` | "the job: {shows}" | `{shows}` |
| `scan.read.good`, `.worn`, `.low`, `.failing` | the reading's word | |
| `scan.fetch` | "Fetch: {part}" | `{part}` |
| `scan.none` | before the scanner (no panel): unchanged, so no key |
| `works.note.scanner` | Torres's taped note | |
| `fault.name.<kind>.<cause>` | the cause in plain words ("The element is failing") | |
| `fault.shows.<kind>.<cause>` | the card ("runs cool") | |
| `fault.sign.<kind>.<cause>` | up close ("cool all over, slow to heat") | |
| `fault.still.<kind>.<cause>` | the wrong-fit line, keyed by the cause whose part you FITTED: what went in and that it's still wrong ("New element in. Still runs cool."). It never names the real cause, so it's right whichever cause is real; show the real cause's `fault.sign` after it if you want a pointer | |
| `fault.tried.<kind>.<cause>` | a P3 note's words when someone fitted that cause's part ("New door seal in. Still leaks.") | |

## Head-scratchers (seat H, 24k)

| Key | Text |
| --- | --- |
| `case.tab.notes`, `case.tab.chief` | Works app tabs: Fault notes, the Chief's notes |
| `case.title` | "Head-scratcher: {machine} {shows}." |
| `case.suspects`, `case.notes` | headings |
| `case.cross`, `case.uncross` | buttons |
| `case.call` | "Call it: {part}?" |
| `case.where` | "Where next?" |
| `case.hint.p3.1` | "Have you read every note? One's on the machine." |
| `case.solved`, `case.wrong` | outcome texts |
| `chief.p3.1` ... `chief.p3.3` | the Chief's notes, page 1 "What's been tried" |
| teacher's hints 2 and 3 (c.train) | kind `work`, `? flag:train.p3.hint.2` / `.3` in the teacher's lines |
