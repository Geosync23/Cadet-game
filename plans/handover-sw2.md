# Handover: SW2 (story writer 2)

**Role:** story writer under LEAD 32, editor CS1 (session_01QcPAXHjQZ2HfZKMCTbaW9v). SW2 was session_017dLaLFBnRUQin3PQEQq6so.
**Branch:** `claude/stories-sw2`, from claude/integration 364c80cb (game 0.92.2). Content only: the game file is
untouched and nothing is baked (that waits for the user).

## What I wrote (all three passed by CS1, 2026-10-24)

| File | Story | Beats |
| --- | --- | --- |
| `content/arcs/teague.arc` | Theo Teague, "The last page" (outline C) | 1-4; 5 crescendo at his send-off, shuttle bay, Day 21 14:30; 6 quiet ending (page on your bunk, Mail from the Heron) |
| `content/arcs/halloran.arc` | Emeka Halloran, "Groaning means breathing" (outline G) | 1-4; 5 crescendo at breakfast from Day 15 (joke 289, "Hull-o"); 6 quiet ending (Yoon ran it); 7 afterglow (Mum's 413, the scone tin) |
| `content/voices/bramwell-basil.voice` | Basil Bramwell's voice card (CS1's call) | |
| `content/arcs/bramwell.arc` | Basil Bramwell, "Your turn" (outline F) | 1-3; 4 crescendo at his new hand's tea, Day 25; 5 quiet ending |

Commits: Theo 1d8e7632, Halloran 3425f821 (and Theo's comments moved to the IF/FAVOUR form), Basil c68b9317, Theo's
fix 38b41a2f ("checked twice" removed).

## Notes for whoever builds or edits these

- Lines the grammar can't express are comments, in CS1's form (outlines.md, the shared rules): `// IF <cond>: <speaker>: <text>`,
  `// DAY:`, `// FAVOUR <id> (new): ...`, `// CRESCENDO rides on: ...`, `// QUIET ENDING for beat N`, `// optional: if present`.
- Flags I invented for the builders: `halloran.jokes` (chosen) / `halloran.jokes.done` (favour emekaJokes done; picks
  Yoon/Lemaire/Yilmaz or Pell/Kovac/Zeke in the crescendo); `bramwell.plant` / `bramwell.plant.done` (favour
  basilPlant; the crescendo needs done, else the quiet ending).
- Quiet endings use `beat=<arc>.<n>` (exactly n told) so they can't follow a told crescendo; Halloran's afterglow uses
  `beat:halloran.5`, true after either the crescendo or its quiet ending.
- Gates are lowered for the windows (Theo Days 3-21, Basil 21-30); see each beat's tier/metDays/gapDays.
- Halloran's mum says "the kitchen's too still" (not "the house is quiet", which is the player's Mum's). CS1 agreed.
- Roster lines that clash with the stories (Halloran's illness line, Theo's transfer-list and stay/go lines) are in
  CS1's plans/crew-stories-build-notes.md with replacement words.
- "Heron" is canon in facts.md on claude/crew-stories-pitch 70ee2243; the name warning goes once that's merged.

## How to check

Plain `lines_check.py` fails on a content-only branch ("baked blocks out of date"). Copy the game to a scratch folder,
`python3 content_gen.py <copy>`, then `python3 lines_check.py <copy>`: PASS, with no "the same line is also in" warnings
for these files. Lines in `// IF` comments aren't seen by the checker: check them by hand (140 characters, voice, repeats).

## Open

Nothing. Waiting in case the user has changes after reading.
