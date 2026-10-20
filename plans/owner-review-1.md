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
