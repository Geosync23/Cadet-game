# Owner stand-in reviews (OR1)

OR1 took over owner stand-in reviews from DR1 (handover on claude/devmode-review-1). Reports to lead 21.

## 1. PA, claude/patch-a eb638e7: batch B and C hooks (2026-10-20)

**Verdict: PASS** (one optional suggestion, below).

Tests on eb638e7: cadet_test integration (5d6ee1c) vs patch-a, run alone: **ALL IDENTICAL**, no errors. check_fast run alone: **QUICK CHECK OK in 213 s**.

| Commit | Section | What it does | Owner check |
|---|---|---|---|
| 651a78f | page CSS | `.devbtn.devglow` pulse, `#devPoint` | CSS only; used only by section 21's `introDevGlowTick` (intro on). No meshes, no draw calls. |
| 279a091 | 22 | `linesHush` also asks `introHush()` | `typeof` guarded, called at run time only. `INTRO_UI` is a load-time const; `night`/`hushTo` only set by the intro, so false with the intro off. |
| 8ee5d6b | 20 | `socialChatter` returns while `introHush()` | Placed after the `schedU` odds test (a hash, no `R()`), before anything is drawn; `CHATTER_AT` untouched. Off with the intro off. |
| ee48072 | 11 | floor tap ends beside a standing person (`tapBeside`) | Ungated, `typeof` guarded; `playerGo` gets the same tile shape `[i,j]`. No `R()`. cadet_test's taps identical. |
| 5cb3aad | 18 | beam goals carry `beam: true` | Adds a field only; `item` kept, so `tradGoalHere` and the beam tap are unchanged. |
| c56c37c | 15b | `ixGoalWorld` honours `beam`; arrow at `w.y` | `ixGoalWorld` result gains an optional `y` only for beam goals; every caller (ixFrame, trkDoneCheck, section 25's devmodeTake/devmodeMove) reads x, z and ignores y. Falls back to `item` off Deck 5. |
| 1f91e90 | 15b | `trkDoneCheck` (in the slot); Tracked items gain `span`; goals gain `trkFrom`/`trkTo` | Additive fields; `trkItems` readers (Tracked, devmodeAppt) unaffected. `span` uses the same absolute minutes as `shipNow()`. No-op unless you tracked something (IX_GOAL is not saved). |
| 55d9a69 | 15 | `shuffleable`: a following escort steps aside even while talking | Only agents with `esc` `follow|`; talk taps stop the player, so no shuffle during a panel. |
| 25248b9 | 15 + words | `t:devwork` tip: a long work step under way, days 1-7, `sure` | Test is inside `teachTry`; every WORK_ACTS kind runs through the act runner with `def.mins`/`done`. Words baked. |

Notes for PR2 and the lead:
- The patch plan's batch C row says "intro only", but #11 (`trkDoneCheck`), #12 (`shuffleable`), #13 (days 1-7) and #17's tap (`tapBeside`) act in normal play too. All are proven identical in the test URLs; whether they should reach beyond the arrival week is a scope call for PR2, not an owner issue.
- Optional (15b, `trkDoneCheck`): tracking something while you're already in its room (a "Now" item, or a place) clears it on the next frame, so the Track tap seems to do nothing. If wanted: in `trkDoneCheck`, remember whether you were already there on its first look (`g.trkSeen`) and clear only once you've arrived from elsewhere, or at `trkTo`.

## 2. PB, claude/patch-b 2e517ff: batch D (2026-10-20)

**Verdict: PASS.** check_fast on 2e517ff, run alone: **QUICK CHECK OK in 211 s**.

### Hook 1d8d606 (section 4b, the toilet stall kit) → `stallCapAdd(g)` (section 14's slot)
- Load order: the kit runs inside `place()` at deck build, after `STALL_CAP` (a load-time const) exists; `stallCapAdd` is a hoisted function declaration, and the call is `typeof` guarded.
- Shared kit at load: one `BoxGeometry` and one `std()` material (colour through `col()`), no `R()`. Made before any deck's watermark, so `unloadDeck` never frees it.
- Shapes: `toiletStall` still returns `{ w, d, tall: true }`; the cap is a `noMerge` child (mergeMeshes skips it), raycast off, no shadows.
- No coplanar surfaces: the cap (.13 x .06 x .04, z .54-.58) encloses the green light (.12 x .05 x .02, z .545-.565); its back is inside the door (z .50-.55).
- Draw calls: +1 per taken stall in view, hidden otherwise. Fine on a phone.

### #10 as performance owner (walkGap, walkLaneStep, LIFT_OUT)
- `walkGap` runs once per walking crew member and loops over the deck's crew: walkers x crew, about 900 cheap tests a frame at Sunday dinner. After 2e517ff, far walkers are rejected with four comparisons before any square root. Timed on paper (30 walkers, 30 crew): **about 5 microseconds a frame** on this machine; a phone 5-10x slower is still well under 0.1 ms of a 16.7 ms frame. **Acceptable; no cheaper approach needed.** If the crew count ever grows a lot, the next step would be one list of walkers per frame (skip the non-walkers once, not per walker).
- `walkLaneStep` now looks up doorways once a step (`laneAt`), so no strings are made each frame. No `R()`: the lane comes from `idHash`. Only the drawn body moves (`lx`, `lz`), so stuck checks, doors and bumps still use the tile position. `LIFT_OUT` is cleared with the deck crew; the planner never reads it.

### PB's cadet_test claim, checked
cadet_test integration vs 2e517ff: DIFFERENCES FOUND (expected). Split with a copy of 2e517ff with #10 and #8 switched off (walkGap 1, no lane, liftOutOk true, no cap):
- **#10 + #8 alone** (copy vs 2e517ff): crew drawn positions shift in every shot; the taps are the same in both. The crew-hidden shot g_nocrew differs only in Oona's speech bubble, which follows her drawn lane.
- **#7 + #9 alone** (integration vs the copy): the plans change (as PB says), so the crew are elsewhere. The scripted tap 1 (450, 380) now lands on **Pell**: his chat panel opens and you don't walk, so taps 2-4, the steering shots and the end state (room, memory counts) all follow from that. Seen in i_tap1's shot. g_nocrew's other differences are the washroom's light and fade, with crew now using the stalls (#9).
- So the claim holds: every difference comes from the planned crew changes (#7, #9) or the drawn lane (#10); none comes from the hook.

## 3. PA, claude/patch-a ffd8ed7: section 10 hooks 155f0d4 + 35e425a, section 15b 50fe32b (2026-10-20)

**Verdict: PASS**, with one recommended fix (below). cadet_test integration (5d6ee1c) vs ffd8ed7, run alone: **ALL IDENTICAL**. check_fast alone: **QUICK CHECK OK in 207 s**.

- **155f0d4 + 35e425a (section 10, `escortStep`).** Its inputs and result are unchanged (`(dt, e)`, returns true). `escBeside` (section 21) moves a non-follow escort's goal off your tile; the ESC_GAP stop now applies only to wait-mode walks whose path ends within 2.4 m of you (`escToYou`), never to `lead`, never to a line walker (`e.after`). Run time only, `typeof` guarded; `ESC_GAP`/`escToYou` are load-time consts in section 21, read only from frames. No `R()`, no draw calls. Follow mode is unchanged in practice: it already stops at `ESC_NEAR` (2 tiles), beyond the .9 m gap. The scenes it reaches outside the intro: crewScene waits (section 10's, the promotion cake's Brennan). The friend seek (`@seek`) is a separate branch, untouched.
- **Recommended fix (section 10):** a wait-mode escort whose path to a tile 1-2 m beyond you goes past you (you standing in a doorway between him and his tile) now stands .9 m short for as long as you stay put. Before, he walked through you. It frees itself when you move, so it's not a lock, but a player waiting for the scene may just stand there. A cheap guard: hold the gap stop at most ~2 s, then walk on as before, e.g. `... && nd < ESC_GAP && nd < dist && (this.gapT = (this.gapT || 0) + dt) < 2) { ...stand... } else { this.gapT = 0; ...walk... }` (gapT resets once he's walking).
- **50fe32b (section 15b slot, `trkDoneCheck`).** A tracked place now clears only after you've been away from it since tracking it (`g.trkAway`, a field on IX_GOAL, not saved); timed items unchanged. This answers my part 1 suggestion for places. Off another deck the check returns early, so you're counted as away once you reach its deck: fine.

## 4. PB, claude/patch-b d3b028f: batch F hooks 22c4442 (17), 9e34423 (24), machine_check's range (2026-10-20)

**Verdict: PASS.** check_fast on d3b028f, alone: **QUICK CHECK OK in 218 s**. career_check alone: **CAREER CHECK OK**.

- **22c4442 (17, `openJobs`)**: same inputs, same result shape; only `mins` changes, and only for `'you'` on service/repair/overhaul jobs (`JOB_TYPES[kind].work * JOB_PACE * tier`), matching section 15's `jobMins` base. The crew's numbers are unchanged. Its only reader is section 15b's job board (display). It still leaves out `careerSpeed` and the log's 10%, as it did before. `typeof` guarded, run time only.
- **9e34423 (24, `WORK_BANDS` Tier 1 'relied' 40 -> 48): a sensible change of the target, not hiding a problem.** The design target is a steady player reaching "Relied on" by the end of Day 8, a very busy one not before Day 5. #16 makes your machine jobs 1/.72 = 1.39x as quick, so XP per hour rises by about that much; 48 is 1.2x, so nobody reaches it later than before the patch. Measured: busy 43 on Day 4, 59 on Day 5 (5 under the line on Day 4); steady 55 on Day 8, "Relied on" in time for Day 9's Tier 2 test job (which needs it), passed on Day 9. It also clears backlog row 12 (career_check's busy-before-Day-5 failure, already red on integration). Tier 2's bands are untouched.
  - Note for the user/PR2, not blocking: the lower Tier 1 bands (steady 8, reliable 18, trusted 30) now come about 1.4x sooner too (busy player "trusted" on Day 3). Nothing tests them; whether they should scale is a design call.
- **machine_check 3-6 -> 3-8 jobs a shift day: sensible.** 6 x 1.39 is about 8.3, so 8 is the old ceiling at the new pace (the plan's "about a third more where the board has work"). Measured 6.2 a day (56 jobs on 9 shift days). The checks that would catch a real problem are unchanged and pass: repairs 49% (40-60%), lowest ship health 94.5 (85+), nothing broken, every repair has a cause, the same twice.

### Part 4 corrected (2026-10-20, after PB's revert 319f541)
My reasoning for 9e34423 was wrong. I assumed that quicker jobs give more points an hour in career_check. But its paper players don't time jobs, so they get the same points a day before and after JOB_PACE. Checked: career_check on integration 5d6ee1c (before batch F) gives the busy player exactly the same, 33 "trusted" on Day 3 and 43 "relied" on Day 4, and fails `busy: "Relied on" before Day 5` (backlog row 12, which the user accepted until a balancing pass; now row 17 too). So 48 changed the target to hide a known, accepted failure, not because batch F moved anything. The revert is right, and so is my design note's corollary: the early "Trusted" predates batch F too. machine_check's 3-7 (6.0 before F, 6.2 after) is a better limit than 3-8. The 22c4442 (openJobs) verdict stands.

## 5. EV1's events base brief, claude/events-base a909e9d (plans/events-base-brief.md), 2026-10-20

**Verdict: PASS WITH FIXES** (the brief; no code yet). Checked against the events plan (claude/events-plan f6996d86, section 5 and the calendar) and the Fridays plan (claude/patch-plan cdeb1ff, rev 4), and against the code on events-base.

What matches: F0-F8 and their sizes (13-15 turns, the plan's 12-15); the calendar (Day 0 arrival, Day 1 Monday: Fridays 5, 12, 19, 26; Sundays 7, 14; storm warning Day 11, front Day 12, all-clear Day 14); the storm's move to Days 11-15 switched on only with the storm update; the Friday hold 15:30-17:00 from Day 5 (the address is 16:00-16:50 in rev 4, dinner 17:00); "both happen" on Day 12; no auditorium all-hands for the storm; called-in people (Days 7, 14, 27); `eventDay` defined false when off (24k's cases at line ~44691 see what they see today); `upcomingTraditions` left alone (a new `eventItems` instead); load-time tables, no `R()`; `isWorkDay` is rota-only (pure), good for `eventCalledIn`.

Fixes:
1. **One source for the Friday hold.** F0a's `evHeld(t)` and F1b's `EV_BEATS` Friday row say the same thing twice. Make `evHeld` read the `EV_BEATS` row (or the other way round), so a change to the Fridays plan's hours is one edit.
2. **Move F7a (the on-paper check) up to just after F1** (turn 5-6), so F2-F6 are built against it. F7b-c (live, crowds) stay late.
3. **`EV_CAL_ON` alone puts today's storm, with its old hours, on Day 11**, onto the team job (09:30) and the ceremony (17:15). Say what F0a's "day_check Day 11 (on)" should show, or check Day 11 only with the storm update. Add career_check and leave_check with the piece on.
4. **`eventDay(d)` and `eventCalledIn(p, d)` must come only from `EV_CALENDAR` and the events' own data, never `eventNow`, `SHIP.event` or anything saved.** 24k's incidents plan is saved per day, so a runtime read would make plans differ after a reload.
5. **`EV_SHIPWIDE` (read through `evTable` -> `eventsOn`, so section 14's planner sees it):** with the switch off, the same table byte for byte (events_check compares its JSON). Give each moment its own hash key rather than `350 + push order`, so the party keeps k 340 whatever is added.
6. **Owners to tell:** the storm's day change and new gatherings reach section 14's planner through `eventsOn`: tell PB (sim, live seat) at F0a. The Fridays plan's part A changes `eventFree` (the 17:15 rule), as the storm update will. Name `eventFree` as shared between them, so the two don't clash.
7. **Patch clashes:** patch-a edits section 18 (`tradJoinMinute`, `tradGoal`: `beam: true`), 20 (`socialChatter`) and 22. Patch-b's batch F edits 15 and 17. Bring both in before F0b (section 20's `SOC_CUE_OF`) and F8 (20c, and 15's Mail).
8. **F7c perf:** coordinate with the Fridays plan's part G (the auditorium at 16:10, the lift lobby at 16:52). The worst case is Day 12's address during the storm's onset routines (storm lighting plus about 65 seated). Add that scene.
9. **F3a `eventClosed`:** build the user question 3 exception in from the start (the auditorium and the way to it open for the Day 12 address), or Tracked and "show on map" hide the address's room.
10. **F3b phones:** the status line is one line. Cap its words (about 60 characters) and take the shot at 360 px wide as well as 390.
- **Re-check of 6e71069:** all ten fixes are in. One new problem in F1a: "an event the calendar skips is decided once at load, from the save's day" would mark the storm skipped when a Day 20 save is reloaded, so `eventDay(12-14)` would differ between a reload and an unbroken run. Sent to EV1: decide the skip once, on the first load with events on, and save it (`SHIP.evFrom` or a list of skipped ids). Or, simpler, keep `eventDay` purely from the calendar and apply the skip only where an event is started.

## 6. PA, claude/patch-a 75aa54a: final hooks cc93550 (10), 6170b46 (20), 6484320 (15), b623325 (19), 8e8f584 (14), 2026-10-21

**Verdict: PASS.** cadet_test integration 0.64.5 (7958332) vs patch-a: **ALL IDENTICAL**. check_fast on the head (efba55a, which adds only PA's handover note over 75aa54a), alone: **QUICK CHECK OK in 211 s**.
- cc93550 (10): my 2 s give-up, as suggested. `gapT` is reset on a new goal and only counts while he's stopped.
- 6170b46 (20): `careerRemark` leaves Zeke out of the pick via `introQuiet` (section 21: intro on, Day 1, after `d1-end:start`), so the next Works crew member can still speak. The `schedU` odds come first, so the hash order is unchanged.
- 6484320 (15): `teachHeld` and `needWarnTick` ask `introHoldNudges` (intro on, Day 1, 16:50 until the beam). A gentle pop-up isn't marked said (`WARN_SAID`), so it comes later. The firm toast shows without "Follow the marker".
- b623325 (19): during the hold, `devHeadsShow` moves the first non-meal heads-up to the front, or waits. It only runs while nothing is showing, and `devHeadsTick` still drops stale entries ('soon' at its start, 'start' 10 minutes after), so a meal's heads-up never shows late.
- 8e8f584 (14): `mine == null` also skips a named desk that went to nobody (null), so the trade never hands out "no desk". The planner is still deterministic; it's all load-time data.

## 7. EV1's F1a, claude/events-base 0313e52: eventDay(d) and puzzle_check P1 (2026-10-21)

**Verdict: PASS** (two notes for later turns).
- **puzzle_check is honest.** The game's own gate is `caseOffer` (section 24k), which refuses a case when `eventDay(d)`. P1 calls `caseOf` directly, so skipping event days copies what the game does. Off: `eventDay` is false, so P1 is unchanged (puzzle_check OK, 76 P1 cases). With `EV_GUARD_ON` alone flipped on in a copy: puzzle_check OK, **57 cases** (the event workdays drop out), every line machine still covered, far above its floor of 10.
- **eventDay reads only `EV_CALENDAR`, `SHIP_EVENTS`' phases and `EV_SKIPPED`.** Storm: warning Day 11, so onset 12, escalation 13, resolution 14, as the plan says.
- Note 1: `EV_SKIPPED` is made once at load from the save (`SHIP.time.day`, `SHIP.eventLog`, `SHIP.event`; loaded before line 36766), so it never changes during play. An event that ran is in the log, so a reload agrees with an unbroken run. But the comment "never ... anything saved" isn't quite true; say "only a set fixed at load". One gap remains for F4: an event whose day passed while it was still waiting (one at a time, or after a Dev mode start) would be skipped by a reload and not by an unbroken run. Save the skipped set once (e.g. `ship.evSkip`) when F4 adds the event save.
- Note 2: today's diplomatic phases give eventDay 28, 29 and 33 (resolution at day +7), not the plan's 27-29. Recheck when the visit update rewrites its phases.

## 8. EV1's F3a hooks, claude/events-base 18f0d9d (code 9ddea29): sections 19 and 15b (2026-10-21)

**Verdict: PASS WITH FIXES** (one fix before `EV_DEVICE_ON` is switched on). cadet_test integration 0.64.6 (675588c) vs 18f0d9d: **ALL IDENTICAL** (against 0.64.5 the only differences are patch-b's known ones, merged in). check_fast alone: **QUICK CHECK OK in 213 s**.
- **s19 `devDay`:** new items carry the same fields as the occasion rows (`from`, `to`, `title`, `where`, `kind: 'event'`, `deck`, `room` key). `try` and `typeof` guarded; `eventItems` returns `[]` when off. The Schedule's list (line ~11611) shows from-to for it; Tracked, `trkDoneCheck`'s span and Dev mode's `devmodeAppt` take it as they take an occasion.
- **s19 `devItemGoal`:** `'event'` joins tradition/occasion/beat. The room is a key (`evRoomKey`), and a name that matches no room gives no arrow, not a wrong one.
- **s15b `trkItems`:** a closed place is left out. The three `TRK_PLACES` goals have what `eventClosed` matches on (the board: room key 'w'; your bunk: a place, so its type; the call booths: room 'B' and the place). `trkItems` runs on a Tracked redraw (once a ship minute) or a tap, not every frame, so `eventRoutines` three times a minute is cheap. Its result shape is unchanged.
- **Fix (s18's meeting line plus s19's heads-ups):** with `EV_DEVICE_ON`, a meeting's `notify` toast (15 minutes before, always shown) is dropped in favour of the device's heads-up. But `devHeadsTick` skips every kind but `appt` and `beat` when heads-ups are off (`!R.on`). So a player with heads-ups off would get **no notice at all** for the storm briefing they're called to. Either keep the toast while heads-ups are off (s18: `notify: EV_DEVICE_ON && typeof deviceApp === 'function' && SHIP.device && SHIP.device.calendarRemind && SHIP.device.calendarRemind.on ? null : m.notify`), or let event meetings through like appointments (s19: devDay sets `meet: x.kind === 'meeting'`, and devHeadsTick's line reads `&& x.kind !== 'beat' && !(x.kind === 'event' && x.meet)`).
- Note for F5 (PR2's side): `eventItems` lists every meeting of the day. Once meetings name ranks, a meeting you're not in should stay out of your Schedule (the gist by Mail instead).

## 9. FR1's Short Fridays turn 3, claude/fridays 4d270ac: hooks in sections 15, 17, 20 (2026-10-21)

**Verdict: PASS WITH FIXES** (one for the words; two loose ends for the next turn). cadet_test 0.64.6 (675588c) vs 4d270ac: **ALL IDENTICAL**. check_fast alone: **QUICK CHECK OK in 211 s**.
- Off is identical: `dayShiftEnd(d)` is `DAY_SHIFT[1]` (1020) unless `friShort(d)`; `CAREER.clockOut` is 1020 too, and `friAutoOut` is `CAREER.autoOut` (1080). `SHORT_FRIDAY` is a const at line 9000, so no load-time call can hit its temporal dead zone.
- The readers changed (s15 `workingNow` and `clockButtons`; s17 `leaveEnd`, `cartPost`'s "left for you first", `jobReserve`'s default `until`; s20 `careerClock`, `clockScreen`, `careerTick`'s auto clock-out and the reminder): each swaps 17:00 for the day's end, nothing else. `leaveEnd` passes the day number (`d0 / 1440 + 1`) correctly.
- `friSkeleton(p, d)` (18f, FR1's) caches per day from the roster, `isWorkDay` and `aboardAllDay` (s14's pure guest-stay test). So it's deterministic, and safe for the planner.
- **Fix (s20 words):** on a short Friday the forgotten-clock-out toast still says "signed you out at 17:00" (the fallback and both `clock.auto` lines in content/banks/career.lines), but it signs you out at 15:30. Use the time: the fallback as `'... signed you out at ' + hhmm(dayShiftEnd(cd)) + '.'`, and a `{time}` slot in `clock.auto` (or a `clock.auto.friday` key) for the writer.
- Loose ends (Part B's list): the team job on even-week Fridays at 14:00 (`TEAM_FRI`) still holds until 17:00 (`until: ... + DAY_SHIFT[1]`, line ~46148), so it can run past your 15:30 end ("Friday team jobs fit by 15:30" isn't done yet). Section 24's other "held for you until 17:00" ends (reserved jobs, leaks, incidents; about 15 `DAY_SHIFT[1]` readers) just hold a job 1.5 hours longer on Fridays. Harmless, but decide on purpose. s17's job board canvas says "day shift" until 17:00 (cosmetic).
