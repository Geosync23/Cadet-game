# Handover: seat E5 (E2's seat, mechanic engineer), Pillar 5 Step 4

Written 2026-10-19 by E5 (session_01QsZymCraDjLzVDooLvigNk). Read `plans/handover-mech-e2.md` first (everything E2 built,
gotchas, how to test); this note adds only what E5 did.

## Branch and builds
- `claude/mech-incidents`. E2's last: 0.51.12 (93fbdb5: `playerRigRebuild` in 24l, a leak +1 in all). E5: 0.51.13 (60a418f),
  0.51.14 (2c513e6). Next build: 0.51.15.

## What E5 built
- **0.51.13:** `playerRigRebuild` (24l, E5 owns it: lead 17's call) also remakes your stand-in at a place (`recBody(ACT)`).
  mech_check `ff` proves the pin is merged into the chest (16 meshes before and after: no extra draw call), back after a
  reload, gone with no grade; `m13` checks a leak pays +1 in all and `m15` that right first time pays +2, only where 24
  core's side-job turn-in (`WORKS_SIDE_KINDS`) is in.
- **0.51.14, M8 stage 2 team parts (24h):** `TEAM_PARTS`, `TEAM_PARTS_DAY` 18, `TEAM_PARTS_LATE` 10, `teamT0`, `teamPartsN`,
  `teamParts(j, t)` (at `teamPost`), `teamPartsCheck(j, t, skip)` (at `teamTick`'s start). Uses E1's `manifestRun`,
  `manifestRunDelivered`, `manifestRunEnd` (hook register). Saved: `j.partsRun`, `j.partsLate`, `side.parts`.
  mech_check `tparts` (only with manifestRun) and `side.parts` in the `side` save round trip.

## Loose ends
- **Rewiring right first time pays 1, not 2, on a merge with E1** (E1's flat side pay `WORK_XP[kind] ?? 1` ignores
  `j.rightFirst`; 0.51.11 dropped 24q's own +1). One line in 24 core's turn-in fixes it:
  `xp = side ? (WORK_XP[kind] ?? 1) + (right ? 1 : 0) : ...`. Asked of lead 17 (E1 inactive). mech_check m15 FAILs on
  merged builds until it's in.
- R5's verdicts on 6714448 (0.51.11), 93fbdb5, 60a418f, 2c513e6: asked, not yet posted.

## Trial merge with E1 (how E5 did it)
Worktree from HEAD, `git merge origin/claude/mech-rounds`: the two build-number lines in the game (take ours) and two
mech_check blocks conflict (keep both; in the EXTRA loop take ours' line plus E1's side/mrun lines).

## Open questions for the user
- The parts each team job asks for are E5's pick (two from STOCK per job); easy to change in `TEAM_PARTS`.
