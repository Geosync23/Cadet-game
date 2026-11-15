# Independent review: the code, its speed and its safety nets (FR1)

FR1 for lead 52, 2026-11-15. Reviewed: main cdd9efd, the live 0.99.91 (game sha256 b321a4ec...95f3). Branch
`claude/fable-review-code`. Phase 1: review only, the game file is untouched. The scripts behind every number are in
`plans/review-fable-probes/` (how to run them is at the end).

## In plain words

The game is in better shape than its size suggests. Earlier performance work was real and it holds: nothing piles up as
the days pass, the save stays small, and the game's own work per frame is light. I re-measured those and agree.

The weak spots are somewhere else. They are about **what happens when something goes wrong**, and about **the first ten
seconds**:

1. **One small error anywhere freezes the game for good, with no message.** The picture stops, taps do nothing, and the
   player is not told. Today nothing catches it.
2. **A save that can't be read is thrown away without a word.** The player lands on Day 1 and, within an hour of play,
   the old save is overwritten. No copy is kept, nothing is said.
3. **When saving stops working (storage full or blocked), the game never says so.** The player plays on and loses it
   all on closing.
4. **Starting the game is one long freeze:** about 3.4 seconds on this test machine, about 10 seconds at the speed of
   a mid-range phone, about 14 on a slow one. A sixth of the part I could measure is one fixable browser setting.
5. **If the 3D library can't be downloaded, the title screen says "LOADING ... 10%" for ever.**
6. **The file carries a lot of scaffolding that is no longer needed** (switches that are always on, about 3,100
   "does this exist?" tests that are always true). It doesn't slow the game, but it hides mistakes and makes every
   change riskier.
7. **The testing is thorough but heavier and leakier than the notes say:** more checks than documented, some run from
   outside the repository, some can pass while testing nothing, and nothing tests a real phone browser.

None of this changes what the game is. Thirteen of the fixes are small and safe (section A). The rest need a plan
(section B). Questions for the user are in section E.

## The numbers at a glance

All on 0.99.91, the container's Chromium with software graphics, a 390 x 844 phone view. "Phone speed" means Chrome's
4x processor slow-down; it is a stand-in, not a phone.

| What | Measured |
|---|---|
| File | 8.87 MB (2.66 MB compressed for download). The crew's words are 37% of it; code comments are 16% (1.4 MB) |
| Load to first picture | 3.4 s here; 10.2 s at 4x slow-down; 14.3 s at 6x. One unbroken freeze (9.2 s of script at 4x) |
| Memory after loading | 27 MB of game objects, 57 MB of model data, 17.7 MB for the script text itself; about 94 MB in all, before the graphics chip's own copy |
| Game code per frame (drawing not counted) | 0.7 to 1.4 ms here (dinner with 58 people: 1.35 ms), so roughly 4 to 7 ms on a mid phone |
| New memory made per frame | 64 KB (quiet deck) to 230 KB (dinner): the browser must sweep it up several times a second |
| Sent to the graphics chip per frame, standing still | 55 to 127 KB of positions plus 24 to 157 KB of bone data, every frame |
| Draw calls / triangles | 106 to 199 calls; Deck 3 draws about 400,000 triangles a frame, Deck 6 about 33,000 |
| Largest deck in memory (Deck 3) | 2.28 million corner points, 52 MB of model data, one 4096 x 2048 floor picture |
| 100 ship days in one sitting, saving on | frame cost flat (0.4 to 1.0 ms), memory flat (77 to 86 MB), save 33 KB growing to 122 KB, written in 2 to 6 ms |
| A Day 100 save reloaded | loads, no errors |

## A. Safe to fix now

Each is small, can sit behind its own switch (off = the game as today), and can be checked with the existing tests.
Ranked by what it saves the player.

### A1. One error in one frame stops the game for good
- **What:** the main loop (`loop()`, section 12, line 80296) asks for its next frame on its last line (80416) and has no
  safety net. If anything it calls fails once, the next frame is never asked for. There is no page-wide error handler
  either.
- **Evidence:** planted one error in `crowd.update` for a single frame: ship time stood at 361.20 for the next 120
  frames, nothing on screen (`robust.py`, test 1). The helper review got the same with `galleyTick`. The file has 809
  `try` blocks; section 12 has none. The loop runs about 40 features' per-frame code from many seats (`eventsTick`
  alone calls about 40).
- **Why it matters:** any rare bug in any feature becomes "the game froze and I lost my evening". If the cause is in
  the save, it freezes again on every reload.
- **Fix:** wrap the loop's body; always ask for the next frame; log the error once; after several bad frames in a row
  show a plain card ("Something went wrong. Your game is saved. Reload the page."). With no error the game is
  identical.
- **Risk and effort:** low, small. Switch `LOOP_GUARD_ON`.

### A2. An unreadable save is silently replaced by a new game
- **What:** `loadGame` (9894) returns nothing for a save it can't read (cut short, or marked with a version it doesn't
  know). The game then starts on Day 1 and the next hourly save overwrites the old one.
- **Evidence:** planted a Day 10 save cut in half, and the same save marked `v: 3`. Both times: Day 1, the usual
  "You wake in Bunk 1" message, and after one ship hour the 48,058 / 96,117 character save had become a 15,563
  character Day 1 save. No other copy in storage.
- **Why it matters:** this is the worst thing the game can do to a player, and it would happen without a word. A
  future build that raises the save version would do it to anyone who opens an older copy of the game afterwards.
- **Fix:** before the first overwrite of a save that failed to load, copy it to `<key>-bad`, and say so once ("Your
  save couldn't be opened. A copy is kept; Saves app, Download my save."). Offer it in the Saves app.
- **Risk and effort:** low, small. Switch `SAVE_KEEP_ON`.

### A3. Saving can stop without the player knowing
- **What:** `saveGame` (9878) wraps everything, the 60 save handlers and the write, in one `try` with an empty `catch`
  ("the game carries on unsaved").
- **Evidence (helper, run):** with storage refusing writes, 4 saves failed in a row with no message and the stored
  save was 10 ship hours old; "Download my save" then handed out that old save and said "Downloaded". One failing
  handler among the 60 also stops every save from then on.
- **Fix:** `saveGame` reports success or failure; one message the first time it fails and a line in the Saves app;
  each handler in its own `try` so one bad handler doesn't cost the whole save.
- **Risk and effort:** low, small. Switch `SAVE_TELL_ON`.

### A4. No 3D library, no message
- **What:** three.js comes from one outside address (line 376) with no fallback and no error message.
- **Evidence:** blocked that download: the page error is "THREE is not defined", the title screen shows "TAP TO WAKE
  THE TERMINAL" and then "LOADING THE SHIP ... 10%" for ever (`robust.py`, test 3).
- **Fix:** when the library fails to load, the title says so in plain words ("Couldn't load the game. Check your
  connection and reload."). A second address is not an option on claude.ai (its pages may only load from cdnjs).
- **Risk and effort:** very low, small.

### A5. A failed night skip leaves a black screen
- **What (helper, run with a planted error):** `sleepGo` (10030) fades to black, then runs the whole night's catch-up
  inside a bare timer. If any part fails the fade stays black and `sleeping` stays true.
- **Fix:** always lift the fade and clear `sleeping`, error or not. Low risk, small.

### A6. Four ways a damaged save stops the game starting
- **What (helper, 444 randomly damaged saves, run):**
  - `endOffDay` (79963) is called during loading before the line that makes `endStep6` (79457) has run. It fails when
    the saved day is ahead of the machines' clock or `ship.machines` is missing.
  - `social.stories.cs` without `book` fails in `storyTick` (57296).
  - `galleyLoad` (19295) accepts junk garden beds, cold store and crates, which then fail every frame in `galleyStep`.
    These are saved as positions in the `GARDEN_CROPS` table, so reordering that table would break existing saves.
  - a note in `social.noteq` with no data fails in `memNote` (54307) on the hour.
- **Why it matters:** "Load a save file" accepts any file whose time and player look right (`saveOk`, 9901), and with
  A1 unfixed each of these is a game that never starts.
- **Fix:** four small guards with defaults. Low risk, small to medium.

### A7. The traditions list is re-read about 30 times a frame
- **What:** `eventsOn(d)` (46962) builds a text signature from every tradition (`filter`, `map`, `join`) on every
  call before it looks at its cache.
- **Evidence:** 26 to 33 calls a frame; 6 to 10% of all game code in the three scenes profiled (`dinner.py`,
  `calls.py`).
- **Fix:** work the signature out once per frame (or only when a flag changes). Same answers.
- **Risk and effort:** low, small. Switch `EVON_MEMO_ON`.

### A8. Walls and doors are re-sent to the graphics chip every frame, moving or not
- **What:** `writeWalls` (1082) and `doorLeavesSync` (734) rewrite every wall, post, sill, pane and door leaf and mark
  them changed on every frame.
- **Evidence:** 12 to 13 uploads, 55 KB a frame on Deck 4 standing still, 127 KB on Deck 3 (this includes the crowd's
  share) (`gl.py`); the two functions are 5 to 15% of game code.
- **Fix:** skip the write when no wall or door height changed since the last frame (compare exactly, so the picture
  is the same bit for bit).
- **Risk and effort:** low, small. Switch `WALLS_STILL_ON`. Needs cadet_test's screenshots identical with it on.

### A9. Half a second of the load is one missing browser hint
- **What:** `grain()` (464) reads a texture's pixels back from the canvas to add noise. `tex()` (450) makes the canvas
  without telling the browser it will be read, so each of the 17 reads waits on the graphics side.
- **Evidence:** 536 to 586 ms in those 17 reads here; 6 to 7 ms with `willReadFrequently: true` (measured twice
  each way). That is about a sixth of the load before the first picture. Only 1.05 million pixels are involved.
- **Fix:** pass the hint for the textures that are grained.
- **Risk:** the hint moves that canvas's drawing from the graphics chip to the processor, which may round a few
  pixels differently. It ships only if cadet_test says the pictures are identical; otherwise it becomes a question
  for the user. Small. Switch `TEX_READ_ON`.

### A10. 161 characters cost 8.8 MB of memory
- **What:** the browser keeps the script's text in memory. Because the script holds 161 characters outside the
  basic set (arrows, dashes, ticks, stars), it stores all 8.8 million at two bytes each.
- **Evidence:** memory snapshot: one 17.67 MB block for the script text; with those 161 written as `→`-style
  escapes it is 8.83 MB, and the game runs the same (no errors).
- **Fix:** write them as escapes (in `content_gen.py` too, where the baked words carry them), and have names_check
  fail on a new one. The words on screen don't change.
- **Risk and effort:** low, small. No switch is possible (it is the text of the file); proof is cadet_test identical.

### A11. Twelve hooks wait for code that was never built
- **What:** `typeof X === 'function'` tests on names that exist nowhere in the file: `galleyShift`, `galleyServe`,
  `bridgeInvitedNow`, `eventModAt`, `traceStops`, `introGuide`, `introGuideEnd`, `scanParts`, `faultWords`,
  `crossBackAddressAt`, `endLineDates`, `DEBUG`. The code behind each never runs.
- **Why it matters:** nobody can tell a planned hook from a typo. A renamed function turns its callers off silently
  the same way.
- **Fix (a check, not a game change):** names_check lists every guarded name that doesn't exist; the list of meant
  ones is kept in the check. Small.

### A12. Two open copies overwrite each other
- **What (helper, seen while testing; I hit it too):** a page being closed saves on its way out (9921) and
  overwrites a newer save made by another tab.
- **Fix:** don't write over a stored save that is newer than the one this page loaded. Low risk, small.

### A13. Checks that flip a switch don't all check that it flipped
- **What (helper, run):** about 25 checks make an "on" or "off" copy of the game by replacing text. Some assert the
  replacement happened; `arrows_check.py` 589 and 706, `controller_check.py` 590 and 1633 and `ending_check.py` 383
  replace nothing today and carry on.
- **Fix:** one shared helper that fails unless exactly one line changed. Small, checks only.

## B. Bigger, needs a plan

### B1. The start-up freeze
- **What:** the whole game is built in one go before the first picture: 3.4 s here, 10.2 s at 4x, 14.3 s at 6x. The
  title screen is painted first (good), but nothing on it can respond during the freeze.
- **Where the time goes** (here, before the first frame, about 1.7 s of script): textures 0.6 s (A9 removes most);
  placing the crew 0.65 s, of which 0.45 s is the machines catching up (`deckCrewFill` -> `whereIs` -> `shipDay` ->
  `machinesNow`); building Deck 4, 0.4 s; reading and compiling the 8.8 MB script 0.14 s (0.8 s at 4x). Then the first
  frame compiles about 20 shader programs: 2.7 s in this software renderer, unknown on a phone, likely the largest
  single piece there.
- **Plan:** (1) A9; (2) build in slices over several frames behind the title screen so the bar moves and taps
  register; (3) compile shaders in the background where the phone allows; (4) put off the machines' catch-up until
  after the first picture. One reading from the user's phone (the Dev Speed card could show load time) would say
  which matters most.
- **Risk and effort:** medium. Load order is delicate in this file (see B7).

### B2. Every crew member's whole plan is asked for again every frame
- **What:** `CrewAgent.update` (73833) calls `whereIs` for each person each frame, which runs `planWhere`, `shipDay`,
  `evChanged`, `machinesNow` and the escort chain (`worksEscort`, `promoEscort`, `p5Escort`, `p5TeacherWait`; the
  last two search and copy the occasions list each time).
- **Evidence:** at dinner with 63 people: 82 `whereIs` a frame and 82 of each of those, plus 201 `flag` reads
  (`calls.py`). Ship time moves one minute every 100 frames, so 99 of 100 answers are the same. It is 6 to 10% of game
  code and a steady source of new memory.
- **Plan:** keep each person's answer until the ship minute changes or something that affects escorts happens.
  This touches the planner's rule (it must give the same plan whenever asked), so it is the sim engineer's to design.
- **Risk and effort:** medium.

### B3. Moving bodies is half the frame
- **What:** `CrowdPerson.update` -> `animateActivity` -> `animateRig`, with three's matrix work, is 45 to 55% of game
  code in a busy room, for everyone on the deck, whether on screen or not, at full rate.
- **Plan:** people off screen or far away animate every second or third frame; seated, still people skip most of the
  bone work. This changes pixels slightly, so it needs the user's eyes.
- **Risk and effort:** medium.

### B4. New memory every frame
- **What:** 64 to 230 KB a frame. The biggest makers: `bake` (71273) and `walkGap` (11906) when a crowd walks,
  `CrewAgent.update`, `animateActivity`, `writeWalls`, the loop's own small helper functions (`hides`, `dep`),
  `p5Escort`, `crewWayOn` (a new list per person per frame).
- **Why it matters:** at 230 KB a frame the browser sweeps memory several times a second; on a phone each sweep can
  drop a frame. Part of "it stutters at dinner".
- **Plan:** A7, A8 and B2 remove a good share. Then a pass through the list above, one by one, with `dinner.py` as
  the measure.

### B5. The picture is drawn flat out, always
- Already measured by PF1 (plans/perf-0996.md) and parked by the user on 2026-11-01: four switches exist (`#pfcap`,
  `#pfpr`, `#pfsh`, `#pfaa`). I agree with PF1's reading: the game draws at up to twice the screen's pixel count, with
  edge smoothing and a 2048 soft shadow, at the screen's full rate (120 a second on the user's phone), including
  while paused and on the title screen. That is the likely cause of "worse the longer I play".
- **New here:** game code at dinner is about 5 to 7 ms on a mid phone. On a 120-a-second screen the whole frame has
  8.3 ms, so there the game code alone nearly fills it; the frame cap at 60 doubles the room. See question E1.

### B6. Memory on the big decks
- Deck 3 holds 2.28 million corner points (52 MB), Deck 2 1.73 million (39 MB), Deck 4 1.24 million (29 MB); about 280
  to 475 furniture pieces per deck stay in memory after being merged into bigger ones (they are hidden, never drawn).
  The floor is one 4096 x 2048 picture: about 33 MB in memory plus about 45 MB on the graphics chip.
- Total after load is about 94 MB before the graphics chip's copy. Phones with 3 to 4 GB may close the page in the
  background sooner than they would a lighter one.
- **Plan:** free the merged originals' data once merged (keep what taps need); A10; see whether the floor needs its
  full size on small screens. Needs the render seat.

### B7. The file's scaffolding
- **Switches:** 60 are always `true`, 17 always `false`, and 31 web-address flags are still read. Each always-on switch
  keeps its "off" code in the file and in every reader's head (`REC_DECK` is tested in 55 places, `EV_ENDING_ON` in
  51, `P5_STEP5` in 34). The project rule (off = the old game) is good while a feature is new; there is no step that
  folds a switch in once the release is out.
- **"Does it exist" tests:** 3,146 of them on 1,055 names; 1,630 are on functions that always exist, 1,451 on tables
  that always exist once loading is past their line. They date from when sections were built apart. Now they are
  always true, and where they are not (during loading, on a `const` further down the file) the test itself fails
  rather than protecting: that is exactly A6's first bug.
- **Silenced errors:** 809 `try` blocks, 45 with an empty `catch`. Useful around other seats' hooks, but they also
  hide real faults (A3).
- **Order:** the sections are not in number order (13, 14, 19, 15 ... 12 last) because code must come after what it
  reads at load. That rule is unwritten in the code and is easy to break.
- **Line length and comments:** 80 lines are over 2,000 characters (the longest is 26,916); comments are 1.4 MB.
  History in comments is valuable, but the published file pays for it in download and memory.
- **Plan:** (1) a "fold" step in each release: switches on for two releases are folded, their off-branches go to the
  archive (the cut-things rule still holds: the record is kept); (2) A11 first, then remove the always-true tests a
  section at a time, cadet_test identical each time; (3) consider publishing a copy with comments stripped while the
  repository keeps the full file (E3).
- **Risk and effort:** each step is low risk but there are many; large in total.

### B8. Save versions
- `SAVE_V` has been 2 since 0.28.1 while the save grew to about 60 handlers. The build number is saved and never
  read. Old saves work because each loader fills in what is missing (the helper loaded 0.64.2 saves from Days 3, 12,
  26 and 34 into 0.99.91 and played 9 more days: no errors). That is a good result, but nothing guards it: no real
  save from a published build is kept and loaded by a check.
- **Plan:** keep one real save per release as a test file and load each in saves_check; use the saved build number
  when a loader needs to know. Note A2: raising `SAVE_V` today would wipe players' saves in older copies.

### B9. Things that are not saved
- (Helper, reading only.) The tray you carry (`SHIP.player.tray`, 14815) has no save handler. The activity in
  progress, an open conversation and a lift ride live only in memory; many "reloaded mid-scene" cases were fixed one
  at a time. Worth one list of what a reload may lose, agreed with the user (E4).

### B10. The tests
From the helper's review (reading and quick runs only; nothing long was run) and my own use of the checks.
- **The round is bigger than documented.** The notes say 33 checks, about 176 minutes. `tools/affected.py` lists 51
  entries, 274 minutes; 12 check files are unknown to it (controller, title, appt, stories, three arrows checks,
  promo_sight, cr1, cr2, p926); round 09991 ran day_check on 24 days. One list that both the round and the notes are
  made from would end this.
- **Five round checks are not in this repository** (`fresh_walk`, `pf_f1_same`, `fixtap_reach`, `fixtap_click`,
  `p5retry_break`); `fresh_walk`, the only multi-day walk-through, is fetched from a review branch and has no OK
  line.
- **Checks can pass while testing nothing.** About 1,100 "not in this build: skipped" guards in the checks; a renamed
  function switches its assertions off and the check still says OK. Plus A13.
- **Real time leaks in.** The test clock replaces `performance.now`, `Date.now` and frames but not `setTimeout`
  (35 in the game); the checks wait in real time 67 times. That is the root of the known flaky ones. Round 09991's
  find G was closed as "likely one-off" although the backlog (CP4-1) records the same part failing one run in three.
- **perf_check fell over twice for me** while other work used the machine: its page load has a 30 second limit and the
  load took 27 seconds under load. It also judges game code per frame from one sample with a 30% margin, has no
  absolute limit, records load time without judging it, and its "week of play" is 28 jumps of 20 frames.
- **Nothing tests a real phone browser.** One engine (headless Chromium, software graphics, a file address, saving
  off). No Safari/WebKit, no Firefox, no touch in 43 of 45 checks, no test with the 3D library blocked, no test of
  a frame error, none of the claude.ai page's storage rules. 5,457 direct calls into the game against 257 clicks.
- **The test picker's map is from 0.64.12** (50,000 lines; the game is 80,419 now).
- **GitHub runs only the quick check**, and nothing stops a publish when the round was skipped.
- **Plan, in order of value:** (1) a WebKit smoke check (load, 200 frames, a tap, save, reload), a blocked-library
  check and a planted-frame-error check; (2) one list of the round; (3) the five missing checks into the repository;
  (4) a build's expected-parts list so a skipped part fails; (5) put `setTimeout` on the test clock; (6) the round as
  a GitHub job in six parts, replacing six hand-run sessions; (7) remake or retire the picker's map.

### B11. The paperwork is now a cost
- `DEV_NOTES.md` is 771 KB, about 190,000 tokens: a fresh session that reads it first, as CLAUDE.md says, has spent a
  fifth of its memory before it starts, against a hand-over rule at 60%. `plans/build-table.md` is 1.8 MB with lines
  up to 6,102 characters; `plans/` is 174 MB in 1,056 files.
- **Plan:** DEV_NOTES becomes a short current page (rules, testing, what's next, a map) with the history moved to an
  archive file per release; the build table one file per release.

## C. Checked and sound

- **Nothing grows with play.** 100 ship days in one page with saving on: frame cost, memory, lists and the save all
  flat (`long-run.txt`). Agrees with PF1's 40 days.
- **Deck changes give memory back** (canvases are emptied on unload, the old deck's tree is taken apart).
- **A lost graphics context comes back** (lost and restored on purpose: the picture returned, a deck change worked;
  only harmless warnings).
- **Time is handled carefully:** frame time is capped, ship time stops while the tab is hidden, hiding the tab pauses
  and saves, no `setInterval`, and nearly all 35 timers are for the page or sound.
- **Storage calls are wrapped throughout**; a bare-minimum save loads; an out-of-range position is put right.
- **Earlier speed work is well done:** crowds drawn in batches, furniture merged, shaders kept across decks, the path
  finder checked against its slow twin, loops written to avoid waste.
- **names_check passes** (6,348 names, 4,316 table keys, 129 registrations).

## D. Proposed fix list for phase 2

In this order, each behind its own switch where a switch is possible, each with a build-table row:
A1, A2, A3, A4, A5, A6, A7, A8, A12, then A10, A9 (only if the pictures come out identical), and the two check-only
items A11 and A13. I would leave everything in B for its own plan.

## E. Questions for the user

1. **The parked speed options.** The frame cap at 60 changes nothing in a still picture and halves the work on a
   120-a-second screen. Would you try `#pfcap` (or `#pfcap.pfpr`) for one long session and say whether it still gets
   worse the longer you play?
2. **When something goes wrong,** is a plain card ("Something went wrong. Your game is saved. Reload the page.") the
   tone you want, or should the game try to carry on quietly and only log it?
3. **A lighter published file.** The game could be published with its code comments stripped (about 1.4 MB less to
   download and hold in memory) while the repository keeps the full file. It adds a publishing step. Wanted?
4. **Reloading mid-activity.** Should a reload put you back exactly where you were (carrying your tray, mid-shower),
   or is "back at a sensible moment nearby" enough? Today it is the second, case by case.
5. **Other browsers.** Is Safari on iPhone a target? Nothing tests it today.

## How these were measured

`plans/review-fable-probes/` (Playwright; three r128 in `$CADET_WORK/three`):
- `loadtrace.js GAME [slow-down]` and `load.js`: load time and what fills it.
- `dinner.py`, `frame.py`: game code per frame, each function's share, new memory per frame.
- `calls.py`: calls per frame of the planner functions. `gl.py`: uploads and draws per frame.
- `mem.py`, `heap.py`, `tris.py`: memory by deck, a memory snapshot by kind, triangles by object.
- `long.py`: 100 ship days in one page, saving on (`long-run.txt` is its output).
- `robust.py`: a planted frame error, a lost graphics context, a blocked 3D library.
- `save-review/`: the helper's damaged-save runs.

Limits: no real phone and no real graphics chip (drawing cost is not measured here, only game code and counts); the
timing runs were on a shared 4-core container, best of several batches; the helper reviews of saving and of the tests
are marked as such, and their "reading only" items are named.
