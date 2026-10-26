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
| The ask (toast + Mail) | `works.ask.<id>` | text, "Subject \| body"; Mail unsigned (the game adds the sender). `{time}` and `{place}` are the meeting's real time and room ("Galley on Deck 3"); without `{time}` in the body the game adds "(time, place.)" after it, so never write a time by hand (p5-fix2) |
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
| `works.record` | the Record's line | `{title}` (FX3: the title and rank together, "Junior Technician" for a junior, "Technician · Officer" after), `{rank}`, `{band}`, `{next}` |

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
| O4 onboarding | Zeke (torres-zeke.lines, kind `week1`): `walk.shuttle.1-5` (plain greeting, "Works Department"), `walk.works.1`, `walk.train.open.1-3` (training-day opener, at the briefing's end), `walk.train.better.1` (after the first job's turn-in), `walk.cabin.wardrobe.1-2` (at your wardrobe after the bunk meeting), `walk.eve.choose.1-2` (you can't do every tradition; after walk.dinner.eve), `walk.tea.explain.1-3`, `walk.tea.go.1-2`, `walk.tea.at.1-3`, `walk.tea.back.1-2` (O5's names) (13:00 tea and biscuits); `mail.zeke.cabin` ("Subject \| body", up to 400); meeting `introBunk` reworded (the middle top bunk, the wardrobe, the device and his Mail); `tip.clothes` (banks/clothes.lines) |
| X crew | kind `seek` (banks/approach.lines): the opener when a crew member has walked up beside you, tiers 1-4, week-1 evening, leaving soon; 70 characters or fewer |
| T traditions | `join.<id>.tip` ({name}, also the arrow label), `join.<id>.notice`, walks only `join.<id>.done` / `.left`, for T's 21 ids (banks/join.lines); `join.name-on-the-beam.tip/.tell/.paint/.notice`; crew `beam.congrats` (banks/beam.lines, Works bank); Zeke `trad.beam.1-4`, Calder `trad.beam.chief` |
| everyone | the 09:00 shift and 13:00 tea and biscuits in every line (was 08:00 / ten to eight / half ten) |

## Step 3 (0.63.3; lead 16's brief plans/brief-p5s3.md; head writer W2)

Proposed by W2 at the start of Step 3. **If your code already uses another name, tell W2 and W2 adopts yours.** Texts
(said by nobody) are `@bank all` kinds in `content/works/step3.lines`; crew words are kinds in each person's own
`content/lines/<id>.lines`, fetched with `lineFor(who, kind, { flags: { '<flag>': true } })`. Mails are "Subject | body",
unsigned. Calder's flag lines also exist for Vance (`vance.lines`) where the page says Vance stands in.

### The test job and the first promotion (C2; X for the walks and crowds)

**Final: C2 0.44.24 uses the b4630d4 names** (our renames crossed three times; agreed final by both). The 0.44.23 text names are kept too (different kinds), so either reads.

| When | Key | Who / kind | Placeholders |
| --- | --- | --- | --- |
| Day 8 in the bay, "Tomorrow, your test job" | `promo.announce` | text (worksText) | |
| ... the Mail if you're not in the bay by 10:00 | `promo.announce.mail` | text, Mail | |
| Day 9, 09:00, as the test job goes up | `promo.test.start` | text | |
| Test job steps, Calder following | `flag:train.t2.step.<take\|fetch\|make\|job\|tune\|done\|turnin>` (+ `look`, `scan` if 24a/24g add stops) | calder `work` | |
| Torres comes by at the end (Tuesday) | `flag:train.t2.torres` | torres-zeke `work` | |
| Passed / not done | `promo.test.passed`, `promo.test.again` | text | `{day}` (weekday) |
| The summons toast (urgent), Torres's nudge | `promo.summons`, `promo.summons.torres` | text | |
| Calder finds you at 11:15 / 17:30 / the ceremony | `flag:promo.fetch.summons`, `.fetch.move`, `.fetch.ceremony` | calder `work` (vance for move and ceremony) | |
| The office scene | meeting `promo.officer` | Calder; one choice of three in this order: proud, surprised, about time (C2 stores promo.reply 1-3) | |
| The scene by Mail, if you never came | `promo.mail` | text, Mail | |
| The crew at the board | kind `promoted` (X; 50 characters) | `banks/promo-works.lines` + torres-zeke, pell ("Told you"), kovac-zainab, halloran-emeka | `{nick}` |
| All day: people who know you | `@reactions promoted` (`content/reactions/promoted.lines`), cue `promoted.you` | crew bank by tier | |
| Mail from friends | kind `mail.promo.friend` (`content/banks/promo.lines`) | crew bank by tier; up to two friends | `{me}` `{nick}` |
| Mail from the Captain | `promo.captain` | text, Mail | |
| Ship app news (one gossip line) | `promo.news` | text | `{me}` |
| Brennan's cake (C2 0.44.24, the lead's call: within 3 m of her at the tea corner, 16:30-17:00) | `flag:promo.cake`; toast `promo.cake.toast` | brennan `work` (and `cue`) ; text | |
| Calder's walk to 4-23 | `flag:promo.walk.start`, `.lift`, `.corridor`, `.door`, `.inside` (C2 0.44.24); text `promo.walk` also there | calder `work`; the same flags in vance `work` | |
| Tomas and Pell with your box; Tomas's goodbye (X) | `flag:promo.box`; `flag:promo.bye` | tomas, pell `work` | |
| Move by Mail (without you) | `promo.move.mail` (C2 0.44.23; also `mail.promo.move`) | text, Mail | |
| The door plate (DA5) | `works.plate` | text: "{name} · {rank}" | `{name}` `{rank}` |
| Ceremony Mail (Day 11, 08:00) | `promo.ceremony.invite` (C2 0.44.23; also `mail.promo.ceremony`) | text, Mail | |
| The ceremony | meeting `promo.ceremony` | marrow, vance, calder, torres-zeke (guests are walk-ons); the line ending ` {pin}` bakes `pin: true` (content_gen), then one choice for your line | |
| The ceremony by Mail, if you never came | `promo.ceremony.mail` | text, Mail | |
| Guests after the ceremony | `@reactions ceremony`, cue `ceremony.you` | guests / friends | |
| The keepsake, the Record | `promo.keepsake` (its name), `works.record.commissioned` (C2 0.44.23; also `works.keepsake.commission`, `works.ms.commissioned` {n}) | text | `{day}` (day number) |
| Calder's look at a grubby uniform, as you come in | `flag:promo.grubby` | calder `work` | |
| Tomas's goodbye, text form (X plays tomas `promo.bye`) | `promo.move.tomas` | text | |
| What's next | `next.t2` (have), `next.wait.t2` (the test set, not done), `next.summons`, `next.move`, `next.ceremony` (C2 reads these or `next.wait.*`) | `next.lines` | |

### Team jobs (M2 24h; X for the crew)

| Key | What | Placeholders |
| --- | --- | --- |
| `works.mech.m8`, `works.ask.m8` | ladder name; Day 11 Mail at 08:05 from Halloran | |
| meeting `train.m8.halloran-emeka` (+ `.torres-zeke`, `.calder`) | at the recycler: spots, your part | |
| `team.name.<job>` | job names: `recycler`, `washer`, `manifold`, `heater`, `scrubber` | |
| `team.card` | the board card | `{job}` `{time}` `{deck}` `{n}` |
| `mail.team` | the 16:00 posting Mail ("Subject \| body") | `{job}` `{time}` `{deck}` `{name}` (the lead) |
| `team.turn.<part>` | your toast: `brace` `pass` `hold` `crank` `tip` `valves` `open` `drain` | |
| `team.start`, `team.wait`, `team.late`, `team.done` | texts: started, waiting for you, started without you, done | `{name}` (the lead) in wait and late |
| `flag:team.call.<part>` + `team.call.start/.done` | the lead's calls, kind `work` in halloran-emeka, torres-zeke, calder, and a works bank fallback (`content/banks/team.lines`); said for the crew's steps too, so they never name you | |
| kind `team` (X's name) | crew talk while they work, one bubble each (`content/banks/team.lines`, works bank + Pell, Kovac, Torres) | |
| `next.m8`, `next.wait.m8` | What's next | |
| `@bank dept:works` fallbacks | `content/banks/team.lines` (calls), `content/banks/promo-works.lines` (the gathering) | |

### Tracing (M3 24i)

| Key | What | Placeholders |
| --- | --- | --- |
| `works.mech.m9`, `works.ask.m9`, `works.tool.pipekit` (have) | | |
| meeting `train.m9.calder` (+ `.halloran-emeka`) | at the board: the pipe kit, the line on the Maps app | |
| `flag:train.m9.follow.<step>`: `give` `map` `read` `wrong` `found` `done` | Calder's words | |
| `trace.title` | "Pipe kit · {machine}" | `{machine}` |
| `trace.full`, `trace.low`, `trace.verylow` | the reading word | |
| `trace.before`, `trace.after` | "Before: {word}" / "After: {word}" | `{word}` |
| `trace.found` | flow fine before, low after | `{machine}` |
| `trace.wrongline` | reading a machine that isn't on the job's line | |
| `trace.symptom.water`, `.heat`, `.air` | the card ("Showers weak on Deck {deck}", "Cold cabins on Deck {deck}") | `{deck}` |
| `trace.line.water/heat/air` | line names (Maps app) | |
| `chief.m9.1-2` | the Chief's notes page | |
| `next.m9`, `next.wait.m9` | What's next | |

### Head-scratchers T2, P1, P2 (H2 24k)

| Key | What | Placeholders |
| --- | --- | --- |
| `works.mech.p1`, `works.mech.p2` | ladder names | |
| `next.p1`, `next.wait.p1`, `next.p2`, `next.wait.p2` | What's next | |
| `flag:train.p1.word` | calder / halloran-emeka `work`: "When does it happen?" | |
| `flag:train.p2.word` | tomas `work` (+ torres-zeke): ask who was there | |
| `chief.p1.1-2`, `chief.p2.1-2` | the Chief's notes pages | |
| `case.title.p1` | "{machine} {shows}, but only {when}." | `{machine}` `{shows}` `{when}` |
| `case.when.evening/morning/night/peak/after` | the when words | |
| `case.strip.title`, `case.strip.fine`, `case.strip.low` | the day strip ("{machine}'s log") and its list fallback | `{machine}`; `{from}` `{to}` |
| `case.line.water/heat/air`, `case.line.<line>.shows` | P1's card: the line's end ("Showers on Deck {deck}") and what it does ("run weak") | `{deck}` |
| `case.ask` | the chat card button: "Ask about the fault" | |
| `case.title.p2` | P2's card (H2 adds "Head-scratcher: ") | `{machine}` `{deck}` `{shows}` |
| `case.p2.head` | Fault notes heading for what people said | |
| `case.hint.p1.1`, `case.hint.p2.1` | the first hints | |
| `case.wrong.p1` | a wrong call in P1 | `{part}` `{where}` `{shows}` |
| `case.strip.allday`, `case.strip.head` | the day strip: fine all day; its heading | |
| `case.wrong.t2` | a wrong call at T2 (the part is spent) | `{part}` |
| `content/cases/p2.lines`: kinds `ask.saw.still`, `ask.saw.door`, `ask.quiet.still`, `ask.quiet.door`, `ask.mixup`, `case.ask.none` (H2's names) | witness answers by what the door did; a mix-up names where they really were | `{time}` `{place}` (with its article: "the lift lobby", "Bunk 3") `{machine}` (short, never sentence-first) |
| `fault.tried.odd` (`faults.lines`) | P3 T2: a note that rules out less than it seems (H2 adds " — Surname") | `{part}` `{shows}` |

### Bridge, meters

| Key | What | Placeholders |
| --- | --- | --- |
| `bridge.locked` | tapping the bridge door before you're invited (C2 / DA5's hook) | |
| meeting `bridgeInvite` (reworded) | Vance's invitation at breakfast, the day before the first bridge hour after the first ship-wide event (C2's placeholder trigger); it opens the bridge too | |
| `meter.<sys>` | short meter names: air water power heat food waste hull comms propulsion transport | |
| `works.turnin.rep`, `works.turnin.meter`, `works.turnin.repN` | the turn-in (C2 and U): "Works reputation up" (words only; C2 passes `{dept}`, unused) / "+{n} {system}" / "+{n} {dept} reputation" (U) | `{n}` `{system}` (the meter.<sys> name) `{dept}` |
| `tiles.paused` | the Tiles notice under the score (U adds the pause sign) | |

## Step 4 (0.63.4; lead 16's brief plans/brief-p5s4.md; D3's pages; head writer W2)

Proposed by W2. **Send W2 your full list in ONE message if your code uses other names; W2 adopts it as is** (Step 3
lesson: no back-and-forth). Texts in `content/works/step4.lines` (`@bank all`); crew words in `content/banks/workshop.lines`
and people's own lines; meetings `train.<id>.<teacher>`.

| Seat | Keys |
| --- | --- |
| all | `works.mech.m10/m11/m12/m13/m14/m15/m17/tickets` (ladder names) |
| E3 M10 workshop (E3's names) | `works.order.ask.<id>`, `works.order.thanks.<id>` ({name}) for guitar-hook mug-rack book-stand lamp-arm plant-hanger fan-spindle drawer-pull tablet-stand; `works.order.lapse` (the Mail's body; E3 adds the subject); the first lesson `work` flag `train.m10.lead` (torres-zeke, halloran-emeka, calder; two lines in order); tinkering has no texts |
| E1 M11 tool upkeep | `works.toolstate.charged/low/due`, `tool.due.<scanner\|pipekit\|logger>`, `bench.<scanner\|pipekit\|logger>`, `bench.done`, `bench.charging` ({time}), `bench.charging.now`, `bench.rack`, `bench.rack.done`; meetings `train.m11.halloran-emeka`, `train.m11.torres-zeke`; Calder `work` flag `upkeep.rack` (stage 3) |
| E1 M12 logbook | `works.log.write`, `works.log.pick`, parts `log.fixed` ({machine} {part}), `log.serviced`, `log.found` ({machine} {shows}), `log.open`, `log.quiet`, `log.saved`; stage 2 `log.flag`, `log.flagged`; stage 3 `case.log.note` ({n} {text}); meeting `train.m12.calder`; Calder `work` flag `log.talk` ({machine}) |
| E2 M13 leaks (matched to E2's code) | `leak.card` ({deck}), `leak.look.above` ({place} = "the north wall"), `leak.look.warmer/here`, `leak.worn`, `leak.turning`, `leak.tight` (the turn), `leak.fix.tighten`, `leak.fix.replace` ({part}), `leak.done`, `leak.found.crew` ({deck}); meetings `train.m13.torres-zeke`, `train.m13.halloran-emeka`, `train.m13.calder` (with a meeting, E2 doesn't read `train.m13.puddle`) |
| E2 M14 irrigation | `noz.plant` (stage 2's plant check), `irr.title` ({n}), `irr.clear`, `irr.cleared`, `irr.flush`, `irr.flushed`, `irr.salad`; meetings `train.m14.cruz-tove`, `train.m14.oneill-imani`, `train.m14.hart-ravi` |
| E2 M15 rewiring | `rewire.card` ({junction}), `rewire.pop`, `rewire.right`, `rewire.done` ({junction}), `rewire.faded`, `rewire.check`, `wire.<red\|blue\|yellow\|green\|white\|black>`; meeting `train.m15.calder` |
| E2 favours | per case id `lamp cold squeak shower clock speaker`: `favour.<id>.ask` (chat), `mail.favour.<id>` (Mail), `.title`, `.sus.1-3` (1 is the real cause), `.clue.1-3`, `.solved`; `favour.call` (the choose card), `favour.not` (a wrong pick), `favour.lapse` ({name}), `favour.head` ({name}); crew kind `favour.thanks` |
| E2 tickets | `mail.ticket.first` (Calder, Day 13), `ticket.card` ({machine} {shows}), `ticket.nohint` (a hint asked before three clues), `ticket.wrong`, `ticket.solved`, `works.grade.1/2/3`, `works.ms.grade` ({grade} {n}), `works.pin`; Calder `work` flag `ticket.solved` |
| E2 team parts | `mail.team.parts` ({job} {time} {name} {parts}), `team.parts.late` ({name}) |
| E1 stages | `round.title.first` ({deck}; playtest item 1's training round), `round.last` ({n}), `round.last.never`, `round.doorway` ({machine} {word}), Torres `work` flag `round.two`; `haul.tidy`; stocktake `stock.count`, `stock.short` ({shelf} {part}), `stock.job`, `stock.fine` ({shelf}) |
| E4 (was E3) cabin, stars (matched to 24t's code) | `cabin.spot.rug/desk/shelf/ledge` (the sentence when you put a thing there); crew kind `cabin.remark` (not read yet); `star.title`, `star.pick` ({a} {b}), `star.right` ({star}), `star.wrong` (retry at once), `star.name` ({n}), `star.done` (ten logged), `works.ms.stars`; sato and mori kind `cue` flag `stars.talk` (every third log; `stars.paid` not read yet) |
| E3 M17 lift roof | meeting `train.m17.halloran-emeka`; Halloran `work` flags `roof.climb`, `roof.grease`, `roof.view`, `roof.done`; `roof.held`, `roof.result`, `roof.resume`; crew kind `roof.wait` |
| FX3 (AR1's findings, 2026-10-22) | `next.t2.rep` ({band}), `next.t2.soon`, `next.t2.set` ({day}: today, tomorrow or a weekday); `works.rep.title`, `works.rep.up` / `works.rep.down` ({band}), `works.rep.missed` (Mail, "Subject \| body", {band}); `works.turnin.you`, `works.turnin.dept` ({dept}), `works.turnin.rep` now the Works team's standing; `inc.warn` (Mail, {time}), `inc.warn.soon`, `inc.goal.follow` ({name} {deck}), `inc.do.yours`, `inc.again` (Mail, {day} {time} {place}); the small rows' asks `works.ask.m3d`, `works.ask.m3i`, `works.ask.p3` are now sent; the inspection morning's arrows `inspect.goal.uniform`, `inspect.goal.bed`, `inspect.goal.locker`, `inspect.goal.here` |
| FX4 (p5-fix4, 2026-10-23) | `inc.goal.wait` ({name}): the call's arrow in her office before the meeting starts (stand-in "Wait here for {name}") |

## Step 5: Senior Officer (lead 39; plans/p5-step5-spec.html on claude/p5-specs; head writer SW3)

Proposed by SW3 with the words already written. **If your code already uses another name, send SW3 your list in ONE
message and SW3 adopts it as is.** Texts (said by nobody) are `@bank all` kinds read with `worksText(key, fallback, vars)`;
people's own words are kind `work` under a flag in `content/lines/<id>.lines` (`worksVoice(id, flag)` / `worksTeach(mech,
id, key)` = flag `train.<mech>.<key>`); the crew's chatter is kinds in a bank, read with `socLine(p, kind, ...)` as 24p's
promoTalkTick does. Meetings are `MEETING_SCRIPTS[id]`; they fill only `{me}`, so any day or time is in the notice and
Mail, and a scene has a twin where the day or time differs.

### The Senior Officer promotion (S5-2, 24u; B1)

| When | Key | Who / kind | Placeholders |
| --- | --- | --- | --- |
| Rep word changes as an Officer (toasts) | `works.rep.up2.trusted`, `works.rep.up2.relied` | text | |
| Nearly there: passing you in the bay at Trusted (once) | `flag:pu3.promo.near` | calder `work`, then halloran-emeka `work` | |
| What's next below Relied on | `next.t3.steps` | text | `{band}` |
| The offer, in person (wherever you are) | meeting `pu3.offer` (test tomorrow), `pu3.offer.monday` (test Monday: offered Fri or Sat), `pu3.offer.party` (Day 14 storm party, bow lounge; cast calder, halloran-emeka, tomas) | two replies each, same order (keen, other); 24u may store `pu3.reply` 1-2 | |
| ... then the urgent notice, the Mail | `pu3.offer.notice`, `mail.pu3.offer` | text | `{day}` |
| ... the Mail when she couldn't find you by 22:00 | `mail.pu3.offer.late` | text | `{day}` |
| Training tab "Your promotion" rows | `pu3.check.title`, `.day`, `.rep` ({band}), `.ps`, `.set` ({day}), `.result` ({day}), `.bar`, `.toast`, `.done`, `.not` | text | |
| Schedule and Tracked rows | `pu3.row.test`, `pu3.row.result`, `pu3.row.bar` ({time}), `pu3.row.toast` | text | |
| Chatter from the offer (how fast; Halloran's own beats the bank) | kind `pu3.soon` | `content/banks/promo-t3.lines`; halloran-emeka | |
| Friends' luck: bubbles, the chat card, the party's raised cups | kind `pu3.luck` (Tomas's own, `place:lounge`, is the party's "Go to bed early. Not yet.") | bank; tomas | |
| Two friends' Mail at 20:00 the evening before | `mail.pu3.luck` (index k = 0, 1) | text, Mail | |
| Test morning: the notice once up; Calder in the bay | `pu3.morning.notice`; `flag:pu3.promo.morning` (calder), else `pu3.morning.say` | text; calder `work` | |
| The board's gold ring on Take it | `pu3.ptr.test` | text | |
| The ring at each step | `pu3.ptr.plan`, `pu3.ptr.warn` ({name}), `pu3.ptr.off`, `pu3.ptr.breaker`, `pu3.ptr.back`, `pu3.ptr.turnin` | text | `{name}` |
| Calder at each step | `train.t3.take`, `.plan` (4 lines: the planning talk), `.warn`, `.warn.late` (one couldn't be found in 30 min: "I'll tell them"), `.off`, `.breaker`, `.back`, `.done`, `.again` | calder `work` (worksTeach('t3', 'calder', key)) | |
| The talk option on someone to warn; the toasts | `pu3.warn.ask`; `pu3.warn.done`, `pu3.warn.calder` ({name}) | text | `{name}` |
| The warned person's answer | kind `pu3.warned` | bank (by dept: works, command, galley, survey) | |
| Crew watching the test | kind `pu3.watch` | bank | |
| Holding another job (hourly) | `pu3.busy.notice` | text | `{time}` |
| Not taken by 15:00 / dropped | `pu3.again.notice`, `mail.pu3.again` | text | `{day}` |
| Torres at the end of the test, if near | `flag:train.t3.torres` | torres-zeke `work` | |
| Passing | `flag:pu3.promo.passed` (calder; torres-zeke's for the bay that evening), `pu3.passed.say`, `mail.pu3.passed`, `pu3.passed.notice` | calder `work`; text | `{day}` `{time}` |
| The bay that evening | kind `pu3.passed` | bank | |
| Result: Mail 06:00, notice once up, ring and arrow | `mail.pu3.result`, `pu3.result.notice`, `pu3.ptr.result` | text | `{time}` |
| The result scene (08:15, her office, seated) | meeting `pu3.result` (bar at 16:30), `pu3.result.fri` (bar at 17:15); two replies, same order | calder | |
| She comes to find you at 08:30 | `flag:pu3.promo.fetch.result` | calder `work` | |
| Torres outside the glass | `flag:pu3.promo.glass` | torres-zeke `work` | |
| By Mail if you never came (09:15) | `mail.pu3.promo` | text | |
| The day: chatter | kind `pu3.senior` (Halloran's and Tomas's own) | bank | |
| Friends' Mail that day (up to two) | kind `mail.pu3.friend` | bank, by tier | `{me}` `{nick}` |
| The bar: invite (morning), notice (30 min before), Calder's "Go.", the ring | `mail.pu3.invite`, `pu3.bar.notice`, `flag:pu3.promo.bar` (calder) else `pu3.bar.say`, `pu3.ptr.bar` | text; calder `work` | `{time}` |
| The bar scene | meeting `pu3.bar` (cast marrow, vance, calder, torres-zeke; the line ending `{pin}` bakes pin: true; one choice after it, 3 replies with `mem:pu3.answer.people/next/torch`) | | |
| Friends right after the bar | kind `pu3.bar.friend` | bank | |
| By Mail if you never came | `mail.pu3.bar` | text | |
| The certificate, the Record, the Ship app | `pu3.keepsake`, `pu3.keepsake.text`, `works.ms.senior` ({n}), `pu3.news` ({me}) | text | |
| The cake | `pu3.ptr.cake`, `pu3.cake.toast`; `flag:pu3.cake` (brennan `work`), `flag:pu3.promo.cake` (calder); kind `pu3.cake` (two friends) | text; brennan, calder; bank | |
| The toast: invite, notice, ring | `mail.pu3.toast`, `pu3.toast.notice`, `pu3.ptr.toast` | text | |
| The toast scene | meeting `pu3.toast` (cast marrow, vance, calder; one choice, 2 replies) | | |
| The framed menu; by Mail if missed | `pu3.menu`, `pu3.menu.text`; `mail.pu3.toast.missed` | text | |
| What's next; the Training tab's home line | `next.pu3.result` ({day}), `next.pu3.bar` ({time}), `next.pu3.toast`; `works.pu3.home` | text | |

### Power safety (ps, S5-1 turn 2)

Meeting `train.ps.calder` (watch-only, Deck 6 port junction; one choice of three); `works.mech.ps`, `works.ask.ps`
(`{time}` `{place}`), `next.ps`, `next.wait.ps`; the test row's `works.mech.t3`, `next.t3`, `next.wait.t3`
(`content/works/promo-t3.lines`).

### M19 Power and relays (S5-3, 24v; `content/works/m19.lines`; matched to B2's code, claude/p5s5-mech-a 3c38a65f)

| What | Keys | Placeholders |
| --- | --- | --- |
| Ladder, ask, What's next | `works.mech.m19`, `works.ask.m19`, `next.m19`, `next.wait.m19` | `{time}` `{place}` |
| Ring line, urgent notice (10:30) | `m19.ring` ({name} {time}), `m19.notice` ({name} {time} {where}: B2 passes name and time too; the words check has no `{ring}`) | |
| The training | meeting `train.m19.calder` (one choice of three); `m19.train.open` ({n}), `m19.train.test`; calder flag `train.m19.tester` (worksTeach) | |
| Job cards | `m19.card.relay` ({place}), `m19.card.batt` ({n}) | |
| A relay rack (R1-R6) | `m19.relay.ok`, `.bad` (one word each, in the lamp list), `.pick`, `.wrong`, `.test`, `.done` | |
| A battery bank (four cell pairs) | `m19.batt.ok`, `.low`, `.pick`, `.wrong`, `.test`, `.done` ({n}) | |
| Stage 2, proposed for B2's turn 2 | `m19.conduit.title` ({machine}), `.test`, `.good`, `.fault`; `m19.tester.give`, `m19.trained.stage2`, `m19.trained.stage3` | |
| The drill: you run Works' part (proposed; not in B2's code yet) | `drill.works.ptr`, `.title`, `.text`, `.call.1-3` (stations, isolate, head count; in order), `.done` ({time}), `.order`; crew kind `drill.works.answer` under `flag:drill.works.call.<n>` (`content/banks/m19.lines`, Works bank); calder flags `drill.works.you`, `drill.works.you.done` | `{time}` |

### M18 Shutdowns (S5-4, 24w; `content/works/m18.lines`)

| What | Keys | Placeholders |
| --- | --- | --- |
| Ladder, ask, What's next, ring, notice | `works.mech.m18`, `works.ask.m18`, `next.m18`, `next.wait.m18`, `m18.ptr`, `m18.notice` | `{time}` `{place}` |
| The training | meeting `train.m18.calder` (one choice of three); calder flags `train.m18.follow.feeds/hour/meal/warn/keep/book` | |
| The planning screen | `sd.tab`, `sd.none`, `sd.head`, `sd.job` ({machine}), `sd.feeds`, `sd.feeds.rooms` ({where} = the branch, {text} = its rooms), `sd.when`, `sd.prev`, `sd.next`, `sd.who`, `sd.who.none`, `sd.who.n` ({n}), `sd.meal`, `sd.class`, `sd.trad`, `sd.warn`, `sd.warned`, `sd.keep`, `sd.keep.none`, `sd.book`, `sd.cancel`, `sd.booked` ({where} {time}), `sd.cancelled`, `sd.booked.row` ({time}), `sd.busyhour`, `sd.yes`, `sd.no`, `sd.needbook` | |
| Warnings | `sd.warn.notice` ({name} {time} {where}), `sd.warn.sent` ({name}), the talk option `sd.warn.ask`; crew kind `sd.warned` (`content/banks/m18.lines`); Brennan in person: brennan `work` flag `sd.warn.brennan` | |
| 22:00 settled; the day | `mail.sd.settled` ({where} {time}), `sd.notice` ({time} {deck}), `sd.ptr` ({time}), `sd.ptr.back`, `sd.done` ({where}), `sd.missed`, `mail.sd.missed`, `m18.trained`; calder flags `sd.day.off`, `sd.day.back` | |
| The crew | kinds `sd.off` (in a fed room as it goes off), `sd.thanks` (warned, quiet hour), `sd.grumble` (a meal, a class, a tradition, or not told), `sd.lapsed` (a missed hour); Brennan's own flags `sd.grumble.brennan`, `sd.thanks.brennan` | |

### M20 The sensor array (S5-5, 24x; `content/works/m20.lines`)

| What | Keys | Placeholders |
| --- | --- | --- |
| Ladder, ask, What's next, ring, notice | `works.mech.m20`, `works.ask.m20`, `next.m20`, `next.wait.m20`, `m20.ptr`, `m20.notice` | `{time}` `{place}` |
| The training | meeting `train.m20.mori` (Mori and Calder; one choice of three); mori flags `train.m20.follow.pick/turn/module/done`; calder flag `train.m20.calder` (her one line at the end) | |
| The rig | `m20.rig.give`, `works.tool.arrayrig`, `works.tool.arrayrig.about` | |
| Pick the star | `m20.pick.title`, `m20.pick.text`; five stars `m20.star.1`-`.5` (button) and `m20.star.<n>.line` (Mori's line); show three of the five; `m20.star.yours` ({star}) if it's in your 24t log | |
| Calibrate, the module | `m20.cal.title` ({machine}), `.text`, `.far`, `.close`, `.on`; `m20.module.title` ({machine}), `.look`, `.swap`, `.done` | |
| Stages, the friendship moment | `m20.trained.stage2`, `.stage3`, `m20.sweep.done`; mori flag `m20.survey` (your readings on Survey's chart) | |

### P4, P5, P9 and the old-mysteries board (S5-6, 24k's slot; `content/works/cases.lines`)

| What | Keys | Placeholders |
| --- | --- | --- |
| P4 Which gauge is lying? | `works.mech.p4`, `next.p4`, `next.wait.p4`, `case.title.p4`, `case.p4.head`, `case.p4.gauge` ({thing} = the gauge, {word} = its reading), `case.p4.scan` ({word}), `case.p4.call` ({thing}), `case.p4.right`, `case.wrong.p4` ({thing}), `case.hint.p4.1`, `chief.p4.title/.1/.2`; torres-zeke flag `train.p4.word` | |
| P5 Follow the line | `works.mech.p5`, `next.p5`, `next.wait.p5`, `case.title.p5`, `case.p5.stop` ({machine} {word}), `case.p5.power`, `case.p5.notester`, `case.hint.p5.1`, `case.wrong.p5` ({part} {machine} {shows}), `chief.p5.title/.1/.2`; calder flag `train.p5.word` | |
| P9 The clash | `works.mech.p9`, `next.p9`, `next.wait.p9`, `case.title.p9` ({machine} {shows} {when}), `case.p9.head`, `case.p9.who` ({name} {thing} {time}), `case.p9.move`, `case.p9.moved`, `case.p9.shut` (with P5_M18), `case.hint.p9.1`, `case.wrong.p9` ({part}), `chief.p9.title/.1/.2`; calder flag `train.p9.word`; the person you ask: kind `p9.move` (`content/banks/cases5.lines`; flag `p9.move.grumble` for a reluctant yes) | |
| The board | `works.mech.mys`, `next.mys`, `next.wait.mys`, `mys.board`, `mys.board.tap`, `mys.board.none`, `mys.take`, `mys.taken`, `mys.solved`, `mys.rep`, `mys.chief` ({title} {me} {n}); five cases `mys.1`-`.5` `.title` and `.line`; torres-zeke flag `mys.word` (Day 21, by the board) | |

Placeholders: lines_check accepts only its fixed list, so the branch is `{where}`, a branch's rooms `{text}`, a gauge or
a crew routine `{thing}`, a reading `{word}`.

### Existing lines changed (spec section 10)

`content/addresses/friday-d19.address` (the Senior line no longer says Deck 2) and `friday-d26.address` (likewise).
The comet's Senior line is in the code (section 18's comet talk, `'Deck 2 has its perks...'`), so SW3 wrote its new
words as `event.comet.captain.senior` in `content/banks/event-comet.lines`; the events seat swaps the string for
`evWordAt('event.comet.captain.senior', 0) || ...`.
