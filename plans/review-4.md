# Turn reviews: PR4

Turn reviewer 4, from 2026-10-21 ~04:50 UTC; took over from PR3 (plans/handover-reviewer-3.md on claude/review-3).
Reports to lead 23 (session_01XXiKm9iPgm565SZ4n1knmU); lead 22 until 05:12. Pushes only to claude/review-4.
The method is PR3's: section.py --diff, build lines untouched, check_fast alone, cadet_test off against the turn's base,
the area's checks on and off, a code read, a live probe at 390x844 for anything timed, saved or on screen.

Setup in this container: `pip install playwright`; three and acorn in /tmp/work-RV4 (and /tmp/work-RV4b); probes load
`plans/review-4/pp.py` (cadet_test.py's top). Worktrees per head in the scratchpad (`w/<x>`), on-copies by
`sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true;/'`. Long runs go through a resumable runner (each step
writes res/<name>.log and .done), because the container restarts.

## EV3 storm S1 (the new hours): claude/storm-update 9561f48, base 89b976f. PASS WITH FIXES (fix 1 blocks)

**Checks:**
- Build lines untouched. Sections: 22 (the generated lines) and 18.
- cadet_test 89b976f→9561f48 off: ALL IDENTICAL (PR3's too).
- check_fast OK in 245 s.
- events_check off: OK. lines_check: PASS (0 errors, 50 warnings).
- bigevents_check (S1's own copy) fails only on the party-night clashes (S6) and the typed 11-17 (EC1's cdf80ce reads 11-16).
- events_check on: 9 FAILs, all also on the base switched on (which had 10 more: the meeting tags S1's check change skips). Nothing new.

**Probe `s1_hours.py` (on-copy, a real save Day 11 13:30):**
- The briefing opens at 14:00 in the Works bay, and Calder's new script plays.
- The device's heads-up replaces the meeting's own toast (F3a), so `told:` stays unset. Not a bug.
- The storm jobs post at 852.
- Thursday 17:00-18:30: no storm Mail.
- Sunday 10:00: settled `bumpy` (blackout 117, spoiled 31, bridgeHungry 12, calls 7.7); the threads are unchanged at 22:00.
- The Captain's line to you is spliced in after Calder's "Mine too" (shot `s1_allclear_you.png`).
- The commendation comes once: the Mail at 10:12 (614 after a skip), across a reload before and after.
- The debrief comes once, Day 15 18:00, from Calder. The event ends Monday midnight (log 11-16). Nothing is sent twice.

Verdict sent to EV3 and lead 23 at ~06:05.

**Fixes:**
1. **(Blocking) Your briefing pick isn't held** (`s1_pick.py`).
   - machinesNow runs hour 14 at 14:00, so jobsHour posts the jobs before the reply, with `posted` 852 (still in the future).
   - eventTakeJob finds the open job, but claimJob looks it up in jobsBoard(), which hides jobs not yet posted, so the claim fails silently.
   - Section 17's wants: claim already ran, and nothing claims it later. All four jobs stay open, claimedBy null, at 14:24.
   - Fix: in eventTakeJob, hold a not-yet-posted open job the way section 17 does (claimedBy 'you', status 'claimed', start j.posted).
   - Assert in a check that the picked job is claimedBy 'you' after 14:12. events_check only checks wants:.
2. PR3's edge 2: with `mail.debrief` set, eventFinish skips the debrief, so an event ended early (Dev mode's End) gets none. Send it in eventFinish when `!e.mine['mail:debrief']`.

**Nits:**
- The Captain says "There's a commendation in your Mail" about 12 minutes before it comes (the all-clear plays at 10:00 in real seconds; the Mail is at 10:12).
- `allclear.you.jobs` can't be reached: one job plus the all-clear (counted as it opens) is always a commendation.
- PR3's edge 1: stormScripts' fallback `findIndex(choice) - 1` gives -2 when neither line is there.
- Crew reaction lines about the lantern supper (S5) are baked with S1 (seen Tuesday 01:00). Fine while off.

## EC1 turns 7 + 8: claude/bigevents-check cdf80ce, f9b2b0b. PASS

- check_fast on f9b2b0b: OK in 296 s. bigevents_check: OK, exit 0.
- Called in: the four at 19321, with the same four cues.
- Mutants c1-c6 (`ec_mutants.py`): 6 of 6 caught.
  - c1: no SOC_HEARS;
  - c2: the note twice;
  - c3: the note at minute 0;
  - c4: Vance noted too;
  - c5: notes while off;
  - c6: the log's endDay +1.
- Nit: cues are read once, at +65.

## EV2 storm S4 (your help counts): claude/storm-s4s8 f2a0eaa + af568f9, base 6608a07. PASS

- cadet_test off: ALL IDENTICAL. check_fast OK in 356 s. events_check off OK. machine_check on OK.
- Probe `s4_help.py`, skipped to Sunday 10:05:
  - left alone: blackout 117, spoiled 31, bridgeHungry 12, calls 4.8 → bumpy;
  - with all three prep jobs done by you Thursday 15:00, and a reload Saturday: 59 / 31 / 6 / 2.9 → smooth, helped:* kept.
- Hooks (16, 17 stand-in): typeof-guarded and null while off. Blackouts come only after the front, and the help is fixed by then, so replays stay consistent.
- Nit: blackoutHour's comment still says "pure".

## Gotchas (PR4)

- `*.png` is in .gitignore: shots need `git add -f`. EV2's plans/storm-shots and EV4's props shots were never pushed for that reason.
- A probe save that starts after an event's day has that event passed over (F0c, evFrom = the load day). Put `'evFrom': 0` in the save's ship.
- `pkill -f <name>` also matches your own shell's command line: kill by PID.
- events_check's LIVE part runs the storm on Day 10 (a day off for you): the briefing pick isn't held there by design (a NOTE).
