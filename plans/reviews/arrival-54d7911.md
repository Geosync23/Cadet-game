# Re-review: claude/arrival 4f6d0b2..54d7911 (0.42.18-0.42.21) — PARTIAL

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES (partial review: stopped by the lead before every check finished; see "Not finished").**

Scope: section 21. a86d052 (0.42.18: Tuesday's health check, `socialSeekAsk`, the Friday mug), e270ee2 (0.42.19: week meetings wait for their speaker, `tipSeen`), d24b017 (0.42.20: Zeke's tour, `introDinner`/step `table`, the first-night bed arrow), 54d7911 (0.42.21: exact writers' line per tour place, Zainab's window 16:00-19:30), plus intro_check-only and docs commits up to b16436f. No `schedU(` in the diff (no hash keys used), no `Math.random`/`Date.now`; the tour paces bubbles with `performance.now()` (cosmetic only, no game state). `python3 name_check.py --branches 4f6d0b2 54d7911`: NAMES OK.

Full merge used for the final runs: arrival b16436f (game = 54d7911) + sim b9089d9 + deck-plans d53cf40 + social 0af9cb8 + social-stories ba09f2b + player b728101 + galley 257aa62 + content a6dd44c; only build-line conflicts resolved (one generated TRADITIONS hunk where the other side was empty, kept). `name_check.py` on it: NAMES OK, node --check parses. Earlier runs below were on merges at e270ee2 (sim 971b4c7) and d24b017 (sim 0cf991a); the code each finding is about is unchanged in 54d7911 (its diff touches only `introWriterLine` and `d4-favour`).

## Previous note (arrival-4f6d0b2), status
- **Finding 1 (briefing starts before its cast is in the room): FIXED** in 0.42.19. `introWeekMeetings` now waits for `b.who` in the room (or 10 minutes). Briefing probe on the 54d7911-era merge (sim 0cf991a): Calder in Main storage 07:40-07:51, both reach the Works bay, `introBriefing` (untrimmed, lines calder ×3, torres-zeke) plays at **07:57**. intro_check **part 10 OK on the full 54d7911 merge** ("introBriefing", speakers calder…tech1, tech2…torres-zeke, `cal: 'Works bay'`; shadow job taken, Torres follow 2 tiles, turned in, ticked).
- **Finding 2 (introPlan double-books 5-stool-1): FIXED by the sim** (0.26.29, `introLay` takes the first free of `alts`). `whereIs` at 07:55: calder 5-stool-1, torres-zeke **5-toolwall-1**.
- **Finding 3 (direct tipsSeen write):** now `tipSeen(k)` when it exists, else the direct write; hook registered. `tipSeen` exists on no branch yet, so the direct write is still what runs until the device engineer adds it. Fine as registered.

## 1. SHOULD FIX (section 21): the first-night bed arrow overwrites and clears other arrows
- `introBedTick` sets `setGoal({ label: 'Your bunk' })` whenever its window is on and the escort isn't leading, without looking at `IX_GOAL`; it calls `clearGoal()` when the window ends or you reach the bunk, whatever the arrow is by then.
- Proven (d24b017 merge, `?nosave&debug`, New game, evening marked done, `skipTo` Monday 18:50, `setGoal` job board): `C 18:50 goal The job board, in the Works bay` → `C 19:01 goal ['Day 1, Monday 19:01', 'Your bunk']`. And with a job-board arrow set at 23:58 while the bed arrow was on: `C after midnight goal ['Day 2, Tuesday 00:01', None]`: the player's own arrow is wiped. The same happens to a device "Go there"/Roster arrow (sections 9218/9360/9435 call setGoal) or a job's arrow.
- Fix: set it only when `!IX_GOAL` (or IX_GOAL is already the bunk's); clear only when `IX_GOAL && IX_GOAL.label === 'Your bunk'` (as the escort's arrow already checks `mine`).

## 2. SHOULD FIX (section 21): `INTRO_UI` is never reset on New game; a second arrival in the same session loses Calder at the table
- `INTRO_UI.calder = true` is set at the Chief's step and never cleared (grep: no other assignment). After New game in the same page, the second evening never calls `crewComeTo('calder', '3-mess-9', …)`: the Chief doesn't come to your table (until a reload). Same for `INTRO_UI.step` (seen stale: after New game mid-walk `ustep: 'haulway'`), `calls`, `more`, `meet` (a queued meeting from the old game would send its gist Mail into the new one) and `bed`.
- Evidence: code (line `if ((I.step === 'chief' || I.step === 'free') && !INTRO_UI.calder && …)`); the probe B2 state dump above. The browser proof of the missing walk (probe D) did not finish.
- Fix: an `introUiReset()` called from `introNewGame` (and `introBegin`): clear `calder`, `step`, `meet`, `lines`, `more`, `calls`, `bed` (clearing its arrow), and `introSay`'s timers.

## 3. SHOULD FIX (sim engineer, section 10/14; test gap in intro_check): the Chief's seat at your table is taken
- On the d24b017 full merge with sim 0cf991a: at the Chief's step `heldBy('3-mess-9')` is **keane-davi**, settled from 18:17 to the end; Calder walks to 3-mess-35, then a tray, then sits at **3-mess-7 at [26, 0]**, not across from you (`introSeat('calder')` = 3-mess-9). Torres at 3-mess-12 and you at 3-mess-10 are fine. (probe A, `SEATS` every 6 looks, 18:12-18:34.)
- This is the lead's "Calder comes visibly to your table and you all sit". The sim's 0.26.29 note says the arrival's seats are "never shared", so it looks like the diners' seat choice (or the seat-taken rule from 0.26.30) doesn't respect Calder's named seat from 18:25. Not re-run on sim b9089d9 (probe C didn't finish), so check it on the current sim first.
- Also: intro_check part 8 should assert who holds 3-mess-9/10/12 at 18:35; today it only checks the steps.

## 4. Low (section 21, or section 19's New game): the health check is booked twice after a second New game
- New game doesn't reset `SHIP.device.appts` (no `newGame` listener in section 19), and `introBookHealth`'s guard is the intro's own `done` key, which New game clears.
- Proven (e270ee2 merge, two New games in one page, each skipped to Monday 05:02, then kept at 14:00 Tuesday): `"kept": [[1, "kept"], [2, "kept"]]`: two "New-crew health check" appointments with Rina at the same time, both kept. (The first one also stays in the device after the New game.)
- Fix: in `introBookHealth`, drop any `kind: 'health', by: 'rina'` appointment still in the future before booking; better, section 19 clears appointments on `simNote('newGame')` (tell the device engineer).

## 5. Low (section 21): the "Health check" item can never tick for some players
- Missed the Tuesday 14:00 appointment: nothing rebooks it (the plan: "if you miss it, it either happens later or arrives as Mail"). Skipped the arrival: `introSkip` books nothing, and SETTLE's `done` only accepts `'intro-health'` (never created) or the booked id, so a self-booked check-up with Rina doesn't count. Either way Calder's "Settled in" Mail and Record line are out of reach.
- Fix: tick on any kept appointment with Rina at the infirmary (`a.with.includes('rina')`), or rebook once on `apptMissed` for it.
- Also: `kind: 'health'` is outside section 14's documented kinds (`checkup` is the infirmary's, `apptKind`); `apptFree`'s work-ok test and social's memory key (`appt.health` vs `appt.checkup`) treat it as social. Use `'checkup'`.

## 6. Low (report vs code): "Tomas, Pell and Zainab come and find you"
- `socialSeekAsk` (social A d1e97bd: signature `(id, { from, until, why })`, returns bool, function declaration so no TDZ, typeof-guarded here, saved in `SHIP.social.seekAsks`, cleared by `socReset` on New game, `why` 'intro:d4-favour' matches its /favour/ test, Day 0 negative `from` fine) only waves you over when that person is already on your deck within `SEEK_NEAR` (10) and free. No plan block brings them to you (`where: 'seek'` plans nothing) and nothing happens if you're never near them: no Mail fallback. Probe (e270ee2 merge): asks registered `["pell", 3990, 4080, "intro:d3-pell", false]`, `["kovac-zainab", 5310, 5400, …, false]`, never done without being near. Either have the sim walk them to you (`crewComeTo`) in the window, or a Mail fallback; at least fix the DEV_NOTES/hook register wording.

## 7. Low (player engineer, section 15): you stand through "Dinner with Torres"
- `dinnerTick` seats you only from the Chief's step; the new `table` step (introDinner, 18:14) seats Torres (`introSeat` now includes 'table') but not you: probe A `act: null, sat: false` at 18:12-18:14, sitting from 18:17 (chief). Make dinnerTick accept `I.step === 'table'` too.

## Checked, fine
- The mug in play (e270ee2 merge): standing in the Tea corner on Deck 5 at Friday 10:33, `d5-mug:met` = 6390, flag `mug` set, toast "Friday tea — Halloran hands you a mug…", no Mail. The past-the-window path sends Halloran's Mail (code; `introLoad` keeps `:met` = -1 and the numeric `d2-health:appt` across a reload).
- The health check kept at 14:00 Tuesday ticks "Health check" (`settle_health` 2278); Rina is at `3-visit-1` (`appt`).
- Tour: all ten places reached on the walk; intro_check part 8 on the 54d7911 merge plays exactly the writers' lines per place (5,5,6,5,9,5,6,6,8,6). New game mid-tour (probe B): tour keys and lines cleared. Going to another deck mid-tour: the steps fall back as before (missed haulway, works, lift), no errors. Reload mid-tour: intro_check part 11 (real `?debug` storage, real `saveGame`, `goto`) OK; `tour:<id>` keys survive in `done`. The tour's queued lines are polled per frame, not timers; `introSay`'s setTimeouts (only 'free' now) fire on `introWalker()` at fire time, so a deck change just drops them.
- intro_check part 11 tests the real reload path (storage on, `?debug`), though it only asserts Torres is on the deck (`esc is not None`), not his distance or mode. Low.
- Save: two small keys in `SHIP.intro.done` plus tour keys (10); `seekAsks` 3 entries. No growth issue.

## Tests
- intro_check on the full 54d7911 merge: **OK**, all parts (0-11; 10: briefing with full cast in the Works bay; 11: reload mid-walk OK; draw-call peaks 175/208/273).
- name_check: `--branches 4f6d0b2 54d7911` OK; on the full merge OK.
- Probes (cadet_test Game, `?nosave&debug`): briefing timing (54d7911-era merge), health/seek/mug (e270ee2 merge), tour/New game/deck change/bed arrow/dinner seats (d24b017 merge).

## Not finished (stopped by the lead)
- intro_check on the arrival branch alone; day_check day 0 and 6 on the merge; the storage-on save probe (round-trip of the health booking and the mug across `?debug` reloads, save size); probe D (second arrival, Calder at the table) and probe C (who is planned on 3-mess-9) on the current sim b9089d9; the duplicate-health probe on the 54d7911 merge.
