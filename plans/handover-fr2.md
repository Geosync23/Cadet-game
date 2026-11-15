# Handover: FR2, the Fable review's play reviewer and fixer (for lead 52)

Written 2026-11-15 by FR2 (session_01GKuymj5amgjHqQCKPsVnFs) at about 55 to 60 percent of memory. A fresh session taking this role reads this first.

## Role, branch, builds
- Role: review 0.99.91 for design and playability (phase 1), then build the agreed bug and polish fixes behind switches (phase 2). Lead: 52 (session_01GKuymmPLvgySfNEhDYyACj). Build master: BM29 (session_01GKuymivPt7VEMWm4jUuY4G, claude/staging-fable-review). Reviewer of my fixes: RV37 (session_01GKuymo8n7x4hGZtoPmWXqX). The other reviewer, code and performance: FR1 (session_01GKuymmYzraWXg9ELUMmqri, claude/fable-review-code).
- Branch: `claude/fable-review-play`, from main cdd9efd (0.99.91, game b321a4ec...95f3). Head 3f73b6b plus this note; game 77a3fc96...63b8 with all switches off. The build number is untouched.
- main does not move. The fixes go into a separate review version on its own link, switched on by the build master.

## What exists
- `plans/review-fable-play.md`: the review (16 findings, the fix list F1-F12, nine design questions for the user with recommendations, space for answers). Screenshots: `plans/review-fable-shots/`; before/after pictures of the fixes: its `fixes/` folder.
- Twelve switches, each `var FRP_..._ON = false;` in the slot of the section it changes. The table, the shared functions touched and what was left unbuilt are in DEV_NOTES, "The Fable review's playability fixes". Rows are in `plans/build-table.md` ("fable-review F1" to "F12", and "F4 fix").
- `frp_check.py`: one part per fix, off and on (line food tray pin lead thanks words say panels label blink tips). It makes its switched-on copies from the exact text `var NAME = false;`.
- Tools I used for playing: `plans/review-fable-probes/` (fw.py the arrow-only walker with logs, drv.py and c.py an interactive phone-size session over a socket, ed.py exact-string edits that must match once, walk-days0-9.json the nine-day log).

## Results at handover
- check_fast OK, lines_check PASS, names_check OK on 3f73b6b. cadet_test off vs 0.99.91 ALL IDENTICAL on 748eec0 (same code; one bank line was shortened after). frp_check all parts OK. interactions_check with all twelve on OK. bubble, arrows pointer/d/f, arrows_check clockin and shift OK with F1-F5 on.
- Not a result: controller_check with the switches on ran out of time twice on a loaded machine (no FAIL line). The full six-runner round has not been run on this work.

## Loose ends
1. RV37's review of the diff: answer its questions; small fixes go on this branch with a build-table row and frp_check.
2. frp_check runs on a switched-on build too (it sets each part's switch off and on itself). BM29's all-on rehearsal finds (lines_check, device_check under FRP_PANELS_ON, the label's restyle) are fixed: see the build table's last fable-review row.
3. Not built on purpose (say so if asked): a panel closing an already-open person's card (section 20's owner); Mum's "Second time's easier" on a later call, Theo's "Pip suits you" before the pip, Tomas's evening greeting at dawn (the dialogue owner's line conditions); thank-you Mails in each host's voice (the writer's); the Last Light's last pop-up ending on a need read-out.
4. The nine design questions are the user's. If answered, record the answers in the review file and in design-doc.md with the work that follows.
5. The review did not cover Sim night, the stories, the storm, the later promotions, the ending, sound or the controller. A second play pass after week 2 would be worth doing.

## Gotchas
- The game file is 8.8 MB: never read it whole. Find lines with grep, edit with `plans/review-fable-probes/ed.py FILE EDITS.json` (each old string must match exactly once).
- A `var` switch is used because code earlier in the file asks for it; helpers like `frpWords()` guard with typeof.
- Bank lines are at most 90 characters (lines_check, which is not in check_fast). Run it after any words change, then `python3 content_gen.py`.
- Setup in a fresh container: `pip install playwright numpy pillow`; three r128 and acorn 8.12.1 by `npm pack` into /tmp/cadet-work; `CADET_CHROME=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`. Four cores only: more than two browser checks at once makes page loads and clicks time out (that is what happened to cadet_test once and controller_check twice).
- Tips, toasts and heads-ups close on real-time timers; under a stepped clock they stay up, so judge overlap, not duration.
- On the arrival nothing outside the Tern can be walked to for a ship minute or two (the ramp).
- F4 keeps FX3's rule: a tap on a person's own body away from the pin's point is theirs.

## How to test
`python3 frp_check.py starship-cadet.html [part ...]`, `bash check_fast.sh`, `python3 lines_check.py`, `python3 cadet_test.py /path/0.99.91.html starship-cadet.html` (ALL IDENTICAL with the switches off), and with a switched-on copy: interactions_check, bubble_check, controller_check, the arrows checks.

## Open questions for the user
The nine at the end of `plans/review-fable-play.md` (Day 1's board, meals in the week 1 arrow, work before clocking in, pay, a day's work, reputation's pace, the first promotion's day, the device's apps, a richer mechanic earlier in week 1).
