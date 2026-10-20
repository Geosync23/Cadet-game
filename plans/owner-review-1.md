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
