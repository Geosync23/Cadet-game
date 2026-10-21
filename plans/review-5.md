# Turn reviews: PR5

Turn reviewer 5, from 2026-10-21 ~08:30 UTC. Took over the Fridays queue from PR4, which keeps the storm. Reports to
lead 23 (session_01XXiKm9iPgm565SZ4n1knmU). Pushes only to claude/review-5 (from claude/fridays 8415d1e).

The method is PR3's (plans/review-3.md on claude/review-3):
- the build lines untouched;
- check_fast alone on the machine;
- cadet_test with the switch off against the base;
- the area's checks on a switch-on copy;
- a code read;
- a live probe on a real save at 390x844;
- mutants planted in the build to prove fridays_check catches them.

The checks run one at a time through a resumable runner (`plans/review-5/runner.sh`: each step writes res/<name>.log
and .done). Probes are in `plans/review-5/`; shots are in `plans/review-5/shots/` (`git add -f`: *.png is ignored).

## FR2: the turn-5 fix (8415d1e) and turn 6, the speech (a22d651). Base: integration 0.64.7 (6ea5acf), merged at 4ee3fdc

**Checks** (the switch-on copy is `sed 's/^const SHORT_FRIDAY = false;/const SHORT_FRIDAY = true;/'`):
- cadet_test from 6ea5acf to 8415d1e, off: ALL IDENTICAL.
- check_fast OK in 441 s.
- lines_check: PASS (0 errors, 6 old warnings).
- fridays_check: OK in 493 s.
  - Day 5 from 15:45: 26 seated at 16:00 with Marrow at the lectern; Vance there by 16:04; 48 of 51 seated by 16:05.
  - All 19 lines said in order, the hush held.
  - The weekly speech has 9-12 lines; save.fri is 786 B with a full ring.
- events_check, on and off: OK. The address: 51 of 63 went on Days 5, 12 and 26.
- day_check Day 5, on: OK.
- day_check Day 12, on: FAILS "the rec deck is on but nobody came to it in the evening". This is backlog #18 (see below).
- bubble_check, on: OK.
- devmode_check, on: OK.
- player_check, on: FAILS in its job loop (fix 1).

**Code read:**
- **friLead:**
  - A day worker sets off at the later of (start - 18..28 min) and their shift's end + 8. Marrow sets off at -30; Vance at his shift's end + 2.
  - It reads only schedFrame, eventFree and seeded schedU (key 1183), so it's pure for the planner.
  - It never makes a goer later than evArrive did (`Math.min(at, ...)`).
  - Off, nothing reads it: FRI_ADDRESS isn't in the traditions.
- **Section 14's join:** `ev-captains-address` sits beside `/^ev-rec-/`. The late joiner's stay is cut to end at 16:50. PB OK'd it.
- **friAddressTick:**
  - It runs only behind `SHORT_FRIDAY`, from eventsTick.
  - Line i comes at 16:04 + i·44/n, by the clock: about 6 real seconds a line, and the bubble lasts the line less 0.4 s.
  - CHATTER_AT is set every frame you're in the room. Section 22's overheard player and section 20's chatter both wait on it (its gap).
- **friSpeech:** the speech is made once a day and kept in FRI.today. The ring keeps 6 weeks and is filtered on load (junk dropped).
- **friFill:** a missing reader gives null, so the line is dropped. The `{winner}` slot calls tallyOf / tallyLabel unguarded; both exist in the build.
- **friSpeaker:**
  - The stand-in finds where the line from you to the speaker leaves the screen (12 halvings), so the bubble sits at that edge.
  - bubblePerson reads w.p, so the bubble is named.
  - One shared FRI_AT vector serves both stand-ins (see the nits).
- **content_gen parse_address:** a bad condition, slot, pose or speaker is an error at bake time. The ids are line_id(file, beat, text).

**Live probe** `fr6_speech.py` (a real save, Day 5, at 390x844):
- Seated: 43 at 15:55, 48 at 16:03 (Marrow and Vance at the lectern), 49 from 16:07.
- Lines 1, 3, 5, 6, 8 at 16:07, 16:11, 16:15, 16:19 and 16:23, on time.
- **The pinned bubble** (shot `on_d5_1606.png`):
  - Marrow is off the right of the screen. Her bubble sits at the right edge, 142-382 px across and 340-425 down.
  - It is named "Captain Odile Marrow", with the tail toward the lectern. It's readable and sits still over still frames.
- **A real reload at 16:24** (saveGame, then the page reloaded):
  - FRI.today is the same 19 ids, and line 9 shows: the line of the moment, not line 0.
  - You're still in the auditorium (Deck 7, room A).
- (Harness note: the first run's reload timed out at Playwright's default 30 s. Give goto 240 s.)

**Mutants:** see below.

**Fixes:**
1. **player_check fails with the switch on** (8415d1e; FR2 reports it OK, so check it on the new head):
   - With the address on, the auditorium seats wear from Day 5, so on Day 11 the first service job is `7-aud-seats@212`. Off, it's `3-filter-1`.
   - The job loop's TAPI taps the ITEM nearest the machine's panel spot. On Deck 7 that is the Lectern (1.3 tiles), and the tap does nothing.
   - The game is fine: a job is done through the Repair button at the panel (jobTap). Tapping the "Seats" item sits you down, as it should.
   - Fix (in player_check, the player engineer's file; there's no seat, so FR3 with the lead's OK): pick a job whose nearest item to the panel is its own, or skip machines where it isn't. This is DEV_NOTES' "checks never assume" rule.
2. **A skipped or slept Friday gets nothing** (probe C2):
   - From Friday Day 19 15:00, skipTo Saturday 07:00. FRI.mailed stays 12: no banner, no Mail, and (turn 7) no dip.
   - friAddressTick acts only on the day itself, after 16:50. Anything crossing midnight (sleepUntil, a nap, Dev's clock) jumps over it.
   - Fix: a SIM_ADVANCE (from, to) hook. When the jump crosses a Friday's 16:50, with the address on that day and neither heard nor mailed, do the 16:50 path.
   - Plus a fridays_check case for it.
   - Probe C1 (missed by staying on Deck 4 on Day 12) is right: one banner at 16:50 and one Mail.
3. **fridays_check gaps** (found by mutants m6 and m7):
   - (a) Reload a weekly speech (Day 33+) after changing a condition; the ids must be kept.
   - (b) On paper, no captains-address segment ends after 16:50.

**Mutants** (`mutants.py`; `mutants.out`): 8 of 10 caught.
- Caught:
  - m1: no lead;
  - m2: no 6-week ring;
  - m3: heard not set;
  - m4: no hush;
  - m5: fri saved while off;
  - m8: the Mail every frame;
  - m9: no 90-character limit;
  - m10: Vance 18 minutes later.
- Missed:
  - m6: friSpeech ignores FRI.today. The check reloads only a dated speech, which comes out the same anyway.
  - m7: a late joiner stays e.dur. events_check misses it too; the overrun is at most about 10 minutes, inside LINGER.

**For turn 10 (sent to the lead):**
- friday-d12.address talks about the ion storm with no condition.
- 0.64.8 has EVENTS_ON false. With SHORT_FRIDAY on alone, the Captain describes a storm that isn't happening.
- Switch both on together, or gate Day 12's speech on the storm.

**Nits:**
- The baked pose, tone and `to: you` aren't used by 18f.
- One FRI_AT vector serves both stand-ins.
- {winner} calls tallyOf and tallyLabel unguarded (both exist).

**Verdict: PASS WITH FIXES** (fixes 1 and 2 block turn 10). Sent to FR3 (FR2 handed over) and lead 24 at ~12:55.

## Gotchas (PR5)

- A probe that plays every frame from 15:35 to 16:24 on Day 5 at 390x844 takes more than 25 minutes. Start the save at 15:55 or 16:18, with step(20).
- A page reload inside a probe needs `goto(..., timeout=240000)`. Don't use `wait_until='commit'`: wait_for_function then never saw __sc.
- fridays_check takes about 8 minutes here (493 s); player_check about 30 minutes.
