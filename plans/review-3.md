# Turn reviews: PR3

Turn reviewer 3, from 2026-10-21. Reports to lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). Pushes only to claude/review-3.

Reviews:
- **FR1**, the Fridays builder, on claude/fridays. The plan is `plans/fridays-plan.md` rev 4 (claude/patch-plan cdeb1ff), parts A-G.
- **EC1**, `bigevents_check.py`, on claude/bigevents-check. It's checked against the events plan (claude/events-plan) and EV1's brief (claude/events-base `plans/events-base-brief.md`).

PR2 keeps EV1's events-base turns; OR1 does hook and owner reviews.

The method is PP1's (`plans/handover-patch-planner.md` on claude/patch-plan) and PR2's (`plans/patch-review-2.md`):
1. `tools/section.py --diff BASE HEAD`: the sections and owners touched; new code in the seat's slot.
2. The build-number lines are untouched.
3. check_fast in a worktree, alone on the machine, with its own CADET_WORK.
4. cadet_test BASE→HEAD with the switch off: ALL IDENTICAL, or each difference explained.
5. The area's own checks (for Fridays: day_check Days 5 and 12, events_check, food_check, leave_check, career_check and the rest of the plan's Checks column).
6. A probe of my own at 390×844, looking at the shots (`.bub{animation:none!important}` before shots). The probes go in `plans/review-3/`.

Verdicts are PASS, PASS WITH FIXES (with the exact fixes) or FAIL, sent to the builder and the lead.

## Setup

- check_fast on integration 675588c (0.64.6) passed in 213 s (CADET_WORK=/tmp/work-RV3).

## Withdrawn: a Friday clash that wasn't (2026-10-21)

I first reported that the Cook-along and the Tiles ladder overlap the address on Fridays. That was wrong. TRADITIONS count weekdays with 0 = Monday (`weekday()`, line 8928), so their `"weekday": 5` is Saturday. With the right numbering, nothing in TRADITIONS or REC_TRADS overlaps Friday 15:30-17:00. The plan's fact holds. The correction went to the lead, FR1 and EW1.

**Gotcha:** `weekday(d)` is 0 = Monday ... 6 = Sunday, in WEEK_SHAPE, TRADITIONS and EV_BEATS alike. Day 0 (the arrival) is a Sunday.

## EW1 friday-weekly.address: claude/events-lines d15803c (content, sent by EW1). PASS WITH FIXES

**Clean:**
- Marrow's voice is right (calm, "we", quiet jokes, nothing on her NEVER list), and there are no spoilers.
- Names and facts match the game and facts.md.
- The pools last 6-8 weeks without obvious repeats.
- Every line fits 90 characters with a 24-character {me} (NAME_MAX) and the longest tradition name, apart from fix 4.

**Fixes:**
1. `cue:tradition.tasting-table` (Wednesday) and `cue:tradition.department-cup` (Monday) never fire: the tradition cue lasts 1 day (SOC_CUE_OF). Add a "this week" condition with FR1, or drop the two lines. {winner} must read as a team name.
2. `cue:tradition.tiles-ladder.you`: the ladder is on Saturday, so its 1-day cue has expired by Friday too. Same remedy as 1.
3. The people pool's `pick: 2` can repeat a welcome or a goodbye. Split it into an arrivals pool and a leavers pool.
4. Line 73 is 94 characters with three leavers (Day 161). "This week" for rotations means since last Friday's address, because they land on Sundays.

**Carried:**
- myrank: still needs agreeing.
- The new slots and conditions are FR1's to build; health: is section 17's.

**For the lead:** the nod rotation has no Bridge/helm week.

## FR1 build brief: claude/fridays e420082 (turn 0). PASS WITH FIXES

**Matches the plan** rev 4 and the user's answers:
- the 15:30 crew end and the 16:00-16:50 address in the auditorium;
- the skeleton crew;
- bubbles, the banner and the Mail;
- the expected dip and its exemptions;
- "both happen" when an event falls on a Friday;
- the 16:00 auto sign-out and the normal clock (revision 3 parked).

**The hold, owners and switch:**
- The hold is one table: EV_BEATS `fridayAddress` {weekday 4, fromDay 5, at [930, 1020]} at events-base 835ab24.
- Owners: PB for sections 13 and 14, OR1 for the rest, EV1 for the storm's keep.
- Off = identical, and each turn has its checks.

**Fixes:**
1. **(Before turn 5, in the brief now.)** Don't gate captains-address with a story flag `fri.on`.
   - `flag()` reads the saved SHIP.flags, and `eventsOn` reads `ev.flag` (line 35169), which feeds the crew's planner. A save from an "on" build would bring the address into an "off" build.
   - rec-all-hands' `rec.on` is set nowhere. The rec traditions are gated by `REC_TRAD_ON` at load (line 34970). Do the same with SHORT_FRIDAY.
2. eventFree is in section 18 (line 35291), not 14. Keep the workaholic tail at most 15:45 (`over()` is strict, so 15:45 + 15 is still free at 16:00).
3. Turn 6's saved no-repeat ring: add player_check, devmode_check and a reload mid-speech. Off adds nothing to the save.
4. Turn 7: define "missed it" exactly; the 16:00 auto sign-out never counts against you.
5. Take a draw-call reading at turn 5, when about 65 first sit in the auditorium.

**Notes:**
- EV_BEATS isn't in integration yet, so the hold assert stays in the check or typeof-guarded.
- TEAM_FRI is [4, 840].
- There are 27 `DAY_SHIFT[1]` reads.
- The day shift has been 09:00-17:00 since 0.71.1.

**Re-review, ac5236a: PASS.**
- All five fixes are in, and the false clash is withdrawn in the brief.
- PB's `dayReport` "shift short" note is in turn 1.
- Leftover: turn 5's row still says `flag: fri.on`, to drop the next time FR1 edits the brief.

**EW1 re-review, claude/events-lines 307addc: PASS.**
- New condition `week:tradition.<id>` (since last Friday's address), for FR1 to build. {winner} reads as words.
- Separate arrivals and leavers pools.
- The leavers line is 74 characters.
- The bridge week is added (the lead's call; a 7-week rotation).

## EC1 bigevents_check.py turn 1 (F7a on paper, plus late saves): claude/bigevents-check bfb2b76. PASS

**Runs:**
- OK in 43 s, exit 0. Plain integration 675588c gives SKIP, exit 0.
- check_fast OK in 211 s. The game is unchanged from the merge d5c2284 (integration + events-base 0313e52).

**It fails when it should:** `plans/review-3/ec_mutants.py` breaks 7 copies of the game, and every one fails with exit 1:
- m1: the hold starts at 15:00;
- m2: the party's hash key is 341;
- m3: eventDay reads SHIP.event;
- m4: the storm's front is at 15:45;
- m5: the hold applies while the calendar is off;
- m6: late saves pass nothing over;
- m8: a tradition in the bow lounge during the party.

**EC1's finding, confirmed and sent to the lead:**
- `eventGatherings(d)` (line 36298) has no caller, so no event meeting's named crew is planned into it. This contradicts F0b's "no schedule change needed".
- It's for section 14 (PB) and EV1. eventOn goes through eventNow, so check it doesn't read live state.

**Nits:**
- The room prints twice in the gathering line.
- Who-slots like 'works:2' are skipped by the "there" check.
- The party's "3 not planned there" is only a note.
- Agree with FR1 which check asserts the address sits inside the hold.

**Gotcha:** planDay's segments are in absolute ship minutes ((d-1)*1440 + minute), not minutes of the day.

## EC1 turn 2 (one merged check with EV1's parts; F1b-c): claude/bigevents-check 85d4ee8. PASS

**Checks:**
- The game's change since turn 1 is exactly events-base 0313e52→1030626.
- The check is OK in 58 s with 17 WAITING lines; check_fast is OK in 206 s.
- The self-test catches its 3 planted clashes.

**Mutants (`ec_mutants.py`, now taking names to run only some):** 10 of 10 caught.
- The turn 1 set; m1 rewritten for EV_BEATS' new multi-row table.
- New for the guard:
  - m9: the guard ignores EV_BEATS;
  - m10: the Captain is allowed two scenes a day;
  - m11: the early table runs 95 min.

**Still open:** turn 1's nits.
- **0c48458 (turn 1 nits 1-2): PASS.** The room is listed once, and the cast slots print SKIP. Nits 3-4 are parked for F7c and FR1. The lead has routed the eventGatherings gap to EV1 + PB in F0b.

## FR1 turn 1 (A1: the switch, 18f, the crew's 15:30 Friday end, the skeleton): claude/fridays b1720a1. PASS

**Checks:**
- Build lines untouched.
- cadet_test 675588c→off: ALL IDENTICAL.
- check_fast OK in 207 s.
- day_check Day 5: OK on and off.
- day_check Day 12 fails the same way on, off and on 675588c (the rec deck's evening guard): it was already there (backlog #18).

**Probe `fr1_t1.py`:**
- Days 4, 6, 11 and 13 are identical on and off.
- The skeleton is strand-erik, shah-dara and larsen-hamid.
- Friday 16:00: helm 1 (Deck 1), watch 1 (Deck 2), infirmary 1, galley 3.
- Day 12 also keeps command and helm, from the storm's double shift.
- 8 Works crew finish a job or clock out by 15:45, inside eventFree's margin.

**Nits:**
- section.py doesn't find 18f's owner.
- recCap and deck3Full treat Friday 15:30-17:00 as working hours (for turn 5/7).
- The watch rating is on Deck 2, not the bridge (say so to the user).

## FR1 turn 2 (A2: the hours rotas' Friday, the dinner rush at 17:00): claude/fridays 3ae4bec. PASS

**Checks:**
- cadet_test off: ALL IDENTICAL.
- check_fast OK in 202 s.
- food_check OK on and off.
- day_check Day 5 on: OK.
- events_check on: OK.

**Probe:**
- The non-Fridays are identical on and off.
- The garden is empty from 15:35 on Day 5.
- The skeleton and the galley stay until 17:00.

**Code:**
- friHours splits a rota block correctly (13:00-21:00 becomes 13:00-15:30 and 17:00-21:00).
- The rush's max(workEnd, 1020) does nothing while off.
