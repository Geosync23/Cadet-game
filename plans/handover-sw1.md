# Handover: SW1 (story writer)

**Role:** story writer under LEAD 32; story lead and editor CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v). Session
session_01Mjn7ezXqrDgXBrdCtddHHJ. Branch `claude/stories-sw1`, from claude/integration 364c80cb (game 0.92.2).
Writing only: no game change, no baking.

## What I own and wrote (all CS1 PASS, 2026-10-24)

From the outlines in content/arcs/outlines.md, "Crew stories (2026-10-24): the ten" (CS1's file, on
claude/crew-stories-pitch):

| Story | File | Kept | New |
| --- | --- | --- | --- |
| A Pell | `content/arcs/pell.arc` | beats 5-6 | 7 crescendo (the practical at the Wednesday open-door tea), 8 quiet ending (Mail "PASSED"), 9 afterglow (the call home, the music box) |
| B Zeke | `content/arcs/torres.arc` | beats 1-3, Calder's beat 5 lines | 4 rewritten ("Forty years": his dad is well and retiring), 5 new letter question and Mail, 6 crescendo (Knit and natter, the scarf, his dad's line read twice), 7 quiet ending |
| D Calder | `content/arcs/calder.arc` | beats 1-4; the old 5 word for word as the quiet ending (beat 6) | 5 crescendo ("Well done." in front of Works, Day 26, just before her question), 7 afterglow (the toolbox on your bench, no "well done") |
| E Kovac | `content/arcs/kovac.arc` | beats 1-3 | 4 crescendo (the Deck 5 lift lobby before the Friday address), 5 quiet ending (Mail), 6 afterglow (the knitted spanner grip) |

Final sha: see `git log claude/stories-sw1`. The last reviewed content commit is 12bf522e. Only the four .arc
files differ from 364c80cb. Kovac's joy line in content/lines/kovac-zainab.lines (the spanner grip, gated on
`mem:moment.kovac.grip`) lives on CS1's branch (43d9482f), not here.

## Conventions used (agreed with CS1, now in outlines.md's shared rules)

- **Lines that only play sometimes** are comments: `// IF <conditions>: <speaker>: <text>`. lines_check skips
  them, so they're checked by hand. They're used for Zeke at Pell's practical, Pell's "you timed me" and "the lad
  was your idea" lines, Zeke's Engine Specialist line, Calder's "one true sentence", and Kovac's Keane lines and
  brake count.
- **Crescendo and quiet-ending comments** sit under `== beat N` in CS1's form, as notes for the builders.
- **New story flags:** `kovac.rode` (set at Kovac's crescendo or her quiet ending; the afterglow needs it).
  `pell.certified` is set by both Pell 7 and Pell 8; Pell 9 needs it.
- **Memory words kept** so existing callbacks in pell.lines, calder.lines and kovac-zainab.lines still fire
  (knew/glad/why/shared; lookafter/onlyone/thanked; fourplease/proud/again). Kovac's old `tellclub` callback no
  longer fires; CS1 noted it as harmless in plans/crew-stories-build-notes.md.

## Gotchas

- **lines_check on a content-only branch** always FAILs with "baked blocks out of date". Check against a scratch
  copy instead:
  `cp starship-cadet.html $SCRATCH/game.html && python3 content_gen.py $SCRATCH/game.html && python3 lines_check.py $SCRATCH/game.html`.
  It should PASS with the same 50 old warnings.
- **lines_check only catches exact repeats.** Grep every new phrase across content/ by hand. Echoes caught and
  reworded this way: "Nine minutes forty" (Volkov), "Ten more minutes with the coils", "Don't tell Brennan",
  "Board's at fourteen", "the right answer", "Go on, then" (Pell's word), "checked twice". Also check other writers'
  crescendos for the same beat: Pell's shaking-hands line clashed with Salo's.
- **Never name a deck by number on screen** (say "the rec deck", not "Seven").
- **The secret biscuit tins are canon** (Ibarra's and Soto's; Pell has told no one): don't give anyone else a tin.

## Second job: Talk a while for main characters (patch 0.92.3 item 15, CS1 PASS at 01293d50)

From plans/talk-main-plan.md (on claude/crew-stories-pitch), in FX13's agreed format: `only: own` before the first
talk; each person's 4 old talks kept and 26 new ones added (10 with no tier gate, then about 7 acquaintance, 6
colleague, 4 friend, 3 close); no small/done blocks (the engine repeats their own talks when the pool runs out). Files:
`content/talkpack/pell.talk`, `torres-zeke.talk`, `calder.talk`, `nandakumar.talk`, and their own card frames at the
end of `content/lines/<id>.lines` (talk.start 5, two behind tier>=friend; sit 3; filler 6; end 5; stop 3;
talk.go.shift/bed/trad 2 each). Calder's colleague tier and above also need rep:known or rep:well. Nandakumar: never anyone's
medical details, her burnout only hinted at close, Rina's exam left out.

- **lines_check needs FX13's reader** (claude/p923-fx13) for `only: own`: check in a worktree of that branch with
  these files copied in, bake, then run lines_check. Integration's reader rejects the line until FX13 is merged.
- **CS1's duplicate checker:** `tools/near_dupes.py` (on claude/crew-stories-pitch): `python3 near_dupes.py HEAD <file>`
  after committing. Aim for 0 EXACT and 0 NEAR. All 8 files are clean.

## Later jobs (2026-10-24/25), all pushed

- **Weekend traditions pitch** (0.92.5 item 16): plans/weekend-traditions-pitch.html on claude/weekend-pitch cbaac1db,
  artifact https://claude.ai/artifact/C43EjSi7MJXUq9jz6yx5Sn (answers in its db at answers/user; a "Since your
  answers" box lists the changes after the user answered).
- **Weekend tradition words** (CS1 PASS): claude/weekend-words-sw1 8d2e66b0. The == sections of saturday-run,
  every-song, night-owls-cocoa (host Mensah), gerald-clinic, sunday-story (21:15), garden-picnic, bread-day and
  big-jigsaw (host Raman); join.lines; content/banks/sunday-story.lines (story.sunday.1-4, Holt reads in order).
  Everything is worded for a 4-week rotation, so nothing says "every week". The decor tap texts sent to FX16 are
  cocoaPot (FX16's) and picnicBasket ("Brown paper parcels in a basket, still warm from the galley. Brennan has tucked a
  bit of garden basil under each knot.").
- **Appointments pitch** (0.92.6 item 9, CS1 PASS): plans/appointments-pitch.html on claude/appointments-pitch
  52dd1cc1. PUB1 publishes it (capabilities {db:{}}).
- **Promotion words for FX19** (0.92.6 items 18/14/11): content/works/promo-sight.lines on claude/promo-words-sw1
  0ba7c452. All 14 keys are as FX19 named them, and the Mails stay at 90 characters (lines_check caps these keys). CS1's
  glance is pending. Flagged to CS1: step3.lines promo.mail ends "Well done." (it breaks Calder's arc rule).

## NOT STARTED: FX17's word list (0.92.6, behind P926_TRADS), handed over at 70% memory

FX17 (session_01YKeSjUhEnJRbmjyHz2aa6u) sent the list on 2026-10-25 ~05:07 UTC. Items, in FX17's build order:
1. Item 13: spoken talk scripts, 8-12 bubble lines (90 characters or fewer) each, as MEETING_SCRIPTS `talk.<speaker>`,
   like talk.sato. Chiefs' talks: Day 32 Holt "The oldest log in the Watch office", Day 46 Ferreira "Messages that
   came home late", Days 60 and 74 the writer's pick. Wren talks (Mondays from Day 32): Day 36 Volkov "How the float room
   floats", Day 39 Zeke "How a drive coil sings", Day 43 Brennan "A spice for every port", then Days 50, 57, 64, 71
   and 78 (+ Thursdays 53/67/81 optional): the writer's speakers and titles.
2. Item 5: One week aboard, Zeke's sit-down card week1.zeke.* (open; jobs/jobs.none; trad/trad.none;
   friend/friend.none; meals.good/meals.missed; late/late.none; 3 replies with answers; close) + join.one-week-aboard.*.
3. Item 2: the swap meet (host Orla Ishikawa): join.market.*, swap.open, swap.thing.1-3 (6-9 to rotate),
   swap.reply.1-3, swap.after.1-3, swap.stall (~6), swap.browse (~8).
4. Item 15: Spice shelf supper: spice.jars (12: owner id, spice, 3-6 word note), spice.open, spice.jar (~12),
   spice.guess (~10), spice.reveal (~4), spice.mine (~8), spice.ask/right/wrong.
5. Item 4: Reading corner (host Esme Walsh): reading.welcome/wrap, reading.titles (~12 invented),
   reading.book (~20, {title}), reading.reply (~8), join.reading-corner.*.
6. Item 3: optional wso.cheer (4-6).
7. Item 7(a): 8 new .trad files, weeks 5-12, each every 8 weeks (k left blank): W5 Mon 17:45 Works hands-on (no
   repairs: Mend-it is cut); W6 Wed 19:30 chart room, Survey or Helm; W7 Sat 11:45 a quiet room (observatory or Deck 1
   observation room); W8 Thu 17:15 a department's open space (2-3 departments); W9 Sun 08:45 garden or promenade; W10
   Mon 17:45 music in the junior common room; W11 Wed 19:30 a making evening; W12 Thu 17:15 a big laugh, 20+ people.
8. Item 7(c): Six weeks aboard (Day 42) and Twelve weeks aboard (Day 84, a toast in the mess) .trad words.

## Loose ends

None open. If the user asks for changes after reading, edit only the four .arc files, rerun the checks above, push
and send the sha to CS1 (copy LEAD 32).
