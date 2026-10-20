# Owner stand-in reviews (OR1)

OR1 took over owner stand-in reviews from DR1 (handover on claude/devmode-review-1). Reports to lead 21.

## 1. PA, claude/patch-a eb638e7: batch B and C hooks (2026-10-20)

**Verdict: PASS** (one optional suggestion, below).

Tests on eb638e7: cadet_test integration (5d6ee1c) vs patch-a, run alone: **ALL IDENTICAL**, no errors. check_fast run alone: **QUICK CHECK OK in 213 s**.

| Commit | Section | What it does | Owner check |
|---|---|---|---|
| 651a78f | page CSS | `.devbtn.devglow` pulse, `#devPoint` | CSS only; used only by section 21's `introDevGlowTick` (intro on). No meshes, no draw calls. |
| 279a091 | 22 | `linesHush` also asks `introHush()` | `typeof` guarded, called at run time only. `INTRO_UI` is a load-time const; `night`/`hushTo` only set by the intro, so false with the intro off. |
| 8ee5d6b | 20 | `socialChatter` returns while `introHush()` | Placed after the `schedU` odds test (a hash, no `R()`), before anything is drawn; `CHATTER_AT` untouched. Off with the intro off. |
| ee48072 | 11 | floor tap ends beside a standing person (`tapBeside`) | Ungated, `typeof` guarded; `playerGo` gets the same tile shape `[i,j]`. No `R()`. cadet_test's taps identical. |
| 5cb3aad | 18 | beam goals carry `beam: true` | Adds a field only; `item` kept, so `tradGoalHere` and the beam tap are unchanged. |
| c56c37c | 15b | `ixGoalWorld` honours `beam`; arrow at `w.y` | `ixGoalWorld` result gains an optional `y` only for beam goals; every caller (ixFrame, trkDoneCheck, section 25's devmodeTake/devmodeMove) reads x, z and ignores y. Falls back to `item` off Deck 5. |
| 1f91e90 | 15b | `trkDoneCheck` (in the slot); Tracked items gain `span`; goals gain `trkFrom`/`trkTo` | Additive fields; `trkItems` readers (Tracked, devmodeAppt) unaffected. `span` uses the same absolute minutes as `shipNow()`. No-op unless you tracked something (IX_GOAL is not saved). |
| 55d9a69 | 15 | `shuffleable`: a following escort steps aside even while talking | Only agents with `esc` `follow|`; talk taps stop the player, so no shuffle during a panel. |
| 25248b9 | 15 + words | `t:devwork` tip: a long work step under way, days 1-7, `sure` | Test is inside `teachTry`; every WORK_ACTS kind runs through the act runner with `def.mins`/`done`. Words baked. |

Notes for PR2 and the lead:
- The patch plan's batch C row says "intro only", but #11 (`trkDoneCheck`), #12 (`shuffleable`), #13 (days 1-7) and #17's tap (`tapBeside`) act in normal play too. All are proven identical in the test URLs; whether they should reach beyond the arrival week is a scope call for PR2, not an owner issue.
- Optional (15b, `trkDoneCheck`): tracking something while you're already in its room (a "Now" item, or a place) clears it on the next frame, so the Track tap seems to do nothing. If wanted: in `trkDoneCheck`, remember whether you were already there on its first look (`g.trkSeen`) and clear only once you've arrived from elsewhere, or at `trkTo`.

## 2. PB, claude/patch-b 2e517ff: batch D (2026-10-20)

**Verdict: PASS.** check_fast on 2e517ff, run alone: **QUICK CHECK OK in 211 s**.

### Hook 1d8d606 (section 4b, the toilet stall kit) → `stallCapAdd(g)` (section 14's slot)
- Load order: the kit runs inside `place()` at deck build, after `STALL_CAP` (a load-time const) exists; `stallCapAdd` is a hoisted function declaration, and the call is `typeof` guarded.
- Shared kit at load: one `BoxGeometry` and one `std()` material (colour through `col()`), no `R()`. Made before any deck's watermark, so `unloadDeck` never frees it.
- Shapes: `toiletStall` still returns `{ w, d, tall: true }`; the cap is a `noMerge` child (mergeMeshes skips it), raycast off, no shadows.
- No coplanar surfaces: the cap (.13 x .06 x .04, z .54-.58) encloses the green light (.12 x .05 x .02, z .545-.565); its back is inside the door (z .50-.55).
- Draw calls: +1 per taken stall in view, hidden otherwise. Fine on a phone.

### #10 as performance owner (walkGap, walkLaneStep, LIFT_OUT)
- `walkGap` runs once per walking crew member and loops over the deck's crew: walkers x crew, about 900 cheap tests a frame at Sunday dinner. After 2e517ff, far walkers are rejected with four comparisons before any square root. Timed on paper (30 walkers, 30 crew): **about 5 microseconds a frame** on this machine; a phone 5-10x slower is still well under 0.1 ms of a 16.7 ms frame. **Acceptable; no cheaper approach needed.** If the crew count ever grows a lot, the next step would be one list of walkers per frame (skip the non-walkers once, not per walker).
- `walkLaneStep` now looks up doorways once a step (`laneAt`), so no strings are made each frame. No `R()`: the lane comes from `idHash`. Only the drawn body moves (`lx`, `lz`), so stuck checks, doors and bumps still use the tile position. `LIFT_OUT` is cleared with the deck crew; the planner never reads it.

### PB's cadet_test claim, checked
cadet_test integration vs 2e517ff: DIFFERENCES FOUND (expected). Split with a copy of 2e517ff with #10 and #8 switched off (walkGap 1, no lane, liftOutOk true, no cap):
- **#10 + #8 alone** (copy vs 2e517ff): crew drawn positions shift in every shot; the taps are the same in both. The crew-hidden shot g_nocrew differs only in Oona's speech bubble, which follows her drawn lane.
- **#7 + #9 alone** (integration vs the copy): the plans change (as PB says), so the crew are elsewhere. The scripted tap 1 (450, 380) now lands on **Pell**: his chat panel opens and you don't walk, so taps 2-4, the steering shots and the end state (room, memory counts) all follow from that. Seen in i_tap1's shot. g_nocrew's other differences are the washroom's light and fade, with crew now using the stalls (#9).
- So the claim holds: every difference comes from the planned crew changes (#7, #9) or the drawn lane (#10); none comes from the hook.

## 3. PA, claude/patch-a ffd8ed7: section 10 hooks 155f0d4 + 35e425a, section 15b 50fe32b (2026-10-20)

**Verdict: PASS**, with one recommended fix (below). cadet_test integration (5d6ee1c) vs ffd8ed7, run alone: **ALL IDENTICAL**. check_fast alone: **QUICK CHECK OK in 207 s**.

- **155f0d4 + 35e425a (section 10, `escortStep`).** Its inputs and result are unchanged (`(dt, e)`, returns true). `escBeside` (section 21) moves a non-follow escort's goal off your tile; the ESC_GAP stop now applies only to wait-mode walks whose path ends within 2.4 m of you (`escToYou`), never to `lead`, never to a line walker (`e.after`). Run time only, `typeof` guarded; `ESC_GAP`/`escToYou` are load-time consts in section 21, read only from frames. No `R()`, no draw calls. Follow mode is unchanged in practice: it already stops at `ESC_NEAR` (2 tiles), beyond the .9 m gap. The scenes it reaches outside the intro: crewScene waits (section 10's, the promotion cake's Brennan). The friend seek (`@seek`) is a separate branch, untouched.
- **Recommended fix (section 10):** a wait-mode escort whose path to a tile 1-2 m beyond you goes past you (you standing in a doorway between him and his tile) now stands .9 m short for as long as you stay put. Before, he walked through you. It frees itself when you move, so it's not a lock, but a player waiting for the scene may just stand there. A cheap guard: hold the gap stop at most ~2 s, then walk on as before, e.g. `... && nd < ESC_GAP && nd < dist && (this.gapT = (this.gapT || 0) + dt) < 2) { ...stand... } else { this.gapT = 0; ...walk... }` (gapT resets once he's walking).
- **50fe32b (section 15b slot, `trkDoneCheck`).** A tracked place now clears only after you've been away from it since tracking it (`g.trkAway`, a field on IX_GOAL, not saved); timed items unchanged. This answers my part 1 suggestion for places. Off another deck the check returns early, so you're counted as away once you reach its deck: fine.

## 4. PB, claude/patch-b d3b028f: batch F hooks 22c4442 (17), 9e34423 (24), machine_check's range (2026-10-20)

**Verdict: PASS.** check_fast on d3b028f, alone: **QUICK CHECK OK in 218 s**. career_check alone: **CAREER CHECK OK**.

- **22c4442 (17, `openJobs`)**: same inputs, same result shape; only `mins` changes, and only for `'you'` on service/repair/overhaul jobs (`JOB_TYPES[kind].work * JOB_PACE * tier`), matching section 15's `jobMins` base. The crew's numbers are unchanged. Its only reader is section 15b's job board (display). It still leaves out `careerSpeed` and the log's 10%, as it did before. `typeof` guarded, run time only.
- **9e34423 (24, `WORK_BANDS` Tier 1 'relied' 40 -> 48): a sensible change of the target, not hiding a problem.** The design target is a steady player reaching "Relied on" by the end of Day 8, a very busy one not before Day 5. #16 makes your machine jobs 1/.72 = 1.39x as quick, so XP per hour rises by about that much; 48 is 1.2x, so nobody reaches it later than before the patch. Measured: busy 43 on Day 4, 59 on Day 5 (5 under the line on Day 4); steady 55 on Day 8, "Relied on" in time for Day 9's Tier 2 test job (which needs it), passed on Day 9. It also clears backlog row 12 (career_check's busy-before-Day-5 failure, already red on integration). Tier 2's bands are untouched.
  - Note for the user/PR2, not blocking: the lower Tier 1 bands (steady 8, reliable 18, trusted 30) now come about 1.4x sooner too (busy player "trusted" on Day 3). Nothing tests them; whether they should scale is a design call.
- **machine_check 3-6 -> 3-8 jobs a shift day: sensible.** 6 x 1.39 is about 8.3, so 8 is the old ceiling at the new pace (the plan's "about a third more where the board has work"). Measured 6.2 a day (56 jobs on 9 shift days). The checks that would catch a real problem are unchanged and pass: repairs 49% (40-60%), lowest ship health 94.5 (85+), nothing broken, every repair has a cause, the same twice.
