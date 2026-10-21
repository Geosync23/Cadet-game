# Crossing the Line: adversarial build review (before L6)

Reviewer ER3 (session_017jM4m1bcqPHbSesi2kSfLr), 2026-10-21. Branch `claude/event-plan-review-3`.
Build reviewed: `claude/line-update` b4efc66 (L1-L5c), builder EV7 (session_01WeSNWT2a7Fs8HS3j9HWamK). Reports to lead 24.
Base: `claude/storm-update` b991877 (the merge base). Method: ER2's (`plans/handover-event-reviewer-2.md`).

## Verdict: round 1 PASS WITH FIXES; round 2 part A (835bcfc): fixes 1-3 and 8 verified, one small leftover (fix 9); part B after the account move

The Line is well built and safe to keep switched off: off, the game is identical, and with it on only Day 7 changes.
The story plays end to end at phone size when walked. Three things need fixing before the switch-on (fixes 1-3).
Fixes 4-7 are small. Fix 8 is for the checks: two of the four mistakes I planted (the supper emptied, Tomas pulled off
watch) pass every check today.

### The checks (each in its own CADET_WORK, one browser check at a time)
| Check | Build | Result |
| --- | --- | --- |
| cadet_test | storm tip b991877 vs line tip b4efc66 (off) | **ALL IDENTICAL**, 0 px, no errors |
| check_fast | line tip (off) | **OK** (253 s) |
| bigevents_check | `EV_LINE_ON = EVENTS_ON` copy | **OK**; its note: "lineCeremony: 53 mean to go, 39 planned there ... 14 meant to go but aren't planned there" (fix 3) |
| events_check | on | **OK** |
| day_check 6, 7, 8 | on | **OK** (Day 7: servery line 130 served, nobody gave up; Deck 3 peak 271 calls in its own camera) |
| food_check 7 (1 day) | on | FAILED: "garden, good" and "garden carry" |
| food_check 7 | off | FAILED: "garden, good" only |
| food_check 7 | storm only (events on, Line off) | FAILED: "garden, good" only |

On food_check: "garden, good" fails on every build, so it isn't the Line's. "Garden carry" fails only with the Line on,
so it isn't "already on the base" as the build table says. In a fresh game, Day 8's garden (gardenCrew 7 and 8, the
Day 8 11:00 pick and crates) is identical on both builds. So it's state an earlier part of the check leaves behind,
and the extra 12 portions or the event's galley key are the likely route. Fix 7 below: EV7 to find which, and
say so in the build table.

## Round 2 (part A): fixes verified on claude/line-update 835bcfc (L5d-L5f)

**Part A only, by lead 24's call before the account move.** Part B (the full check set again: cadet_test off, check_fast,
events, day 6-8, food 7) comes after the move.

| Round 1 | Now (a new game, 390x844 where walked) |
| --- | --- |
| 1. A reload mid-panel loses the moment | **Fixed.** `p_reload.py`: the Saturday moment is offered again after the reload. `pell.py`: Pell's guess is offered again after a reload mid-panel, then plays to the end. |
| 2. The supper is one sitting, and Pell isn't at it | **Fixed.** 59 come, at most 39 at once, all seated (mess seats and the long tables' chairs, type `event`/sit). Pell is seated 18:30-19:19, and his guess plays when walked to with the secret set. |
| 3. First-timers miss their ceremony | **Mostly fixed.** 14 of 22 are there (was 12); the crowd is 46 plus you (was 43). **Leftover (fix 9 below).** |
| PR6's late Captain | **Fixed.** She's at `3-bow-lounge-line-lead-1` from 14:30; Brennan at lead 2 from 14:40 to 14:55. |
| Jobs held to 13:45 | **Done** (`hold: 825`). |
| 8. Check gaps: P2, P3 | **Closed.** Re-planted against bigevents_check 7c7d4eb: Q2 (the supper unseated, so empty) FAILs ("only 0 came ... fewer than 40" and "isn't seated"). Q3 (the watch stands easy) FAILs ("tomas is off watch ...", "ueda-vera is off watch ...", "a crowd of 63, over 60"). |
| Saruth, Tomas | Saruth is in the garden at 14:45. Tomas is at `2-watch-6` through 14:30-15:00 and on the Lap at 20:40. |

Not re-checked in part A: fixes 4-6 and 7 (EV7 and FD1 report them done), P4 (the off menu leak), and the nits.

### 9. Leftover from fix 3: three first-timers still skip their own ceremony (small; after the move if EV7 has stopped)
- **Lemaire** (night shift, a day off on Day 7, `ownFor` true) sits on a bench, `3-bench-14`, 14:17-15:44, through his own
  ceremony.
- **Reyes** (works) and **Yoon** (infirmary), both night shift, wake at 14:22-14:29 and go to the music corner and the gym
  14:29-15:24.
- (Madsen is the galley line, Varga cooking, Keane asleep, Tomas and Ueda on watch: those are right.)
- **Repro:** `plans/er3-probes/r2.js` and `r2b.js` (probe.py ON.html): `firstNot`, and each one's plans 14:00-15:15.
- **Fix:** an off-duty honouree's leisure block gives way to the ceremony (Lemaire). A night worker who wakes before
  14:30 comes before their leisure (Reyes, Yoon). That would put 17 of 22 there.

## How I tested

- Headless Chromium at 390x844, a new game each run, a switched-on copy
  (`sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/; s/^const EV_LINE_ON = false;/const EV_LINE_ON = true;/'`).
- I walked to every moment with a real path (`playerGo`), never stood the player on top of someone.
- On paper: `planDay`, `whereIs`, `devDay`, `galleyMenu` for every person, Days 1-30, three builds.
- Probes: `plans/er3-probes/` (they need `/tmp/cadet-work/three`; `common.py` holds the helpers).

## Off: identical

- cadet_test, storm tip b991877 as old, line tip b4efc66 as new: **ALL IDENTICAL**, 0 px on every shot, no errors.
- Storm only (EVENTS_ON on, EV_LINE_ON off) against the storm tip on: every person's plan, Days 1-30, the menu and
  `eventsOn` are **identical**. So `evLaterSpans`, the new `evClosed` and the galley-stint meeting hook change nothing
  for the storm.
- Line on: only **Day 7** changes (Day 6 and Days 8-30 are identical to storm-only).

## On: the story, walked at 390x844

| When | What I saw | OK? |
| --- | --- | --- |
| Sat 18:00 | Vance's Mail "Tomorrow we cross the Line". Status: "Tomorrow at 14:30 we cross the Line into the Veyli reach." | yes |
| Sat 19:01 | Walked to Tomas (mess seat 3-mess-5, 1.5 m): `lineTomasSat` opened. Reply 0 set `line.promised`. His 22:50 Mail was held back. | yes (but see fix 1) |
| Sat, no meeting | His Mail "On watch tomorrow" at 22:50. | yes |
| Sun 10:40 | Walked to Brennan in the bow lounge: her offer bubble and toast. | yes |
| Sun 12:50 | Both jobs on the board, held for you to 14:15. Took the punch; in the galley, Brennan's secret toast ("Pickle brine..."). | yes |
| Sun 14:20 | Walked from the plaza into the lounge (48,10). | yes |
| Sun 14:30 | The horn: notice, felt once (`felt:horn`), the Captain's banner "All hands". | yes |
| Sun 14:40 | The oath opened in the lounge: Cruz and Walsh as first1/first2, the three answers. Reply 1 set `line.answer.watch`. | yes |
| Sun 14:56 | The dunking: 33 mugs in the crowd. | yes |
| Sun 15:15 | Brennan's supper Mail; resolution status. | yes |
| Sun 15:25 | Deck 2: walked to Tomas at his post (he's at the toilet 15:06-15:18): `lineTomasMug` opened, `story:mug` 2. | yes |
| Sun 18:27 | In the servery line (33,4), promised but no mug and missed the ceremony: Brennan's `punch.saved` then `punch.savedYou` (6.4 m). | yes (see fix 5) |
| Sun 18:00-19:15 | The Line supper: everyone seated, no standing spot, no tray outside the mess. | yes (but see fix 2) |
| Sun 20:48 | Joined Tomas's Lap with a tap; at the bow turn `lineLap` played, Tomas's line "You said 'even the ones on watch'...". | yes |
| Mon | Plaque by the lounge door with your answer ("Is this the part with the punch?" when picked); certificate above your bunk shelf; no commendation. | yes |
| Tue | Record: "Crossed the Line into the Veyli reach, Day 7." with no "came through it" line. The event logged Days 6-9; the storm starts on Day 11 as before. | yes |
| Schedule | Day 7 shows the ceremony, "The Line supper 18:00" and the Lap. | yes (nit 10) |

**Numbers (a new game, on paper):** 76 aboard (74 crew, Saruth, Ulla); 22 first-timers aboard (34 on the roster);
the ceremony 43 there at once (4 of them the cast) plus you; 21 could stand easy, 16 came; Saruth in the garden; Ulla in the
crowd; Tomas at `2-watch-6` 08:51-17:00 (a toilet break 15:06-15:18) and on the Lap 20:27-21:11; the first-timers fill all
ten front spots; the Captain, Brennan, Cruz and Walsh on the four lead spots.

**Draw calls, 390x844 (normal zoom / widest):** the oath 308 / 396; the dunking 387 / 413; the supper 315 / 411 and
301 / 395; the Deck 2 mug 207; Monday's plaque 332; Deck 4 certificate 207-288. All under 450.

## Fixes

### 1. A reload with a story panel open loses the moment for good (the storm's fix 1 trap, again)
`lineMoment` sets the `story:*` key **as the panel opens**: `story:sat`, `story:mug` (2), `story:guess`, `story:lap`.
The save on a hidden tab (`visibilitychange`, line 9145: a phone switching apps) or the hourly save keeps that key.
After the reload the panel is gone (moment scripts aren't replayed), and the key says it happened.
- **Repro** (`plans/er3-probes/p_reload.py ON.html`): Saturday 19:01, walk to Tomas, the panel opens, one line read,
  then the reload as ER2's probe does it (DIALOGUE gone, `e.mine` kept). Walk back to him: **not offered again**. At 23:00:
  **no Tomas Mail** either (`unless: 'story:sat'`), and no `line.promised`. You get neither the moment nor the Mail.
- The same for the mug (`story:mug` 2 makes the Lap line say "mug" though you never finished it), the guess and the Lap.
- **Fix:** do what `stormMoment` does (ER2's storm fix): set the key in the panel's `onEnd` (however it closes), not
  as it opens. Prove it with the repro: offered again after the reload, and the Mail if you walk away.

### 2. The Line supper is no bigger than an ordinary Sunday, and Pell isn't at it
The user's decision was seated sittings **with staggered arrival**, for a supper of "up to about 60". As built, the
staggering doesn't happen:
- 44 people come, and 44 are there at once (18:30-18:45). On the storm build the same Sunday table gets 45.
  Nobody leaves and is replaced: a 75-minute window (18:00-19:15) with 45-60 minute stays only leaves room for one sitting.
  The lantern supper gets about 51 with 105 minutes (to 19:45).
- About 30 crew who'd come eat a plain dinner instead, many in the **bow lounge**. Pell is one of them: 18:11-18:42 at
  `3-lounge-24`, then the gym. **So `lineSupperGuess` (Pell's guess at the punch in the mess) can never play in a new game.**
  I stood in the mess 18:20-18:55 with `story:secret` set: Pell was 15-22 m away.
- **Repro:** on paper, `planDay(p, 7)` for everyone: 44 with an `ev-sunday-table` tag, the peak 44 at 18:30;
  Pell `18:11 dinner @3-lounge-24`.
- **Fix:**
  - Pull Pell to 1 for the Line supper (the story needs him there), as the Lap does.
  - Make room for a second sitting, so about 55 come with no more than 48 at once. Either:
    - shorter stays (30-45); or
    - a longer window (to 19:45, as the lantern supper; the gold and the afterglow can stay at 19:15).

    Measure both and take the one nearer 55.
  - bigevents_check's supper row should report how many came, not only the peak.

### 3. A third of the first-timers miss their own ceremony
10 of the 22 first-timers aren't there.
- Two are on duty and that's right: Tomas (the story) and Ueda (watch).
- Varga is cooking (the galley line, right) and Keane is asleep (the night shift, fine).
- But six are just busy:
  - Bakshi and Hart are **playing Winner Stays On** on the rec deck at 14:40;
  - Reyes is at the music corner, Yoon at the gym, Lemaire on a bench, Madsen resting.

The plan: "First-timers stand at the front". The ceremony is *for* them, and the crew's chatter tells them "First-timers to
the front. That's you". bigevents_check notes the same gap ("14 meant to go but aren't planned there").
- **Fix:** treat the off-duty first-timers as the ceremony's honourees (the birthday's `own`, or a `prio`), so a leisure
  block or a game gives way to it. Keep the night shift asleep. That should also lift the crowd from 43 to about 49, over the
  plan's "45 or more".

### 4. The ceremony's "thanks" says the oath and the punch happened before they do (small)
At 14:36 you get the gathering's thanks, as a toast and as a Mail from the Captain ("Thanks for coming"): "You stand
with the crowd ... while the Captain reads the old oath ... Then a mug of Line punch, all of it. You're a Line-crosser now."
The oath starts at 14:40 and the punch is at 14:55.
- **Fix:** send the thanks after the punch, about 15:00, or use words about arriving (EW2's call).

### 5. Brennan's two supper lines cut each other off (small)
If you promised Tomas a mug and didn't take it, and also missed the ceremony, `punch.saved` and `punch.savedYou` fire one ship
minute apart. That's 1.7 real seconds, and `bubbleSay` replaces a speaker's bubble, so the first line shows for under 2
of its 5 seconds.
- **Repro:** p3b.py with `miss`. Both keys were set by 18:33.
- **Fix:** wait about 4 ship minutes after `story:saved` before `savedYou`.

### 6. The punch job only counts for the mug once you turn it in (small)
With `TURN_IN` on, `finishJob` leaves the job awaiting turn-in, and `eventJobDone('linePunch', true)` is false until you
turn it in at a board. So if you carry the punch but miss the oath, you get no mug for Tomas unless you also went to a
board.
- **Fix:** count the work as done (`j.workDone`), or say so in the plan.

### 7. food_check 7's "garden carry" FAIL is the Line's (small, explain it)
See the checks table. It fails with the Line on and passes storm-only and off. Find the part of the check whose leftover
state changes Day 8's pick (probably the extra 12 or the galley key on the event), fix it in the game or the check
(the check is PB's), and correct the build-table row.

## Nits (no action needed unless the author agrees)
8. The supper's ask "Come and find a seat. Or a wall." and the thanks "full to the walls" read as standing room. That no
   longer fits the seated supper (EW2).
9. Tomas says "Right. Bed. Early start." at 19:01, then climbs on the rec deck until 22:40 (EW2, or open his moment
   later).
10. The Schedule shows two rows, both called "Crossing the Line": 14:30 (tradition) and 14:40 (event). Name the second
   "The oath".
11. At 14:40 the Captain's 14:30 banner is still on screen as the oath panel opens. 10 ship minutes is about 17 real
    seconds, and the banner stays about 20. On a phone the two cover most of the screen for about 3 seconds.
12. The plaque's quote ("We crossed together. Even the ones on watch.") isn't quite your words ("We crossed together,
    all of us. Even the ones on watch."). That's fine if it's the writers' choice.
13. Vance has two dinners on Day 7: a 28-minute placeless "dinner", then a second queue at 19:00. The same shape is
    on the base on Day 21 (Santos, Amadi). It's not the Line's: a backlog row for section 14.

## Planted mistakes (do the checks catch them?)
Four mistakes planted in copies (`plans/er3-probes/`: the plants are one-line edits, listed here):

| Plant | Which check | Caught? |
| --- | --- | --- |
| P1: Saruth comes to the ceremony (`who` without `p.id === 'saruth' \|\|`) | bigevents_check | **yes**: "Saruth is at the Line's ceremony" |
| P2: the Line supper's row back to `where: [[3, '@gather-mess']]`, no `stay`/`seated`. In fact this **empties the supper: 0 diners** | bigevents_check, day_check 7 | **no**: bigevents prints "WAITING ... 0 seats, 0 standing spots, 0 at once" and ends OK; day_check OK |
| P3: the watch left out of standing easy's `not`. Tomas and Ueda leave their posts for the ceremony, which **breaks the story** | bigevents_check | **no**: it reads Tomas at 10:00 only, and ends OK |
| P4: switch off, but `linePudding` ignores the switch. The Day 7 menu says "the Line supper, with apple crumble" in an **off** game | cadet_test (vs the tip), food_check 7 (off) | **no**: cadet_test ALL IDENTICAL; food_check prints the menu but fails only on its usual garden line |

### 8. Close the check gaps the plants found (for EC1, bigevents_check's owner; EV7 to ask)
- **P2:** the Line supper's row should **FAIL**, not wait, when it isn't seated, and when fewer than about 40 come.
  It should also print "came" beside the peak (see fix 2).
- **P3:** Tomas at his post **through 14:30-15:15** (every 5 minutes), and Ueda too, the watch's other hand.
- **P4:** the off part ("nothing with it off") should also read `galleyMenu(7)` (no "Line" in it), `eventsOn(7)` (no
  `lineCeremony`), and that the 'bow-lounge-line' venue doesn't exist.

## What to re-check in round 2
Known from others (lead 24), to verify after EV7's fix turn:
- The volunteer jobs held to 13:45, not 14:15: a skipped punch job went to the crew at 15:00 and put Eklund in two
  places.
- PR6: the Captain reaches the bow glass only at 14:52-14:56 for a 14:40 oath, and the crowd arrives 14:43-14:52. In my
  walk the oath panel opened at 14:40 anyway, because it opens when *you* are in the room. So the Captain reads the oath
  while still walking in. Check that she's at the glass at 14:40.

Fix 1's repro; P2 and P3 planted again once fix 8 is in (they must now FAIL); fix 2's numbers (came, peak, Pell's guess played when walked); fix 3's crowd and first-timers at the
front; then bigevents_check, day_check 7, food_check 7 and cadet_test off again.
