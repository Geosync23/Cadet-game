# Reviews for 0.60.7 (reviewer 0607)

- **Reviewer:** session_01BusfBzBamabWrCsrwQeABh, branch `claude/reviews-0607` (from live 0.60.6a, c8685cf). Reports to lead 10 (session_014hkEBULoSV9EKZZSwMWyPd).
- **Depth:** behaviour, save and schedule changes in depth (determinism: nothing at load calls `R()`; saves within budget; phones first; every colour through `col()`); content and test-only changes skimmed.
- **Verdicts:** PASS / FAIL, findings HIGH / MED / LOW, each with a concrete path. Newest first under "Verdicts". Probes saved under `plans/reviews-0607/`.

## Queue
(empty)

## Verdicts

### Head writer 0.48.82, claude/writer-0607 2799442 (skim; supersedes c2b1b6a): PASS, one MED to fix before the bake
Only `content/lines/torres-zeke.lines` (+ keys and DEV_NOTES). No lines_check change in this commit (the 5-line lines_check change is in f57d98c, reviewed below: fine).
- **Checks:** `content_gen.py` then `lines_check.py` on a scratch copy: **PASS** (0 errors, the same 2 old warnings; 8084 lines).
- **MED: a line tells the player there's lunch.** `walk.talk.6`: "Lunch is in the mess. Brennan notices if you skip it." design-doc (the schedules section, about line 778) says two meals a day and no lunch, and lunch is listed as "answered no (2026-10-16), not to be re-asked". A new player is told on Day 1 to go to a meal that never happens. Suggested: "Dinner's at five in the mess. Brennan notices if you skip it." (or breakfast). One line.
- **LOW 1:** walk.talk lines left over "carry on next walk". `walk.talk.24` ("Tonight there's the beam. Don't run off at five.") and `.29` ("Nearly home time.") are only true on Day 1 before 17:00. If the onboarding engineer carries the leftovers past Day 1 or past five, they'd be wrong. Either the onboarding engineer stops walk.talk at 17:00 on Day 1, or these two get a `time:`/day condition. Worth a word between the writer and onboarding.
- **LOW 2:** "Ask me how I know." twice in Zeke's Day 1 lines (`walk.job2.panel.washer` and `walk.talk.8`), likely heard within the same hour.
- **Facts checked:** the time clock is by the tea corner (5-timeclock-1), the shift is 08:00-17:00 with the 17:00 auto clock-out, Saturday and Sunday are the weekend, the laundry is on Deck 4, Knit and natter is on Tuesdays against Tiles, and Lap of the Wren is on Mondays. All right.

### Head writer 0.48.81, claude/writer-0607 7e4fb1e..c2b1b6a (skim): PASS
Text only (45 files, +1457 lines) and two small lines_check rule changes; no game code.
- **Checks:** `lines_check.py` on c2b1b6a as pushed: FAIL only for "the baked blocks in the game file are out of date" (expected: the writer doesn't bake; the build master does). After `content_gen.py` on a scratch copy: **PASS** (0 errors, 2 old warnings about "(Say nothing)"; 8047 lines, up from 7515).
- **lines_check change:** adds the placeholders `time hours n max part shelf drink` and lets `tip.*` lines run to 200 characters. Both fit the plan (the first-evening tips are long). Fine.
- **Facts, checked against design-doc and the plan:** the gym is on Deck 3, the booths and crew store on Deck 3, Gym club (id `running` kept) has every machine, Name on the beam is the Works bay. The low-need pop-ups use the user's own words ("You need to pee"), one main line per need plus spares. Tone is warm and plain throughout.
- **LOW 1:** `clock.screen.ready` says "Shift starts at 08:00." as fixed text. Fine for the Works shift today; if the player's shift ever moves, it would be wrong. Suggest `{time}` (already allowed) when PE6 wires it.
- **LOW 2:** the 13 `content/trad-words/*.words` files aren't read by content_gen or lines_check, so their lengths and placeholders are unchecked until the traditions engineer pastes them into `.trad` files. The traditions engineer should run lines_check after pasting.
- **Note:** `clockscreen.lines`'s header mentions `{day}`, but no line uses it and it isn't in the allowed list; harmless.

