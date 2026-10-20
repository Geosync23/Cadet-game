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

## Quick check of v3, the lean Dev mode (claude/devmode-plan 2cc8898), 2026-10-20

In plain words: **Set career works, with three conditions.** I ran a rough Set career on a scratch copy: a Dev save, workdays excused day by day, the career written each morning from the ladder's days, Officer from Day 10, then Day 11 played as a player who doesn't turn up. It ran with no errors. The career exists and survives a save, and the ladder carries on correctly (Day 11 offers Team jobs, m8). The three conditions:
1. Start the Dev game with **Skip to Monday**, not by shuttle.
2. Write the **opened** rows (`op`) as well as the trained ones (`tr`).
3. Expect the storm's missed-meeting Mail.

Scripts: `plans/devmode-review-1/setcareer.py` (by shuttle, beats marked done) and `setcareer_skip.py` (Skip to Monday). Printouts: `out_setcareer_*.txt`.

| What the lead asked | Result |
|---|---|
| The career exists (`SHIP.works` after Day 1 17:00) | yes: `worksInit` from Day 2's morning; rank, tier, `home` (the cabin, 4-23), `done` (summons2, ceremony2, move2, and the game added cake2 itself) all kept by `worksClean` after a save |
| Officer on Day 10 | yes (set from Day 10's morning); `playerBed()` is the cabin, so "wake in your bed" wakes you in the cabin |
| The ladder carries on | **only if `W.op` is written too.** With `op`: Day 11 opens m8 (ask, then meeting), as for a real Officer. With only `tr`: Day 11 re-opens **m3i, the inspection, already trained** (`worksOpened` reads only `W.op`; `out_setcareer_noop.txt`) |
| No missed-meeting Mail | none from the first week. There is "Storm briefing (notes)" (the storm's Day 10 briefing, missed while excused), plus "Recycler membrane change (notes)" from my Day 11 no-show (expected). The storm one is the "no part in the storm" v3 already lists; say it on the panel |
| Settling-in, Zeke's lines | with Skip to Monday: every week flag set (`intro.device`, `met.calder`, `week1.d2`-`d7`, `week1.done`), the arrival ended, no clock trouble. Not set: `mug`, `seedling` and the Settling-in ticks (`SHIP.intro.settle` empty). That's approximate and fine, but list it in "What's set" |

### Findings

- **V3-1 (should fix): "A new Dev game by shuttle" then marked beats stops the clock at Day 0.** While the arrival is on its first step, `introTick` sets the clock back to **Day 0, 17:30 on every frame** (line 40016: `if (I.step === 'manifest') { SHIP.time.day = INTRO_START.day; ... }`). Marking `SHIP.intro.done` doesn't move `I.step`. In my run, the first frame after reaching Day 11 put the clock back to Day 0 17:30 (`out_setcareer_shuttle.txt`: `step "manifest"`, the week's flags unset). **Fix:** Set career starts with `newGameStart(false)` + `introSkip()`. intro_check part 5 says that gives the same points and flags as the arrival evening. Then mark the first-week meetings `:met` before the skip passes them, and let the game's own week run set its flags (it did). That also answers v3-q2: "always new" is fine, but **by Skip to Monday**.
- **V3-2 (should fix): write `W.op`, not just `W.tr`.** Each trained row must also sit in `W.op[its day]`, or the ladder offers it again (seen: m3i re-opened on Day 11). devmode_check: after Set career to Day N, play Day N+1 and expect no row that's already trained to open.
- **V3-3 (should fix): set the fresh-save start switch first.** A brand-new Dev save has `INTRO_BOOT` on (no save, not nosave), so the first `introTick` frame calls `newGameStart(true)` and starts the arrival over whatever Dev mode has done. In my first run it wiped a finished Set career back to Day 0. D1 should let that first frame happen before any Dev action, or clear `INTRO_BOOT` when Dev mode starts its own game (a section 21 hook, owner first).
- **V3-4 (nit): with no fixed seed, two Set careers to the same day can differ.** About 57% of games have a sick day by Day 30 (`gs` random). Mark and Undo are exact, so for the user that's fine. But devmode_check can only compare fields, not save bytes, unless the one-line seed hook stays (Dev only, cheap). Say which.
- **V3-5 (nit): the hooks list.** Add **20 (social)** for "friendships get a starting level" (that writes `SHIP.social`, so the social engineer's shapes apply), and **21** for `introSkip` + `INTRO_BOOT` (V3-1, V3-3). The rest (13, 15, 18, 20 excused, 24/24p, page) matches what v3 does. The pip: `promoPip()` isn't called by writing `W.done`, so the collar may show no pip until something calls it. Call it after Set career.
- **Stop 1 and the dropped parts:** nothing in Stop 1 needed the replay, the kept days or IndexedDB. Mark, Undo and Copy my real game are plain localStorage saves, three at about 120 KB each, well inside the limit. The only thing that leaned on the dropped seed is devmode_check's repeatability (V3-4).

## Owner review (standing in for the sim engineer, section 13, and the onboarding engineer, section 21): Dev mode D1 hooks, claude/devmode fffb8e2

**PASS WITH FIXES** (none of the fixes blocks a merge; the game's behaviour with Dev off is proven unchanged).

Reviewed: c9cc785 (13: `DEVMODE = URL_FLAGS.has('dev') && !NOSAVE`, `SAVE_KEY` moved below the switches with "-dev"), 55add3f (21: `INTRO_KEY` "-dev", `introWanted` reads `INTRO_KEY`), and the rest of D1 (section 25, devmode_check.py) for anything that could touch the real game.

What I ran (scratch copies, 390 × 844):
- **cadet_test** integration 5dd740c against devmode fffb8e2: **ALL IDENTICAL** (0 px everywhere, no errors).
- **devmode_check** on fffb8e2: **DEVMODE CHECK OK**.
- **names_check**: OK (3823 names).
- **The real game's storage, byte for byte** (`savecmp.py`, `savecmp2.py`, `out_savecmp.txt`). The same session in both builds, starting from the same real save: no switch, `#debug`, `?nosave`, `#nosave.dev`, `#debug.nosave`, and again with `starship-cadet-arrived` present. Every storage key came out **identical** between the two builds, with the career's random `gs` zeroed (it's random in both). With `#nosave.dev`, `DEVMODE` is false. A `#dev` session over a real save plus the arrived key left both real keys unchanged and wrote only `starship-cadet-save-dev`.

Checked by reading:
- **Load order:** nothing reads `SAVE_KEY` or `SAVE_V` above their new line 8998 (first use: `saveGame`, 9005). `INTRO_KEY` (39124) is read by `introArrived`, `introMarkArrived` and `introWanted`. The only call at load is `INTRO_BOOT` at 39360, after 39124. The others are called at run time (New game, the career's end card).
- **No other copy of the key texts:** in the game, each text appears once (8998, 39124). Outside it, they appear only in docs and in devmode_check's own list (`REAL`), which is right.
- **The shared rule:** neither key is read outside its own section. No shared function's inputs or result change. `DEVMODE` is a new name owned by 13 and read by 21 and 25.
- **Section 25:** every function returns at once with `DEVMODE` off, and only the `hashchange` listener is always registered. It acts only when the `dev` word appears and never writes storage. Its Dev state goes into the Dev save only (`SAVE_EXTRA` is pushed only under `DEVMODE`).

Fixes (suggested patches; I don't push to claude/devmode):

1. **Should fix: devmode_check doesn't test the intro key, and can't catch an added real key.** In `part_off` the real game never finishes the arrival, so `REAL` storage is only `starship-cadet-save`, and `real` (the bytes kept) has no `starship-cadet-arrived`. Also `dev_keys_ok` accepts any REAL key, and the loop only compares keys that existed before. So a Dev session that *wrote* the real arrived key would pass. Patch for `part_real`:
   ```python
   -    pg = Page(ctx, ''); pg.ev('saveGame()'); real = {k: v for k, v in store(pg).items() if k in REAL}; pg.close()
   +    pg = Page(ctx, ''); pg.ev('saveGame()'); real = {k: v for k, v in store(pg).items() if k in REAL}; pg.close()
   +    for gone in (False, True):     # both ways: the real arrived key absent (a Dev session must not add it) and present (must not change)
   ```
   Simpler and enough: run the Dev part twice, once as now and once after `pg.page.evaluate("localStorage.setItem('starship-cadet-arrived', '1')")`. In both runs, check `{k: v for k, v in st.items() if k in REAL} == real` (the same keys *and* bytes), not just `st.get(k) == v` for the old keys. In the Dev session, also call `introSkip()` so the Dev side writes its arrived key (`starship-cadet-arrived-dev` must appear, and the real one mustn't).
2. **Nit: a stale comment in 21 (line 39382).** "(a function declaration reading the key directly: section 13 asks this at load, before this section has run)" is no longer true: it reads `INTRO_KEY`, and the only load-time call (39360) comes after it. Patch:
   ```
   -// (a function declaration reading the key directly: section 13 asks this at load, before this section has run)
   +// (reads INTRO_KEY, so never call it above line ~39124: in the dead zone its try/catch would quietly say false and the arrival would never start)
   ```
3. **Should fix (docs, same commit per CLAUDE.md): owners.md and map.md.** Add section 25 (owner: the Dev mode engineer), its slot (map.md "Each seat's slot"), and `DEVMODE` as a shared name: owner 13, read by 21 and 25. `SAVE_KEY`/`INTRO_KEY` now depend on it.
4. **Nit: the hashchange word test doesn't match the link parser.** Line 8994 reads a token's name up to its first "-" (so `#dev-1` turns Dev on), but the listener tests `t === 'dev'`, so it would offer "Dev link removed" in a Dev page opened with `#dev-…`. Patch: `const on = location.hash.slice(1).split('.').some(t => (t.includes('-') ? t.slice(0, t.indexOf('-')) : t) === 'dev');`.

Waiting for D2's third hook (13: `freezeSync` and `saveGame` read `devmodeHold()`).

## Owner review, round 2: Dev mode D2/D3 hooks (claude/devmode 78b4985)

**PASS WITH FIXES.** With Dev off, all four hooks are proven no-ops. One should-fix concerns DB1's rule for excusing workdays.

Hooks: 58d63a4 (13: `freezeSync` and `saveGame` ask `devmodeHold()`), e02c085 (20: `careerOff` reads `devmodeExcused(d)`), b1de9f6 (15: the skip step skips `needsDrain` while held), 9d96a16 (11: the SIM_ADVANCE `deckCrewFill` is skipped while held).

Dev off (all run on 78b4985 against integration 5dd740c):
- **cadet_test: ALL IDENTICAL.** **day_check: OK.** **leave_check: OK.**
- **career_check:** fails `busy: "Relied on" before Day 5` with output **identical to integration's**. That's backlog row 12, known and accepted, so it isn't from Dev mode.
- **Real storage byte for byte** (`savecmp.py`/`savecmp2.py`): identical between the builds with no switch, `#debug`, `?nosave`, `#nosave.dev` and `#debug.nosave`, and with the arrived key. A `#dev` session leaves both real keys untouched.
- **By reading:** each hook short-circuits on `typeof devmodeHold === 'function' && devmodeHold()`, which is `DEVMODE && DM_HOLD` and false with Dev off. Both are hoisted (function declaration, `var`), so the hooks are safe at any load point. `devmodeExcused` returns false at once with Dev off, and at load it reads `SAVED.dev` (absent from a real save).

**DB1's "no careerTick line needed": true.** Every miss and leave path goes through `careerOff`/`playerShiftOn`: the miss loop (`careerRota(k) && !careerOff(k)`), `careerDayEnd` (returns on `careerOff`), the run counter `c.ms` (only from the miss loop), `c.on` (needs `!careerOff`), the clock-in reminder and `shiftTick`'s shift-start note (both `playerShiftOn`). Leave earning and sick days are unaffected.

**Should fix: the excuse rule turns a late start into a lost day, even when nothing could be missed.** DB1 excuses a day when a jump crosses any part of 09:00-12:30 with you not clocked in. Through `careerOff`, that makes the day a day off: no clocking in, no jobs held for you, no ladder row that day. Measured with `excuse.py` (Dev on, a fresh Dev save via Skip to Monday):

| Jump | Excused | Can clock in after | Your jobs on the board by 16:00 |
|---|---|---|---|
| Day 2, 08:00 → 08:55 | no | yes ("in") | 4 |
| Day 2, 08:00 → 09:30 | **yes** | **no** | **0** |
| Day 9, 08:00 → 10:00 | **yes** | **no** | **0** |
| Day 9, 09:30 → 09:40 (ten minutes) | **yes** | **no** | **0** |

The normal game never reaches these states. Leave can't be booked after 08:30 the day before. Until 12:30 a player who arrives late can still clock in, and is only late. On Days 1-7 (`CAREER.grace`) a miss never counts at all. Excusing Day 2 is exactly what breaks the user's first real use (the Day 2 morning recipe): one hop past 09:00 and Day 2's work is gone. On Day 9 the Tier 2 test job stayed held for a player now "off" (`repair/20`).

Patch (section 25, `devmodeSkipTo`): excuse only what the game would count as a miss. That's a day after the grace week, whose 12:30 the jump reaches or passes, with you not clocked in:
```js
-      const a = (d - 1) * 1440 + DAY_SHIFT[0], b = (d - 1) * 1440 + CAREER.missBy;
-      if (to <= a || from >= b || !careerRota(d) || careerOff(d) || careerClockedIn(d)) continue;
+      const b = (d - 1) * 1440 + CAREER.missBy;           // the minute the game counts a miss (careerTick: m >= missBy)
+      if (d <= CAREER.grace || to < b || from >= b || !careerRota(d) || careerOff(d) || careerClockedIn(d)) continue;
```
A jump that ends before 12:30 leaves you late but able to clock in, as in the game. The Clock tab's text and devmode_check's expectations change to match ("excused once the jump passes 12:30, from Day 8").

**Nits**
- **`devmodeSettle` doesn't take you out of a shower or booth line** (`queueOut(false)`, as `newGameStart` does). Sleeping can't start from a line, but a Dev jump can, so you'd come back hours later still queued. Add `if (typeof queueOut === 'function') queueOut(false);`.
- **A hold that never ends:** `devmodeLoad` and `devmodeClear` set `DM_HOLD = true` and then `location.reload()`. If the reload doesn't happen (blocked, cancelled), the game stays frozen and never saves. Add a safety: `setTimeout(() => { if (DM_HOLD) { DM_HOLD = false; devmodeSay('The reload didn\'t happen: nothing changed.'); } }, 4000);`. The Dev save was already written, so say "reload to see it".
- **`devmodeLoad` writes the Dev save without `devmodeWrite`'s space check.** It's the same size as what it replaces, so that's fine, but say so in a comment.

## D4 review: Take me to, Mark here / Back to mark (claude/devmode bb6e78a)

**PASS.** No new hooks: every game change in bb6e78a is inside section 25 (diff hunks from line 49856 on), so the six hooks reviewed in rounds 1 and 2 are still the full list. Ran: cadet_test against integration **ALL IDENTICAL**, devmode_check **OK** (all six parts, including "move: 148 rooms" and "Mark and Back to mark byte for byte, twice"), names_check OK.

- **Take me to** runs under `devmodeDo` (the Undo kept first, settled, frozen under the fade), refuses during the arrival and inside a meeting (`devmodeStory`), and closes the lift panel before `goToDeck`. Landing in a room where a meeting is due starts it, which is what "Next appointment" is for.
- **Mark** goes through `devmodeWrite` (space check) and keeps the arrived key too. **Back to mark** keeps an Undo, then reloads through `devmodeLoad`. The real keys are only ever read.
- **Nit: two rooms you can't walk out of.** `locked.py` took me to every room of every deck. All rooms except two have a walking way back to the lift: the **Probe bay (Deck 2, P)** and the **Bay door gear (Deck 5, d**, the hidden door gear already on the backlog). devmode_check lists the same two. Take me to works from anywhere, so it's never a dead end, but mark them in the room list ("no way out on foot: use Take me to").
- Still open from round 2 (in DB1's fixes commit): the excuse rule, `queueOut` in `devmodeSettle`, and the reload safety. devmode_check's clock part expects `excused [1, 2, 3, 4, 5, 8]`; with the patch it becomes `[8]` (Days 1-5 are in the grace week), so the check changes with the fix.

## Final check for Stop 1a: DB1's fixes (claude/devmode 305b572 + 0c33f5a)

**PASS for merging into claude/integration, with one fix to make before the user gets the Dev link.** With Dev off the game is proven unchanged, and every round 1, round 2 and D4 item is in. DB1's 4-second safety loses an Undo when the reload is merely slow, which on a phone over the Claude app is likely.

Re-run on 305b572:
- **cadet_test** against integration: **ALL IDENTICAL** (renderer noise only). **devmode_check: OK**, now with the arrived-key and short-hop tests, excused `[8, 9]`. names_check OK.
- **savecmp / savecmp2:** the real storage is byte-identical to integration's with no switch, `#debug`, `?nosave`, `#nosave.dev`, `#debug.nosave` and the arrived key. A `#dev` session leaves the real keys untouched.
- **excuse.py:** Day 2 08:00→09:30, Day 9 08:00→10:00 and Day 9 09:30→09:40 now excuse **nothing**, and you can clock in after each, as in the game. The rule is exactly my patch.
- `queueOut(false)` in `devmodeSettle`, the `#dev-…` parse, and 21's comment (0c33f5a) are all in. owners.md and map.md are updated.

**Should fix before the user's Dev link: the 4 s safety can undo an Undo.** `devmodeReload` lets go of the hold after 4 s and calls `saveGame()`. But a reload that's only slow keeps the old page running until the new page arrives. So the old page writes its current game over the kept save, and the new page then loads that. `devmodeUndo` has also already deleted the Undo record. Measured (`slowreload.py`: Dev on, a +3 h jump, then Undo, with the page served over http and its reload held back):

| Reload takes | After the reload | Undo record |
|---|---|---|
| 2 s | Day 1 06:00: **Undo happened** | gone (used) |
| 6 s | Day 1 09:00: **Undo didn't happen**, with no message (the reload wiped the panel) | **gone: it can't be tried again** |

The same goes for Back to mark and Copy my real game: they silently don't happen, though their records survive. Clear: Mark and Undo are cleared, and the Dev save is written back.

DB1's reasoning ("the next save would overwrite the kept save anyway") is the problem: the next save only happens because the hold lets go. Keep the hold until the new page takes over. Then the kept save stays in place however long the reload takes. If the tab is closed, the `pagehide` save is held too, so the next opening loads the kept save and the action happened. Patch:
```js
-function devmodeReload(why) {                             // reload; if the browser hasn't after 4 s, carry on as you were and say so
-  devmodeSay(why + ': reloading…'); location.reload();
-  setTimeout(() => { DM_HOLD = false; saveGame(); devmodeSay('The page didn\'t reload, so ' + why + ' didn\'t happen. Try again.'); }, 4000);
-}
+function devmodeReload(why) {                             // reload, staying held (frozen, unsaved) until the new page takes over: the kept save stays in place
+  devmodeSay(why + ': reloading…'); location.reload();
+  setTimeout(() => devmodeSay(why + ': still reloading. If the page doesn\'t come back, reload it yourself: nothing is lost.'), 4000);
+}
```
And in `devmodeUndo`, don't delete the Undo record before the reload: drop `localStorage.removeItem(DM_KEY.undo)`. A second Undo then goes back to the same moment, which is harmless. If DB1 wants it gone, set a `sessionStorage` flag before the reload and remove the record on the new page when the flag is there. devmodeLoad's "browser wouldn't store it" branch already lets go correctly, since nothing was written.

Stop 1a's six hooks, final: 13 (`DEVMODE`, `SAVE_KEY`; `freezeSync`/`saveGame` ask `devmodeHold`), 21 (`INTRO_KEY`, `introWanted`), 20 (`careerOff` reads `devmodeExcused`), 15 (needs kept while held), 11 (`deckCrewFill` once). All are reviewed and proven no-ops with Dev off.

## Final Stop 1a verdict (claude/devmode fa394b3, with c521577)

**PASS.** The slow-reload fix is exactly the patch: the hold stays on through the reload, the 4 s note only says "still reloading", and `devmodeUndo` keeps its record until the new page drops it (a `sessionStorage` note). Also in: section 25's start-up line moved to the section's end (it ran before `DM_KEY` existed), and the two rooms with no way back are marked "(no way back)" (`DM_SHUT`, which devmode_check keeps true).
- **slowreload.py:** with the reload held 6 s, the Undo **happened** and its record was used up. At 2 s the same.
- **cadet_test** against integration: **ALL IDENTICAL**. **devmode_check: OK**, including its new "slow" part (Undo and Back to mark with a 6 s reload). names_check OK.
- **savecmp / savecmp2:** the real storage is byte-identical to integration's in all five modes and with the arrived key. A `#dev` session leaves the real keys untouched.

## Owner stand-in review: patch E (claude/patch-e 2e2575d), sections 20, 19 and the deck signs

**PASS.** With the switches off, the game is the same as integration's apart from #25's deliberate rename. The patch-to-Dev-mode interplay works on a scratch merge.

- **cadet_test**, integration against patch-e: 0 px. The only difference is `state ['items']`, the deck directory's text (#25's rename, not behind a switch, as the user asked). With #25 taken out (a scratch revert of bc66e30's game lines): **ALL IDENTICAL** (renderer noise only). Run alone, that is: run at the same time as another cadet_test on 4 cores, it showed false pixel differences in f_noshadow/g_nocrew/h_crewback, so cadet_tests shouldn't be run side by side.
- **savecmp:** the real save is byte-identical to integration's in all five modes. names_check OK on patch-e and on a scratch merge with claude/devmode fa394b3 (the game merges cleanly; only `plans/build-table.md` clashes).
- **Shared functions, section 20:** `careerClock(now, quiet, hold)`: every existing caller passes two arguments, and with no `hold` the side effects run at once, exactly as before. `clockScreen(said, ask, after)`: the existing callers pass at most two, and the new path runs only under `CLOCK_UNDO_ON`. `rankCardRole(p)` returns `p.role` when `RANK_CARD_ON` is off, so the chat card's role and section 19's roster row (9e276a4) are unchanged. `shopMenuButton` returns null when off.
- **#25's sign:** `fillText(name, 38, y, w - 46)` applies only to names over 20 characters, and `w` is the texture callback's width. Fine.
- **The Undo window with Dev mode merged** (`undowin.py`, scratch merge, `#dev.clockundo`, Day 9 08:56):
  - A, a clock-in then a Dev jump (+3 h): the window settles before the jump, through `devmodeKeep`'s save. The clock-in stands, the note keeps 08:56, and the day isn't excused.
  - B, a save inside the window: settled.
  - C, a clock-in at 08:58 with frames played on: the window had closed by 09:00. Undo then does nothing; the shift counts, and the next morning shows no miss. If an Undo ever lands after `shiftStart`, `flag('shiftSent') === u.keep.sent` keeps `c.on`, as the comment says.
  - careerOff is untouched by the patch. Dev mode's excuse checks `careerClockedIn`, and a punch counts at once, so a jump straight after clocking in is never excused.
- **Nit:** the held side effects run at settle time, so the `clock` note is stamped then (C: `in@09:00` for an 08:58 punch). It's at most the window's 5 ship minutes, and nothing reads the note's minute today. Leave it, or note it in the comment.

## Owner stand-in reviews: patch #5 hooks (claude/patch-e ab685bb) and the mug/cocoa hooks (claude/devmode 375827b)

**Both PASS.**

**Patch E (#5, the spine ladder, and 274a31f).** cadet_test against integration: the only difference is `state ['items']`, #25's directory text, the same as the earlier PASS, with 0 px. names_check OK.
- f1757b0 (section 11): both taps ask `ladderTap`, which returns false at once with `LADDER_ON` off (or during a ride). `updateRide` hands over only rides with `r.ladder`, which only `ladderStep`'s own rides carry.
- 1218845 (section 4d): the Deck 5 east call panel and the two tier texts are skipped only under `LADDER_ON`. The line sits inside Deck 5's `dress()`, run at deck build, long after section 15b's `LADDER_ON` exists (line 14422), so it's safe at load.
- 274a31f: the section 20 lines are now `typeof`-guarded (`rankCardRole`, `shopMenuButton`, `shopMenuOpen`), with the same results when off. No shared function's inputs or results change.

**Mug and cocoa (#30, #29) on claude/devmode.** cadet_test against integration: **ALL IDENTICAL**. names_check OK.
- c6f1158 (15): `mugTick` returns at once when off, and the hold falls through to `mugHeld()`, which is null when off.
- 4420bff (15b): `mugPose()` is null when off, so the drink pose is `drink` as before. `putWhat` and Put down get `mugHeld`/`mugPut`, both null when off.
- c1036ae (15b): `A.def.also = mugAlso(...)` returns a copy with the same values when off. `ACT.def` is a fresh copy per activity (`{ ...PLAYER_ACTS[kind] }`, line 12962), so cocoa's +8 leisure never leaks into the shared definition. `mugFinish` uses `mugAlso` too, so "drunk as you go" gets it as well.
- 05314b6 (8b slot): `HOLDS.mug` and `ACTS.cocoa` are added in the performance engineer's slot, and only used through `mugHeld`/`mugPose`.

## Owner stand-in review: patch #26 First Light Cocoa hooks (claude/patch-e cf45e2a), my last

**PASS.** Hooks: 1c4bc67 (18), 93bf4e5 (5), 57b77e5 (21), e720cea (section 15's slot functions made hoisted).
- **cadet_test** against integration: only `state ['items']`, #25's directory text, the same as every earlier patch E run, with 0 px. names_check OK.
- **`evcmp.py`:** `eventsOn` for Days 1-30, plus `eventPlan` for 40 crew on Day 4, hash **identical** to integration's (d1aae5144d0f), with no `first-light` listed while `FLC_ON` is off.
- **Load order.** `TRAD_JOIN['first-light']` reads `MUG_ON` when the table is built; `MUG_ON` is declared at 14508, before `TRAD_JOIN` at 35475. `applyLight` (section 5) may run before section 15: `flcDim` is now a function declaration reading the `var FLC_DIM`, which is undefined then, so `|| 0` gives no dim. `flcBusy` is called only at run time (section 21's arrow), never before `FLC_ON` exists.
- **Section 18 when off:** the tradition is skipped unless `FLC_ON`. The `'cocoa'` tag keys are added for every event, but only events that carry a cocoa tag use them, and none do with the switch off. `evTagId`'s widened suffix can't misread an id, since no tradition id ends in "-cocoa". `flcJoin` is reached only for `first-light`.
- **Sections 5 and 21:** the light is multiplied by `1 - flcDim()`, which is 1 when off. The bed arrow's extra condition is false when off (`flcBusy` returns `FLC_ON && …`).
