# Re-review: claude/sim-engineer 971b4c7..a7673e0 (0.26.29)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** Fixes 1 and 2 are needed before this is combined: with them out, the sim's own new day_check case and social A's social_check both fail on the full merge.

Diff read in full (section 13's bus comment, 14's gatherings, schedBuild, shipDay, introPlan and introLay, and 17's repair and job notes; also day_check, player_check, design-doc and DEV_NOTES). name_check `--branches 971b4c7 a7673e0`: NAMES OK (1 new name, `INTRO_EARLY`). Seat line OK: no new `schedU` keys.

Merges tested:
- **M1**, the full merge: origin/claude/arrival 8c28e91 + sim-engineer + deck-plans-1-2-6 + social + social-stories + player-needs + galley 28ce141. I resolved only the build lines and the DEV_NOTES table, and took player-needs' copies of player_check.py and cadet_test.py. NAMES OK.
- **M2**: M1 + origin/claude/ship-events 3463d84. The `"meal"` tags on the five traditions live only on ship-events (section 18 0.34.38), so M1 never runs the new meal code. In section 18's dialogue hunks I took the ship-events side, since it is newer there. NAMES OK.

## 1. MUST FIX (sim, section 14 `introLay`): the arrival dinner still puts two people on the Chief's seat, and the new day_check case fails on the merge
- The claim was "the arrival's seats on time and never shared". The `alts` and `free` check only covers beats by room or tile. A **named** seat (`w.placeId`, Calder's `3-mess-9` across from yours) is taken as given, with no occupancy check. On top of that, `INTRO_EARLY` moves it 5 minutes earlier, into the dinner rush.
- The proof is the sim's own new day_check part 5, run on the merges (on the branch it only prints "no arrival here"):
  - M2, `day_check.py starship-cadet.html 0` and `... 35`: `Arrival on, days 0 and 1, places booked twice: ['3-mess-9 volkov-maeve/calder@1105']` → **DAY CHECK FAILED**.
  - Probe on M2 (`newGameStart(true)`, then `shipDay(0)`): Calder `18:25-20:00 3-mess-9 intro-chief`, Volkov `18:00-18:51 dinner ev-sunday-table-talk` on 3-mess-9. Day 0 is a Sunday, the Sunday long table reserves 3-mess-9 among its first 44 seats in id order, and Volkov is one of its diners.
  - The same happens on M1 with no meal traditions at all: `3-mess-9 keane-davi/calder@18:25`, Keane `17:52-18:27`. So the named seat collides with ordinary dinner too. The 5 minutes early is exactly what makes Keane's dinner overlap.
- Suggested fix: book an intro named seat before the day is planned, so nobody else can take it. Either put it in `occ.res` for its window, tagged so only that beat may use it, or have shipDay pre-book it in `occ`. Also leave it out of a meal tradition's reserved seats. Then day_check part 5 is OK on M1 and M2.

## 2. MUST FIX (sim, section 17 `jobEffect`): the repair note's new `t` breaks social A's time-jump check on the full merge
- `simLater('repair', { ..., job: j.kind, ..., t })` now stamps the note with the job's own finish minute. For a crew job that is `j.done` (`jobFinish(j, j.done, ...)` in the hourly loop), and it can fall before the social hour already run. Before, the note carried `SIM_AT`, the hour being run.
- Proof (A/B on M1, social_check's jump part): the build as merged gives `Two days in one jump the same as hour by hour (with bus notes): False` → SOCIAL CHECK FAILED. The only failure in the full 14-day run is `a time jump gives a different social life`. In a copy of M1 that differs only by dropping `, t` from that one line (`rv-not.html`), the result is **True**. This was the open item 5 in my handover ("the jump test is True on the full merge"), and it is now broken again.
- Suggested fix: stamp it as before (leave `t` out so `SIM_AT` applies), or use `Math.max(t, SIM_AT)`. Keep `job:` as it is. Then run social_check on the full merge.

## 3. SHOULD FIX (sim, shipDay's meal-tradition reservation): reserved seats sit empty while the ordinary diners are pushed off the mess
- `n` counts everyone whose `eventPlan` includes the tradition. Not all of them eat there: the galley rota crew get their meal at rota time (`ate.dinner` is then true, so `mt` never applies), and night workers eat before. So more seats are held than are used, and the mess has only **44** mess seats.
- Probe on M2, with `shipDay(d)` over days 1-14 (M1 is the baseline, with no meal tags):
  - Sunday, day 7: 46 going, **37 sat**, all 44 mess seats reserved 17:55-19:00, and **28** ordinary dinners taken on lounge seats or benches (M1: 0).
  - Day 14: 41 reserved, 38 sat, 20 off the mess.
  - Tasting table (days 3 and 10): 27 and 30 reserved, 24 and 25 sat, 7 and 6 off the mess.
  - The 9 "going but not sat" on day 7 (janssen-hugo, takahashi-wen, navarro-mateo, reyes-alejandro, achterberg-lars, ibarra-rafael, keane-davi, jovanovic-petra, garcia-greta) all ate an ordinary dinner at 17:15-18:10, mostly on lounge seats.
  - events_check on M2 agrees: `sunday-table went 37/56`.
- Suggested fix: count only those whose plan will really use it (not on the galley rota at dinner, not eating before), or release a reserved seat 10-15 minutes in when nobody has taken it (the shipDay comment already describes that release for other events). Never reserve all the seats. This is design-visible: on Sundays a third of the ship eats dinner in the lounge with no long table.

## 4. Low (sim, player_check): the washer test no longer exercises the game's pick
- The new check uses its own filter (`kind === 'washer'`, the **first** washer in range) and never calls `machineTap`. It also skips the name-and-number match when a real washer is near.
- Proof (branch, probe for each "Washer N" item): `machineTap`'s nearest pick is correct for all four (4-washer-1..4). The test's own pick, however, is wrong for 2, 3 and 4 (`Washer 2 -> test picks 4-washer-1`, `Washer 3 -> 4-washer-2`, `Washer 4 -> 4-washer-3`). It passes today only because it tests `Washer 1` (`['Washer 1', '4-washer-1', True]`), so a wrong-washer bug in the game would go unseen.
- Suggested fix: player-needs' version (stub first, else the real machine **nearest**, sorted, and still matching the number). It is already on origin/claude/player-needs, and I took it in the merges.

## 5. Low (contract): `kind` in payloads
- The old bug "simNote overwrites a payload's `kind`" is settled **by contract, not in code**. simNote still does `Object.assign(copy, { kind, t })`. Sections 13 and 17 now send `job` (repair and job notes), and the bus comment says a payload never carries `kind`.
- Still violating it: social B's `simNote('bond', { a, b, kind, was })` (storyHour's set and drop, social-stories 15466-15467). The bond kind (friends, rivals ...) arrives as `kind: 'bond'`. Nobody listens to `bond` yet, so nothing breaks today.
- pillar4-plan.md's appendix still says `repair {who, machine, kind, deck}` and `bond {a, b, kind}`.
- Suggested fix: social B renames the field (`bond: kind`), and the lead updates the plan appendix. Also, `isFinite(data.t)` accepts `null` and numeric strings (global `isFinite` coerces). `Number.isFinite` would match the comment ("a non-number t").

## Checked, fine
- **Repair cue through the real bus** (M1, social_check): `{'cue': True, 'wrong': False, 'mem': True, 'queued': 0}`. Social A's key reads `machineById(d.machine).kind`, then `d.job`, then `d.kind` unless it is 'repair'. memRepair and repNote read only `who`, `machine` and `state`. Arrival's `introJobNote` and SETTLE read `step`, `reserved` and `tag`, never the job note's `kind`. No other branch reads repair or job `.kind` (searched arrival, social, social-stories, player-needs, galley, ship-events and ship-integration).
- **Meals:** crew still eat twice a day. day_check `meals < 2 0` on the branch (day 6) and on M2 (days 0 and 35). In M2's 14 days, nobody has two dinners: one esposito-yara "2" was a 4-minute standing gap between the queue and her seat, and she isn't going to anything. The only people with no dinner are the guests v-jaramillo-ulla and v-wexley-hale, the same in M1.
- **The galley agrees** (M2, food_check `1 7`: FOOD CHECK OK). Tradition diners are served from their first dinner segment (`galleyEvents`). The long breakfast serves to 10:00, and the tasting voters are those tagged `ev-tasting-table` (`25 went; 25 came to taste`). `day 55-58: came = got, missed 0`.
- **Determinism:** `Plans the same twice: True` on every day_check. The reservation calls `eventPlan`, which is pure. `meet` entries are new objects each build.
- **Day 0 and rotation day 35:** day_check on M2 days 0 and 35 is clean apart from finding 1 (the bunk handover and the leavers are unchanged).

## Tests
- Branch a7673e0: day_check day 6 OK, MACHINE CHECK OK, PLAYER CHECK OK. Days 0 and 35 ran on M2: the plans are clean, but the check FAILED on finding 1.
- M1: intro_check OK (parts 0-11). social_check FAILED, on the jump test only (finding 2). Repair cue OK.
- M2: food_check OK. events_check (14 days) FAILED. Those failures are not from this diff:
  - Hosts 5 minutes early (`cruz-tove at harvest-supper 17:55`, `rina at tiles-night 19:57` ...): the `e.host ? 5 : 0` rule is already in 971b4c7.
  - `one-week-aboard never happened` (arrival or traditions).
  - Reviewer 2 and the traditions engineer should look at those against the host-early rule.
