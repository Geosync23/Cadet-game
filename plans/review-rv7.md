# Reviews by RV7 (Pillar 5 fixes and the guiding arrows; taking over from AR2)

Reviewer RV7 (session_01RLTBGbbdRbUkKME189xL4k), for lead 29 (session_01A9rNreAGVbsY1HgPucDMA7). Branch `claude/review-rv7`
(notes only; the game is never edited here). Earlier verdicts: AR2's `plans/review-fx2.md` (claude/arrows-plan-2) and
RV6's `plans/review-arrows-*.md` (claude/review-arrows). Probes used are in `plans/review-rv7/`.

## 1. AC2 6610dc7 on claude/arrows-c (base d2dade6): PASS WITH FIXES (check lines only)

What it does: (a) 15b `ixBoard`'s `doable` gives a Take it to a registered job kind that isn't a side job (a round, a
haul), exposed as `ixBoard.doable` and used by D's `guideTakeable`; (b) the 14:50 drill arrow is FX2's own line again
(no `trk` tag); (c) S9 says "Works reputation down: <word>" on a drop; (d) FX1's "Nothing on the board" word waits
through a meeting, a training's watch or turn, or a dialogue.

The code is right and small. `doable` keeps the old rule and adds `(chore || registered non-side kind) && jobStepDone`;
`JOB_KINDS` is only read at run time (no load-order problem). `drillGoal`/`drillClose` still clear the drill arrow at
the last stop, at the all-clear and after a day jump, so dropping FX1's `trk` doesn't bring back "the arrow stayed up
for days". S9 marks a word as reached only on the way up (or the word the game loads with), so a word first met by a
drop still gets its "Works reputation: ..." when reached upward later. The board's word isn't marked said while held, so
it comes once the meeting / training / dialogue ends.

| Test | Result |
| --- | --- |
| cadet_test d2dade6 -> 6610dc7, alone | ALL IDENTICAL (no differences to explain) |
| interactions_check on 6610dc7 | INTERACTIONS CHECK OK ("a round on the board": offered, Take it, haul doable, drill not) |
| interactions_check on d2dade6 | crashes with `TypeError: ixBoard.doable is not a function` (counts as a failure, but see fix 3) |
| arrows_d_check on 6610dc7 | OK |
| arrows_d_check on d2dade6 | FAILED on exactly the two new lines (S6 held in a meeting; S9 the drop) |
| Planted faults (9, `plans/review-rv7/mut.py`) | caught: the old `doable` (interactions), `doable` without the side test (interactions), no drop toast (arrows_d), no meeting hold (arrows_d). NOT caught by any check: no dialogue hold, no training watch/turn hold, `guideTakeable` back to its own copy of the old rule, the drill line with FX1's `trk` tag back (arrows_d and mech_check m3d both OK), S9's old "seen" marking |
| "Trained: rounds" toasts | once, in every week run (arrows off and on; toasts logged only when they reach the screen) |
| Other kinds the new rule opens | incident, leak, nozzle, tracedemo (tune and rewire have a machine, so already had a Take it). None was on the player's board Days 2-8 in any run |

**arrows_check week** (the follower: goes where the arrow points, taps what it names):

| Build | Arrows off | Arrows on |
| --- | --- | --- |
| d2dade6 (base) | learned: m3d, m2 only. Rounds never learned (stuck at "Take your first round at the job board", the board's "coming soon") | the same |
| 6610dc7 | m1 (Day 3, not Day 2: the follower took "Clean a vent: laundry" at 11:20 Day 2 and stuck there), m3d, m2 | m1 on Day 2, m3d, m2 |
| 6610dc7 + FX3's 2cdc1df (fix 14 cherry-picked; a full merge of p5-fix3 conflicts in the burst pipe lines) | m1 Day 3, m3d, m2: still stuck at the laundry, because the follower calls `playerTap` directly (no screen tap, so fix 14's ray test can't see it) | m1 Day 2, m3d, m2 |
| the same, my follower with a real screen tap at every chore pin (`arrows_check_rt.diff`) | m1 Day 2, m3d, m2; the haul lesson's run taken from the board (19:21 Day 3), then stuck on its stops | the same |

So in no combination are Hauling (m4), the inspection (m3i), Tuning (m5), the scanner (m7) or p3 learned on Days 2-8
by following the arrows. What's in AC2's diff is the step that lets the round (and the haul's turn) be taken at all:
"Take your first round at the job board" (red on base, Days 2, 3 and 8) is gone, and Rounds is learned. The rest is
outside this commit:

- **The laundry stop's pin over Washer 1:** FX3's fix 14 (real taps). The arrows_check follower doesn't make real taps
  there, so its week stays red at the laundry until the follower does (or the stop moves off the washer).
- **The haul's cart stop (new to the player now that hauls can be taken):** the pin is on the floor beside Cart dock 1.
  Tapping the dock itself says "Cart dock 1: in good order." and starts nothing (a restock's cart does start from the
  dock tap, via cartTap). A floor tap at the pin works (`p_cart.py`, both builds). The same trap as the laundry; FX3's
  area (Hauling).
- **With real taps, the haul and delivery drops stick:** "Crew store stock to the crew store, Deck 3", "Linen to the
  laundry, Deck 4", "Pick up a crate of linen", "Take medical supplies to the infirmary, Deck 3". Not traced further.
- **The haul lesson's run is taken late** (19:21 on Day 3 in my runs, after the shift): the follower is busy with other
  board jobs all afternoon; the training's turn isn't put first on the board for it.

Fixes (checks only, no game change):
1. Lines for what's untested: the board's word held during a dialogue and during a training's watch and turn;
   `guideTakeable` with only a round (or a haul) on the board gives "Take a job at the board"; the drill arrow is
   still up after you reach the Works bay at 14:55 (the reason the `trk` tag came out); a word first met by a drop
   is said ("Works reputation: ...") when it's later reached going up.
2. arrows_d_check's header says a drop shows "the pointer to the Works app's Training tab"; the code (rightly) only
   toasts on a drop. Fix the words.
3. interactions_check's new part: guard `ixBoard.doable` with `typeof` so an older build prints a FAIL line, not a
   crash that stops the rest of the check.

For the lead (not AC2's): is it wanted that incidents, leaks, nozzles and the trace demo also get a Take it when one
is on your board? The rule allows it; none showed up in the week.

## 2. FX3 2cdc1df on claude/p5-fix3 (fix 14, on 8aae063 which AR2 passed): PASS

What it does: `choreRayTap` in 15's `playerTap`, after `jobTap`: if you hold a chore (`ixChore`, which includes the
registered kinds), the tap landed on a machine (real or stand-in) and the tap's line passes within `JOB_RAY` (0.6 m)
of your chore's next stop, the stop starts there (`ixChoreTap` at the stop's spot). The linen drop and the laundry vent
stop (4-laundry-1) stand by Washer 1, which took the tap before. `stubTap` only looks a stand-in up (no side effect).

| Test | Result |
| --- | --- |
| interactions_check on 8aae063 | FAILED on the new line only: the camera turn with Washer 2 under the pin starts nothing (linen and vent) |
| interactions_check on 2cdc1df | INTERACTIONS CHECK OK: all 8 taps (2 chores x 4 camera turns) start the stop |
| cadet_test 8aae063 -> 2cdc1df, alone | ALL IDENTICAL (renderer noise only: up to 46 px one level off) |
| clothes_check, player_check on 2cdc1df | ALL OK, PLAYER CHECK OK |
| Planted: no ray test (any machine tap does the stop) | caught ("a lamp chore in the laundry: Washer 1 does its own thing") |
| Planted: no machine test (any tap on the line to the pin) | not caught (small: worth one line, e.g. the hamper or a seat on the line still does its own thing) |

Notes: (1) the arrows_check follower calls `playerTap` directly with no screen tap, so this fix can't help its week
(it stays stuck at the laundry); a real tap does work (my follower variant). (2) The same trap is now on the haul's cart
stop (pin beside Cart dock 1: a tap on the dock says "in good order"), see item 1. `choreRayTap` helps only when the
tap's line passes within 0.6 m of the pin.

## 3. claude/arrows-c 69d1ed9 + 78fef90 (AC2: the FX3 merge, the tea arrow, my 6610dc7 fixes, follower changes): PASS

In it: 00f4436 merges p5-fix3 2cdc1df (FX3 fixes 10-14); 695cf6e the tea arrow carries FX1's trk window (gone when tea's
over, 14:00, or once you reach the Tea corner); 78fef90 the board's Take it only for rounds and hauls (`BOARD_KINDS`,
lead 29) and the check lines I asked for; c26f194 / 7ff2c27 / 69d1ed9 the arrows_check follower only (a job held for
you first at the board; a tap that answers but starts nothing, or starts a sit-down or laundry, is followed by a real
tap at the pin; up from a sit-down once its minutes are in).

The merge's one clash (the burst pipe) keeps both sides: AC1's F4 queue entries and `incGoalNow`, FX3's `incPark` and
its WORK_TICKS, `incWho` "Calder" with the queue off too, and FX1's trk window on the call's arrow.

| Test | Result |
| --- | --- |
| cadet_test 6610dc7 -> 69d1ed9, alone | differs in e_night ... i_tap3 only (up to 12k px): the other-deck arrow's words, "Take the lift to Deck 3: food, Deck 3" -> "Tap the lift: Deck 3 · Food" (FX3's fix 10, passed by AR2). Same place, same arrow. Intended |
| cadet_test 69d1ed9 -> 78fef90, alone | ALL IDENTICAL |
| player_check on 695cf6e~1 | FAILED on "tea not taken: the arrow goes when tea is over" only |
| player_check on 69d1ed9 | PLAYER CHECK OK |
| Planted: tea's trkTo a day late | caught (player_check) |
| interactions_check on 69d1ed9 | OK |
| arrows_d_check on 78fef90 | OK |
| My planted faults on 78fef90: no dialogue hold, no training hold, the drill trk tag back, S9's old seen marking, guideTakeable's old rule (arrows_d); any non-side kind takeable (interactions) | all 6 caught |
| Week (`p_week.py`, 78fef90's own follower), arrows off | learned m1 Day 2, m3d and m4 Day 3, m5 Day 4, m2 Day 8. Not: m3i, m7, p3, m6. "Trained" toasts once each |
| the same, arrows on | m1 Day 2, m3d and m4 Day 3, m5 Day 4. **No "Trained: ..." toast reached the screen at all** (see A) |

A. **The pop-up queue drops "Trained: ..." (arrows on; piece B, AR1's design, not this commit).** At most 3 wait; the
oldest waiting is dropped. At 11:00 on Day 2 six arrive at once (Round done, Zeke's line, "That's a round", Work done,
Trained: rounds, Job complete) and "Trained: rounds" is pushed out before its turn (`p_toast.py`). Earlier runs showed
it only by luck of timing. Suggest: a training's toast is never dropped ({ now: true }, or the queue drops the least
important first, or merges a job's own run of toasts).
B. **Day 5 lost to the climbing wall (the follower):** it taps the Climbing wall nearest the holds' pin and climbs all
day (recClimb isn't one of the sit-downs 69d1ed9 ends), so the scanner meeting is missed (m7 meet -> ask). A player
tapping the floor at the pin gets the job (FX3 fix 8/12). Follower fix: end any activity that isn't the job's stop.
C. **"Put the seal back: main storage" up from Day 6 05:50 over the weekend** (seals left in hand from the abandoned
holds job; FX3's put-back arrow, fix 9). Over 3 hours on a day off. FX3's call whether it should wait for a workday.
D. Still stuck once: "Linen to the laundry, Deck 4" (a haul drop; with FX3). The inspection (m3i) isn't reached on
Day 4 (the arrows plan's Day 4 warning).
E. A real rewire job has a machine, so it gets a Take it through the old machine rule (as before 6610dc7; tier 2). The
interactions line tests `{ kind: 'rewire' }` without a machine, so it doesn't prove "never a rewire". Lead 29's call.

## 4. claude/arrows-c 86faa86 + 5160b81: the game change PASS; the follower change FIXES NEEDED

86faa86 (game): 15b `ixJobStep` returns null once you've clocked out today, so there's no job arrow (steps, Turn it in,
Take a job) after clock-out; a job you hold stays in Tracked; a put-back part keeps its arrow.

| Test | Result |
| --- | --- |
| cadet_test 78fef90 -> 86faa86, alone | ALL IDENTICAL |
| arrows_d_check on 86faa86 | OK; my planted fault (clocked out "tomorrow" instead of today) caught ("after clock-out: no job arrow") |
| Week with 78fef90's follower on 86faa86's game, off / on | the same as 78fef90 (m1, m3d, m4, m5 learned; m2 off) |

86faa86 + 5160b81 (follower): a real floor tap at the pin whenever the arrow is your job's own step (5160b81: not
when the goal names an item, i.e. the board). With it the week collapses:

| Follower | Arrows off | Arrows on |
| --- | --- | --- |
| 86faa86 | stuck at "Clock in at the time clock" every workday from Day 2 08:04: never clocks in; only m3d learned | stuck at "Turn it in at the job board" every day; only m3d |
| 5160b81 | the same: stuck at Clock in (the clock's goal has a place, no item) | stuck at "Turn it in at the job board" from Day 2 10:50; nothing learned |

A floor tap at the clock's or the board's pin opens neither. Fix: keep the real tap for a job's own stop (a chore's
stop, a machine's spot) and tap the clock and the board by name, or tap the thing first and the floor only when nothing
started (78fef90's order already does that).

## 5. FX3 claude/p5-fix3 410954b, c3d246f, cc61962 (fixes 16-18): PASS

16 (410954b): `choreRayTap` back to fix 14's ray test (FB1's choreThingTap on claude/fe-cartdock handles haul stops).
17 (c3d246f): on an inspection morning, 06:00-06:30, a direct arrow through your berth: wardrobe (fresh uniform), bunk
(make the bed), locker, then "Inspection at 06:30: your berth" if you've left it; never over another arrow; off with
GUIDE_ON (the queue's F2 is AC2's). 18 (cc61962): with your job on the climbing holds, a tap on the Climbing wall in
its room starts the job (`JOB_THING`), not a climb; it ends in the same `actStart('job', ...)` as the machine path.

| Test | Result |
| --- | --- |
| cadet_test 3b7b13db -> 410954b, alone | ALL IDENTICAL |
| cadet_test 440730f -> cc61962, alone | ALL IDENTICAL |
| mech_check fx3 on 440730f | FAILED on the new inspection-arrows line only |
| mech_check fx3 on cc61962 | MECH CHECK OK |
| interactions_check on c3d246f | FAILED on the new climbing-wall line only (a climb started) |
| interactions_check on cc61962 | OK |
| Planted: over another arrow; steps out of order | both caught |
| Planted: the arrow also with GUIDE_ON (no stepping aside) | not caught (one line worth adding) |

Note: with the arrows queue on, nobody shows the inspection arrows until AC2 wires `inspectGoal` into the queue (F2).
The earlier optional line (a non-machine thing on the pin's line keeps its own tap) is still optional.

## 6. claude/arrows-c 483c3da..14249d8 (AC2: the pop-up queue keeps a training's word; F2; the follower): PASS

483c3da: when the pop-up queue (arrows on) is full, the oldest waiting pop-up that isn't a "Trained: ..." or "Works
reputation" word is dropped (`TQ_KEEP`). If every waiting pop-up is one of these, none is dropped (a few, no harm).
5f7e91c (F2): from 06:00 to 06:30 on an inspection morning, `guideShift` asks the queue for FX3's `inspectGoal` at level 2.
This happens before the shift's clock-in returns, so it works before you clock in. The other commits in the range are
the follower and docs, and merges RV8 passed. The game is the same at 5f7e91c and 14249d8.

| Test | Result |
| --- | --- |
| cadet_test 483c3da^ -> 483c3da, and 5f7e91c^ -> 5f7e91c, alone | ALL IDENTICAL, both |
| arrows_d_check on 14249d8 | OK |
| Planted: the queue drops the oldest again; F2 at level 5; F2 off | all caught |
| Planted: the queue drops the newest instead of the oldest non-keeper | not caught (minor) |
| Week (14249d8's own follower), arrows off | learned m1 (Day 2), m4 and m3d (Day 3), m3i and m5 (Day 4), m2. Not: m7, p3, m6 |
| Week, arrows on | learned m1, m4, m3d, m3i, m5, **m7 (Day 5)**, m2. Not: p3 (FX5's fix, RV9), m6 (stuck at "Mop up (2 of 2)", Day 8: FX3's mop fix) |
| "Trained: ..." pop-ups | every training said once and reached the screen, arrows off and on (7 with the arrows on) |

Still stuck: "Clean a vent: hydroponics garden" Day 4 (both runs; FX3's vent fix) and "Clean a vent: lift plaza" Day 8 (arrows off).
With the arrows off, m7 isn't learned on Day 5 (FX4's m7 fix, RV9).

## 7. claude/arrows-c 8dd03049 (AC3; arrows_check follower only): PASS

Two follower lines: (1) while a `career:` arrow is up (Calder's call, a summons, the test, a move, a ceremony) the
follower ends what it's working on and goes; (2) in a training meeting's room while the meeting is on, it waits for it
to start. The game file at 8dd03049 is 14249d8 plus FX5's p3 fix (RV9's). Week on 8dd03049:

| Arrows | Learned | Stuck |
| --- | --- | --- |
| off | m1, m4, m3d, m3i, m5, m2 (6 "Trained" pop-ups) | the hydroponics vent (Day 4), the lift plaza vent (Day 8) |
| on | m1, m4, m3d, m3i, m5, m7, p3 (Day 5 11:02, FX5), m2 (8 "Trained" pop-ups) | the hydroponics vent, "Mop up (2 of 2)" (Day 8) |

Nothing got worse. What these lines are for (Day 8's m6 at "ask" with the arrows off) can't show yet: with the arrows
off the scanner isn't learned on Day 5 (FX4's fix), so Making it safe doesn't open on Day 8.

## 8. The shipped default (teaching arrows on in 0.92.0): a week before AC3's switch commit

A copy of arrows-c 8dd03049 with `POINT_ON = true` and `GUIDE_ON = true` at load (no run-time overrides),
`plans/review-rv7/p_audit.py` (the week, logging every arrow's source and level), `p_ptr.py` (the panel pointer).

| Teaching arrows | Learned | Stuck |
| --- | --- | --- |
| First times (the default) | m1, m4, m3d, m3i, m5, m7, p3, m2 | "Mop up (2 of 2)" Day 8 (m6; FX3), the hydroponics vent Day 4 |
| Off | m1, m3d, m3i, m2 only | the hydroponics vent |

With Off, the queue drops T2 ("Stay close and watch <teacher>", level 3). `trainWatchArrow` (the old direct watch
arrow) runs only with the queue off, so a lesson's watch step has no arrow at all, and Hauling, Tuning, the scanner and
p3 are lost. That fails lead 30's rule (Off removes only what exists to teach, never the arrow the game had before).
Under Off these stay, which is right by that rule: the job arrows, the shift chain (Take a job, Shift over), the meeting
arrows (L2), the inspection (L2) and the drill. The panel pointer is off under Off: at 08:01 on Day 2 "First times"
asks p:clock:in, and Off asks nothing.

## 9. claude/arrows-c e3c7c183 + 764438d4 + f8ed8521 (AC3: the teaching arrows switched on; Off keeps the watch arrow): PASS

e3c7c183: `POINT_ON = true`, `GUIDE_ON = true`, Settings shows Teaching arrows (default First times), design-doc;
the arrow checks make their own switched-off copy for their "off" parts. 764438d4: device_check empties the pop-up
queue before reading a toast. f8ed8521: `guideTeach` skips an entry marked `everyday` (T2's watch arrow), so Off
keeps it; T2's first-time tip stays hidden under Off.

| Test | Result |
| --- | --- |
| cadet_test c14a799d (before the switch) -> f8ed8521, alone | ALL IDENTICAL (its shots are Day 1, where the intro's own arrows run and the queue adds nothing) |
| arrows_d, arrows_f, arrows_pointer on f8ed8521 | OK, all three |
| Week, the build as shipped (no run-time overrides), First times | m1 Day 2, m4 and m3d Day 3, m3i and m5 Day 4, m7 and p3 Day 5, m2; 8 "Trained" pop-ups shown. Not m6 |
| Week, Teaching arrows Off | the same lessons on the same days; the watch arrows ("Stay close and watch ...") show |
| Panel pointer, 08:01 Day 2 | First times: p:clock:in asked; Off: none |

Under Off, what still shows (all things the game had before, or not teaching): job arrows, the shift chain, meeting
arrows, the watch arrows, the inspection, the drill, Calder's call. What goes: the panel pointers and the first-time
tips. Still stuck in both: "Mop up (2 of 2)" (Day 8, m6) and the hydroponics vent (Day 4), FX3's fix 19.
Note: urgent device notifications now wait their turn in the pop-up queue (a second or two), like every other pop-up.

## 10. FX3 fix 19, claude/p5-fix3 518ee9ef (on arrows-c 14249d84): PASS

Section 11's tap: when someone is near the tap on screen and the tap is on the arrow's pin (`IX_PIN`, within 22 px) or
beside them (more than 10 px from their body points), and the floor under it is your job's stop (`jobSpotTap`), the
job; else `tapCrew` as before. Calder by the second puddle (Day 8) and a crew member at the garden vent took every pin
tap as a chat.

| Test | Result |
| --- | --- |
| cadet_test 14249d84 -> 518ee9ef, alone | ALL IDENTICAL |
| interactions_check --quick on 14249d84 | FAILED on the new line only (0 of 4 taps at the pin mop the puddle) |
| interactions_check --quick on 518ee9ef | OK (4 of 4; a tap on someone away from it is still a chat) |
| Planted: pin taps ignored | caught |
| Planted: "on the person" widened to 40 px | not caught (minor: only matters for a tap near your stop, off the pin) |
| Week on 518ee9ef, arrows off | nothing stuck, no arrow over 3 hours (m7 on Day 8: FX4's fix isn't in this base) |
| Week on 518ee9ef, arrows on | nothing stuck; m6 learned on Day 8 11:08 (p3: FX5's fix isn't in this base) |

Trade-off to know: with a job in hand, a tap near someone standing close to your stop (but not right on their body)
now goes to the job, not a chat.

FX3 adda4fe5 (test only): interactions_check also taps the floor beside someone at the puddle, off the pin, and
expects the mop. OK on 518ee9ef; it catches the 40 px fault (19 px from Oona: nothing started). Both planted faults caught.

## 11. The check-side fixes since the switch (lead 31's question): none hides a game problem

- intro_check 34da38fc (the pilot's ramp line): `p_ramp.py` plays the arrival in real time (sign, then 35 s) on
  arrows-c 8ab6089 with the arrows on and on a copy with them off. The pilot's line is the only pop-up both ways, and
  it stays its full time. The 2.5 s happens only inside intro_check: 150 frames in well under a second of real time,
  while the queue counts real time.
- intro_check 7989742a: a training meeting has the arrow from 15 minutes before (the queue's T1, level 2, by design).
- interactions_check fdd15400: test setup only (a fresh game has no career yet).
- controller_check (controller-tests-3): with arrows on, B puts away one waiting pop-up per press (up to four in a
  burst), where one press used to clear the one on screen. A small UX change, not a fault.

## 12. 0.92.0, claude/integration-next-fe1 4147f03d (BM14's merge, arrows-c last): PASS WITH FIXES (one check)

Game sha256 c2180854...4f1286, matches lead 31's. Only the arrows-c merge (b657a4e) had game clashes, four, each
resolved keeping both sides: Settings (the Teaching arrows row, then the controller's padSetBlocks), section 19's slot
(the panel pointer, then tip-clear's tipClear), jobEnd's repair finish (caseFitted first, then finishJob with padBuzz),
ixPinBooth/IX_PIN (arrows-c's, new). The other eight merges had none in the game. FX7's floor-tap fix and FX3's fix 19
auto-merged in separate code. controller_check taken whole from CTT3: the base's copy equals 2a76b818, which CTT3's
branch contains, so nothing is lost.

| Test | Result |
| --- | --- |
| cadet_test 362d0ff (just before arrows-c) -> 4147f03d, alone | ALL IDENTICAL: arrows-c adds nothing to its shots |
| cadet_test arrows-c 7d97d538 -> 4147f03d, alone | differs from a_start on, whole screen from i_tap1: the other pieces' changes (meals and hygiene); the player heads for "A toilet" where arrows-c's went for food. arrows-c itself adds nothing (the line above) |
| arrows_d, arrows_f, arrows_pointer on 4147f03d | OK, all three |
| Week, the build as shipped, First times | all nine learned: m1 Day 2; m4, m3d Day 3; m3i, m5 Day 4; m7, p3 Day 5; m6, m2 Day 8. Nothing stuck, no arrow over 3 hours, 9 "Trained" pop-ups, no page errors |
| Week, Teaching arrows Off | the same, lesson for lesson |
| Panel pointer | First times: p:clock:in asked; Off: none |
| mech_check (all) on 4147f03d | **FAIL** in part fx3, then a crash: "m6: after the talk the arrow follows the teacher to the pipe (None)", then `a['goal'][2]` on None |
| mech_check fx3 on arrows-c 7d97d538 | the same FAIL and crash: not from the merge, from the switch (arrows on by default) |

The fix needed (AC3 / FX3): mech_check's fx3 part was written for the arrows off; with the queue on, the burst pipe's
follow arrow is a queue entry (F4, level 1), not a direct goal, and in the check's Day 8 scenario m6 goes back to "ask"
after the talk. Play shows m6 learned on Day 8 with the arrows on and with Off, so it is most likely the check (it
reads IX_GOAL; and its scenario may lean on the direct arrow). That has to be shown, and the part made to pass
with the shipped switches, before the round can be green.
