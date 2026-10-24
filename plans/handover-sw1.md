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

## Loose ends

None open. If the user asks for changes after reading, edit only the four .arc files, rerun the checks above, push
and send the sha to CS1 (copy LEAD 32).
