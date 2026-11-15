# Review: FR1's review fixes A1-A8 and A12 (RV37 for lead 52)

RV37, 2026-11-15. Reviewed: branch `claude/fable-review-code`, commit 05adee4 (game sha256 908d3c3e...e3fa with every
switch off), against the live 0.99.91 (main cdd9efd, game b321a4ec...95f3). I never edited the game. My probes are in
`plans/rv37-probes/` (how to run them is at the end). This review also stands as the owner check for the sections the
fixes touch (1, 4a/4b, 12, 13, 16, 18, 19, 20/20c, 29b). A9 (TEX_READ_ON) and A10 were not reviewed, as briefed.

## Verdicts

| Fix | Switch | Verdict |
|---|---|---|
| A1 the main loop's safety net and card | LOOP_GUARD_ON | FIXES NEEDED (small: the card's words; errors that come and go) |
| A2 an unreadable save is kept | SAVE_KEEP_ON | FIXES NEEDED (small: a second unreadable save; Throw it away) |
| A3 save failures are said | SAVE_TELL_ON | FIXES NEEDED (the "one failing handler" half; the storage half is good) |
| A4 no 3D library | LIB_SAY_ON | PASS |
| A5 a failed night skip | SLEEP_SAFE_ON | PASS |
| A6 four damaged-save guards | LOAD_SAFE_ON | PASS |
| A7 the traditions list kept | EVON_MEMO_ON | PASS |
| A8 walls and doors sent only when changed | WALLS_STILL_ON | PASS |
| A12 two tabs | SAVE_TAB_ON | PASS, with one small thing worth fixing (Download in a stopped tab) |

None of the FIXES NEEDED items can hurt a player while the switches stay off. They matter on the day a switch goes on.

## 1. Switches off: the game as today (all nine: yes)

- Read the whole game diff line by line (368 lines of diff). Every changed line is behind its switch. Two lines read
  `SAVE_ST` without a switch (`tickShip`: `if (SAVE_ST.say)`; `slotsView`: `SAVE_ST.other`, `SAVE_ST.fail`): nothing
  ever fills them with the switches off, and `tickShip` is only called from the main loop, long after `SAVE_ST` is made.
  `slotText` and `slotDownload` behave as before when `saveGame` answers nothing (it only answers with A3 or A12 on).
  The 3D library's script tag gained `onerror="window.tiLibFail&&window.tiLibFail()"`: nothing with the switch off.
- `python3 cadet_test.py OLD(0.99.91) NEW(05adee4, all off)`: **ALL IDENTICAL**, errors A [] B [].
- `node names_check.js`: names_check: OK.

## 2. Switches on (A1-A8, A12, and A4): the whole game

- `python3 cadet_test.py OLD(0.99.91) ON`: **ALL IDENTICAL**, errors A [] B [].
- `python3 robust_check.py starship-cadet.html`: ROBUST CHECK OK (722 s here, three other runs beside it).
- On a copy of 05adee4 with the nine switches on: `bash check_fast.sh`: QUICK CHECK OK in 534 s; SAVES CHECK OK;
  EVENTS CHECK OK; DEVMODE CHECK OK; day_check: no FAIL line (the run was cut off by the account's usage stop before
  its last line). title_check: four controller lines failed twice while six other runs shared the machine; with the
  machine quiet the same switches pass (TITLE CHECK OK on the second pass, below), so I put it down to load.
  food, fridays and dev_arrow were not run (cut off; usage is tight).

## 3. Fix by fix

### A1 LOOP_GUARD_ON: FIXES NEEDED (small)

What is right: one bad frame is only a skipped frame; the card comes once; it sits on top of everything (also over the
night's fade); Reload works and the game comes back where it was (the page saves as it leaves, as always).

1. **The card says "Your game is saved." when that can be untrue.** Probe `loop 3`: under `?nosave` (nothing is ever
   saved) the card says it. Probe `loop 4`: storage refusing, the game already telling the player "Not saving", nothing
   at all in storage: the card still says "Your game is saved." It is also untrue in a tab that has stopped saving
   (A12). Ask: don't promise. For example "Something went wrong" / "Reload the page to carry on from your last save."
2. **An error that comes and goes never brings the card**, because the count goes back to nought on every good frame.
   Probe `loop 2`: 19 bad frames of every 20, 600 frames: no card, and ship time ran at a twentieth of its speed (0.6
   minutes where 12 should pass), so to the player the game is frozen exactly as before the fix, with no word. Probe
   `loop 1`: every other frame bad: no card, half speed for ever, 300 errors logged. Ask: let the count run down
   slowly instead of clearing (for example one off for each good frame, or "20 bad among the last 120").
3. Small, to taste: the card is a little see-through, so a message under it shows through (loop-card.png); the card
   takes no focus (keyboard and controller players can't press Reload without a pointer).

### A2 SAVE_KEEP_ON: FIXES NEEDED (small)

What is right: the copy is made before anything overwrites the save, text for text; a good save is left alone; slots
2 and 3 get their own copy (`starship-cadet-save-2-bad`, probe `keep 3`) and the slot list doesn't mistake it for a
slot; Dev mode's saves have their own.

1. **A second unreadable save is dropped while the player is told it was kept.** The code keeps only the first copy
   (on purpose: "the oldest has the most to lose"). Probe `keep 2`: copy A kept; later a second unreadable save B in
   the same slot: the message says "The old save is kept", the Saves app offers A, and an hour on B is nowhere in
   storage. Either keep both (a second key), or keep the newer one, or at least don't say "kept" when it wasn't.
   My pick: keep the newest too (`-bad2`), because the save the player was just playing is the one they will ask for.
2. **"Throw it away" deletes at one tap.** Deleting a slot asks "sure?" first (`SLOT_UI.sure`); this is the only copy
   of a save the player may want. Ask: the same second step.
3. To know, not to fix now: with an unreadable save the title screen says "> no crew record: new cadet" (probe
   `keep 4`), and the "couldn't be opened" message then arrives at the first frame of the new game, during the
   shuttle arrival. It would be kinder if the title itself said so. The downloaded file can't be loaded back by this
   build ("Load a save file" refuses it, rightly); it is for sending to us.

Words: plain. "Your save couldn't be opened" / "A new game has started instead. The old save is kept: open your
device, then Saves, to download it." Good.

### A3 SAVE_TELL_ON: FIXES NEEDED (one half)

The storage half is good: told once ("Not saving"), the Saves app says so, Download my save hands over the game as
it is now, told again when saving works. The save text is the same as today's code writes: probe `tell 1`, same play
on both, the texts differ only in `ship.career.gs`, which also differs between two runs of the same build.

**The "one failing handler" half can lose part of a save, quietly, where today nothing is lost.** The code says the
failed handler's part "is taken from the last save that held it". That only works when the part is a top-level key
of the save AND a save already worked earlier in the same sitting:
- About half of the 52 handlers write inside `save.player` or `save.ship` (credits, locker, needs, carry, alarm,
  career, works, events, appointments, the ending). For those nothing is put back. Probe `tell 2`: the credits handler
  fails; `saveGame` answers true; the stored save has no credits, locker or chats; the player is told nothing.
- `SAVE_ST.kept` is empty until the first good save of a sitting. Probe `tell 3`: load a Day 10 save, the social
  handler fails at the first save: the stored save has no `social` at all (the loaded one had it), nothing is said,
  and after a reload the player has met 0 people (5 before).
- Today, the same fault (probe `tell 4`): nothing is written, and the Day 10 save in storage stays whole.
So with the switch on a rare bug in one handler turns "saving has stopped (and nobody says so)" into "a part of your
game is wiped at the next reload (and nobody says so)". Ask, either of:
- simple: a handler that fails makes it a failed save: nothing written, counted, the player told (the message is
  there already). Today's safety plus the word. Or
- thorough: carry the failed handler's part over from the save in storage (read at load, not only this sitting),
  including the keys inside `player` and `ship`, and still tell the player something is wrong.
robust_check's own test passes because it picks a top-level part after two good saves.

### A4 LIB_SAY_ON: PASS

Probe `lib` (the real way in, no test flags, with and without a save): the title comes up awake with "> no link to
the ship" and "THE GAME COULDN'T LOAD. CHECK YOUR CONNECTION, THEN RELOAD THE PAGE."; no menu; taps, Enter and 2.5
seconds later it still says so (lib-first-visit.png). Words: plain.

### A5 SLEEP_SAFE_ON: PASS

Read: the night's work runs as before inside a try; on an error the knock is dropped, the light is set, the fade
lifts and `sleeping` clears in the usual timer. robust_check proves off = black for good, on = you wake. To know: you
then get "Good morning" at whatever time the failed catch-up reached; better than a black screen.

### A6 LOAD_SAFE_ON: PASS

Read the four guards. Probe `load`: sixteen more damaged saves in the same four places (stories as a number or a
list, book as text, garden as a number, junk beds and crates, produce as text, notes with empty or text data, a note
that is not a list, no machines, Day 80): all start and play two hours on, no errors, no card. A sound game: over 16
ship days in 2-hour steps `galleySafe` changed the galley 0 times of 192.

### A7 EVON_MEMO_ON: PASS

Only the list of which traditions carry a flag is kept; the flags' values are still read on every call, so a flag
set mid-frame or by a Dev jump can't go stale. The list is checked entry by entry on every call. No code changes a
tradition's `flag` or `unflag` in place (searched). Probe `memo`: 24 ship days in 3-hour steps, the kept list equal
to a fresh one 192 of 192 times; a tradition replaced in place, put back, added and removed: right each time; Dev
mode after a jump to Day 21: right. events_check and fridays_check on the all-on copy: see section 2.

### A8 WALLS_STILL_ON: PASS

No one but `writeWalls` and `doorLeavesSync` writes these meshes (searched: `wallIM`, `hdrIM`, `postIM`, `hpostIM`,
`sillIM`, `paneIM`, `DOOR_LEAVES`), so nothing relied on the every-frame flag. A new deck makes new meshes, which
have no copy yet, so they are sent. Probe `walls`: 162 pictures with every frame drawn (the first four frames, the
Walls button twice and back, Decks 3, 6, 5, 7, 4 each with its first five frames and the Walls button, a morning
with five doors moving, four turns of the view), switch off against on: 0 differ.

### A12 SAVE_TAB_ON: PASS (one small thing)

Probes `tab`: a new game over a Day 10 save in the same tab saves (1); Load a save file into the slot being played,
older or newer, then saves (2); two real tabs on one browser: the one behind stops and says so, the one ahead keeps
saving (5). Words: plain.
- **Worth fixing:** in a tab that has stopped, "Download my save" hands over this tab's game as it was when it
  stopped, not as it is now, and says "Downloaded". Probe `tab 3`: two ship hours later it hands over minute 601,
  the tab is at minute 726. (`saveGameSafe` returns before it makes the text once `other` is set.)
- To know: it guards one way only, as FR1 wrote. If the other tab started a new game, or loaded an older file, this
  tab still saves over it (probe `tab 4`), as today.

## 4. Seen on the way (not FR1's)

- Under load, "Load a save file" into the slot being played sometimes came back as the game before it in my test
  rig, on 0.99.91 as well as on the branch (2 of 6 and 1 of 2 tries). The file is written, the page reloads, and the
  old Day 10 save is what the new page reads. I think it is the rig (a headless browser on file:// pages, three
  other runs beside it), and saves_check passes, but nobody has ruled out a real race. One backlog line suggested.

## 5. How to run the probes

`python3 plans/rv37-probes/rv37_probe.py starship-cadet.html [loop keep tell tab memo walls load lib]` from the
repository's folder, set up as for cadet_test (CADET_WORK, CADET_CHROME). It prints what happens and judges nothing.
`RV_TELL1=none` runs only `tell 1` with both builds off (to see the run-to-run difference).

## 6. Second pass: FR1's repairs, commit 1155555 (game off 0a9f7e3d...c118)

Read the second diff line by line (166 lines), then reran my probes on a copy with the nine switches on.

| Fix | Verdict on 1155555 |
|---|---|
| A1 | PASS |
| A2 | FIXES NEEDED, one small thing left: "Throw it away" still deletes at one tap (now both copies) |
| A3 | PASS on the rule "whole or none"; one thing for the lead to decide (a part can stay old without a word) |
| A12 | PASS |
| tools/one_byte.py (A10) | PASS |

- **A1.** Bad frames are counted over the last 120: every other frame bad: card; 19 of 20: card; one in five: card;
  one in eight: no card (fair: the game runs). At most three errors are logged. The card now says what is true:
  under `?nosave` "Reload the page to start again."; storage refusing and nothing stored: "This game has no save yet.
  Reload the page to start again."; otherwise "Your game is saved up to Day N, hh:mm. Reload the page to carry on from
  there." To know: pressing Reload saves on the way out when saving works, so you usually come back at the moment of
  the fault, a little later than the card says; harmless.
- **A2.** A second, different unreadable save now goes under `<key>-bad-2` and the Saves app offers "Download the
  later one"; no room for a copy: the player is told so, not "kept". Still open: probe `keep 2`: one tap on "Throw it
  away" removes both copies with no "sure?" (deleting a slot asks first). Lead 52 asked for this.
- **A3.** A failing handler now makes the save again from the start without it and puts in what that handler added
  the last time it worked (also inside `player` and `ship`); a handler that has never worked this sitting: nothing is
  written and the player is told. Probes: `tell 2` (credits handler fails after a good save): the stored save has
  credits, locker and chats; `tell 2b` (it fails half way, having written junk): the junk never reaches storage;
  `tell 3` (the social handler fails at the first save after loading): saveGame false, "Not saving" said, the loaded
  save untouched, 5 people met after a reload. So the last whole save is never replaced by one with a piece missing.
  **For the lead:** in `tell 2b` the player had earned 500 credits; the save is written every hour with the old 40,
  nothing is said and the Saves app shows nothing, for the rest of the sitting; after a reload the same fault turns
  into "Not saving". My judgement: the rebuild is safe and better than not saving at all (everything else stays
  fresh, and Download my save works), but it should say so once ("Part of your game isn't saving ..."). If that
  word is not wanted, the simple cure (any failure = no write, told) is the more honest of the two.
- **A12.** Probe `tab 3`: a stopped tab's Download my save hands over minute 726 with the tab at 726.
- **tools/one_byte.py.** Ran it on a copy of 1155555: 161 characters (132 in code, 29 in comments), "1430563 tokens
  read the same", a second run "already in one-byte form", `--check` exit 0, names_check OK, content_gen "up to
  date", no character outside Latin-1 left. My own proof, apart from the tool's: both scripts parsed whole and the
  two syntax trees compared (positions aside): equal except one regular expression's own text (`/^[pause sign]/`
  written with its escape: the same match); all 425 template pieces have the same raw text; the script has no tagged
  templates and no `String.raw`, the only places an escape could read differently. No check searches the game's text
  for one of the rewritten characters. To know: the mark line moves every script line down by one.
- Whole game on 1155555: cadet_test 0.99.91 vs 1155555 all off: ALL IDENTICAL; vs the nine on: ALL IDENTICAL (run alone;
  a first run beside another showed a few pixels one level off, the software renderer's known noise); title_check on the all-on copy: TITLE CHECK OK.

## 7. Backlog line suggested (lead 52 carries it)

"Load a save file" into the slot being played: in RV37's test rig, under load, the page sometimes came back with the
game from before the file (on 0.99.91 too: 1 of 2 tries; branch: 2 of 6). Probably the rig (headless browser, file://
pages, a start-up script that plants a save), saves_check passes; not ruled out as a real race between the write and
the reload. To check: the same on a served page with nothing else running.
