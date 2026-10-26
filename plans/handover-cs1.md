# Handover: CS1 (crew stories lead and words checker)

Written 2026-10-26 by CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v) at about 50% memory, for a fresh CS1. Lead: lead 37
(session_019GcNZ4GGEqfiuYDYnue7nX). Read CLAUDE.md, then this.

## Role
- Words owner for the **crew stories** (`content/stories/`), and the team's **words checker**: every writer's new lines
  (traditions, talks, appointments, jobs, Mail) come to CS1 for voice, canon and no-repeats before they're merged.
- Plain-language plan pages for the user when the lead asks (pitch pages with a saved answers form).
- Only push to **claude/crew-stories-pitch** (this session's rule). For other branches: put a single, self-contained commit
  on this branch and tell the build master to cherry-pick it (done for design-doc ae4d60de).

## Branch and what's on it
- `content/stories/*.arc`: the six crew stories (Pell, Theo/teague, Basil/bramwell, Halloran, Kovac, Saad/salo) and
  `bramwell-basil.voice`; switched on in 0.92.6 (`STORIES_ON`). `content/stories/waiting/*.story` (not baked): Zeke/torres,
  Calder, Raman, Kowalczyk, waiting for career steps. Every story file matches claude/integration except
  `bramwell.arc` (abe48f47: Basil 4 is now a welcome dinner in the mess on Day 25, because the crew welcome tea is
  retired; agreed with FX22b, who builds the event swap on claude/event-swap).
- `content/arcs/outlines.md` ("Crew stories" outlines A-J), `content/facts.md` (story canon rows),
  `plans/crew-stories-build-notes.md`, `plans/crew-stories-pitch.html`, `plans/crew-stories-read.html`,
  `plans/talk-main-plan.md`, `tools/near_dupes.py`.
- Plan pages: `plans/trad-variety-pitch.html` (round 1), `plans/trad-variety-pitch-2.html` (round 2, 22 ideas).
- `plans/trad-0932-words.txt` (efb4c610): words for the 14 new traditions and Brennan's reworked tasting table, sent to
  FX24 (session_017zuWxNJfppnVwkQDtiwnb6, claude/trad-0932). FX24 may ask for a different shape: reshape on request.

## The stories' grammar (FX21's, documented in content/README.md)
`if <conds> | who: text` per line; conditions `here:<crewId>`, `day:21 / 3-21 / 15- / -20 / 19,26`; beat fields
`crescendo:` (trad:<id> | event:<id> | farewell | meal:breakfast|dinner), `quiet:`, `follows: a|b`, `lead:`, `title:`,
`invite:` (Mail the evening before, `{at}` = the booked time), `cast:`. A crescendo's people go to its gathering if
free (planner hook A). A step whose day window passes without a quiet ending of its own is skipped.

## How to check words
- Duplicates: `python3 tools/near_dupes.py <branch> <file of "- " lines>` (exact plus 0.82 near-matches against content/).
- Bake on a scratch worktree of the target branch: `git worktree add --detach <dir> <branch>`, copy the files in,
  `python3 content_gen.py` then `python3 lines_check.py` (expect PASS; warnings are normal), remove the worktree.
- Canon: `content/facts.md` (roster table, hobby clusters, canon rows), `content/voices/<id>.voice` (talk, avoid),
  the stories' secrets (Halloran's jokes are his late dad's numbered book; Raman's near miss; Holt and the Veyli; Tomas's
  Watch exam; Marrow's daughter; Sato never admits the third comet matters; Mori never compared to Sato; Calder says
  no "well done" before her story's payoff). Hesper Dock is Brennan's arc place; Theo leaves on Day 21; Alvarez and
  Moreau leave on Day 77.

## Loose ends
- Three Calder "well done" lines before her payoff, reported to lead 35 (step3.lines promo.mail, promo.ceremony.meet,
  one-week-aboard.trad Mail): check they were fixed.
- design-doc.md "Crew stories" says Basil's scene is at the welcome tea: it should now say a welcome dinner in the mess
  (told lead 37).
- Kovac's joy line (the spanner grip) is a comment in kovac.arc beat 6, to add to kovac-zainab.lines: check it went in
  at switch-on.
- Stage 2 stories (waiting/) need: Zeke's Engine Specialist day, Calder's question Day 26, Raman's comet (now Friday
  Day 26, 21:30; Bakshi's night helm rota to check), Kowalczyk's night shift (the user chose Days 19-20, so her story's
  Days 22-24 and its Day 24 05:50 crescendo must be rewritten).
- The user's tradition decisions: round 1 noes (comics wall, hum night, Sato's tea, map night, paper boats, newsletter,
  learn a dance, cranes) and round 2 noes (dawn chorus, cart derby, gallery evening, lost property, lunch quiz, tiny
  portraits, soup, star journals) are parked: never reuse their names. Valo post day was left blank.
