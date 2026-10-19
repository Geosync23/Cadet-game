# Handover: Pillar 5 seat H2, head-scratchers (Step 3: the T2 band, P1, P2)

Written 2026-10-19 by seat H2 (session_01SixL3TcPYoHEP1DPv8cBRZ), who succeeded seat H. Read CLAUDE.md, the Step 3 brief
(`git show origin/claude/lead-pillar1:plans/brief-p5s3.md`), `plans/handover-puzzles.md` (seat H's note: the engine,
the scanner, P3, the gotchas, all still true), then this. Pages: `git show origin/claude/p5-design:plans/mechanics/<page>.html`
for case-engine (#t2), p1-when-does-it-happen, p2-who-saw-what, fault-tables (Tier 2).

## Role, branch, builds

- **Seat H2**, branch `claude/mech-cases`, builds **0.55.13-0.55.16** on base 0.63.2r (`claude/ship-integration` 898d58d).
  Lead 16 session_01UMyfd16GqSdgNyz5PE8qSv (was 14, 15); build master BM6 session_01F8k6hqdBRoxDJMzqAuiHqR; reviewer R3
  session_01AR6tGFiSZF7hL1LfVpWgng (0.55.13 PASS); writer W2 session_01866TWKzGRgZmFcxiYRi4db; S2 session_01Wiqm2pAvvyJYGQyUgbsfXY;
  C2 session_014yREkgPvuwMyxBtoqB1P14; M3 session_01WJczDg7E7y1jR96aCMbNew.
- **Hash keys (lead 14):** 1000 P1's busiest hours on ties, 1001 P2's witness order, 1002 P3's wrong-size note, 894 P2's
  mix-up; 1003-1004 spare. (892 and 893 were already the engine's: the P1/P2 pages' keys were moved.)
- **Reserve slots:** 21 P1's first case, 22 P2's first (20 is P3's and C2's test job, 11 M3's m9).
- Merged in: S2's 5cc7646 (0.33.56, the Tier 2 fault tables). Not merged: C2's 0.44.22 (rows p1/p2, `said` in worksClean),
  M3's tracing, S2's MACHINE_LINKS (not out yet). They meet on the build master's combine.

## What H2 built (all in 24k unless said)

- **0.55.13 the T2 band:** `CASE_SPENT` (seal, cartridge, filter, membrane, oxygen cell, uv lamp: a wrong call on a Tier 2
  job uses it up; "The seal is used up." `case.wrong.t2`); `caseBandOf(kind, band)` (a kind's own `bands`, else
  `CASE_BANDS`); P3 keeps T1's size as an Officer (no machine has 4 part causes with one card) and half the time (1002) one
  note that rules out less than it seems (`src.odd`: a suspect's part in the wrong size, kills nothing, takes no stock,
  `fault.tried.odd`); `caseTalker` (talk it through: Torres when on, else Calder, Halloran) as `c.by`.
- **0.55.14 P1:** `CASE_KINDS.p1` (see the 0.55.14 DEV_NOTES row and the block's header comment). Suspects `'machine:cause'`
  (`caseSusAt`); `caseLog(id, d)` 24 digits from MACH_HIST; decoys only where the log is fine (`caseLogFine`, 80%+ every
  hour); roll cases put a same-`when` decoy first (lead 16). Engine additions: a kind's `title`, `card` (`caseCard`),
  `start` and calls (`caseAt`), `wrong` (the wrong-fit line), `noScan`; `caseSus` asks the kind first. Device block
  `strip` + `devStrip(rows, fallback)` in section 19 (CSS `.device .strip`, `.st-*`). `p1Stage`: 3-pump-1, from 16:00
  Day 11, or (build with an m9 row) once m9 is trained (M3's ask, 0.55.16). Stand-in line `P1_LINES.water` until
  `MACHINE_LINKS`; `caseLine(id, line)` reads MACHINE_LINKS[line] as an array of ids or `{ ids | machines | order }`.
  Chief's notes show non-case pages with their own `open()` (M3's tracing page).
- **0.55.15 P2:** `CASE_KINDS.p2` (see the 0.55.15 row). `caseRoomsNear` (rooms touching on the deck map), `caseDoor`
  (the machine room's door went within 5 minutes, from the plans), `caseShows(m, f, t)`, `p2Seen`, `p2Witnesses`, the
  mix-up (same kind, else same system, another deck, when the real one was quiet), `p2ShowAt` (roll cases wait 12 h to a
  shift minute; their window read from the plans at posting), `p2Line` (lineFor with `peek` and the clue's minute, so
  the same words every time; `{place}` with its article), the chat card (`caseAskButton`, `caseAskSay`; section 20's two
  lines), `p2Word` (Tomas or Torres eating in the room you're in, from the day the p2 row opens) → `p2Said1` sets
  `SHIP.works.said.p2` and `cases.said.p2`, then `p2ShowFirst`. `CASE_KINDS.p2.open()` is false until then (the user's gate).
- **0.55.16:** the section 17 hooks (jobCard → caseCard; jobStopsBase → caseAt), S2's tables merged, P1 after m9.

## Shared formats

- P1 clue: `{ id: 'l0', type: 'log', src: { m, log: '9999…' (24 digits), d }, at: panel place, kills: ['m:cause'] }`.
- P2 clue: `{ id: 'w0' | 'x0', type: 'person', src: { ask, t, saw: 0|1, door: 0|1, pl, mix? }, at: null, kills }`.
- `SHIP.works.cases` gains `p1`, `p2` (first cases' ids or 'none'), `said: { p2 }`, and a case's `doubt` (only when used).
  A waiting P2 first case is saved with no clues (caseClean allows it for that one).
- Writer keys read: `case.title.p1|p2`, `case.line.<line>[.shows]`, `case.when.<evening|morning|peak|night|after>`,
  `case.strip.title|fine|low|allday|head`, `case.wrong.p1|t2`, `case.hint.p1.1|p2.1`, `case.p2.head`, `case.ask`,
  `case.ask.none`, `chief.p1.1-2`, `chief.p2.1-2`, `fault.tried.odd`, `train.p1.word` / `train.p2.word` (voice flags),
  `ask.saw.still|door`, `ask.quiet.still|door`, `ask.mixup` (content/cases/p2.lines, read with lineFor). W2 has them all
  (claude/writer-p5 0cdde89).

## Loose ends

- **MACHINE_LINKS** (S2) not out yet: P1 has only the stand-in water line (4 machines), so a badly running machine on it
  leaves too few decoys and the fault stays a plain repair; heat and air lines get P1 cases once MACHINE_LINKS is in.
  Check `caseLine` against its real shape.
- The device's old Jobs section (section 17's `jobsSection`) still says the room of a P1 case's own machine; the board
  card and the arrow don't. Ask S2 for a caseCard check there too if it matters.
- C2's 0.44.22 adds rows p1/p2 and keeps `said`: my `CAREER_LADDER.push` only runs if the row is missing, and the
  `cases.said` copy is harmless; it can go once the combine has C2's cleaner.
- Not built (judgement calls, told to the lead): P3's night-shift handover log (T2 form); P1's T2+ forms (two machines on
  one junction, the logger); P2's T2+ forms (another shift, two decks).
- The P3 talk-it-through toast still names `c.by` with `.split(' ')[0]` (Calder's name is "Chief Calder"?): check the words.

## Gotchas

- Clue honesty is the contract: P1 decoys must really have run fine (the test checks every digit against MACH_HIST);
  P2 witnesses must really be there (planWhere) and say what the cause's `when` really did then. Any new rule for what
  "shows" means goes in `caseShows`/`caseWhenHours` so both kinds stay consistent.
- `planDay` is read for future days at posting (P2's roll window); an appointment made later can change a plan, so a
  rare witness may not "really" be there by then. puzzle_check checks at posting.
- `caseWhenHours('peak')` uses the kind's use counter: water's busiest hours include mornings, so a roll P1 card often
  says "at the busy hours"; the first case is forced to the evening (P1_FIRST.hours).
- Two P2 scripted checks need the player standing in Tomas's breakfast room: puzzle_check moves the player there
  (`goToDeck`, `placeSpot`); the meal is 08:29 on Day 15 in a new game (Mess, Deck 3).

## How to test

```
pip install playwright; mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
export CADET_CHROME=/opt/pw-browsers/chromium
python3 puzzle_check.py BUILD.html        # ~4 min; prints stand-ins and hooks it found
python3 cadet_test.py OLD.html NEW.html    # ALL IDENTICAL on this branch (nothing drawn)
python3 device_check.py / social_check.py / machine_check.py / intro_check.py BUILD.html   # sections 19 / 20 / 17
```

## Open questions for the user

None from seat H2.
