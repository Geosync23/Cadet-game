# Handover: storm builder 2 (EV4), the ion storm update

Written 2026-10-21 by EV4 (session_01MqpjPG6mDFe5avrDxcNWTU), after S9. Read EV3's note first
(`plans/handover-storm-builder.md`: the whole design, what S1-S8 built, the gotchas), then this one.

## Role, branch, people

- **Role:** the ion storm update (plans/event-storm-plan.md v1.2 on claude/event-plan-storm), section 18's storm block
  and slot `// ---- slot: Storm builder`, with small hooks elsewhere. **Never set the build lines** (lead 23 confirmed):
  name each turn in a build-table row ("Ion storm update" table, plans/build-table.md).
- **Branch:** `claude/storm-update`: claude/fridays 7a0e5f7 merged in (lead 23's call) and S2 built on it (see the build table's 'storm S2' row). Merge `claude/storm-s4s8` (EV2) whenever EV2 pushes (last: e723f1d).
  Take `bigevents_check.py` from `claude/bigevents-check` (EC1) as is (last: e3f1da9); never edit it.
- **Lead:** lead 23, session_01XXiKm9iPgm565SZ4n1knmU (overnight: questions to the lead only, never the user).
- **Reviews:** PR4 (session_014WyaZtasY32m5fnkBxuR9d) every turn, also as the stand-in owner of 4d (props) and 8b
  (shipFeelFrame's hook). PB (session_01FWW2piuXkFYaRRzLXZiqYb) owns 10/13/14. EC1 (session_01QgShGXD6P24DDxTp8npN41)
  owns bigevents_check. EV2 (session_017S7eVMgX34nSt8fxZ5kat9) S4/S8. FR2 (session_019m7hCEtBsPA3ascA2Bqu9V) Fridays.
  ER2 (session_01S8pboNujAzZgMSWFK84CxD): the adversarial build review after S9, before S10.

## What I built (all off with `EV_STORM_ON` = `EVENTS_ON` false; cadet_test ALL IDENTICAL every turn)

| Commit | What |
| --- | --- |
| 4476186 | S1 fix 2: `eventFinish` sends the debrief unless the timed one already went (`e.mine['mail:debrief']`), then marks it. (EV3's 5b81161 was the same fix; merged, my line kept.) |
| b9aa775 | Standing diners: section 10's `trayTo(id, w)` asks the slot's pure `evStandTray(pl, w)` for crowd spots: a tray only at a meal gathering's own crowd spots, its meal, its ev- tag, its window. day_check allows exactly that. perf_check scene 'lantern supper, the mess Sat 18:30'. PB: OK. |
| 96bb2c6 | Props (4d): `dressLantern`, DECK_DRESS `lanternMess` (12 lanterns on the long tables) and `stormLantern` (the trace on the galley pass), 2 draw calls each. 8b's shipFeelFrame: `FEEL_S.lamp` eased toward the slot's `stormSupperDim(deck)` (.85 while lanternMess is out on Deck 3): the emergency-light level. |
| 4fa198f | day_check: the R6 rec-deck FAIL is a printed line on a day the storm shuts Deck 7 (PR4: PASS). |
| 05865b7 | events_check: the day-10 pick hold: you're on the Works drill (drill-pressure@10) that day, so section 17 rightly leaves the pick open; a FAIL again otherwise (PR4: fine). |
| 74c216e, 9c1a441 | Crowds (lead 23's call: supper at most 60, party at most its 34 places at once, the rest drop in): supper pull .77 (63 mean to go, 54 at once); party `stay: [30, 60]` (EV_SHIPWIDE passes a moment's `stay`): 45 come, at most 27 at once. PR4's S6 fix 1: `evDressed` keeps `base`, `evIsTrad(ev)` replaces the identity tests (the Monday Lap joinable). S1 nit: stormScripts' fallback. |
| 2228a05 | Crowds, lead 23's final rule (at most 60 meaning to go; never more at once than the places, standing counted): supper pull .73 (59 mean to go, at most 51 at once); the party has the bow lounge's standing spots again (94 places) plus its stays (at most 27 at once; 343-416 draw calls at 390 px). bigevents_check OK. |
| f32d901 | S9: DECK_DRESS `framedMenu` (the Captain's table's trace) above your keepsake shelf, bunk or cabin 4-23; a DECK_DRESS entry's `on()` (dressShow skips it while false) keeps it off with the switch. join_check allows the storm's Monday Lap. |

Shots: plans/storm-shots/ (`git add -f`: *.png is in .gitignore).

## Open (after f32d901)

- **PR4's review** of 96bb2c6 (props, 8b hook), f32d901 (S3-S7 fixes, S9) and 2228a05 (crowds): waiting (b9aa775 PASS).
- **ER2's adversarial build review** (lead 23 asked it; pointed at 2228a05): findings come to this role. S10 waits for
  ER2's PASS and the user's review.
- **Not done, told PR4:** "There's a commendation in your Mail" is said at 10:00, the Mail comes at commendAt 10:12
  (a words/timing call); `allclear.you.jobs` can't be reached (harmless).
- **S9's 'old placeholder code':** skipped; lead 23 makes it an open question for the user.
- **Deck 4 '454':** not reproducible (common room at most 323 on; perf_check's row stands in Cabin 4-05, 433-436).
- **Backlog 18b** (perf_check's scenes use tile numbers as world x,z in nearestOpen: they may measure the wrong room) and
  **#19** (join_check first-light FAIL, off too: FLC_ON): for their owners.
- **S2: built** on this branch with claude/fridays merged in (Marrow 15:35 so she leaves at 15:30, Vance 15:45, to 16:50). The Fridays builder is FR3 (session_01935gmiyLoy5fgvs3xQd7QC); the storm reviewer is PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i; PR4 handed over). fridays_check FAILs only on the storm's own address lines while the storm is off: FR3's to fix. Then S10 (the switch) after ER2's and PR6's PASS on S2.

## S10, the switch-on (for EV5, session_012DBTAAiTTNJYugQL4YLScJ; lead 23's call)

**When:** after PR6's PASS on this branch (ab58e7b / 892af70) and FR3's fridays_check fix (its "lines that never fill"
must leave out the storm's own address lines while EV_STORM_ON is off). ER2 has passed S1-S9 and S2.

**What (the plan's S10 row: "Switch on (`EVENTS_ON = true`) after the user's review; the full round; design-doc and
DEV_NOTES"):**
1. Section 18, one line: `const EVENTS_ON = false;` → `true` (it turns on EV_CAL_ON, EV_GUARD_ON, EV_NOTES_ON,
   EV_DEVICE_ON, EV_REPLAY_ON, EV_STORM_ON, EV_RANK_ON, EV_COMMS_ON with it). Keep its comment truthful. Short Fridays
   has its own switch (`SHORT_FRIDAY`), FR3's, which isn't S10's to flip; S2 only matters when both are on.
2. cadet_test now differs on purpose (the game changes): prove it like 0.15.1 did. A copy of the new build with the
   line put back to false must be ALL IDENTICAL to the build before S10. Then judge the new shots by eye.
3. The full round on the new build, as built (no copies needed now): check_fast; events_check; bigevents_check (EC1's
   newest from claude/bigevents-check; its 'off' parts then test a switched-off copy); day_check on Days 11-15 and a
   quiet day (7); food_check `BUILD 11 4` (days 28/31 known, pre-existing); join_check (first-light = backlog #19);
   social_check; devmode_check; player_check; interactions_check; device_check; perf_check (the 'lantern supper' scene;
   mind backlog 18b, its scenes stand you in the wrong room); intro_check in pieces (the plan says so); deck_check,
   machine_check, clothes_check, leave_check, career_check, mech_check. Note each FAIL against the same check on 892af70
   switched on (the old state) so only new ones count.
4. design-doc.md: the ion storm section to "built and on" (the plan's decisions, story A "Sixty by lamplight", the
   lantern supper at about 60 with 22 standing, the party drop-in, S2's address); move answered questions out of Open
   questions. DEV_NOTES: the storm update's section says it's on, and how to switch it off (the one line).
5. Build-table row "storm S10" (never the build lines: the build master's), push, then PR6 and ER2 review, and the
   lead tells the user in the morning. It reaches the user's game only through the build master's merge (Fridays first).

## Gotchas (new)

- `nearestOpen(x, z, who)` takes world coordinates: `const c = cellPos(i, j); nearestOpen(c.x, c.z, player)`.
- A gathering moment (non-meal) plans its goers onto the venue's crowd spots ('@<id>' / the venue pool), not its
  `places`; bigevents_check's "places" counts the `places` list.
- `DRESS.on` fills on eventsTick, not on goToDeck: call `EV_MIN = -1; eventsTick()` in a probe before reading it.
- Test copies: regenerate the switched-on copy after every edit (I lost a run to a stale one).
- Three lanes in parallel are fine with separate CADET_WORK dirs (cw, cw2, cw3 symlinking three/ and acorn/).

## How to test a turn

names_check → probe on a switched-on copy → the area's checks off and on (events_check, day_check 13/14, food_check
`BUILD 11 4`, join_check, bigevents_check) → cadet_test against the last pushed tip → check_fast → build-table row and
DEV_NOTES line → commit, push → PR4 (+ owners) and lead 23.
