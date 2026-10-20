# Dev mode plan: adversarial review 1 (DR1)

Reviewer DR1, 2026-10-20, for lead 20. Reviewed: `claude/devmode-plan` **v1.1, 6c837fd** (and v1, 2f7b9e4), `plans/devmode-plan.html/.md`. DJ1's report (`claude/devmode-dayjump`) wasn't on GitHub yet, so it isn't reviewed here. Every claim below was run on scratch copies of `claude/integration` 5dd740c (0.64.2 + step 2): playwright, Chromium, three r128, phone size 390 × 844. The scripts and their printouts are in `plans/devmode-review-1/`. Nothing in the game was changed.

## In plain words (for the user)

The plan is sound in shape: a hidden panel opened with `#dev`, its own save, and the day jump done by **replaying a steady player**. That's the right call, and the plan is honest that the steady player is the big piece of work. v1.1 already took in my early notes: no new button, a fixed seed, and "End and undo" for events.

What I found when I ran it:

1. **The replay is only repeatable with the seed fixed. v1.1 adds that, but check it's done everywhere.** Run the way Dev mode will really run (its own save, not "nosave"), two replays to Day 14 came out different. One got sick on Day 11 and ended with 92 xp; the other didn't, and ended with 104. The plan's "the same twice" was measured with "nosave", which hides this. Fixing the seed (v1.1) cures it: I found no other random source in the game.
2. **The plan's name for the switch, `DEV`, is already taken** by the device (`const DEV` at section 19). As written, the game wouldn't load at all. names_check catches it ("Identifier 'DEV' has already been declared"), so it would never reach you, but the plan needs another name.
3. **Kept days are thrown away "when the build number changes". But helpers never change the build number now**, only the build master does. So while helpers are testing their own work (the very time Dev mode is used most), an old kept day would be loaded into new code without anyone noticing. Stamp them with a fingerprint of the game file instead.
4. **The replay must freeze the clock between its chunks.** The plan pauses between days so the phone can draw. But the game's clock and crew run on every drawn frame, so the result would depend on the phone's speed. The plan's timings came from a test that never draws between days, so they couldn't show this.
5. **"Start promotion now" and "End now" each need a real change in someone else's section, not "a small hook".** The promotion test only opens on Day 9 or later, once you're "Relied on" and trained in making things safe. An event's ending sits inside `eventAdvance`; there's no function for it to call.
6. **Starting a tradition today moves people right now:** 20 of the 74 crew are somewhere else at once, and 57 have a different evening. The morning's plans stay the same (good). Ten other parts of the game read the traditions list (the galley, incidents, social and more), and the plan only re-plans the crew.
7. **The size is about 13-17 turns, not 8-10.** The steady player needs a line for each training and mechanic: 17 career rows plus the arrival week, chats and friendships. Each is owned by a different seat, and several have hands-on steps (the incident's valve, the round's marks). My quick steady player is still a Junior on Day 14: no drill, no "What's been tried?", no "Making it safe", no test. That's the same wall DP1 hit.
8. **Two things to add:** an **Undo** for every Dev action, since a Skip can end the career for good (let go on Day 20, gone on Day 21); and an easy way to get the real `#dev` link on a phone.

On the questions: I agree with the recommendations for q2, q3, q4, q5, q8, q9 and q10. **q1** needs a bigger tap area than the clock line (about 16 points tall today). **q6** matters less than it reads: the game already gives the same first-week points either way. **q7** is fine, but should also say that 20 crew move at once. I'd add three questions: an Undo, how many kept days to store, and whether a phone jump may take 2 minutes or should start from a kept day.

**Verdict: good to show the user after these fixes**: one blocker, eight should-fixes and a handful of nits. None of them changes the plan's direction.

## How the ratings work
- **Blocker:** the plan as written would break the game or give a wrong result without anyone noticing; fix it in the plan before the user signs off.
- **Should fix:** a real gap, a claim that's wrong or a cost not counted; fix it in the plan or say why not.
- **Nit:** small, wording or later.

## Blocker

### B1. Kept days are stamped with the build number, which no longer changes on helper branches
- **Plan:** 4.2 and Risks: "Stamped with the build number, and thrown away when it changes."
- **Evidence:** CLAUDE.md "How we work": helpers don't change the two build-number lines; only the build master sets them when merging. So every helper's branch, and every turn between merges, runs different code under the same `GAME_BUILD`. A kept day saved by yesterday's code loads silently into today's. That's exactly the case Dev mode is for (a seat testing its own change on Day 14).
- **Why it's a blocker:** a wrong state that looks right. A "bug" or a "fix" seen in Dev mode could come from a stale kept day and not from the code under test. Nobody would know.
- **Fix:** stamp kept days with a fingerprint of the game itself, computed in Dev mode only. For example, a quick hash of the main script's text at load (about 5 MB, a few tens of ms, never with Dev off). Also add the steady player's own version and the seed. devmode_check: change one character of the game, and the kept days must be dropped.

## Should fix

### S1. Determinism: the plan's "the same twice" was measured under nosave. v1.1's fixed seed is the cure, but it must be the whole cure, and proven
- **Evidence:** `plans/devmode-review-1/replay.py`, the same steady player in two modes, 30-minute steps, to Day 14:

  | Run | Seed (gs) | Sick day | xp Day 14 | Fingerprint (seed zeroed) |
  |---|---|---|---|---|
  | nosave #1 | 0 | none | 104 | 6d4879ac3143 |
  | nosave #2 | 0 | none | 104 | 6d4879ac3143 |
  | Dev save #1 | 630109002 | Day 11 | 92 | 2b7e1cf6329b |
  | Dev save #2 | 827155169 | none | 104 | 06ffcbfb385a |

  Dev save #2 differs from nosave only in `clothes.grime` (the clothes are on with saving on). With the game's odds (1 in 28 a day after Day 7, `SICK`), about 57% of games have a sick day before Day 30, so most unfixed replays would differ.
- **Checked:** the only `Math.random` / `Date.now` in game logic is `careerInit`'s gs (line 36912). So fixing gs in the Dev save (v1.1, one hook in `careerInit`) should be enough. The plan should **measure it**: replay twice *with saving on* in devmode_check (v1.1 lists this under risks; make it D1's or D5's check, not later).
- **Also:** the seed must be fixed *before* `careerInit` first runs, which happens lazily. A Dev save copied from an existing game (q2's third option) already has a random gs; say what happens then.

### S2. The switch's name `DEV` is already a top-level name (section 19)
- **Plan:** section 8: "Add `DEV = URL_FLAGS.has('dev')` next to DEBUG"; risks: "one switch, `DEV`"; section 25 "inside `if (DEV)`".
- **Evidence:** line 10807 `const DEV = { open: false, app: 'home', ... }` (the device's state, 73 uses of `DEV.`). On a scratch copy with the plan's line added, names_check says: `FAIL the game's script does not parse: Identifier 'DEV' has already been declared at section 19 (DEVICE), game line 10807`. The whole game would fail to load.
- **Also:** the plan's CSS class `.dev` sits next to the device's `.devsheet`, `.devbtn`, `.devhu` and `.devtip`, and the id `devBtn` is the Device button. **Fix:** a name like `DEVMODE` / `.devmode`, checked with `grep` and names_check, and written into owners.md.
- **Order:** `SAVE_KEY` (line 8989) is declared *before* `URL_FLAGS` (8991), so `SAVE_KEY + (DEVMODE ? '-dev' : '')` needs the flag read before line 8989, or the two lines swapped. Otherwise it fails with "Cannot access before initialization". The owner of section 13 reviews.

### S3. The replay in the live page must run frozen, with the frame-driven parts held
- **Plan:** 3.1 and Risks: "one ship day at a time, with a pause between days so the screen keeps drawing."
- **Evidence:** the main loop (section 12, lines 49861-49867) runs `tickShip(dt)` (real-time minutes onto the ship clock, then `apptTick`, `shiftTick` and `careerTick`), `galleyTick`, `worksTick`, `eventsTick`, `socialTick`, `introTick` and `worksCareerTick` **on every frame unless frozen** (`run = !freezeSync()`). Section 20's crew seeking you out and chatter (`playerHeard`) and section 21's tour also pace themselves by `simNow()`. During a pause between days, all of these move the state by however many frames the phone drew. DP1/DJ1 measured inside one `page.evaluate` with no frames, so the timings and fingerprints couldn't show it.
- **Fix:** hold `PAUSE.on` (or a Dev freeze through `freezeSync`) for the whole replay, with no deck crew drawn until the end. Turn off toasts, tips, bubbles and the address banner, or make them quiet. DJ's tips-off changes saved flags (`c.k` tip bits), so prefer "quiet" to "off". devmode_check: replay to Day 10 in the *live page with frames between chunks*, twice, and get the same fingerprint as the one-task replay.

### S4. "Start promotion now" needs more than a hook in 24p
- **Plan:** 3.2: "sets your test job for today ... uses section 24p's own test-day setting, through a small hook."
- **Evidence:** `SHIP.works.test.day` exists, but the test only starts when the ladder opens row t2 (`ladderTick`, line 41735). That needs `d >= r.day` (Day 9), `ladderNeeds` (Relied on and trained m6), no training under way (`W.cur`), no big row opened that day, Calder or Vance on shift (`ladderTeacher`), and before 14:00 (`PROMO.until - 60`). `SHIP.works` doesn't even exist before Day 1 at 17:00. On a Monday, Day 3, setting the test day does nothing.
- **Fix:** say what Dev does. It could call `ladderOpen(row, d, t)` directly after setting `W.test` (bypassing the needs; a change to how 24 core is used, reviewed by its owner). Or it could refuse with the reason ("Needs: Relied on; trained in making things safe. Jump to Day 9 instead"). Plus what happens after 14:00 and on days off.

### S5. "End now" and "Start now" for events don't match section 18's code
- **Evidence:** the ending (score, traces, log, debrief, commendation) is **inline in `eventAdvance`** (lines 35476-35488), and only fires when `t >= startDay + days`. There's no function to call. Options: split it out (a change to section 18's shared code, so its owner goes first), or move `startDay` back so the end has passed. The second rewrites `eventNow` for the whole past span, re-plans, and logs a wrong `endDay`.
- "Start now: the warning starts at the next quarter hour": phases are fixed `[day, minute]` in the event's data (the storm's warning is `[0, 360]`, 06:00). `eventStart(id, day)` takes a day only. Started at 15:00 today, the warning has already begun (and its Day-0 meetings, like Calder's 09:15 briefing, are missed). Started tomorrow, you wait. Say which, or plan a minute offset (another section 18 change).
- The events plan counts F6 as 1 turn inside F0-F8 (12-15) and orders F0-F8 *after* Dev mode. DP1 counts it again as D8, and its phase jumps wait for F4, which comes later. Settle this with the events planner: either D8 is F6 (and the events plan drops it), or D8 is the start/threads/end-and-undo part and the phase jumps come with F4.

### S6. Starting a tradition today: the plan re-plans the crew, but nine other parts also read `eventsOn`
- **Evidence** (`replan.py`): Day 3 at 15:40, a Dev-list tradition at 16:00, then today's plans dropped and made again (eventOneOff's way):

  | | Changed (of 74 crew) |
  |---|---|
  | segments that ended before now | **0** (good: the past stays) |
  | where they are right now | **20** |
  | their evening | **57** (one tradition reshuffles nearly everyone) |

- owners.md: `eventsOn` is read by sections 14, 19, 15, 16, 20, 20c, 23, 24c, 24f and 10. Some work things out once and keep them: the galley's cake day, 24f's incident plan (which avoids tradition days and the morning before a tradition evening), the device's calendar and section 20's invitations. A mid-day change to `eventsOn(today)` makes them disagree with what was decided earlier. In a Dev save that may be acceptable, but the plan says "one line in eventsOn", and that is a change to a shared function's result in Dev mode. So per owners.md the traditions engineer reviews it, and the plan should list each reader and what it does: re-reads, keeps the old answer, or is refreshed by Dev.
- A tradition "in 20 minutes" can fall inside the day shift (16:00 above): only crew who are free go. Say so on the panel ("11 going").

### S7. The size: about 13-17 turns, not 8-10
- **The steady player (D5-D6, planned as 2 turns).** My run (`replay.py`, Days 1-14): trained m1, m4, m3i, m5, m7, m2. Still missing by Day 14: **m3d** (the Wednesday drill isn't attended), **p3** (a small row that needs a use), **m6** (the Day 8 incident call; 24f has hands-on steps: a valve chosen from the pipe, mop, then the fix), and so **t2**: still Junior on Day 14. The same wall as DP1's. Each mechanic (17 rows in `CAREER_LADDER`, sections 24a-24t) needs a paper line written by or with its owner. The arrival week with saving on needs the escort steps (`introAdvance(t, here)`, intro_check has a paper driver). Friendships need arc_check's "diligent player". mech_check's `PARTS` already know how to do each mechanic's steps on paper; the plan should say they're the starting point (they set state by hand, e.g. `W.tr.m6 = 8`, so they need adapting). Realistic: 4-6 turns, owners included.
- **D1-D4:** the Dev save, the name and order fixes, the panel, Clock with "settle what's mid-flight", Career, and Traditions with ten readers: 5 turns, not 4.
- **D8:** the snapshot for End and undo, the ending split, the minute offset: 2 turns.
- **D7:** the fingerprint, kept days with a quota guard, Stop, the reload path, phone timing: 1-2 turns.
- **devmode_check** itself: it must stay under a minute to join check_fast. A Day 10 replay is about 10 s, so fine, but the "Officer on Day 10" milestone can't pass until D6 is done. Say it starts as "not yet" (like mech_check's rows not in the build), so check_fast doesn't go red in between.

### S8. An Undo for Dev actions
- **Evidence** (`skiponly.py`): a skip-only player is let go on Day 20 and the career ends on Day 21 (`c.end`). After that the Dev save is a finished game. A one-big-jump skip (Day 12 to 20, `probe1.py`) never gets let go (`c.go` null), so the step size changes the outcome. The plan steps by 30 minutes, which is right. v1.1 gives events "End and undo", but nothing else can be undone: a Skip, a set xp or a started tradition.
- **Fix:** keep the save from just before each Dev action (one slot, the Dev key + "-undo") and an "Undo last" button. That's cheap, and it answers "test it, then try again", which is the user's main use.

## Nits

- **N1 (q1).** The clock line is about 16 px tall (12.5 px font) and `.hud` is `pointer-events:none` today (line 15), so taps pass through to the deck. Making it tappable in Dev changes what a tap there does, and the target is well under the plan's own 26 pt (Apple's guide is 44). Make the whole place-and-clock card the Dev target in Dev mode. Screenshot: `plans/devmode-review-1/hud-390x844-day27.png`.
- **N2.** The device already has a bottom sheet (`body.devsheet`, toasts move to `66vh + 12px`, line 190). The Dev sheet must not open over it, and toasts must clear it too. Add both to devmode_check's screenshots, with a dialogue and a chat card showing.
- **N3. Kept days share the origin's storage with the real save.** About 7 × 100-120 KB plus the Dev save plus an undo slot comes to about 1 MB of a 5 MB origin limit. That's fine, but `saveGame` swallows a full store silently (line 9011, "the game carries on unsaved"), so a full store would stop the *real* game saving without a word. Cap the kept days and check the space before writing.
- **N4.** A hash change doesn't reload the page. Adding `#dev` to an open real game shows nothing; removing it from a Dev tab stays in Dev (still labelled, so harmless). Listen for `hashchange` and offer a reload.
- **N5.** On a phone in the Claude app you can't easily type `#dev` onto an artifact link. Plan to give the user the ready-made Dev link at each stop, and check at Stop 1 that the reload at the end of a jump keeps `#dev` inside claude.ai's frame.
- **N6 (q6).** intro_check part 5 says skipping the arrival gives "the same points, flags and steps as after the arrival evening". So the arrival's first friendships exist either way. q6 matters for testing the arrival itself and its time cost (an extra paper evening with escort steps), less for believability. Reword it.
- **N7.** A replay day is one JavaScript task: about 0.8 s on desktop, 4-5 s at the 4× phone stand-in. So "Stop" can take a few seconds to answer. Half-day chunks (frozen, S3) would help.
- **N8.** Saving on costs about 15-20% more replay time (Day 14: 10.0/10.6 s nosave against 12.1/11.7 s with the Dev save). Re-measure the phone numbers with saving on.
- **N9.** Checked and true: 60 traditions; 3 waiting for a flag (`rec-film-night`, `rec-all-hands`, `bridge-hour`); `eventStart` doesn't check drafts; the planner reads `SHIP.event` (`evChanged`); `.hud` holds the clock; "let go on Day 20" for a skip-only player.

## Leaks into the normal game and the real save (asked for in my brief)

- **With Dev off:** nothing in the plan runs except the name-guarded hooks: `SAVE_KEY`/`INTRO_KEY` suffixes, a fixed-seed branch in `careerInit`, the `eventsOn` line, and the CSS under a class that's never set. With S2's rename, cadet_test ALL IDENTICAL is plausible, and the plan proves it every turn. One thing to add to devmode_check: with Dev off, `localStorage` holds only the two real keys and no `-dev`, `-undo` or kept-day keys (v1.1 has the `-dev` part).
- **The real save:** the plan is right that only two names exist (I found no others: `localStorage` appears 7 times, all through `SAVE_KEY` or `INTRO_KEY`, plus `introWanted`'s literal copy, which the plan covers). `?debug` alone writes the real save (DEBUG doesn't imply NOSAVE), so devmode_check should also prove `#dev.debug` stays on the Dev key. The remaining risks are N3 (the shared quota) and N4 (hash changes).

## The questions, one by one

| q | DP1's recommendation | DR1 |
|---|---|---|
| dm-q1 | `#dev` + tap the clock | Agree with `#dev`; make the whole HUD card the target (N1); give the user the link (N5) |
| dm-q2 | its own save | Agree; plus the fixed seed proven with saving on (S1), an undo slot (S8) and the quota guard (N3) |
| dm-q3 | (a) replay + kept days | Agree; stamp with the game's fingerprint (B1); replay frozen (S3) |
| dm-q4 | steady now | Agree; steady alone is 4-6 turns (S7) |
| dm-q5 | two buttons | Agree; Skip should say it can end the career, and offer Undo (S8) |
| dm-q6 | yes, arrive by shuttle | Fine either way; the points are the same (N6); costs one more paper evening |
| dm-q7 | today, under the lift's fade | Agree; tell the user 20 of 74 move and 57 evenings change; list the other nine readers (S6) |
| dm-q8 | yes, approximate | Agree |
| dm-q9 | three stops | Agree; with 13-17 turns, Stop 2 (the day jump) is the long one |
| dm-q10 | keep, hidden | Agree; it costs nothing with Dev off once S2 and N3 are done |
| missing | | **Undo** (S8); **how many kept days** (storage, N3); **a 2-minute first jump on a phone, or a kept day made on the computer first?** |

## How this was run
- `plans/devmode-review-1/probe1.py`: plain `skipTo` jumps to Days 3, 8, 12, 20 and 27; the HUD shot at 390 × 844.
- `replay.py GAME MODE DAYS` (MODE `nosave` or `devsave`: a scratch copy with the keys suffixed `-dev` and no nosave, fresh storage): a steady player like DP1's description (clocks in and out, keeps training meetings, watches, does training jobs, else the board's top job) in 30-minute steps, then sleeps to 06:00. It prints the rank, xp, trained rows, misses and sick day each day, and a fingerprint of the save with the seed zeroed. Printouts: `out_*.txt`.
- `replan.py`: Day 3 at 15:40, a Dev-list tradition at 16:00, plans made again; it counts the changed past, present and evening segments.
- `skiponly.py`: skip-only, 30-minute steps, Days 1-30: misses, the warning steps, let go, the end.
- names_check on a copy with the plan's `DEV` line (S2).
- Setup as DEV_NOTES "Testing"; each run in its own `CADET_WORK`.

## Re-check of v2 (claude/devmode-plan 97da6b9), 2026-10-20

In plain words: **every one of my findings is fixed in v2**, including the blocker. Two new gaps, both small: "Excused" skips have no mechanism or hook yet (the game's leave runs out after 3 days), and the first-week meetings need the real deck drawn, which costs time in the replay.

| Finding | v2 | Status |
|---|---|---|
| B1 kept days stamped with the build number | the game script's fingerprint + the steady player's version + the seed; devmode_check changes one character and the kept days must drop (4.1, risks) | **fixed** |
| S1 random seed | gs from the Dev seed (career engineer's hook); "two saving-on runs identical" in D2's devmode_check; DP1's v2 measured the same twice with saving on, seed 1 | **fixed**. One thing left: say what *Copy my real game* does with the copied save's random gs (keep it = that game's luck, not repeatable; or replace it with the Dev seed) |
| S2 `DEV` taken, order of SAVE_KEY | `DEVMODE`, `.devmode`, declarations swapped or read first, "no top-level name already in use" | **fixed** |
| S3 the replay must freeze | freezeSync for every Dev action; frozen half-day pieces; crew placed once at the end; pop-ups quiet, not off | **fixed** |
| S4 Start promotion now | needs shown; `ladderOpen` only when just the day is missing, agreed with 24's owner | **fixed** |
| S5 End now / Start now / F6 | End and undo by default; End and keep waits for the split (section 18 owner, with the events plan); start today if its first phase is still ahead, else tomorrow; F6 shrinks in the events plan | **fixed** (the events plan must actually be edited to match; the lead tracks that) |
| S6 ten readers of eventsOn | the readers table with each one's behaviour; traditions engineer reviews first | **fixed** (the table is right against owners.md; "keeps its answer" for 16, 20/20c, 24c and 24f is said on the panel) |
| S7 the size | 13-17 turns, 3 stops, Officer-on-Day-10 starts as "not yet" | **fixed** |
| S8 Undo | Undo last for every Dev action (q11) | **fixed** |

### New, from v2

- **V2-1 (should fix): "Excused" has no mechanism or hook.** v2 (3.2): "A skipped workday counts as leave." But the game's leave is real state: 3 days to start (`CAREER.leave`), +1 every 28 days, at most 5. It must be booked before 08:30 the day before (`careerCanBook`), and it's spent (`c.l--`). So "Excused" by real leave runs out after 3 skipped workdays, uses up the player's leave, and can't excuse today once the shift has started. Leave also feeds `careerOff`, which feeds `playerShiftOn`, read in 42 places, the crew planner (section 14) among them. Checked on a scratch copy: a new game's `c.l` is 3. **Fix:** a Dev-only "excused" list read in `careerOff` (one line, the career engineer, section 20). It's set before a day is planned, and for today mid-shift the miss isn't counted (one line in `careerTick`'s miss loop). Add both to section 9's hook list.
- **V2-2 (should fix, small): the needs hook isn't listed.** "Needs kept as a normal day would leave them" changes section 15's skip step (`SIM_ADVANCE` at line 13533, `needsDrain`). That's the player engineer's, so add it to the hook list. Top up needs is Dev-only, so it's fine in section 25.
- **V2-3 (nit): the first week in person costs deck changes.** `inMeeting` needs `deckDef.num === w.deck` and the player in the room, and the speaker check falls back after 10 minutes (`introWeekMeetings`), so frozen crew are fine. But the replay must `goToDeck` for each first-week meeting and back. Measured on a scratch copy (`deckswap.py`): 0.3-1.7 s a deck change on a computer (Deck 3 the slowest), so roughly 5× on a phone. Count it in D7's timing, and check memory over those round trips (deck_check's rule).
- **Checked true in v2:** the readers table matches owners.md; `inMeeting` and `introWeekMeetings` read as v2 says; `#dev.debug` stays on the Dev key by design (the `SAVE_KEY` suffix).
