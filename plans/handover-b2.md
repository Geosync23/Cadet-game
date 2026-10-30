# Handover: B2 (mechanics seat A, Pillar 5 Step 5)

- **Role:** mechanics seat A builder, hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi); now reporting to **lead 40** (session_01NXybH7NNqM8M4ngiyidq6m). My session: session_015mjNkxuGoEZGKA2ksBPz9u. Reviewer: **RV20** (session_01PyJwfvfQVu4oXTYDMGkacw; notes in plans/review-rv20.md on claude/review-rv20).
- **Spec:** `plans/p5-step5-spec.html` on claude/p5-specs (EP2; slots updated in 90e72a2d, the ladder order in 79c4d275).
- **Branches:**
  - `claude/p5s5-mech-a` 5c745377: S5-3 (M19) turns 1-2 and RV20's fixes, on B1's skeleton 5957d244, merged with the fix below (so it now carries claude/staging-0.93.3 acbb52e0).
  - `claude/workstep-tap-fix` c79a66dc: a live fix for today's game (from claude/staging-0.93.3 acbb52e0, not behind a switch). Rewiring's steps by tap.
- **Build-table rows:** `0.93.4-m.1`, `0.93.4-m.2`, `workstep-tap-fix`. The build-number lines are untouched.

## What I built

### S5-3, M19 power and relays (section 24v, behind `P5_M19`)
- **The lesson.** `WORK_MECH.m19`: Day 17 at 11:00 (`at`) in the bridge's relay room (Deck 1, u).
  - Calder swaps the relay on 1-relay-1 while you watch; then 1-relay-2 is yours (look, pull, seat, test).
  - Its jobs use their own job slot, `PWR_SLOT` 32.
- **The beats** (`pwrBeats`): an urgent notice at 10:30 (24p's `promoNotice`), then a level-1 `guideAsk` (`m19:meet:<day>`) from 10:45 with the ring line "Power and relays with Calder, 11:00".
  - Said in person (`pwrAskSay`): if you're near Calder after the ask, she tells you herself.
  - Calder's appointment (`pwrHost`): booked at the rack's panel, 5 minutes before the lesson. The relay room has no non-machine place, so section 18's occasionAdd booked none and she only arrived at 11:17.
- **The tester.** It comes through the row's tool (24 core's worksTrained, so never twice). Calder's `train.m19.tester` line plays only when the tester is new (onSim 'tool').
- **Rewiring folds in.** M15 Rewiring folds into M19 (EP2's ladder order): onSim 'trained' sets `W.tr.m15` and counts m15 as opened. B1 builds the ladderTick rule in 24 core.
- **Job kinds** (Tier 3, all side kinds like rewiring; each carries `j.machine` and is stepped by tap through 15b's `ixStepwise`):
  - `relayswap`: read the lamps, pick the failing relay of R1-R6, swap, test.
  - `battcell`: read the bars, pick the low pair of cells (one of 4), swap, check.
  - `conduitrun`: stage 2. At a crawlway conduit's inspection box under Deck 6, the tester reads its three feeds, you pick the low one and tag it. Sends `simNote('conduitRun', { machine, deck })` for S5-6's P5.
  - A wrong pick reopens that stop (veto); it's never a fail.
- **The weekly job:** one a week from the week after the lesson, 08:00 on a workday of yours, never rewiring's day (`pwrDay`). The kinds rotate (`pwrKindOf`): relay swap and battery check, plus the conduit run from stage 2 if you have the tester. Not taken: the crew get it the next day.
- **Uses** count from these jobs turned in by you, and from any repair of yours on a relay or battery machine. Stages: 3 uses and 6 uses, as the row says; stage 3 is Step 6's P6.
- **The Senior Officer's drill** (`pwrdrill`, a side job; 24c's drill is untouched and stays the juniors'):
  - Wednesdays at 14:50 once you're trained in M19, at the Works bay's muster hatch.
  - Three calls on pick cards: muster, the week's action, report to the bridge. The crew answer each call; a wrong call reopens the card.
  - A level-1 arrow with the ring line "Run the Works part of the drill". The all-clear at 15:15 ends it whatever the state.
- **The power line and its faults** (lead 39's addition; section 17's data shapes, added from 24v at load, only with P5_M19):
  - `MACHINE_LINKS.power`: the four battery banks side by side, then 5-inverter-1, then the conduits as branches (6-conduit-1 feeds Decks 1-3, 6-conduit-2 feeds Decks 4-6).
  - `LINE_ENDS.power`: each deck's junction after its conduit.
  - `SYMPTOM_TEXT.power`, and `FAULT_CAUSES` for battery, inverter, conduit and junction (powerjunction shares junction's table).
  - B4 agreed the names. Section 17's `traceFor` gets one line: the power line is never traced with the pipe kit.
- **Save:** `SHIP.works.side.pwr` = `{ done, wrongs, week }`, cleaned on read (`pwrState`).
- **Random-choice keys:** 1060-1064 for M19 (1060-1064 in use). **1065-1069 are reserved for M20.**
- **Words:**
  - SW3 wrote turn 1's words to match my keys (claude/p5s5-words 277b9c15; content/works/m19.lines, meeting train.m19.calder, Calder's train.m19.tester).
  - I wrote turn 2's words myself (lead 39's call; SW3's session ended) in `content/works/m19-runs.lines`, baked; lines_check PASS. RV20 reads them.
  - Until SW3's branch merges, the stand-in meeting `train.m19.calder` is made in 24v (marked stub).

### claude/workstep-tap-fix (RV20's M3; also a live bug in M15 Rewiring)
- **The bug:** a registered job kind on a machine, with stops other than the panel's single `'job'` stop, was played as section 15's plain timed repair.
  - Section 15's `jobTap` took the tap at the machine, and `jobBegin` found no `'job'` stop.
  - 15b's `ixChore` left out any job with `j.machine`, so the stop-by-stop path never saw it.
- **The fix:**
  - 15b's new `ixStepwise(j)` lets `ixChore` take such a job.
  - One guard line at the top of section 15's `jobTap` returns false for it. The player engineer should look at that line.
  - Tuning (a single 'job' stop with a turn) keeps jobBegin's path.
- **The check:** mech_check part `wstap` (runs with m15, m19 or wstap). It taps a rewiring job at its machine at 390x844 through `playerTap` (not `ixTap`, which is only one of the `PLAYER_TAPS` handlers), and every stop plays. It FAILS on the build before the fix. On mech-a, `JOB_TAP_EXTRA['relayswap']` adds a relay swap.

### Checks added
- `mech_check.py`:
  - Part m19 (`part_m19` + `part_m19b`): the beats, the tester, Rewiring folding in, the weekly jobs, the picks, uses and stages, the crew's fallback, the save, the line and faults, conduit runs, the drill, none for an Officer.
  - Part wstap.
  - m9's traced-share count now counts only line machines at your tier.
- `controller_check.py`: part `m19` (a relay swap, a battery check and a conduit run by pad, each with a wrong pick). `P5_PARTS` / `p5_on` / `p5_copy`: the part says "not yet" while P5_STEP5 is off; `CTL_P5S5=1` runs it on a copy with the switch on.

## Tests (last)
- **mech-a 5c745377:**
  - Switch off: cadet_test ALL IDENTICAL against workstep-tap-fix's build; check_fast OK (416 s).
  - Switch on (a copy): mech_check m19, m15 and wstap OK, except m19's "asked on Day 17" and "notice at 10:30" lines. **Those FAIL until B1's ladder order is merged:** without it, Rewiring's lesson opens first.
  - On 9f49eda0: full mech_check and machine_check OK; controller_check m19 OK (CTL_P5S5=1).
- **workstep-tap-fix c79a66dc:** check_fast OK; cadet_test against acbb52e0 ALL IDENTICAL (renderer noise only); mech_check m15, m5 and wstap OK. interactions_check was still running when I wrote this (no FAIL so far); see my message to lead 40.

## Loose ends
- RV20's re-review of 5c745377 and c79a66dc is pending; I stand by for its fixes only.
- B1's ladder order is merged (claude/p5s5-career 51b1a9c6): mech_check m19 passes in full on a switch-on copy, the Day 17 11:00 ask and the 10:30 notice included. 24v's own Rewiring fold-in hook is removed (24u's does it).
- RV20's S2 (a stale team-job arrow over the lesson's step) is not touched: it looks older than Step 5.
- The Calendar's Wednesday drill line still shows the juniors' drill for a Senior (24c's drillDue only knows juniors).

## For B3: S5-5, M20 the sensor array (section 24x, `P5_M20`)
- **The spec (S5-5):** Friday Day 19, 10:00-12:00. Hana Mori with Calder in Deck 2's array room (room A: 2-array-1, plus racks 2-racks-1 and -2).
  - You're given the calibration rig: the row already has `tool: 'arrayrig'`, so worksTrained gives it.
  - A "Pick the star" card: Mori names three stars, you pick one. You calibrate against it with tuning's dial (a `turn` stop, as 24e's `tuneStops`; already pad-ready). Then you replace a failing module.
  - Stages: one sensor; a full sweep; readings that feed Survey (a friendship moment with Mori). If you logged that star (24t, the star logger), a line says so.
  - Save `SHIP.works.ar` = `{ star, sweeps, day }`, read back from the save yourself (worksClean keeps only 24 core's fields).
- **Fixed for you:** job slot **34** (spec 90e72a2d). Random-choice keys **1065-1069** (lead 39 OK'd). The row: `by: ['mori', 'calder']`, stages at 0, 2 and 4 uses, `tool: 'arrayrig'`.
- **The beats:** the ring line "The sensor array with Hana Mori, 10:00", a level-1 arrow to the array room from 09:45, a notice at 09:30, said in person before any Mail. Copy `pwrBeats` and `pwrAskSay` in 24v. `WORK_MECH.m20.at = () => 600`.
- **Gotchas I hit, all relevant to M20:**
  1. **The teacher won't come.** Room A has only machine places (2-works-7, -8, -9), so occasionAdd books no appointment and Mori never walks there. Either the deck architect adds two places in a `// P5 places block` for Deck 2 (the spec's plan: Mori at the rack, you at the array panel; check with deck_check), or book her appointment yourself at a panel place, as `pwrHost` does. Prove it with RV20's live probe (plans/rv20-m19-live.py on claude/review-rv20).
  2. **Jobs on a machine need stop tags other than `'job'`,** so 15b's `ixStepwise` steps them by tap (needs workstep-tap-fix, already in mech-a). A single `'job'` stop goes through jobBegin like tuning, which is right for a pure dial.
  3. **Two teachers.** ladderTeacher picks the first on shift from `by`. For "Mori with Calder", have Calder say her one line by `worksSay` or `worksTeach` (M19 shows the pattern).
  4. **Watch the ladder.** One big lesson a day. m20 is Day 19, the same Friday as the booked shutdown after lunch (S5-4). The training must end by 12:00.
  5. **Tests:** use `playerTap`, not `ixTap`, to tap things. The mech_check TRAIN frame answers stops with no result, so give the training job no pick, or answer it in your part, as `rewRight` does for rewiring.
  6. **Text placeholders:** lines_check accepts only its fixed list (`lines_check.py` PLACEHOLDERS: name, time, where, text, n, deck, star, word, place ...). {star} exists.
  7. **The 2-racks machines are kind 'relay'.** M19's weekly relay swap may land on them. Harmless, but don't be surprised.
- **Checks for M20:**
  - mech_check part m20 (add `PARTS['m20']`; copy part_m19's shape).
  - controller_check: add `'m20'` to `P5_PARTS`, `PART_FN` and `NEEDS` (as m19). Pick the rack and the card; reach "Pick the star".
  - deck_check (Deck 2), machine_check.
  - `JOB_TAP_EXTRA['<your kind>']` in mech_check's wstap.

## How to test
- **Setup:** `pip install playwright numpy pillow`; three r128 and acorn into /tmp/cadet-work (testing-guide section 2); `CADET_CHROME=/opt/pw-browsers/chromium`.
- **Switch-on copy:** `sed "s/const P5_STEP5 = URL_FLAGS.has('p5s5');/const P5_STEP5 = true;/" starship-cadet.html > on.html`, then `python3 mech_check.py on.html m19 wstap`.
- **Controller:** `CTL_P5S5=1 python3 controller_check.py starship-cadet.html m19`.
- **Load:** give parallel runs their own CADET_WORK. interactions_check takes over 30 minutes, so give it a long timeout.
