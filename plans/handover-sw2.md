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

## Second job: Talk a while pools (patch 0.92.3 item 15, CS1 passed 905ec5f1)

- `content/talkpack/{tomas,rina,brennan,sato}.talk`: TW1's four talks kept, `only: own` before the first `==`, 26 new
  each (11 with no tier gate, then acquaintance, 7 colleague, 4 friend, 3 close). Story secrets kept out (Tomas's exam,
  Rina's exam and Gran before beat rina.4, Brennan's fire/Nell/sage/book, Sato's lucky survey and third comet).
  Brennan's TW1 `pans` talk had one line changed at CS1's request (cook-by-ear half cut; id kept).
- Their own card frames in `content/lines/<id>.lines`: talk.start (5, 2 behind tier>=friend), sit 3, filler 6, end 5,
  stop 3, go.shift/bed/trad 2 each.
- Checking: the current .talk reader rejects `only:` until FX13's change; check on a scratch copy with that line
  stripped. Run CS1's `tools/near_dupes.py <branch> <file>` (claude/crew-stories-pitch) on every file: zero EXACT.

## Later small jobs (all done)

- **Name on the beam explain** (0.92.3 item 13): `content/banks/join.lines` `join.name-on-the-beam.explain`, 4 Zeke
  bubbles; final 4533c325 (with bf1496ff, 2bd054f3). CS1 PASS.
- **Inspection walk** (0.93.2, FX20): new `content/works/inspect-walk.lines` (room.b-h, arrive, away, done); commits
  c4567bf6, 197630c4, e4cf8a68. CS1 FINAL PASS. Bunk residents: content/facts.md lines 84-92.
- **Promo beats polish** (FX28): branch `claude/sw2-promo-polish` 62fa4f3f, 9689b966 (on claude/promo-beats bd558a8).
- **Comet polish** (FX25): `claude/sw2-comet-polish` c8897265; FX25 took it into claude/comet 157d1cfb.
- **Swap fix**: Day 26 "three days of guests", plus both Friday Mail headers made swap-safe (they're single lines,
  read in both modes): `claude/sw2-swap-fix-0933` from staging-0.93.3 d9c7e5f0 (sha in the last message to lead 39).
  The old parked copy is `claude/sw2-swap-fix` 39ab4fef (superseded).

## Not started: handed back

- **"A Veyli vessel needs help"** words (lead 39; plans/veyli-vessel-spec.html section 8 on claude/p5-specs e9f0962c;
  ~200 lines; branch claude/vessel-words from claude/staging-0.93.3; builders VB1 session_01UsjGN26E88zwrNPWwef4iT,
  VB2 session_01KRBGtugjBpv5iGcV5WDvCP). Handed back at 59% memory for a fresh writer.

## Setting up the checks in a fresh container (what worked)

- `pip install playwright` (numpy and pillow were there; the browser is /opt/pw-browsers/chromium:
  `export CADET_CHROME=/opt/pw-browsers/chromium`).
- `npm pack` was very slow through the proxy; this worked: `mkdir -p /tmp/cadet-work/{three,acorn,test}`, then
  `curl -sS -o acorn.tgz https://registry.npmjs.org/acorn/-/acorn-8.12.1.tgz && tar xzf acorn.tgz` in acorn/, and
  `npm pack three@0.128.0` left in the background (it finished in a few minutes; cdnjs was refused by the proxy).
- check_fast ~5 minutes; fridays_check needs well over 5 minutes here (give it 15). Use a separate CADET_WORK when two
  browser checks run at once.
- Working on someone else's branch: `git worktree add -b <my-branch> <scratch>/x <their-sha>`, edit, re-bake there,
  push my branch, and send them the commit to cherry-pick. Never push to their branch unless the lead says so.
- CS1's duplicate checker: `git show origin/claude/crew-stories-pitch:tools/near_dupes.py > <scratch>/near_dupes.py`,
  then `python3 <scratch>/near_dupes.py HEAD <file>` after committing. Aim for zero EXACT; look at every NEAR.

## Open

Nothing. Waiting in case the user has changes after reading.
