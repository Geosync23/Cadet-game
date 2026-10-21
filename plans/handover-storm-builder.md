# Handover: storm builder 1 (EV3), the ion storm update

Written 2026-10-21 by EV3 (session_01ReekSsFi1ToaTpSq926Drq) at about 500k tokens, after S1, S3, S5, S6, S7. A fresh
storm builder reads this, then `plans/handover-events-engineer-1.md` (EV1's, on claude/events-base) and the storm plan
(`plans/event-storm-plan.md` v1.2 on claude/event-plan-storm: every recommendation decided, story A).

## Role, branch, people

- **Role:** the ion storm update, turns S1-S10 of the storm plan, in section 18 (this role holds it for events) with
  small hooks elsewhere. Never set the build number.
- **Branch:** `claude/storm-update` (from claude/events-base 13bb264 + claude/events-base-2 merged, 89b976f). Pushed:
  9561f48 (S1), d3bf237 (S3, S5, S6, S7). Merge claude/events-base-2 again as EV2 pushes (F5 ranks, F8 comms).
- **Lead:** lead 23, session_01XXiKm9iPgm565SZ4n1knmU (lead 22 has handed over; overnight: questions to the lead
  only). **Reviews:** PR4 (session_014WyaZtasY32m5fnkBxuR9d) each turn, the hooks outside 13/14/10 and the props as the
  4d stand-in (PR3 has handed over; its partial S1 notes are in claude/review-3 plans/handover-reviewer-3.md); PB (session_01FWW2piuXkFYaRRzLXZiqYb) for
  sections 13/14/10; EC1 (session_01QgShGXD6P24DDxTp8npN41) owns bigevents_check.py (never edit it; I took 818add7 as is);
  ER2 (session_01S8pboNujAzZgMSWFK84CxD) does the adversarial build review after S9, before S10. EV2
  (session_017S7eVMgX34nSt8fxZ5kat9) built S4 and S8 on claude/storm-s4s8 (merged into claude/storm-update, ff16dd5);
  read plans/handover-events-engineer-2.md: don't replace `S.jobs.warning` (it pushes stormRota), don't replace the
  stormBriefing meeting object (it sets scriptBy, F5), don't register 'calderStorm.officer' (it does).
  FR2 (session_019m7hCEtBsPA3ascA2Bqu9V) builds the Fridays (the Day 12 address).

## What's built (all behind `const EV_STORM_ON = EVENTS_ON`, section 18 by the other EV_ lines)

Off = today's storm: cadet_test ALL IDENTICAL against the turn before, every turn. Details per turn: plans/build-table.md
"Ion storm update" rows S1, S3, S5, S6, S7; DEV_NOTES "The ion storm update".

- **Data:** one block right after `stormCallBacklog` (`if (EV_STORM_ON) { const S = SHIP_EVENTS.ionStorm; ... }`).
  It must stay before the `EV_SHIPWIDE` loop and EV2's `EV_MEET_TAGS` (both made from the storm at load).
- **Functions:** the slot `// ---- slot: Storm builder` at the end of section 18. Anything the data block calls at load
  must be a function declaration (evWord, evWordAt, evFill, evBankMail): consts there are in their dead zone at load.
- **S1:** days 5; briefing 14:00; jobs 852 (pick held); `settle`/`eventSettle` (e.mine.settled; eventScore stops);
  `commendAt [3, 612]`/`eventCommend`; debrief a timed Mail [4, 1080]; writers' Mail/banner/commendation; stormScripts
  (baked calderStorm; captainAllClear by band via a `get lines()`, the 'you' line after "Mine too").
- **S3:** 'deck:7' closed onset+escalation; `evOpenFor`; section 14 evClosed + recVisit; 15r recEventShut; first
  all-hands = Day 5 16:50 (`stormAllHandsTick`).
- **S5:** lanternSupper moment (k 352, meal 'dinner', places seats + @long-table + @gather-mess, Brennan 1); routine
  `off`; dressing `at`; timed Mail; stormLanterns job 14:00; galley keeps the bridge's tray portions 16:00-18:00 (16).
- **S6:** `EV_DAY_DRESS` (declared beside eventsOn; evDressMake/evDressed; dressed copies made lazily: spreading a
  tradition at load hits fields that read ROSTER). Lap to Monday 20:30, talent night to Day 21, party words, tidy 10:30.
- **S7:** stormStoryTick (play only, e.mine 'story:*'); stormMoment ('moment:' copies, never a commendation); range job
  via postEventJob + `reserved`/`until` when you're on another job; Mail `unless`; `settleTraces` stormLantern.
- **Words:** EW1/EW2's ionStorm files are in content/ (moved from plans/events-ready/ionStorm, claude/events-lines-2 7a9761a).

## Decided tonight (leads 22 and 23)

- **Props:** no deck architect seat is live: the storm builder builds DECK_DRESS 'lanternMess' (S5) and the trace
  'stormLantern' (S7) in the deck kit's style (col() for every colour, no coplanar surfaces, shared kit made at load
  never calls R()), with phone shots (390x844) and draw calls measured with ~60 in the mess (budget 450). PR4 reviews.
- **Standing diners:** the supper keeps its 22 standing places and they eat standing with a tray, scoped as PB said:
  (1) section 14's tradMeal gives the tray and standing pose only when the place is one of that gathering's own crowd
  spots (type 'event', `gather` = its venue) during its meal; (2) day_check allows exactly that (a '<deck>-<venue>-crowd-N'
  spot, act dinner, the gathering's ev- tag, in its window); (3) behind EV_STORM_ON; (4) a perf_check scene at 18:30.
  The user confirms in the morning: keep it easy to switch off (dropping `{ deck: 3, pool: '@gather-mess' }` from the
  supper's places gives about 48). NOT BUILT YET.
- **S2:** wait until claude/fridays reaches claude/integration (never merge claude/fridays); the Marrow/Vance window is
  [940, 1010] (15:40-16:50): agree the exact minute with FR2.
- **PR4's S1 find, fixed** (after d3bf237): the briefing pick wasn't held when section 17 had already posted the job
  for 14:12 at 14:00 (the board hides future postings, so claimJob failed): eventTakeJob holds it directly; events_check
  LIVE asserts the battery job is claimedBy 'you' after the briefing.

## Open finds (after ff16dd5)

- **The pick held, day-10 path:** events_check's LIVE part (the storm started on day 10) shows the battery job you picked
  is posted at 14:12 with `wants:stormBatteries` set but stays open (claimedBy null), though `playerShiftOn(10)` is true;
  a probe with the storm started on Day 11 (the calendar's) holds it ('claimed:you'). It prints a NOTE, not a FAIL.
  Find why section 17's claim-on-post (eventJobsHour, `wants:` and `!mine`) refuses on day 10, then make it a FAIL again.
- **bigevents_check (EC1's cdf80ce) switched on:** "party: 45 people for 34 places"; "lanternSupper: a crowd of 68, over
  about 60" (my probe counted 59 at the supper's places: see what EC1 counts, likely everyone in the mess at 18:30);
  "Lap of the Wren not on D15 at 20:30" (my probe has it on: check how its 'calendar'/'on' parts flip the switches;
  EV_DAY_DRESS needs EV_STORM_ON and EV_CAL_ON); plus its known 'off:'/'calendar:' rows that test a switched-on copy.

## PR4's S1 review (PASS WITH FIXES)

- Fix 1 (the pick held): done in 3367aab (see the open find above for the day-10 path).
- Fix 2 (an event ended early, Dev mode's End, got no debrief): done after fc23557 (eventFinish sends its own debrief
  unless the timed one already went: `e.mine['mail:debrief']`).
- Nits, open: "There's a commendation in your Mail" is said about 12 minutes before the letter (send it as the all-clear
  opens, or reword); `event.ionStorm.allclear.you.jobs` can't be reached (one job + the all-clear is always a
  commendation); stormScripts' fallback index is -2 when neither "Mine too" nor a choice is found.

## Left to do

1. **S2 (waits on lead 22's call about Fridays):** the 'captains-address' tradition exists only on claude/fridays.
   Design: the doubleShift rule gets `except: [{ ids: ['marrow', 'vance'], day: 1, at: [960, 1010] }]`; section 18's
   evArrive lets a person on a double shift go to a tradition in that window (return e.from), eventPlan marks it
   `meet: true`, section 14's gatherings() passes `meet` (and act 'work') through so shiftWithBreaks makes it a break
   (EV2's F0b 'meet' mechanism). Stay-in not in the Friday hold: add `off` windows (S5's mechanism) or filter by
   `evHeld(t)` in eventRoutines. The all-clear's four called in: EV2's F0b already plans named people into meetings
   (check day_check 14 and bigevents cast). The 24p promotion hold (lead 22): a typeof-guarded line in
   `promoSummonsDay()` skipping a day d when [d, summonsAt], [d, 17:00 move] or [d+1, 17:15 ceremony] falls in the
   storm's held span (a new pure `evHeldFor(d, m)` from evCalPlan: onset start to the all-clear's end). PB reviews 14,
   PR3 reviews 24p.
0. **The standing-tray scoping and the two props** (above).
2. **S4: built by EV2** (merged). ballasts → blackout, batteries → bridgeHungry, booth rota job → calls; calls retune in
   `stormCallBacklog` only (about 25 min a call left alone, 15 with the rota), never `callOwed`. bigevents_check runs
   the three ways.
3. **S8: built by EV2** (merged; check its scriptBy officer works with stormScripts' baked calderStorm). banner on phones (HUD), status/Schedule/Record, the Officer's briefing
   (`calderStorm.officer`, rank officer+, via F5's ranks; stormScripts currently installs the junior version only).
4. **S9:** small things (placeholder code, the framed menu prop, Deck 4 common room draw calls 454) and the supper's
   perf_check scene (about 60 in the mess, 390x844).
5. Then ER2's review, then S10 (switch on only after the user's review).

## Open questions / waiting on others

- **PB:** the supper's 22 standing diners eat standing with a tray; day_check 13 (switched on) FAILs "standing still
  with a tray". Options sent: (a) allow it in tradMeal + day_check (recommended), (b) no tray when standing, (c) drop
  the standing spots (about 48 instead of 55-60).
- **Deck architect (lead 22 to name):** DECK_DRESS 'lanternMess' (lanterns on the long tables, mess lights at emergency
  level, 17:30-19:45 Saturday) and the trace 'stormLantern' (a lantern on the galley pass from the all-clear; tap words
  `event.ionStorm.trace.lantern`). Unknown ids show nothing until built.
- **EC1:** bigevents_check expects 'ionStorm:11-17' (now 11-16) and its stormNew test makes the party-night clashes
  FAIL until S6 (now built: rerun it).
- day_check's rec-deck evening comparison FAILs on storm days by design (the deck is shut): the check's owner may skip
  it when `eventClosed({ deck: 7 })` holds; Day 12 off already fails it (backlog #18).

## Gotchas

- Container restarts: commit locally before long checks. My resumable runner: a script that appends "TAG exit N tail"
  to a log and skips finished tags; one CADET_WORK per lane; cd to a scratch dir (cadet_test writes shots to cwd).
- `pkill -f <pattern>` matched my own shell and killed it (exit 144): kill by PID.
- cadet_test under a busy machine once showed a_start differing (13097 px); alone it was identical, twice.
- events_check switched on now passes; its HOOKS part clears EV_DAYS/SHIP_DAYS first (earlier parts plan the storm
  from day 10).
- food_check switched on has five FAILs on the base too (menu, garden x2, late meals, rota): not ours.

## How to test a turn

names_check → probe on a switched-on copy (cadet_test's Game class: `exec(open('cadet_test.py').read().split('a, shots
= run(')[0])`; skipTo, setShipNow, eventsTick, goToDeck, cellPos/nearestOpen to place the player) → area checks off
and on (events_check, day_check N, food_check N, join_check, devmode_check, bigevents_check) → cadet_test previous vs
new → check_fast alone → build-table row → commit, push → PR3 (+ owners) and lead 22.
