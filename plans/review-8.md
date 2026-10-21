# Turn reviews: PR8

Second Fridays reviewer, from 2026-10-21 ~14:30 UTC (lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r). Builder: FR3
(session_01935gmiyLoy5fgvs3xQd7QC). PR5 (session_01Eh4drBZjJ82DjYx6XaTt1F) keeps turns 7, 8, 9 and 11b2220.
Pushes only to claude/review-8 (from claude/fridays 0dc4562).

Method (PR3's, as PR5 uses it): build lines untouched; cadet_test off against the base; check_fast alone; the area's
checks on; a code read; a live probe on a real save at 390x844. Checks run one at a time through
`plans/review-8/runner.sh` (resumable, res/<name>.log). Probe: `plans/review-8/p8_fri.py`; shots in
`plans/review-8/shots/` (`git add -f`).

Copies: `t10` = 0dc4562 as pushed (SHORT_FRIDAY on, EVENTS_ON off); `t10off` = the same with SHORT_FRIDAY false;
`t10ev` = on with EVENTS_ON true; `base9` = 11b2220 (the turn-9 tip).

## FR3: turn 10, switch on (0dc4562)

**Checks (each alone):**
- cadet_test base9 → t10off: ALL IDENTICAL (81 s).
- check_fast on 0dc4562: QUICK CHECK OK in 300 s.
- fridays_check t10: OK (613 s). Day 5 16:10: 49 seated, lectern Marrow + Vance. **Day 12 16:10: 51 seated, lectern []**
  (Marrow and Vance on the storm's double shift). The live fill: 26 seated at 16:00, 48 at 16:05.
- fridays_check t10ev (EVENTS_ON true): OK. Same Day 12 empty lectern; the storm's lines still never fill (no
  EV_STORM_ON in this build, so the check leaves them out; FR3's note that it fails there applies to a build with it).
- lines_check: PASS (0 errors, the 6 old warnings).
- events_check t10: OK. t10ev: FAILED, 21 FAILs, all the events base's own (ionStorm-stormBriefing / allClear "not on",
  the storm not due on day 10, ready room, Captain's table, all-clear party, eventRoutines, eventGuestDays,
  rec-slow-stretch missing Day 14, the film night move). The control copy `t10evoff` (EVENTS_ON on, Fridays off)
  fails 20 of the 21 the same. The one more with Fridays on: **quiet-watch Day 300 (a Saturday), Deck 3: 7/9 reached**
  ('rina>3-lounge-3 21:30', 'nordqvist-dmitri>3-lounge-1 21:32'); off it's 8/9 (rina only, under the threshold), and
  with EVENTS_ON off it's 8/9 too. A small knock-on of the two switches together (Nordqvist's Saturday evening walk);
  not blocking, but the combined release's events_check will show it: for FR3 / EV to look at when they merge.
- day_check 5 OK; 19 OK; 12 FAILS only backlog #18 (also with EVENTS_ON).
- bigevents_check t10: OK. t10ev: 3 FAILs, all in its own "switch off" parts (it flips the switches itself from an
  EVENTS_ON-off build): a check limit, not the game.
- join_check: OK.
- The rest of the broad round (bubble, interactions, clothes, talk, social, intro, devmode, career, mech, puzzle, food,
  perf, arc, path, tiles, disc) was dropped for lead 24's account-move window: FR3's row lists them run.

**Finds so far:**
1. **Day 12 says nothing.** With EVENTS_ON off or on, 51 people sit in the auditorium and nobody is at the lectern
   (the storm's double shift keeps Marrow and Vance on the bridge). friAddressTick waits for the line's speaker in
   DECK_CREW, so no line is ever said; a player there still counts as heard (no Mail). EVENTS_ON alone doesn't fix it:
   it needs EV4's storm update (Marrow released from 15:30, Vance from 15:45). So the "switch on together" release has
   to carry Fridays, EVENTS_ON **and** the storm update; with Fridays alone, Day 12 is a silent hall (and its Mail
   describes a storm that isn't happening).
2. **Day 19 announces an arrival that doesn't happen.** "And at dinner a new junior comes up the Tern's ramp…" and the
   Mail's "a welcome this Sunday for our new junior" are unconditional, but this build's first rotation is Day 35
   (ROSTER_ROTATIONS). Only the {sunleavers} line drops. Fix: give the welcome line a slot or condition that empties
   when no one arrives Days 20-21 (e.g. `{sunarrivals}`, as {sunleavers}), and the same for the Mail sentence; or keep
   turn 10 off the release until claude/patch-crew lands. Also "talent night … a week late" and Days 12/19/26's storm,
   comet and Veyli lines all assume the events base (find 1).
3. **An old save loaded on a Friday evening is punished for an address it never had** (probe `p8_fri.py t10 up`).
   A save written without `fri` (every save from the published game, or from any build with the switch off), Day 5 at
   18:00, loaded into 0dc4562: on the first frame FRI.mailed = 5, `rep.cnt.address` = 1 (work -2), the banner, and
   the Mail "All hands: the Captain's Friday address" stamped 18:00. The player never had a 15:30 shift end, a
   heads-up or an address to go to. It hits only saves made on a Friday from 16:50 to midnight (and on Day 5+ only),
   once, -2 work, but it's the first thing a returning player sees. Fix (18f, small): when the save has no `fri`
   part, mark today as already mailed if it's a Friday past the address's end (`if (SHORT_FRIDAY && !(SAVED && SAVED.fri)
   && friShort(SHIP.time.day) && minute >= 1010) FRI.mailed = SHIP.time.day`), or never dip on a day the save began
   past 16:50; and a fridays_check case for it (a fri-less save at Friday 18:00: no dip, no Mail).

**Live probe** (`p8_fri.py`, a real save, 390x844, logs in res/p_d5, p_up, p_d12):
- Day 5 from 15:12: the heads-up toast at 15:20 ("Short Friday · Your shift ends at 15:30. The Captain's address is
  at 16:00, in the rec deck auditorium."), FRI.hu = 5; shot `t10_d5_1524.png`. The clock words: "Short Friday: on
  shift since 15:30. Clock out from 15:30. The Captain's at four." / "Clocked out at 15:30. …"; dayShiftEnd(5) = 930.
- In the auditorium from 15:56: 43 seated with Marrow at 15:56-15:59; Vance by 16:03 (47); 49 at 16:06. Line 0 at
  16:06 is Vance's "Settle, please. The Captain." in a named bubble pinned at the right edge (162-382 px, 396-440 down:
  readable). Shot `t10_d5_1605.png`. Line 2 by 16:09.
- After 16:50: heard 5, mailed 0, work unchanged, `address` count 0: no dip, no banner. The tradition's
  "Thanks for coming" Mail came at 16:06.
- The dinner part of the probe stood on Deck 3's main lift, not in the mess (my probe's slip; shot `t10_d5_1720.png`
  is the lift). The spread is checked on paper by fridays_check (OK).
- Day 12 from 15:56 (switch on, EVENTS_ON off): 46 → 51 seated by 16:16, lectern [] all the way, FRI_SAID null at
  16:30: **no line said** (find 1). Shot `t10_d12_1630.png` (the "Feeling rough" card is the fresh save's sick roll).

**Verdict: PASS WITH FIXES.** The switch itself is sound: off is identical, the round is green apart from the known
failures, and a Day 5 Friday plays as designed on a phone. Before it ships: (1) the release must carry Fridays,
EVENTS_ON and EV4's storm update together, or Day 12's lectern stays empty and Days 12/19/26 speak of events that
don't happen (the lead's rule, now with the storm update named); (2) Day 19's welcome line and Mail sentence need a
condition on a Day 20-21 arrival (FR3's `arriving` fix, announced); (3) the old-save Friday evening dip.

## FR3: PR5's turn-6 fixes (208581c8)

**Code read:**
- `friMissed(d, e, at)` is the 16:50 path, shared by the tick and a SIM_ADVANCE hook (only when on). The hook walks
  every day from the jump's start to its end and fires for each Friday whose end (`e.to`) lies in (from, to]. The
  Mail is stamped 16:50, and `mailed` guards a repeat. A jump that ends exactly at 16:50 is the hook's; one that starts
  there is the tick's. No double.
- `heard` counts only if you were in the auditorium before the jump began: right.
- A jump across several Fridays (Dev's clock) gives one banner and one Mail per Friday, each dated, and one dip per
  Friday that was a shift day. Probe: Day 26 and Day 33 in one jump, 2 banners, 2 Mails at 16:50 on each day, count
  +2. (The big work fall in that run, 48 → 6.71, is the skipped week of missed shifts, not Fridays.)
- player_check's TOK uses section 15's own machine test (its room, MACHINE_NEAR, .8 of the panel). It hands back
  (`dropJob`) and moves on, up to 8 tries.

**Checks:**
- The new fridays_check on the old build (t10): FAILED (1), only the new case: `[[5.95, 1, True], [5.95, 1, 33, 0, 0]]`
  (no banner, no Mail, no dip). On 208581c8: FRIDAYS CHECK OK. The jump gives `[5.71, 3, 40, 1, 1]`; the weekly
  reload gives `[10, 9, True]`; the stays `[38, 13, 1031]`, none too late.
- Probe (the game's own sleepUntil, Friday Day 19 15:00 → Saturday 07:00, 208581c8): mailed 19, work 50 → 48,
  one banner, the Mail at 16:50 on Day 19. PR5's C2 is fixed.
- cadet_test t10off → f11off: ALL IDENTICAL. check_fast at 208581c8: OK in 308 s.
- player_check (switch on), mutants m11 (no hook) and m12 (Mail stamped at the jump's end): see below.

## FR3: backlog #20 (e18844fb)

Section 14 (PB reviews the section): an intro beat with only `alts` now reserves its first alt for its window in
shipDay's intro reservations, and introLay takes `alts[0]` when none is free ("they wait by it") instead of null.
Not behind a switch. Every intro beat without a named place is like this, not only d5-mug, so it can move crew who
used to sit in a beat room's first seat on any arrival-week day. FR3 ran intro --week/--evening/--firsts, day 1 and
day 5. Mine below.
