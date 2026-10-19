# Handover: rec engineer B2 (RB2), the rec deck's works, rounds 3-4

**Role:** RB in `plans/brief-recdeck.md` (claude/lead-pillar1), after RB (see `plans/handover-rec-rb.md` for rounds 1-2). Reports to lead 18 (session_01CBur9nrJ411pFkHopF96RL). Session: session_018cunWUG3yeKN8NzCPdRbTy.
**Branch:** `claude/rec-works`, series 0.84.x. Reviewer R7 session_01HCwvy5w432bhz41UYxHYwq; build master BM8 session_01YGy9FDmcbkySMJpVPYJaAo; RA session_012mZrFQrGpbNeNWuRg4Bxyp; W3 session_01LbftuR6cNubo3CvAScTuv5.

## Builds
| Build | Hash | What |
| --- | --- | --- |
| 0.84.8 | 0ab43cd | `recShow(state)` (null/film/talk/allhands/talent): house lights (applyLight, only in room 'A'), the screen cloth on a noMerge pivot, three stage light pools; W3's rec.shut.* and trace.pool.drip/.up keys. |
| 0.84.9 | 11fb633 | Poses sing/juggle/bow/address; crew moves `perform { act, len }` and `address {}`; `recCrewBalls`; mic stand; piano side-on + bench; phone budget measured. |
| 0.84.10 | f319ab3 | device_check/machine_check loop over DECK_ORDER. |
| 0.84.11 | 32f7710 | `REC_DECK = true` (merge LAST, after RA and W3). |

## Interfaces given
- RA: `recShow(state)`, idempotent, call every tick; stage spots (room 'A', y .55): lectern [9.3, 7.3] w, mic [9.3, 9.6] w, juggler ~[9.3, 10.2] w, piano bench [9.0, 11.25] s.
- W3: wired keys; `symptom.pool` -> use `trace.symptom.pool` (S2's traceTitle reads it).

## Gotchas
- `mergeMeshes` checks `userData.noMerge` on each MESH, not its group: anything that moves needs it on the mesh itself.
- Crowd bodies standing on a place with y >= .3 keep their root on the floor (the legs stand on the stage): add `pos.y - root.y` for props in world space.
- `REC_POOLS/REC_SHOWS/REC_SHOW` live by `REC_DECK` at the top: a save on the rec deck builds Deck 7 before section 8c loads.
- machineFx on R is 4 meshes only while R has no 'shower' places.

## Testing
Own CADET_WORK per run (scratch `w*/` with `test/` and a `three` link). Probes used: auditorium shows and stage poses at 390x844, crowd bodies placed by hand (`crowd.add(rosterSpec(ROSTER[i]))` + `h.set`).

## Loose ends
- Review fixes from R7 on 0.84.4-0.84.11.
- Phone budget measured with hand-placed crowds; re-measure once RA's crew places are merged (day_check's draw calls).
