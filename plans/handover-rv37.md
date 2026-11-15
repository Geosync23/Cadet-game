# Handover: RV37 (reviewer of the Fable review's fixes; lead 52)

Session session_01GKuymo8n7x4hGZtoPmWXqX. Branch claude/review-rv37 (from FR1's 05adee4): notes plans/review-rv37.md,
probes plans/rv37-probes/. Never edits the game. Written 2026-11-15 at about half of memory.

## Verdicts sent (to lead 52; final ones also to BM29)
- FR1 (claude/fable-review-code): **PASS at a077808** (game off 923b6c64...1c5d): A1-A8, A12, A4 and tools/one_byte.py.
  History: 05adee4 A1 A2 A3 FIXES NEEDED; 1155555 A2 (Throw it away) and A3 (a quiet old part) open; a077808 all closed.
  A9 TEX_READ_ON was not reviewed on (briefed: stays off).
- FR2 (claude/fable-review-play): F1-F11 PASS at 8094ac2 (game off 085256a4...4fdd). **F12 open**: "The bridge data
  bus are running" (frpPlural), and the Calendar button becomes "Don't remind me" (lead 52). The unswitched quiz
  line ("rec dec" to "rec deck") is accepted by lead 52. Waiting for FR2's fix commit.

## Loose end for whoever takes this
When FR2 pushes the F12 fix: read `git diff 8094ac2 <new head> -- starship-cadet.html`; from a checkout of that head
run `python3 <path>/plans/rv37-probes/rv37_frp_probe.py starship-cadet.html words` (the plural list must not hold
"Bridge data bus"), check the game's sha256 with switches off, and that cadet_test old vs new off is ALL IDENTICAL
(or take FR2's run if usage is tight). Send the final verdict with the exact commit to lead 52 and BM29
(session_01GKuymivPt7VEMWm4jUuY4G).

## Probes
- rv37_probe.py GAME.html [loop keep tell tab memo walls load lib]: FR1's fixes; run from this branch's folder (it
  uses robust_check.py's kit from the repository root). It switches the nine on itself. RV_TELL1=none: tell 1 only.
- rv37_frp_probe.py GAME.html [pin pad words food needs]: FR2's fixes; run from a checkout of FR2's branch (it uses
  frp_check.py's and arrows_check.py's kit from the current folder). food and needs take about ten minutes each.

## Gotchas
- Kit: pip install playwright; three r128 and acorn 8.12.1 by npm pack into /tmp/cadet-work; CADET_CHROME=
  /opt/pw-browsers/chromium; a CADET_WORK of its own for each run at once.
- Four cores: more than three browser runs at once gave title_check four false controller failures and cadet_test a
  few pixels one level off. Rerun alone before believing either.
- FR2's switches are `var NAME = false;`, FR1's are `const NAME = false;` (LIB_SAY_ON is in the page's first script).
- Under a stepped clock pop-ups never close by themselves; one left open holds every later warning back (my nine-day
  Food run shows no warning on Day 4 for that reason).
- The save holds ship.career.gs, which differs between two runs of the same build: leave it out when comparing saves.
- "Load a save file" into the slot being played sometimes came back as the old game in my rig, on 0.99.91 too
  (section 7 of the notes; lead 52 carries the backlog line).

## Open questions for the user
None from this seat.
