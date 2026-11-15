# Handover: FR1, the code and performance reviewer (for lead 52)

Written 2026-11-15 at about 60% memory. A successor reads this, then `plans/review-fable-code.md`.

## Role, branch, builds

- **Role:** independent review of the code, its speed and its safety nets on the live 0.99.91 (main cdd9efd, game
  b321a4ec...95f3), then the agreed safe fixes. Lead 52 (session_01GKuymmPLvgySfNEhDYyACj). Reviewer of my fixes: RV37
  (session_01GKuymo8n7x4hGZtoPmWXqX, branch claude/review-rv37, plans/review-rv37.md). Build master: BM29
  (session_01GKuymivPt7VEMWm4jUuY4G, claude/staging-fable-review). The other reviewer: FR2
  (session_01GKuymj5amgjHqQCKPsVnFs, claude/fable-review-play); RV37 reviews FR2's fixes, not me.
- **Branch:** `claude/fable-review-code`, from main cdd9efd. No build-number change (the build master's).
- **Commits:** d537ce1 the report and probes; 05adee4 the fixes; f26a4a2 A10 applied (a mistake of timing) and 97f75d3
  taking it back as a tool; 1155555 the second pass; then the third pass (this commit: see the log).
- **Game, all review switches off:** see the last commit's message. With the switches off the game is 0.99.91:
  cadet_test ALL IDENTICAL.

## What I built

The report: `plans/review-fable-code.md` (section A safe fixes, B bigger items left for their own plans, E questions
for the user). The scripts behind its numbers: `plans/review-fable-probes/`.

The fixes, each behind its own switch, all **off** (declared together at the end of section 1; `LIB_SAY_ON` is in the
page's first script, tiEarly). The build master switches them on.

| Switch | Fix | Where |
|---|---|---|
| `LOOP_GUARD_ON` | A1: a bad frame doesn't stop the game; 20 bad among the last 120 bring a card that names the save really in storage | section 12: `loopGuard`, `loopMark`, `loopCard`, `loopCardLine` |
| `SAVE_KEEP_ON` | A2: an unreadable save is kept (`SAVE_KEY + '-bad'`, a later one `-bad-2`), the player told, the Saves app offers both, Throw it away asks first | 13: `loadGameSafe`; 19: `slotsAct` (baddl, baddl2, baddel, baddelgo), `slotsView`, `slotDownload(given, named)` |
| `SAVE_TELL_ON` | A3: a save that can't be made or written is a failed save: nothing written, the player told, told again when it works | 13: `saveGameSafe`, `saveMake`, `saveFailed`, `saveSay` (from `tickShip`), `SAVE_ST`, `SAVE_WORDS`; 19: `slotText` |
| `LIB_SAY_ON` | A4: no three.js: the title says so | tiEarly: `window.tiLibFail`; the three.js tag's onerror |
| `SLEEP_SAFE_ON` | A5: a failed night skip lifts the fade | 13: `sleepGo` |
| `LOAD_SAFE_ON` | A6: four damaged saves load | 29b `endOffDay`, 20c `storyCS`, 16 `galleySafe`, 20 `memNote` |
| `EVON_MEMO_ON` | A7: eventsOn keeps its flagged list | 18: `evonFlagged` |
| `WALLS_STILL_ON` | A8: walls and door leaves uploaded only when changed | 4b `instChanged`, `writeWalls`; 4a `doorLeavesSync` |
| `SAVE_TAB_ON` | A12: a tab doesn't save over a game another tab took further; its Download gives its own game as it is now | 13: `saveGameSafe` |
| `TEX_READ_ON` | A9: **stays off**: not pixel-identical. Pictures for the user: `plans/review-fable-shots/` | section 2 `tex` |

Not switches:
- **A10** `tools/one_byte.py`: puts the script in one-byte characters (8.85 MB less memory). **Not applied on this
  branch**: the build master runs it last on staging, after every word change. It proves token equality itself and adds
  the mark `[one-byte script]`; with the mark, content_gen.py (`baked_body`, `one_byte`), lines_check.py and
  names_check.js follow it.
- **A11** names_check.js: fails on a "does it exist" test on a name made nowhere; eleven known ones in `WAITING`.
- **A13** cadet_test.py: `flip(src, name, value)`, which fails unless exactly one switch line changed.
- **robust_check.py** (about 10 minutes): one part per fix, each on a copy with the switch on and a planted fault.
  In tools/affected.py as `robust`. It is not yet in the round's six-runner split: the build master adds it.

## Review state

- RV37 on 05adee4: PASS A4, A5, A6, A7, A8, A12. FIXES on A1, A2, A3 (and a note on A12): all taken, in the second and
  third passes. A3 follows RV37's simple cure (a failing handler is a failed save); the second pass's "make the save
  again without the failed handler" was taken out again in the third.
- RV37 has **not yet re-reviewed the third pass**. Expect small follow-ups on A1, A2, A3.
- BM29 rehearsed the merge with FR2 and one_byte.py: clean. Its find (lines_check after one_byte.py) is fixed here.

## Loose ends

- The full six-runner round has not been run on any of this. Only: names_check, content_gen --check, lines_check,
  cadet_test (off and on), check_fast, robust_check, saves_check, title_check.
- cadet_test against the nine switches on said once "ALL IDENTICAL (apart from renderer noise: some pixels 1 level
  off)" and twice plain ALL IDENTICAL: the known software-renderer noise, not looked into further.
- Backlog rows FR1-1 (five checks' own switch replaces change nothing today) and FR1-2 (Copy save as text copies the
  game being played, not the kept copy).
- Owner reviews for the small edits in sections 12, 13, 19, 18, 4a/4b, 16, 20, 20c, 29b and tiEarly: RV37 did the
  owner check on 05adee4.
- Section B of the report (the load freeze, the per-frame plan lookups, body animation, memory on the big decks, the
  file's scaffolding, save versions, the test process, the size of DEV_NOTES) is untouched: each needs its own plan.

## Gotchas

- The game queues pop-ups (`guideToast`): a check that reads a pop-up sets `window.cadetPopupsNow = true` before the
  game loads, and robust_check notes every pop-up rather than reading the one on screen.
- A page being left saves on its way out (pagehide). To plant a save for a test, plant it from an init script before
  the game's script runs, not by writing storage and reloading.
- `skipTo` calls `saveGame` itself: a check counting failed saves must allow for it.
- The checks' own page load has a 30 second limit in cadet_test's `Game`; under a busy machine perf_check fails on it.
- Switch lines must stay exactly `const NAME = false;` (or true): `flip()` and perf_check's `switched()` read them.
- Messages between sessions can arrive late (two of the lead's reached me after I had acted): read the queue before
  each push.

## How to test

```
export CADET_CHROME=/opt/pw-browsers/chromium          # CADET_WORK needs three/ and acorn/ (DEV_NOTES "Testing")
node names_check.js && python3 content_gen.py --check && python3 lines_check.py --quiet
git show cdd9efd:starship-cadet.html > old.html && python3 cadet_test.py old.html starship-cadet.html   # ALL IDENTICAL
python3 robust_check.py starship-cadet.html            # ROBUST CHECK OK; or one part: loop keep tell lib sleep load memo walls tab hint
bash check_fast.sh
python3 tools/one_byte.py --check                      # reports only; without --check it converts (staging only)
```

## Open questions for the user (through the lead)

The five in the report's section E (the parked frame cap, the tone of the error card, a comment-stripped published
file, reloading mid-activity, Safari), plus: the texture hint A9 (the two pictures; by eye they look the same, it saves
about half a second of load on the test machine).
