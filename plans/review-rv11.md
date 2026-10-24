# RV11's reviews for 0.92.2 (2026-10-23)

Reviewer RV11, reporting to lead 31, then lead 32 (from ~20:30 UTC), and BM15. All three fixes are on claude/integration-next 54efee21 (the 0.92.1 candidate).
Runs: `plans/review-rv11/runs.txt` (each check's exit code, time and last line). Probes: `plans/review-rv11/*.py`.

| Fix | Branch, commit | Verdict |
|---|---|---|
| FX6 team repairs near new | claude/team-restore 28bcc102 | PASS |
| DV1 Day 2 solo job | claude/d2-solo-tap e81ef301 (292f4f77 + a test-only line) | PASS |
| FX3 relay shelf glow | claude/p5-fix3 04c38a76 (+ 5d1b7290 handover, docs) | PASS (after one fix) |
| DS1 goodnight words | claude/goodnight-words afc5e7a4 | FIXES NEEDED, then cancelled by lead 32 |

## FX6: TEAM_RESTORE 90 to 98
- One constant (section 17), used by the team finish and 24h's teamOthersRight. design-doc Machines paragraph added.
- machine_check: on 54efee21 it fails only on "team repairs leave machines at 90, not close to new". OK on the fix.
- mech_check: on 54efee21 it fails only on "m8: a team job leaves its machines close to new". OK on the fix.
- Planted faults, both caught by machine_check: TEAM_RESTORE 97 (the 98 line); the team finish left at 90 (5w, recycler 94.6 as it was done).
- check_fast OK; cadet_test ALL IDENTICAL; day_check 1 and 16 OK.
- What a player sees: machines fixed by a team job read 98% instead of 90%.

## DV1: a tap on the speaker walks you in; the arrow at the visitor spot
- introMeetGo (section 21) is asked first in introTap; the beat row carries `place: b.stand` (section 19).
- Part 18 (--solotap): fails on 54efee21 (arrow, walk, meeting); OK on the fix.
- Planted faults caught: no place (the arrow line); no playerGo (the walk and meeting lines).
- First gap: a wider time window was not caught. The 10:05 tap is refused by the met guard first.
- DV1 added an 08:35 tap (e81ef301). It catches the window start planted 30 minutes early (path 5), and passes on the fix.
- Full intro_check OK; interactions_check OK; check_fast OK; cadet_test ALL IDENTICAL.
- Side effect probed (d1_probe.py), the Monday briefing: a tap on Calder from the main lift at 08:52 walks you to the bay's first map tile [13,0], and the briefing starts at 08:55 as you enter.

## FX3: a tap on the glow takes the part
- First version (85b6250a) was on dbc62255, not 54efee21. It also asked the glow before tapCrew, so a tap on a crewmate standing in front of the glow fetched the part instead of talking to them. fx3_crew_probe.py: 30 of 30 fetch (54efee21: 30 of 30 talk).
- FX3 moved the glow tap to after tapCrew, rebased onto 54efee21 (04c38a76), and added a crew line to the check.
- FX3's block run alone (fx3_only.py): on 54efee21 the glow line fails (22 of 216); on the fix it passes (216 of 216), and the crew line passes (6 of 6 talk).
- Planted faults: glow before tapCrew (85b6250a's game) is caught by the crew line; the wrong shelf is caught by the glow line (216 of 216).
- My probe on the fix: 30 of 30 talk.
- Whole interactions_check, machine_check, player_check and check_fast OK.
- cadet_test: the first run showed 14,812 px in a_start, all inside a speech bubble, on a loaded machine. A re-run and a base-vs-base run were both ALL IDENTICAL.

## DS1 goodnight words (cancelled)
- "Breakfast from six", but the game serves breakfast from 07:00 (MEALS [420, 540]; the servery's text says 07:00).
- Lead 32 cancelled it: ZW1 misread MEALS.

## Gotchas
- interactions_check takes about 50 minutes with 3 or 4 browsers running at once; it is about 30 minutes alone.
- A copy of intro_check.py or interactions_check.py must keep its file name, because it finds cadet_test.py by replacing its own name.
- `pgrep -f`/`pkill -f` with the pattern in the same command line matches the shell itself; use `ps -eo pid,args | grep '[x]...'`.

# RV11's reviews for 0.92.3 (2026-10-24; lead 32, then lead 33 from ~04:00 UTC)

All from claude/integration 364c80cb (0.92.2). Runs appended to `plans/review-rv11/runs.txt`; new probes fx4_shots.py, fx8_occ.py, ds1_tip.py.

| Fix | Items | Branch, commit | Verdict |
|---|---|---|---|
| FX4 | 2, 12, 14, 20, 26 | claude/p923-fx4 97251620 | PASS (after two item-14 fixes) |
| FX8 | 22, 28 | claude/p923-fx8 9fd5b500 | PASS (after one fix) |
| DS1 | 1, 7, 8, 9, 10 | claude/p923-ds1 b49a01db | PASS (notes) |

## FX4
- First look (64b28176) found two item-14 problems. The HUD button still read "Tracked" (only its aria-label had changed). At 320 px the lift's "→ Schedule tracker" badge ran 27 px past its deck button (318 vs 291).
- 97251620 fixed both; device_check has a line for each, and both fail on 9be5c21e.
- device_check's new lines fail on 364c80cb. Planted faults caught: meter hidden; beam at 15 min; on-shift badge; old badge style.
- Item 26: clothes_check's three lines fail on 64b28176. Plants caught: no tip; remarks for stale clothes only; flag renamed.
- check_fast, player_check and the full interactions_check OK. cadet_test: only the HUD button's box and j_steer1's bump word.
- Notes: on Day 1 at 10:00 the old "Yesterday's clothes" toast and the new tip say the same at once. Dinner's 16:45 heads-up waits behind the beam strip.

## FX8
- First look (35c4a252): the tap kept occasion appointments too. Proved (fx8_occ.py): a tap on Calder from the Works bay marked her progress talk met on the device, with the occasion unmet.
- 9fd5b500 skips occasions and needs the person in the appointment's room or within 2.5 tiles of their spot. Two new lines fail on 35c4a252.
- Plants caught: occasion skip removed; the "there for it" test removed.
- Full interactions_check, check_fast and day_check 2 OK; cadet_test ALL IDENTICAL.
- Nit: on old builds the check crashes on "apptTapKeep is not defined" rather than failing cleanly.
- Item 28: findings only.

## DS1
- Part 18 (--p923) fails on 364c80cb for all five items. All five planted faults are caught.
- check_fast and clothes_check OK; cadet_test ALL IDENTICAL.
- Full intro_check: two of three runs crashed in part 12 at the new game's form-button click; the third passed, as did 0.92.2's full run. A repro (part 13, then a new game) hangs on that click on 0.92.2 too, so this is read as a check flake.
- Notes: two "part 18"s in intro_check; a comment moved off INTRO_ARROWS.call; the stand-in bedtime tip is about 220 characters (nine lines at 320 px) and lines_check doesn't see it.

## Gotchas (new)
- A fake work meter (ACT without kind) breaks recFrame on the next frame; fake it with ACT.kind set and don't step frames.
- intro_check --firsts runs part 13b, which the full run doesn't, so it is not a faithful repro of the full run's order.

# RV11's reviews for 0.92.4 (2026-10-24; lead 33, then lead 34 from ~15:00 UTC)

From claude/integration 3866c8f3 (0.92.3).

| Fix | Item | Branch, commit | Verdict |
|---|---|---|---|
| FX4 | B: dirty clothes | claude/p924-fx4 177bcc37 | PASS (after one fix) |
| FX8 | C: crew glide off a place | claude/p924-fx8 69356d11 | PASS (after a test-only fix) |

- FX4: 823a6d25 cut the only "no clean clothes left" message, and its next-day tip pointed at an empty wardrobe. 7301d763 gives both tips a laundry wording when you're out of clean clothes, and 177bcc37 rewords it.
- FX4 checks: clothes_check's new lines fail before and pass after; plants caught (same-day tip; out-of-clothes branch off). check_fast, player_check OK; cadet_test ALL IDENTICAL.
- FX8: g8_mesh.py reads the drawn body (a.h.pos) frame by frame. On Deck 3, short get-ups move at most 0.13 tiles a frame (0.92.3: 1.09); long ones (over CREW_UP_MAX 1.2) still jump at once, by design.
- FX8 checks: cadet_test differences are the glide alone (with CREW_UP_V = 1e9, ALL IDENTICAL). day_check, path, bubble and check_fast OK.
- FX8's open fix: day_check's line sums a.x + a.lx + a.hx instead of reading the drawn body, so a plant that drops hx from h.set (a visible hop) passes.
- FX8 69356d11: day_check's line reads a.h.pos. The hx-dropped plant now fails all 7 decks (0.94-1.19); OK on the fix; fails on 3866c8f3. Long get-ups still hop by design; backlog FX8-1 (swimmer leaving a lane, 5.2 tiles) is old.

# RV11's reviews for 0.92.5 (2026-10-24; lead 34)

| Fix | Items | Branch, commit | Verdict |
|---|---|---|---|
| FX9 | 6 (piano only for talent night), 7 (booth/sofa/armchair flicker) | claude/p925-fx9b 863d43d0 | PASS |

- deck_check's two new parts fail on 3866c8f3 and pass on the fix. Plants caught: booth backrest back to 1.40; armchair arms back to the old sizes; piano always visible.
- A hidden piano takes no taps (pick uses isShown); floor taps ignore its rec:act place. Its tiles stay blocked on other nights.
- check_fast and events_check OK. cadet_test differs only at Deck 4's lounge seats (crops viewed).
- The screenshots FX9 named (plans/shots-0925-*.png) aren't in the commit.
