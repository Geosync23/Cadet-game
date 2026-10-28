# Starship Cadet: the testing guide

The whole testing process in one place, in plain language. DEV_NOTES.md's "Testing" section is the short version;
this is the long one. Written by TS3 (the test-speed engineer) on 2026-10-21 at the user's request, on
`claude/opt-tests`; checked for accuracy by OR2. Numbers are from 0.64.12 (claude/integration a4a5735) unless
another build is named. When a number here and a check's own output disagree, the check is right: fix this page.

## THE RULE: every game change runs the full round, split across six check runners

**The user, 2026-10-22: "We just need to keep testing fully."** Every change to the game runs the **full round** of
checks (all 33, the event days included) **before it is merged or published**, always **split across six check
runners (CR1-CR6) at once**, about 65 minutes (interactions_check alone is ~64 since 0.93.3; backlog BM18-1). The test picker (`tools/affected.py`, section 4) is only a quick aid
while you work; it is **never the gate**. check_fast still runs before every push.

### The six-way split (fixed; balanced on the measured minutes alone, about 260 in all; rebalanced in 0.93.3 for interactions_check's ~64 min)

| Runner | Its share | Minutes alone |
|---|---|---|
| **CR1** | `player_check` (the long one, ~20 min on a release run: a light share), devmode, bubble, puzzle, social, talk; the four arrows checks (arrows, arrows_pointer, dev_arrow); `day_check` Days **4, 11** (Thursdays: the bunk inspection, from 0.93.2) | ~45 |
| **CR2** | `intro_check` (whole), `perf_check BUILD OLD`, `cadet_test OLD BUILD`, path, arc, lines, `lines_check --day`, p926; `day_check` Days **21, 22** (the comet; from 0.93.3) | ~54 |
| **CR3** | `day_check` Days **0, 1, 5, 7**, weekend (from 0.92.5); arrows_d, arrows_f, controller (every part but reach); promo_sight, `sound_check` (from 0.93.3) | ~52 |
| **CR4** | `day_check` Days **6, 8, 12, 13** (storm Saturday), **16, 19**; appt_check; `saves_check` (from 0.93.2) | ~45 |
| **CR5** | `interactions_check` (whole; ~64 min since 0.93.3, backlog BM18-1), career | ~66 |
| **CR6** | `bash check_fast.sh` (words, names, deck, machine, leave, device), mech, bigevents, fridays, disc, tiles, join, food (`1 7` and `11 4`), clothes, stories, `promo_beats_check` (from 0.93.2); `day_check` Day **27**, events (from 0.93.3) | ~54 |

`OLD` = the last release's game (`git show <release commit>:starship-cadet.html > old.html`). Every check runs with
its default arguments unless the table says otherwise (`intro_check` whole, not in pieces). If a check is added, give
it to the runner with the lightest share and update this table and the picker's `CHECKS` (section 4).

### How a runner runs its share (step by step)

1. **Check out the named commit** the build master sends: `git fetch origin <branch> && git checkout --detach <commit>`.
2. **Confirm the game file**: `sha256sum starship-cadet.html` must equal the sha256 the build master sent. If it
   doesn't, stop and tell the build master: you'd be testing a different file.
3. Set up once (section 2's setup: playwright, three.js r128 and acorn in `CADET_WORK`, `CADET_CHROME`), and use your
   own `CADET_WORK` (`export CADET_WORK=/tmp/work-crN`).
4. **Run your share one check at a time**, in the table's order, each with its exit code and last line kept
   (`python3 X_check.py starship-cadet.html > logs/X.txt 2>&1; echo "X exit $?"`). Long shares: split into background
   scripts under 90 minutes.
5. **For any FAIL**: run the same check on the last release's game (`OLD`). If it fails there **the same way** and has
   a backlog row in the list of known old failures below, it's a known old failure. Anything else is **new**: say so
   plainly, with the FAIL lines.
6. **Write `plans/checks-crN.md`** on your own branch (`claude/checks-crN`): the commit, the sha256, then a table
   `Check | Result | Key lines`, then each FAIL with "known old (backlog N)" or "NEW", and the proof (the OLD run).
7. **Report to the build master and the lead**: "CRn: OK" or "CRn: FAIL: <check>: <one line>, known old (backlog N) /
   NEW", with the link to your notes.

### Runners talk to each other

The six runners, the build master and the lead message each other directly (session ids are in `TEAM.md`, not here)
when:
1. **a sha256 doesn't match**: tell everyone and stop; nobody tests until the build master sends the right one;
2. **a failure could affect other shares** (a broken build, the game crashing on load, a shared setup problem): tell
   everyone at once, so nobody spends half an hour on a broken file;
3. **someone fixes a setup problem** (a missing package, a CADET_WORK mix-up): share the fix;
4. **someone finishes early**: offer to take a check from the slowest runner; agree it between the two of you, copy
   the lead, and never run a check twice by accident (the one who hands it over says so before the other starts);
5. **any FAIL not on the known-old list**: tell the build master and the lead at once, not only in your notes.

### The build master's part

1. Build the candidate (section 7): merges, switches, `content_gen.py --check`, `node names_check.js`, check_fast.
2. **Send all six runners the commit and the game's sha256** (`sha256sum starship-cadet.html`), and the last
   release's commit for `OLD`.
3. **Wait for all six reports.**
4. **Merge and publish only when every runner says OK, or every FAIL is a known old one** (below, with its backlog row
   and the OLD run showing the same FAIL). Any NEW FAIL: back to the change's owner; nothing is merged or published.
5. Record the round: the build-table row names the six runners' notes and the sha256.

### What counts as a known old failure

A FAIL is **known old** only if all three hold: it has a row in `plans/backlog.md`; the same check on the last release
(`OLD`) fails **the same way**; and its message matches the row. **The list (lead 25, 2026-10-22): backlog 12**
(career_check `busy: "Relied on" before Day 5`) **and backlog 14** (perf_check "memory grows across deck round trips",
+2 geometries a lap). Nothing else. **Updated for 0.64.15 on (lead 26/27): the list is backlog 14 and backlog 23** (food_check `7 1` "garden, good", fails the same on 0.64.14); backlog 12 no longer shows since playtest patch 1's part G, and its return would be the old failure, not a new one. **perf_check frame-time spikes:** a spike in one scene that doesn't repeat on a second measure is noise (three rounds, three different one-off spikes, none repeated: backlog 32); re-measure before calling it. Three that used to fail are **fixed in 0.64.14** (claude/integration 8e239328):
backlog 18 (day_check Day 12 "the rec deck is on but nobody came", PB2's fix), backlog 26 (tiles_check
"opening the board adds nothing to the 3D scene") and food_check `11 4` "harvest salad" (PB2's fix). On 0.64.14 and
later they must pass: if one fails again, it's a real FAIL.

Contents
1. Why we test this way (the user's rules)
2. Every check: what it covers, how long, how to run it, what its FAILs mean
3. The full round
4. The test picker (`tools/affected.py`)
5. Remaking the coverage map, step by step
6. The replay proof, the planted faults and the known failures
7. The release-candidate procedure
8. Pixel-identical regressions, browser quirks, old vs new failures
9. Troubleshooting, and a worked example from 21 October
10. Glossary

---

## 1. Why we test this way (the user's rules)

The game is one big file that many sessions change at once. The checks are what keep one session's change from
quietly breaking another's. The user's rules, in their words where we have them:

- **Safety first.** "Careful" was the user's choice for picking checks (2026-10-21, 19:15): "rules + the coverage map
  as it is: any check that runs a changed line is picked". A faster setting ("Middle") was tried and only to be adopted
  "if its replay picks ALL 23 known failures ... If it misses even one, we stay on (a)" (21:45). It saved nothing, so
  we stay on Careful.
- **The full round runs on every game change** before it's merged or published, split across six check runners (the
  user, 2026-10-22: "We just need to keep testing fully"; see THE RULE at the top). Earlier (2026-10-21) it was: before
  every release, when the map is remade, and at least once a day.
- **A shortcut has to prove itself first.** From the optimization plan: the picker "applies only once turn 1 shows it
  would have caught every real failure of the last 20 merges".
- **Never push when check_fast says FAILED** (CLAUDE.md, "How we work").
- **Regressions on unchanged decks must be pixel-identical**, and when they aren't, find out why before moving on
  (CLAUDE.md). New features stay switched off, and "off" must be ALL IDENTICAL against the build before.
- **Checks play the real, drawn game** (the user, 2026-10-21): no headless-only or no-drawing runs. The one exception:
  player_check's polling steps may skip drawing (user OK, 21 Oct); everything else draws.
- **Never change the look of the game** (pixels identical); no texture cache.
- **Saved-game fixtures** (starting a check from a stored save instead of playing up to it): only with caution, never
  as the only check, and not in this optimization pass (the user's answer to the plan).
- **Found a bug outside your brief? Add a row to `plans/backlog.md`**; don't fix it on the side (CLAUDE.md).
- **Run browser checks one at a time** (at most two on a 4-core machine, each in its own CADET_WORK; see 3.3).

## 2. Every check

All browser checks need `CADET_CHROME=/opt/pw-browsers/chromium` in a cloud session, and `CADET_WORK` (default
`/tmp/cadet-work`) holding three.js r128 in `three/` (and acorn 8.12.1 in `acorn/` for check_fast). Setup in a fresh
container:

```
pip install playwright numpy pillow
mkdir -p /tmp/cadet-work/three /tmp/cadet-work/acorn /tmp/cadet-work/test
cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
cd /tmp/cadet-work/acorn && npm pack acorn@8.12.1 && tar xzf acorn-8.12.1.tgz
export CADET_CHROME=/opt/pw-browsers/chromium
```

**check_fast in a fresh container:** names_check needs acorn (`npm pack acorn@8.12.1` into `$CADET_WORK/acorn`, as
above); without it the quick check stops at its second step (lead 27).

Every check **exits 1 when it fails** and prints an OK line when it passes; a step counts as passed only with both
(exit 0 and the OK line). "Minutes" are minutes alone on 4 cores (`CHECKS` in tools/affected.py; measured in
plans/opt-measure.md on claude/opt-render, section 4, and since). `BUILD.html` means the game file you're testing.

### 2.1 The quick check and its parts

| Check | What it covers | Minutes | Run | OK line |
|---|---|---|---|---|
| **check_fast.sh** | The quick check before every push: content_gen --check, names_check, then two lanes side by side (deck → machine → leave, and device), each in its own CADET_WORK. Stops early if a fast step fails. GitHub runs the same on every push that touches the game, the checks or the words. | ~5 (4-7) | `bash check_fast.sh` (`CHECK_LOGS` sets the log folder) | `QUICK CHECK OK in N s` |
| **content_gen.py --check** | The words baked into the game (LINES, MEETINGS, TALKS, TRADITIONS, ADDRESSES) match `content/`. | seconds | `python3 content_gen.py starship-cadet.html --check`; to bake: drop `--check`, then check again | `up to date: ...` |
| **names_check.js** | The script parses as the browser reads it; no name, shared-table key or registration made twice (gated blocks included); no "Deck 7" on screen. | 1 s | `node names_check.js [GAME.html]` | `names_check: OK` |
| **deck_check.py** | Every deck: each room tile and tappable thing reachable from the lift, places valid, crew and draw calls listed, Deck 4's memory over round trips. | 4 | `python3 deck_check.py BUILD.html` | `DECK CHECK OK` |
| **machine_check.py** | The ship's machines on paper for 14 days: wear, faults, repairs, with an ideal crew and the real Works crew; looks and effects in range; the same twice. | 1 | `python3 machine_check.py BUILD.html [DAYS]` | `MACHINE CHECK OK` |
| **leave_check.py** | Leave, missed shifts and being let go, on paper: booking leave, sick days, the Chief → Captain → let go, recovery, the save size. | 1 | `python3 leave_check.py BUILD.html` | `LEAVE CHECK OK` |
| **device_check.py** | Section 19, your device: every app opens and draws, home tiles and badges, Back/Close, heads-ups, Maps, Memos, Needs, the Schedule lists only what really happens. | 4 | `python3 device_check.py BUILD.html` | `device_check: OK` |

Common FAILs: `QUICK CHECK FAILED (the fast steps; browser checks not run)` means the words weren't baked (run
content_gen) or names_check found a parse error or a name made twice (it names both copies' section and line).
Otherwise check_fast prints each failing step's log path and first FAIL lines. A deck_check FAIL is usually a room
or item you can't reach.

### 2.2 The other checks

| Check | What it covers | Minutes | Run (useful arguments) | OK line |
|---|---|---|---|---|
| **cadet_test.py** | Compares two builds on Deck 4: game state, 300 paths, 3000 collision probes, crew, taps, ~15 screenshots. See 8.1. | 2 | from a scratch folder: `git show HEAD~1:starship-cadet.html > old.html; python3 cadet_test.py old.html BUILD.html` | `ALL IDENTICAL` |
| **day_check.py** | Fast-forwards one ship day: everyone sleeps 6 h+ in their own bed, eats twice, works their shift; no place held twice; nobody stuck over 10 ship minutes; draw calls under 450; the same day twice. | 8 per day | `python3 day_check.py BUILD.html DAY` (DAY default 1, a Monday). The event days: see 3.2 | `DAY CHECK OK` |
| **player_check.py** | Section 15, you: needs over normal and neglect weeks, the speed rule, sleep, bonuses, Mail, the store, machines, carts, crawlways, activities; `--long` checks the save stays under 250 KB to Day 280. | 6 | `python3 player_check.py BUILD.html` / `--long [DAYS]` | `PLAYER CHECK OK` / `SAVE BUDGET OK` |
| **intro_check.py** | The arrival and first week (section 21), parts 0-12: the happy path, the wanderer and the idler, save and reload at every step, skip-intro, the evening walked in the real game (part 8), first launch, the week's beats. | 11 whole | `python3 intro_check.py BUILD.html` (everything); `--evening` (part 8, ~5 min), `--dawdle` (part 8, lingering), `--week` (the week, 3-7 min), `--week --beats=d4-quiz,d5-invite`, `--firsts` | `OK` |
| **interactions_check.py** | Section 15b: tapping real things starts the activity (pose, need rising), "In use", private places left alone, the job board, the goal pointer, draw calls. | ~64 (since 0.93.3; was 8; backlog BM18-1) | `python3 interactions_check.py BUILD.html [--quick]` | `INTERACTIONS CHECK OK` |
| **perf_check.py** | Busy scenes at phone size (portrait 1.5 and 0.7 zoom, landscape): draw calls (budget 450), triangles, game ms a frame, crew; memory over a week and deck round trips; with OLD, regressions. You must stand in the scene's own room. | 15 with OLD | `python3 perf_check.py BUILD.html OLD.html` (writes perf_check.json in the folder you run it from: move it before committing) | `PERF CHECK OK` |
| **mech_check.py** | Each mechanic on the ladder: its training end to end, stage 0 once trained, twice the same, then its own parts. | 6 | `python3 mech_check.py BUILD.html [m1 m4 ...]` | `MECH CHECK OK` |
| **events_check.py** | The small traditions (section 18): each due exactly when it should be, who goes and where, the deck minute by minute, Mail the evening before, ship notes, the voice budget, a ship year on paper. | 6 | `python3 events_check.py BUILD.html [DAYS]` | `EVENTS CHECK OK` |
| **bigevents_check.py** | The ship-wide events (storm, comet, diplomatic visit) from the game's data: off = today's game; on (in a copy): calendar days, phases, the Friday hold, the career-beat guard, casts, places, clashes, late saves. | 5 | `python3 bigevents_check.py BUILD.html` | `BIGEVENTS CHECK OK` |
| **fridays_check.py** | Short Fridays and the Captain's address (section 18f), off and on copies: the 15:30 shift end, the address every Friday from Day 5, the speakers and seats, the speech lines, the missed banner and Mail. | 4 | `python3 fridays_check.py BUILD.html` | `FRIDAYS CHECK OK` |
| **bubble_check.py** | Speech bubbles at phone size with uneven frame times: they follow the speaker without shaking, jumping or swapping sides. | 5 | `python3 bubble_check.py BUILD.html` | `BUBBLE CHECK OK` |
| **devmode_check.py** | Dev mode (section 25, `#dev`): nothing without the Dev link, the real save untouched, Undo, Mark, the Dev clock, Take me to, Set career, Traditions, the Career tab. | 5 | `python3 devmode_check.py BUILD.html [off real store clock move slow career set card trad]` | `DEVMODE CHECK OK` |
| **dev_arrow_check.py** | Dev mode's career arrow (section 25's slot, DV1): none without #dev; through the first career steps (Day 0 to Hauling's ask, Teaching arrows Off, another deck) it names the right next step; drawn with its DEV tag, still over frames, apart from the game's arrow on and off screen; Show/Hide kept over a reload. | 2 | `python3 dev_arrow_check.py BUILD.html [off walk look]` | `DEV ARROW CHECK OK` |
| **disc_check.py** | Lightdisc (23b): rules, determinism, balance, the same game at 60/30/20 fps, the save, a game on the deck under 200 draw calls. | 3 | `python3 disc_check.py BUILD.html [GAMES]` | `ALL OK` |
| **tiles_check.py** | Tiles (23): rules, balance, skill order, determinism, the board on 320/390 phones (44 px squares, a game by taps), the board adds nothing to the 3D scene. | 3 | `python3 tiles_check.py BUILD.html [GAMES]` | `ALL OK` |
| **join_check.py** | Tap to join (18): being there doesn't join, tapping the leader does, markers and arrows, Lap of the Wren, Name on the beam, through a reload. | 3 | `python3 join_check.py BUILD.html` | `JOIN CHECK OK` |
| **weekend_check.py** | The weekend traditions (18, on from 0.92.5; a copy with WEEKEND_ON off is the base): the 4-week rotation's days, the old weekend traditions unchanged (days, times, places, hosts; at most 2 people fewer, never under their fewest), hosts, at least 5 at the late ones, every join and its end (seated ones in a seat), decor on its days, no birthday within an hour, the deck head-count table, Bread day, the jigsaw, the Sunday story. | 12 | `python3 weekend_check.py BUILD.html` | `WEEKEND CHECK OK` |
| **clothes_check.py** | Clothes and laundry by real taps: the wardrobe, yesterday's clothes, the hamper, the washers, the save mid-wash. | 2 | `python3 clothes_check.py BUILD.html` | `ALL OK` |
| **path_check.py** | `findPath` gives exactly the old `findPathScan`'s paths: random pairs on every deck, then every real call of a played Monday. | 2 | `python3 path_check.py BUILD.html [PAIRS]` | `PATH CHECK OK` |
| **puzzle_check.py** | The head-scratchers (24k): the chips, the case engine's bands and rates, a case in play, the save. | 2 | `python3 puzzle_check.py BUILD.html` | `PUZZLE CHECK OK` |
| **food_check.py** | The galley over whole days: food ready on time, waits, portions, the dish pit, cold store, the rota, carts, spoilage, menu, harvest, garden. | 2 | `python3 food_check.py BUILD.html [DAY N]` (default 1 7; releases also run `11 4`) | `FOOD CHECK OK` |
| **career_check.py** | The Works career on paper: a steady, a very busy and a lazy player; each row on its day; bands, tools, penalties, the save. | 2 | `python3 career_check.py BUILD.html` | `CAREER CHECK OK` |
| **social_check.py** | The crew's social life on paper: 14 days twice the same, a big jump = hour by hour, the save, Say hello / Talk a while, affinities and news. | 1 | `python3 social_check.py BUILD.html [DAYS]` / `--long` | `SOCIAL CHECK OK` |
| **talk_check.py** | Talk a while's picker on paper: baked, no repeats, gates, determinism, the save; part (i), repeated lines over Days 1-3 with a chatty player (DL1). | 2 | `python3 talk_check.py BUILD.html` | `TALK CHECK OK` |
| **arc_check.py** | Can every story arc reach its last beat? A diligent player over 70 days; a stalled arc is listed with its next beat. | 1 | `python3 arc_check.py BUILD.html [DAYS] [arcs\|themes\|calls\|booth]` | `ARC CHECK OK` |
| **lines_check.py** | The writers' `content/` files: parseable, tokens, conditions, length, crew ids, banned words, baked blocks up to date (warnings don't fail); `--day` the voice budget in the browser. | 1 | `python3 lines_check.py [GAME.html]` / `--day` | `lines_check: PASS (0 errors, N warnings)` |

### 2.3 Known FAILs and what they mean

Only backlog 12 and 14 are **known old** failures that don't block a merge (THE RULE, at the top); the others below are flakes or fixed, listed so you can recognise them. A known one must look exactly like this. A new
FAIL, or one of these with a different message, is new (see 8.3).

| Check | FAIL | What it means |
|---|---|---|
| career_check | `busy: "Relied on" before Day 5` | Known and accepted (backlog 12 and 17): waits for the user's balancing pass. Never "fix" it by changing the check. |
| perf_check | `memory grows across deck round trips` (+2 geometries: 548 → 548 → 550 in backlog 14; 520 → 520 → 522 on the storm + Fridays candidate) | Known (backlog 14). perf_check exits 1 on this alone. A single frame-time spike can also show; measure again. |
| tiles_check | `phone 390 (or 320): opening the board adds nothing to the 3D scene` | **Fixed in 0.64.14 (claude/integration 8e239328): must pass from then on; a FAIL is real.** Before: Known since 0.64.11 (backlog 26): the check's own timing. It counts while the device's framing still eases on real time and something comes into view. Not a game bug. |
| devmode_check | the clock part: `clocked in, the jump didn't keep you clocked in` | A flake (backlog 21): real-time waits plus, before DB2's fix, a random seed giving an early sick day about 1 run in 28. Run it alone; open until full runs stay green. |
| day_check Day 12 | `the rec deck is on but nobody came to it in the evening` | **Fixed in 0.64.14 (claude/integration 8e239328): must pass from then on; a FAIL is real.** Before: Backlog 18: on Day 12 (a Friday) the plans' rec-deck evening is empty **with the storm off too** (0.64.6; claude/fridays with SHORT_FRIDAY off); Day 5 passes. Open. |
| day_check Day 13 (storm on) | the same message, on the storm's Saturday | A separate case: the storm shuts the rec deck that day; EV4's 4fa198f skips the comparison only on days the storm shuts the deck. Check it on the combined storm build. |
| day_check Day 3 | two crew in one breakfast seat (e.g. 3-mess-42) | Backlog 11. |
| food_check `11 4` | `harvest salad` (part 4g) | **Fixed in 0.64.14 (claude/integration 8e239328): must pass from then on; a FAIL is real.** Before: Since 0.64.11's crew patch Day 20 is the farewell supper (CR2's find; no backlog row yet). `1 7` passes. |
| food_check from Day 7 | `garden, good` (4j) | Backlog 23. |
| join_check | `first-light: not on in 400 days` | Backlog 19, when `FLC_ON` is off. |
| lines_check | warnings | Never a FAIL. Integration has 6 known warnings; the storm build 49 (43 storm meeting repeats). |
| cadet_test | i_tap1 a few pixels 1 level off | Renderer noise; counted as identical. See 8.1. |

## 3. The full round

### 3.1 When it's required

The full round runs on **every game change, before it is merged or published**, split across the six runners (THE
RULE, at the top). It also runs whenever the coverage map is remade (the map run itself doesn't count). While you're
working, check_fast before every push, and the picker (section 4) as a quick aid.

### 3.2 What's in it, and in what order

The full round is `check_fast` plus every entry in `CHECKS` in tools/affected.py (`python3 tools/affected.py` on a
change to cadet_test.py prints them all, with `--cmd` for the commands). Run the cheap, telling ones first so a
problem shows early:

1. `bash check_fast.sh` (5 min: words, names, deck, machine, leave, device)
2. `cadet_test.py OLD.html BUILD.html` against the last release (2 min)
3. the short ones: lines, talk, social, arc, career, food (and `food 11 4`), clothes, path, puzzle, join, disc, tiles (~20 min)
4. day_check on Day 1, then **the event days** (8 min each; below)
5. events, bigevents, fridays, mech, bubble, devmode (~31 min)
6. player, interactions (14 min)
7. perf_check against the last release (15 min)
8. intro_check whole (11 min; or in pieces: `--evening`, `--firsts`, `--week`)

**The event days** (lead 25, 2026-10-21: day_check on Day 1 alone misses an event day's own failures, e.g. the storm's
Days 12-13). From the game's calendar (`EV_CALENDAR`, `EV_BEATS`, `ROSTER_ROTATIONS`, section 18f):

| Day | What happens | day_check entry |
|---|---|---|
| 0 | the arrival (Sunday) | `day0` |
| 1 | the first Monday (the baseline) | `day1` |
| 5 | the first Friday: Short Fridays and the Captain's address (when on) | `day5` |
| 7 | Crossing the Line (Sunday; its Mail on Day 6) | `day7` |
| 12 | the ion storm's front (Friday; the warning is Day 11) | `day12` |
| 13 | the storm's Saturday (the rec deck shut) | `day13` |
| 15 | Pillar 5 Step 5: your Tier 3 test (09:00-15:00, with `P5_STEP5` on; off, a plain Monday) | `day15` |
| 16 | Pillar 5 Step 5: your result 08:15 and the Senior Officer's bar 16:30 (with `P5_STEP5` on; also the visit's warning with the swap) | `day16` |
| 17 | the diplomatic visit's greeting (Wednesday 10:00; the visit is Days 16-19 since the event swap, 0.93.2, `EV_SWAP_ON`; was `day16`, the comet's old day) | `day17` |
| 19 | a Friday with its own address, and your first night shift | `day19` |
| 21 | the first crew rotation (the Tern) | `day21` |
| 22 | the comet (Monday 21:30, since the event swap; was `day27`, the visit's old finale) | `day22` |
| 23 | Pillar 5 Step 6: the crews' welcome 06:00, the Captain's badge 16:30, your second night from 21:00 (with `P5_STEP6` on; off, a plain Tuesday) | `day23` |
| 24 | Pillar 5 Step 6: your third night, leading a team (with `P5_STEP6` on; off, a plain Wednesday) | `day24` |
| 25 | Pillar 5 Step 6: off nights at 06:00, your Deck 2 quarters after dinner (with `P5_STEP6` on; off, a plain Thursday) | `day25` |
| 26 | Pillar 5 Step 6: mentoring Basil 09:00-15:30, Calder's question at Four weeks aboard 18:40 (with `P5_STEP6` on; also Day 26's address) | `day26` |

Others worth a run when their area changes: Day 9 (the officer's test), 10-11 (summons, ceremony), 14 (the storm's
all-clear), 77 (the next rotation). The picker already names the days above (`EVENT_DAYS`; Days 23-26 added by Step 6's first turn, W6, about 16 minutes more in the round: the build master puts them on the lightest shares). When the calendar gains
an event day: add it to `EVENT_DAYS` **and** its own `CHECKS` entry (the `dayN` line) in tools/affected.py, to the
rules of the section that holds the event, and to `ALL` in `plans/opt-cover/cov_run.sh` (its `day[0-9]*` case runs
whichever days are named); its cover lands in the map at the next remake.

With the event days the full round is 33 checks, about 176 minutes alone, plus check_fast.

### 3.3 Run one at a time

- **One browser check at a time** is the rule; at most two on a 4-core machine, each in its **own CADET_WORK**: every
  check copies the build into `$CADET_WORK/test/` under fixed names (`_career_save.html`, `_mech_save.html`, ...), so
  two runs in one folder can load each other's copy and pass falsely.
  `export CADET_WORK=/tmp/work-<tag>; mkdir -p $CADET_WORK/test; ln -sfn /tmp/cadet-work/three $CADET_WORK/three`
- A third browser at once gave "game failed to start"; five gave 30 s load timeouts. A busy machine once changed
  cadet_test's shots f, g and h.
- Background commands stop at their time limit (2 hours at most): split the round into scripts of about 90 minutes
  (e.g. check_fast + cadet_test + the short ones; then the days; then the long ones).

### 3.4 Recording the results

- A runner writes a notes file on its own branch (e.g. `plans/checks-cr2.md`): the build (base, merges, conflicts,
  switch values with line numbers, content_gen --check, names_check, the sha256), then a table `Check | Result | Key
  lines`, then any FAIL with "old or new" and its proof (8.3).
- The build master keeps `plans/cand-<build>-results.md` and adds the build's row to `plans/build-table.md` with the
  proof (e.g. "cadet_test vs c575a8e ALL IDENTICAL (0 px on every shot), check_fast QUICK CHECK OK in 317 s").
- Judge each check by **both** its exit code and its last line.

## 4. The test picker (`tools/affected.py`)

**The picker is a quick aid while you work, never the gate** (the user, 2026-10-22): the full round decides (THE
RULE, at the top).

### 4.1 Using it

```
python3 tools/affected.py               # your branch since it left claude/integration, uncommitted work included
python3 tools/affected.py A B           # one change, e.g. M~1 M for a merge
python3 tools/affected.py --why         # what picked each check
python3 tools/affected.py --cmd         # the commands, shortest first
```

While working: `bash check_fast.sh`, then the commands `--cmd` prints, one at a time, to find a problem early. It
changes nothing.

### 4.2 How it decides

It picks the **union** of two lists and never fewer than either:

1. **The rules** (`RULES` in the script): for each game section a change touches, the checks DEV_NOTES says to run
   "whenever it changes". Sections everything reads (1, 4, 4a, 4c, 12, 13) run every check. **A section not in the
   table runs every check**, so a new section is never missed.
2. **The coverage map** (`tools/check_map.json`): every check was run once with Chrome recording which game lines it
   ran. A change picks every check that **ran one of the changed lines** (for a pure insertion, the lines either
   side), and for a changed table or other top-level value, every check that **ran a line reading it**. The changed
   lines are moved into the map's own game by a diff, so a map from a slightly older build still lines up. Lines that
   ran only while the page opened pick cadet (and deck, which check_fast runs anyway).

Other files: a check file picks that check (day_check.py picks every day); cadet_test.py picks everything (every check
runs on it); `content/` picks section 22's checks (lines, talk, bubble). tools/, plans/ and notes pick nothing.
check_fast's own checks (deck, machine, leave, device) are never listed: they run anyway.

### 4.3 The rules table

The rules, as of 0.64.12 (`RULES` in tools/affected.py is the master; `python3 tools/section.py` lists the sections):

| Section | Checks |
|---|---|
| page (HTML, CSS) | cadet, interactions, bubble |
| 1 setup, 4 / 4a / 4c, 12 main loop, 13 time and save | everything |
| 2, 3 textures, kit | cadet, deck |
| 4b | cadet, deck, perf |
| 4d | cadet, deck, day1, events, path |
| 4e | cadet, deck, disc, day1 |
| 5 | cadet, perf |
| 6 | cadet, bubble |
| 7 paths | path, day1 |
| 8, 8b, 8c | cadet, perf (+ day1; 8c: disc, day1, perf) |
| 9 crew data | day1, events, cadet, deck, day21 |
| 10 crew agents | day1, cadet, deck, events |
| 11 input | cadet, interactions, bubble |
| 14 schedules | day1, events, food, machine, intro, cadet, join, bigevents, fridays, day12, day21 |
| 15 player | player, interactions, clothes, leave |
| 15b, 15r | interactions, player, join / deck, disc, interactions |
| 16 food | food, day1 |
| 17 machines | machine, mech, career, puzzle |
| 18 events | events, join, intro, bigevents, fridays, day7, day12, day13, day17, day22 |
| 18f Fridays | fridays, events, join, intro, bigevents, day1, food, perf, day5, day19 |
| 19 device | device, puzzle, player |
| 20, 20c social | social, arc, bubble, lines / social, arc |
| 21, 21b intro | intro, clothes, day0 / clothes |
| 22 words | lines, talk, bubble |
| 23, 23b games | tiles / disc |
| 24 and its parts | career, mech, leave (24k: puzzle, mech, career) |
| 25 Dev mode | devmode |

### 4.4 The settings: (a) Careful and (b) Middle

- **(a) Careful, the picker's setting** (the user, 2026-10-21; since 2026-10-22 an aid only): the rules plus the whole map, as above. Over the last 20 game
  commits it picks on average 24 of 33 checks, about 132 minutes (the full round with the event days: 176 minutes;
  the rules alone: 12 checks, 73 minutes). Before the event days were added it was 17 of 24 checks, 77 of 104 minutes.
  The event days come together: every day_check day runs nearly the same planner code, so a change one day runs,
  most days run. Picks vary with what a turn's lines reach, not its area: in the replay most Dev mode turns pick 1 check but one
  picked 23; most crew, events and Fridays turns pick 20-24 (close to the full round), but one crew turn picked 6 and
  one events turn 10.
- **(b) Middle, tried and not used** (`--middle`): lines that nearly every check runs (at least 23 of 28: about 2,000
  of the 50,000 lines any check runs) pick by the rules only, and **a change to one of those shared lines runs the full
  round** (the shared-code safeguard). It picked every known failure, but saved nothing (17.4 checks, 77 min before the event days; 24.7, 133 min with them): the
  safeguard fires on 9 of 20 commits, because most turns touch the shared crew and clock code. **Known hole** (OR2's
  F1): a changed table read only by shared lines escapes both the map and the safeguard (222 such tables; DAY's hemi
  .85 → .86 picks 21 checks under (a), 3 under (b)). Fix before any second look: fire the safeguard on such tables too;
  one shared neighbour enough for an insertion; `SHARED` as a share (80%) of the map's checks.

### 4.5 When NOT to trust it (run the full round instead)

- **Before a release, when the map is remade, and once a day**: always the full round (3.1).
- **The map is old**: big new code since the map's build (a new deck, a new section, a switch turned on) picks only by
  its neighbours and the rules. Remake the map (section 5) or run the full round.
- **A switch is flipped** (`EVENTS_ON`, `SHORT_FRIDAY`, `REC_DECK`, ...): the map was made with it off, so the code
  behind it never ran in the map. Its section's rules still pick, but run the full round for a switch-on.
- **The game doesn't parse** (the picker says so and picks everything).
- **A merge of several branches**: pick on `M~1 M` and on each branch; when in doubt, the full round.
- **A check file you don't know** (a brand-new check): it isn't in `CHECKS` until someone adds it; run it yourself.
- **Real-time or browser trouble** (toasts, framing, GPU canvas): the map only knows which lines ran, not timing.
- **Shared files outside the game** (cadet_test.py, the words) are handled, but a change to `tools/` or a check's
  helper module is not: run the checks that import it.

## 5. Remaking the coverage map, step by step

Do it when a full round runs (at least every release) and after a big change. It's a separate run that doesn't count:
coverage roughly doubles a check's time, and its results never judge a check.

1. Start from the branch you'll merge, clean (`git status` empty), integration merged in.
2. Run every check once under coverage, one at a time, on a frozen copy (the branch can move meanwhile):
   `bash plans/opt-cover/cov_run.sh /tmp/cov-<build>` (all checks in its `ALL` list, the event days included; about 2 h 15 for the
   28 and ~45 min for the 9 event days). Name checks to run only those. A cover already in the folder is kept, so a stopped run resumes.
   Background jobs stop at 2 hours: run it in two or three pieces, e.g.
   `cov_run.sh /tmp/cov intro day1 interactions fridays player perf`, then the rest.
3. Read `/tmp/cov-<build>/log/_summary.txt`: each check's exit. A check that fails its normal run fails here too
   (perf's +2 geometries, career's known FAIL, tiles): that's fine for the map, which only records lines.
4. Merge the covers into the map, naming the commit whose game they ran on:
   `python3 tools/affected.py --merge tools/check_map.json <commit> /tmp/cov-<build>/*.json`
   (a cover of another game is left out with a message).
5. Copy the covers into `plans/opt-cover/` (they're the map's record).
6. Prove it: `python3 tools/affected_replay.py` (must end "23 of 23 known failures picked", exit 0) and
   `python3 tools/affected_planted.py` (6 of 6). If either misses: fix `RULES` or the map, never the replay.
7. Run the full round normally (3.1), `bash check_fast.sh`, commit with the numbers, push.

A new check: add it to `CHECKS` (command, minutes) and the `RULES` of the sections it covers in tools/affected.py, and
to `ALL` in `plans/opt-cover/cov_run.sh`; until the map is remade it's picked by the rules only. A new section: add its
`RULES` row (until then it runs everything).

## 6. The replay proof, the planted faults and the known failures

### 6.1 The replay (`tools/affected_replay.py`)

`python3 tools/affected_replay.py [--middle] [--last N] [--branch REF] [--map FILE]` (about 2 minutes, CPU only;
needs the whole git history: `git fetch --unshallow`). It does two things:

1. For the last N (20) game commits on claude/integration: the checks the rules alone and (a) would pick (and (b),
   with `--middle`), and their minutes. This is the cost.
2. For each **known failure** (below): was the check that really failed picked, by check_fast, the rules or the map?
   Exits 1 on any miss.

Output for 0.64.12: `plans/opt-cover/replay-0.64.12.txt`.

### 6.2 The known failures (`plans/opt-cover/failures.md`)

Real check failures caught at review or merge, found in the notes, whose causing commit still exists: 14 commits,
23 commit-check pairs. All 23 are picked under (a) and (b); three only by the map.

| Commit | Check(s) that failed | What it was | Picked by |
|---|---|---|---|
| 955b16e | bigevents, social | events base F0b, the calledIn cue | rules |
| 1c4bc67 | mech, events, join | First Light Cocoa (FLC_ON gate) | mech by **the map**; events, join by rules |
| 155f0d4 | intro (--evening) | patch #17, the escort's stop | **the map** |
| ee48072 | intro (--evening) | patch #17, the floor tap: **inherited from 155f0d4** (proved: ee48072 with 155f0d4 undone passes; its only line is a floor tap intro_check never makes); checked against 155f0d4 | **the map** |
| 1f91e90 | interactions | patch #11 trkDoneCheck | rules |
| 2e46584, 32f7710 | career | the rec deck's machines, switched on | rules |
| 22ff1bb | machine, disc | recVisit | check_fast, rules |
| 3a1cc57 | machine | recShutAt reads MACH_HIST | check_fast |
| 9abd51f | day1, events | Maeve's rec lift rides as commute | rules |
| 693e4f4 | leave, mech, interactions, machine | varied mornings | check_fast, rules |
| ec0cbc3 | player, machine | the queues | rules, check_fast |
| 0f34cfb | interactions | devHeadsTick | rules |
| 1d602ff | leave | the turn-in chip's text | check_fast |

Add a row whenever a check catches a real failure at review or merge: the commit and the checks it broke. A commit
that only carried an earlier commit's failure gets "Inherited from <commit>" in its row, with the proof.

**What the known failures prove, and what they don't** (OR2's point): only 3 of the 14 commits are ones where (a)
picks well under all checks (two more pick 23 of 24), so "23 of 23" proves less than it sounds. That's why there are planted faults too.

### 6.3 The planted faults (`tools/affected_planted.py`)

Six one-line faults, each in **one** section, each breaking a check that section's rules **don't** name, so only the
map can pick it. `python3 tools/affected_planted.py` checks the picks on paper (under a minute);
`--run` also runs each fault's check on its faulty copy (about 40 minutes, one at a time) and requires it to FAIL (a fault its check doesn't notice proves nothing).

| Fault | Section | Must pick | Rules alone | The check on the faulty copy |
|---|---|---|---|---|
| an escort to a tile goes nowhere (`escortGoal`) | 10 | intro | miss | 12 new FAILs |
| a typo in the seek chip (`seekEl`) | 20 | intro | miss | TypeError |
| a due tool no longer slows a look step (`workStep`) | 15 | mech | miss | 1 new FAIL |
| a typo in `eventDay` (`fals`) | 18 | career | miss | ReferenceError (on top of its known FAIL) |
| a typo in the health booking (`pls.id`) | 21 | player | miss | ReferenceError |
| your tasting vote isn't kept (`tallyVote`) | 18 | food | miss | 2 new FAILs |

All 6 are picked by (a) and (b), by the map alone. The three crash typos prove coverage (a check catches one only by running its line); the three behaviour faults (escort, tool slow-down, tasting vote) are the stronger evidence that a check notices wrong behaviour (OR2). A fault counts only if its check prints a FAIL or error the game as
it is doesn't, or exits 1 where the game as it is exits 0. Six other faults were tried first and their checks stayed
green (e.g. intro_check doesn't notice the day shift starting an hour late): listed in planted.md as gaps for the
checks' owners.

Results: plans/opt-cover/planted.md.

## 7. The release-candidate procedure

1. **The build master alone pushes to `claude/integration`.** For each reviewed piece of work: merge (never rebase or
   force-push someone else's branch), set the two build lines (the header's `build` and `GAME_BUILD`), add the
   build-table row, run check_fast plus the area's checks (the picker), push, and read GitHub's tick for that exact
   commit. Prepare merges in a separate worktree: `git worktree add --detach /tmp/wt-x origin/claude/integration`.
2. **Build the candidate**: the release's branches merged on top of integration, in the agreed order, e.g. 0.64.12 +
   claude/storm-update 0b77dfc + claude/fridays 3bd9b2c for the storm + Fridays release; the switches set; the words
   baked (`content_gen.py --check`); `node names_check.js`. A candidate can wait on `claude/integration-next`; once
   approved it's fast-forwarded: `git push origin <tip>:claude/integration`.
3. **The sha256 match.** When several runners build the same candidate on their own, each records
   `sha256sum starship-cadet.html`. Matching hashes prove everyone tested the same bytes (the storm + Fridays candidate:
   `23fb9118abc3679fd1eea658a072817fd6f2831a9560f1bf86358ada768cb7df`, CR2 and CR3). The same is done for the
   published page: `git show <commit>:starship-cadet.html | sha256sum` must match the file that's published, and any
   page edits (title, the Dev line) are made by a script that asserts each target string appears exactly once, then a
   `diff` proves nothing else changed.
4. **Split check runners.** The full round shared between runners halves the time (about 45 minutes instead of 1.5
   hours in BM6's round). Each runner: its own session, its own `CADET_WORK`, one browser check at a time, its half of
   the list (e.g. CR2: talk, social, join, lines, lines --day, food 11 4, food 1 7, mech, career; CR3: perf against the
   base, arc, path, tiles, disc, puzzle, deck), its notes file pushed on its own branch (3.4).
5. **Which file wins in merges** (check files clash too):
   - `day_check.py`: storm-update's (it has EV4's 4fa198f storm skip).
   - `perf_check.py`: claude/opt-render's side in both clashes (SCENES and SCENE_JS); it holds everything opt-tests'
     does, plus PR7's noSpot guard. Merge opt-render first, then opt-tests; then check_fast and cadet_test.
   - `food_check.py`: keep **both** changes when food-waits meets line-update (the `fresh()` calls and EV5's
     eventMeetTag line).
   - `mech_check.py` PARTS: keep both (`plans/build-master/union24.py`).
   - `plans/build-table.md`, `plans/backlog.md`: keep both sides; incoming rows under their own heading; clashing
     backlog numbers renumbered.
   - The two build-number lines: the build master's.
   - `plans/build-master/verify_merge.py BASE RESULT FILE C1 C2 ...` checks every helper's added lines are in the
     result and the removed ones gone.
6. **Results**: every FAIL explained as known (2.3) or old (8.3) before the release; the lead tells the user.

## 8. Regressions, browser quirks, old vs new failures

### 8.1 Pixel-identical regressions (cadet_test)

- `python3 cadet_test.py OLD.html NEW.html`, from a scratch folder (screenshots land there). It compares the game's
  state (every key's JSON), 300 paths, 3000 collision probes, crew, taps and about 15 screenshots on Deck 4, in
  SwiftShader (`--use-gl=angle --use-angle=swiftshader`).
- **ALL IDENTICAL** = every state key equal and every shot's largest per-pixel difference at most 1 level. It prints
  `differing px N max M` per shot; max 1 with N > 0 is renderer noise ("ALL IDENTICAL (apart from renderer noise ...)").
  Anything over 1, or a `DIFF` state line, prints `DIFFERENCES FOUND` and exits 1.
- **i_tap1** has ~78 pixels 1 level off along a hull edge, even for changes that touch no 3D. More than 1 level: look again.
- **When it differs**: find out why before moving on (CLAUDE.md). Build copies with one switch on at a time (a `sed` on
  the switch line, in a copy) and compare each against the switches-off build. "g_nocrew 0 px" with other shots
  different means the crew stand elsewhere: when a crew change is expected, compare the crew-hidden shot, or undo the
  crew change in a test copy and expect ALL IDENTICAL. Explain every difference in the build-table row.
- cadet_test hides toasts, the `+N` need notes and the device button's glow, and turns off CSS transitions, because
  they run on real time.
- **Run cadet_test strictly alone**, with no other browser check in the container. With a second browser running beside
  it, the HUD's blurred glass can come out 1 level off in 6-46 pixels (seen twice on 2026-10-22, RV2); alone, the same
  builds are plain ALL IDENTICAL, and a build compared with itself gives zero pixels (lead 27).

### 8.2 Browser quirks

- **The GPU canvas on Deck 7's sign.** A screenshot of Deck 7 at 390x844 showed 2 pixels one level off on the glow of
  the REC DECK sign (`KIT.recBigSign`, a 1024x300 canvas drawn with `shadowBlur`), lap to lap, even in the old build.
  Chromium puts a 2D canvas on the GPU or not depending on what else it holds, and a memory fix changed that. With
  Chromium's `--disable-accelerated-2d-canvas` it's identical: the browser, not the game. Use that flag in a probe (OR2's
  `keep_shots_cpu.py` patches cadet_test's launch arguments in a copy) to tell the two apart; it's not in the checks.
- **Drawing is the cost.** In SwiftShader a drawn frame is about 0.65 s of a 0.72 s step, set by draw calls, not
  pixels. Checks draw the last frame of each step (player_check's polling steps: none). A check that steps
  `window.__step` itself must set `window.__skip` around all but the last frame.
- **gl.finish** returns at once here, so drawing time is billed to the next call; time a frame with a 1-pixel
  `gl.readPixels` after it.
- **Real time**: toasts hide on a 5.6 s `setTimeout`, the tip card and heads-ups on timers, the device's framing eases
  by requestAnimationFrame. A check that reads them must clear or wait for them itself (player_check's phone block;
  tiles_check's backlog 26 was this).
- intro_check's reloads take up to 120 s (`RELOAD_MS`). Background jobs stop at 2 hours. Never `pkill -f` a pattern
  (it matches the shell running it). `*.png` is gitignored: add shots with `git add -f`. perf_check writes
  `perf_check.json` where it runs.

### 8.3 Old vs new failures

When a check fails:
1. **Is it known?** Same message as in 2.3 → known; carry on (say so in your results).
2. **Re-run it on the base** (the build before your change, e.g. `git show origin/claude/integration:starship-cadet.html`)
   with the same check file. Fails the same way there → **old**, not yours: don't fix it on the side.
3. **Old: find where it began.** Run it on older builds (`git log --oneline -- starship-cadet.html`) and halve the
   range: OK at A, FAIL at B. `python3 tools/affected.py A~1 A --why` on each commit in between shows which ones the
   check runs. Confirm with a run of the suspect commit and its parent.
4. **Add a backlog row** (`plans/backlog.md`): the FAIL, where it's OK and where not, the commit, the cause if known,
   who found it; tell the lead. If it's a known-failure candidate for the picker, add it to failures.md.
5. **New (yours)**: fix it before pushing. Never push when check_fast says FAILED. Never change a check to make it
   pass unless the check itself is wrong, and then say so in the commit and get the owner's review.
6. **A flake** (passes on a re-run, same build): say so, run it alone once more, and add a backlog row if it repeats.

GitHub's quick check (`.github/workflows/quick-check.yml`) runs check_fast on every push to a `claude/` branch or main
that touches the game, a check, the words or check_fast; green in about 5 minutes, red in about 30 s; the logs are
the run's "check-logs". A newer push to the same branch cancels the older run.

## 9. Troubleshooting

| Trouble | Do this |
|---|---|
| `game failed to start` / 30 s timeouts | Too many browsers at once: one at a time (two at most, own CADET_WORK each). |
| A check passed in parallel but fails alone (or the reverse) | Two runs shared a CADET_WORK: give each its own (3.3). |
| `QUICK CHECK FAILED (the fast steps ...)` | `python3 content_gen.py starship-cadet.html` then `--check`; or read names_check's two line numbers. |
| cadet_test DIFFERENCES FOUND | Read which shots/keys differ (8.1); flip one switch per copy; crew moves show in all but g_nocrew. |
| A check's time doubled | Coverage or another browser running; a busy machine. Run it alone. |
| The replay says "not in this clone" | `git fetch --unshallow`. |
| The picker lists everything | A section everything reads changed, a section not in `RULES`, cadet_test.py changed, or the game doesn't parse (`--why`). |
| The picker lists nothing for a game change | It never should for the game: check `--why`; a changed line no check ran and a section with a short rule. Run the section's checks by hand and tell TS. |
| A background run stopped | Background jobs stop at their limit (≤ 2 h); a session restart re-runs a running command from the start. Split runs; cov_run.sh resumes. |
| perf_check fails on +2 geometries | Known (backlog 14). |
| intro_check times out on a reload | Normal reloads take 31-32 s; `RELOAD_MS` is 120 s. Run it alone. |

### 9.1 A worked example from 21 October 2026

Two real cases from the day the picker was finished:

**Case 1: tiles_check fails, but not because of anyone's change.** While the coverage map was being made on 0.64.12,
tiles_check exited 1: `FAIL phone 390: opening the board adds nothing to the 3D scene`.
1. Known? Not in the backlog then.
2. Was it the coverage recorder? Ran tiles_check plain on 0.64.12: the same FAIL. So it's real.
3. Old or new? Ran it on 0.64.11 (FAIL, at phone 320) and 0.64.8 (OK, twice). So it began between 0.64.8 and 0.64.11:
   old, not new to anyone's turn that day.
4. Which commits? `affected.py` on each commit 0.64.8..0.64.11 listed the ones whose changed lines tiles_check runs:
   the crew patch T1-T3b, Dev mode D5, Short Fridays 1-8. The section rules alone (23 → tiles) would have named none of
   them, which is exactly what the map is for. CR3, the same evening, bisected it to the crew patch T2 (4dbdca8, the
   opening camera) and found the cause: the check counts while the device's framing still eases on real time.
5. Backlog row 26 (CR3's; TS3 had written the same as a row 24 on its branch, dropped at the merge): the check's timing, not a game bug; nobody fixed it on the side.

**Case 2: a known failure that wasn't what it seemed.** The known-failure list said ee48072 broke intro_check
--evening, and the picker (rules and map) didn't pick intro for it. Before changing the rules to force intro on every
section-11 change (11 more minutes a turn), the claim was tested: ee48072 changes one line, the floor tap, and
intro_check never taps the floor. Ran intro --evening on ee48072 with 155f0d4 undone: OK (283 s); on ee48072 as it was:
FAILED (264 s). Its parent already carried 155f0d4's escort change. So the failure was 155f0d4's, inherited; the row
says so and the replay checks it against 155f0d4, which the map picks. Lesson: prove a failure's cause before
building rules around it.

## 10. Glossary

- **build / game file**: `starship-cadet.html`, the whole game in one file. A build is one version of it (0.64.12).
- **branch**: a line of work in git. `claude/integration` is the shared one; each session works on its own.
- **commit**: one saved change. Its short id (e.g. `155f0d4`) names it.
- **merge**: bringing one branch's changes into another. A **clash** (conflict) is when both changed the same lines.
- **section**: a numbered part of the game file (`// ==== 14. SCHEDULES ====`); `tools/section.py` lists them.
- **check**: a Python script that opens the game in a browser (or works on paper) and tests one area; prints OK or
  FAIL.
- **check_fast**: the 5-minute quick check before every push.
- **the full round**: every check, run alone, one after another (~3 hours with the event days).
- **the picker**: `tools/affected.py`, which lists the checks a change needs.
- **the rules**: the picker's table of which checks to run when a section changes.
- **coverage / the map**: a record of which game lines each check ran, made by `tools/check_cover.py`; the map is all
  of them in `tools/check_map.json`.
- **the replay**: running the picker on past commits to see what it would have picked.
- **known failure**: a real past failure (failures.md) the picker must always pick. Also: a FAIL that's known and
  accepted today (2.3).
- **planted fault**: a small bug put in on purpose (in a throwaway copy) to prove the picker would catch it.
- **regression**: something that used to work and now doesn't.
- **pixel-identical / ALL IDENTICAL**: two builds draw exactly the same pictures (within 1 level of noise).
- **flake**: a check that sometimes fails on the same build, usually from real-time timing.
- **CADET_WORK**: the folder where checks keep three.js and their test copies; one per run at once.
- **SwiftShader**: the software graphics the checks' browser uses (no GPU), so drawing is slow.
- **switch**: a `const X = false` line that keeps a new feature off (`EVENTS_ON`, `SHORT_FRIDAY`).
- **release candidate**: the exact build meant for a release, tested whole before it's published.
- **sha256**: a fingerprint of a file; two files with the same sha256 are the same bytes.
- **backlog**: `plans/backlog.md`, the list of small known bugs.
- **bisect**: halving a range of commits to find the one where something began.
