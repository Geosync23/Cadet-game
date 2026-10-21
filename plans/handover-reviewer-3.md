# Handover: turn reviewer 3 (PR3)

**Role.** PR3 is a turn reviewer for Starship Cadet. The job is adversarial: does a turn do what its plan says, does it break anything, are the checks run and green, does it work on phones?
- Started 2026-10-21 ~00:20 UTC for lead 21. Since ~01:10 it has reported to **lead 22** (session_01BGQCZLK6gYTnqu6mwZ61jB).
- Overnight (from ~03:35, the user asleep) PR3 is **the events team's turn reviewer**: EV2/EV3's events-base and storm turns, the Fridays turns and EC1's checks. Questions go to lead 22, never to the user.
- PR3 pushes only to **claude/review-3**: notes in `plans/review-3.md`, probes in `plans/review-3/`.
- Verdicts are PASS, PASS WITH FIXES (with the exact fixes) or FAIL, sent to the builder and the lead.
- Owner hooks: PB reviews sections 13, 14 and 10; PR3 covers every other section's hooks (OR1 has handed over).

A fresh session taking over reads this first, then `plans/review-3.md` (every verdict with its evidence).

## Who's who (session ids)

- Lead 22: session_01BGQCZLK6gYTnqu6mwZ61jB.
- EV2, the events base on claude/events-base-2: session_017S7eVMgX34nSt8fxZ5kat9.
- EV3, the ion storm on claude/storm-update: session_01ReekSsFi1ToaTpSq926Drq.
- EC1, bigevents_check.py on claude/bigevents-check: session_01QgShGXD6P24DDxTp8npN41.
- FR1, Fridays on claude/fridays: session_01FXFdUaCbBurQbdY9E58HKs. Handed over after turn 5; its note is `plans/handover-fridays-builder-1.md` (claude/fridays 812ff15). The lead is starting a successor.
- EW1 and EW2, writers on claude/events-lines and claude/events-lines-2: EW1 is session_01KkAhg7eVhPenBBVfLufPU1.
- PB, the sim seat (13/14/10 owner reviews): session_01FWW2piuXkFYaRRzLXZiqYb.

## Reviews done (details and evidence in plans/review-3.md)

| What | Commit | Verdict |
|---|---|---|
| EW1 friday-weekly.address | d15803c, then 307addc | PASS WITH FIXES, then PASS |
| FR1 Fridays build brief | e420082, then ac5236a | PASS WITH FIXES (no saved story flag as the gate), then PASS |
| EC1 bigevents turns 1-6 | bfb2b76, 85d4ee8, 0c48458, 4438336, b6fcaef, f5c1599, 818add7 | all PASS (mutants caught) |
| FR1 turns 1-4 | b1720a1, 3ae4bec, 3a76b2a, 56fbd2b | PASS |
| FR1 turn 5, the address as a tradition | 78112ef | **PASS WITH FIXES: the crew arrive 12-36 min late** (the open item, below) |
| EW2 nit fixes | 47a99a6 | PASS (nit: `!who:dlamini-lukas` on resolution.lines line 9) |
| EV1 F4, replay through reloads | 13bb264 | PASS |
| EV2 F0b, called in | ab67c99 | PASS WITH FIXES (calledIn missing from SOC_HEARS); fixed in ca2f9d6/394182b, PASS |
| EV2 F5 + F8 + PB's F0b fix | 80c4963 | PASS |
| EV3 storm S1 | 9561f48 | in progress at the time of writing; see the end of review-3.md |

## Open items to follow

1. **The Fridays successor's first job (FR1 turn 5's fix).** The crew set off for the address at 16:00 and arrive late. Marrow is at the lectern at 16:12, Vance at 16:27, and 49 are seated only by 16:36. Remedy: plan the trip ahead (patch #9's walk lead) or start the crew's segment earlier, plus a live part in fridays_check. Re-test with `plans/review-3/fr5_fill.py`. Expected: Marrow and Vance at the lectern by about 16:02, and at least 80% seated.
2. **Day 12's address has no Captain** (Marrow and Vance on the old storm's double shift). EV3's storm update must exempt them. Check it on EV3's turns.
3. **Attendance** is about 50 seated, against the Fridays plan's "60-70". This was told to the lead for the user.
4. **F5's rank parts** have no data yet (no meeting has ranks or scriptBy). Exercise them when EV3's S8 lands.
5. EC1's bigevents_check needs updating for S1's 5-day storm (11-16, not 11-17) and the party-night clashes (EV3's S6).
6. A design point sent to lead 22: an evFrom-0 save loaded on Day 20 runs the whole missed storm in catch-up at load.
7. Backlog rows found or confirmed: #18 (day_check Day 12's rec-deck evening guard, already failing on 0.64.6) and #19 (join_check with FLC_ON off).

## How to review (PP1's method, as used here)

1. `git fetch origin <branch>:refs/remotes/origin/<branch>`. Then `python3 tools/section.py --diff BASE HEAD`. Then `git diff BASE HEAD -- starship-cadet.html | grep -n "build 0\.\|GAME_BUILD"` must print nothing.
2. A worktree per head: `git worktree add -f /tmp/rv/<x> HEAD`. Copies: `git show C:starship-cadet.html > x.html`. A switched-on copy: `sed 's/const SHORT_FRIDAY = false/const SHORT_FRIDAY = true/'`, or `const EVENTS_ON = false;` → `true`.
3. Run these one after another in the background (never side by side; 4 cores), with `CADET_WORK=/tmp/work-RV3 CADET_CHROME=/opt/pw-browsers/chromium`:
   - cadet_test BASE→HEAD off;
   - check_fast in the worktree;
   - the area's checks, on and off.
   The setup is in DEV_NOTES "Testing": three in /tmp/cadet-work/three, acorn in /tmp/cadet-work/acorn, and /tmp/work-RV3 linking both.
4. **Mutants for EC1's check:** `plans/review-3/ec_mutants.py GAME.html [names...]` breaks copies and expects exit 1. Add new mutants for each new part. A mutant whose text isn't found prints SKIP: rewrite it against the new code.
5. **Probes:** `plans/review-3/*.py`. They need `/tmp/rv/pp.py`, made with `git show origin/claude/patch-plan:plans/patch-plan-probes/pp.py > /tmp/rv/pp.py`; set its SHOTS line to /tmp/rv/shots. Then run at 390×844 and look at the shots: `.bub{animation:none!important}`.

## Gotchas learned

- `weekday(d)` is 0 = Monday ... 6 = Sunday, in TRADITIONS, WEEK_SHAPE and EV_BEATS alike, and Day 0 is a Sunday. I once misread "weekday": 5 as Friday and raised a false clash; it was withdrawn.
- planDay's segments are in absolute ship minutes ((d-1)*1440 + minute).
- DECK_CREW's position is `a.x` / `a.z` (world). `a.h` is the render handle.
- A probe that jumps with skipTo straight into a gathering shows an empty room: the crew walk in after the jump. To see lateness, jump earlier and play frames.
- The game saves again as the page unloads. A probe that edits localStorage must block `Storage.prototype.setItem` before reloading.
- Seed a real save the way EC1 does: localStorage `starship-cadet-save` plus `starship-cadet-arrived`, under a sessionStorage "seeded" guard so a reload keeps the game's own save.
- A tradition's 1-day cue (`cue:tradition.<id>`) has expired by the next day. Writers need EW1's `week:tradition.<id>` for "this week".
- A ship note reaches section 20 only if its kind is in SOC_HEARS (the F0b bug).

## Memory

About 495k of 1M when this was written (2026-10-21 ~05:00 UTC). The rule: tell the lead at 500k; at 600k finish this note, push and stay idle.
