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
| The meeting at the place | meeting `train.<id>.<teacherId>` | e.g. `train.m7.halloran-emeka` (Day 5: m7 and p3's teachers are torres-zeke, halloran-emeka, calder; first on shift). Pick by the teacher who actually teaches (the `by` list's first on shift). Small openings use the same id (one or two lines) |
| The ask (toast + Mail) | `works.ask.<id>` | text, "Subject \| body"; Mail unsigned (the game adds the sender) |
| Teacher's words while they lead (you watch) | kind `work` in the teacher's own lines, `? flag:train.<id>.lead.<step>` | every line under a flag plays in order. Seat C (0.44.1) plays `lead.take` when they lead you to it and `lead.done` when they hand over; job steps: `take`, `fetch`, `make`, `hold` (= the panel), `carry` (cart, pickup, drop), `done` (turn-in is followed by `works.trained`). The mechanics' own steps (`look` on rounds, `turn` in tuning, `choose`, `wait`) are named for seats M1/M2 |
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

## Step 2 (seats M1, M2; batch 2)

Meetings (24.2): `train.m1.torres-zeke`, `train.m4.esposito-yara`, `train.m3d.calder`, `train.m3i.tomas`,
`train.m5.calder` (Brennan in the cast), `train.m6.calder`, `train.m2.torres-zeke` (one line). Asks: `works.ask.<id>` for
m1 m4 m3d m5 m3i m6 m2 (Mail "Subject | body", up to 140).

Teachers' step words (kind `work`, flags as above): Torres `train.m1.lead.look`, `train.m1.follow.look/done`, and the mark
reactions `train.m1.mark.right` (you marked worn/off on a worn/faulty machine), `.mark.wrong` (fine on a worn one),
`.mark.okay` (worn/off on a healthy one). Yara `train.m4.lead.load`, `train.m4.follow.load/drop/done`; `haul.goodroute`
(Yara's kind, stage 2). Calder `train.m5.lead.turn`, `train.m5.follow.turn/done`, `train.m6.follow.choose/wrong/clean/fetch/done`;
`drill.time.fast|ok|slow` (her kind); `clothes.grubby` (her kind). Brennan `train.m5.grumble` (breakfast, Day 4) and
`train.m5.follow.done` (the biscuit); `inc.alarm` (her kind). Tomas `inc.mop` (passing while you mop).

| Seat | Texts (`content/works/step2.lines` unless noted) |
| --- | --- |
| M1 rounds | `round.title` ({deck}), `round.mark.fine/worn/off`, `round.okay`, `round.found` ({machine}), `round.done`, `round.pick`, `round.nose`; signs `sign.<kind>.healthy/worn/faulty` (`signs.lines`, Tier 1 kinds + scrubber, heater) |
| M1 hauling | `haul.title` ({n}), `haul.manifest`, `haul.crate.<dest>`, `haul.stop.<dest>` (laundry infirmary store galley bridge), `haul.load`, `haul.drop`, `haul.done`, `haul.order`, `haul.goodroute.note`; stocktake `stock.title/look/wrong ({part} {shelf})/move/moved`; `haul.thanks` (crew, `remarks.lines`) |
| M1 drill + inspection | `drill.kind.fire/pressure/power`, `drill.cal` ({drill}), `drill.toast`, `drill.job.<kind>`, `drill.allclear`, `drill.offduty`; `inspect.bed.button`, `inspect.locker.button`, `inspect.bed.done`, `inspect.locker.done`, `inspect.reminder`, `inspect.mail.subject`; the duty officer's remarks (`inspect.lines`): `inspect.nod`, `.uniform`, `.bed`, `.locker`, `.two`, `.none` and Mail `inspect.mail.<result>` |
| M2 tuning | `tune.title` ({machine}), `tune.minus`, `tune.plus`, `tune.hot/warm/steady/cool/cold`, `tune.done` |
| M2 incidents | `inc.card.burst` ({room}), `.lift`, `.alarm`; `inc.toast.<id>` ({deck}); `inc.step.safe/clean/fix`; `inc.wrong.valve`; `inc.safe.<id>`, `inc.clean.<id>`; `inc.done`; `inc.missed`; `inc.thanks` (the rescued rider, `remarks.lines`); reactions `@reactions incident.burst|lift|alarm` (cue `incident.<id>`, `.you` when you handled it) |
| M1 uniform | `uniform.rule`, `uniform.grubby`, `uniform.wait` ({machine}); crew `clothes.grubby` (`remarks.lines`, gated `flag:clothes.grubby`) |

## Playtest 1 (0.63.2; lead 13's brief plans/brief-playtest1.md)

| Seat | Keys |
| --- | --- |
| O4 onboarding | Zeke (torres-zeke.lines, kind `week1`): `walk.shuttle.1-5` (plain greeting, "Works Department"), `walk.works.1`, `walk.day1.1-3` (training-day opener), `walk.follow.1-30` (4 is new: "jobs get better as you go"; the rest moved up one), `walk.dinner.eve.4-5` (you can't do every tradition), `walk.tea.1-3`, `walk.tea.go.1-2`, `walk.tea.at.1-3`, `walk.tea.after.1` (13:00 tea and biscuits); `mail.zeke-welcome` ("Subject \| body", up to 400); meeting `introBunk` reworded (the middle top bunk, the wardrobe, the device and his Mail); `tip.clothes.day1` (banks/clothes.lines) |
| X crew | kind `seek` (banks/approach.lines): the opener when a crew member has walked up beside you, tiers 1-4, week-1 evening, leaving soon; 70 characters or fewer |
| T traditions | `join.tip.<tradId>` ({host}), `join.notice.<tradId>` (up to 200), `join.done.<tradId>` for lap-of-the-wren, sunrise-stretch, running, cook-along, lantern-walk, knit-and-natter, tiles-ladder (banks/join.lines); `beam.tip`, `beam.done`; crew `beam.congrats` (to you), `beam.cheer` ({other}, a later Works arrival) in banks/beam.lines; Zeke `trad.beam.1-4` (restored), Calder `trad.beam.chief` |
| everyone | the 09:00 shift and 13:00 tea and biscuits in every line (was 08:00 / ten to eight / half ten) |
